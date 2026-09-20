# Research Statement: Temporal Robustness in Smart Contract Vulnerability Detection

## Problem
Smart contract vulnerability detectors are trained on historical data but deployed indefinitely on new contracts. As blockchain technology evolves, contract code patterns and vulnerability characteristics change. **Do detectors maintain performance under temporal distribution shift?**

## Research Gap
Recent surveys (2024) explicitly identify temporal generalization as insufficiently investigated in smart contract security. Most prior work uses random train-test splits, which don't reflect real deployment scenarios.

## Our Contribution
1. **Framework**: Chronological evaluation methodology for vulnerability detectors
2. **Analysis**: Systematic assessment of temporal robustness
3. **Roadmap**: Drift-aware adaptive detection system

## Current Phase: Validation POC
- ✅ Implemented chronological evaluation framework
- ✅ Validated approach on SmartBugs dataset
- ✅ Demonstrated framework feasibility

## Next Phase: Scale & Enhance
- SolidityGLUE dataset (500+ contracts, real timestamps)
- Drift detection module
- Adaptive retraining mechanism
- Publication-ready analysis

## Why This Matters
- Enables long-term deployment of security tools
- Provides practitioners with retraining guidelines
- Advances research in ML robustness for blockchain
- Addresses documented literature gap