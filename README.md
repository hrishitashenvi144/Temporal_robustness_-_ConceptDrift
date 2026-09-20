# Smart Contract Temporal Robustness POC

## Overview
Proof-of-concept demonstrating temporal robustness evaluation framework for smart contract vulnerability detectors.

## Problem
Do vulnerability detectors maintain performance as smart contracts evolve over time?

## Methodology
- Chronological train-test splits (not random)
- Train on old Solidity versions (0.4.x - 2015 era)
- Test on new Solidity versions (0.8.x - 2024 era)
- Random Forest classifier

## Results
- Framework validated on SmartBugs dataset (30 contracts)
- Consistent performance across time periods (F1≈0.789)
- Demonstrates framework feasibility

## Files
- `src/create_labels.py` - Create vulnerability labels
- `src/feature_extractor.py` - Extract code features
- `src/train_detector.py` - Train detector, evaluate performance
- `src/visualize_results.py` - Create visualizations

## Usage
```powershell
python src/create_labels.py
python src/feature_extractor.py
python src/train_detector.py
python src/visualize_results.py
```

## Next Steps
1. Scale to SolidityGLUE dataset (500+ contracts)
2. Implement drift detection module
3. Build adaptive retraining framework
4. Publish findings

## Author
Hrishita

