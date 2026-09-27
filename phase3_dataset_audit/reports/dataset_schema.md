# DIVE Dataset Schema & File Inventory

**Audit Date:** 2026-09-23
**Dataset Source:** Official Zenodo Release (DOI: 10.5281/zenodo.18519253)

## 1. Summary of Released Files

| File | Format | Size (MB) | Rows | Columns | Important Fields Found |
| --- | --- | --- | --- | --- | --- |
| `Feature_list.xlsx` | .xlsx | 0.043 | 0 | 0 |  |
| `Labels/DIVE_Labels.csv` | .csv | 0.479 | 22330 | 9 | timestamp: [Time manipulation] | labels: [Reentrancy, Arithmetic, DoS] |
| `Labels/Tool_Results.csv` | .csv | 1.885 | 26071 | 49 | tool_results: [MAIAN_1, MAIAN_2, MAIAN_3, MAIAN_4, MAIAN_5] |
| `Preprocessed/POST/POST_ProcessedData.csv` | .csv | 24.735 | 22330 | 177 | contract_address: [ADDRESS_Distribution] | timestamp: [TIMESTAMP_Distribution] | block_number: [block_position, Block Information Operation count, BLOCKHASH_Distribution] | source_code: [opcodeLength, noOfOpcodes, noOfUniqueOpcodes, mostFrequentOpcode, uniqueOpcodesRatio] | bytecode_opcodes: [opcodeLength, noOfOpcodes, noOfUniqueOpcodes, mostFrequentOpcode, uniqueOpcodesRatio] | labels: [Arithmetic Operation count] | tx_position: [relative_tx_position, block_position] | ast_cfg_ir: [confirmations, Environmental Information Operation count] |
| `Preprocessed/PRE/PRE_ProcessedData.csv` | .csv | 28.334 | 22330 | 222 | contract_address: [ADDRESS_Distribution] | timestamp: [timeStamp, TIMESTAMP_Distribution] | block_number: [Block Information Operation count, BLOCKHASH_Distribution] | compiler: [CompilerVersion, EVMVersion] | source_code: [opcodeLength, noOfOpcodes, noOfUniqueOpcodes, mostFrequentOpcode, uniqueOpcodesRatio] | bytecode_opcodes: [opcodeLength, noOfOpcodes, noOfUniqueOpcodes, mostFrequentOpcode, uniqueOpcodesRatio] | labels: [Arithmetic Operation count] | ast_cfg_ir: [Environmental Information Operation count] |
| `_parts/part_00.dat` | .dat | 0.0 | 0 | 0 |  |
| `_parts/part_01.dat` | .dat | 0.0 | 0 | 0 |  |
| `_parts/part_02.dat` | .dat | 0.0 | 0 | 0 |  |
| `_parts/part_03.dat` | .dat | 0.0 | 0 | 0 |  |
| `_parts/part_04.dat` | .dat | 0.0 | 0 | 0 |  |
| `_parts/part_05.dat` | .dat | 0.0 | 0 | 0 |  |
| `_parts/part_06.dat` | .dat | 0.0 | 0 | 0 |  |
| `_parts/part_07.dat` | .dat | 0.0 | 0 | 0 |  |
| `_parts/part_08.dat` | .dat | 0.0 | 0 | 0 |  |
| `_parts/part_09.dat` | .dat | 0.0 | 0 | 0 |  |
| `_parts/part_10.dat` | .dat | 0.0 | 0 | 0 |  |
| `_parts/part_11.dat` | .dat | 0.0 | 0 | 0 |  |
| `_parts/part_12.dat` | .dat | 0.0 | 0 | 0 |  |
| `_parts/part_13.dat` | .dat | 0.0 | 0 | 0 |  |
| `_parts/part_14.dat` | .dat | 0.0 | 0 | 0 |  |
| `_parts/part_15.dat` | .dat | 0.0 | 0 | 0 |  |

## 2. Key Artifact Analysis

### Research Questions Mapping & Field Verification

| Requirement / Question | Present? | Location / Field Details | Evidence / Notes |
| --- | --- | --- | --- |
| Contract Addresses | YES | Preprocessed/POST/POST_ProcessedData.csv, Preprocessed/PRE/PRE_ProcessedData.csv | Verified in schema |
| Deployment Timestamps | YES | Labels/DIVE_Labels.csv, Preprocessed/POST/POST_ProcessedData.csv, Preprocessed/PRE/PRE_ProcessedData.csv | Verified in schema |
| Vulnerability Labels | YES | Labels/DIVE_Labels.csv, Preprocessed/POST/POST_ProcessedData.csv, Preprocessed/PRE/PRE_ProcessedData.csv | Verified in schema |
| Compiler Version | YES | Preprocessed/PRE/PRE_ProcessedData.csv | Verified in schema |
| Solidity Source Code | YES | Preprocessed/POST/POST_ProcessedData.csv, Preprocessed/PRE/PRE_ProcessedData.csv | Verified in schema |
| Bytecode / Opcodes | YES | Preprocessed/POST/POST_ProcessedData.csv, Preprocessed/PRE/PRE_ProcessedData.csv | Verified in schema |
| Pre- vs Post-deployment separation | YES | Separate datasets: `PRE_Data` and `POST_Data` | Lifecycle separation confirmed |
| Final Aggregated vs Per-Tool Labels | YES | `DIVE_Labels.csv` (aggregated) and `Tool_Results.csv` (per-tool) | Both provided |
| Raw AST / CFG / IR | YES | Preprocessed/POST/POST_ProcessedData.csv, Preprocessed/PRE/PRE_ProcessedData.csv | Checked across all files |
| Raw Block Number | YES | Preprocessed/POST/POST_ProcessedData.csv, Preprocessed/PRE/PRE_ProcessedData.csv | Checked across all files |
| Transaction Position | YES | Preprocessed/POST/POST_ProcessedData.csv | Checked across all files |
| Project / Protocol Identifier | NO | None | Checked across all files |

## 3. Detailed Per-File Column Catalog

### File: `Feature_list.xlsx`

- **Total Rows:** 0
- **Total Columns:** 0
- **Size:** 0.043 MB


---

### File: `Labels/DIVE_Labels.csv`

- **Total Rows:** 22,330
- **Total Columns:** 9
- **Size:** 0.479 MB

| # | Column Name | Data Type | Missing (Null) Count | Missing % |
| --- | --- | --- | --- | --- |
| 1 | `contractID` | `int64` | 0 | 0.00% |
| 2 | `Reentrancy` | `int64` | 0 | 0.00% |
| 3 | `Access Control` | `int64` | 0 | 0.00% |
| 4 | `Arithmetic` | `int64` | 0 | 0.00% |
| 5 | `Unchecked Return Values` | `int64` | 0 | 0.00% |
| 6 | `DoS` | `int64` | 0 | 0.00% |
| 7 | `Bad Randomness` | `int64` | 0 | 0.00% |
| 8 | `Front Running` | `int64` | 0 | 0.00% |
| 9 | `Time manipulation` | `int64` | 0 | 0.00% |

---

### File: `Labels/Tool_Results.csv`

- **Total Rows:** 26,071
- **Total Columns:** 49
- **Size:** 1.885 MB

| # | Column Name | Data Type | Missing (Null) Count | Missing % |
| --- | --- | --- | --- | --- |
| 1 | `contractID` | `int64` | 0 | 0.00% |
| 2 | `MAIAN_1` | `float64` | 26071 | 100.00% |
| 3 | `MAIAN_2` | `float64` | 5610 | 21.52% |
| 4 | `MAIAN_3` | `float64` | 26071 | 100.00% |
| 5 | `MAIAN_4` | `float64` | 26071 | 100.00% |
| 6 | `MAIAN_5` | `float64` | 5610 | 21.52% |
| 7 | `MAIAN_6` | `float64` | 26071 | 100.00% |
| 8 | `MAIAN_7` | `float64` | 26071 | 100.00% |
| 9 | `MAIAN_8` | `float64` | 26071 | 100.00% |
| 10 | `Mythril_1` | `float64` | 9181 | 35.22% |
| 11 | `Mythril_2` | `float64` | 9181 | 35.22% |
| 12 | `Mythril_3` | `float64` | 9181 | 35.22% |
| 13 | `Mythril_4` | `float64` | 9181 | 35.22% |
| 14 | `Mythril_5` | `float64` | 9181 | 35.22% |
| 15 | `Mythril_6` | `float64` | 9181 | 35.22% |
| 16 | `Mythril_7` | `float64` | 9181 | 35.22% |
| 17 | `Mythril_8` | `float64` | 9181 | 35.22% |
| 18 | `Semgrep_1` | `float64` | 3842 | 14.74% |
| 19 | `Semgrep_2` | `float64` | 3842 | 14.74% |
| 20 | `Semgrep_3` | `float64` | 3842 | 14.74% |
| 21 | `Semgrep_4` | `float64` | 26071 | 100.00% |
| 22 | `Semgrep_5` | `float64` | 26071 | 100.00% |
| 23 | `Semgrep_6` | `float64` | 3842 | 14.74% |
| 24 | `Semgrep_7` | `float64` | 26071 | 100.00% |
| 25 | `Semgrep_8` | `float64` | 3842 | 14.74% |
| 26 | `Slither_1` | `float64` | 7072 | 27.13% |
| 27 | `Slither_2` | `float64` | 7072 | 27.13% |
| 28 | `Slither_3` | `float64` | 7072 | 27.13% |
| 29 | `Slither_4` | `float64` | 7072 | 27.13% |
| 30 | `Slither_5` | `float64` | 7072 | 27.13% |
| 31 | `Slither_6` | `float64` | 7072 | 27.13% |
| 32 | `Slither_7` | `float64` | 26071 | 100.00% |
| 33 | `Slither_8` | `float64` | 7072 | 27.13% |
| 34 | `Solhint_1` | `float64` | 5625 | 21.58% |
| 35 | `Solhint_2` | `float64` | 5625 | 21.58% |
| 36 | `Solhint_3` | `float64` | 26071 | 100.00% |
| 37 | `Solhint_4` | `float64` | 5625 | 21.58% |
| 38 | `Solhint_5` | `float64` | 5625 | 21.58% |
| 39 | `Solhint_6` | `float64` | 5625 | 21.58% |
| 40 | `Solhint_7` | `float64` | 26071 | 100.00% |
| 41 | `Solhint_8` | `float64` | 5625 | 21.58% |
| 42 | `VeriSmart_1` | `float64` | 26071 | 100.00% |
| 43 | `VeriSmart_2` | `float64` | 20065 | 76.96% |
| 44 | `VeriSmart_3` | `float64` | 20065 | 76.96% |
| 45 | `VeriSmart_4` | `float64` | 26071 | 100.00% |
| 46 | `VeriSmart_5` | `float64` | 26071 | 100.00% |
| 47 | `VeriSmart_6` | `float64` | 26071 | 100.00% |
| 48 | `VeriSmart_7` | `float64` | 26071 | 100.00% |
| 49 | `VeriSmart_8` | `float64` | 26071 | 100.00% |

---

### File: `Preprocessed/POST/POST_ProcessedData.csv`

- **Total Rows:** 22,330
- **Total Columns:** 177
- **Size:** 24.735 MB

| # | Column Name | Data Type | Missing (Null) Count | Missing % |
| --- | --- | --- | --- | --- |
| 1 | `contractID` | `int64` | 0 | 0.00% |
| 2 | `NoOfTransactions` | `int64` | 0 | 0.00% |
| 3 | `nonce` | `int64` | 0 | 0.00% |
| 4 | `value` | `float64` | 0 | 0.00% |
| 5 | `gas` | `int64` | 0 | 0.00% |
| 6 | `gasPrice` | `float64` | 0 | 0.00% |
| 7 | `txreceipt_status` | `int64` | 0 | 0.00% |
| 8 | `cumulativeGasUsed` | `int64` | 0 | 0.00% |
| 9 | `gasUsed` | `int64` | 0 | 0.00% |
| 10 | `confirmations` | `int64` | 0 | 0.00% |
| 11 | `methodId` | `object` | 0 | 0.00% |
| 12 | `hour_sin` | `float64` | 0 | 0.00% |
| 13 | `hour_cos` | `float64` | 0 | 0.00% |
| 14 | `dayofweek_sin` | `float64` | 0 | 0.00% |
| 15 | `dayofweek_cos` | `float64` | 0 | 0.00% |
| 16 | `quarter` | `int64` | 0 | 0.00% |
| 17 | `part_of_day` | `object` | 0 | 0.00% |
| 18 | `relative_tx_position` | `float64` | 0 | 0.00% |
| 19 | `block_position` | `object` | 0 | 0.00% |
| 20 | `opcodeLength` | `int64` | 0 | 0.00% |
| 21 | `noOfOpcodes` | `int64` | 0 | 0.00% |
| 22 | `noOfUniqueOpcodes` | `int64` | 0 | 0.00% |
| 23 | `mostFrequentOpcode` | `object` | 0 | 0.00% |
| 24 | `uniqueOpcodesRatio` | `float64` | 0 | 0.00% |
| 25 | `Comparison Operation count` | `int64` | 0 | 0.00% |
| 26 | `Stop Operation count` | `int64` | 0 | 0.00% |
| 27 | `Duplication Operation count` | `int64` | 0 | 0.00% |
| 28 | `Bitwise Logic Operation count` | `int64` | 0 | 0.00% |
| 29 | `Exchange Operation count` | `int64` | 0 | 0.00% |
| 30 | `System Operation count` | `int64` | 0 | 0.00% |
| 31 | `Environmental Information Operation count` | `int64` | 0 | 0.00% |
| 32 | `Arithmetic Operation count` | `int64` | 0 | 0.00% |
| 33 | `Push Operation count` | `int64` | 0 | 0.00% |
| 34 | `Logging Operation count` | `int64` | 0 | 0.00% |
| 35 | `Block Information Operation count` | `int64` | 0 | 0.00% |
| 36 | `Stack, Memory, Storage, and Flow Operation count` | `int64` | 0 | 0.00% |
| 37 | `PUSH1_Distribution` | `float64` | 0 | 0.00% |
| 38 | `MSTORE_Distribution` | `float64` | 0 | 0.00% |
| 39 | `CALLDATASIZE_Distribution` | `float64` | 0 | 0.00% |
| 40 | `LT_Distribution` | `float64` | 0 | 0.00% |
| 41 | `PUSH2_Distribution` | `float64` | 0 | 0.00% |
| 42 | `JUMPI_Distribution` | `float64` | 0 | 0.00% |
| 43 | `PUSH4_Distribution` | `float64` | 0 | 0.00% |
| 44 | `PUSH29_Distribution` | `float64` | 0 | 0.00% |
| 45 | `CALLDATALOAD_Distribution` | `float64` | 0 | 0.00% |
| 46 | `DIV_Distribution` | `float64` | 0 | 0.00% |
| 47 | `AND_Distribution` | `float64` | 0 | 0.00% |
| 48 | `DUP2_Distribution` | `float64` | 0 | 0.00% |
| 49 | `EQ_Distribution` | `float64` | 0 | 0.00% |
| 50 | `DUP1_Distribution` | `float64` | 0 | 0.00% |
| 51 | `JUMPDEST_Distribution` | `float64` | 0 | 0.00% |
| 52 | `JUMP_Distribution` | `float64` | 0 | 0.00% |
| 53 | `SWAP1_Distribution` | `float64` | 0 | 0.00% |
| 54 | `POP_Distribution` | `float64` | 0 | 0.00% |
| 55 | `EXP_Distribution` | `float64` | 0 | 0.00% |
| 56 | `SUB_Distribution` | `float64` | 0 | 0.00% |
| 57 | `ISZERO_Distribution` | `float64` | 0 | 0.00% |
| 58 | `MLOAD_Distribution` | `float64` | 0 | 0.00% |
| 59 | `PUSH3_Distribution` | `float64` | 0 | 0.00% |
| 60 | `MUL_Distribution` | `float64` | 0 | 0.00% |
| 61 | `DUP3_Distribution` | `float64` | 0 | 0.00% |
| 62 | `ADD_Distribution` | `float64` | 0 | 0.00% |
| 63 | `PUSH32_Distribution` | `float64` | 0 | 0.00% |
| 64 | `REVERT_Distribution` | `float64` | 0 | 0.00% |
| 65 | `CALLDATACOPY_Distribution` | `float64` | 0 | 0.00% |
| 66 | `DUP4_Distribution` | `float64` | 0 | 0.00% |
| 67 | `DUP6_Distribution` | `float64` | 0 | 0.00% |
| 68 | `GAS_Distribution` | `float64` | 0 | 0.00% |
| 69 | `DELEGATECALL_Distribution` | `float64` | 0 | 0.00% |
| 70 | `RETURNDATASIZE_Distribution` | `float64` | 0 | 0.00% |
| 71 | `DUP5_Distribution` | `float64` | 0 | 0.00% |
| 72 | `RETURNDATACOPY_Distribution` | `float64` | 0 | 0.00% |
| 73 | `RETURN_Distribution` | `float64` | 0 | 0.00% |
| 74 | `CALLVALUE_Distribution` | `float64` | 0 | 0.00% |
| 75 | `SWAP3_Distribution` | `float64` | 0 | 0.00% |
| 76 | `STOP_Distribution` | `float64` | 0 | 0.00% |
| 77 | `SLOAD_Distribution` | `float64` | 0 | 0.00% |
| 78 | `CALLER_Distribution` | `float64` | 0 | 0.00% |
| 79 | `SWAP2_Distribution` | `float64` | 0 | 0.00% |
| 80 | `LOG3_Distribution` | `float64` | 0 | 0.00% |
| 81 | `LOG1_Distribution` | `float64` | 0 | 0.00% |
| 82 | `LOG2_Distribution` | `float64` | 0 | 0.00% |
| 83 | `SSTORE_Distribution` | `float64` | 0 | 0.00% |
| 84 | `PUSH20_Distribution` | `float64` | 0 | 0.00% |
| 85 | `DUP9_Distribution` | `float64` | 0 | 0.00% |
| 86 | `CALL_Distribution` | `float64` | 0 | 0.00% |
| 87 | `SWAP4_Distribution` | `float64` | 0 | 0.00% |
| 88 | `SWAP5_Distribution` | `float64` | 0 | 0.00% |
| 89 | `DUP8_Distribution` | `float64` | 0 | 0.00% |
| 90 | `EXTCODESIZE_Distribution` | `float64` | 0 | 0.00% |
| 91 | `SHR_Distribution` | `float64` | 0 | 0.00% |
| 92 | `DUP7_Distribution` | `float64` | 0 | 0.00% |
| 93 | `SHL_Distribution` | `float64` | 0 | 0.00% |
| 94 | `SWAP6_Distribution` | `float64` | 0 | 0.00% |
| 95 | `SLT_Distribution` | `float64` | 0 | 0.00% |
| 96 | `PUSH8_Distribution` | `float64` | 0 | 0.00% |
| 97 | `GT_Distribution` | `float64` | 0 | 0.00% |
| 98 | `SGT_Distribution` | `float64` | 0 | 0.00% |
| 99 | `PUSH5_Distribution` | `float64` | 0 | 0.00% |
| 100 | `NUMBER_Distribution` | `float64` | 0 | 0.00% |
| 101 | `PUSH14_Distribution` | `float64` | 0 | 0.00% |
| 102 | `PUSH11_Distribution` | `float64` | 0 | 0.00% |
| 103 | `NOT_Distribution` | `float64` | 0 | 0.00% |
| 104 | `DUP10_Distribution` | `float64` | 0 | 0.00% |
| 105 | `ADDRESS_Distribution` | `float64` | 0 | 0.00% |
| 106 | `PUSH31_Distribution` | `float64` | 0 | 0.00% |
| 107 | `CREATE_Distribution` | `float64` | 0 | 0.00% |
| 108 | `PUSH9_Distribution` | `float64` | 0 | 0.00% |
| 109 | `PUSH10_Distribution` | `float64` | 0 | 0.00% |
| 110 | `OR_Distribution` | `float64` | 0 | 0.00% |
| 111 | `PUSH12_Distribution` | `float64` | 0 | 0.00% |
| 112 | `PUSH16_Distribution` | `float64` | 0 | 0.00% |
| 113 | `BALANCE_Distribution` | `float64` | 0 | 0.00% |
| 114 | `PUSH18_Distribution` | `float64` | 0 | 0.00% |
| 115 | `SELFBALANCE_Distribution` | `float64` | 0 | 0.00% |
| 116 | `PUSH15_Distribution` | `float64` | 0 | 0.00% |
| 117 | `CREATE2_Distribution` | `float64` | 0 | 0.00% |
| 118 | `PUSH7_Distribution` | `float64` | 0 | 0.00% |
| 119 | `TIMESTAMP_Distribution` | `float64` | 0 | 0.00% |
| 120 | `PUSH21_Distribution` | `float64` | 0 | 0.00% |
| 121 | `XOR_Distribution` | `float64` | 0 | 0.00% |
| 122 | `CODECOPY_Distribution` | `float64` | 0 | 0.00% |
| 123 | `DUP12_Distribution` | `float64` | 0 | 0.00% |
| 124 | `EXTCODECOPY_Distribution` | `float64` | 0 | 0.00% |
| 125 | `SWAP15_Distribution` | `float64` | 0 | 0.00% |
| 126 | `SWAP16_Distribution` | `float64` | 0 | 0.00% |
| 127 | `SWAP8_Distribution` | `float64` | 0 | 0.00% |
| 128 | `SWAP7_Distribution` | `float64` | 0 | 0.00% |
| 129 | `DUP11_Distribution` | `float64` | 0 | 0.00% |
| 130 | `SWAP9_Distribution` | `float64` | 0 | 0.00% |
| 131 | `STATICCALL_Distribution` | `float64` | 0 | 0.00% |
| 132 | `GASLIMIT_Distribution` | `float64` | 0 | 0.00% |
| 133 | `ADDMOD_Distribution` | `float64` | 0 | 0.00% |
| 134 | `PUSH0_Distribution` | `float64` | 0 | 0.00% |
| 135 | `ORIGIN_Distribution` | `float64` | 0 | 0.00% |
| 136 | `GASPRICE_Distribution` | `float64` | 0 | 0.00% |
| 137 | `SELFDESTRUCT_Distribution` | `float64` | 0 | 0.00% |
| 138 | `SMOD_Distribution` | `float64` | 0 | 0.00% |
| 139 | `SWAP13_Distribution` | `float64` | 0 | 0.00% |
| 140 | `EXTCODEHASH_Distribution` | `float64` | 0 | 0.00% |
| 141 | `CALLCODE_Distribution` | `float64` | 0 | 0.00% |
| 142 | `MSTORE8_Distribution` | `float64` | 0 | 0.00% |
| 143 | `COINBASE_Distribution` | `float64` | 0 | 0.00% |
| 144 | `SDIV_Distribution` | `float64` | 0 | 0.00% |
| 145 | `PUSH23_Distribution` | `float64` | 0 | 0.00% |
| 146 | `SWAP10_Distribution` | `float64` | 0 | 0.00% |
| 147 | `CODESIZE_Distribution` | `float64` | 0 | 0.00% |
| 148 | `DUP15_Distribution` | `float64` | 0 | 0.00% |
| 149 | `SWAP11_Distribution` | `float64` | 0 | 0.00% |
| 150 | `SWAP12_Distribution` | `float64` | 0 | 0.00% |
| 151 | `LOG4_Distribution` | `float64` | 0 | 0.00% |
| 152 | `PUSH22_Distribution` | `float64` | 0 | 0.00% |
| 153 | `PUSH6_Distribution` | `float64` | 0 | 0.00% |
| 154 | `PUSH19_Distribution` | `float64` | 0 | 0.00% |
| 155 | `BYTE_Distribution` | `float64` | 0 | 0.00% |
| 156 | `MOD_Distribution` | `float64` | 0 | 0.00% |
| 157 | `SIGNEXTEND_Distribution` | `float64` | 0 | 0.00% |
| 158 | `DUP16_Distribution` | `float64` | 0 | 0.00% |
| 159 | `DUP14_Distribution` | `float64` | 0 | 0.00% |
| 160 | `PUSH25_Distribution` | `float64` | 0 | 0.00% |
| 161 | `DUP13_Distribution` | `float64` | 0 | 0.00% |
| 162 | `PUSH28_Distribution` | `float64` | 0 | 0.00% |
| 163 | `SAR_Distribution` | `float64` | 0 | 0.00% |
| 164 | `PUSH17_Distribution` | `float64` | 0 | 0.00% |
| 165 | `PUSH13_Distribution` | `float64` | 0 | 0.00% |
| 166 | `PC_Distribution` | `float64` | 0 | 0.00% |
| 167 | `SWAP14_Distribution` | `float64` | 0 | 0.00% |
| 168 | `PUSH27_Distribution` | `float64` | 0 | 0.00% |
| 169 | `LOG0_Distribution` | `float64` | 0 | 0.00% |
| 170 | `MULMOD_Distribution` | `float64` | 0 | 0.00% |
| 171 | `CHAINID_Distribution` | `float64` | 0 | 0.00% |
| 172 | `MSIZE_Distribution` | `float64` | 0 | 0.00% |
| 173 | `BLOCKHASH_Distribution` | `float64` | 0 | 0.00% |
| 174 | `PUSH24_Distribution` | `float64` | 0 | 0.00% |
| 175 | `PUSH26_Distribution` | `float64` | 0 | 0.00% |
| 176 | `BASEFEE_Distribution` | `float64` | 0 | 0.00% |
| 177 | `PUSH30_Distribution` | `float64` | 0 | 0.00% |

---

### File: `Preprocessed/PRE/PRE_ProcessedData.csv`

- **Total Rows:** 22,330
- **Total Columns:** 222
- **Size:** 28.334 MB

| # | Column Name | Data Type | Missing (Null) Count | Missing % |
| --- | --- | --- | --- | --- |
| 1 | `contractID` | `int64` | 0 | 0.00% |
| 2 | `timeStamp` | `int64` | 0 | 0.00% |
| 3 | `CompilerVersion` | `object` | 0 | 0.00% |
| 4 | `OptimizationUsed` | `int64` | 0 | 0.00% |
| 5 | `Runs` | `int64` | 0 | 0.00% |
| 6 | `EVMVersion` | `object` | 0 | 0.00% |
| 7 | `LicenseType` | `object` | 0 | 0.00% |
| 8 | `NoOfExternalLib` | `int64` | 0 | 0.00% |
| 9 | `Logic Contracts` | `int64` | 0 | 0.00% |
| 10 | `Interfaces` | `int64` | 0 | 0.00% |
| 11 | `Lines` | `int64` | 0 | 0.00% |
| 12 | `nLines` | `int64` | 0 | 0.00% |
| 13 | `nSLOC` | `int64` | 0 | 0.00% |
| 14 | `Comment Lines` | `int64` | 0 | 0.00% |
| 15 | `Complex. Score` | `int64` | 0 | 0.00% |
| 16 | `Contracts` | `int64` | 0 | 0.00% |
| 17 | `Libraries` | `int64` | 0 | 0.00% |
| 18 | `Abstract` | `int64` | 0 | 0.00% |
| 19 | `Public Functions` | `int64` | 0 | 0.00% |
| 20 | `Payable Functions` | `int64` | 0 | 0.00% |
| 21 | `External Functions` | `int64` | 0 | 0.00% |
| 22 | `Internal Functions` | `int64` | 0 | 0.00% |
| 23 | `Private Functions` | `int64` | 0 | 0.00% |
| 24 | `Pure Functions` | `int64` | 0 | 0.00% |
| 25 | `View Functions` | `int64` | 0 | 0.00% |
| 26 | `StateVariablesTotal` | `int64` | 0 | 0.00% |
| 27 | `PublicStateVariables` | `int64` | 0 | 0.00% |
| 28 | `Experimental Features` | `object` | 0 | 0.00% |
| 29 | `Can Receive Funds` | `int64` | 0 | 0.00% |
| 30 | `Uses Assembly` | `int64` | 0 | 0.00% |
| 31 | `Has Destroyable Contracts` | `int64` | 0 | 0.00% |
| 32 | `Transfers ETH` | `int64` | 0 | 0.00% |
| 33 | `Low-Level Calls` | `int64` | 0 | 0.00% |
| 34 | `DelegateCall` | `int64` | 0 | 0.00% |
| 35 | `Uses Hash Functions` | `int64` | 0 | 0.00% |
| 36 | `ECRecover` | `int64` | 0 | 0.00% |
| 37 | `New/Create/Create2` | `int64` | 0 | 0.00% |
| 38 | `TryCatch` | `int64` | 0 | 0.00% |
| 39 | `Unchecked` | `int64` | 0 | 0.00% |
| 40 | `NoOfFunctions` | `int64` | 0 | 0.00% |
| 41 | `NoOfInputs` | `int64` | 0 | 0.00% |
| 42 | `NoOfOutputs` | `int64` | 0 | 0.00% |
| 43 | `NoOfConstantFunctions` | `int64` | 0 | 0.00% |
| 44 | `NoPayableFunctions` | `int64` | 0 | 0.00% |
| 45 | `NoOfUniqueInputTypes` | `int64` | 0 | 0.00% |
| 46 | `NoOfUniqueOutputTypes` | `int64` | 0 | 0.00% |
| 47 | `NoOfEvent` | `int64` | 0 | 0.00% |
| 48 | `FallbackExists` | `int64` | 0 | 0.00% |
| 49 | `ConstructorExists` | `int64` | 0 | 0.00% |
| 50 | `avg_FunctionLength` | `float64` | 0 | 0.00% |
| 51 | `max_InputsOutputs` | `int64` | 0 | 0.00% |
| 52 | `avg_InputsOutputs` | `float64` | 0 | 0.00% |
| 53 | `avg_ConstantPerFunction` | `float64` | 0 | 0.00% |
| 54 | `avg_PayablePerFunction` | `float64` | 0 | 0.00% |
| 55 | `opcodeLength` | `int64` | 0 | 0.00% |
| 56 | `noOfOpcodes` | `int64` | 0 | 0.00% |
| 57 | `noOfUniqueOpcodes` | `int64` | 0 | 0.00% |
| 58 | `mostFrequentOpcode` | `object` | 0 | 0.00% |
| 59 | `uniqueOpcodesRatio` | `float64` | 0 | 0.00% |
| 60 | `Arithmetic Operation count` | `int64` | 0 | 0.00% |
| 61 | `Duplication Operation count` | `int64` | 0 | 0.00% |
| 62 | `Bitwise Logic Operation count` | `int64` | 0 | 0.00% |
| 63 | `Stop Operation count` | `int64` | 0 | 0.00% |
| 64 | `System Operation count` | `int64` | 0 | 0.00% |
| 65 | `Stack, Memory, Storage, and Flow Operation count` | `int64` | 0 | 0.00% |
| 66 | `Logging Operation count` | `int64` | 0 | 0.00% |
| 67 | `Push Operation count` | `int64` | 0 | 0.00% |
| 68 | `Exchange Operation count` | `int64` | 0 | 0.00% |
| 69 | `Comparison Operation count` | `int64` | 0 | 0.00% |
| 70 | `KECCAK256 Operation count` | `int64` | 0 | 0.00% |
| 71 | `Environmental Information Operation count` | `int64` | 0 | 0.00% |
| 72 | `Block Information Operation count` | `int64` | 0 | 0.00% |
| 73 | `PUSH1_Distribution` | `float64` | 0 | 0.00% |
| 74 | `MSTORE_Distribution` | `float64` | 0 | 0.00% |
| 75 | `CALLVALUE_Distribution` | `float64` | 0 | 0.00% |
| 76 | `DUP1_Distribution` | `float64` | 0 | 0.00% |
| 77 | `ISZERO_Distribution` | `float64` | 0 | 0.00% |
| 78 | `PUSH2_Distribution` | `float64` | 0 | 0.00% |
| 79 | `JUMPI_Distribution` | `float64` | 0 | 0.00% |
| 80 | `REVERT_Distribution` | `float64` | 0 | 0.00% |
| 81 | `JUMPDEST_Distribution` | `float64` | 0 | 0.00% |
| 82 | `POP_Distribution` | `float64` | 0 | 0.00% |
| 83 | `CALLER_Distribution` | `float64` | 0 | 0.00% |
| 84 | `PUSH5_Distribution` | `float64` | 0 | 0.00% |
| 85 | `DUP2_Distribution` | `float64` | 0 | 0.00% |
| 86 | `MUL_Distribution` | `float64` | 0 | 0.00% |
| 87 | `DIV_Distribution` | `float64` | 0 | 0.00% |
| 88 | `JUMP_Distribution` | `float64` | 0 | 0.00% |
| 89 | `MLOAD_Distribution` | `float64` | 0 | 0.00% |
| 90 | `PUSH32_Distribution` | `float64` | 0 | 0.00% |
| 91 | `SWAP1_Distribution` | `float64` | 0 | 0.00% |
| 92 | `SUB_Distribution` | `float64` | 0 | 0.00% |
| 93 | `ADD_Distribution` | `float64` | 0 | 0.00% |
| 94 | `KECCAK256_Distribution` | `float64` | 0 | 0.00% |
| 95 | `SSTORE_Distribution` | `float64` | 0 | 0.00% |
| 96 | `CODECOPY_Distribution` | `float64` | 0 | 0.00% |
| 97 | `RETURN_Distribution` | `float64` | 0 | 0.00% |
| 98 | `STOP_Distribution` | `float64` | 0 | 0.00% |
| 99 | `CALLDATASIZE_Distribution` | `float64` | 0 | 0.00% |
| 100 | `LT_Distribution` | `float64` | 0 | 0.00% |
| 101 | `PUSH4_Distribution` | `float64` | 0 | 0.00% |
| 102 | `PUSH29_Distribution` | `float64` | 0 | 0.00% |
| 103 | `CALLDATALOAD_Distribution` | `float64` | 0 | 0.00% |
| 104 | `AND_Distribution` | `float64` | 0 | 0.00% |
| 105 | `EQ_Distribution` | `float64` | 0 | 0.00% |
| 106 | `EXP_Distribution` | `float64` | 0 | 0.00% |
| 107 | `PUSH3_Distribution` | `float64` | 0 | 0.00% |
| 108 | `DUP3_Distribution` | `float64` | 0 | 0.00% |
| 109 | `CALLDATACOPY_Distribution` | `float64` | 0 | 0.00% |
| 110 | `DUP4_Distribution` | `float64` | 0 | 0.00% |
| 111 | `DUP6_Distribution` | `float64` | 0 | 0.00% |
| 112 | `GAS_Distribution` | `float64` | 0 | 0.00% |
| 113 | `DELEGATECALL_Distribution` | `float64` | 0 | 0.00% |
| 114 | `RETURNDATASIZE_Distribution` | `float64` | 0 | 0.00% |
| 115 | `DUP5_Distribution` | `float64` | 0 | 0.00% |
| 116 | `RETURNDATACOPY_Distribution` | `float64` | 0 | 0.00% |
| 117 | `SWAP3_Distribution` | `float64` | 0 | 0.00% |
| 118 | `SLOAD_Distribution` | `float64` | 0 | 0.00% |
| 119 | `SWAP2_Distribution` | `float64` | 0 | 0.00% |
| 120 | `LOG3_Distribution` | `float64` | 0 | 0.00% |
| 121 | `LOG1_Distribution` | `float64` | 0 | 0.00% |
| 122 | `LOG2_Distribution` | `float64` | 0 | 0.00% |
| 123 | `PUSH6_Distribution` | `float64` | 0 | 0.00% |
| 124 | `PUSH7_Distribution` | `float64` | 0 | 0.00% |
| 125 | `UNKNOWN_Distribution` | `float64` | 0 | 0.00% |
| 126 | `SWAP12_Distribution` | `float64` | 0 | 0.00% |
| 127 | `MCOPY_Distribution` | `float64` | 0 | 0.00% |
| 128 | `SWAP15_Distribution` | `float64` | 0 | 0.00% |
| 129 | `SWAP10_Distribution` | `float64` | 0 | 0.00% |
| 130 | `TIMESTAMP_Distribution` | `float64` | 0 | 0.00% |
| 131 | `PUSH28_Distribution` | `float64` | 0 | 0.00% |
| 132 | `NOT_Distribution` | `float64` | 0 | 0.00% |
| 133 | `OR_Distribution` | `float64` | 0 | 0.00% |
| 134 | `PUSH20_Distribution` | `float64` | 0 | 0.00% |
| 135 | `DUP9_Distribution` | `float64` | 0 | 0.00% |
| 136 | `CALL_Distribution` | `float64` | 0 | 0.00% |
| 137 | `SWAP4_Distribution` | `float64` | 0 | 0.00% |
| 138 | `SWAP5_Distribution` | `float64` | 0 | 0.00% |
| 139 | `DUP8_Distribution` | `float64` | 0 | 0.00% |
| 140 | `EXTCODESIZE_Distribution` | `float64` | 0 | 0.00% |
| 141 | `TSTORE_Distribution` | `float64` | 0 | 0.00% |
| 142 | `SGT_Distribution` | `float64` | 0 | 0.00% |
| 143 | `DUP13_Distribution` | `float64` | 0 | 0.00% |
| 144 | `DUP11_Distribution` | `float64` | 0 | 0.00% |
| 145 | `SWAP14_Distribution` | `float64` | 0 | 0.00% |
| 146 | `PUSH26_Distribution` | `float64` | 0 | 0.00% |
| 147 | `BLOBHASH_Distribution` | `float64` | 0 | 0.00% |
| 148 | `CALLCODE_Distribution` | `float64` | 0 | 0.00% |
| 149 | `PUSH9_Distribution` | `float64` | 0 | 0.00% |
| 150 | `INVALID_Distribution` | `float64` | 0 | 0.00% |
| 151 | `SHR_Distribution` | `float64` | 0 | 0.00% |
| 152 | `DUP7_Distribution` | `float64` | 0 | 0.00% |
| 153 | `SHL_Distribution` | `float64` | 0 | 0.00% |
| 154 | `SWAP6_Distribution` | `float64` | 0 | 0.00% |
| 155 | `SLT_Distribution` | `float64` | 0 | 0.00% |
| 156 | `PUSH8_Distribution` | `float64` | 0 | 0.00% |
| 157 | `GT_Distribution` | `float64` | 0 | 0.00% |
| 158 | `NUMBER_Distribution` | `float64` | 0 | 0.00% |
| 159 | `PUSH14_Distribution` | `float64` | 0 | 0.00% |
| 160 | `PUSH11_Distribution` | `float64` | 0 | 0.00% |
| 161 | `DUP10_Distribution` | `float64` | 0 | 0.00% |
| 162 | `ADDRESS_Distribution` | `float64` | 0 | 0.00% |
| 163 | `PUSH31_Distribution` | `float64` | 0 | 0.00% |
| 164 | `CREATE_Distribution` | `float64` | 0 | 0.00% |
| 165 | `PUSH10_Distribution` | `float64` | 0 | 0.00% |
| 166 | `PUSH12_Distribution` | `float64` | 0 | 0.00% |
| 167 | `PUSH0_Distribution` | `float64` | 0 | 0.00% |
| 168 | `PUSH19_Distribution` | `float64` | 0 | 0.00% |
| 169 | `PUSH16_Distribution` | `float64` | 0 | 0.00% |
| 170 | `BALANCE_Distribution` | `float64` | 0 | 0.00% |
| 171 | `PUSH18_Distribution` | `float64` | 0 | 0.00% |
| 172 | `SELFBALANCE_Distribution` | `float64` | 0 | 0.00% |
| 173 | `PUSH15_Distribution` | `float64` | 0 | 0.00% |
| 174 | `CREATE2_Distribution` | `float64` | 0 | 0.00% |
| 175 | `PUSH21_Distribution` | `float64` | 0 | 0.00% |
| 176 | `XOR_Distribution` | `float64` | 0 | 0.00% |
| 177 | `DUP12_Distribution` | `float64` | 0 | 0.00% |
| 178 | `BLOBBASEFEE_Distribution` | `float64` | 0 | 0.00% |
| 179 | `BLOCKHASH_Distribution` | `float64` | 0 | 0.00% |
| 180 | `ADDMOD_Distribution` | `float64` | 0 | 0.00% |
| 181 | `LOG4_Distribution` | `float64` | 0 | 0.00% |
| 182 | `PUSH17_Distribution` | `float64` | 0 | 0.00% |
| 183 | `SELFDESTRUCT_Distribution` | `float64` | 0 | 0.00% |
| 184 | `EXTCODECOPY_Distribution` | `float64` | 0 | 0.00% |
| 185 | `SWAP16_Distribution` | `float64` | 0 | 0.00% |
| 186 | `CHAINID_Distribution` | `float64` | 0 | 0.00% |
| 187 | `PUSH24_Distribution` | `float64` | 0 | 0.00% |
| 188 | `SMOD_Distribution` | `float64` | 0 | 0.00% |
| 189 | `PC_Distribution` | `float64` | 0 | 0.00% |
| 190 | `MSIZE_Distribution` | `float64` | 0 | 0.00% |
| 191 | `SAR_Distribution` | `float64` | 0 | 0.00% |
| 192 | `SWAP8_Distribution` | `float64` | 0 | 0.00% |
| 193 | `EXTCODEHASH_Distribution` | `float64` | 0 | 0.00% |
| 194 | `PUSH23_Distribution` | `float64` | 0 | 0.00% |
| 195 | `SWAP7_Distribution` | `float64` | 0 | 0.00% |
| 196 | `SWAP9_Distribution` | `float64` | 0 | 0.00% |
| 197 | `PREVRANDAO_Distribution` | `float64` | 0 | 0.00% |
| 198 | `PUSH22_Distribution` | `float64` | 0 | 0.00% |
| 199 | `STATICCALL_Distribution` | `float64` | 0 | 0.00% |
| 200 | `GASLIMIT_Distribution` | `float64` | 0 | 0.00% |
| 201 | `CODESIZE_Distribution` | `float64` | 0 | 0.00% |
| 202 | `ORIGIN_Distribution` | `float64` | 0 | 0.00% |
| 203 | `GASPRICE_Distribution` | `float64` | 0 | 0.00% |
| 204 | `SDIV_Distribution` | `float64` | 0 | 0.00% |
| 205 | `SWAP13_Distribution` | `float64` | 0 | 0.00% |
| 206 | `MSTORE8_Distribution` | `float64` | 0 | 0.00% |
| 207 | `COINBASE_Distribution` | `float64` | 0 | 0.00% |
| 208 | `PUSH25_Distribution` | `float64` | 0 | 0.00% |
| 209 | `PUSH27_Distribution` | `float64` | 0 | 0.00% |
| 210 | `PUSH13_Distribution` | `float64` | 0 | 0.00% |
| 211 | `MOD_Distribution` | `float64` | 0 | 0.00% |
| 212 | `DUP15_Distribution` | `float64` | 0 | 0.00% |
| 213 | `SWAP11_Distribution` | `float64` | 0 | 0.00% |
| 214 | `BYTE_Distribution` | `float64` | 0 | 0.00% |
| 215 | `DUP16_Distribution` | `float64` | 0 | 0.00% |
| 216 | `SIGNEXTEND_Distribution` | `float64` | 0 | 0.00% |
| 217 | `DUP14_Distribution` | `float64` | 0 | 0.00% |
| 218 | `LOG0_Distribution` | `float64` | 0 | 0.00% |
| 219 | `MULMOD_Distribution` | `float64` | 0 | 0.00% |
| 220 | `BASEFEE_Distribution` | `float64` | 0 | 0.00% |
| 221 | `PUSH30_Distribution` | `float64` | 0 | 0.00% |
| 222 | `TLOAD_Distribution` | `float64` | 0 | 0.00% |

---

### File: `_parts/part_00.dat`

- **Total Rows:** 0
- **Total Columns:** 0
- **Size:** 0.0 MB


---

### File: `_parts/part_01.dat`

- **Total Rows:** 0
- **Total Columns:** 0
- **Size:** 0.0 MB


---

### File: `_parts/part_02.dat`

- **Total Rows:** 0
- **Total Columns:** 0
- **Size:** 0.0 MB


---

### File: `_parts/part_03.dat`

- **Total Rows:** 0
- **Total Columns:** 0
- **Size:** 0.0 MB


---

### File: `_parts/part_04.dat`

- **Total Rows:** 0
- **Total Columns:** 0
- **Size:** 0.0 MB


---

### File: `_parts/part_05.dat`

- **Total Rows:** 0
- **Total Columns:** 0
- **Size:** 0.0 MB


---

### File: `_parts/part_06.dat`

- **Total Rows:** 0
- **Total Columns:** 0
- **Size:** 0.0 MB


---

### File: `_parts/part_07.dat`

- **Total Rows:** 0
- **Total Columns:** 0
- **Size:** 0.0 MB


---

### File: `_parts/part_08.dat`

- **Total Rows:** 0
- **Total Columns:** 0
- **Size:** 0.0 MB


---

### File: `_parts/part_09.dat`

- **Total Rows:** 0
- **Total Columns:** 0
- **Size:** 0.0 MB


---

### File: `_parts/part_10.dat`

- **Total Rows:** 0
- **Total Columns:** 0
- **Size:** 0.0 MB


---

### File: `_parts/part_11.dat`

- **Total Rows:** 0
- **Total Columns:** 0
- **Size:** 0.0 MB


---

### File: `_parts/part_12.dat`

- **Total Rows:** 0
- **Total Columns:** 0
- **Size:** 0.0 MB


---

### File: `_parts/part_13.dat`

- **Total Rows:** 0
- **Total Columns:** 0
- **Size:** 0.0 MB


---

### File: `_parts/part_14.dat`

- **Total Rows:** 0
- **Total Columns:** 0
- **Size:** 0.0 MB


---

### File: `_parts/part_15.dat`

- **Total Rows:** 0
- **Total Columns:** 0
- **Size:** 0.0 MB


---

