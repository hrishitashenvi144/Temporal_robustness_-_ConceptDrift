# -*- coding: utf-8 -*-
"""
Research Analytics Dashboard
Title: Temporal Robustness and Drift-Aware Adaptation for Ethereum Smart Contract Vulnerability Detection
Author: Research Pair Programming & Antigravity IDE
Environment: Python 3.11 / Streamlit / Plotly
"""

import json
from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# -----------------------------------------------------------------------------
# Configuration & Robust Project Root Resolution
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Temporal Robustness Dashboard",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Research Data Directories
DIR_PHASE2 = PROJECT_ROOT / "smart-contract-temporal-demo" / "results"
DIR_AUDIT = PROJECT_ROOT / "phase3_dataset_audit" / "reports"
DIR_P3B = PROJECT_ROOT / "phase3_temporal_ml" / "reports"
DIR_P4 = PROJECT_ROOT / "phase3_temporal_ml" / "reports" / "phase4"
DIR_P5 = PROJECT_ROOT / "phase3_temporal_ml" / "reports" / "phase5"

# -----------------------------------------------------------------------------
# Clean Academic / Scientific Laboratory Styling (No gradients, no AI clichés)
# -----------------------------------------------------------------------------
ACADEMIC_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: #0f172a;
    background-color: #fcfcfd;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2.5rem !important;
    max-width: 1240px;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background-color: #f8fafc;
    border-right: 1px solid #e2e8f0;
    padding-top: 1rem;
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 1rem !important;
}

/* Category header tag */
.academic-tag {
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #475569;
    background-color: #f1f5f9;
    padding: 2px 8px;
    border-radius: 4px;
    border: 1px solid #e2e8f0;
    margin-bottom: 0.4rem;
}

.page-title {
    font-size: 1.55rem;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 0.25rem;
    letter-spacing: -0.02em;
}

.page-subtitle {
    font-size: 0.95rem;
    font-weight: 400;
    color: #64748b;
    margin-bottom: 1.25rem;
}

/* Research Question Callout */
.rq-box {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-left: 4px solid #1e3a8a;
    padding: 1rem 1.25rem;
    border-radius: 4px;
    margin-bottom: 1.5rem;
}

.rq-title {
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #1e3a8a;
    margin-bottom: 0.35rem;
}

.rq-text {
    font-size: 0.98rem;
    font-weight: 500;
    color: #1e293b;
    line-height: 1.45;
    margin: 0;
}

/* Section Box */
.section-box {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 1.2rem;
    margin-bottom: 1.25rem;
}

.box-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: #0f172a;
    margin-bottom: 0.75rem;
    border-bottom: 1px solid #f1f5f9;
    padding-bottom: 0.4rem;
}

/* Metric Display Strip */
.metric-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.25rem;
    flex-wrap: wrap;
}

.metric-cell {
    flex: 1;
    min-width: 140px;
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 0.75rem 1rem;
}

.metric-cell-label {
    font-size: 0.75rem;
    font-weight: 500;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 0.2rem;
}

.metric-cell-value {
    font-size: 1.35rem;
    font-weight: 700;
    color: #0f172a;
    font-family: 'Inter', sans-serif;
}

.metric-cell-sub {
    font-size: 0.78rem;
    color: #475569;
    margin-top: 0.15rem;
}

/* Clean Data Table */
.clean-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
    margin-top: 0.5rem;
}

.clean-table th {
    background-color: #f8fafc;
    color: #475569;
    font-weight: 600;
    text-align: left;
    padding: 8px 12px;
    border-bottom: 2px solid #e2e8f0;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.03em;
}

.clean-table td {
    padding: 8px 12px;
    border-bottom: 1px solid #f1f5f9;
    color: #1e293b;
}

.clean-table tr:hover {
    background-color: #fcfcfd;
}

/* Flowchart Step */
.pipeline-step {
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 0.75rem;
    text-align: center;
    background: #ffffff;
}
.pipeline-step-title {
    font-size: 0.78rem;
    font-weight: 700;
    color: #0f172a;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.pipeline-step-desc {
    font-size: 0.72rem;
    color: #64748b;
    margin-top: 2px;
}

/* Guardrails Note */
.guardrail-box {
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-left: 3px solid #64748b;
    border-radius: 4px;
    padding: 0.85rem 1rem;
    font-size: 0.85rem;
    color: #334155;
    line-height: 1.5;
    margin-top: 0.75rem;
}

div[data-testid="stHorizontalBlock"] {
    align-items: flex-start;
}
</style>
"""

st.markdown(ACADEMIC_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Data Loading Utilities (Cached, Graceful Failover, No Synthetic Creation)
# -----------------------------------------------------------------------------
@st.cache_data
def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)

@st.cache_data
def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Global Data Dictionaries
DF_P2 = load_csv(DIR_PHASE2 / "static_vs_adaptive_comparison.csv")
DF_CONTRACTS_YEAR = load_csv(DIR_AUDIT / "contracts_per_year.csv")
DF_COMPILER_YEAR = load_csv(DIR_AUDIT / "compiler_major_families_by_year.csv")
DF_LABELS_YEAR = load_csv(DIR_AUDIT / "labels_by_year.csv")
DF_FROZEN = load_csv(DIR_P3B / "frozen_model_results.csv")
DF_ADAPT = load_csv(DIR_P3B / "adaptation_results.csv")
DF_P4_SHIFT = load_csv(DIR_P4 / "feature_distribution_shift.csv")
DF_P4_PREV = load_csv(DIR_P4 / "vulnerability_prevalence_by_cohort.csv")
DF_P4_COMPILER = load_csv(DIR_P4 / "compiler_composition_by_cohort.csv")
DF_P5_ALL = load_csv(DIR_P5 / "phase5_model_comparison.csv")
DF_P5_V08 = load_csv(DIR_P5 / "phase5_v08_comparison.csv")
META_P5 = load_json(DIR_P5 / "phase5_metadata.json")

# -----------------------------------------------------------------------------
# Plotly Academic Styling Helper
# -----------------------------------------------------------------------------
def format_academic_chart(fig, height=360, show_legend=True):
    fig.update_layout(
        template="plotly_white",
        font=dict(family="Inter, -apple-system, sans-serif", size=12, color="#334155"),
        height=height,
        margin=dict(l=40, r=20, t=35, b=35),
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11),
        ),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
    )
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="#f1f5f9",
        linecolor="#cbd5e1",
        tickfont=dict(size=11),
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="#f1f5f9",
        linecolor="#cbd5e1",
        tickfont=dict(size=11),
    )
    return fig

# -----------------------------------------------------------------------------
# Sidebar Navigation (Clean & Editorial)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="academic-tag">Research Project</div>', unsafe_allow_html=True)
    st.markdown("### Navigation")
    
    selected_page = st.radio(
        label="Select Section",
        options=[
            "01 — Overview",
            "02 — Dataset & Temporal Evolution",
            "03 — Chronological Baseline",
            "04 — Adaptation",
            "05 — Historical vs Contemporary",
            "06 — Conclusions",
        ],
        index=0,
        label_visibility="collapsed",
    )
    
    st.markdown("---")
    st.markdown(
        """
        <div style="font-size: 0.75rem; color: #64748b; line-height: 1.4;">
        <b>Temporal Robustness Study</b><br>
        Dataset: DIVE (22,330 contracts)<br>
        Span: 2016 – 2024<br>
        Models: Multi-label LR & RF<br>
        Features: 215 audited PRE metrics
        </div>
        """,
        unsafe_allow_html=True,
    )

# =============================================================================
# PAGE 01 — OVERVIEW
# =============================================================================
if selected_page == "01 — Overview":
    st.markdown('<div class="academic-tag">Section 01 · Research Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Temporal Robustness & Drift-Aware Adaptation</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Ethereum Smart Contract Vulnerability Detection Under Chronological Distribution Shift</div>', unsafe_allow_html=True)

    # Research Question
    st.markdown(
        """
        <div class="rq-box">
            <div class="rq-title">Central Research Question</div>
            <p class="rq-text">
                "How does the reliability of smart-contract vulnerability detectors change under temporally ordered distribution shift, and can drift-aware adaptation recover future-period performance without introducing temporal leakage?"
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Study at a Glance
    st.markdown('<div class="box-title">Study at a Glance</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="metric-row">
            <div class="metric-cell">
                <div class="metric-cell-label">Analyzed Contracts</div>
                <div class="metric-cell-value">22,330</div>
                <div class="metric-cell-sub">Contract-level sample</div>
            </div>
            <div class="metric-cell">
                <div class="metric-cell-label">Temporal Span</div>
                <div class="metric-cell-value">2016–2024</div>
                <div class="metric-cell-sub">9 deployment years</div>
            </div>
            <div class="metric-cell">
                <div class="metric-cell-label">Vulnerability Targets</div>
                <div class="metric-cell-value">8 Categories</div>
                <div class="metric-cell-sub">Multi-label classification</div>
            </div>
            <div class="metric-cell">
                <div class="metric-cell-label">Audited Features</div>
                <div class="metric-cell-value">215 Metrics</div>
                <div class="metric-cell-sub">Pre-deployment only</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Visual Research Pipeline
    st.markdown('<div class="box-title">Research Methodology Pipeline</div>', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(
            """
            <div class="pipeline-step">
                <div class="pipeline-step-title">01 · DIVE Audit</div>
                <div class="pipeline-step-desc">22,330 contracts, timestamp integrity, compiler version mapping</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="pipeline-step">
                <div class="pipeline-step-title">02 · Baseline (3B)</div>
                <div class="pipeline-step-desc">Chronological splits (2016-21 train, 2022 val, 2023 adapt, 2024 test)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            """
            <div class="pipeline-step">
                <div class="pipeline-step-title">03 · Shifts (P4)</div>
                <div class="pipeline-step-desc">645 feature comparisons: statistical P(X), P(Y), & compiler confounds</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            """
            <div class="pipeline-step">
                <div class="pipeline-step-title">04 · Hist vs Cont (P5)</div>
                <div class="pipeline-step-desc">Historical (2016-21) vs Contemporary (2023) evaluated on 2024</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col5:
        st.markdown(
            """
            <div class="pipeline-step">
                <div class="pipeline-step-title">05 · Robustness</div>
                <div class="pipeline-step-desc">Solidity v0.8.x stratification & multi-threshold forensic analysis</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # What the study establishes vs Interpretation boundaries
    c_left, c_right = st.columns(2)
    with c_left:
        st.markdown(
            """
            <div class="section-box">
                <div class="box-title">What the Empirical Evidence Establishes</div>
                <ul style="font-size: 0.85rem; color: #334155; line-height: 1.6; padding-left: 1.2rem; margin: 0;">
                    <li><b>Chronological Performance Degradation:</b> Detectors trained on historical contracts experience systematic accuracy and ranking loss on future deployment cohorts.</li>
                    <li><b>Adaptation Benefit:</b> Retraining models incorporating intermediate-period data (2023) yields measurable recovery on the 2024 test cohort.</li>
                    <li><b>Significant P(X) and P(Y) Shifts:</b> All 645 feature-cohort comparisons demonstrate statistically significant distributional shifts after Benjamini-Hochberg FDR correction.</li>
                    <li><b>Altered Future Error Profiles:</b> Contemporary training substantially alters false-positive rates (cutting false alarms by thousands of contracts).</li>
                    <li><b>Compiler Stratification Robustness:</b> Restricting evaluation to Solidity <code>v0.8.x</code> contracts confirms that findings are not an artifact of compiler version heterogeneity in 2024.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c_right:
        st.markdown(
            """
            <div class="section-box">
                <div class="box-title">Methodological Boundaries & Guardrails</div>
                <ul style="font-size: 0.85rem; color: #334155; line-height: 1.6; padding-left: 1.2rem; margin: 0;">
                    <li><b>Controlled Prototype Limitation:</b> Phase 2 demonstrated algorithmic adaptation on synthetic scaling, not natural temporal concept drift.</li>
                    <li><b>Automated Proxy Labels:</b> DIVE ground-truth labels are generated via automated static tooling and post-hoc aggregation, not expert manual audit.</li>
                    <li><b>Compiler Confounding:</b> The rapid ecosystem transition from Solidity <code>v0.4.x</code> to <code>v0.8.x</code> is a discrete language-level shock.</li>
                    <li><b>Chronology vs. Clone Leakage:</b> Chronological splitting alone does not eliminate project-level source clone or proxy-implementation leakage.</li>
                    <li><b>P(Y|X) Nuance:</b> The evidence is consistent with evolving feature-label relationships, but support mismatch and tooling artifacts remain open hypotheses.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

# =============================================================================
# PAGE 02 — DATASET & TEMPORAL EVOLUTION
# =============================================================================
elif selected_page == "02 — Dataset & Temporal Evolution":
    st.markdown('<div class="academic-tag">Section 02 · Dataset Audit & Distributional Shift</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Dataset Composition & Temporal Evolution</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Auditing the multi-year DIVE benchmark and characterizing P(X), P(Y), and compiler shifts</div>', unsafe_allow_html=True)

    tab_a, tab_b, tab_c, tab_d = st.tabs([
        "A. Dataset Composition",
        "B. Vulnerability Prevalence Over Time",
        "C. Compiler Composition Confound",
        "D. Feature Distribution Shift (Phase 4)",
    ])

    with tab_a:
        st.markdown('<div class="box-title">Contract Deployment Distribution (2016–2024)</div>', unsafe_allow_html=True)
        if not DF_CONTRACTS_YEAR.empty:
            fig_comp = go.Figure()
            fig_comp.add_trace(go.Bar(
                x=DF_CONTRACTS_YEAR["year"],
                y=DF_CONTRACTS_YEAR["contract_count"],
                marker_color="#1e293b",
                text=DF_CONTRACTS_YEAR["contract_count"].apply(lambda v: f"{v:,}"),
                textposition="outside",
            ))
            fig_comp.update_layout(
                xaxis_title="Deployment Year",
                yaxis_title="Contract Count",
                yaxis=dict(range=[0, 8200]),
            )
            st.plotly_chart(format_academic_chart(fig_comp, height=340, show_legend=False), use_container_width=True)
            
            st.markdown(
                """
                <div class="guardrail-box">
                <b>Cohort Observations:</b> Contract frequency is heavily bi-modal, peaking in 2018 (5,909 contracts) during the initial ICO wave and again in 2023 (7,166 contracts) and 2024 (4,200 contracts). Years 2016 (16) and 2020 (11) represent small samples that should not be over-interpreted in isolation.
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.warning("contracts_per_year.csv not found.")

    with tab_b:
        st.markdown('<div class="box-title">Vulnerability Prevalence Evolution Across Cohorts</div>', unsafe_allow_html=True)
        if not DF_LABELS_YEAR.empty:
            vuln_options = [
                ("Reentrancy", "reentrancy_pct"),
                ("Access Control", "access_control_pct"),
                ("Arithmetic", "arithmetic_pct"),
                ("Unchecked Low-Level Calls", "unchecked_low_level_calls_pct"),
                ("Denial of Service (DoS)", "dos_pct"),
                ("Bad Randomness", "bad_randomness_pct"),
                ("Front Running", "front_running_pct"),
                ("Time Manipulation", "time_manipulation_pct"),
            ]
            vuln_labels = [opt[0] for opt in vuln_options]
            selected_vuln_idx = st.selectbox("Select Vulnerability Category to Inspect:", range(len(vuln_labels)), format_func=lambda i: vuln_labels[i])
            chosen_name, chosen_col = vuln_options[selected_vuln_idx]
            
            fig_prev = go.Figure()
            fig_prev.add_trace(go.Scatter(
                x=DF_LABELS_YEAR["year"],
                y=DF_LABELS_YEAR[chosen_col],
                mode="lines+markers",
                line=dict(color="#2563eb", width=2.5),
                marker=dict(size=7, color="#1e3a8a"),
                name=chosen_name,
            ))
            fig_prev.update_layout(
                xaxis_title="Deployment Year",
                yaxis_title="Prevalence (%)",
                yaxis=dict(range=[0, max(100, DF_LABELS_YEAR[chosen_col].max() + 10)]),
            )
            st.plotly_chart(format_academic_chart(fig_prev, height=330, show_legend=False), use_container_width=True)
            
            # Show cross-table for this vulnerability
            st.markdown(f"**Annual Prevalence Breakdown for {chosen_name}:**")
            summary_table = DF_LABELS_YEAR[["year", "total_contracts", chosen_col]].copy()
            summary_table.columns = ["Year", "Total Contracts", "Prevalence (%)"]
            summary_table["Prevalence (%)"] = summary_table["Prevalence (%)"].apply(lambda v: f"{v:.2f}%")
            st.dataframe(summary_table.set_index("Year").T, use_container_width=True)
        else:
            st.warning("labels_by_year.csv not found.")

    with tab_c:
        st.markdown('<div class="box-title">Compiler Family Transition (2016–2024)</div>', unsafe_allow_html=True)
        if not DF_COMPILER_YEAR.empty:
            pivot_compiler = DF_COMPILER_YEAR.pivot(index="year", columns="compiler_family", values="percentage_within_year").fillna(0)
            
            fig_comp_fam = go.Figure()
            colors = {"v0.4.x": "#475569", "v0.5.x": "#94a3b8", "v0.6.x": "#cbd5e1", "v0.7.x": "#38bdf8", "v0.8.x": "#1e3a8a"}
            for fam in ["v0.4.x", "v0.5.x", "v0.6.x", "v0.7.x", "v0.8.x"]:
                if fam in pivot_compiler.columns:
                    fig_comp_fam.add_trace(go.Bar(
                        x=pivot_compiler.index,
                        y=pivot_compiler[fam],
                        name=fam,
                        marker_color=colors.get(fam, "#64748b"),
                    ))
            fig_comp_fam.update_layout(
                barmode="stack",
                xaxis_title="Deployment Year",
                yaxis_title="Share of Year (%)",
                yaxis=dict(range=[0, 100]),
            )
            st.plotly_chart(format_academic_chart(fig_comp_fam, height=340), use_container_width=True)
            
            st.markdown(
                """
                <div class="guardrail-box">
                <b>Language Evolution as a Primary Confound:</b> Prior to 2020, over 99% of deployed contracts utilized compiler family <code>v0.4.x</code>. By 2022–2024, over 95% of contracts compiled with <code>v0.8.x</code>. Because Solidity v0.8.0 introduced fundamental language-level semantics (such as default arithmetic overflow reverts and restricted visibility syntax), compiler evolution is a primary structural confound that must be isolated.
                </div>
                """,
                unsafe_allow_html=True,
            )

    with tab_d:
        st.markdown('<div class="box-title">Feature Distribution Shift Analysis (Phase 4 Kolmogorov–Smirnov Tests)</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="rq-box" style="margin-bottom: 1rem;">
                <div class="rq-title">Phase 4 Statistical Outcome</div>
                <p class="rq-text">
                    <b>All 645 feature–cohort comparisons were statistically significant after Benjamini-Hochberg FDR correction (p &lt; 0.05).</b>
                </p>
                <div style="font-size: 0.8rem; color: #475569; margin-top: 4px;">
                    <i>Note: This corresponds to 215 audited numeric features compared across 3 chronological pairs (Historical Train vs 2022, 2023, and 2024), yielding 645 distinct statistical hypothesis tests.</i>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        if not DF_P4_SHIFT.empty:
            c_sel1, c_sel2 = st.columns([1, 2])
            with c_sel1:
                cohort_options = sorted(DF_P4_SHIFT["cohort"].unique())
                cohort_labels = {"validation": "Train vs 2022 (Validation)", "adaptation": "Train vs 2023 (Adaptation)", "test": "Train vs 2024 (Final Test)"}
                selected_cohort = st.selectbox(
                    "Select Cohort Comparison Pair:",
                    cohort_options,
                    format_func=lambda c: cohort_labels.get(c, c),
                )
            
            sub_shift = DF_P4_SHIFT[DF_P4_SHIFT["cohort"] == selected_cohort].sort_values("ks_stat", ascending=False)
            
            with c_sel2:
                search_feat = st.text_input("Filter feature name:", "")
                if search_feat:
                    sub_shift = sub_shift[sub_shift["feature"].str.contains(search_feat, case=False, na=False)]
            
            st.markdown(f"**Top Distributional Shifts for: {cohort_labels.get(selected_cohort, selected_cohort)}**")
            top_table = sub_shift[["feature", "ks_stat", "p_value", "p_value_fdr"]].head(10).copy()
            top_table.columns = ["Feature Name", "KS Statistic", "Raw p-value", "FDR p-value"]
            top_table["KS Statistic"] = top_table["KS Statistic"].apply(lambda v: f"{v:.4f}")
            top_table["Raw p-value"] = top_table["Raw p-value"].apply(lambda v: f"{v:.2e}")
            top_table["FDR p-value"] = top_table["FDR p-value"].apply(lambda v: f"{v:.2e}")
            st.dataframe(top_table, use_container_width=True)

# =============================================================================
# PAGE 03 — CHRONOLOGICAL BASELINE
# =============================================================================
elif selected_page == "03 — Chronological Baseline":
    st.markdown('<div class="academic-tag">Section 03 · Empirical Baseline</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Chronological Baseline Performance</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Evaluating detectors trained on historical contracts (2016–2021) across future deployment periods</div>', unsafe_allow_html=True)

    # Chronological Split Timeline
    st.markdown(
        """
        <div class="metric-row">
            <div class="metric-cell">
                <div class="metric-cell-label">Historical Train</div>
                <div class="metric-cell-value">9,950</div>
                <div class="metric-cell-sub">2016 – 2021 deployments</div>
            </div>
            <div class="metric-cell">
                <div class="metric-cell-label">Validation Set</div>
                <div class="metric-cell-value">1,014</div>
                <div class="metric-cell-sub">2022 deployments</div>
            </div>
            <div class="metric-cell">
                <div class="metric-cell-label">Adaptation Window</div>
                <div class="metric-cell-value">7,166</div>
                <div class="metric-cell-sub">2023 deployments</div>
            </div>
            <div class="metric-cell">
                <div class="metric-cell-label">Final Evaluation</div>
                <div class="metric-cell-value">4,200</div>
                <div class="metric-cell-sub">2024 deployments</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not DF_FROZEN.empty and not DF_ADAPT.empty:
        # Assemble Macro F1 & PR-AUC across periods
        # Periods: 2022 (Val), 2023 (Adapt), 2024 (Frozen), 2024 (Adapted)
        periods_order = ["2022", "2023", "2024_Frozen", "2024_Adapted"]
        
        # Extract from frozen_model_results
        lr_frozen = DF_FROZEN[(DF_FROZEN["model"] == "LogisticRegression") & (DF_FROZEN["vulnerability"] == "macro")]
        rf_frozen = DF_FROZEN[(DF_FROZEN["model"] == "RandomForest") & (DF_FROZEN["vulnerability"] == "macro")]
        
        # Extract from adaptation_results (last 2 rows are the adapted macro)
        lr_adapt = DF_ADAPT[(DF_ADAPT["model"] == "LogisticRegression") & (DF_ADAPT["vulnerability"] == "macro")].iloc[-1]
        rf_adapt = DF_ADAPT[(DF_ADAPT["model"] == "RandomForest") & (DF_ADAPT["vulnerability"] == "macro")].iloc[-1]
        
        lr_f1 = [
            lr_frozen[lr_frozen["period"] == "2022"]["f1"].values[0],
            lr_frozen[lr_frozen["period"] == "2023"]["f1"].values[0],
            lr_frozen[lr_frozen["period"] == "2024"]["f1"].values[0],
            lr_adapt["f1"],
        ]
        
        rf_f1 = [
            rf_frozen[rf_frozen["period"] == "2022"]["f1"].values[0],
            rf_frozen[rf_frozen["period"] == "2023"]["f1"].values[0],
            rf_frozen[rf_frozen["period"] == "2024"]["f1"].values[0],
            rf_adapt["f1"],
        ]
        
        lr_prauc = [
            lr_frozen[lr_frozen["period"] == "2022"]["pr_auc"].values[0],
            lr_frozen[lr_frozen["period"] == "2023"]["pr_auc"].values[0],
            lr_frozen[lr_frozen["period"] == "2024"]["pr_auc"].values[0],
            lr_adapt["pr_auc"],
        ]
        
        rf_prauc = [
            rf_frozen[rf_frozen["period"] == "2022"]["pr_auc"].values[0],
            rf_frozen[rf_frozen["period"] == "2023"]["pr_auc"].values[0],
            rf_frozen[rf_frozen["period"] == "2024"]["pr_auc"].values[0],
            rf_adapt["pr_auc"],
        ]

        c_f1, c_prauc = st.columns(2)
        with c_f1:
            st.markdown('<div class="box-title">Macro-F1 Trajectory Across Chronological Cohorts</div>', unsafe_allow_html=True)
            fig_f1 = go.Figure()
            fig_f1.add_trace(go.Scatter(
                x=["2022 (Val)", "2023", "2024 (Frozen)", "2024 (Adapted)"],
                y=rf_f1,
                mode="lines+markers",
                name="Random Forest",
                line=dict(color="#1e293b", width=2.5),
                marker=dict(size=8),
            ))
            fig_f1.add_trace(go.Scatter(
                x=["2022 (Val)", "2023", "2024 (Frozen)", "2024 (Adapted)"],
                y=lr_f1,
                mode="lines+markers",
                name="Logistic Regression",
                line=dict(color="#64748b", width=2, dash="dash"),
                marker=dict(size=7),
            ))
            fig_f1.update_layout(
                yaxis_title="Macro-F1 Score",
                yaxis=dict(range=[0.3, 0.8]),
            )
            st.plotly_chart(format_academic_chart(fig_f1, height=320), use_container_width=True)

        with c_prauc:
            st.markdown('<div class="box-title">Macro-PR-AUC Trajectory Across Chronological Cohorts</div>', unsafe_allow_html=True)
            fig_pr = go.Figure()
            fig_pr.add_trace(go.Scatter(
                x=["2022 (Val)", "2023", "2024 (Frozen)", "2024 (Adapted)"],
                y=rf_prauc,
                mode="lines+markers",
                name="Random Forest",
                line=dict(color="#1e293b", width=2.5),
                marker=dict(size=8),
            ))
            fig_pr.add_trace(go.Scatter(
                x=["2022 (Val)", "2023", "2024 (Frozen)", "2024 (Adapted)"],
                y=lr_prauc,
                mode="lines+markers",
                name="Logistic Regression",
                line=dict(color="#64748b", width=2, dash="dash"),
                marker=dict(size=7),
            ))
            fig_pr.update_layout(
                yaxis_title="Macro-PR-AUC",
                yaxis=dict(range=[0.3, 0.85]),
            )
            st.plotly_chart(format_academic_chart(fig_pr, height=320), use_container_width=True)

        # Compact Metric Table
        st.markdown('<div class="box-title">Summary Performance Matrix (Macro-Averaged)</div>', unsafe_allow_html=True)
        summary_df = pd.DataFrame([
            {
                "Model": "Logistic Regression",
                "2022 Validation (F1 / PR-AUC)": f"{lr_f1[0]:.4f} / {lr_prauc[0]:.4f}",
                "2023 Interim (F1 / PR-AUC)": f"{lr_f1[1]:.4f} / {lr_prauc[1]:.4f}",
                "2024 Frozen (F1 / PR-AUC)": f"{lr_f1[2]:.4f} / {lr_prauc[2]:.4f}",
                "2024 Adapted (F1 / PR-AUC)": f"{lr_f1[3]:.4f} / {lr_prauc[3]:.4f}",
                "Recovery Delta (Δ F1 / Δ PR-AUC)": f"+{lr_f1[3]-lr_f1[2]:.4f} / +{lr_prauc[3]-lr_prauc[2]:.4f}",
            },
            {
                "Model": "Random Forest",
                "2022 Validation (F1 / PR-AUC)": f"{rf_f1[0]:.4f} / {rf_prauc[0]:.4f}",
                "2023 Interim (F1 / PR-AUC)": f"{rf_f1[1]:.4f} / {rf_prauc[1]:.4f}",
                "2024 Frozen (F1 / PR-AUC)": f"{rf_f1[2]:.4f} / {rf_prauc[2]:.4f}",
                "2024 Adapted (F1 / PR-AUC)": f"{rf_f1[3]:.4f} / {rf_prauc[3]:.4f}",
                "Recovery Delta (Δ F1 / Δ PR-AUC)": f"+{rf_f1[3]-rf_f1[2]:.4f} / +{rf_prauc[3]-rf_prauc[2]:.4f}",
            },
        ])
        st.dataframe(summary_df.set_index("Model"), use_container_width=True)

        st.markdown(
            """
            <div class="guardrail-box">
            <b>Interpretation Notes:</b><br>
            • <b>Frozen Detector:</b> Models trained strictly on historical data (2016–2021) exhibit gradual performance degradation as evaluation moves into later chronological cohorts (2022 → 2023 → 2024).<br>
            • <b>Adapted Detector:</b> Incorporating interim adaptation data (2023) recovers ranking capability on 2024 (RF PR-AUC rises from 0.5419 to 0.6760).<br>
            • <b>Academic Boundary:</b> Performance degradation under temporal shift is observable, but does not by itself prove pure concept drift without isolating covariate shift and prior probability changes.
            </div>
            """,
            unsafe_allow_html=True,
        )

# =============================================================================
# PAGE 04 — ADAPTATION
# =============================================================================
elif selected_page == "04 — Adaptation":
    st.markdown('<div class="academic-tag">Section 04 · Adaptation Recovery</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Drift-Aware Adaptation Results</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Measuring recovery on future periods and contrasting real-world adaptation with the controlled Phase 2 prototype</div>', unsafe_allow_html=True)

    c_real, c_synth = st.columns([3, 2])

    with c_real:
        st.markdown('<div class="box-title">Real-World DIVE Dataset: 2024 Frozen vs. Adapted</div>', unsafe_allow_html=True)
        
        # Load 2024 frozen vs adapted metrics
        lr_fr_row = DF_FROZEN[(DF_FROZEN["model"] == "LogisticRegression") & (DF_FROZEN["period"] == "2024") & (DF_FROZEN["vulnerability"] == "macro")].iloc[0]
        lr_ad_row = DF_ADAPT[(DF_ADAPT["model"] == "LogisticRegression") & (DF_ADAPT["period"] == "2024") & (DF_ADAPT["vulnerability"] == "macro")].iloc[-1]
        
        rf_fr_row = DF_FROZEN[(DF_FROZEN["model"] == "RandomForest") & (DF_FROZEN["period"] == "2024") & (DF_FROZEN["vulnerability"] == "macro")].iloc[0]
        rf_ad_row = DF_ADAPT[(DF_ADAPT["model"] == "RandomForest") & (DF_ADAPT["period"] == "2024") & (DF_ADAPT["vulnerability"] == "macro")].iloc[-1]
        
        fig_rec = go.Figure()
        fig_rec.add_trace(go.Bar(
            name="2024 Frozen",
            x=["LR Macro-F1", "LR PR-AUC", "RF Macro-F1", "RF PR-AUC"],
            y=[lr_fr_row["f1"], lr_fr_row["pr_auc"], rf_fr_row["f1"], rf_fr_row["pr_auc"]],
            marker_color="#94a3b8",
            text=[f"{v:.3f}" for v in [lr_fr_row["f1"], lr_fr_row["pr_auc"], rf_fr_row["f1"], rf_fr_row["pr_auc"]]],
            textposition="auto",
        ))
        fig_rec.add_trace(go.Bar(
            name="2024 Adapted",
            x=["LR Macro-F1", "LR PR-AUC", "RF Macro-F1", "RF PR-AUC"],
            y=[lr_ad_row["f1"], lr_ad_row["pr_auc"], rf_ad_row["f1"], rf_ad_row["pr_auc"]],
            marker_color="#1e293b",
            text=[f"{v:.3f}" for v in [lr_ad_row["f1"], lr_ad_row["pr_auc"], rf_ad_row["f1"], rf_ad_row["pr_auc"]]],
            textposition="auto",
        ))
        fig_rec.update_layout(
            barmode="group",
            yaxis_title="Score",
            yaxis=dict(range=[0, 0.85]),
        )
        st.plotly_chart(format_academic_chart(fig_rec, height=330), use_container_width=True)

        st.markdown(
            f"""
            <div style="font-size: 0.85rem; color: #334155;">
            <b>Empirical Delta Summary on 2024 Test Cohort:</b><br>
            • <b>Logistic Regression:</b> Macro-F1: <code>{lr_fr_row['f1']:.4f} → {lr_ad_row['f1']:.4f}</code> (<b>+{lr_ad_row['f1']-lr_fr_row['f1']:.4f}</b>) | PR-AUC: <code>{lr_fr_row['pr_auc']:.4f} → {lr_ad_row['pr_auc']:.4f}</code> (<b>+{lr_ad_row['pr_auc']-lr_fr_row['pr_auc']:.4f}</b>)<br>
            • <b>Random Forest:</b> Macro-F1: <code>{rf_fr_row['f1']:.4f} → {rf_ad_row['f1']:.4f}</code> (<b>+{rf_ad_row['f1']-rf_fr_row['f1']:.4f}</b>) | PR-AUC: <code>{rf_fr_row['pr_auc']:.4f} → {rf_ad_row['pr_auc']:.4f}</code> (<b>+{rf_ad_row['pr_auc']-rf_fr_row['pr_auc']:.4f}</b>)
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c_synth:
        st.markdown('<div class="box-title">Controlled Prototype (Phase 2 Benchmark)</div>', unsafe_allow_html=True)
        if not DF_P2.empty:
            p2_static_new = DF_P2[(DF_P2["Period"] == "period_new") & (DF_P2["Model"] == "Static")]["F1"].values[0]
            p2_adapt_new = DF_P2[(DF_P2["Period"] == "period_new") & (DF_P2["Model"] == "Adaptive_PostAdaptation")]["F1"].values[0]
            
            fig_p2 = go.Figure()
            fig_p2.add_trace(go.Bar(
                x=["Static Detector", "Adaptive Detector"],
                y=[p2_static_new, p2_adapt_new],
                marker_color=["#94a3b8", "#1e3a8a"],
                text=[f"{p2_static_new:.3f}", f"{p2_adapt_new:.3f}"],
                textposition="auto",
            ))
            fig_p2.update_layout(
                yaxis_title="F1 Score on period_new",
                yaxis=dict(range=[0, 1.0]),
            )
            st.plotly_chart(format_academic_chart(fig_p2, height=270, show_legend=False), use_container_width=True)
            
            st.markdown(
                f"""
                <div class="guardrail-box">
                <b>Methodological Prototype Status:</b><br>
                In the controlled Phase 2 synthetic experiment, an imposed feature shift degraded Static F1 to <b>{p2_static_new:.3f}</b>, and drift-aware retraining recovered F1 to <b>{p2_adapt_new:.3f}</b> (+{p2_adapt_new - p2_static_new:.3f} absolute, +46.3% relative).<br>
                <b>Important Distinction:</b> Phase 2 represents a controlled proof-of-concept for adaptation algorithms; it is <i>not</i> evidence of natural temporal evolution in Ethereum smart contracts.
                </div>
                """,
                unsafe_allow_html=True,
            )

# =============================================================================
# PAGE 05 — HISTORICAL VS CONTEMPORARY (CENTRAL RESEARCH PAGE)
# =============================================================================
elif selected_page == "05 — Historical vs Contemporary":
    st.markdown('<div class="academic-tag">Section 05 · Feature–Label Stability (Phase 5)</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Historical vs. Contemporary Training</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Evaluating models trained on distinct epochs (2016–2021 vs. 2023) against the exact same untouched 2024 test cohort</div>', unsafe_allow_html=True)

    # Interactive Selectors
    c_mod, c_coh = st.columns([1, 1])
    with c_mod:
        selected_model = st.radio(
            "Select Machine Learning Architecture:",
            ["RandomForest", "LogisticRegression"],
            format_func=lambda m: "Random Forest (200 Trees)" if m == "RandomForest" else "Logistic Regression (StandardScaler)",
            horizontal=True,
        )
    with c_coh:
        selected_eval_scope = st.radio(
            "Select Test Cohort Stratification:",
            ["All 2024 Contracts (N=4,200)", "Solidity v0.8.x Only (N=4,118)"],
            horizontal=True,
        )

    # Pick the appropriate Phase 5 CSV
    is_v08 = "v0.8.x" in selected_eval_scope
    active_p5_df = DF_P5_V08 if is_v08 else DF_P5_ALL
    cohort_hist_tag = "historical_v08" if is_v08 else "historical"
    cohort_cont_tag = "contemporary_v08" if is_v08 else "contemporary"

    if not active_p5_df.empty:
        # Extract Macro Rows
        hist_macro = active_p5_df[(active_p5_df["model"] == selected_model) & (active_p5_df["training_cohort"] == cohort_hist_tag) & (active_p5_df["vulnerability"] == "macro")].iloc[0]
        cont_macro = active_p5_df[(active_p5_df["model"] == selected_model) & (active_p5_df["training_cohort"] == cohort_cont_tag) & (active_p5_df["vulnerability"] == "macro")].iloc[0]

        # Top Macro-Level Metric Strip
        d_prec = cont_macro["precision"] - hist_macro["precision"]
        d_rec = cont_macro["recall"] - hist_macro["recall"]
        d_f1 = cont_macro["f1"] - hist_macro["f1"]
        d_pr = cont_macro["pr_auc"] - hist_macro["pr_auc"]
        d_fp = int(cont_macro["false_positives"] - hist_macro["false_positives"])
        d_fn = int(cont_macro["false_negatives"] - hist_macro["false_negatives"])

        st.markdown(
            f"""
            <div class="metric-row">
                <div class="metric-cell">
                    <div class="metric-cell-label">Macro Precision</div>
                    <div class="metric-cell-value">{cont_macro['precision']:.4f}</div>
                    <div class="metric-cell-sub">Hist: {hist_macro['precision']:.4f} ({d_prec:+.4f})</div>
                </div>
                <div class="metric-cell">
                    <div class="metric-cell-label">Macro Recall</div>
                    <div class="metric-cell-value">{cont_macro['recall']:.4f}</div>
                    <div class="metric-cell-sub">Hist: {hist_macro['recall']:.4f} ({d_rec:+.4f})</div>
                </div>
                <div class="metric-cell">
                    <div class="metric-cell-label">Macro F1 (τ=0.5)</div>
                    <div class="metric-cell-value">{cont_macro['f1']:.4f}</div>
                    <div class="metric-cell-sub">Hist: {hist_macro['f1']:.4f} ({d_f1:+.4f})</div>
                </div>
                <div class="metric-cell">
                    <div class="metric-cell-label">Macro PR-AUC</div>
                    <div class="metric-cell-value">{cont_macro['pr_auc']:.4f}</div>
                    <div class="metric-cell-sub">Hist: {hist_macro['pr_auc']:.4f} (<b>{d_pr:+.4f}</b>)</div>
                </div>
                <div class="metric-cell">
                    <div class="metric-cell-label">Total False Positives</div>
                    <div class="metric-cell-value">{int(cont_macro['false_positives']):,}</div>
                    <div class="metric-cell-sub">Hist: {int(hist_macro['false_positives']):,} (<b>{d_fp:+d}</b>)</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Per-Vulnerability Deep Dive
        sub_hist = active_p5_df[(active_p5_df["model"] == selected_model) & (active_p5_df["training_cohort"] == cohort_hist_tag) & (active_p5_df["vulnerability"] != "macro")].set_index("vulnerability")
        sub_cont = active_p5_df[(active_p5_df["model"] == selected_model) & (active_p5_df["training_cohort"] == cohort_cont_tag) & (active_p5_df["vulnerability"] != "macro")].set_index("vulnerability")

        vuln_list = list(sub_hist.index)
        delta_prauc = [sub_cont.loc[v, "pr_auc"] - sub_hist.loc[v, "pr_auc"] for v in vuln_list]
        hist_prauc = [sub_hist.loc[v, "pr_auc"] for v in vuln_list]
        cont_prauc = [sub_cont.loc[v, "pr_auc"] for v in vuln_list]

        c_chart, c_table = st.columns([1, 1])

        with c_chart:
            st.markdown('<div class="box-title">PR-AUC Shift by Vulnerability Category</div>', unsafe_allow_html=True)
            fig_vuln = go.Figure()
            fig_vuln.add_trace(go.Bar(
                y=vuln_list,
                x=hist_prauc,
                name="Historical Model (2016-21)",
                orientation="h",
                marker_color="#94a3b8",
            ))
            fig_vuln.add_trace(go.Bar(
                y=vuln_list,
                x=cont_prauc,
                name="Contemporary Model (2023)",
                orientation="h",
                marker_color="#1e3a8a",
            ))
            fig_vuln.update_layout(
                barmode="group",
                xaxis_title="PR-AUC",
                yaxis_title="",
                yaxis=dict(autorange="reversed"),
                xaxis=dict(range=[0, 1.05]),
            )
            st.plotly_chart(format_academic_chart(fig_vuln, height=380), use_container_width=True)

        with c_table:
            st.markdown('<div class="box-title">Detailed Per-Category Forensic Matrix</div>', unsafe_allow_html=True)
            detail_records = []
            for v in vuln_list:
                h = sub_hist.loc[v]
                c = sub_cont.loc[v]
                detail_records.append({
                    "Vulnerability": v,
                    "Hist PR-AUC": f"{h['pr_auc']:.4f}",
                    "Cont PR-AUC": f"{c['pr_auc']:.4f}",
                    "Δ PR-AUC": f"{c['pr_auc'] - h['pr_auc']:+.4f}",
                    "Hist FP": f"{int(h['false_positives']):,}",
                    "Cont FP": f"{int(c['false_positives']):,}",
                    "Δ FP": f"{int(c['false_positives'] - h['false_positives']):+d}",
                    "Cont F1": f"{c['f1']:.4f}",
                })
            st.dataframe(pd.DataFrame(detail_records).set_index("Vulnerability"), use_container_width=True)

        # Forensic Callouts for Crucial Categories
        st.markdown('<div class="box-title">Vulnerability-Specific Scientific Interpretations</div>', unsafe_allow_html=True)
        col_v1, col_v2, col_v3 = st.columns(3)
        with col_v1:
            st.markdown(
                """
                <div class="section-box">
                    <div style="font-weight: 600; font-size: 0.85rem; color: #1e3a8a;">Arithmetic Vulnerabilities</div>
                    <div style="font-size: 0.8rem; color: #334155; margin-top: 4px; line-height: 1.45;">
                    <b>Massive Ranking Gain:</b> Contemporary RF gains <b>+0.3356 PR-AUC</b> (0.3959 → 0.7315) and cuts false positives by 74.8% (2,342 → 591).<br>
                    <i>Context:</i> Directly aligns with Solidity ≥0.8.0 built-in overflow/underflow protection altering static heuristic validity.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col_v2:
            st.markdown(
                """
                <div class="section-box">
                    <div style="font-weight: 600; font-size: 0.85rem; color: #1e3a8a;">Denial of Service (DoS)</div>
                    <div style="font-size: 0.8rem; color: #334155; margin-top: 4px; line-height: 1.45;">
                    <b>Substantial Ranking Gain:</b> Contemporary RF gains <b>+0.2361 PR-AUC</b> (0.2741 → 0.5102) while precision rises from 20.3% to 52.9%.<br>
                    <i>Context:</i> False positives drop by 334 contracts without compromising true-positive detection sensitivity.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col_v3:
            st.markdown(
                """
                <div class="section-box">
                    <div style="font-weight: 600; font-size: 0.85rem; color: #1e3a8a;">Reentrancy & Access Control</div>
                    <div style="font-size: 0.8rem; color: #334155; margin-top: 4px; line-height: 1.45;">
                    <b>Remarkable Temporal Robustness:</b> Both categories maintain &gt;0.985 PR-AUC and &gt;0.94 F1 regardless of training epoch.<br>
                    <i>Context:</i> Core programmatic invariants (modifiers, call ordering) remain structurally preserved over time.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Compiler Stratification Note
        st.markdown(
            """
            <div class="guardrail-box">
            <b>Compiler Stratification Finding:</b> Exactly 4,118 of the 4,200 contracts (98.05%) in the 2024 test cohort compile with Solidity <code>v0.8.x</code>. When evaluation is restricted strictly to <code>v0.8.x</code>, the Random Forest macro PR-AUC gain is <b>+0.0911</b> (compared to <b>+0.0898</b> on the full cohort), confirming that contemporary superiority is not driven by compiler mixture in the test set.
            </div>
            """,
            unsafe_allow_html=True,
        )

# =============================================================================
# PAGE 06 — CONCLUSIONS
# =============================================================================
elif selected_page == "06 — Conclusions":
    st.markdown('<div class="academic-tag">Section 06 · Summary & Roadmap</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Research Conclusions & Next Steps</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Synthesizing findings, acknowledging empirical boundaries, and establishing Phase 6 roadmap</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
            <div class="section-box" style="height: 100%;">
                <div class="box-title" style="color: #0f172a;">1. Established by the Experiments</div>
                <ul style="font-size: 0.85rem; color: #334155; line-height: 1.6; padding-left: 1.2rem; margin: 0;">
                    <li><b>Temporal Degradation:</b> Static detectors trained on historical contracts experience systematic accuracy and ranking degradation on future deployment periods.</li>
                    <li><b>Adaptation Benefit:</b> Retraining with intermediate chronological data recovers future-period discriminative power.</li>
                    <li><b>P(X) & P(Y) Shift:</b> Statistically significant distributional shift across all 645 feature-cohort comparisons (FDR <i>p</i> &lt; 0.05).</li>
                    <li><b>Distinct Error Profiles:</b> Contemporary training reduces false alarms by thousands of contracts on 2024 evaluations.</li>
                    <li><b>Heterogeneous Sensitivity:</b> Reentrancy and Access Control remain robust; Arithmetic and DoS exhibit dramatic shifts.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="section-box" style="height: 100%;">
                <div class="box-title" style="color: #0f172a;">2. What is Not Established</div>
                <ul style="font-size: 0.85rem; color: #334155; line-height: 1.6; padding-left: 1.2rem; margin: 0;">
                    <li><b>Natural Concept Drift is Not Proven:</b> The evidence is consistent with evolving <i>P(Y|X)</i>, but does not prove causal concept drift.</li>
                    <li><b>Support Mismatch:</b> Performance differences may reflect denser training coverage in modern feature space rather than a pure shift in conditional mapping.</li>
                    <li><b>Tooling Artifacts:</b> DIVE labels rely on automated static analysis heuristics that may interact differently with older vs. newer ASTs.</li>
                    <li><b>Clone Leakage:</b> Potential opcode-skeleton duplicate leakage across the 2023/2024 boundary has not yet been isolated.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            """
            <div class="section-box" style="height: 100%;">
                <div class="box-title" style="color: #0f172a;">3. Recommended Phase 6 Study</div>
                <ul style="font-size: 0.85rem; color: #334155; line-height: 1.6; padding-left: 1.2rem; margin: 0;">
                    <li><b>Recalibration vs. Retraining:</b> Test whether decision-threshold optimization or Platt/Isotonic scaling recovers historical model performance without updating weights.</li>
                    <li><b>Covariate Shift Reweighting:</b> Apply density ratio estimation (importance weighting) to historical samples to isolate true <i>P(Y|X)</i> shift from <i>P(X)</i> shift.</li>
                    <li><b>Opcode Skeleton Clone Audit:</b> Filter the 15.47% duplicate skeleton families across the 2023/2024 boundary to control for project-level leakage.</li>
                    <li><b>Targeted Robustness:</b> Develop drift-resilient feature subsets focused on temporally invariant structural metrics.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="rq-box">
            <div class="rq-title">Concluding Research Takeaway</div>
            <p class="rq-text" style="font-size: 0.92rem; font-weight: 400; color: #334155;">
                Temporal evaluation in smart contract vulnerability detection is not merely an academic exercise; it reveals that static machine learning detectors deployed without adaptation produce massive false-positive inflation on future-period contracts. Drift-aware adaptation recovers ranking capability, but achieving rigorous, leak-free security auditing requires explicit controls for compiler evolution, class imbalance, and ecosystem-level structural shifts.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
