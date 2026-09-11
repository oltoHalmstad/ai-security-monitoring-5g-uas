"""CI validation for the publication-facing 5G/UAS reproducibility repository."""
from pathlib import Path
import csv
import json
import math
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "README.md", "CITATION.cff", ".zenodo.json", "LICENSE", "LICENSE_CODE_MIT", "requirements.txt",
    "analysis/validate_repository.py", "analysis/reproduce_manuscript_analysis.py",
    "docs/REPRODUCIBILITY.md", "docs/DATASET_CARD.md", "docs/MANUSCRIPT_ARTIFACT_ALIGNMENT.md",
    "results/fair_groupwise_comparison.csv", "results/cross_domain_transfer_results.csv",
    "results/distribution_shift_results.csv", "results/window_level_model_metrics.csv", "schema/schema_reference.json",
]
RESULT_TABLES = [
    "results/fair_groupwise_comparison.csv", "results/cross_domain_transfer_results.csv",
    "results/distribution_shift_results.csv", "results/window_level_model_metrics.csv",
]
EXPECTED_AUTHORS = [
    "Torstensson, Olga", "Shrestha, Basudeo", "Prokopovych-Tkachenko, Dmytro",
    "Galushchenko, Oleksandr", "Nunes, Raul Ceretta", "de Freitas, Edison Pignaton",
]
errors = []

def fail(message): errors.append(message)
def approx(value, expected, tol=5e-4):
    try: return math.isclose(float(value), expected, abs_tol=tol)
    except (TypeError, ValueError): return False

def dict_rows(rel):
    path = ROOT / rel
    if not path.is_file(): return []
    with path.open(newline="", encoding="utf-8") as h: return list(csv.DictReader(h))

for rel in REQUIRED_FILES:
    if not (ROOT / rel).is_file(): fail(f"missing required file: {rel}")

for rel in RESULT_TABLES:
    path = ROOT / rel
    if not path.is_file(): continue
    with path.open(newline="", encoding="utf-8") as h: rows = list(csv.reader(h))
    if len(rows) < 2: fail(f"result table has no data rows: {rel}")
    elif len(rows[0]) != len(set(rows[0])): fail(f"result table has duplicate header fields: {rel}")

schema_path = ROOT / "schema/schema_reference.json"
if schema_path.is_file():
    try: schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except Exception as exc: fail(f"invalid schema JSON: {exc}")
    else:
        columns = schema.get("columns")
        if not isinstance(columns, list) or len(columns) != 44: fail("schema must contain 44 ordered columns")
        elif len(columns) != len(set(columns)): fail("schema contains duplicate column names")
        elif columns[-1] != "incident_label": fail("schema final column must be incident_label")
        if schema.get("categorical_values", {}).get("incident_label") != ["normal", "suspicious", "malicious"]:
            fail("schema incident_label values are incorrect")
        if schema.get("provenance", {}).get("reference_doi") != "10.5281/zenodo.20825334":
            fail("schema precursor DOI mismatch")

zenodo = None
if (ROOT / ".zenodo.json").is_file():
    try: zenodo = json.loads((ROOT / ".zenodo.json").read_text(encoding="utf-8"))
    except Exception as exc: fail(f"invalid .zenodo.json: {exc}")
    else:
        if zenodo.get("license") != "CC-BY-4.0": fail("Zenodo primary license must be CC-BY-4.0")
        if str(zenodo.get("version")) != "2.0.0": fail("Zenodo version must be 2.0.0")
        if [c.get("name") for c in zenodo.get("creators", [])] != EXPECTED_AUTHORS: fail("Zenodo creator order mismatch")

citation = None
if (ROOT / "CITATION.cff").is_file():
    try: citation = yaml.safe_load((ROOT / "CITATION.cff").read_text(encoding="utf-8"))
    except Exception as exc: fail(f"invalid CITATION.cff: {exc}")
    else:
        cff_names = [f"{a.get('family-names')}, {a.get('given-names')}" for a in citation.get("authors", [])]
        if cff_names != EXPECTED_AUTHORS: fail("CITATION.cff author order mismatch")

if isinstance(zenodo, dict) and isinstance(citation, dict):
    if zenodo.get("title") != citation.get("title"): fail("artifact title mismatch between .zenodo.json and CITATION.cff")
    if zenodo.get("license") != citation.get("license"): fail("license mismatch between .zenodo.json and CITATION.cff")
    if str(zenodo.get("version")) != str(citation.get("version")): fail("version mismatch between .zenodo.json and CITATION.cff")

license_text = (ROOT / "LICENSE").read_text(encoding="utf-8") if (ROOT / "LICENSE").is_file() else ""
mit_text = (ROOT / "LICENSE_CODE_MIT").read_text(encoding="utf-8") if (ROOT / "LICENSE_CODE_MIT").is_file() else ""
if "CC BY 4.0" not in license_text or "MIT" not in license_text: fail("dual-license notice incomplete")
if "MIT License" not in mit_text: fail("MIT code license missing")

for n, raw in enumerate((ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines(), 1) if (ROOT / "requirements.txt").is_file() else []:
    line = raw.strip()
    if line and not line.startswith("#") and "==" not in line: fail(f"requirements line {n} is not pinned: {line}")

group = dict_rows("results/fair_groupwise_comparison.csv")
r = next((x for x in group if x.get("dataset") == "cosim" and x.get("feature_set") == "traffic+5g" and x.get("model") == "HGB"), None)
if not r or not approx(r.get("macro_f1_mean"), 0.6259): fail("co-sim traffic+5g HGB result mismatch")
r = next((x for x in group if x.get("dataset") == "synthetic" and x.get("feature_set") == "all" and x.get("model") == "HGB"), None)
if not r or not approx(r.get("macro_f1_mean"), 0.9980): fail("synthetic all-feature HGB result mismatch")

transfer = dict_rows("results/cross_domain_transfer_results.csv")
if len(transfer) != 12 or {r.get("model") for r in transfer} != {"RF", "HGB"}: fail("transfer table must contain 12 RF/HGB rows")
r = next((x for x in transfer if x.get("direction") == "synthetic_to_cosim" and x.get("feature_set") == "all" and x.get("model") == "RF"), None)
if not r or not approx(r.get("macro_f1"), 0.4125286809): fail("synthetic-to-cosim RF all-feature result mismatch")

shift = dict_rows("results/distribution_shift_results.csv")
r = next((x for x in shift if x.get("subset") == "normal" and x.get("feature") == "packet_count"), None)
if not r or not approx(r.get("ks_D"), 0.9928264093): fail("normal packet-count KS result mismatch")
r = next((x for x in shift if x.get("subset") == "normal" and x.get("feature") == "api_request_count"), None)
if not r or not approx(r.get("ks_D"), 0.9996725606): fail("normal API-request-count KS result mismatch")

window = dict_rows("results/window_level_model_metrics.csv")
if len(window) != 15: fail("window-level model table must contain 15 rows")
r = next((x for x in window if x.get("model") == "gradient boosting" and x.get("dataset") == "Co-simulation" and x.get("feature_set") == "full feature set"), None)
if not r or not approx(r.get("macro_f1"), 0.8239): fail("window-level HGB result mismatch")

for rel in ("README.md", "docs/REPRODUCIBILITY.md"):
    path = ROOT / rel
    if path.is_file():
        for script in re.findall(r"\bpython(?:3)?\s+([A-Za-z0-9_./-]+\.py)\b", path.read_text(encoding="utf-8")):
            if not (ROOT / script).is_file(): fail(f"{rel} references missing script: {script}")

if errors:
    print("REPOSITORY VALIDATION: FAILED")
    for error in errors: print("-", error)
    sys.exit(1)
print(f"REPOSITORY VALIDATION: PASSED ({len(REQUIRED_FILES)} required files checked; manuscript result anchors aligned)")
