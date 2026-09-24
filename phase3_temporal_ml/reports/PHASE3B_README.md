# Phase 3B – Temporal Robustness Baseline

## Research question
How does a vulnerability detector trained on historically available contracts generalize to later contracts, and how does controlled adaptation using newly available data affect future‑period performance?

## Dataset
DIVE (22,330 contracts, 2016‑2024). Primary feature source: PRE_ProcessedData.csv. Labels: DIVE_Labels.csv (8 binary vulnerability columns).

## Chronological split
- Train (frozen & initial adaptive): 2016‑2021
- Validation: 2022
- Adaptation data: 2023
- Test (final evaluation): 2024

## Feature policy
Audited 215 numeric PRE features (reports/final_feature_list.csv). Excluded identifier, temporal, compiler version, and categorical columns as documented. No additional feature engineering.

## Models
- Logistic Regression (StandardScaler, class_weight='balanced')
- Random Forest (200 trees, class_weight='balanced')
Fixed random_state=42. Threshold 0.5 for binary decisions.

## Metrics
Precision, Recall, F1, PR‑AUC, false positives, false negatives, positive‑label count, sample count. Macro‑averaged F1 and PR‑AUC across the 8 vulnerabilities.

## Leakage controls
Phase 3A opcode fingerprint audit: 22,328 unique fingerprints, 2 exact duplicate families, 4 contracts in duplicate families, 0 cross‑year exact duplicate families. Near‑duplicate/source‑level leakage not assessed.

## Compiler confounding
CompilerVersion is retained only for analysis; major family distributions are reported per temporal cohort.

## Reproducibility
Run the experiment with `python scripts/run_phase3b.py`. The script is deterministic and verifies identical outputs across two runs (hash comparison).

## Outputs
- reports/final_feature_list.csv
- reports/feature_audit.csv
- reports/temporal_cohort_summary.csv
- reports/frozen_model_results.csv
- reports/adaptation_results.csv
- reports/compiler_cohort_summary.csv
- reports/vulnerability_temporal_summary.csv
- reports/experiment_metadata.json
- reports/PHASE3B_README.md
