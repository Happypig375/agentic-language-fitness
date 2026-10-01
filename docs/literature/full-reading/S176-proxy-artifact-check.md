# S176 — passive check of released proxy-analysis data

This supplements the [complete S176 paper reading](S176-llm-proxy-replication.md). It reconstructs selected code and saved data, not the original model/test/mutation execution.

## Pin, acquisition and coverage

Repository [pin `4bc2ed63917557a8c879e6c733b8fa41c15b9871`](https://github.com/drixs2050/Cov_mut_bug_detect_correlation/tree/4bc2ed63917557a8c879e6c733b8fa41c15b9871). GitHub's recursive metadata tree contains **2,688 entries**, untruncated; filename inventory is not whole-content coverage. The unauthenticated API returned rate-limit 403; the already-authorized GitHub CLI retrieved the public metadata.

The [Zenodo concept](https://doi.org/10.5281/zenodo.21429528) resolves through its API to version **v1.0.1**, [DOI 10.5281/zenodo.21437945](https://doi.org/10.5281/zenodo.21437945), July 19, 2026, listing one **40,825,444-byte ZIP**. The ZIP was not downloaded. Git tag v1.0.1 points to `ec54e97222b08821e3b01a3f8e5b5a567abb2564`; the GitHub comparison with the chosen pin lists one later commit changing only README and .gitignore. The selected code/data are unchanged across those Git revisions; that does not independently verify archived ZIP bytes.

Native linked attachments `XYJRFMDL` and `S6AAJM76` preserve pin/archive locators. Cached source/data remain outside public Git. The local manifest hashes **113 files / 10,118,641 bytes**, plus README **9,638 bytes**, SHA-256 `4dc313aa967a6c3b27767e7cb6b66a5e44171807cdd80809bd3f311acca5f1a0`: **114 files / 10,128,279 bytes** in total. This includes **105 CSVs / 3,394,073 bytes**, six notebooks, a complete prompt example and the PIT wrapper, plus README. Notebook files are acquired whole, but source/output coverage is bounded below.

Read scope: full README and prompt; fixed-analysis cells 0–5, 8–14, 19, 24, 26, 28–29 and 31; buggy-analysis cells 13–14 and 20; selected cached tabular outputs; unification cells 0/4/6/8/14/22/27; cleaning cell 7; fixed-execution cell 53 and selected ranges in main cell 101; complete PIT wrapper. Plot cells were inventoried, not all executed or reconstructed. All **33,390 CSV rows**, headers and selected identity/eligibility/count/coverage/mutation fields were parsed with independent read-only code. The remaining generated code, raw logs, helper implementations and archive payload were not exhaustively read.

No notebook was imported/evaluated. No author sampler, new random draws, model, Java, benchmark or mutation engine ran. The Pearson calculations below use deterministic descriptive arithmetic on released aggregates, not new inferential tests.

## Rows, selection and size control

Every CSV has 318 rows and 34 columns, despite README's 33-column description. Each has 233 unique project/bug/version IDs; several focal-method rows belong to the same bug. A repeated ID is not automatically a duplicate method: the CSV lacks a method-signature column, so row-to-source mapping is a separate unresolved task.

Unsized fixed/buggy sets each contain the thirteen paper configurations. Fixed size ten has an additional Qwen-3-Next-80B CSV, excluded by the notebook's original-model list. Buggy size ten has that extra model **and lacks Gemini-2-5-flash**, leaving twelve original configurations. Do not silently use the replacement as the missing model.

The fixed notebook admits a row if **all compiled OR partly compiled OR compiled-count ≥ k**. The buggy notebook uses only the first two flags. The execution harness subsamples only when the available compiled-test count exceeds k; smaller suites are retained. Counts from the original-model rows are:

| Input / setting | Original model settings present | Retained method rows | Rows with compiled count below k |
| --- | ---: | ---: | ---: |
| Fixed / 3 | 13 | 2,411 | 63 |
| Fixed / 5 | 13 | 2,408 | 188 |
| Fixed / 10 | 13 | 2,407 | 1,063 |
| Buggy / 3 | 13 | 3,326 | 209 |
| Buggy / 5 | 13 | 3,327 | 455 |
| Buggy / 10 | 12 | 3,087 | 1,537 |

These are method/configuration rows, not independent projects. Each fixed setting also retains 38 rows with zero compiled tests; unsized/3/5 buggy settings retain 34, and buggy ten retains 31 among its twelve original configurations. For example, the fixed Claude reasoning CSV includes Cli_32 with zero generated/compiled tests and “all compiled” set to one. Equality of zero compiled and zero generated in the harness can produce that flag. Thus “at least one compilable test” and “exactly k tests” are not enforced by the inspected path.

The retained unsized population varies by model: **155–218 fixed**, **235–273 buggy** method rows. The unsized 26 CSVs contain 8,268 rows but sum to **92,560 generated tests**, not the paper's 101,123. Raw-generation/extraction/repair accounting remains unresolved.

## Positive numerical binding and denominator sensitivity

The analysis sums `Reported Bug`. For 100-row draws, a count and proportion differ by a common constant. In the inter-model full-population setting, the retained-row count differs by model. A count remains equivalent to detection per all 318 attempted methods, whereas dividing by each retained population asks a different conditional question.

Independent arithmetic on the unsized fixed CSVs reproduces the paper's central Pearson coefficients:

| Metric versus detection | Count target / common 318 denominator | Detection per retained method |
| --- | ---: | ---: |
| Mean branch coverage | .860969 (paper .861) | .649905 |
| Mean raw mutation score | .863312 (paper .863) | .694467 |

The right column is a sensitivity to the estimand, not a corrected publication value or an inferential claim. Positive association remains in both. No independent model selection, net-cost or future-fault benefit is demonstrated by either column.

For fixed sizes 3/5/10, count-target branch correlations are .678644/.854555/.858473 and raw-mutation correlations .702328/.694936/.833145, matching the printed rounded values. This binds those tables to the retained/capped data; it does not repair the exact-size discrepancy. Conditional-rate raw-mutation values are .337277/.602926/.836152, illustrating how different eligibility denominators can matter.

Buggy-input mean-branch/count values are .349239 unsized, .407331 at three, −.050817 at five and .391065 at ten (twelve original settings). The size-three result slightly exceeds the paper's own .4 threshold for “weak”; its conditional-rate counterpart is .427807. Treat “uniformly weak” as an overbroad summary for this release, without substituting threshold labels for effect interpretation or extrapolating to unexamined metrics.

The fixed notebook currently selects all thirteen configurations, but cached correlation tables inspected in cells 19/24/29/31 have **n=1,000**, a single-model-sized output. Source configuration, stale cached outputs and paper tables are different evidence. The configured loop could pool up to thirteen thousand overlapping draws, not thirteen thousand independent generated suites. Camera-ready plotting cells contain transcribed values, as README explicitly states; they are not independent recomputation.

## Measurement and source correspondence

- The unification function accepts only public/protected methods and explicitly excludes default/package-private methods. This differs from the paper's non-private rule.
- The pipeline initializes metric/status fields to zero and records failures separately. The analysis does not filter on metric-success flags. Among 2,411 retained unsized fixed rows, 1,217 have branch-success zero and 341 mutation-success zero. These flags can mix unavailable measurements, errors and no applicable opportunities; they are not all proven execution failures or genuine zero coverage.
- The cleaning cell converts any floating value in [0,1] to a percentage, irrespective of column type. Full JSON-to-CSV correspondence was not audited, so no quantified corruption claim follows.
- The full PIT wrapper mutates `target_class_fqn` and parses its final class-wide “Generated/Killed” summary. No focal-method argument/filter exists in that path. Its default mutator setting is ALL, with overridable timeouts; unseen execution environment values remain unbound. This differs from the paper's focal-method raw-denominator description.
- The normalized score denominator subtracts a parsed “no coverage” count if present; otherwise the wrapper falls back to all mutants. Therefore the semantics depend on the available log, not simply a label.
- Fixed-execution code removes tests failing on the fixed version before the PIT call. The mutation suite can differ from the original suite used for real-bug outcomes/coverage.
- The paper/README call the ordinary metric statement coverage from CodeCover, while Zenodo describes JaCoCo coverage, PIT mutation and CodeCover condition coverage. The inspected notebook reads ordinary coverage from the existing execution report and condition coverage through a separate helper. Whole-helper/log verification is still needed to settle the exact metric definition; do not normalize the discrepancy away.

These limitations qualify size-control, metric-equivalence and generic-validity claims. They do not erase the reproduced favorable model-level association or prove the underlying application test executions wrong. Full raw-log correspondence, all tool outcomes, archive bytes, alternate analysis revisions and the omitted coefficient sets remain outside this bounded check.
