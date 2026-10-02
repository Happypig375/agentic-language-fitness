# S169 — passive ASSENT artifact correspondence

The [publication note](S169-assent-proxy-evaluation.md) owns the method and scientific interpretation. This inspection consumes released files and performs our own counts, means and elementary arithmetic. It does not run/import author programs, generate suites, execute tests, fit models or reproduce the experiment.

## Identity and actual coverage

[ASSENT](https://github.com/zhangpengNJU/ASSENT/tree/eea99de3c4f5408193c27dc863cd9e85efd9e86f), commit **`eea99de3c4f5408193c27dc863cd9e85efd9e86f`**, 2023-09-25T11:25:03Z. The final paper's reference dates access to that day, but its revision is later; exact final-analysis binding is unestablished. The untruncated Git tree has 314 entries. The pinned ZIP contains **303 files, 1,575,977 uncompressed bytes**; ZIP 1,196,216 bytes, SHA-256 `6fc59debea28388c28aaf9fc7e9c99a8156ad9dbdb78cf4555300906754bf769`, MD5 `735502e5f490752b324df29de859fed2`. Native attachment **`WNTB4YY7`** is under parent `M52NJ7J3`, with uploaded bytes read back and verified.

All README text is read (4,024 bytes, SHA-256 `02576b44cef39da7e9f59384d68274a532a89e09d40d48cf9b2de756a12a1208`). Complete static source coverage: `RQ1-3/RQ1.py` (652 lines), `RQ4/compareAutoTest.py` (366), `RQ5/RQ5.py` (501), `RQ5/GetBranchCov.py` (47), and `RQ6/RQ6.py` (468). `RQ4/RQ1.py` is compared in full against the first file: its only change removes the final `main()` invocation. No GUI implementation or generated-test body is credited as read.

| Source | SHA-256 |
| --- | --- |
| `RQ1-3/RQ1.py` | `adcfe1d305358ae40736e61d8a413295f557368e171b5cf33acf8ca505a38e3e` |
| `RQ4/RQ1.py` | `f77ffbfbc9be36eb95da2ae15afd3964cb56aa05f42b5ff8c788bd4294348ce4` |
| `RQ4/compareAutoTest.py` | `85b3959c789213fcf3a1ccd74183d0f4a58a735dde1a7af9b17f690d8e7ce357` |
| `RQ5/RQ5.py` | `65d6ec11a9da7ed9de300073e96a63a7dbd8f6d22721fa503b49191ce8437306` |
| `RQ5/GetBranchCov.py` | `e198e3cc839f87fe553d7da182aabb96b0250597915b41841f518aa322d37146` |
| `RQ6/RQ6.py` | `e661da193fa7e52df2d8aafe76520c5cf0711adedb1afa43008eeec6af201af5` |

Own aggregation consumes **31 result CSVs**: fifteen RQ1, fourteen merged RQ4, one RQ5 and one RQ6. Another **122 individual RQ4 CSVs** receive row/column inventory only (one row each), not independent-result credit. All 123 test-archive filenames receive project/bug identity checks; archive contents are not inspected. Per-file bytes/hashes and derived checks remain in ignored artifacts.

README links three Figshare raw-coverage deposits. Metadata, names, versions and declared MD5 are checked; **their bodies are not downloaded/read**:

| Deposit, all v1 on 2023-09-21 | Declared file | Bytes / MD5 |
| --- | --- | --- |
| [24168123](https://doi.org/10.6084/m9.figshare.24168123.v1) | `b1.zip`, file 42405720 | 16,460,943,957 / `f79baf65af15d4634a8d52050f1c786c` |
| [24171789](https://doi.org/10.6084/m9.figshare.24171789.v1) | two `b2.zip` entries, 42412149/42412344 | 9,744,493,551 each / `71b6d7f1ca8becfd716625d48821d2bb` each |
| [24166641](https://doi.org/10.6084/m9.figshare.24166641.v1) | `statement.zip`, file 42403707 | 19,506,396,654 / `69e789ae37e3feb1a40e8d190b465e74` |

One copy of each distinct declared package totals about 45.7 GB. These remain available but uninspected raw dependencies, not access-denied evidence. They are unnecessary for the bounded published-summary checks below; execution/reproduction remains outside this assignment.

## RQ1: conditional sensitivity, different membership

The fifteen CSVs contain **366 rows for 360 distinct project/bug keys**. JacksonXml's six rows are each repeated exactly, leaving its project means unchanged. The paper's Table 4 ranges enumerate **353** IDs, its stated sample and Venn diagrams use **361**, and the release uses the separate population above.

The three membership differences are explicit: Chart has 18 released versus 14 listed IDs (table-only 4,10,14,15,19; release-only 6,7,8,12,17,21,22,23,24); Closure adds 152,153,159,163 beyond the listed 22; Mockito omits listed 35. Do not silently choose a corrected publication denominator.

Released project means are SC .53274385, BC .60933232, MS/SMS .80150747, CMS .42376925, RMS **.57130887**, COS .63813919. Apart from small printing/rounding differences, Table 5 agrees except **Compress RMS: .65769231 released versus .784 printed**, which accounts for the material overall RMS difference (.5713 versus .580). Mutation's principal conditional advantage survives this discrepancy.

MS and SMS agree on every released row. The raw released MS/SC/BC Venn regions match the publication except all-three **187 versus 183** and none **50 versus 49**. COS/SC/BC similarly differs in all-three **161 versus 158**, SC-and-BC-only **35 versus 34**, and none **70 versus 69**. Repeated JacksonXml rows do not alone reconcile every region to the printed population. These are source/data differences, not a fresh fault-detection experiment.

The source computes strict score increases, twenty RMS/CMS selections, and coverage after removing trigger methods. The README describes row/column orientation incorrectly: actual rows are bug records with eight fields. It also says RQ2/RQ3 require modifying RQ1; no separate released code or result file supplies those variants. The main script is a configured partial-project runner, not the exact all-project analysis manifest. No unsupported inference about the original execution follows.

## RQ4: matching means with duplicate weighting

Fourteen merged files contain **131 rows for 121 unique project/bug keys**. Chart contributes nineteen rows for nine keys; eight keys repeat. All seven aggregate project means and the individual project summaries reproduce Table 10 to its displayed precision, preserving the positive automatic-pool result.

There are **123 distinct project/bug archive names**, agreeing with the paper's generated-suite count. Chart 5 and JacksonDatabind 4 have archives but no merged result. The 122 individual result files are not substituted for the published merged weighting. Duplicate keys could represent repeated outputs or repeated measurements; no replicate metadata justifies treating them as independent faults. The paper-to-artifact population/weighting gap remains.

The inspected generator uses a 300-second EvoSuite budget, runs fixed-version-generated tests against buggy versions, and skips empty/failed trigger extraction and zero mutation scores. That confirms selection on generated fault exposure, not random retention of the original developer-pool sample. Raw generated Java bodies and their oracle adequacy remain uninspected.

## RQ5/RQ6: missingness and population are consequential

`RQ5/reault/result.csv` (the directory is spelled this way) has two headers and **322 distinct identifiers**, each with 105 correlation fields: seven metrics × three coefficients × five sampling ratios. SHA-256 `8ffb9a9afe508d8fa051870748b504a99fc0ac14e09bcdb2aac7ac38d5b7aa6b`. It does not provide the original 100-suite score/label vectors. Finite-value arithmetic supports broadly low non-BC correlations but is not a rerun of the correlation estimates.

| Sampling ratio | BC NaN entries per coefficient | BC values exactly −1 | Other finite BC entries |
| --- | ---: | ---: | ---: |
| 10% | 29 | 28 | 265 |
| 20% | 284 | 28 | 10 |
| 30% | 293 | 28 | 1 |
| 40% | 293 | 28 | 1 |
| 50% | 294 | 28 | 0 |

The source directly calls SciPy correlation functions and writes −1 for a missing-length BC vector. It contains no final aggregation/filtering script explaining the plotted BC means. README attributes −1 to branch-data failures. NaN and missingness must stay separate from observed zero/negative associations; −1 in other metrics is not automatically a sentinel. This snapshot cannot establish the final paper's positive BC curves or a common complete-case comparison.

Static RQ5 source additionally refers to global `i` in the output filename before the shown top-level loop defines it. RQ6 opens its output once but closes it inside the first successful iteration and catches subsequent exceptions. These are concrete standalone source/output correspondence limits, not failures observed by executing either file. Both consume external kill/coverage formats; without inspecting the raw archives, their truthy string kill-field test is not labeled a demonstrated erroneous count.

`RQ6/pc.csv` has **366 distinct identifiers** and reproduces all six published PC means: .86728658/.83402136/.69990059/.58097265/.72899022/.66996472. SHA-256 `0d4265622580df6c070e7c333d0c25101a5306179bb8bacce6f583600f05d7f0`. The file includes **72 Jsoup identifiers**, whereas Table 4 supplies no Jsoup main-sample IDs. It therefore does not certify a robustness comparison over the same fault population. The source maximizes observed trigger fractions per goal; original rows/matrices and selected-mutant identities are needed for a full trace.

## Disposition

The artifact supports the automatic-pool means, PC means and much of the manual sensitivity comparison. It also bounds exact population, missingness, tie-rule and final-analysis claims. These distinctions preserve useful positive/null evidence without inventing reproducibility or upgrading agreement to a complete correctness oracle. Copyrighted bodies, source and extraction dumps remain in Zotero/ignored local artifacts.
