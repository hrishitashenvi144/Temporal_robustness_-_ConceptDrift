# -*- coding: utf-8 -*-
"""
Phase 5 – Temporal Stability of the Feature–Label Relationship

This script builds on the exact Phase 3B pipeline (same preprocessing, 215‑feature list,
model hyper‑parameters, class weighting, random_state and threshold).
It trains two versions of each model (Logistic Regression and Random Forest):
  * historical – trained on contracts from 2016‑2021
  * contemporary – trained on contracts from 2023 only
Both models are evaluated on the untouched 2024 test set.
A second evaluation restricts the test set to contracts whose compiler family is ``v0.8.x``.
All results are saved under ``phase3_temporal_ml/reports/phase5/``.
The script runs the entire experiment twice and verifies that the SHA‑256 hashes of the
two CSV files and the JSON metadata are identical (deterministic verification).
"""

import json
import hashlib
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    average_precision_score,
    confusion_matrix,
)

# ------------------------------------------------------------
# Paths (mirroring run_phase3b.py)
ROOT = Path("c:/Users/LAPTOPS24/Documents/HRISHITA/CLG/Blockchain/demo1")
WORKSPACE = ROOT / "phase3_temporal_ml"
REPORTS = WORKSPACE / "reports"
SCRIPTS = WORKSPACE / "scripts"

PRE_CSV = ROOT / "phase3_dataset_audit" / "raw" / "Preprocessed" / "PRE" / "PRE_ProcessedData.csv"
LABELS_CSV = ROOT / "phase3_dataset_audit" / "raw" / "Labels" / "DIVE_Labels.csv"
FINAL_FEATURE_LIST = REPORTS / "final_feature_list.csv"

# Output directory for Phase 5
PHASE5_OUT = REPORTS / "phase5"
PHASE5_OUT.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------
# Helper utilities

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def compute_metrics(y_true: np.ndarray, y_scores: np.ndarray, thresh: float = 0.5):
    y_pred = (y_scores >= thresh).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    pr_auc = average_precision_score(y_true, y_scores) if y_true.sum() > 0 else np.nan
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "pr_auc": pr_auc,
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "positive_count": int(y_true.sum()),
        "sample_count": int(len(y_true)),
    }

def macro_average(values):
    vals = [v for v in values if not np.isnan(v)]
    return float(np.mean(vals)) if vals else np.nan

# ------------------------------------------------------------
# Load data (identical to Phase 3B)
print("Loading PRE data…")
pre_df = pd.read_csv(PRE_CSV)
print(f"PRE rows: {pre_df.shape[0]}, columns: {pre_df.shape[1]}")

print("Loading label data…")
labels_df = pd.read_csv(LABELS_CSV)
print(f"Labels rows: {labels_df.shape[0]}, columns: {labels_df.shape[1]}")

print("Merging on contractID…")
merged = pre_df.merge(labels_df, on="contractID", how="inner")
print(f"Merged rows: {merged.shape[0]}")

# Year column
merged["year"] = pd.to_datetime(merged["timeStamp"], unit="s").dt.year

# Compiler family extraction (same regex as Phase 3B)
import re

def compiler_family(v):
    m = re.search(r"v(\d+\.\d+)\.", str(v))
    return f"v{m.group(1)}.x" if m else "unknown"

merged["compiler_family"] = merged["CompilerVersion"].apply(compiler_family)

# Load audited 215‑feature list
feature_list_df = pd.read_csv(FINAL_FEATURE_LIST)
retained_features = feature_list_df["feature_name"].tolist()
print(f"Retained feature count (should be 215): {len(retained_features)}")

X = merged[retained_features].apply(pd.to_numeric, errors="coerce")

y_columns = [
    "Reentrancy",
    "Access Control",
    "Arithmetic",
    "Unchecked Return Values",
    "DoS",
    "Bad Randomness",
    "Front Running",
    "Time manipulation",
]
Y = merged[y_columns].astype(int)

# ------------------------------------------------------------
# Cohort definitions (same as Phase 3B)
train_years = list(range(2016, 2022))  # 2016‑2021
historical_mask = merged["year"].isin(train_years)
contemporary_mask = merged["year"] == 2023  # only 2023 contracts
test_mask = merged["year"] == 2024  # final test set – never used for training

# Sub‑sets
X_train_hist, Y_train_hist = X[historical_mask], Y[historical_mask]
X_train_cont, Y_train_cont = X[contemporary_mask], Y[contemporary_mask]
X_test, Y_test = X[test_mask], Y[test_mask]

# v0.8.x test subset
v08_test_mask = test_mask & (merged["compiler_family"] == "v0.8.x")
X_test_v08, Y_test_v08 = X[v08_test_mask], Y[v08_test_mask]

# Sample size bookkeeping
sample_sizes = {
    "historical_train": int(X_train_hist.shape[0]),
    "contemporary_train": int(X_train_cont.shape[0]),
    "test_total": int(X_test.shape[0]),
    "test_v08": int(X_test_v08.shape[0]),
}
print("Sample sizes:", sample_sizes)

# ------------------------------------------------------------
# Model factories (exact Phase 3B configurations)
random_state = 42
threshold = 0.5

logreg_factory = lambda: Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(class_weight='balanced', random_state=random_state, max_iter=1000)),
])

rf_factory = lambda: RandomForestClassifier(
    n_estimators=200,
    class_weight='balanced',
    random_state=random_state,
    n_jobs=-1,
)

model_defs = [
    ("LogisticRegression", logreg_factory),
    ("RandomForest", rf_factory),
]

# ------------------------------------------------------------
# Train‑and‑evaluate helper

def train_evaluate(model_name, estimator_factory, X_tr, Y_tr, X_ev, Y_ev, cohort_label, period_label="2024"):
    results = []
    for vuln in y_columns:
        y_tr = Y_tr[vuln].values
        clf = estimator_factory()
        clf.fit(X_tr, y_tr)
        # obtain scores
        if hasattr(clf, "predict_proba"):
            y_score = clf.predict_proba(X_ev)[:, 1]
        else:
            y_score = clf.decision_function(X_ev)
        metrics = compute_metrics(Y_ev[vuln].values, y_score, thresh=threshold)
        result = {
            "model": model_name,
            "training_cohort": cohort_label,
            "period": period_label,
            "vulnerability": vuln,
            "precision": metrics["precision"],
            "recall": metrics["recall"],
            "f1": metrics["f1"],
            "pr_auc": metrics["pr_auc"],
            "false_positives": metrics["false_positives"],
            "false_negatives": metrics["false_negatives"],
            "positive_count": metrics["positive_count"],
            "sample_count": metrics["sample_count"],
        }
        results.append(result)
    return results

# ------------------------------------------------------------
# Run experiment twice and collect hashes for deterministic verification
all_hashes = {}
for run_id in range(2):
    print(f"--- Run {run_id + 1} ---")
    all_results = []
    # Historical models (train 2016‑2021)
    for name, factory in model_defs:
        all_results.extend(
            train_evaluate(name, factory, X_train_hist, Y_train_hist, X_test, Y_test, "historical")
        )
    # Contemporary models (train 2023 only)
    for name, factory in model_defs:
        all_results.extend(
            train_evaluate(name, factory, X_train_cont, Y_train_cont, X_test, Y_test, "contemporary")
        )
    df_all = pd.DataFrame(all_results)

    # Macro‑averages per model+training_cohort
    macro_rows = []
    for (model, cohort), grp in df_all.groupby(["model", "training_cohort"]):
        macro_rows.append({
            "model": model,
            "training_cohort": cohort,
            "period": "2024",
            "vulnerability": "macro",
            "precision": macro_average(grp["precision"].values),
            "recall": macro_average(grp["recall"].values),
            "f1": macro_average(grp["f1"].values),
            "pr_auc": macro_average(grp["pr_auc"].values),
            "false_positives": int(grp["false_positives"].sum()),
            "false_negatives": int(grp["false_negatives"].sum()),
            "positive_count": int(grp["positive_count"].sum()),
            "sample_count": int(grp["sample_count"].sum()),
        })
    df_all = pd.concat([df_all, pd.DataFrame(macro_rows)], ignore_index=True)

    # v0.8.x restricted evaluation
    v08_results = []
    for name, factory in model_defs:
        v08_results.extend(
            train_evaluate(name, factory, X_train_hist, Y_train_hist, X_test_v08, Y_test_v08, "historical_v08")
        )
    for name, factory in model_defs:
        v08_results.extend(
            train_evaluate(name, factory, X_train_cont, Y_train_cont, X_test_v08, Y_test_v08, "contemporary_v08")
        )
    df_v08 = pd.DataFrame(v08_results)
    # Macro for v0.8.x
    macro_v08 = []
    for (model, cohort), grp in df_v08.groupby(["model", "training_cohort"]):
        macro_v08.append({
            "model": model,
            "training_cohort": cohort,
            "period": "2024",
            "vulnerability": "macro",
            "precision": macro_average(grp["precision"].values),
            "recall": macro_average(grp["recall"].values),
            "f1": macro_average(grp["f1"] .values),
            "pr_auc": macro_average(grp["pr_auc"].values),
            "false_positives": int(grp["false_positives"].sum()),
            "false_negatives": int(grp["false_negatives"].sum()),
            "positive_count": int(grp["positive_count"].sum()),
            "sample_count": int(grp["sample_count"].sum()),
        })
    df_v08 = pd.concat([df_v08, pd.DataFrame(macro_v08)], ignore_index=True)

    # Save CSVs (overwrites on second run – deterministic content)
    all_path = PHASE5_OUT / "phase5_model_comparison.csv"
    v08_path = PHASE5_OUT / "phase5_v08_comparison.csv"
    df_all.to_csv(all_path, index=False)
    df_v08.to_csv(v08_path, index=False)

    # Metadata JSON
    metadata = {
        "feature_count": len(retained_features),
        "random_state": random_state,
        "threshold": threshold,
        "training_samples": {
            "historical": sample_sizes["historical_train"],
            "contemporary": sample_sizes["contemporary_train"],
        },
        "test_samples": {
            "total": sample_sizes["test_total"],
            "v0.8.x": sample_sizes["test_v08"],
        },
        "model_hyperparameters": {
            "LogisticRegression": {"class_weight": "balanced", "max_iter": 1000},
            "RandomForest": {"n_estimators": 200, "class_weight": "balanced"},
        },
        "description": "Phase 5 experiment testing temporal stability of the feature‑label relationship. No 2024 data used for training or threshold selection.",
    }
    meta_path = PHASE5_OUT / "phase5_metadata.json"
    with meta_path.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    # README
    readme_path = PHASE5_OUT / "PHASE5_README.md"
    with readme_path.open("w", encoding="utf-8") as f:
        f.write("# Phase 5 – Temporal Stability of the Feature–Label Relationship\n\n")
        f.write("## Goal\nTest whether the relationship learned between the audited 215 numeric PRE features and the eight binary DIVE vulnerabilities remains stable over time.\n\n")
        f.write("## Data splits (identical to Phase 3B)\n- **Historical training**: contracts from 2016‑2021 (train years)\n- **Contemporary training**: contracts from 2023 only\n- **Test**: contracts from 2024 – never used for training, preprocessing, or threshold selection.\n- **v0.8.x subset**: test contracts whose `compiler_family` equals `v0.8.x`.\n\n")
        f.write(f"## Sample counts\n- Historical train contracts: {sample_sizes['historical_train']}\n- Contemporary train contracts (2023): {sample_sizes['contemporary_train']}\n- Test contracts (2024): {sample_sizes['test_total']}\n- Test contracts v0.8.x: {sample_sizes['test_v08']}\n\n")
        f.write("## Models (unchanged from Phase 3B)\n- Logistic Regression (StandardScaler, `class_weight='balanced'`, `random_state=42`, `max_iter=1000`).\n- Random Forest (`n_estimators=200`, `class_weight='balanced'`, `random_state=42`).\n- Decision threshold fixed at 0.5 for both models.\n\n")
        f.write("## Metrics reported per vulnerability\nPrecision, Recall, F1, PR‑AUC, false positives, false negatives. Macro‑averaged F1 and PR‑AUC are also provided.\n\n")
        f.write("## Determinism check\nThe script runs the full pipeline twice and verifies that the SHA‑256 hashes of the two CSV files and the JSON metadata are identical across runs.\n\n")
        f.write("## Outputs\n- `phase5_model_comparison.csv` – results on the full 2024 test set.\n- `phase5_v08_comparison.csv` – results limited to compiler family `v0.8.x`.\n- `phase5_metadata.json` – experiment configuration and sample sizes.\n- `PHASE5_README.md` – this document.\n")

    # Compute hashes for this run
    run_hashes = {
        "all_csv": sha256_file(all_path),
        "v08_csv": sha256_file(v08_path),
        "metadata": sha256_file(meta_path),
    }
    all_hashes[run_id] = run_hashes

# Verify deterministic hashes between runs
if all_hashes[0] == all_hashes[1]:
    print("Deterministic verification SUCCESS – identical hashes across two runs.")
else:
    print("Deterministic verification FAILURE – hashes differ between runs.")
    print("Run 0 hashes:", all_hashes[0])
    print("Run 1 hashes:", all_hashes[1])

# End of script
