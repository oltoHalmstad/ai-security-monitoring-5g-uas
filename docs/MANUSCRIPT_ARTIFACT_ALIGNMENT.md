# Manuscript-artifact alignment

Manuscript: **AI-Assisted Security Monitoring in 5G-Enabled UAS Wireless Networks: Run-Wise Validation and Cross-Domain Transfer**

Artifact: **5G/UAS Wireless-Security Co-Simulation Dataset and Reproducibility Artifact for AI-Assisted Security Monitoring**, version 2.0.0

Companion Zenodo DOI: **10.5281/zenodo.22709680**

Publication repository: https://github.com/oltoHalmstad/ai-security-monitoring-5g-uas

## Alignment checks

- Creator order matches the manuscript and Zenodo metadata: Olga Torstensson; Basudeo Shrestha; Dmytro Prokopovych-Tkachenko; Oleksandr Galushchenko; Raul Ceretta Nunes; Edison Pignaton de Freitas.
- Both datasets use the same ordered 44-column telemetry schema.
- Co-simulation dimensions match the manuscript: 17,779 rows, 43 runs, 15,247 normal, 912 suspicious, 1,620 malicious.
- `results/fair_groupwise_comparison.csv` matches Table 6 / Fig. 8.
- `results/cross_domain_transfer_results.csv` contains both RF and HGB results; the manuscript reports RF as the primary Table 7 summary and notes the HGB traffic+5G all-normal collapse.
- `results/distribution_shift_results.csv` contains API-request count, supporting the normal-class KS D ≈ 1.000 statement, and packet count KS D ≈ 0.993.
- `results/window_level_model_metrics.csv` supports the secondary 70/30 results used in Section 4.5 / Fig. 7.
- Exact copies of all 10 manuscript figures are distributed in the companion Zenodo package under `figures/manuscript/`; they are not duplicated in this lightweight GitHub repository.
- Primary Zenodo license is CC BY 4.0; original research code is additionally MIT-licensed.
- The manuscript, Zenodo package metadata, `CITATION.cff`, and repository documentation use the same reserved companion DOI: **10.5281/zenodo.22709680**.
