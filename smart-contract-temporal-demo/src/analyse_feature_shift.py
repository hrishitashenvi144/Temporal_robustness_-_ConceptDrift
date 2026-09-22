"""
Standalone Feature-Distribution Shift Analysis Utility
======================================================

Calculates distribution shifts across temporal cohorts (period_old, period_medium, period_new)
using identical definitions to the primary experimental pipeline.
"""

import os
import pandas as pd

from compare_static_vs_adaptive import (
    DATA_PATH,
    FEATURE_COLS,
    FEATURE_SHIFT_CSV_PATH,
    TARGET_COL,
    COHORT_ORDER,
    validate_dataset,
    compute_feature_shift_analysis
)


def main():
    print("=" * 80)
    print("STANDALONE FEATURE SHIFT ANALYSIS")
    print("=" * 80)

    # Validate dataset
    df = validate_dataset(DATA_PATH, FEATURE_COLS, TARGET_COL, COHORT_ORDER)

    # Compute feature shift
    shift_df = compute_feature_shift_analysis(df, FEATURE_COLS)

    print("\nFeature-Distribution Shift Results:")
    print("-" * 80)
    for _, row in shift_df.iterrows():
        print(f"\nFeature: {row['Feature']}")
        print(f"  Old Mean:      {row['Old_Mean']:.3f} (Std: {row['Old_Std']:.3f})")
        print(f"  Medium Mean:   {row['Medium_Mean']:.3f} (Std: {row['Medium_Std']:.3f})")
        print(f"  New Mean:      {row['New_Mean']:.3f} (Std: {row['New_Std']:.3f})")
        print(f"  Old -> Medium: {row['Old_to_Medium_%']:+.2f}%")
        print(f"  Old -> New:    {row['Old_to_New_%']:+.2f}%")

    os.makedirs(os.path.dirname(FEATURE_SHIFT_CSV_PATH), exist_ok=True)
    shift_df.to_csv(FEATURE_SHIFT_CSV_PATH, index=False)
    print("\n" + "=" * 80)
    print(f"Saved feature-shift analysis to: {FEATURE_SHIFT_CSV_PATH}")


if __name__ == "__main__":
    main()