"""
02_temporal_and_labels.py
Audits deployment timestamps and 8-class DASP multi-label vulnerability distributions.

Timestamp source: raw/Preprocessed/PRE/PRE_ProcessedData.csv  (column: timeStamp)
Label source:     raw/Labels/DIVE_Labels.csv

Generates:
- phase3_dataset_audit/reports/contracts_per_year.csv
- phase3_dataset_audit/reports/labels_by_year.csv
- phase3_dataset_audit/reports/label_prevalence_summary.csv
- phase3_dataset_audit/reports/label_cooccurrence_matrix.csv
"""

import os
import sys
import pandas as pd
import numpy as np
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "raw")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

os.makedirs(REPORTS_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Hard-coded file paths -- do NOT use generic substring matching to find these
# ---------------------------------------------------------------------------
LABELS_PATH = os.path.join(RAW_DIR, "Labels", "DIVE_Labels.csv")
PRE_PATH    = os.path.join(RAW_DIR, "Preprocessed", "PRE", "PRE_ProcessedData.csv")

# The exact column names expected in each file
LABEL_ID_COL      = "contractID"
PRE_ID_COL        = "contractID"
PRE_TIMESTAMP_COL = "timeStamp"

# Sanity bounds for deployment years (Ethereum mainnet launched mid-2015)
YEAR_MIN = 2015
YEAR_MAX = datetime.datetime.utcnow().year


def normalize_id(series):
    """Convert contractID to a normalised string (str, strip, lowercase)."""
    return series.astype(str).str.strip().str.lower()


def parse_to_year(val):
    """
    Parse a single timestamp value to a calendar year.
    - Accepts Unix seconds (>= 1e8) or Unix milliseconds (>= 1e11).
    - Accepts ISO datetime strings.
    - Rejects values that are clearly 0/1 vulnerability flags (< 2).
    - Rejects years outside [YEAR_MIN, YEAR_MAX].
    - Returns np.nan for anything invalid/missing.
    """
    if pd.isnull(val):
        return np.nan
    try:
        num = float(val)
        # Explicitly reject 0 and 1 -- these are vulnerability flags, not timestamps
        if num < 2:
            return np.nan
        if num >= 1e11:  # milliseconds -> convert to seconds
            num = num / 1000.0
        if num >= 1e8:   # plausible Unix-seconds range
            dt = datetime.datetime.utcfromtimestamp(num)
            yr = dt.year
            if YEAR_MIN <= yr <= YEAR_MAX:
                return yr
            else:
                return np.nan  # out-of-range -> invalid
    except (ValueError, OSError, OverflowError, TypeError):
        pass
    # Try datetime string
    try:
        dt = pd.to_datetime(val, utc=True)
        yr = dt.year
        if YEAR_MIN <= yr <= YEAR_MAX:
            return yr
    except Exception:
        pass
    return np.nan


def to_binary(series):
    """Binarise a label column robustly."""
    if series.dtype in [int, float, bool, np.int64, np.float64]:
        return (series == 1).astype(int)
    return series.astype(str).str.strip().isin(["1", "True", "true", "1.0"]).astype(int)


def analyze_temporal_and_labels():
    print("=== Step 2: Temporal Distribution and Multi-Label Vulnerability Audit ===\n")

    # ------------------------------------------------------------------
    # 1. Load files with explicit paths -- verify required columns exist
    # ------------------------------------------------------------------
    if not os.path.exists(LABELS_PATH):
        raise FileNotFoundError(f"Labels file not found: {LABELS_PATH}")
    labels_df = pd.read_csv(LABELS_PATH, low_memory=False)
    print(f"Labels file : {LABELS_PATH}")
    print(f"  Rows: {len(labels_df):,}  |  Columns: {list(labels_df.columns)}")
    if LABEL_ID_COL not in labels_df.columns:
        raise ValueError(
            f"Expected column '{LABEL_ID_COL}' not found in DIVE_Labels.csv. "
            f"Available: {list(labels_df.columns)}"
        )

    if not os.path.exists(PRE_PATH):
        raise FileNotFoundError(f"PRE file not found: {PRE_PATH}")
    pre_df = pd.read_csv(PRE_PATH, low_memory=False)
    print(f"\nPRE file    : {PRE_PATH}")
    print(f"  Rows: {len(pre_df):,}  |  First 10 columns: {list(pre_df.columns)[:10]}")
    for required in [PRE_ID_COL, PRE_TIMESTAMP_COL]:
        if required not in pre_df.columns:
            raise ValueError(
                f"Expected column '{required}' not found in PRE_ProcessedData.csv. "
                f"Available: {list(pre_df.columns)}"
            )

    # ------------------------------------------------------------------
    # 2. Join diagnostics -- abort on duplicates or zero matches
    # ------------------------------------------------------------------
    labels_df = labels_df.copy()
    pre_df    = pre_df.copy()
    labels_df["_join_id"] = normalize_id(labels_df[LABEL_ID_COL])
    pre_df["_join_id"]    = normalize_id(pre_df[PRE_ID_COL])

    label_ids    = set(labels_df["_join_id"])
    pre_ids      = set(pre_df["_join_id"])
    matched      = label_ids & pre_ids
    labels_no_pre = label_ids - pre_ids
    pre_no_labels = pre_ids   - label_ids
    dup_labels   = labels_df[labels_df["_join_id"].duplicated(keep=False)]["_join_id"].nunique()
    dup_pre      = pre_df[pre_df["_join_id"].duplicated(keep=False)]["_join_id"].nunique()

    print("\n--- Join Diagnostics ---")
    print(f"  Label rows              : {len(labels_df):,}")
    print(f"  PRE rows                : {len(pre_df):,}")
    print(f"  Matching contractIDs    : {len(matched):,}")
    print(f"  Labels without PRE      : {len(labels_no_pre):,}")
    print(f"  PRE without labels      : {len(pre_no_labels):,}")
    print(f"  Duplicate IDs in Labels : {dup_labels:,}")
    print(f"  Duplicate IDs in PRE    : {dup_pre:,}")

    if dup_labels > 0:
        raise ValueError(
            f"ABORT: {dup_labels} contractID(s) appear more than once in DIVE_Labels.csv. "
            "The join is not one-to-one."
        )
    if dup_pre > 0:
        raise ValueError(
            f"ABORT: {dup_pre} contractID(s) appear more than once in PRE_ProcessedData.csv. "
            "The join is not one-to-one."
        )
    if len(matched) == 0:
        raise ValueError(
            "ABORT: No matching contractIDs between DIVE_Labels.csv and PRE_ProcessedData.csv."
        )

    # ------------------------------------------------------------------
    # 3. Merge -- left join so every label row is preserved
    # ------------------------------------------------------------------
    merged_df = pd.merge(
        labels_df,
        pre_df[["_join_id", PRE_TIMESTAMP_COL]],
        on="_join_id",
        how="left"
    )

    # ------------------------------------------------------------------
    # 4. Report timestamp source
    #    IMPORTANT: timeStamp column is taken ONLY from PRE_ProcessedData.csv.
    #    DIVE_Labels.csv is the vulnerability-label source only.
    # ------------------------------------------------------------------
    ts_raw = merged_df[PRE_TIMESTAMP_COL]
    print(f"\nTimestamp source: PRE_ProcessedData.csv")
    print(f"Timestamp column: {PRE_TIMESTAMP_COL}")
    print(f"Sample raw timestamps: {ts_raw.dropna().head(10).tolist()}")

    # ------------------------------------------------------------------
    # 5. Parse timestamps -> deployment year
    # ------------------------------------------------------------------
    years = ts_raw.apply(parse_to_year)
    merged_df["deployment_year"] = years

    total_contracts   = len(merged_df)
    matched_contracts = int(ts_raw.notna().sum())
    missing_ts        = int(years.isnull().sum())
    missing_pre       = int(ts_raw.isna().sum())
    valid_years       = years.dropna().astype(int)

    print(f"\n--- Pre-Save Validation Summary ---")
    print(f"  Total contracts            : {total_contracts:,}")
    print(f"  Matched contracts (PRE)    : {matched_contracts:,}")
    print(f"  Missing PRE records        : {missing_pre:,}")
    print(f"  Missing/invalid timestamps : {missing_ts:,} ({missing_ts / total_contracts * 100:.2f}%)")
    if len(valid_years) > 0:
        print(f"  Earliest deployment year   : {valid_years.min()}")
        print(f"  Latest deployment year     : {valid_years.max()}")
    else:
        print("  [WARNING] No valid deployment years found.")

    # Guard: refuse to save if all valid years are 1970
    if len(valid_years) > 0:
        unique_years_found = set(valid_years.unique())
        if unique_years_found == {1970}:
            raise ValueError(
                "ABORT: All parsed deployment years are 1970. "
                "0/1 vulnerability labels were incorrectly treated as Unix timestamps. "
                "Check the timestamp column source and parsing logic."
            )
        if all(y < YEAR_MIN for y in unique_years_found):
            raise ValueError(
                f"ABORT: All parsed deployment years {sorted(unique_years_found)} are before "
                f"{YEAR_MIN}. Ethereum did not exist then. "
                "Check the timestamp column source and parsing logic."
            )

    # Print year distribution before saving
    year_counts = merged_df["deployment_year"].value_counts(dropna=False).sort_index()
    print("\n--- Contracts per Year ---")
    for yr, cnt in year_counts.items():
        yr_label = "Missing / Invalid" if pd.isnull(yr) else str(int(yr))
        pct = cnt / total_contracts * 100
        print(f"  {yr_label}: {cnt:,} contracts ({pct:.2f}%)")

    # ------------------------------------------------------------------
    # 6. Save contracts_per_year.csv
    # ------------------------------------------------------------------
    contracts_per_year_data = []
    for yr, cnt in year_counts.items():
        yr_label = "Missing / Invalid" if pd.isnull(yr) else str(int(yr))
        pct = round(cnt / total_contracts * 100, 3)
        contracts_per_year_data.append({
            "year": yr_label,
            "contract_count": int(cnt),
            "percentage_of_dataset": pct
        })
    cpy_df = pd.DataFrame(contracts_per_year_data)
    cpy_path = os.path.join(REPORTS_DIR, "contracts_per_year.csv")
    cpy_df.to_csv(cpy_path, index=False)
    print(f"\n[SAVED] {cpy_path}")

    # ------------------------------------------------------------------
    # 7. DASP 8 category mapping
    #    Use EXACT column names from DIVE_Labels.csv -- no substring match.
    #    'Time manipulation' is a vulnerability label, NOT a timestamp.
    # ------------------------------------------------------------------
    dasp_exact_map = {
        "reentrancy":               "Reentrancy",
        "access_control":           "Access Control",
        "arithmetic":               "Arithmetic",
        "unchecked_low_level_calls": "Unchecked Return Values",
        "dos":                      "DoS",
        "bad_randomness":           "Bad Randomness",
        "front_running":            "Front Running",
        "time_manipulation":        "Time manipulation",
    }

    missing_label_cols = [
        (std, col) for std, col in dasp_exact_map.items()
        if col not in labels_df.columns
    ]
    if missing_label_cols:
        print(f"\n[WARNING] DASP columns not found in DIVE_Labels.csv:")
        for std, col in missing_label_cols:
            print(f"  {std} -> '{col}'")
        for std, _ in missing_label_cols:
            del dasp_exact_map[std]

    print("\n--- DASP 8 Categories Column Mapping ---")
    for std_name, actual_col in dasp_exact_map.items():
        print(f"  {std_name} -> '{actual_col}'")

    # Build binary label matrix
    binary_label_df = pd.DataFrame(index=merged_df.index)
    for std_name, col in dasp_exact_map.items():
        binary_label_df[std_name] = to_binary(merged_df[col])

    # ------------------------------------------------------------------
    # 8. labels_by_year.csv
    # ------------------------------------------------------------------
    unique_years_list = sorted([y for y in merged_df["deployment_year"].unique() if pd.notnull(y)])
    year_buckets = [(yr, False) for yr in unique_years_list]
    if missing_ts > 0:
        year_buckets.append((np.nan, True))

    records_by_year = []
    for yr, is_missing in year_buckets:
        if is_missing:
            sub_idx = merged_df["deployment_year"].isnull()
            yr_str  = "Missing / Invalid"
        else:
            sub_idx = merged_df["deployment_year"] == yr
            yr_str  = str(int(yr))
        sub_count = int(sub_idx.sum())
        row_dict  = {"year": yr_str, "total_contracts": sub_count}
        for std_name in dasp_exact_map:
            pos_count = int(binary_label_df.loc[sub_idx, std_name].sum())
            pct = round(pos_count / sub_count * 100, 2) if sub_count > 0 else 0.0
            row_dict[f"{std_name}_positive"] = pos_count
            row_dict[f"{std_name}_pct"]      = pct
        records_by_year.append(row_dict)

    lby_df  = pd.DataFrame(records_by_year)
    lby_path = os.path.join(REPORTS_DIR, "labels_by_year.csv")
    lby_df.to_csv(lby_path, index=False)
    print(f"[SAVED] {lby_path}")

    # ------------------------------------------------------------------
    # 9. label_prevalence_summary.csv
    # ------------------------------------------------------------------
    prev_records = []
    for std_name, col in dasp_exact_map.items():
        pos_cnt = int(binary_label_df[std_name].sum())
        prev_records.append({
            "vulnerability_category": std_name,
            "column_in_dive":         col,
            "positive_contracts":     pos_cnt,
            "prevalence_pct":         round(pos_cnt / total_contracts * 100, 3),
        })
    prev_df  = pd.DataFrame(prev_records)
    prev_path = os.path.join(REPORTS_DIR, "label_prevalence_summary.csv")
    prev_df.to_csv(prev_path, index=False)
    print(f"[SAVED] {prev_path}")

    # ------------------------------------------------------------------
    # 10. label_cooccurrence_matrix.csv
    # ------------------------------------------------------------------
    cooccur      = binary_label_df.T.dot(binary_label_df)
    cooccur_path = os.path.join(REPORTS_DIR, "label_cooccurrence_matrix.csv")
    cooccur.to_csv(cooccur_path)
    print(f"[SAVED] {cooccur_path}")

    # ------------------------------------------------------------------
    # 11. Multi-label count distribution per contract
    # ------------------------------------------------------------------
    labels_per_contract = binary_label_df.sum(axis=1)
    label_count_dist    = labels_per_contract.value_counts().sort_index()
    print("\n--- Label Count Distribution per Contract ---")
    for cnt, num_c in label_count_dist.items():
        print(f"  {cnt} vulnerabilities: {num_c:,} contracts ({num_c / total_contracts * 100:.2f}%)")

    print("\n=== Step 2 Complete ===")


if __name__ == "__main__":
    analyze_temporal_and_labels()
