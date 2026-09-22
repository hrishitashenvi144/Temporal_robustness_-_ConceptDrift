"""
Temporal Robustness and Drift-Aware Adaptation Experiment Pipeline (Phase 2)
=============================================================================

Research Title:
"Temporal Robustness and Drift-Aware Adaptation for Ethereum Smart Contract Vulnerability Detection"

Methodological Note:
Temporal cohorts in Phase 2 represent controlled distribution-shift simulations
rather than naturally observed temporal evolution. The drift detector measures
feature-distribution shift P(X), not definitive concept drift P(Y|X).
Cohort period_new is strictly held out from training, retraining, scaler fitting,
and adaptation decisions.

Temporal Order:
period_old -> period_medium -> period_new
"""

import json
import logging
import os
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_fscore_support
from sklearn.preprocessing import StandardScaler

from adaptive_detector import AdaptiveDetector

# Configure ASCII-safe logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


# =====================================================================
# CONFIGURATION & CONSTANTS
# =====================================================================

DATA_PATH = "data/raw/poc_data/contracts_with_features.csv"
RESULTS_DIR = "results"
RESULTS_CSV_PATH = os.path.join(RESULTS_DIR, "temporal_experiment_results.csv")
LEGACY_RESULTS_CSV_PATH = os.path.join(RESULTS_DIR, "static_vs_adaptive_comparison.csv")
FEATURE_SHIFT_CSV_PATH = os.path.join(RESULTS_DIR, "feature_shift_analysis.csv")
METADATA_JSON_PATH = os.path.join(RESULTS_DIR, "experiment_metadata.json")

FEATURE_COLS = [
    "lines_of_code",
    "function_count",
    "external_calls",
    "requires",
    "loops",
    "code_length"
]

TARGET_COL = "has_vulnerability"
COHORT_ORDER = ["period_old", "period_medium", "period_new"]
RANDOM_SEED = 42
N_ESTIMATORS = 50
DRIFT_THRESHOLD = 0.10
DRIFT_METHOD = "combined"


# =====================================================================
# STAGE A: DATA LOADING & COHORT VALIDATION
# =====================================================================

def validate_dataset(
    data_path: str,
    feature_cols: List[str],
    target_col: str,
    expected_periods: List[str]
) -> pd.DataFrame:
    """
    Load dataset and validate that expected cohorts, features, and target labels exist
    with valid types and no missing values.
    
    Fails loudly on any validation error.
    """
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset file not found at: {data_path}")

    df = pd.read_csv(data_path)
    if len(df) == 0:
        raise ValueError(f"Dataset at {data_path} is empty.")

    # Validate target column
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in dataset. Columns: {list(df.columns)}")

    # Validate feature columns
    missing_features = [col for col in feature_cols if col not in df.columns]
    if missing_features:
        raise ValueError(f"Missing required feature columns: {missing_features}")

    # Validate period column
    if "period" not in df.columns:
        raise ValueError(f"Temporal partition column 'period' not found in dataset.")

    # Check for NaN / infinite values in features or labels
    if df[feature_cols].isnull().values.any():
        raise ValueError("Dataset contains NaN values in feature columns.")

    if not np.isfinite(df[feature_cols].values).all():
        raise ValueError("Dataset contains infinite values in feature columns.")

    if df[target_col].isnull().values.any():
        raise ValueError(f"Target column '{target_col}' contains NaN values.")

    # Validate target labels (binary 0 or 1)
    unique_labels = set(df[target_col].unique())
    if not unique_labels.issubset({0, 1}):
        raise ValueError(f"Invalid target labels: expected binary {0, 1}, found {unique_labels}")

    # Validate each expected cohort
    present_periods = df["period"].unique().tolist()
    for period in expected_periods:
        if period not in present_periods:
            raise ValueError(
                f"Required temporal cohort '{period}' not found in dataset. "
                f"Present cohorts: {present_periods}"
            )
        cohort_count = len(df[df["period"] == period])
        if cohort_count == 0:
            raise ValueError(f"Temporal cohort '{period}' contains 0 samples.")

    logger.info(
        f"Validation passed for dataset '{data_path}': "
        f"{len(df)} total rows across cohorts {expected_periods}."
    )
    return df


# =====================================================================
# STAGE B: FEATURE-SHIFT ANALYSIS
# =====================================================================

def compute_feature_shift_analysis(
    df: pd.DataFrame,
    feature_cols: List[str]
) -> pd.DataFrame:
    """
    Calculate mean, standard deviation, and percentage shifts for all features
    across temporal cohorts (period_old, period_medium, period_new).
    """
    rows = []

    for feature in feature_cols:
        old_series = df[df["period"] == "period_old"][feature].astype(float)
        medium_series = df[df["period"] == "period_medium"][feature].astype(float)
        new_series = df[df["period"] == "period_new"][feature].astype(float)

        old_mean = float(old_series.mean())
        medium_mean = float(medium_series.mean())
        new_mean = float(new_series.mean())

        old_std = float(old_series.std())
        medium_std = float(medium_series.std())
        new_std = float(new_series.std())

        old_to_medium_pct = (
            ((medium_mean - old_mean) / old_mean * 100.0)
            if old_mean != 0.0 else 0.0
        )
        old_to_new_pct = (
            ((new_mean - old_mean) / old_mean * 100.0)
            if old_mean != 0.0 else 0.0
        )

        rows.append({
            "Feature": feature,
            "Old_Mean": old_mean,
            "Medium_Mean": medium_mean,
            "New_Mean": new_mean,
            "Old_to_Medium_%": old_to_medium_pct,
            "Old_to_New_%": old_to_new_pct,
            "Old_Std": old_std,
            "Medium_Std": medium_std,
            "New_Std": new_std
        })

    return pd.DataFrame(rows)


# =====================================================================
# EVALUATION HELPER
# =====================================================================

def evaluate_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    period_name: str
) -> Dict[str, Any]:
    """
    Compute binary precision, recall, and F1 score from predictions.
    """
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true,
        y_pred,
        average="binary",
        zero_division=0
    )
    return {
        "Period": period_name,
        "Precision": float(precision),
        "Recall": float(recall),
        "F1": float(f1),
        "Evaluation_Samples": len(y_true)
    }


# =====================================================================
# STAGE K: DATA LEAKAGE VERIFICATION
# =====================================================================

def verify_temporal_leakage_safety(
    df: pd.DataFrame,
    train_indices: np.ndarray,
    adaptation_indices: np.ndarray,
    new_indices: np.ndarray
) -> Dict[str, bool]:
    """
    Explicitly verify that period_new samples never participate in training,
    retraining, or adaptation datasets.
    """
    train_idx_set = set(train_indices)
    adapt_idx_set = set(adaptation_indices)
    new_idx_set = set(new_indices)

    # Check index overlap
    overlap_train_new = train_idx_set.intersection(new_idx_set)
    overlap_adapt_new = adapt_idx_set.intersection(new_idx_set)

    leakage_checks = {
        "period_new_not_in_initial_train": len(overlap_train_new) == 0,
        "period_new_not_in_adaptation": len(overlap_adapt_new) == 0,
        "adaptation_contains_old_and_medium_only": adapt_idx_set == train_idx_set.union(
            set(df[df["period"] == "period_medium"].index)
        )
    }

    if not all(leakage_checks.values()):
        raise AssertionError(f"Temporal data leakage detected! Checks: {leakage_checks}")

    logger.info("Leakage verification passed: period_new is strictly held out.")
    return leakage_checks


# =====================================================================
# MAIN EXPERIMENT PIPELINE
# =====================================================================

def run_experiment() -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
    """
    Execute the complete, reproducible Phase 2 experimental pipeline.
    """
    print("=" * 80)
    print("PHASE 2: TEMPORAL ROBUSTNESS & DRIFT-AWARE ADAPTATION EXPERIMENT")
    print("=" * 80)

    # 1 & 2. Load dataset and validate cohorts
    print("\n[Stage 1 & 2] Loading dataset and validating cohorts...")
    df = validate_dataset(DATA_PATH, FEATURE_COLS, TARGET_COL, COHORT_ORDER)

    df_old = df[df["period"] == "period_old"]
    df_medium = df[df["period"] == "period_medium"]
    df_new = df[df["period"] == "period_new"]

    X_old = df_old[FEATURE_COLS].values
    y_old = df_old[TARGET_COL].values

    X_medium = df_medium[FEATURE_COLS].values
    y_medium = df_medium[TARGET_COL].values

    X_new = df_new[FEATURE_COLS].values
    y_new = df_new[TARGET_COL].values

    cohort_sizes = {
        "period_old": len(df_old),
        "period_medium": len(df_medium),
        "period_new": len(df_new)
    }

    for cohort, size in cohort_sizes.items():
        print(f"  Cohort '{cohort}': {size} samples")

    # 3. Calculate feature-shift statistics
    print("\n[Stage 3] Calculating feature-distribution shift statistics...")
    shift_df = compute_feature_shift_analysis(df, FEATURE_COLS)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    shift_df.to_csv(FEATURE_SHIFT_CSV_PATH, index=False)
    print(f"  Saved feature-shift analysis to: {FEATURE_SHIFT_CSV_PATH}")

    # 4 & 5. Train and evaluate static baseline on period_old
    print("\n" + "-" * 80)
    print("[Stage 4 & 5] STATIC BASELINE DETECTOR (TRAIN ONLY ON PERIOD_OLD)")
    print("-" * 80)

    static_scaler = StandardScaler()
    X_old_scaled = static_scaler.fit_transform(X_old)

    static_model = RandomForestClassifier(
        n_estimators=N_ESTIMATORS,
        random_state=RANDOM_SEED
    )
    static_model.fit(X_old_scaled, y_old)

    # Evaluate static model on Old, Medium, New
    static_old_eval = evaluate_metrics(
        y_old,
        static_model.predict(X_old_scaled),
        "period_old"
    )

    X_medium_scaled_static = static_scaler.transform(X_medium)
    static_medium_eval = evaluate_metrics(
        y_medium,
        static_model.predict(X_medium_scaled_static),
        "period_medium"
    )

    X_new_scaled_static = static_scaler.transform(X_new)
    static_new_eval = evaluate_metrics(
        y_new,
        static_model.predict(X_new_scaled_static),
        "period_new"
    )

    print(f"  Static / Old:    Precision={static_old_eval['Precision']:.3f}, "
          f"Recall={static_old_eval['Recall']:.3f}, F1={static_old_eval['F1']:.3f}")
    print(f"  Static / Medium: Precision={static_medium_eval['Precision']:.3f}, "
          f"Recall={static_medium_eval['Recall']:.3f}, F1={static_medium_eval['F1']:.3f}")
    print(f"  Static / New:    Precision={static_new_eval['Precision']:.3f}, "
          f"Recall={static_new_eval['Recall']:.3f}, F1={static_new_eval['F1']:.3f}")

    # 6, 7, 8. Adaptive detector initial fit, pre-adaptation eval & drift detection
    print("\n" + "-" * 80)
    print("[Stage 6, 7, 8] ADAPTIVE DETECTOR (PRE-ADAPTATION EVALUATION & DRIFT CHECK)")
    print("-" * 80)

    adaptive_rf = RandomForestClassifier(
        n_estimators=N_ESTIMATORS,
        random_state=RANDOM_SEED
    )
    adaptive = AdaptiveDetector(
        model=adaptive_rf,
        drift_threshold=DRIFT_THRESHOLD,
        drift_method=DRIFT_METHOD
    )
    adaptive.fit(X_old, y_old)

    # Pre-adaptation evaluation on period_medium
    adaptive_medium_eval = adaptive.evaluate_and_detect(
        X_medium,
        y_medium,
        period_name="period_medium"
    )

    drift_score = float(adaptive_medium_eval["Drift_Score"])
    drift_detected = bool(adaptive_medium_eval["Drift_Detected"])
    drift_threshold = float(adaptive_medium_eval["Drift_Threshold"])

    print(f"  Adaptive / Medium Pre-Adaptation: Precision={adaptive_medium_eval['Precision']:.3f}, "
          f"Recall={adaptive_medium_eval['Recall']:.3f}, F1={adaptive_medium_eval['F1']:.3f}")
    print(f"  Medium Feature Drift Score: {drift_score:.3f} (Threshold: {drift_threshold:.2f})")
    print(f"  Drift Detected: {drift_detected}")

    # 9. Retrain if drift is detected (strictly on OLD + MEDIUM)
    retrained_occurred = False
    adaptation_training_samples = len(X_old)
    adaptation_indices = df_old.index.values

    if drift_detected:
        print("\n[Stage 9] Drift detected above threshold! Retraining on period_old + period_medium...")
        X_adaptation = np.vstack([X_old, X_medium])
        y_adaptation = np.hstack([y_old, y_medium])
        adaptation_training_samples = len(X_adaptation)
        adaptation_indices = np.concatenate([df_old.index.values, df_medium.index.values])

        adaptive.retrain(
            X_adaptation,
            y_adaptation,
            period_name="period_medium"
        )
        retrained_occurred = True
        print(f"  Adaptive detector retrained on {adaptation_training_samples} cumulative samples.")
    else:
        print("\n[Stage 9] No drift detected. Maintaining frozen initial model.")

    # 10. Evaluate adapted model on strictly unseen period_new
    print("\n" + "-" * 80)
    print("[Stage 10] EVALUATION ON UNSEEN COHORT (PERIOD_NEW)")
    print("-" * 80)
    print("  Note: period_new is strictly unseen during training, scaler fitting, and adaptation.")

    adaptive_new_eval = adaptive.evaluate(
        X_new,
        y_new,
        period_name="period_new"
    )

    print(f"  Adaptive / New Post-Adaptation: Precision={adaptive_new_eval['Precision']:.3f}, "
          f"Recall={adaptive_new_eval['Recall']:.3f}, F1={adaptive_new_eval['F1']:.3f}")

    # Leakage verification
    leakage_results = verify_temporal_leakage_safety(
        df=df,
        train_indices=df_old.index.values,
        adaptation_indices=adaptation_indices,
        new_indices=df_new.index.values
    )

    # 11. Compile and save standardized results CSV
    results_records = [
        {
            "Period": "period_old",
            "Model": "Static",
            "Precision": static_old_eval["Precision"],
            "Recall": static_old_eval["Recall"],
            "F1": static_old_eval["F1"],
            "Drift_Detected": False,
            "Drift_Score": np.nan,
            "Retrained": False,
            "Training_Samples": len(X_old),
            "Evaluation_Samples": len(X_old)
        },
        {
            "Period": "period_medium",
            "Model": "Static",
            "Precision": static_medium_eval["Precision"],
            "Recall": static_medium_eval["Recall"],
            "F1": static_medium_eval["F1"],
            "Drift_Detected": False,
            "Drift_Score": np.nan,
            "Retrained": False,
            "Training_Samples": len(X_old),
            "Evaluation_Samples": len(X_medium)
        },
        {
            "Period": "period_new",
            "Model": "Static",
            "Precision": static_new_eval["Precision"],
            "Recall": static_new_eval["Recall"],
            "F1": static_new_eval["F1"],
            "Drift_Detected": False,
            "Drift_Score": np.nan,
            "Retrained": False,
            "Training_Samples": len(X_old),
            "Evaluation_Samples": len(X_new)
        },
        {
            "Period": "period_medium",
            "Model": "Adaptive_PreAdaptation",
            "Precision": adaptive_medium_eval["Precision"],
            "Recall": adaptive_medium_eval["Recall"],
            "F1": adaptive_medium_eval["F1"],
            "Drift_Detected": drift_detected,
            "Drift_Score": drift_score,
            "Retrained": retrained_occurred,
            "Training_Samples": len(X_old),
            "Evaluation_Samples": len(X_medium)
        },
        {
            "Period": "period_new",
            "Model": "Adaptive_PostAdaptation",
            "Precision": adaptive_new_eval["Precision"],
            "Recall": adaptive_new_eval["Recall"],
            "F1": adaptive_new_eval["F1"],
            "Drift_Detected": False,
            "Drift_Score": np.nan,
            "Retrained": False,
            "Training_Samples": adaptation_training_samples,
            "Evaluation_Samples": len(X_new)
        }
    ]

    results_df = pd.DataFrame(results_records)
    results_df.to_csv(RESULTS_CSV_PATH, index=False)
    results_df.to_csv(LEGACY_RESULTS_CSV_PATH, index=False)
    print(f"\n[Stage 11] Saved experiment results to: {RESULTS_CSV_PATH}")

    # 12. Save experiment metadata JSON
    metadata = {
        "experiment_name": "Temporal Robustness and Drift-Aware Adaptation for Ethereum Smart Contract Vulnerability Detection",
        "experiment_version": "Phase 2 (Controlled Distribution-Shift Simulation)",
        "random_seed": RANDOM_SEED,
        "model_name": "RandomForestClassifier",
        "n_estimators": N_ESTIMATORS,
        "drift_method": DRIFT_METHOD,
        "drift_threshold": DRIFT_THRESHOLD,
        "feature_columns": FEATURE_COLS,
        "target_column": TARGET_COL,
        "cohort_order": COHORT_ORDER,
        "cohort_sizes": cohort_sizes,
        "training_protocol": (
            "Static model trained on period_old only. "
            "Adaptive detector trained on period_old, evaluated on period_medium before adaptation, "
            "retrained on period_old + period_medium upon drift trigger, and evaluated on unseen period_new."
        ),
        "adaptation_protocol": (
            "Cumulative retraining on period_old + period_medium when feature-distribution drift "
            "exceeds threshold on period_medium. period_new is strictly held out."
        ),
        "dataset_description": "SmartBugs-derived POC dataset containing 6 structural Solidity features across 3 temporal cohorts.",
        "temporal_shift_description": "Controlled multiplicative feature perturbation simulated with fixed random seed 42.",
        "evaluation_metrics": ["Precision", "Recall", "F1"],
        "output_files": {
            "results_csv": RESULTS_CSV_PATH,
            "feature_shift_csv": FEATURE_SHIFT_CSV_PATH,
            "metadata_json": METADATA_JSON_PATH
        },
        "leakage_verification_passed": leakage_results,
        "methodological_note": (
            "Temporal cohorts in Phase 2 are controlled experimental cohorts with simulated feature perturbation "
            "rather than naturally observed temporal evolution. The drift detector measures feature-distribution shift "
            "P(X) and does not establish concept drift P(Y|X). Cohort period_new is strictly held out from training, "
            "retraining, scaler fitting, and adaptation decisions. Current results demonstrate the behavior of the "
            "experimental protocol, not universal real-world temporal robustness."
        )
    }

    with open(METADATA_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"[Stage 12] Saved experiment metadata to: {METADATA_JSON_PATH}")

    # 13. Calculate and print summary metrics
    static_old_f1 = static_old_eval["F1"]
    static_medium_f1 = static_medium_eval["F1"]
    static_new_f1 = static_new_eval["F1"]

    adaptive_medium_f1 = adaptive_medium_eval["F1"]
    adaptive_new_f1 = adaptive_new_eval["F1"]

    static_degradation_medium = static_old_f1 - static_medium_f1
    static_degradation_medium_pct = (
        (static_degradation_medium / static_old_f1 * 100.0)
        if static_old_f1 > 0 else 0.0
    )

    static_degradation_new = static_old_f1 - static_new_f1
    static_degradation_new_pct = (
        (static_degradation_new / static_old_f1 * 100.0)
        if static_old_f1 > 0 else 0.0
    )

    adaptive_vs_static_new_abs = adaptive_new_f1 - static_new_f1
    adaptive_vs_static_new_rel = (
        (adaptive_vs_static_new_abs / static_new_f1 * 100.0)
        if static_new_f1 > 0 else 0.0
    )

    retraining_events = len(adaptive.retrain_history)

    print("\n" + "=" * 80)
    print("CONCISE RESEARCH SUMMARY")
    print("=" * 80)

    print(f"Static Old F1:                         {static_old_f1:.3f}")
    print(f"Static Medium F1:                      {static_medium_f1:.3f}")
    print(f"Static New F1:                         {static_new_f1:.3f}")
    print(f"Static Old -> Medium F1 Degradation:   {static_degradation_medium:.3f} ({static_degradation_medium_pct:.1f}%)")
    print(f"Static Old -> New F1 Degradation:      {static_degradation_new:.3f} ({static_degradation_new_pct:.1f}%)")
    print(f"Adaptive Medium Pre-Adaptation F1:     {adaptive_medium_f1:.3f}")
    print(f"Medium Drift Score:                    {drift_score:.3f}")
    print(f"Drift Threshold:                       {drift_threshold:.2f}")
    print(f"Drift Detected:                        {drift_detected}")
    print(f"Retraining Occurred:                   {retrained_occurred}")
    print(f"Adaptive New Post-Adaptation F1:       {adaptive_new_f1:.3f}")
    print(f"Adaptive vs Static New Absolute Gain:  {adaptive_vs_static_new_abs:+.3f}")
    print(f"Adaptive vs Static New Relative Gain:  {adaptive_vs_static_new_rel:+.1f}%")
    print(f"Number of Retraining Events:           {retraining_events}")

    print("\n" + "=" * 80)
    print("EXPERIMENT PIPELINE EXECUTION COMPLETED")
    print("=" * 80)

    summary_metrics = {
        "static_old_f1": static_old_f1,
        "static_medium_f1": static_medium_f1,
        "static_new_f1": static_new_f1,
        "static_degradation_medium": static_degradation_medium,
        "static_degradation_medium_pct": static_degradation_medium_pct,
        "static_degradation_new": static_degradation_new,
        "static_degradation_new_pct": static_degradation_new_pct,
        "adaptive_medium_f1": adaptive_medium_f1,
        "drift_score": drift_score,
        "drift_threshold": drift_threshold,
        "drift_detected": drift_detected,
        "retraining_occurred": retrained_occurred,
        "adaptive_new_f1": adaptive_new_f1,
        "adaptive_vs_static_new_abs": adaptive_vs_static_new_abs,
        "adaptive_vs_static_new_rel": adaptive_vs_static_new_rel,
        "retraining_events": retraining_events
    }

    return results_df, shift_df, summary_metrics


if __name__ == "__main__":
    run_experiment()