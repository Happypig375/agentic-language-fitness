# S185 — Published aggregation and source correspondence

This bounded passive inspection accompanies [the complete paper reading](S185-cognitive-complexity-validation.md), 2026-10-02. It executes no author R, SonarQube measurement, participant task or experiment. Our own code only inventories files, reads published cells and checks elementary counts/formulas.

## Identity and coverage

Paper reference 3 resolves to [Zenodo 3949828](https://doi.org/10.5281/zenodo.3949828), release v1.0, 17 July 2020. The archive `mmunozba/esem20-cognitive-complexity-validation-v1.0.zip` is **13,219,712 bytes**, SHA-256 `776a7bb2463bd880a04fb32e8d66be9095a237e6eecf45accb2c456f33d9028a`, MD5 `f8e780a074b958d4dc8cd7a383ad45fe`, matching Zenodo's declared MD5. It has 216 regular files, 17,785,757 uncompressed bytes, under `mmunozba-esem20-cognitive-complexity-validation-fb50a59`. The complete archive is attached and byte-verified under native parent `P8K8Y4LX`, attachment **`BRA4J3PB`v5115**. Archive acquisition is not a claim that every member was read.

| Complete text/source reading | Bytes | SHA-256 |
| --- | --- | --- |
| `README.md`, all 13 lines | 1,589 | `ec91ffec9004f7b3a5d2f34fd7ba8e9213b7dfec4bd3153efbfb383f205ed366` |
| `data-analysis/data-analysis.R`, all 360 lines | 18,707 | `67dc20c9b1da9174008cdfa205370d901ddf8f5ee48f08dd20969738ba741fac` |
| `data-analysis/dataset-descriptions.md`, all 306 lines | 16,395 | `b9b78cb172c09daae2495f3bcddf368a921644c06a97d286beeb15e28ccea6c2` |
| `systematic-literature-search/literature-search-overview.md` | 10,549 | `c3091e872acd94c0e17775037e5bbaa9c65a740ad84e6ecef5e95dbb0f9db870` |

All **five forest-plot PNGs** are visually inspected and correspond to the paper's time, correctness, ratings, physiology and composite plots. Other QQ/density/scatter plots and search-stage spreadsheets are not read as complete artifacts. No original-study source links are followed to claim primary readings of those ten studies.

The read-only workbook `data-analysis/dataset.xlsx`, **91,139 bytes**, SHA-256 `98a3db9a763a51da220027e2066e9c5a72a0ccb353861e0e39e8a5bb2d312097`, is parsed with our standard-library ZIP/XML reader. All populated cells are machine-inspected for identity, counts and formula correspondence; manual coverage is the headers, representative rows, all forty study-8 time rows, selected identifier overlaps and printed check outputs. This is not a claim of manually reading every value. No workbook is modified and no dependency is installed.

| Sheet | Data rows | Variables | Interpretation |
| --- | --- | --- | --- |
| time | 369 | 13 | Repeated outcomes; nine studies contribute 327 representative entries |
| correctness | 269 | 7 | Six studies; study 4 has two disjoint task groups |
| ratings | 256 | 6 | Four studies / 203 entries after accounting for repeated outcomes |
| physiological | 36 | 3 | Three outcomes on the same twelve snippets |
| composite | 269 | 7 | Derived from time/correctness aggregate cells |

These **1,199 measurement rows** are published aggregates, not the approximately 24,000 original human responses. The 427 representative entries have 406 distinct study/snippet-label keys because study 8 reuses labels. This does not establish that there were only 406 distinct source programs.

## Analysis source: what the reconstruction establishes

`data-analysis.R` lines 16–21 load five already prepared sheets. Lines 45–86 calculate Pearson, Spearman and Kendall correlations over each variable's rows, retaining the row count. Lines 97–137 build seven composite variables from paired columns **by row position**, using their observed maxima. The produced workbook is a separate output; the script initially reads the composite sheet already included in `dataset.xlsx`.

Our check verifies that all seven paired identifier orders match and all **269 saved composite values** agree with the printed formula to maximum absolute difference **5.56×10⁻¹⁷**. This verifies aggregate-cell arithmetic, not whether the original human data were correctly aggregated or whether the construct is valid. Study 4's complex-task maximum correctness is .8333, study 6's .8148 and study 9's .6508, illustrating why composite zero need not mean perfect answers.

Lines 144–217 generate distribution checks; those tests are not rerun. The later selection uses Pearson for study 4's complex-task time variable and study 2's BA31post measure, with transformed Kendall coefficients otherwise. Lines 272–275 implement `sin(pi*tau/2)`. Lines 278–290 combine selected repeated outcomes with an **arithmetic mean of correlations**, retaining the first sample size. Lines 294–303 combine the two study-4 task groups with an arithmetic mean and summed size. Lines 308–311 call `metacor` using Fisher-z correlations, a random-effects result and Sidik–Jonkman tau estimation. No general outcome-covariance or multilevel structure is specified in this read file.

Repeated outcomes include study 7's first-impression time, thinking time and their total, study 9's two time measures, and paired ratings in studies 1/9. The three physiological outcomes remain separate twelve-snippet rows. Calling the analysis multilevel does not itself resolve these dependencies. The dataset descriptions explicitly document study 2's code subset from study 1; all twelve identifier/metric pairs correspond in the workbook. This does not imply identical human responses.

## The study-8 descriptive discrepancy

The descriptive routine at lines 236–246 retains the first observed `(did, snippet_id)` pair. Study 8 has forty JavaScript rows but nineteen distinct labels; `aStructure`, for example, appears with scores 9, 13 and 17, while `bStructure` has 10, 16 and 23. Some repeated labels also have unchanged scores and different times. Without the original source bodies these labels cannot safely be treated as unique program identities or accidental duplicate observations.

Our elementary summaries give:

| Study-8 interpretation | n | Median | Minimum | Maximum | Sample SD | Rows above 15 |
| --- | --- | --- | --- | --- | --- | --- |
| All released time rows | 40 | 5 | 1 | 23 | 5.16894 | 4 |
| Source's first-seen identifier filter | 19 | 4 | 1 | 14 | 3.60312 | 0 |
| Paper Table 2 | 40 stated | 4 | 1 | 14 | 3.60 | Not tabulated |

The filtered values explain the printed descriptive statistics, while the correlation routine uses all forty rows. Other studies' first-seen metric summaries correspond to Table 2. We have **not recalculated the reported correlations, meta-analysis or confidence intervals**, and do not infer that the original effect estimates are invalid from this descriptive mismatch. The release does narrow a specific range/threshold claim.

## Limits and consequence

No SonarQube version lock or complete source-measurement pipeline is established by the four read files. Search exports, original code, original human observations, author environment and exact final-publisher correspondence remain outside the reconstruction.

Preserve the paper's favorable average time/ease associations and mixed correctness evidence. Its released aggregation is substantially inspectable, but data availability, a matching plot and verified cell arithmetic are different from independent reproduction or causal validation. This supplement changes the interpretation of metric range, observation dependence and the composite outcome; it supplies no Nu, F#, agent-repair or live-evolution benefit estimate.
