import os
from pathlib import Path
import pandas as pd
import re

def extract_features(contract_code):
    """Extract simple metrics from smart contract code"""
    
    features = {
        'lines_of_code': len(contract_code.split('\n')),
        'function_count': len(re.findall(r'function\s+\w+', contract_code)),
        'external_calls': contract_code.count('.call('),
        'requires': len(re.findall(r'require\s*\(', contract_code)),
        'loops': len(re.findall(r'for\s*\(|while\s*\(', contract_code)),
        'code_length': len(contract_code),
    }
    return features

def process_contracts(data_dir):
    """Process all contracts in data directory"""
    
    rows = []
    
    # Process each period folder
    for period_folder in ['period_old', 'period_medium', 'period_new']:
        period_path = Path(data_dir) / period_folder
        
        for sol_file in period_path.glob('*.sol'):
            # Read contract code
            with open(sol_file, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Extract features
            features = extract_features(code)
            features['file'] = sol_file.name
            features['period'] = period_folder
            
            rows.append(features)
    
    return pd.DataFrame(rows)

# Run it
if __name__ == "__main__":
    df = process_contracts('data/raw/poc_data')
    
    # Merge with labels
    labels = pd.read_csv('data/raw/poc_data/all_labels.csv')
    df = df.merge(labels[['file', 'has_vulnerability']], on='file')
    
    # Save
    df.to_csv('data/raw/poc_data/contracts_with_features.csv', index=False)
    
    print("Features extracted!")
    print(df.to_string())