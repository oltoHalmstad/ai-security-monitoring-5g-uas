# AI-Assisted Security Monitoring in 5G-Enabled UAS Wireless Networks

Reproducibility repository supporting the manuscript **“AI-Assisted Security Monitoring in 5G-Enabled UAS Wireless Networks: Run-Wise Validation and Cross-Domain Transfer”**, prepared for the Springer *Wireless Networks* collection **AI-powered Secure and Smart Wireless Networks**.

**Authors:** Olga Torstensson; Basudeo Shrestha; Dmytro Prokopovych-Tkachenko; Oleksandr Galushchenko; Raul Ceretta Nunes; Edison Pignaton de Freitas.

## What this repository supports

The study evaluates the same 44-column 5G/UAS security-telemetry schema across two evidence levels: a 10,000-row synthetic reference dataset and a 17,779-row co-simulation dataset generated from 43 independent Gazebo/PX4/ROS 2 + OMNeT++/INET/Simu5G runs.

Key manuscript results include:

- matched five-fold mission/run-group validation: all-feature HGB macro-F1 **0.998 ± 0.001** on the synthetic reference versus **0.624 ± 0.057** on co-simulation;
- traffic + 5G HGB macro-F1 **0.626 ± 0.056** on co-simulation;
- suspicious-event F1 approximately **0.375** under run-wise evaluation;
- zero-shot synthetic → co-simulation RF macro-F1 **0.413** with all non-leaking features;
- reverse co-simulation → synthetic RF macro-F1 **0.234**;
- strong normal-class distribution shift, including KS D ≈ **0.993** for packet count.

The precursor synthetic dataset is publicly archived at DOI **10.5281/zenodo.20825334**.

## Repository structure

```text
analysis/       reproducible analysis and validation scripts
docs/           dataset, experiment and provenance documentation
manifests/      scenario YAML files
results/        run-wise, transfer and distribution-shift results
schema/         44-column telemetry schema
src/            co-simulation orchestration, bridge and validation code
.github/        CI validation workflow
```

Large research data, exact manuscript figures, per-run CSV files, and representative provenance artifacts are intended for the companion **Zenodo v2.0.0** release. This keeps the GitHub repository reviewable while Zenodo provides immutable archival storage and a DOI.

## Quick start

```bash
python -m pip install -r requirements.txt
python analysis/validate_package.py
python analysis/reproduce_manuscript_analysis.py
python analysis/make_key_figures.py
```

The downstream analysis does not require Gazebo/PX4/ROS 2/OMNeT++/INET/Simu5G. Full source co-simulation recreation requires those external tools; versions and boundaries are documented under `docs/`.

## Reproducibility boundary

The original co-simulation environment used Ubuntu 24.04, ROS 2 Jazzy, Gazebo Sim 8.11.0, PX4 SITL/x500, OMNeT++ 6.0.1, INET 4.5, and Simu5G 1.2.2. Third-party simulator installations and several gigabytes of regenerable `.vec` / `.mcap` intermediates are not redistributed.

## License

Original research materials are released under **Creative Commons Attribution 4.0 International (CC BY 4.0)**. Third-party dependencies retain their own licenses.

## Citation

Use `CITATION.cff`. Repository: https://github.com/oltoHalmstad/ai-security-monitoring-5g-uas

Until the companion Zenodo DOI is reserved, cite the manuscript/repository together with the precursor DOI **10.5281/zenodo.20825334** where relevant.
