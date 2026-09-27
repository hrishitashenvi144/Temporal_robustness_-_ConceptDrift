# Phase 3A: DIVE Data Quality Audit Report

**Total Samples Audited:** 22,330

## 1. Quality & Completeness Summary

| Quality Dimension | Checked Field / Artifact | Value / Count | % of Dataset | Assessment / Status |
| --- | --- | --- | --- | --- |
| Total Records | Dataset Rows | 22,330 | 100.0% | Complete |
| Unique Contract IDs | `contractID` | 22,330 | 100.00% | Unique |
| Duplicate Rows | All Columns | 0 | 0.00% | No exact duplicate rows |
| Missing Deployment Timestamps | `Time manipulation` | 0 | 0.00% | Zero missing |
| Missing Compiler Versions | `CompilerVersion` | 0 | 0.00% | Zero missing |
| Missing Vulnerability Labels | 8 DASP Categories | 0 | 0.00% | Zero missing |
| Contracts with 0 Positive Labels | Multi-label 0-count | 2,686 | 12.03% | Benign / Non-vulnerable |
| Contracts with 1 Positive Label | Multi-label 1-count | 4,221 | 18.90% | Single-vulnerability |
| Contracts with 2+ Positive Labels | Multi-label >1-count | 15,423 | 69.07% | Multi-vulnerability |
| Max Positives per Contract | Max label sum | 8 / 8 | N/A | Highest co-occurrence |
| Raw Source Code Present | Source column/files | YES | Available | Verified |
| Raw Bytecode Present | Bytecode column/files | NO | Not released in dataset | Extracted opcode distributions only |
| Opcode Representations | Opcode feature columns | YES | Available | Opcode frequency distributions |
| Project / Protocol Identifier | Creator / Repo metadata | NO | NOT AVAILABLE | Project leakage cannot be fully metadata-isolated |

## 2. Multi-Label Distribution Details

| Number of Active Vulnerabilities | Contract Count | Percentage |
| --- | --- | --- |
| 0 vulnerabilities | 2,686 | 12.03% |
| 1 vulnerabilities | 4,221 | 18.90% |
| 2 vulnerabilities | 4,882 | 21.86% |
| 3 vulnerabilities | 4,598 | 20.59% |
| 4 vulnerabilities | 3,206 | 14.36% |
| 5 vulnerabilities | 2,152 | 9.64% |
| 6 vulnerabilities | 542 | 2.43% |
| 7 vulnerabilities | 40 | 0.18% |
| 8 vulnerabilities | 3 | 0.01% |
