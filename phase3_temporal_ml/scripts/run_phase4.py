import pandas as pd
import numpy as np
import os
import json
from pathlib import Path
from scipy.stats import wasserstein_distance, ks_2samp
from statsmodels.stats.multitest import multipletests
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import hashlib

# Set deterministic environment
np.random.seed(42)

# Paths
BASE_DIR = Path('c:/Users/LAPTOPS24/Documents/HRISHITA/CLG/Blockchain/demo1/phase3_temporal_ml')
DATA_DIR = BASE_DIR / 'raw'
REPORT_DIR = BASE_DIR / 'reports'
FIG_DIR = REPORT_DIR / 'figures'
SCRIPT_DIR = BASE_DIR / 'scripts'

# Ensure report directories exist
REPORT_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Load data
pre_path = DATA_DIR / 'Preprocessed' / 'PRE' / 'PRE_ProcessedData.csv'
labels_path = DATA_DIR / 'Labels' / 'DIVE_Labels.csv'
feature_list_path = BASE_DIR / 'reports' / 'final_feature_list.csv'

pre_df = pd.read_csv(pre_path)
labels_df = pd.read_csv(labels_path)
feature_list = pd.read_csv(feature_list_path)

# Keep only the 215 retained numeric features (excluded ones flagged in final_feature_list)
retained_features = feature_list[feature_list['included'] == True]['feature_name'].tolist()
X = pre_df[retained_features].copy()

# Merge with labels on contractID
merged = X.merge(labels_df, on='contractID')

# Derive year from timestamp (UNIX seconds)
merged['year'] = pd.to_datetime(merged['timeStamp'], unit='s').dt.year

# Cohort definitions (exact as Phase 3B)
cohort_map = {
    'train': merged[merged['year'].between(2016, 2021)],
    'validation': merged[merged['year'] == 2022],
    'adaptation': merged[merged['year'] == 2023],
    'test': merged[merged['year'] == 2024]
}

# ---------- PART A: Feature distribution shift ----------
comparisons = [
    ('train', 'validation'),
    ('validation', 'adaptation'),
    ('adaptation', 'test'),
    ('train', 'test')
]

feature_shift_records = []
summary_records = []

for grp1, grp2 in comparisons:
    df1 = cohort_map[grp1]
    df2 = cohort_map[grp2]
    pvals = []
    stats = []
    for feat in retained_features:
        x1 = df1[feat].dropna()
        x2 = df2[feat].dropna()
        mean1, mean2 = x1.mean(), x2.mean()
        median1, median2 = x1.median(), x2.median()
        std1, std2 = x1.std(ddof=0), x2.std(ddof=0)
        iqr1 = np.percentile(x1, 75) - np.percentile(x1, 25)
        iqr2 = np.percentile(x2, 75) - np.percentile(x2, 25)
        pooled_std = np.sqrt((std1 ** 2 + std2 ** 2) / 2)
        d = (mean1 - mean2) / pooled_std if pooled_std != 0 else 0.0
        wd = wasserstein_distance(x1, x2)
        ks_stat, ks_p = ks_2samp(x1, x2)
        pvals.append(ks_p)
        stats.append({
            'feature': feat,
            'group1': grp1,
            'group2': grp2,
            'mean1': mean1,
            'mean2': mean2,
            'median1': median1,
            'median2': median2,
            'std1': std1,
            'std2': std2,
            'iqr1': iqr1,
            'iqr2': iqr2,
            'cohen_d': d,
            'wasserstein': wd,
            'ks_stat': ks_stat,
            'ks_p': ks_p
        })
    # Benjamini-Hochberg FDR
    reject, qvals, _, _ = multipletests(pvals, alpha=0.05, method='fdr_bh')
    meaningful_thresh_d = 0.2
    meaningful_thresh_wd = 0.1
    sig_count = int(reject.sum())
    meaningful_count = sum((abs(s['cohen_d']) >= meaningful_thresh_d) or (s['wasserstein'] >= meaningful_thresh_wd) for s in stats)
    for i, s in enumerate(stats):
        s.update({
            'ks_significant': bool(reject[i]),
            'q_value': qvals[i],
            'meaningful': (abs(s['cohen_d']) >= meaningful_thresh_d) or (s['wasserstein'] >= meaningful_thresh_wd)
        })
        feature_shift_records.append(s)
    summary_records.append({
        'comparison': f"{grp1}_vs_{grp2}",
        'features_tested': len(retained_features),
        'significant_shift': sig_count,
        'meaningful_shift': meaningful_count
    })

# Save detailed shift table
feature_shift_df = pd.DataFrame(feature_shift_records)
feature_shift_df.to_csv(REPORT_DIR / 'phase4_feature_shift.csv', index=False)

# Save summary
summary_df = pd.DataFrame(summary_records)
summary_df.to_csv(REPORT_DIR / 'phase4_feature_shift_summary.csv', index=False)

# ---------- TOP 20 shifted features (by max absolute Cohen's d across comparisons) ----------
feature_shift_df['abs_cohen_d'] = feature_shift_df['cohen_d'].abs()
max_abs = feature_shift_df.groupby('feature')['abs_cohen_d'].max().sort_values(ascending=False).head(20)
top_features = feature_shift_df[feature_shift_df['feature'].isin(max_abs.index)]
# Keep rows where the abs_cohen_d equals the max for that feature (first occurrence)
top_df = top_features.loc[top_features.groupby('feature')['abs_cohen_d'].idxmax()]
top_df.to_csv(REPORT_DIR / 'phase4_top_shifted_features.csv', index=False)

# ---------- PART B: Vulnerability prevalence ----------
vuln_cols = [c for c in labels_df.columns if c != 'contractID']
prevalence_records = []
# Yearly prevalence (including combined 2016-2021)
for yr in range(2016, 2025):
    df_year = merged[merged['year'] == yr]
    total = len(df_year)
    for vuln in vuln_cols:
        pos = df_year[vuln].sum()
        prevalence = pos / total if total else np.nan
        prevalence_records.append({
            'vulnerability': vuln,
            'period': str(yr),
            'positive_count': int(pos),
            'total_count': int(total),
            'prevalence': prevalence
        })
# Combined periods
combined = {
    '2016-2021': merged[merged['year'].between(2016, 2021)],
    '2022': merged[merged['year'] == 2022],
    '2023': merged[merged['year'] == 2023],
    '2024': merged[merged['year'] == 2024]
}
for name, df in combined.items():
    total = len(df)
    for vuln in vuln_cols:
        pos = df[vuln].sum()
        prevalence = pos / total if total else np.nan
        prevalence_records.append({
            'vulnerability': vuln,
            'period': name,
            'positive_count': int(pos),
            'total_count': int(total),
            'prevalence': prevalence
        })
prev_df = pd.DataFrame(prevalence_records)
# Compute absolute & relative changes relative to previous period (ordered by period string)
prev_df.sort_values(['vulnerability', 'period'], inplace=True)
prev_df['abs_change'] = np.nan
prev_df['rel_change'] = np.nan
for vuln in vuln_cols:
    sub = prev_df[prev_df['vulnerability'] == vuln].reset_index(drop=True)
    for i in range(1, len(sub)):
        prev = sub.loc[i-1]
        cur = sub.loc[i]
        if pd.notnull(prev['prevalence']) and pd.notnull(cur['prevalence']):
            diff = cur['prevalence'] - prev['prevalence']
            rel = diff / prev['prevalence'] if prev['prevalence'] != 0 else np.nan
            prev_df.loc[sub.index[i], 'abs_change'] = diff
            prev_df.loc[sub.index[i], 'rel_change'] = rel
prev_df.to_csv(REPORT_DIR / 'phase4_vulnerability_prevalence.csv', index=False)

# ---------- PART C: Compiler confounding ----------
import re

def compiler_family(ver):
    m = re.search(r'v(\d+\.\d+)', str(ver))
    return f"v{m.group(1)}" if m else 'unknown'

merged['compiler_family'] = merged['CompilerVersion'].apply(compiler_family)
compiler_summary = []
for cohort_name, df in cohort_map.items():
    total = len(df)
    counts = df['compiler_family'].value_counts()
    for fam, cnt in counts.items():
        compiler_summary.append({
            'cohort': cohort_name,
            'compiler_family': fam,
            'count': int(cnt),
            'percentage': cnt / total if total else np.nan
        })
compiler_summary_df = pd.DataFrame(compiler_summary)
compiler_summary_df.to_csv(REPORT_DIR / 'phase4_compiler_summary.csv', index=False)

# Vulnerability prevalence by compiler family (minimum sample size 30 as in Phase 3A)
min_samples = 30
vuln_compiler = []
for cohort_name, df in cohort_map.items():
    for fam, fam_df in df.groupby('compiler_family'):
        if len(fam_df) < min_samples:
            continue
        for vuln in vuln_cols:
            pos = fam_df[vuln].sum()
            total = len(fam_df)
            prev = pos / total if total else np.nan
            vuln_compiler.append({
                'cohort': cohort_name,
                'compiler_family': fam,
                'vulnerability': vuln,
                'positive_count': int(pos),
                'total_count': int(total),
                'prevalence': prev
            })
pd.DataFrame(vuln_compiler).to_csv(REPORT_DIR / 'phase4_vuln_by_compiler.csv', index=False)

# ---------- PART D: Compiler‑stratified temporal analysis ----------
strat_records = []
for fam, fam_df in merged.groupby('compiler_family'):
    if len(fam_df) < min_samples:
        continue
    fam_cohorts = {
        'train': fam_df[fam_df['year'].between(2016, 2021)],
        'validation': fam_df[fam_df['year'] == 2022],
        'adaptation': fam_df[fam_df['year'] == 2023],
        'test': fam_df[fam_df['year'] == 2024]
    }
    for grp1, grp2 in comparisons:
        d1 = fam_cohorts[grp1]
        d2 = fam_cohorts[grp2]
        if len(d1) < min_samples or len(d2) < min_samples:
            continue
        for feat in retained_features:
            x1 = d1[feat].dropna()
            x2 = d2[feat].dropna()
            if x1.empty or x2.empty:
                continue
            mean1, mean2 = x1.mean(), x2.mean()
            std1, std2 = x1.std(ddof=0), x2.std(ddof=0)
            pooled = np.sqrt((std1 ** 2 + std2 ** 2) / 2)
            d = (mean1 - mean2) / pooled if pooled != 0 else 0.0
            wd = wasserstein_distance(x1, x2)
            ks_stat, ks_p = ks_2samp(x1, x2)
            strat_records.append({
                'compiler_family': fam,
                'feature': feat,
                'comparison': f"{grp1}_vs_{grp2}",
                'cohen_d': d,
                'wasserstein': wd,
                'ks_stat': ks_stat,
                'ks_p': ks_p
            })
strat_df = pd.DataFrame(strat_records)
strat_df.to_csv(REPORT_DIR / 'phase4_compiler_stratified_analysis.csv', index=False)

# ---------- PART E: Summary JSON ----------
summary = {
    'retained_feature_count': len(retained_features),
    'feature_shift_summary': summary_records,
    'top_shifted_features': top_df[['feature', 'group1', 'group2', 'cohen_d', 'wasserstein', 'ks_stat']].to_dict(orient='records'),
    'vulnerability_prevalence_snapshot': prev_df.head().to_dict(orient='records'),
    'compiler_summary_snapshot': compiler_summary_df.head().to_dict(orient='records'),
    'compiler_stratified_rows': len(strat_df),
    'deterministic': True
}
with open(REPORT_DIR / 'phase4_summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

# ---------- Figures ----------
# 1. Heatmap of mean absolute Cohen's d per feature/comparison
heat = feature_shift_df.groupby(['feature', 'comparison'])['abs_cohen_d'].mean().unstack(fill_value=0)
plt.figure(figsize=(12, 10))
sns.heatmap(heat, cmap='viridis')
plt.title("Mean Absolute Cohen's d per Feature & Comparison")
plt.tight_layout()
plt.savefig(FIG_DIR / 'temporal_feature_shift_overview.png')
plt.close()

# 2. Vulnerability prevalence over years (line plot)
plt.figure(figsize=(10, 6))
for vuln in vuln_cols:
    sub = prev_df[prev_df['vulnerability'] == vuln]
    yearly = sub[sub['period'].str.isnumeric()]
    plt.plot(yearly['period'].astype(int), yearly['prevalence'], marker='o', label=vuln)
plt.xlabel('Year')
plt.ylabel('Prevalence')
plt.title('Vulnerability Prevalence Over Years')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(FIG_DIR / 'vulnerability_prevalence_over_time.png')
plt.close()

# 3. Compiler distribution over time (stacked bar chart)
comp_year = merged.groupby(['year', 'compiler_family']).size().unstack(fill_value=0)
comp_year.plot(kind='bar', stacked=True, figsize=(10, 6))
plt.xlabel('Year')
plt.ylabel('Number of Contracts')
plt.title('Compiler Family Distribution Over Time')
plt.tight_layout()
plt.savefig(FIG_DIR / 'compiler_distribution_over_time.png')
plt.close()

# 4. Top 20 shifted features bar chart
plt.figure(figsize=(12, 6))
order = top_df.sort_values('abs_cohen_d', ascending=False)['feature']
sns.barplot(data=top_df, x='feature', y='abs_cohen_d', order=order)
plt.xticks(rotation=90)
plt.ylabel('Absolute Cohen\'s d')
plt.title('Top 20 Shifted Features')
plt.tight_layout()
plt.savefig(FIG_DIR / 'top_feature_shifts.png')
plt.close()

# ---------- Verification hashes ----------
hashes = []
for fname in ['phase4_feature_shift.csv','phase4_feature_shift_summary.csv','phase4_top_shifted_features.csv','phase4_vulnerability_prevalence.csv','phase4_compiler_summary.csv','phase4_compiler_stratified_analysis.csv']:
    path = REPORT_DIR / fname
    h = hashlib.sha256(path.read_bytes()).hexdigest()
    hashes.append({'file': fname, 'sha256': h})
pd.DataFrame(hashes).to_csv(REPORT_DIR / 'phase4_output_hashes.csv', index=False)
print('Phase 4 analysis complete. Hash file written.')
