# AI-Assisted Security Monitoring in 5G-Enabled UAS Wireless Networks

Reproducibility repository supporting the manuscript **“AI-Assisted Security Monitoring in 5G-Enabled UAS Wireless Networks: Run-Wise Validation and Cross-Domain Transfer”**, prepared for Springer *Wireless Networks* and the collection **AI-powered Secure and Smart Wireless Networks**.

**Authors:** Olga Torstensson; Basudeo Shrestha; Dmytro Prokopovych-Tkachenko; Oleksandr Galushchenko; Raul Ceretta Nunes; Edison Pignaton de Freitas.

## Evidence and headline results

The manuscript evaluates the same ordered 44-column 5G/UAS security-telemetry schema across two evidence levels: a 10,000-row synthetic reference and a 17,779-row co-simulation dataset from 43 independent Gazebo/PX4/ROS 2 + OMNeT++/INET/Simu5G runs.

Publication-facing result anchors in this repository are:

- `results/fair_groupwise_comparison.csv`: matched five-fold mission/run-group validation. All-feature HGB macro-F1 is **0.998 ± 0.001** on the synthetic reference and **0.624 ± 0.057** on co-simulation; traffic+5G HGB reaches **0.626 ± 0.056** on co-simulation.
- `results/cross_domain_transfer_results.csv`: complete RF/HGB zero-shot transfer. Synthetic→co-simulation RF reaches **0.413** macro-F1 with all features and **0.308** with traffic+5G; the latter predicts all target rows as normal.
- `results/distribution_shift_results.csv`: all-row and normal-only KS diagnostics. Normal packet-count KS D is **0.993** and normal API-request-count D rounds to **1.000**.
- `results/window_level_model_metrics.csv`: secondary 70/30 window-level comparison. HGB reaches **0.824** macro-F1 with the full co-simulation feature set and **0.820** with traffic+5G.

Companion Zenodo v2.0.0 DOI: **10.5281/zenodo.22709680**.

The precursor synthetic dataset remains public at DOI **10.5281/zenodo.20825334**.

## Repository structure

```text
analysis/       reproducible analysis and repository-validation scripts
docs/           dataset, reproducibility, and manuscript-artifact alignment notes
results/        publication-facing validation, transfer, shift, and window-level tables
schema/         44-column telemetry schema reference
.github/        GitHub Actions validation workflow
```

Large research data, 43 per-run CSVs, 43 YAML manifests, exact manuscript figures, source co-simulation code, and representative provenance are maintained in the companion **Zenodo v2.0.0** artifact at https://doi.org/10.5281/zenodo.22709680 rather than duplicated in this lightweight GitHub repository.

## Quick repository validation

```bash
python -m pip install -r requirements.txt
python analysis/validate_repository.py
```

## Reproduce manuscript analyses

Download the companion Zenodo v2.0.0 artifact from https://doi.org/10.5281/zenodo.22709680 and place its aggregate datasets at:

```text
data/synthetic_reference/drone_network_telemetry_dataset.csv
data/cosimulation/drone_network_telemetry_cosim.csv
```

Then run:

```bash
python analysis/reproduce_manuscript_analysis.py
```

The script regenerates matched group-wise validation, RF/HGB zero-shot transfer, and KS distribution-shift tables under `analysis_outputs/`.

## Reproducibility boundary

The original co-simulation environment used Ubuntu 24.04, ROS 2 Jazzy, Gazebo Sim 8.11.0, PX4 SITL/x500, OMNeT++ 6.0.1, INET 4.5, and Simu5G 1.2.2. Third-party simulator installations and several gigabytes of regenerable `.vec` and `.mcap` intermediates are not redistributed. The study therefore supports simulation/co-simulation claims, not field- or testbed-validation claims.

## Licensing

Datasets, documentation, metadata, reports, and figures are licensed under **CC BY 4.0**. Original research code is additionally licensed under the **MIT License**. See `LICENSE` and `LICENSE_CODE_MIT`.

## Citation and archival record

Use `CITATION.cff`. The companion archival DOI for version 2.0.0 is **https://doi.org/10.5281/zenodo.22709680**.

Repository: https://github.com/oltoHalmstad/ai-security-monitoring-5g-uas
