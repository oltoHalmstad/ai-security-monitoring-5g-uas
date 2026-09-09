"""Lightweight CI validation for the GitHub publication-facing repository."""
from pathlib import Path
import csv, json, sys

ROOT = Path(__file__).resolve().parents[1]
required = [
    'README.md','CITATION.cff','requirements.txt',
    'results/fair_groupwise_comparison.csv',
    'results/cross_domain_transfer_results.csv',
    'results/distribution_shift_results.csv',
    'docs/REPRODUCIBILITY.md','docs/DATASET_CARD.md',
    'schema/schema_reference.json'
]
errors = []
for rel in required:
    if not (ROOT/rel).is_file():
        errors.append(f'missing {rel}')

for rel in ['results/fair_groupwise_comparison.csv','results/cross_domain_transfer_results.csv','results/distribution_shift_results.csv']:
    p = ROOT/rel
    if p.is_file():
        with p.open(newline='', encoding='utf-8') as f:
            rows = list(csv.reader(f))
        if len(rows) < 2:
            errors.append(f'empty result table {rel}')

p = ROOT/'schema/schema_reference.json'
if p.is_file():
    try:
        json.loads(p.read_text(encoding='utf-8'))
    except Exception as exc:
        errors.append(f'invalid schema JSON: {exc}')

if errors:
    print('REPOSITORY VALIDATION: FAILED')
    for e in errors:
        print('-', e)
    sys.exit(1)
print('REPOSITORY VALIDATION: PASSED')
