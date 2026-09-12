"""Reproduce the primary robustness analyses used in the Wireless Networks manuscript.

The two aggregate datasets are distributed in the published companion Zenodo v2.1.0
artifact (DOI: 10.5281/zenodo.22722487), not in this lightweight GitHub repository.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, f1_score, precision_recall_fscore_support
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder

ROOT = Path(__file__).resolve().parents[1]
SYN = ROOT / "data/synthetic_reference/drone_network_telemetry_dataset.csv"
COS = ROOT / "data/cosimulation/drone_network_telemetry_cosim.csv"
OUT = ROOT / "analysis_outputs"
OUT.mkdir(exist_ok=True)

traffic = ["packet_count","byte_count","packets_per_second","throughput_kbps","latency_ms","jitter_ms","packet_loss_rate","retransmission_rate","connection_duration_sec"]
# Historical artifact label: "traffic+5g". The context bundle below also includes
# generic source/destination ports and protocol, so it is not a pure 5G-only ablation.
ctx = ["source_port","destination_port","protocol","network_slice_id","cell_id","signal_quality_dbm","handover_event","handover_count"]
exclude = {"timestamp","organization_id","fleet_id","drone_id","mission_id","source_ip","destination_ip","session_id","attack_type","attack_stage","severity","recommended_response","anomaly_score","incident_label"}
classes = ["normal","suspicious","malicious"]


def rf_pipe(df, features):
    num = [c for c in features if pd.api.types.is_numeric_dtype(df[c])]
    cat = [c for c in features if c not in num]
    pre = ColumnTransformer([
        ("num", SimpleImputer(strategy="median"), num),
        ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")), ("enc", OneHotEncoder(handle_unknown="ignore"))]), cat),
    ])
    return Pipeline([("pre", pre), ("model", RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1))])


def hgb_pipe(df, features):
    num = [c for c in features if pd.api.types.is_numeric_dtype(df[c])]
    cat = [c for c in features if c not in num]
    pre = ColumnTransformer([
        ("num", SimpleImputer(strategy="median"), num),
        ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")), ("enc", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1))]), cat),
    ])
    return Pipeline([("pre", pre), ("model", HistGradientBoostingClassifier(random_state=42, max_iter=100))])


def group_eval(name, df):
    all_features = [c for c in df.columns if c not in exclude]
    sets = {"traffic+5g": traffic + ctx, "all": all_features}
    cv = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)
    rows = []
    for set_name, features in sets.items():
        for model_name, maker in [("RF", rf_pipe), ("HGB", hgb_pipe)]:
            fold, yt, yp = [], [], []
            for tr, te in cv.split(df[features], df.incident_label, df.mission_id):
                model = maker(df.iloc[tr], features)
                model.fit(df.iloc[tr][features], df.iloc[tr].incident_label)
                pred = model.predict(df.iloc[te][features])
                fold.append((accuracy_score(df.iloc[te].incident_label, pred), f1_score(df.iloc[te].incident_label, pred, average="macro", zero_division=0)))
                yt.extend(df.iloc[te].incident_label)
                yp.extend(pred)
            pr, rc, fc, sup = precision_recall_fscore_support(yt, yp, labels=classes, zero_division=0)
            row = {"dataset": name, "feature_set": set_name, "model": model_name,
                   "accuracy_mean": np.mean([x[0] for x in fold]), "accuracy_sd": np.std([x[0] for x in fold], ddof=1),
                   "macro_f1_mean": np.mean([x[1] for x in fold]), "macro_f1_sd": np.std([x[1] for x in fold], ddof=1)}
            for i, cls in enumerate(classes):
                row.update({f"{cls}_precision": pr[i], f"{cls}_recall": rc[i], f"{cls}_f1": fc[i], f"{cls}_support": int(sup[i])})
            rows.append(row)
    return rows


def transfer(train_name, train, test_name, test):
    all_features = [c for c in train.columns if c not in exclude]
    sets = {"traffic": traffic, "traffic+5g": traffic + ctx, "all": all_features}
    rows = []
    for set_name, features in sets.items():
        for model_name, maker in [("RF", rf_pipe), ("HGB", hgb_pipe)]:
            model = maker(train, features)
            model.fit(train[features], train.incident_label)
            pred = model.predict(test[features])
            pr, rc, fc, sup = precision_recall_fscore_support(test.incident_label, pred, labels=classes, zero_division=0)
            row = {"direction": f"{train_name}_to_{test_name}", "feature_set": set_name, "model": model_name,
                   "accuracy": accuracy_score(test.incident_label, pred), "macro_f1": f1_score(test.incident_label, pred, average="macro", zero_division=0)}
            for i, cls in enumerate(classes):
                row.update({f"{cls}_precision": pr[i], f"{cls}_recall": rc[i], f"{cls}_f1": fc[i], f"{cls}_support": int(sup[i])})
            rows.append(row)
    return rows


if not SYN.exists() or not COS.exists():
    raise SystemExit("Companion datasets not found. Download the published Zenodo v2.1.0 artifact (DOI: 10.5281/zenodo.22722487) and place the aggregate CSVs under data/ as documented in docs/REPRODUCIBILITY.md.")

syn = pd.read_csv(SYN)
cos = pd.read_csv(COS)
pd.DataFrame(group_eval("synthetic", syn) + group_eval("cosim", cos)).to_csv(OUT / "fair_groupwise_comparison_reproduced.csv", index=False)
pd.DataFrame(transfer("synthetic", syn, "cosim", cos) + transfer("cosim", cos, "synthetic", syn)).to_csv(OUT / "cross_domain_transfer_results_reproduced.csv", index=False)

features = ["packet_count","byte_count","packets_per_second","throughput_kbps","latency_ms","jitter_ms","packet_loss_rate","retransmission_rate","connection_duration_sec","signal_quality_dbm","command_channel_activity","api_request_count","failed_connection_attempts"]
rows = []
for subset in ["all", "normal"]:
    a = syn if subset == "all" else syn[syn.incident_label == "normal"]
    b = cos if subset == "all" else cos[cos.incident_label == "normal"]
    for feature in features:
        x = a[feature].dropna().astype(float)
        y = b[feature].dropna().astype(float)
        D, p = ks_2samp(x, y)
        rows.append({"subset": subset, "feature": feature, "synthetic_median": x.median(), "cosim_median": y.median(), "ks_D": D, "ks_p": p})
pd.DataFrame(rows).to_csv(OUT / "distribution_shift_results_reproduced.csv", index=False)
print("Wrote", OUT)
