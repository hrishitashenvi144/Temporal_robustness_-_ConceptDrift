# Phase 5 – Temporal Stability of the Feature–Label Relationship

## Goal
Test whether the relationship learned between the audited 215 numeric PRE features and the eight binary DIVE vulnerabilities remains stable over time.

## Data splits (identical to Phase 3B)
- **Historical training**: contracts from 2016‑2021 (train years)
- **Contemporary training**: contracts from 2023 only
- **Test**: contracts from 2024 – never used for training, preprocessing, or threshold selection.
- **v0.8.x subset**: test contracts whose `compiler_family` equals `v0.8.x`.

## Sample counts
- Historical train contracts: 9950
- Contemporary train contracts (2023): 7166
- Test contracts (2024): 4200
- Test contracts v0.8.x: 4118

## Models (unchanged from Phase 3B)
- Logistic Regression (StandardScaler, `class_weight='balanced'`, `random_state=42`, `max_iter=1000`).
- Random Forest (`n_estimators=200`, `class_weight='balanced'`, `random_state=42`).
- Decision threshold fixed at 0.5 for both models.

## Metrics reported per vulnerability
Precision, Recall, F1, PR‑AUC, false positives, false negatives. Macro‑averaged F1 and PR‑AUC are also provided.

## Determinism check
The script runs the full pipeline twice and verifies that the SHA‑256 hashes of the two CSV files and the JSON metadata are identical across runs.

## Outputs
- `phase5_model_comparison.csv` – results on the full 2024 test set.
- `phase5_v08_comparison.csv` – results limited to compiler family `v0.8.x`.
- `phase5_metadata.json` – experiment configuration and sample sizes.
- `PHASE5_README.md` – this document.
