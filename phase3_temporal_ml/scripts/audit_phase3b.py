import pandas as pd, os, json, re

# Paths
PRE_CSV = r"c:/Users/LAPTOPS24/Documents/HRISHITA/CLG/Blockchain/demo1/phase3_dataset_audit/raw/Preprocessed/PRE/PRE_ProcessedData.csv"
LABELS_CSV = r"c:/Users/LAPTOPS24/Documents/HRISHITA/CLG/Blockchain/demo1/phase3_dataset_audit/raw/Labels/DIVE_Labels.csv"
REPORT_DIR = r"c:/Users/LAPTOPS24/Documents/HRISHITA/CLG/Blockchain/demo1/phase3_temporal_ml/reports"
os.makedirs(REPORT_DIR, exist_ok=True)

# Load data
print("Loading PRE CSV...")
pre_df = pd.read_csv(PRE_CSV)
print(f"Loaded {pre_df.shape[0]} rows, {pre_df.shape[1]} columns")

# Identify columns
all_columns = list(pre_df.columns)

# Exclusion rules
exclude_contractID = ['contractID']
exclude_timestamp = ['timeStamp']
# Derived calendar-time variable will be created later; none present now.
exclude_compiler = ['CompilerVersion']
# Categorical / non‑numeric columns (excluding numeric ones)
# Determine dtype after pandas load – object types are non‑numeric.
non_numeric = [c for c in all_columns if pre_df[c].dtype == object]
# From those, we will explicitly exclude EVMVersion, LicenseType, mostFrequentOpcode (though not leakage per user)
exclude_categorical = ['EVMVersion', 'LicenseType', 'mostFrequentOpcode']
# Combine exclusions (but keep numeric columns that are object after loading?)
# Build exclusion dict with reasons
exclusions = {}
for c in exclude_contractID:
    exclusions[c] = 'identifier (contractID)'
for c in exclude_timestamp:
    exclusions[c] = 'temporal leakage (deployment timestamp)'
for c in exclude_compiler:
    exclusions[c] = 'compiler version (reserved for analysis)'
for c in exclude_categorical:
    exclusions[c] = 'categorical/non‑numeric (baseline numeric‑only)'
# Any other non‑numeric columns (object dtype) that are not already excluded
for c in non_numeric:
    if c not in exclusions:
        exclusions[c] = 'non‑numeric column'

# Determine retained columns (numeric dtype and not excluded)
retained = []
for c in all_columns:
    if c in exclusions:
        continue
    if pd.api.types.is_numeric_dtype(pre_df[c]):
        retained.append(c)
    else:
        # hidden identifier check – any column containing 'id' (case‑insensitive) and numeric
        if re.search(r'id', c, re.I) and pd.api.types.is_numeric_dtype(pre_df[c]):
            exclusions[c] = 'potential identifier (contains id)'
        else:
            exclusions[c] = 'non‑numeric column'

# Feature audit summary
feature_audit = []
for c in all_columns:
    dtype = str(pre_df[c].dtype)
    included = c not in exclusions
    reason = exclusions.get(c, '')
    feature_audit.append({
        'feature_name': c,
        'dtype': dtype,
        'feature_group': 'numeric' if pd.api.types.is_numeric_dtype(pre_df[c]) else 'non-numeric',
        'included': included,
        'exclusion_reason': reason
    })

# Save final feature list
final_feature_df = pd.DataFrame([f for f in feature_audit if f['included']])
final_feature_path = os.path.join(REPORT_DIR, 'final_feature_list.csv')
final_feature_df.to_csv(final_feature_path, index=False)

# Save audit table (full)
audit_path = os.path.join(REPORT_DIR, 'feature_audit.csv')
pd.DataFrame(feature_audit).to_csv(audit_path, index=False)

# Missing value counts and zero‑variance counts for retained features
missing_counts = pre_df[retained].isnull().sum()
zero_var = [c for c in retained if pre_df[c].nunique() == 1]

# Compiler family derivation (major version)
compiler_series = pre_df['CompilerVersion'].astype(str)
def family(v):
    m = re.search(r'v(\d+\.\d+)\.', v)
    return f"v{m.group(1)}.x" if m else 'unknown'
compiler_family = compiler_series.apply(family)
# Add year column from timestamp for temporal cohort
pre_df['year'] = pd.to_datetime(pre_df['timeStamp'], unit='s').dt.year
cohorts = {2022: 'validation', 2023: 'adaptation', 2024: 'test'}
# Produce compiler family counts per cohort
compiler_counts = {}
for year, label in cohorts.items():
    df_year = pre_df[pre_df['year'] == year]
    counts = df_year['CompilerVersion'].apply(family).value_counts().to_dict()
    compiler_counts[label] = counts

# Print summary
print('\n--- Feature audit summary ---')
print(f"Total original PRE columns: {len(all_columns)}")
print(f"Retained numeric features: {len(retained)}")
print(f"Excluded features: {len(exclusions)}")
print('Excluded columns:')
for col, reason in exclusions.items():
    print(f"  {col}: {reason}")
print('\nFirst 20 retained features:')
for col in retained[:20]:
    print(f"  {col}")
print('\nMissing value counts (retained):')
print(missing_counts[missing_counts>0])
print('\nZero‑variance features:')
print(zero_var)
print('\nCompiler family distribution by cohort:')
print(json.dumps(compiler_counts, indent=2))

# Also output counts for final report
print('\n--- End of audit ---')
