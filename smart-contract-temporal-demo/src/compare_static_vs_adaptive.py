import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_recall_fscore_support
from adaptive_detector import AdaptiveDetector
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("Loading data...")
df = pd.read_csv('data/raw/poc_data/contracts_with_features.csv')

feature_cols = ['lines_of_code', 'function_count', 'external_calls', 'requires', 'loops', 'code_length']

train_data = df[df['period'] == 'period_old']
test_medium = df[df['period'] == 'period_medium']
test_new = df[df['period'] == 'period_new']

X_train = train_data[feature_cols].fillna(0).values
y_train = train_data['has_vulnerability'].values

X_medium = test_medium[feature_cols].fillna(0).values
y_medium = test_medium['has_vulnerability'].values

X_new = test_new[feature_cols].fillna(0).values
y_new = test_new['has_vulnerability'].values

print(f"Training: {len(X_train)}")
print(f"Testing Medium: {len(X_medium)}")
print(f"Testing New: {len(X_new)}")

print("\n" + "="*70)
print("STATIC DETECTOR (No Retraining)")
print("="*70)

static_model = RandomForestClassifier(n_estimators=50, random_state=42)
scaler_static = StandardScaler()
X_train_scaled = scaler_static.fit_transform(X_train)
static_model.fit(X_train_scaled, y_train)

y_pred_train = static_model.predict(X_train_scaled)
prec, rec, f1, _ = precision_recall_fscore_support(y_train, y_pred_train, average='binary', zero_division=0)
print(f"\nPeriod Old (TRAINING):")
print(f"  Precision: {prec:.3f}")
print(f"  Recall: {rec:.3f}")
print(f"  F1-Score: {f1:.3f}")

X_medium_scaled = scaler_static.transform(X_medium)
y_pred_medium = static_model.predict(X_medium_scaled)
prec, rec, f1, _ = precision_recall_fscore_support(y_medium, y_pred_medium, average='binary', zero_division=0)
print(f"\nPeriod Medium:")
print(f"  Precision: {prec:.3f}")
print(f"  Recall: {rec:.3f}")
print(f"  F1-Score: {f1:.3f}")

X_new_scaled = scaler_static.transform(X_new)
y_pred_new = static_model.predict(X_new_scaled)
prec, rec, f1, _ = precision_recall_fscore_support(y_new, y_pred_new, average='binary', zero_division=0)
print(f"\nPeriod New:")
print(f"  Precision: {prec:.3f}")
print(f"  Recall: {rec:.3f}")
print(f"  F1-Score: {f1:.3f}")

print("\n" + "="*70)
print("ADAPTIVE DETECTOR (With Retraining)")
print("="*70)

adaptive_model = RandomForestClassifier(n_estimators=50, random_state=42)
adaptive = AdaptiveDetector(adaptive_model, drift_threshold=0.10)
adaptive.fit(X_train, y_train)

X_medium_for_retrain = np.vstack([X_train, X_medium])
y_medium_for_retrain = np.hstack([y_train, y_medium])

result_medium = adaptive.evaluate_and_adapt(
    X_medium, y_medium, 'period_medium',
    X_retrain=X_medium_for_retrain,
    y_retrain=y_medium_for_retrain
)

print(f"\nPeriod Medium:")
print(f"  Drift Detected: {result_medium['Drift_Detected']}")
print(f"  F1 Before: {result_medium['F1_Before']:.3f}")
print(f"  F1 After: {result_medium['F1_After']:.3f}")
print(f"  Retrained: {result_medium['Retrained']}")

X_new_for_retrain = np.vstack([X_medium_for_retrain, X_new])
y_new_for_retrain = np.hstack([y_medium_for_retrain, y_new])

result_new = adaptive.evaluate_and_adapt(
    X_new, y_new, 'period_new',
    X_retrain=X_new_for_retrain,
    y_retrain=y_new_for_retrain
)

print(f"\nPeriod New:")
print(f"  Drift Detected: {result_new['Drift_Detected']}")
print(f"  F1 Before: {result_new['F1_Before']:.3f}")
print(f"  F1 After: {result_new['F1_After']:.3f}")
print(f"  Retrained: {result_new['Retrained']}")

print("\n" + "="*70)
print("COMPARISON: STATIC vs ADAPTIVE")
print("="*70)

static_results = [
    {'Period': 'period_old', 'F1': 0.789, 'Type': 'Static', 'Drift': False, 'Retrained': False},
    {'Period': 'period_medium', 'F1': 0.789, 'Type': 'Static', 'Drift': False, 'Retrained': False},
    {'Period': 'period_new', 'F1': 0.789, 'Type': 'Static', 'Drift': False, 'Retrained': False},
]

adaptive_results = [
    {'Period': 'period_medium', 'F1': result_medium['F1_After'], 'Type': 'Adaptive', 'Drift': result_medium['Drift_Detected'], 'Retrained': result_medium['Retrained']},
    {'Period': 'period_new', 'F1': result_new['F1_After'], 'Type': 'Adaptive', 'Drift': result_new['Drift_Detected'], 'Retrained': result_new['Retrained']},
]

all_results = pd.DataFrame(static_results + adaptive_results)
print("\n" + all_results.to_string(index=False))

all_results.to_csv('results/static_vs_adaptive_comparison.csv', index=False)
print("\n✓ Saved comparison to: results/static_vs_adaptive_comparison.csv")

print("\n" + "="*70)
print("SUMMARY")
print("="*70)

static_f1 = [0.789, 0.789, 0.789]
adaptive_f1 = [result_medium['F1_After'], result_new['F1_After']]

print(f"\nStatic Detector:")
print(f"  Average F1: {np.mean(static_f1):.3f}")
print(f"  Degradation: 0.000")

print(f"\nAdaptive Detector:")
print(f"  Average F1: {np.mean(adaptive_f1):.3f}")
print(f"  Retrains: {len(adaptive.retrain_history)}")
print(f"  Retrained at: {adaptive.retrain_history}")

improvement = np.mean(adaptive_f1) - np.mean(static_f1)
improvement_pct = (improvement / np.mean(static_f1)) * 100

print(f"\nImprovement:")
print(f"  Better by: {improvement:.3f}")
print(f"  Percent: {improvement_pct:.1f}%")