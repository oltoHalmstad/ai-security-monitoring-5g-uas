"""CI validation for the publication-facing reproducibility repository."""
from pathlib import Path
import csv
import json
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "CITATION.cff",
    ".zenodo.json",
    "requirements.txt",
    "analysis/validate_repository.py",
    "analysis/reproduce_manuscript_analysis.py",
    "docs/REPRODUCIBILITY.md",
    "docs/DATASET_CARD.md",
    "results/fair_groupwise_comparison.csv",
    "results/cross_domain_transfer_results.csv",
    "results/distribution_shift_results.csv",
    "schema/schema_reference.json",
]

RESULT_TABLES = [
    "results/fair_groupwise_comparison.csv",
    "results/cross_domain_transfer_results.csv",
    "results/distribution_shift_results.csv",
]

errors = []


def fail(message: str) -> None:
    errors.append(message)


for rel in REQUIRED_FILES:
    path = ROOT / rel
    if not path.is_file():
        fail(f"missing required file: {rel}")

for rel in RESULT_TABLES:
    path = ROOT / rel
    if not path.is_file():
        continue
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    if len(rows) < 2:
        fail(f"result table has no data rows: {rel}")
        continue
    header = rows[0]
    if not header or any(not cell.strip() for cell in header):
        fail(f"result table has an empty header field: {rel}")
    if len(header) != len(set(header)):
        fail(f"result table has duplicate header fields: {rel}")

schema_path = ROOT / "schema/schema_reference.json"
if schema_path.is_file():
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid schema JSON: {exc}")
    else:
        columns = schema.get("columns")
        if not isinstance(columns, list):
            fail("schema columns must be a list")
        else:
            if len(columns) != 44:
                fail(f"schema must contain 44 columns, found {len(columns)}")
            if len(columns) != len(set(columns)):
                fail("schema contains duplicate column names")
            if columns and columns[-1] != "incident_label":
                fail("schema final column must be incident_label")
        categorical = schema.get("categorical_values", {})
        labels = categorical.get("incident_label") if isinstance(categorical, dict) else None
        if labels != ["normal", "suspicious", "malicious"]:
            fail("schema incident_label values must be normal, suspicious, malicious")
        if schema.get("schema_version") != 1:
            fail("schema_version must be 1")
        provenance = schema.get("provenance")
        if not isinstance(provenance, dict) or not provenance.get("reference_doi"):
            fail("schema provenance.reference_doi is required")

zenodo_path = ROOT / ".zenodo.json"
zenodo = None
if zenodo_path.is_file():
    try:
        zenodo = json.loads(zenodo_path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid .zenodo.json: {exc}")
    else:
        for key in ("title", "creators", "license", "version", "related_identifiers"):
            if not zenodo.get(key):
                fail(f".zenodo.json missing required metadata: {key}")

citation_path = ROOT / "CITATION.cff"
citation = None
if citation_path.is_file():
    try:
        citation = yaml.safe_load(citation_path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid CITATION.cff YAML: {exc}")
    else:
        if not isinstance(citation, dict):
            fail("CITATION.cff must contain a YAML mapping")
        else:
            for key in ("cff-version", "title", "authors", "license", "version"):
                if not citation.get(key):
                    fail(f"CITATION.cff missing required metadata: {key}")

if isinstance(zenodo, dict) and isinstance(citation, dict):
    if str(zenodo.get("version")) != str(citation.get("version")):
        fail("version mismatch between .zenodo.json and CITATION.cff")
    if zenodo.get("license") != citation.get("license"):
        fail("license mismatch between .zenodo.json and CITATION.cff")
    creators = zenodo.get("creators")
    authors = citation.get("authors")
    if isinstance(creators, list) and isinstance(authors, list) and len(creators) != len(authors):
        fail("creator count mismatch between .zenodo.json and CITATION.cff")

requirements_path = ROOT / "requirements.txt"
if requirements_path.is_file():
    for line_number, raw in enumerate(requirements_path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "==" not in line:
            fail(f"requirements.txt line {line_number} is not version-pinned: {line}")

# Keep executable documentation honest: every local Python script mentioned in
# README or the reproducibility guide must exist in this GitHub repository.
for rel in ("README.md", "docs/REPRODUCIBILITY.md"):
    path = ROOT / rel
    if not path.is_file():
        continue
    text = path.read_text(encoding="utf-8")
    for script in re.findall(r"\bpython(?:3)?\s+([A-Za-z0-9_./-]+\.py)\b", text):
        if not (ROOT / script).is_file():
            fail(f"{rel} references missing script: {script}")

if errors:
    print("REPOSITORY VALIDATION: FAILED")
    for error in errors:
        print("-", error)
    sys.exit(1)

print(f"REPOSITORY VALIDATION: PASSED ({len(REQUIRED_FILES)} required files checked)")
