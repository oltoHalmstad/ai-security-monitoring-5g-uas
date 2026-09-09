# Reproducibility guide

## Publication-facing GitHub repository

This repository contains the analysis code, result tables, schema and documentation needed to review the manuscript's robustness claims. The complete 17,779-row co-simulation dataset, 43 per-run CSVs, all 43 YAML manifests, exact manuscript figures and representative end-to-end provenance artifacts are packaged for the companion Zenodo v2.0.0 release.

## Environment

The downstream analysis uses Python 3.12 with the packages in `requirements.txt`.

```bash
python -m pip install -r requirements.txt
python analysis/validate_repository.py
```

## Full analysis

After downloading the companion Zenodo data into the paths documented in the release package, run:

```bash
python analysis/reproduce_manuscript_analysis.py
python analysis/make_key_figures.py
```

The analysis uses complete mission/run groups for validation and excludes identifiers and post-label fields that would leak class information.

## Source co-simulation

The original environment used Ubuntu 24.04, ROS 2 Jazzy, Gazebo Sim 8.11.0, PX4 SITL/x500, OMNeT++ 6.0.1, INET 4.5, and Simu5G 1.2.2. Third-party simulator installations and large regenerable `.vec`/`.mcap` intermediates are not redistributed.

## Expected dataset dimensions

- synthetic reference: 10,000 rows × 44 columns;
- co-simulation aggregate: 17,779 rows × 44 columns;
- 43 independent co-simulation runs;
- class totals: 15,247 normal, 912 suspicious, 1,620 malicious.
