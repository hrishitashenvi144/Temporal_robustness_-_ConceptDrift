import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix
import numpy as np

# Load features
df = pd.read_csv('data/raw/poc_data/contracts_with_features.csv')

print("=" * 60)
print("TEMPORAL ROBUSTNESS")
print("=" * 60)

# Get feature columns
feature_cols = ['lines_of_code', 'function_count', 'external_calls', 'requires', 'loops', 'code_length']

# CHRONOLOGICAL SPLIT (not random!)
# Train on period_old only
train_data = df[df['period'] == 'period_old']
test_medium = df[df['period'] == 'period_medium']
test_new = df[df['period'] == 'period_new']

print(f"\nData split:")
print(f"  Training (period_old): {len(train_data)} samples")
print(f"  Testing (period_medium): {len(test_medium)} samples")
print(f"  Testing (period_new): {len(test_new)} samples")

# Extract features
X_train = train_data[feature_cols]
y_train = train_data['has_vulnerability']

# Train detector
detector = RandomForestClassifier(n_estimators=50, random_state=42)
detector.fit(X_train, y_train)

print("\n" + "=" * 60)
print("RESULTS: Static Detector (No Retraining)")
print("=" * 60)

# Evaluate on each period
results = []

# Training period
y_pred_train = detector.predict(X_train)
prec, rec, f1, _ = precision_recall_fscore_support(y_train, y_pred_train, average='binary', zero_division=0)
cm = confusion_matrix(y_train, y_pred_train, labels=[0, 1])
if cm.size == 4:
    tn, fp, fn, tp = cm.ravel()
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
else:
    # All samples are same label
    fpr = 0

print(f"\nPeriod Old (TRAINING):")
print(f"  Precision: {prec:.3f}")
print(f"  Recall: {rec:.3f}")
print(f"  F1-Score: {f1:.3f}")
print(f"  False Positive Rate: {fpr:.3f}")

results.append({
    'Period': 'period_old',
    'Precision': prec,
    'Recall': rec,
    'F1-Score': f1,
    'False_Positive_Rate': fpr
})

# Test on medium period (future data)
X_test_medium = test_medium[feature_cols]
y_test_medium = test_medium['has_vulnerability']
y_pred_medium = detector.predict(X_test_medium)
prec, rec, f1, _ = precision_recall_fscore_support(y_test_medium, y_pred_medium, average='binary', zero_division=0)
cm = confusion_matrix(y_train, y_pred_train, labels=[0, 1])
if cm.size == 4:
    tn, fp, fn, tp = cm.ravel()
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
else:
    # All samples are same label
    fpr = 0

print(f"\nPeriod Medium (FUTURE):")
print(f"  Precision: {prec:.3f}")
print(f"  Recall: {rec:.3f}")
print(f"  F1-Score: {f1:.3f}")
print(f"  False Positive Rate: {fpr:.3f}")

results.append({
    'Period': 'period_medium',
    'Precision': prec,
    'Recall': rec,
    'F1-Score': f1,
    'False_Positive_Rate': fpr
})

# Test on new period (even more future data)
X_test_new = test_new[feature_cols]
y_test_new = test_new['has_vulnerability']
y_pred_new = detector.predict(X_test_new)
prec, rec, f1, _ = precision_recall_fscore_support(y_test_new, y_pred_new, average='binary', zero_division=0)
cm = confusion_matrix(y_train, y_pred_train, labels=[0, 1])
if cm.size == 4:
    tn, fp, fn, tp = cm.ravel()
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
else:
    # All samples are same label
    fpr = 0

print(f"\nPeriod New (MOST FUTURE):")
print(f"  Precision: {prec:.3f}")
print(f"  Recall: {rec:.3f}")
print(f"  F1-Score: {f1:.3f}")
print(f"  False Positive Rate: {fpr:.3f}")

results.append({
    'Period': 'period_new',
    'Precision': prec,
    'Recall': rec,
    'F1-Score': f1,
    'False_Positive_Rate': fpr
})

# Save results
results_df = pd.DataFrame(results)
results_df.to_csv('results/temporal_evaluation_static.csv', index=False)

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(results_df.to_string(index=False))

# Calculate degradation
initial_f1 = results_df.iloc[0]['F1-Score']
final_f1 = results_df.iloc[-1]['F1-Score']
degradation = initial_f1 - final_f1

print(f"\nF1-Score Degradation: {degradation:.3f} ({degradation/initial_f1*100:.1f}%)")