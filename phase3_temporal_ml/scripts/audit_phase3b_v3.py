import pandas as pd, os, json, re, sys

# Paths
PRE_CSV = r"c:/Users/LAPTOPS24/Documents/HRISHITA/CLG/Blockchain/demo1/phase3_dataset_audit/raw/Preprocessed/PRE/PRE_ProcessedData.csv"
REPORT_DIR = r"c:/Users/LAPTOPS24/Documents/HRISHITA/CLG/Blockchain/demo1/phase3_temporal_ml/reports"
os.makedirs(REPORT_DIR, exist_ok=True)

# Load data
pre_df = pd.read_csv(PRE_CSV)
all_columns = list(pre_df.columns)

# Exclusion rules
exclude_contractID = ['contractID']
exclude_timestamp = ['timeStamp']
exclude_compiler = ['CompilerVersion']
exclude_categorical = ['EVMVersion', 'LicenseType', 'mostFrequentOpcode']

# Build exclusion dict with reasons
exclusions = {}
for c in exclude_contractID:
    exclusions[c] = 'identifier (contractID)'
for c in exclude_timestamp:
    exclusions[c] = 'temporal leakage (deployment timestamp)'
for c in exclude_compiler:
    exclusions[c] = 'compiler version (reserved for analysis)'
for c in exclude_categorical:
    exclusions[c] = 'categorical/non-numeric (baseline numeric-only)'
# Any other non-numeric (object dtype) columns not already excluded
for c in all_columns:
    if c in exclusions:
        continue
    if pre_df[c].dtype == object:
        exclusions[c] = 'non-numeric column'

# Determine retained numeric columns (excluding any that are in exclusions)
retained = [c for c in all_columns if c not in exclusions and pd.api.types.is_numeric_dtype(pre_df[c])]

# Feature audit table
audit_rows = []
for c in all_columns:
    dtype = str(pre_df[c].dtype)
    included = c in retained
    audit_rows.append({
        'feature_name': c,
        'dtype': dtype,
        'feature_group': 'numeric' if pd.api.types.is_numeric_dtype(pre_df[c]) else 'non-numeric',
        'included': included,
        'exclusion_reason': '' if included else exclusions.get(c, '')
    })

audit_df = pd.DataFrame(audit_rows)
audit_df.to_csv(os.path.join(REPORT_DIR, 'feature_audit.csv'), index=False)

# Final feature list
final_feature_df = audit_df[audit_df['included']].copy()
final_feature_df.to_csv(os.path.join(REPORT_DIR, 'final_feature_list.csv'), index=False)

# Missing value counts for retained features
missing_counts = pre_df[retained].isnull().sum()
missing_counts = missing_counts[missing_counts > 0]

# Zero-variance features among retained
zero_variance = [c for c in retained if pre_df[c].nunique() == 1]

# Compiler family derivation
def compiler_family(v):
    m = re.search(r'v(\d+\.\d+)\.', str(v))
    return f"v{m.group(1)}.x" if m else 'unknown'
pre_df['compiler_family'] = pre_df['CompilerVersion'].apply(compiler_family)
pre_df['year'] = pd.to_datetime(pre_df['timeStamp'], unit='s').dt.year
cohort_map = {2022: 'validation', 2023: 'adaptation', 2024: 'test'}
compiler_counts = {}
for yr, label in cohort_map.items():
    counts = pre_df[pre_df['year'] == yr]['compiler_family'].value_counts().to_dict()
    compiler_counts[label] = counts

# Prepare textual summary (ASCII safe)
lines = []
lines.append('--- Feature audit summary ---')
lines.append(f'Total original PRE columns: {len(all_columns)}')
lines.append(f'Retained numeric features: {len(retained)}')
lines.append(f'Excluded features: {len(exclusions)}')
lines.append('Excluded columns:')
for col, reason in exclusions.items():
    lines.append(f'  {col}: {reason}')
lines.append('')
lines.append('First 20 retained features:')
for col in retained[:20]:
    lines.append(f'  {col}')
lines.append('')
lines.append('Missing value counts (retained):')
if not missing_counts.empty:
    for col, cnt in missing_counts.items():
        lines.append(f'  {col}: {cnt}')
else:
    lines.append('  None')
lines.append('')
lines.append('Zero-variance features (retained):')
if zero_variance:
    for col in zero_variance:
        lines.append(f'  {col}')
else:
    lines.append('  None')
lines.append('')
lines.append('Compiler family distribution by temporal cohort:')
lines.append(json.dumps(compiler_counts, indent=2))
summary_text = "\n".join(lines)
# Ensure ascii safe for printing
summary_ascii = summary_text.encode('ascii', errors='ignore').decode()
# Save summary to artifact for user
summary_path = os.path.join(REPORT_DIR, 'audit_summary.txt')
with open(summary_path, 'w', encoding='utf-8') as f:
    f.write(summary_ascii)
print(summary_ascii)
