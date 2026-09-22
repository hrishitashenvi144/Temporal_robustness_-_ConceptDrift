import pandas as pd
import numpy as np

# Load extracted features
df = pd.read_csv('data/raw/poc_data/contracts_with_features.csv')

print("Adding temporal variations to simulate code evolution...")

# Set seed for reproducibility
np.random.seed(42)

# Add variations per period
# Simulates: Code patterns change over time
modified_df = df.copy()

for idx, row in modified_df.iterrows():
    period = row['period']
    
    # Period-specific variations
    if period == 'period_old':
        # Old code: More complex, more issues
        noise = np.random.normal(1.0, 0.05)  # +5% variation
        
    elif period == 'period_medium':
        # Medium code: Some improvements
        noise = np.random.normal(1.1, 0.05)  # +10% variation
        
    else:  # period_new
        # New code: Better practices, less complexity
        noise = np.random.normal(1.2, 0.05)  # +20% variation
    
    # Apply variations to features
    feature_cols = ['lines_of_code', 'function_count', 'external_calls', 'requires', 'loops', 'code_length']
    
    for col in feature_cols:
        modified_df.at[idx, col] = int(modified_df.at[idx, col] * noise)

# Save modified features
modified_df.to_csv('data/raw/poc_data/contracts_with_features.csv', index=False)

print("✓ Temporal variations added!")
print("\nFeature changes by period:")
print("Period Old:    +5% variation (simulating old complex code)")
print("Period Medium: +10% variation (simulating improving code)")
print("Period New:    +20% variation (simulating modern refactored code)")