# S168 — passive supplement and analysis correspondence

The [publication reconstruction](S168-suite-size-confounding.md) owns scientific claims. This check reads published files and performs our own counts, means and elementary covariance arithmetic. It does **not** run/import author Python/Java/R, fit prediction models, repeat bootstrap analyses, generate suites or execute Defects4J. Full publication reading, artifact inspection and experimental reproduction remain separate.

## Identity and coverage

[Figshare24598707v5](https://doi.org/10.6084/m9.figshare.24598707.v5),2025-02-23, CC-BY4.0; file 52547432,61,618,292 bytes,MD5`a132e9b8b23111e93297426d9201c62c`,SHA-256`8439055b5150ec1191ebf10eef77765a5ca207c40d1588d14eb56264705052a6`. Native ZIP`CHMX4VQ6` is under existing parent`UVZ6NCSS`; uploaded bytes were read back and checked. The first deposit predates publication; v5 also precedes the last manuscript revision. No claim that an unversioned link supplies the final analysis snapshot.

The ZIP has 9,003 entries and 252,327,488 uncompressed bytes including directories/Mac metadata. There are 3,877 actual nonhidden files under`Supplementary Material/`:2,697 CSVs,35 Python,8 Java,3 JARs,565 properties,565 logs,3 Markdown and 1 PDF. This inventory is not body reading of every file. All three READMEs are read; the 318-byte TCP and 314-byte TSR notes name coverage helpers and working-directory/TestNo inputs, but are not complete build/analysis instructions.

Internal`supplementary file.pdf`:7 pages,493,835 bytes,SHA-256`3689642e9d0b761176ab02a2fbd709f55411eb373e72c4814430fabc386edf63`. All text, twelve tables and visual pages 2–7 are covered. Table 1 enumerates 565 bug IDs; Table 2 lists 257 failed cases by three categories; Tables 3–8 give model settings and 9–12 extend association analyses. Its placeholder DOI and affiliations are retained as version differences.

## Data checks

**155 CSV files** were consumed for the selected checks:3 raw global files,3 adjusted global files,33 project-adjusted files, and 116 optimization files (29 project/criterion combinations × two rules × reduction/prioritization). Each has a private path/size/hash/row/column inventory. Bodies and extraction dumps remain ignored; only derived findings are committed.

- Raw rows and detected labels reproduce 17,603/3,613 statement,18,044/4,225 branch and 19,229/5,564 mutation counts. Unique feature/outcome tuples are 15,514/15,584/11,873; these tuples do **not** identify distinct test suites, so repeated values are not established duplicate suites.
- Adjusted global files contain 15,069/12,881/14,149 rows, with 3,103/3,121/4,248 positive labels. Their original`nX,Z,Y`multisets equal the selected project concatenations. The mutation folder also contains JacksonCore, although that project is not in the reported significant-project aggregate; it is excluded from this aggregate membership check.
- In all 33 project-adjusted files, stored`nXr`equals the OLS residual **plus twice the fitted intercept**, within floating-point precision. Global files similarly match`X − aZ + intercept`, but use a combined-sample fit. Global slopes are.69768696/.74905243/.74316464 and intercepts 49.37793320/46.16843779/43.70239000. Maximum discrepancies from that formula are below 8×10⁻¹⁴. Stored means are 98.75586641/92.33687558/87.40478000, rather than zero. This locates an intercept-sign and fit-scope correspondence issue; it does not establish a consequential model-output change after centering.
- Optimization files supply 2,090/1,705/1,760 rows per rule, exactly five repetitions of 418/341/352 fault cases. Their means produce the main note's reduction-loss tradeoff and positive coverage/adverse mutation-prioritization directions. Repetitions are not additional faults.
- Most aggregate values agree to four decimals. Branch raw reduction is.8509496615 versus printed.8510; statement adjusted time APFDc is.8666447911 versus printed.8667. These small last-decimal mismatches remain explicit.
- Lang statement reduction has raw/adjusted means.705212856/.653588960, difference.051623896, and medians.808614485/.663636364. Table 23 instead prints.0516 as the adjusted median and.0681 as its mean difference. This is a localized publication/data discrepancy, not grounds to discard its favorable detection-loss change.

## Bounded source inspection

Static text search covers all 43 Python/Java source names for regression/PROCESS/residual production. The only`LinearRegression`hits are in the coverage-to-mutation prediction helper. No R file, PROCESS syntax or residual-producing fit is supplied by that search. This absence in v5 is not proof that the authors never had those programs.

| File under `Supplementary Material/src/` | Actual reading | SHA-256 |
| --- | --- | --- |
| `test suite generation/my_greedy_selection.py` | All 246 lines/7,604 bytes; mutation generation and trigger-label lookup | `5eca2be25ad87094dff25996dcf39cfc9e49917fd6601a0d488944672cef0eba` |
| `test suite reduction/tsr_greedy_cln_adq.py` | All 355 lines/11,560 bytes; reset/fallback selection and helpers | `9f6f8dfe8f8bda16a2a9576bf14cb558dd3116d0fad5ae5550cf78ffb83a9dd4` |
| `predicting test suite effectiveness/number of test cases/statement coverage/tsep_clnstmt.py` | Lines 1–275 of 468/18,353 bytes; remaining estimators not fully read | `27676974b34b3bae75ca1e773bd9280f421d0e5a5b1102150c9ccbccf0a92c51` |
| `probabilistic coupling/my_mut_pc.py` | All 218 lines/8,389 bytes | `7e1010a64eb37929bc1eae79eb6243fe928733976226e44cc1063b44b9a5d2ab` |
| `probabilistic coupling/my_stmt_pc.py` | All 187 lines/6,580 bytes | `63d9a93c25f9a2347c5160efbb59cbb228c7ec86a081ca9f0b2a266e1389d255` |

Other named Java/tuning/prediction files received only selected search hits, not complete-source credit. Prioritization means are read from output data, not regenerated by a reconstructed runner.

The mutation generator updates its previous score after accepting a test, supplying the assignment omitted by Algorithm 1. Its known-fault label comes from developer trigger metadata; this read does not re-execute faults. Kill-map rows are treated as kills without an active status filter; no claim that this is wrong is made without a separately verified format interpretation.

The reduction script hardcodes a coefficient and a joda-time example, performs five repetitions, and references three cost-map functions that are neither defined nor imported in the file. Its selected-score reset mechanism can change behavior even though the uniform one-test penalty cannot change candidate ranking at a fixed iteration. No silent source repair or executable-reproduction claim follows.

The inspected statement-prediction script reads a four-column CSV yet selects column indices 6 and 4. Its internal scoring calls macroF1/macro geometric mean, while the paper supplies binary formulas. The LR`C`literal is 1e−6 versus supplement 1e−5. It splits by suite row, fits its scaler on the entire training portion before cross-validation and uses already-produced residuals. These concrete interface/estimation differences prevent certifying an exact paper-to-script rerun, without erasing arithmetic agreement in separate output files.

Both coupling scripts include JacksonDatabind, explaining why their intended directory population can exceed optimization's excluded-project population. The mutation function maximizes trigger overlap among selected tests, then averages suites. The statement function averages over class-by-suite combinations; its parser can return Python lists but its consumer calls string methods. Neither matching PC output nor the complete referenced suite trace is present in the inspected package inventory. Consequently.46/.85 remain publication values with a more specific implementation/weighting uncertainty, not reconstructed comparable probabilities.

## Disposition

The released counts and aggregate selection outcomes are usable, bounded evidence. Causal identification, exact PROCESS estimates, fold-specific preprocessing, known-fault grouping, PC aggregation and final-publication/script binding remain separate limitations. Recomputing means does not validate every inference, and a source discrepancy does not negate every observed benefit. The package and all copyrighted files stay in ignored local artifacts/Zotero.
