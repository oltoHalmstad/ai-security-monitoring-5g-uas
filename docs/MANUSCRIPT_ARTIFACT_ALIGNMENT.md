# Manuscript-artifact alignment

Manuscript: **AI-Assisted Security Monitoring in 5G-Enabled UAS Wireless Networks: Run-Wise Validation and Cross-Domain Transfer**

Artifact: **5G/UAS Wireless-Security Co-Simulation Dataset and Reproducibility Artifact for AI-Assisted Security Monitoring**, version 2.1.0

Published companion Zenodo DOI: **10.5281/zenodo.22722487**

Public Zenodo record: https://zenodo.org/records/22722487

Previous published artifact version: **2.0.0**, DOI **10.5281/zenodo.22709680**

Publication repository: https://github.com/oltoHalmstad/ai-security-monitoring-5g-uas

## Alignment checks

- Creator order matches the manuscript and Zenodo metadata: Olga Torstensson; Basudeo Shrestha; Dmytro Prokopovych-Tkachenko; Oleksandr Galushchenko; Raul Ceretta Nunes; Edison Pignaton de Freitas.
- Both datasets use the same ordered 44-column telemetry schema.
- Co-simulation dimensions match the manuscript: 17,779 rows, 43 runs, 15,247 normal, 912 suspicious, 1,620 malicious.
- `results/fair_groupwise_comparison.csv` supports Table 7 and Fig. 6.
- `results/cross_domain_transfer_results.csv` contains both RF and HGB results; Table 8 and Fig. 7 summarize the primary RF transfer comparison while the text reports the HGB all-feature and combined-bundle results.
- `results/distribution_shift_results.csv` supports Fig. 8, including normal API-request-count KS D approximately 1.000 and packet-count D approximately 0.993.
- `results/window_level_model_metrics.csv` supports the secondary 70/30 results in Section 4.4.
- The published Zenodo v2.1.0 package contains exact copies of all 9 manuscript figures under `figures/manuscript/`.
- Primary Zenodo license is CC BY 4.0; original research code is additionally MIT-licensed.
- The manuscript, published Zenodo v2.1.0 package metadata, `CITATION.cff`, and repository documentation use the same companion DOI: **10.5281/zenodo.22722487**.
- Version 2.1.0 is a manuscript/artifact alignment update; the scientific data rows and headline result values are unchanged from version 2.0.0.
