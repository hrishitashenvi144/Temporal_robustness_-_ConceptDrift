# Phase 5 Forensic Analysis: Temporal Stability of the Feature–Label Relationship

**Document Version:** 1.0  
**Date:** September 2026  
**Artifact Path:** [phase5_forensic_analysis.md](file:///c:/Users/LAPTOPS24/Documents/HRISHITA/CLG/Blockchain/demo1/phase3_temporal_ml/reports/phase5/phase5_forensic_analysis.md)  
**Parent Pipeline:** Phase 5 – Temporal Stability of Feature–Label Relationship  
**Status:** Complete and Deterministically Verified  

---

## Executive Summary

Phase 5 investigated whether the relationship between contract-level features and vulnerability labels remained stable over time by comparing two separate multi-label models evaluated on the **exact same untouched 2024 test cohort** ($N = 4,200$ contracts, of which $N = 4,118$ belong to Solidity compiler family `v0.8.x`):
1. **Historical Model:** Trained on contracts deployed from **2016 through 2021** ($N = 9,950$).
2. **Contemporary Model:** Trained on contracts deployed in **2023 only** ($N = 7,166$).

Both models were trained using the audited 215 numeric PRE features, fixed random seed (`42`), balanced class weighting, and evaluated at a fixed decision threshold ($0.5$). **No 2024 data was used for training, feature scaling, or threshold selection.**

---

## 1. Full Metric Comparison (Historical vs. Contemporary)

### A. Full 2024 Test Cohort ($N = 4,200$)

#### Logistic Regression
*All metrics evaluated at decision threshold $\tau = 0.5$.*

| Vulnerability | Model Cohort | Precision | Recall | F1 Score | PR-AUC | False Positives (FP) | False Negatives (FN) | Positives ($N$) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Reentrancy** | Historical | 0.5657 | 0.9343 | 0.7047 | 0.8727 | 1,364 | 125 | 1,902 |
| | Contemporary | 0.9662 | 0.8722 | 0.9168 | 0.9519 | 58 | 243 | 1,902 |
| | **Delta ($\Delta$)** | **+0.4005** | **-0.0620** | **+0.2121** | **+0.0792** | **-1,306** | **+118** | — |
| **Access Control** | Historical | 0.9727 | 0.8250 | 0.8928 | 0.9706 | 66 | 498 | 2,846 |
| | Contemporary | 0.9812 | 0.9375 | 0.9588 | 0.9772 | 51 | 178 | 2,846 |
| | **Delta ($\Delta$)** | **+0.0086** | **+0.1124** | **+0.0661** | **+0.0065** | **-15** | **-320** | — |
| **Arithmetic** | Historical | 0.4024 | 0.9875 | 0.5718 | 0.4303 | 2,465 | 21 | 1,681 |
| | Contemporary | 0.6993 | 0.6127 | 0.6531 | 0.7016 | 443 | 651 | 1,681 |
| | **Delta ($\Delta$)** | **+0.2968** | **-0.3748** | **+0.0813** | **+0.2713** | **-2,022** | **+630** | — |
| **Unchecked Return Values** | Historical | 0.2383 | 0.9392 | 0.3801 | 0.3661 | 2,813 | 57 | 937 |
| | Contemporary | 0.7507 | 0.8068 | 0.7778 | 0.8219 | 251 | 181 | 937 |
| | **Delta ($\Delta$)** | **+0.5125** | **-0.1323** | **+0.3976** | **+0.4559** | **-2,562** | **+124** | — |
| **DoS** | Historical | 0.0724 | 0.8127 | 0.1330 | 0.1048 | 2,780 | 50 | 267 |
| | Contemporary | 0.2901 | 0.3521 | 0.3181 | 0.1993 | 230 | 173 | 267 |
| | **Delta ($\Delta$)** | **+0.2177** | **-0.4607** | **+0.1851** | **+0.0945** | **-2,550** | **+123** | — |
| **Bad Randomness** | Historical | 0.0592 | 0.1892 | 0.0901 | 0.0574 | 334 | 90 | 111 |
| | Contemporary | 0.0720 | 0.0811 | 0.0763 | 0.0721 | 116 | 102 | 111 |
| | **Delta ($\Delta$)** | **+0.0128** | **-0.1081** | **-0.0139** | **+0.0146** | **-218** | **+12** | — |
| **Front Running** | Historical | 0.0043 | 0.9091 | 0.0085 | 0.0072 | 2,321 | 1 | 11 |
| | Contemporary | 0.0500 | 0.0909 | 0.0645 | 0.0133 | 19 | 10 | 11 |
| | **Delta ($\Delta$)** | **+0.0457** | **-0.8182** | **+0.0560** | **+0.0061** | **-2,302** | **+9** | — |
| **Time manipulation** | Historical | 0.5780 | 0.2956 | 0.3912 | 0.5289 | 368 | 1,201 | 1,705 |
| | Contemporary | 0.4589 | 0.7372 | 0.5657 | 0.5463 | 1,482 | 448 | 1,705 |
| | **Delta ($\Delta$)** | **-0.1191** | **+0.4416** | **+0.1746** | **+0.0174** | **+1,114** | **-753** | — |
| **Macro Average** | Historical | 0.3616 | 0.7366 | 0.3965 | 0.4173 | 12,511 | 2,043 | 9,460 |
| | Contemporary | 0.5336 | 0.5613 | 0.5414 | 0.5355 | 2,650 | 1,986 | 9,460 |
| | **Delta ($\Delta$)** | **+0.1719** | **-0.1753** | **+0.1449** | **+0.1182** | **-9,861** | **-57** | — |

---

#### Random Forest (200 Trees)
*All metrics evaluated at decision threshold $\tau = 0.5$.*

| Vulnerability | Model Cohort | Precision | Recall | F1 Score | PR-AUC | False Positives (FP) | False Negatives (FN) | Positives ($N$) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Reentrancy** | Historical | 0.9647 | 0.9332 | 0.9487 | 0.9854 | 65 | 127 | 1,902 |
| | Contemporary | 0.9487 | 0.9427 | 0.9457 | 0.9899 | 97 | 109 | 1,902 |
| | **Delta ($\Delta$)** | **-0.0160** | **+0.0095** | **-0.0030** | **+0.0045** | **+32** | **-18** | — |
| **Access Control** | Historical | 0.9894 | 0.9487 | 0.9686 | 0.9935 | 29 | 146 | 2,846 |
| | Contemporary | 0.9967 | 0.9571 | 0.9765 | 0.9944 | 9 | 122 | 2,846 |
| | **Delta ($\Delta$)** | **+0.0073** | **+0.0084** | **+0.0079** | **+0.0009** | **-20** | **-24** | — |
| **Arithmetic** | Historical | 0.4078 | 0.9595 | 0.5724 | 0.3959 | 2,342 | 68 | 1,681 |
| | Contemporary | 0.6778 | 0.7394 | 0.7073 | 0.7315 | 591 | 438 | 1,681 |
| | **Delta ($\Delta$)** | **+0.2699** | **-0.2201** | **+0.1349** | **+0.3356** | **-1,751** | **+370** | — |
| **Unchecked Return Values** | Historical | 0.8116 | 0.7908 | 0.8011 | 0.8416 | 172 | 196 | 937 |
| | Contemporary | 0.7758 | 0.8495 | 0.8110 | 0.8740 | 230 | 141 | 937 |
| | **Delta ($\Delta$)** | **-0.0358** | **+0.0587** | **+0.0099** | **+0.0324** | **+58** | **-55** | — |
| **DoS** | Historical | 0.2033 | 0.4120 | 0.2723 | 0.2741 | 431 | 157 | 267 |
| | Contemporary | 0.5291 | 0.4082 | 0.4609 | 0.5102 | 97 | 158 | 267 |
| | **Delta ($\Delta$)** | **+0.3258** | **-0.0037** | **+0.1886** | **+0.2361** | **-334** | **+1** | — |
| **Bad Randomness** | Historical | 1.0000 | 0.0090 | 0.0179 | 0.2024 | 0 | 110 | 111 |
| | Contemporary | 0.0000 | 0.0000 | 0.0000 | 0.4365 | 0 | 111 | 111 |
| | **Delta ($\Delta$)** | **-1.0000** | **-0.0090** | **-0.0179** | **+0.2341** | **0** | **+1** | — |
| **Front Running** | Historical | 0.0000 | 0.0000 | 0.0000 | 0.1007 | 0 | 11 | 11 |
| | Contemporary | 0.0000 | 0.0000 | 0.0000 | 0.0273 | 0 | 11 | 11 |
| | **Delta ($\Delta$)** | **0.0000** | **0.0000** | **0.0000** | **-0.0734** | **0** | **0** | — |
| **Time manipulation** | Historical | 0.5882 | 0.9273 | 0.7198 | 0.7129 | 1,107 | 124 | 1,705 |
| | Contemporary | 0.8397 | 0.2334 | 0.3653 | 0.6612 | 76 | 1,307 | 1,705 |
| | **Delta ($\Delta$)** | **+0.2515** | **-0.6938** | **-0.3545** | **-0.0516** | **-1,031** | **+1,183** | — |
| **Macro Average** | Historical | 0.6206 | 0.6226 | 0.5376 | 0.5633 | 4,146 | 939 | 9,460 |
| | Contemporary | 0.5960 | 0.5163 | 0.5333 | 0.6532 | 1,100 | 2,397 | 9,460 |
| | **Delta ($\Delta$)** | **-0.0247** | **-0.1063** | **-0.0043** | **+0.0898** | **-3,046** | **+1,458** | — |

---

### B. Compiler-Stratified Test Cohort: 2024 Solidity `v0.8.x` Only ($N = 4,118$)

#### Logistic Regression (`v0.8.x`)

| Vulnerability | Model Cohort | Precision | Recall | F1 Score | PR-AUC | False Positives (FP) | False Negatives (FN) | Positives ($N$) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Reentrancy** | Historical | 0.5645 | 0.9407 | 0.7056 | 0.8788 | 1,358 | 111 | 1,871 |
| | Contemporary | 0.9687 | 0.8755 | 0.9197 | 0.9528 | 53 | 233 | 1,871 |
| | **Delta ($\Delta$)** | **+0.4042** | **-0.0652** | **+0.2142** | **+0.0741** | **-1,305** | **+122** | — |
| **Access Control** | Historical | 0.9736 | 0.8333 | 0.8980 | 0.9719 | 63 | 464 | 2,784 |
| | Contemporary | 0.9820 | 0.9411 | 0.9611 | 0.9783 | 48 | 164 | 2,784 |
| | **Delta ($\Delta$)** | **+0.0084** | **+0.1078** | **+0.0631** | **+0.0063** | **-15** | **-300** | — |
| **Arithmetic** | Historical | 0.3964 | 0.9908 | 0.5663 | 0.4299 | 2,453 | 15 | 1,626 |
| | Contemporary | 0.6909 | 0.6076 | 0.6466 | 0.6910 | 442 | 638 | 1,626 |
| | **Delta ($\Delta$)** | **+0.2945** | **-0.3831** | **+0.0803** | **+0.2610** | **-2,011** | **+623** | — |
| **Unchecked Return Values** | Historical | 0.2303 | 0.9428 | 0.3702 | 0.3684 | 2,807 | 51 | 891 |
| | Contemporary | 0.7435 | 0.8036 | 0.7724 | 0.8178 | 247 | 175 | 891 |
| | **Delta ($\Delta$)** | **+0.5132** | **-0.1392** | **+0.4022** | **+0.4495** | **-2,560** | **+124** | — |
| **DoS** | Historical | 0.0662 | 0.8000 | 0.1222 | 0.1061 | 2,766 | 49 | 245 |
| | Contemporary | 0.2648 | 0.3102 | 0.2857 | 0.1742 | 211 | 169 | 245 |
| | **Delta ($\Delta$)** | **+0.1986** | **-0.4898** | **+0.1635** | **+0.0682** | **-2,555** | **+120** | — |
| **Bad Randomness** | Historical | 0.0573 | 0.1818 | 0.0871 | 0.0526 | 329 | 90 | 110 |
| | Contemporary | 0.0645 | 0.0727 | 0.0684 | 0.0694 | 116 | 102 | 110 |
| | **Delta ($\Delta$)** | **+0.0072** | **-0.1091** | **-0.0188** | **+0.0168** | **-213** | **+12** | — |
| **Front Running** | Historical | 0.0043 | 0.9091 | 0.0085 | 0.0072 | 2,319 | 1 | 11 |
| | Contemporary | 0.0526 | 0.0909 | 0.0667 | 0.0134 | 18 | 10 | 11 |
| | **Delta ($\Delta$)** | **+0.0483** | **-0.8182** | **+0.0581** | **+0.0062** | **-2,301** | **+9** | — |
| **Time manipulation** | Historical | 0.5642 | 0.2816 | 0.3757 | 0.5172 | 363 | 1,199 | 1,669 |
| | Contemporary | 0.4536 | 0.7352 | 0.5610 | 0.5421 | 1,478 | 442 | 1,669 |
| | **Delta ($\Delta$)** | **-0.1106** | **+0.4536** | **+0.1853** | **+0.0249** | **+1,115** | **-757** | — |
| **Macro Average** | Historical | 0.3571 | 0.7350 | 0.3917 | 0.4165 | 12,458 | 1,980 | 9,207 |
| | Contemporary | 0.5276 | 0.5546 | 0.5352 | 0.5299 | 2,613 | 1,933 | 9,207 |
| | **Delta ($\Delta$)** | **+0.1705** | **-0.1804** | **+0.1435** | **+0.1134** | **-9,845** | **-47** | — |

---

#### Random Forest (`v0.8.x`)

| Vulnerability | Model Cohort | Precision | Recall | F1 Score | PR-AUC | False Positives (FP) | False Negatives (FN) | Positives ($N$) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Reentrancy** | Historical | 0.9679 | 0.9343 | 0.9508 | 0.9917 | 58 | 123 | 1,871 |
| | Contemporary | 0.9495 | 0.9444 | 0.9469 | 0.9903 | 94 | 104 | 1,871 |
| | **Delta ($\Delta$)** | **-0.0184** | **+0.0102** | **-0.0038** | **-0.0014** | **+36** | **-19** | — |
| **Access Control** | Historical | 0.9907 | 0.9522 | 0.9711 | 0.9939 | 25 | 133 | 2,784 |
| | Contemporary | 0.9981 | 0.9591 | 0.9782 | 0.9946 | 5 | 114 | 2,784 |
| | **Delta ($\Delta$)** | **+0.0075** | **+0.0068** | **+0.0071** | **+0.0007** | **-20** | **-19** | — |
| **Arithmetic** | Historical | 0.4014 | 0.9631 | 0.5667 | 0.3850 | 2,335 | 60 | 1,626 |
| | Contemporary | 0.6723 | 0.7392 | 0.7042 | 0.7289 | 586 | 424 | 1,626 |
| | **Delta ($\Delta$)** | **+0.2708** | **-0.2239** | **+0.1375** | **+0.3438** | **-1,749** | **+364** | — |
| **Unchecked Return Values** | Historical | 0.8060 | 0.7834 | 0.7945 | 0.8354 | 168 | 193 | 891 |
| | Contemporary | 0.7696 | 0.8474 | 0.8066 | 0.8737 | 226 | 136 | 891 |
| | **Delta ($\Delta$)** | **-0.0364** | **+0.0640** | **+0.0121** | **+0.0383** | **+58** | **-57** | — |
| **DoS** | Historical | 0.1839 | 0.3918 | 0.2503 | 0.2478 | 426 | 149 | 245 |
| | Contemporary | 0.5052 | 0.3959 | 0.4439 | 0.4945 | 95 | 148 | 245 |
| | **Delta ($\Delta$)** | **+0.3213** | **+0.0041** | **+0.1936** | **+0.2468** | **-331** | **-1** | — |
| **Bad Randomness** | Historical | 0.0000 | 0.0000 | 0.0000 | 0.1939 | 0 | 110 | 110 |
| | Contemporary | 0.0000 | 0.0000 | 0.0000 | 0.4256 | 0 | 110 | 110 |
| | **Delta ($\Delta$)** | **0.0000** | **0.0000** | **0.0000** | **+0.2317** | **0** | **0** | — |
| **Front Running** | Historical | 0.0000 | 0.0000 | 0.0000 | 0.1012 | 0 | 11 | 11 |
| | Contemporary | 0.0000 | 0.0000 | 0.0000 | 0.0276 | 0 | 11 | 11 |
| | **Delta ($\Delta$)** | **0.0000** | **0.0000** | **0.0000** | **-0.0737** | **0** | **0** | — |
| **Time manipulation** | Historical | 0.5834 | 0.9263 | 0.7159 | 0.7079 | 1,104 | 123 | 1,669 |
| | Contemporary | 0.8322 | 0.2199 | 0.3479 | 0.6505 | 74 | 1,302 | 1,669 |
| | **Delta ($\Delta$)** | **+0.2488** | **-0.7064** | **-0.3680** | **-0.0574** | **-1,030** | **+1,179** | — |
| **Macro Average** | Historical | 0.4917 | 0.6189 | 0.5312 | 0.5571 | 4,116 | 902 | 9,207 |
| | Contemporary | 0.5909 | 0.5132 | 0.5285 | 0.6482 | 1,080 | 2,349 | 9,207 |
| | **Delta ($\Delta$)** | **+0.0992** | **-0.1057** | **-0.0027** | **+0.0911** | **-3,036** | **+1,447** | — |

---

## 2. Summary of Contemporary-Minus-Historical Deltas

Across both full-2024 and `v0.8.x`-restricted cohorts:
1. **False Positive Reduction:** The contemporary models drastically reduce false positives across the board. In Logistic Regression, total false positives plummet from 12,511 to 2,650 ($\Delta = -9,861$). In Random Forest, false positives drop from 4,146 to 1,100 ($\Delta = -3,046$).
2. **Ranking Metric (PR-AUC):** Contemporary training yields higher PR-AUC across most categories:
   - Random Forest macro PR-AUC improves by **+0.0898** (full) and **+0.0911** (`v0.8.x`).
   - Logistic Regression macro PR-AUC improves by **+0.1182** (full) and **+0.1134** (`v0.8.x`).
3. **Threshold-Specific Sensitivity Trade-off:** At the uncalibrated decision threshold of $\tau = 0.5$, contemporary models exhibit a much more conservative decision boundary for low-prevalence or structurally shifted categories, lowering recall while substantially increasing precision.

---

## 3. Areas of Improvement vs. Degradation

### Where Contemporary Models Improve:
- **Arithmetic:** Dramatic, unambiguous improvement in both models.
  - Logistic Regression: PR-AUC $+0.2713$, Precision $+0.2968$, FP drops from 2,465 to 443.
  - Random Forest: PR-AUC $+0.3356$ (0.3959 $\to$ 0.7315), Precision $+0.2699$, F1 $+0.1349$, FP drops from 2,342 to 591.
- **Denial of Service (DoS):**
  - Random Forest: PR-AUC $+0.2361$ (0.2741 $\to$ 0.5102), Precision $+0.3258$, F1 $+0.1886$, FP drops by 334.
  - Logistic Regression: Precision $+0.2177$, F1 $+0.1851$, FP drops by 2,550.
- **Unchecked Return Values:**
  - Logistic Regression: PR-AUC $+0.4559$ (0.3661 $\to$ 0.8219), Precision $+0.5125$, F1 $+0.3976$, FP drops by 2,562.
  - Random Forest: PR-AUC $+0.0324$ (0.8416 $\to$ 0.8740), F1 $+0.0099$.
- **Reentrancy (Logistic Regression):**
  - Precision increases from 0.5657 to 0.9662 ($+0.4005$), F1 increases from 0.7047 to 0.9168 ($+0.2121$), and FP drops from 1,364 to 58.
- **Bad Randomness (Ranking):**
  - Random Forest PR-AUC increases from 0.2024 to 0.4365 ($+0.2341$).

### Where Contemporary Models Degrade:
- **Time Manipulation (at fixed $\tau = 0.5$):**
  - Random Forest F1 drops by **$-0.3545$** (from 0.7198 down to 0.3653) because recall plunges from 0.9273 to 0.2334 (false negatives rise by $+1,183$). Although precision rises from 0.5882 to 0.8397 and false positives drop by 1,031, the model becomes severely under-predictive at the default 0.5 threshold. PR-AUC shows a mild decrease of $-0.0516$.
- **Front Running:**
  - Extremely sparse in 2024 ($N = 11$ positives out of 4,200, prevalence 0.26%).
  - Random Forest PR-AUC drops from 0.1007 to 0.0273 ($-0.0734$). Neither model achieves non-zero F1 at $\tau = 0.5$.
- **Recall on Arithmetic & DoS (at $\tau = 0.5$):**
  - Because the historical model grossly over-predicted these categories (capturing almost all positives at the expense of massive false alarms, e.g., Arithmetic recall was $0.9595$ with 2,342 FPs), the contemporary model's more disciplined predictions produce lower recall at $\tau = 0.5$ (Arithmetic recall $0.7394$, DoS recall $0.4082$).

---

## 4. Logistic Regression: Broad vs. Concentrated Improvement

The macro-F1 gain for Logistic Regression ($+0.1449$, from 0.3965 to 0.5414) is **broad-based across most categories rather than concentrated in an isolated single class**:
- **7 out of 8 categories** exhibit positive F1 deltas:
  - Unchecked Return Values: $+0.3976$
  - Reentrancy: $+0.2121$
  - DoS: $+0.1851$
  - Time manipulation: $+0.1746$
  - Arithmetic: $+0.0813$
  - Access Control: $+0.0661$
  - Front Running: $+0.0560$
  - Only Bad Randomness slightly declined ($-0.0139$, from 0.0901 to 0.0763).

**Mechanism:** The historical Logistic Regression model suffered from massive probability over-estimation on 2024 data, producing an overwhelming **12,511 false positives** across 4,200 test contracts (an average of $\sim 3$ false alarms per contract). Training on 2023 contracts realigned the linear weights with the contemporary feature distribution, eliminating **9,861 false positives** while holding false negatives essentially flat (2,043 $\to$ 1,986, $\Delta = -57$).

---

## 5. Random Forest: Flat Macro-F1 vs. Substantial Macro-PR-AUC Gain

Why did Random Forest macro-F1 stay almost unchanged ($0.5376 \to 0.5333$, $\Delta = -0.0043$), while macro-PR-AUC improved substantially ($0.5633 \to 0.6532$, $\Delta = +0.0898$)?

### The Arithmetic Mean Offset:
Macro-F1 is an unweighted arithmetic average of per-class F1 scores evaluated at a single arbitrary threshold ($\tau = 0.5$). Looking at the per-class F1 deltas:
- Large gains: DoS ($+0.1886$), Arithmetic ($+0.1349$), Unchecked Return Values ($+0.0099$), Access Control ($+0.0079$).
- Neutral: Front Running ($0.0000$), Reentrancy ($-0.0030$), Bad Randomness ($-0.0179$).
- Large loss: **Time manipulation ($-0.3545$)**.

The single drop in Time manipulation F1 ($-0.3545$) almost exactly balances the combined gains of DoS ($+0.1886$) and Arithmetic ($+0.1349$) in the 8-class arithmetic mean:
$$\frac{+0.1886 + 0.1349 - 0.3545 + \dots}{8} \approx -0.0043$$

### Threshold-Independence of PR-AUC:
PR-AUC evaluates ranking across **all possible decision thresholds** rather than fixing $\tau = 0.5$:
- Arithmetic PR-AUC: $+0.3356$ ($0.3959 \to 0.7315$)
- DoS PR-AUC: $+0.2361$ ($0.2741 \to 0.5102$)
- Bad Randomness PR-AUC: $+0.2341$ ($0.2024 \to 0.4365$)
- Unchecked Return Values PR-AUC: $+0.0324$ ($0.8416 \to 0.8740$)
- Reentrancy PR-AUC: $+0.0045$ ($0.9854 \to 0.9899$)
- Access Control PR-AUC: $+0.0009$ ($0.9935 \to 0.9944$)
- Only Front Running ($-0.0734$) and Time manipulation ($-0.0516$) saw PR-AUC declines.

**Descriptive Finding:** The contemporary Random Forest is demonstrably a superior probability ranker on 2024 data across 6 of the 8 vulnerability classes. The stagnation in macro-F1 is an artifact of evaluating an uncalibrated fixed decision threshold ($\tau = 0.5$) across shifting posterior distributions, particularly for Time manipulation.

---

## 6. Detailed Vulnerability Analyses

### Arithmetic
- **Historical RF:** Precision 0.4078, Recall 0.9595, PR-AUC 0.3959, FP = 2,342, FN = 68.
- **Contemporary RF:** Precision 0.6778, Recall 0.7394, PR-AUC 0.7315, FP = 591, FN = 438.
- **Analysis:** The historical model generates 2,342 false alarms on 4,200 contracts. In historical contracts (2016–2021, mostly Solidity v0.4.x), unchecked arithmetic was standard, and static tools flagged raw arithmetic operations as potential overflows. Starting in Solidity v0.8.0, arithmetic operations revert on overflow/underflow by default. The contemporary model learns feature associations on 2023 (v0.8.x) contracts, slashing false positives by 74.8% and driving a $+0.3356$ PR-AUC improvement.

### Denial of Service (DoS)
- **Historical RF:** Precision 0.2033, Recall 0.4120, PR-AUC 0.2741, FP = 431, FN = 157.
- **Contemporary RF:** Precision 0.5291, Recall 0.4082, PR-AUC 0.5102, FP = 97, FN = 158.
- **Analysis:** Recall is virtually identical (0.4120 vs 0.4082, exactly 1 additional FN), but precision more than doubles (from 20.3% to 52.9%) due to a 77.5% drop in false positives (431 down to 97). PR-AUC nearly doubles from 0.2741 to 0.5102 ($+0.2361$).

### Time Manipulation
- **Historical RF:** Precision 0.5882, Recall 0.9273, F1 0.7198, PR-AUC 0.7129, FP = 1,107, FN = 124.
- **Contemporary RF:** Precision 0.8397, Recall 0.2334, F1 0.3653, PR-AUC 0.6612, FP = 76, FN = 1,307.
- **Analysis:** The contemporary model shifts its predicted probabilities downward, requiring higher evidence to cross 0.5. While precision rises from 58.8% to 84.0% and FP falls by 1,031, recall drops drastically at $\tau = 0.5$. Ranking quality (PR-AUC) experiences only a moderate decline ($-0.0516$), indicating that the primary difference is threshold calibration rather than an inability to rank.

### Reentrancy
- **Historical RF:** Precision 0.9647, Recall 0.9332, F1 0.9487, PR-AUC 0.9854.
- **Contemporary RF:** Precision 0.9487, Recall 0.9427, F1 0.9457, PR-AUC 0.9899.
- **Analysis:** Reentrancy exhibits remarkable temporal stability across both epochs. The Random Forest achieves $>0.985$ PR-AUC and $>0.94$ F1 regardless of whether it is trained on 2016–2021 or 2023 data. In Logistic Regression, the contemporary model eliminates 1,306 false positives, raising F1 from 0.7047 to 0.9168.

### Access Control
- **Historical RF:** Precision 0.9894, Recall 0.9487, F1 0.9686, PR-AUC 0.9935.
- **Contemporary RF:** Precision 0.9967, Recall 0.9571, F1 0.9765, PR-AUC 0.9944.
- **Analysis:** Access Control is the most prevalent vulnerability in the dataset. Both historical and contemporary models achieve near-perfect discrimination ($>0.993$ PR-AUC, $>0.968$ F1) with minimal temporal variation.

### Bad Randomness
- **Prevalence:** 111 positives out of 4,200 contracts (2.64%).
- **Historical RF:** Precision 1.0000, Recall 0.0090 (1 TP, 110 FN), F1 0.0179, PR-AUC 0.2024.
- **Contemporary RF:** Precision 0.0000, Recall 0.0000, F1 0.0000, PR-AUC 0.4365.
- **Analysis:** Due to severe class imbalance, RF probabilities rarely exceed 0.5, resulting in near-zero F1. However, threshold-free PR-AUC more than doubles from 0.2024 to 0.4365 ($+0.2341$), demonstrating that contemporary training dramatically improves relative ranking of true positives.

### Front Running
- **Prevalence:** 11 positives out of 4,200 contracts (0.26%).
- **Historical RF:** PR-AUC 0.1007, Precision 0.0, Recall 0.0, F1 0.0.
- **Contemporary RF:** PR-AUC 0.0273, Precision 0.0, Recall 0.0, F1 0.0.
- **Historical LR:** Precision 0.0043, Recall 0.9091, FP = 2,321, FN = 1.
- **Contemporary LR:** Precision 0.0500, Recall 0.0909, FP = 19, FN = 10.
- **Analysis:** Extreme class sparsity makes point estimates highly uncertain. The historical Logistic Regression achieved 0.9091 recall only by predicting 2,322 positive classifications for 11 actual positives (a 99.6% false positive rate). The contemporary model ceases blanket positive prediction.

### Unchecked Return Values
- **Historical RF:** Precision 0.8116, Recall 0.7908, F1 0.8011, PR-AUC 0.8416.
- **Contemporary RF:** Precision 0.7758, Recall 0.8495, F1 0.8110, PR-AUC 0.8740.
- **Logistic Regression:** PR-AUC leaps from 0.3661 to 0.8219 ($+0.4559$), with F1 rising from 0.3801 to 0.7778.
- **Analysis:** Both models benefit from contemporary training, with Random Forest showing consistent modest gains and Logistic Regression showing large gains in calibration and ranking.

---

## 7. Full-2024 vs. Compiler-Restricted (`v0.8.x`) Cohort Comparison

Because 4,118 of the 4,200 contracts in 2024 (98.05%) belong to compiler family `v0.8.x`, restricting the test set to `v0.8.x` removes the 82 non-v0.8 contracts (9 from v0.4.x, 13 from v0.5.x, 37 from v0.6.x, 23 from v0.7.x).

| Model / Comparison | Full 2024 Macro F1 Delta | `v0.8.x` Macro F1 Delta | Full 2024 Macro PR-AUC Delta | `v0.8.x` Macro PR-AUC Delta |
| :--- | :--- | :--- | :--- | :--- |
| **Logistic Regression** | **+0.1449** | **+0.1435** | **+0.1182** | **+0.1134** |
| **Random Forest** | **-0.0043** | **-0.0027** | **+0.0898** | **+0.0911** |

### Per-Vulnerability Consistency:
- **RF Arithmetic PR-AUC Delta:** Full $= +0.3356$; `v0.8.x` $= +0.3438$.
- **RF DoS PR-AUC Delta:** Full $= +0.2361$; `v0.8.x` $= +0.2468$.
- **RF Bad Randomness PR-AUC Delta:** Full $= +0.2341$; `v0.8.x` $= +0.2317$.
- **RF Time manipulation F1 Delta:** Full $= -0.3545$; `v0.8.x` $= -0.3680$.

**Conclusion:** **The qualitative and quantitative patterns survive compiler restriction completely intact.** The performance differences between historical and contemporary models cannot be explained away as an artifact of non-v0.8 contracts in the 2024 evaluation set.

---

## 8. Cross-Reference with Phase 4 Prevalence

Below is a direct comparison between the observed label prevalence across cohorts (from Phase 4) and the Phase 5 Random Forest PR-AUC performance changes:

| Vulnerability | Historical Train Prev (2016–2021) | Contemporary Train Prev (2023) | Test Prev (2024) | RF Historical PR-AUC (2024) | RF Contemporary PR-AUC (2024) | RF Delta PR-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Reentrancy** | 46.01% | 61.60% | 45.29% | 0.9854 | 0.9899 | +0.0045 |
| **Access Control** | 78.74% | 73.18% | 67.76% | 0.9935 | 0.9944 | +0.0009 |
| **Arithmetic** | 32.85% | 54.65% | 40.02% | 0.3959 | 0.7315 | **+0.3356** |
| **Unchecked Ret. Vals**| 18.72% | 36.59% | 22.31% | 0.8416 | 0.8740 | +0.0324 |
| **DoS** | 25.40% | 10.73% | 6.36% | 0.2741 | 0.5102 | **+0.2361** |
| **Bad Randomness** | 4.18% | 1.20% | 2.64% | 0.2024 | 0.4365 | **+0.2341** |
| **Front Running** | 5.93% | 0.07% | 0.26% | 0.1007 | 0.0273 | -0.0734 |
| **Time manipulation** | 25.43% | 22.54% | 40.60% | 0.7129 | 0.6612 | -0.0516 |

### Descriptive Observations (Non-Causal):
1. **Prevalence Shifts are Non-Monotonic:** For example, Arithmetic prevalence rose from 32.9% in Historical Train to 54.6% in 2023, then declined to 40.0% in 2024. Time manipulation hovered around 22–25% before jumping to 40.6% in 2024.
2. **Prevalence Shift Does Not Directly Dictate PR-AUC Gain:**
   - Arithmetic prevalence in 2024 (40.0%) was closer to Historical Train (32.9%) than to Contemporary Train (54.6%), yet Contemporary RF gained $+0.3356$ PR-AUC over Historical RF.
   - DoS prevalence declined consistently ($25.4\% \to 10.7\% \to 6.4\%$). Contemporary RF was trained on a lower prevalence than Historical RF, yet its PR-AUC on 2024 was nearly double ($0.2741 \to 0.5102$).
   - This indicates that PR-AUC gains are not mere reflections of matching prior base rates, but reflect improved discriminative ranking over the input features.

---

## 9. Methodological Guardrails: What is Established vs. Unresolved

To maintain strict scientific rigor, we explicitly categorize the evidence across the formal components of distribution shift:

```
Distribution Shift Decomposition:
P(X, Y) = P(X) * P(Y|X)   or   P(Y) * P(X|Y)
```

### A. Evidence of $P(X)$ Shift (Covariate Shift) — Strongly Established
- Phase 4 demonstrated that feature distributions change substantially over time.
- All 645 Kolmogorov-Smirnov feature-cohort comparisons (215 features across 3 cohort pairs) were statistically significant before and after Benjamini-Hochberg FDR correction ($p < 0.05$).
- Architectural metrics (lines of code, complexity scores, function visibility breakdowns, optimization usage) shifted markedly between 2016–2021 and 2023–2024.

### B. Evidence of $P(Y)$ Shift (Prior Probability Shift) — Strongly Established
- Observed label prevalence changed substantially across cohorts.
- Front Running dropped from $\sim 5.9\%$ (2016–2021) to $\sim 0.07\%$ (2023) and $\sim 0.26\%$ (2024).
- DoS dropped from $\sim 25.4\%$ to $\sim 6.4\%$.
- Arithmetic shifted from $32.9\% \to 54.6\% \to 40.0\%$.

### C. Evidence Consistent with $P(Y|X)$ Shift (Concept Drift) — Strongly Supported but not Causal Proof
- When evaluated on the **exact same untouched 2024 test data**, models trained on contemporary data (2023) achieve substantially higher PR-AUC and vastly lower false positive rates for specific vulnerability classes (Arithmetic $+0.3356$, DoS $+0.2361$) than models trained on historical data (2016–2021).
- This divergence persists when restricted to Solidity `v0.8.x`.
- **Why this does not constitute definitive proof of pure concept drift:**
  1. **Support Mismatch:** If contemporary training data populates regions of feature space $X$ that were absent or sparse in 2016–2021, the contemporary model may simply have better local support rather than an altered conditional mapping $P(Y|X)$.
  2. **Automated Label Tooling:** DIVE labels are generated by static analysis tools (e.g., Slither, Mythril) aggregated by a fixed heuristic rule. A tool's sensitivity or false positive characteristics may interact differently with v0.8 ASTs than with v0.4 ASTs.
  3. **Threshold vs. Posterior Shift:** A fixed threshold ($\tau = 0.5$) conflates decision boundary calibration with changes in conditional probability.

### D. Things that Remain Unresolved
1. **Source-Level and Implementation Clone Leakage:** The extent to which 2024 contracts share source-level ASTs, proxy implementations, or library code with 2023 contracts vs. 2016–2021 contracts remains unquantified.
2. **Optimal Decision Boundary vs. Conditional Shift:** Whether performance differences at $\tau = 0.5$ can be recovered by simple threshold tuning / recalibration on validation data without updating model weights.
3. **True Natural Evolution vs. Synthetic Ecosystem Shocks:** How much of the shift stems from the discrete hard-fork introduction of Solidity 0.8 (language-level semantic change) versus continuous gradual temporal drift.

---

## 10. Audit & Experimental Lineage

- **Audited Feature Count:** Exactly 215 numeric features from `PRE_ProcessedData.csv`.
- **Excluded Columns:** `contractID`, `timeStamp`, `year`, all `DIVE_Labels` targets, all `POST` features, and `CompilerVersion` (held as a stratification variable).
- **Preprocessing:**
  - Logistic Regression: `StandardScaler` fitted on training cohort only; evaluated on test.
  - Random Forest: Raw numeric feature matrix.
- **Model Configurations:**
  - Logistic Regression: `class_weight='balanced'`, `random_state=42`, `max_iter=1000`.
  - Random Forest: `n_estimators=200`, `class_weight='balanced'`, `random_state=42`, `n_jobs=-1`.
- **Decision Threshold:** Fixed at $\tau = 0.5$ across all classes.
- **Random Seed:** 42.
- **Cohort Split Boundaries:**
  - Historical Training: Deployments 2016 through 2021 ($N = 9,950$).
  - Contemporary Training: Deployments 2023 only ($N = 7,166$).
  - Final Test: Deployments 2024 only ($N = 4,200$; `v0.8.x` $N = 4,118$).
- **Leakage Integrity:** **Zero 2024 data entered training, feature scaling, imputation, or hyperparameter selection.**

---

## 11. Deterministic Verification & File Hashes

The Phase 5 execution script was run twice in full, computing SHA-256 hashes of all artifacts on each pass. All hashes were verified to be identical across runs:

| File Name | SHA-256 Hash |
| :--- | :--- |
| `phase5_model_comparison.csv` | `ec5681b9a3d72d565ae7611deecc0c6953b71fef47514801c89fe3ce9d723f6e` |
| `phase5_v08_comparison.csv` | `068f26b93cae13c3eb04fa058eb0e725dd37a90a136de66fdc2e44ef5a5f266e` |
| `phase5_metadata.json` | `e54a8c2192d4e2d07241a6519ab5ae11f51ab298d007113dc4d59b75cbccddac` |
| `PHASE5_README.md` | `1a1114e31053a3cce504b9dcb5532cd731c05203d4e1aedc136fe4dfd2741ce6` |

---

## 12. Research Interpretation & Recommended Next Experiment

### What Phase 5 Actually Establishes:
1. Historical models trained on 2016–2021 suffer severe false positive inflation when deployed on 2024 contracts, particularly for Arithmetic, DoS, and Unchecked Return Values.
2. Contemporary models trained on 2023 data achieve substantially better probability ranking (PR-AUC $+0.09$ to $+0.34$) and reduce false alarms by thousands of contracts on 2024 test data.
3. This empirical divergence is not an artifact of compiler version heterogeneity in the test set, as restricting to Solidity `v0.8.x` preserves the identical quantitative pattern.
4. Vulnerabilities behave heterogeneously: Reentrancy and Access Control remain temporally stable, while Arithmetic and DoS exhibit large shifts.

### What Phase 5 Does NOT Establish:
1. It does **not** prove pure concept drift ($P(Y|X)$ change) in isolation from covariate shift ($P(X)$ shift) or label prevalence shift ($P(Y)$ shift).
2. It does **not** establish causal drivers behind the shift.
3. It does **not** rule out clone or near-duplicate leakage between the 2023 adaptation cohort and the 2024 test cohort.

### Recommended Next Experiment (Phase 6):
The strongest, most scientifically defensible next step is **not** to add more complex models (e.g. XGBoost, Deep Learning), but to perform a **Disentanglement and Adaptation Validity Study**:
1. **Recalibration & Threshold Adaptation vs. Retraining:**
   - Test whether simply updating the decision threshold $\tau$ or applying Platt/Isotonic recalibration using a small chronological validation window (e.g., 2022 or late 2023) recovers the performance of the historical model, or if model weights must truly be updated on contemporary samples.
2. **Covariate Shift Reweighting (Density Ratio Estimation):**
   - Apply importance weighting ($w(x) = \frac{P_{2023}(x)}{P_{hist}(x)}$) to historical data. If reweighted historical training fails to recover contemporary performance on Arithmetic/DoS, that provides substantially stronger evidence of genuine $P(Y|X)$ shift rather than mere $P(X)$ covariate shift.
3. **Opcode-Skeleton Clone Leakage Control:**
   - Audit whether the superior performance of the 2023-trained model on 2024 is driven by shared opcode skeletons across the 2023/2024 boundary (as identified in the DIVE paper's 15.47% duplicate skeleton analysis).
