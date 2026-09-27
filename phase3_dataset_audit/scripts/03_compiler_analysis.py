"""
03_compiler_analysis.py
Audits Solidity compiler version distribution across calendar years and computes
the Year x Compiler vulnerability prevalence matrix.
Generates:
- phase3_dataset_audit/reports/compiler_by_year.csv
- phase3_dataset_audit/reports/compiler_major_families_by_year.csv
- phase3_dataset_audit/reports/labels_by_year_and_compiler.csv
"""

import os
import sys
import re
import pandas as pd
import numpy as np
import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_DIR = os.path.join(BASE_DIR, "raw")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

os.makedirs(REPORTS_DIR, exist_ok=True)

def normalize_compiler_version(v_str):
    if pd.isnull(v_str):
        return "Unknown / Missing"
    s = str(v_str).strip().lower()
    if s in ["", "nan", "none", "unknown"]:
        return "Unknown / Missing"
    
    # Extract version pattern like 0.4.24, 0.5.16, 0.8.20, etc.
    # Often formatted as v0.4.24+commit.e79f32ba or 0.4.24
    m = re.search(r'v?(\d+\.\d+\.\d+)', s)
    if m:
        exact = m.group(1)
        major_minor = re.match(r'(\d+\.\d+)', exact).group(1)
        family = f"v{major_minor}.x"
        return exact, family
    m2 = re.search(r'v?(\d+\.\d+)', s)
    if m2:
        major_minor = m2.group(1)
        return f"{major_minor}.0", f"v{major_minor}.x"
        
    return s, s

def run_compiler_analysis():
    print("=== Step 3: Year x Compiler Confounder Analysis ===")
    
    # Load PRE data (contains CompilerVersion and timestamp)
    pre_path = os.path.join(RAW_DIR, "Preprocessed", "PRE", "PRE_ProcessedData.csv")
    if not os.path.exists(pre_path):
        raise FileNotFoundError(f"PRE file not found: {pre_path}")
    pre_df = pd.read_csv(pre_path, low_memory=False)

    # Verify required columns
    required_pre_cols = ["contractID", "timeStamp", "CompilerVersion"]
    for col in required_pre_cols:
        if col not in pre_df.columns:
            raise ValueError(f"Expected column '{col}' not found in PRE_ProcessedData.csv")

    # Load labels
    labels_file = os.path.join(RAW_DIR, "Labels", "DIVE_Labels.csv")
    if not os.path.exists(labels_file):
        for root, dirs, files in os.walk(RAW_DIR):
            for f in files:
                if f.lower() == "dive_labels.csv" and "__MACOSX" not in root:
                    labels_file = os.path.join(root, f)
                    break
    labels_df = pd.read_csv(labels_file, low_memory=False)

    # Merge on contractID
    merged = pd.merge(labels_df, pre_df, left_on="contractID", right_on="contractID", how="inner", suffixes=("_lbl", "_feat"))

    # Locate labels and timestamps
    # Load labels
    labels_file = os.path.join(RAW_DIR, "Labels", "DIVE_Labels.csv")
    if not os.path.exists(labels_file):
        for root, dirs, files in os.walk(RAW_DIR):
            for f in files:
                if f.lower() == "dive_labels.csv" and "__MACOSX" not in root:
                    labels_file = os.path.join(root, f)
                    break
                    
    labels_df = pd.read_csv(labels_file, low_memory=False)
    
    # Identify address columns to join
    # Use explicit timestamp column from PRE data
    ts_col_merged = "timeStamp"
        
    def parse_to_year(val):
        if pd.isnull(val):
            return np.nan
        try:
            num = float(val)
            if num > 1e11:
                num = num / 1000.0
            if num > 1e8:
                return datetime.datetime.utcfromtimestamp(num).year
        except (ValueError, TypeError):
            pass
        try:
            return pd.to_datetime(val).year
        except Exception:
            return np.nan

    merged["deployment_year"] = merged[ts_col_merged].apply(parse_to_year)
    
    # Raw compiler version
    raw_comp_col = next((c for c in merged.columns if any(k in c.lower() for k in ["compiler", "solc", "version"])), None)
    merged["raw_compiler_version"] = merged[raw_comp_col]
    
    # Normalized versions
    exact_versions = []
    major_families = []
    for val in merged["raw_compiler_version"]:
        exact_v, fam = normalize_compiler_version(val)
        exact_versions.append(exact_v)
        major_families.append(fam)
        
    merged["normalized_exact_compiler"] = exact_versions
    merged["compiler_major_family"] = major_families
    
    # 1. compiler_by_year.csv (Exact raw / normalized compiler versions per year)
    records_comp_year = []
    for yr, yr_group in merged.groupby("deployment_year", dropna=False):
        yr_str = "Missing / Invalid" if pd.isnull(yr) else str(int(yr))
        yr_total = len(yr_group)
        comp_counts = yr_group["raw_compiler_version"].value_counts(dropna=False)
        for comp, count in comp_counts.items():
            comp_str = "Missing / Null" if pd.isnull(comp) else str(comp)
            exact_norm, fam = normalize_compiler_version(comp)
            records_comp_year.append({
                "year": yr_str,
                "raw_compiler_version": comp_str,
                "normalized_version": exact_norm,
                "compiler_family": fam,
                "contract_count": count,
                "percentage_within_year": round((count / yr_total) * 100, 3)
            })
            
    cby_df = pd.DataFrame(records_comp_year)
    cby_path = os.path.join(REPORTS_DIR, "compiler_by_year.csv")
    cby_df.to_csv(cby_path, index=False)
    print(f"[SAVED] {cby_path}")
    
    # 2. compiler_major_families_by_year.csv
    fam_records = []
    for yr, yr_group in merged.groupby("deployment_year", dropna=False):
        yr_str = "Missing / Invalid" if pd.isnull(yr) else str(int(yr))
        yr_total = len(yr_group)
        fam_counts = yr_group["compiler_major_family"].value_counts(dropna=False)
        for fam, count in fam_counts.items():
            fam_records.append({
                "year": yr_str,
                "compiler_family": fam,
                "contract_count": count,
                "percentage_within_year": round((count / yr_total) * 100, 3)
            })
    fam_df = pd.DataFrame(fam_records)
    fam_path = os.path.join(REPORTS_DIR, "compiler_major_families_by_year.csv")
    fam_df.to_csv(fam_path, index=False)
    print(f"[SAVED] {fam_path}")

    # 3. labels_by_year_and_compiler.csv
    dasp_categories = [
        ("reentrancy", ["reentrancy", "reentrant"]),
        ("access_control", ["access_control", "accesscontrol", "access"]),
        ("arithmetic", ["arithmetic", "overflow", "underflow", "integer_overflow"]),
        ("unchecked_low_level_calls", ["unchecked_low_level_calls", "unchecked_call", "unchecked_calls", "unchecked"]),
        ("dos", ["denial_of_service", "dos"]),
        ("bad_randomness", ["bad_randomness", "randomness", "random"]),
        ("front_running", ["front_running", "frontrunning", "front_run"]),
        ("time_manipulation", ["time_manipulation", "timestamp_dependency", "time", "timestamp"])
    ]
    
    matched_label_cols = {}
    for standard_name, aliases in dasp_categories:
        for col in labels_df.columns:
            c_norm = col.lower().replace("-", "_").replace(" ", "_")
            if any(alias == c_norm or alias in c_norm for alias in aliases):
                matched_label_cols[standard_name] = col
                break

    matrix_records = []
    for (yr, fam), group in merged.groupby(["deployment_year", "compiler_major_family"], dropna=False):
        yr_str = "Missing / Invalid" if pd.isnull(yr) else str(int(yr))
        group_total = len(group)
        
        row_dict = {
            "year": yr_str,
            "compiler_family": fam,
            "total_contracts": group_total
        }
        
        for cat_key in matched_label_cols:
            col_name = matched_label_cols[cat_key]
            # Handle potential duplicate column names after merge
            c_series = group[col_name]
            if isinstance(c_series, pd.DataFrame):
                c_series = c_series.iloc[:, 0]
            pos_cnt = int((c_series == 1).sum() if c_series.dtype in [int, float, bool] else (c_series.astype(str).str.strip().isin(["1", "True", "true", "1.0"])).sum())
            row_dict[f"{cat_key}_positive"] = pos_cnt
            row_dict[f"{cat_key}_pct"] = round((pos_cnt / group_total * 100), 2) if group_total > 0 else 0.0
            
        matrix_records.append(row_dict)
        
    mat_df = pd.DataFrame(matrix_records)
    mat_path = os.path.join(REPORTS_DIR, "labels_by_year_and_compiler.csv")
    mat_df.to_csv(mat_path, index=False)
    print(f"[SAVED] {mat_path}")

if __name__ == "__main__":
    run_compiler_analysis()
