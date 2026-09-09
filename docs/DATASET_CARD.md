# Dataset card

## Purpose

The artifact is designed to evaluate AI-assisted cyber-incident monitoring in 5G-enabled unmanned aerial system (UAS) wireless networks under a controlled transition from synthetic telemetry to measurement-derived co-simulation telemetry.

## Data resources

| Resource | Rows | Columns | Grouping |
|---|---:|---:|---|
| Synthetic reference | 10,000 | 44 | synthetic `mission_id` |
| Co-simulation aggregate | 17,779 | 44 | 43 complete runs |

Co-simulation labels: 15,247 normal; 912 suspicious; 1,620 malicious.

## Scenario families

- **Benign:** baseline plus parameter sweeps for speed, duration, drone count, cell count, background load, wireless condition, slice configuration, hover, and aggregation window.
- **Suspicious:** handover, authentication degradation, retries, and dropout without a malicious source.
- **Malicious:** denial of service, session hijacking, identity theft, control-protocol attack, lateral movement, and network-application/API attack, including intensity and timing variants.

## Intended uses

- run-wise intrusion-detection evaluation;
- feature-context ablation for traffic, 5G context, and security indicators;
- synthetic-to-co-simulation domain-transfer analysis;
- reproducibility exercises for wireless-network security research.

## Out-of-scope claims

The data are simulation/co-simulation evidence, not field data. The artifact does not establish operational detector effectiveness, real-RF robustness, or deployment safety. Response fields are recommendations and were not executed as containment actions in the current study.
