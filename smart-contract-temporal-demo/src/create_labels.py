import json
import pandas as pd
import os
from pathlib import Path

# Read the vulnerabilities.json
with open('C:\\Users\\LAPTOPS24\\Documents\\HRISHITA\\CLG\\Blockchain\\demo1\\smartbugs\\samples\\vulnerabilities.json', 'r') as f:
    vuln_data = json.load(f)

# Create a dictionary mapping contract names to vulnerabilities
contract_vulns = {}
for item in vuln_data:
    name = item['name']
    categories = [v['category'] for v in item['vulnerabilities']]
    contract_vulns[name] = categories

# Now create labels for each period
def create_period_labels(period_path, period_name):
    contracts = list(Path(period_path).glob('*.sol'))
    
    rows = []
    for contract_file in contracts:
        contract_name = contract_file.name
        
        # Get vulnerabilities for this contract
        vulns = contract_vulns.get(contract_name, [])
        
        # Create row
        row = {
            'file': contract_name,
            'period': period_name,
            'has_vulnerability': 1 if len(vulns) > 0 else 0,
            'vulnerability_types': ','.join(vulns) if vulns else 'none',
            'num_vulnerabilities': len(vulns)
        }
        rows.append(row)
    
    return pd.DataFrame(rows)

# Create labels for each period
period_old_df = create_period_labels('data/raw/poc_data/period_old', 'period_old')
period_medium_df = create_period_labels('data/raw/poc_data/period_medium', 'period_medium')
period_new_df = create_period_labels('data/raw/poc_data/period_new', 'period_new')

# Combine all
all_labels = pd.concat([period_old_df, period_medium_df, period_new_df], ignore_index=True)

# Save
all_labels.to_csv('data/raw/poc_data/all_labels.csv', index=False)

print("Labels created!")
print(all_labels.to_string())