# Research Analytics Dashboard

**Research Project:** *Temporal Robustness and Drift-Aware Adaptation for Ethereum Smart Contract Vulnerability Detection*  
**Environment:** Python 3.11  
**Framework:** Streamlit & Plotly (Custom Research Presentation Layer)  

---

## 1. Overview

This dashboard serves as the interactive research presentation and forensic analysis layer for the completed empirical phases of the project. It directly visualizes existing experimental results across the multi-year DIVE dataset (22,330 Ethereum smart contracts, 2016–2024), chronological baselines, distribution shift analyses, adaptation experiments, and historical-vs-contemporary evaluations.

**Design Philosophy:** Built as a scientific research interface prioritizing precision, restrained editorial aesthetics, methodological honesty, and zero synthetic fabrication or silent retraining.

---

## 2. Directory Structure & Data Lineage

The dashboard is completely decoupled from model training pipelines and operates strictly on deterministic experimental outputs via relative paths:

```
demo1/
├── dashboard/
│   ├── app.py                      # Main Streamlit dashboard application
│   ├── requirements.txt            # Python dependencies
│   └── README.md                   # This documentation
│
├── smart-contract-temporal-demo/   # Phase 2 (Controlled Prototype)
│   └── results/
│       └── static_vs_adaptive_comparison.csv
│
├── phase3_dataset_audit/           # Phase 3A (DIVE Dataset Audit)
│   └── reports/
│       ├── contracts_per_year.csv
│       ├── compiler_major_families_by_year.csv
│       └── labels_by_year.csv
│
└── phase3_temporal_ml/             # Phase 3B, 4, and 5 Experimental Outputs
    └── reports/
        ├── frozen_model_results.csv        # Phase 3B chronological degradation
        ├── adaptation_results.csv          # Phase 3B / Phase 4 adaptation recovery
        ├── phase4/
        │   ├── feature_distribution_shift.csv
        │   ├── vulnerability_prevalence_by_cohort.csv
        │   └── compiler_composition_by_cohort.csv
        └── phase5/
            ├── phase5_model_comparison.csv # Historical vs Contemporary (All 2024)
            ├── phase5_v08_comparison.csv   # Historical vs Contemporary (v0.8.x only)
            └── phase5_metadata.json
```

---

## 3. Installation & Setup

Using the dedicated research environment in the workspace:

```powershell
# Navigate to workspace root
cd "C:\Users\LAPTOPS24\Documents\HRISHITA\CLG\Blockchain\demo1"

# Activate research virtual environment
.\research_venv\Scripts\Activate.ps1

# Install requirements
pip install -r dashboard\requirements.txt
```

---

## 4. Launching the Dashboard

To run the dashboard from the workspace root:

```powershell
streamlit run dashboard\app.py
```

Or from within the `dashboard` directory:

```powershell
cd dashboard
streamlit run app.py
```

The application will launch locally at `http://localhost:8501`.

---

## 5. Dashboard Architecture & Sections

1. **01 — Overview:** Central research question, 22,330 contract scope, 5-stage methodology pipeline, verified empirical findings, and academic boundaries.
2. **02 — Dataset & Temporal Evolution:** Annual contract deployment distribution, vulnerability prevalence trajectories (2016–2024), Solidity compiler family transition (`v0.4.x` $\to$ `v0.8.x`), and interactive Phase 4 Kolmogorov–Smirnov test shift browser.
3. **03 — Chronological Baseline:** Chronological splitting (2016–2021 Train, 2022 Val, 2023 Adapt, 2024 Test), performance trajectories over time, and degradation analysis.
4. **04 — Adaptation:** 2024 Frozen vs. Adapted recovery analysis, contrasted clearly with the controlled Phase 2 synthetic scaling prototype.
5. **05 — Historical vs Contemporary:** Central Phase 5 forensic evaluation comparing models trained on 2016–2021 vs. 2023 evaluated on the exact same 2024 test cohort, featuring compiler stratification (`v0.8.x`) and per-vulnerability breakdowns (Arithmetic, DoS, Reentrancy, etc.).
6. **06 — Conclusions:** Structured three-part summary: What is empirically established, what remains unproven / unresolved, and the recommended Phase 6 experimental roadmap.
