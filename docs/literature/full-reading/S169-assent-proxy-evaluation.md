# S169 — ASSENT, ground truth and proxy agreement

## Identity and coverage

Peng Zhang et al., *Assessing Effectiveness of Test Suites: What Do We Know and What Should We Do?*, ACM TOSEM 33(4), article 86, April 2024, [DOI 10.1145/3635713](https://doi.org/10.1145/3635713). The final publisher-formatted PDF is lawfully available from [coauthor Xiao Yu](https://xiaoyu-cs.github.io/pdf/TestSuites.pdf): **32 pages, 2,925,263 bytes**, SHA-256 `9c070267b28a7401cbc005689323dc3034b49ed0d001f24e2e64252e98b5bf7e`. Received 2023-04-30, revised 2023-11-08, accepted 2023-11-22. The final author list includes Zeyu Lu and Xiao Yu.

Existing native parent/note **`M52NJ7J3`/`WQQUR4JR`**, DOI and collection `PKLXQNEE` were checked before reading. New final attachment **`DNSWYPES`** preserves the earlier **`QYPX52BD`**: eleven-page arXiv 2204.09165v1, 2022-04-19, 3,039,506 bytes, SHA-256 `fe68129f8b0036b5e2304cc90db44ef541cfb55c1a9dd03c124d1edc10691a53`. That preprint has a different title and nine authors; it remains opening-only coverage, not another fully read work or an assumed equivalent edition.

**All 32 final pages, six figures, ten tables, eight numbered equations, the Spearman derivation, OP definitions, seven footnotes and 48 references are read.** Visual pages **7, 8, 10, 13–18, 21–28** cover the structured material (17 pages). The rotated Table 1 on p.7 was read visually after its extraction produced excessive spacing/truncation. The [pinned artifact check](S169-assent-artifact-check.md) separately records passive source/data coverage. No author program, test generator, correlation analysis or experiment was run.

## What the framework contributes

ASSENT separates three decisions often conflated in a proxy evaluation: what establishes the ordering of test suites, how the compared suites are constructed, and how agreement with that ordering is measured. Its GUI helps articulate a configuration; it does not supply an independent correctness oracle. Table 1 places earlier studies in this vocabulary, making unlike claims easier to compare.

The principal configuration takes the complete developer-test pool **A = T**, and **B = T − C**, where C contains all tests known to trigger the selected real fault. B is a proper subset, and A detects that fault while B does not. The **order-preservation measure OP** is the fraction of these pairs for which a metric also increases strictly. A metric tie fails to preserve this strict order.

For valid, noninterfering tests, retaining a superset preserves detection of faults already exposed by a subset. The paper extends that rationale to unobserved faults. **Our interpretation:** the construction identifies a useful conditional sensitivity question, but neither a strict advantage on unknown faults nor noninterference follows merely from set inclusion. S167 supplies concrete reasons to retain runtime/instrumentation assumptions. Conversely, a comparison of equal-sized suites against a specified known-fault endpoint remains a meaningful different question; uncertainty about other faults does not invalidate that endpoint.

The paper itself notes that **test count would attain OP = 1** under its principal configuration. Removing all triggers makes B the largest trigger-free subset, reducing the relative size difference, but size still perfectly orders every pair. High OP therefore does not prove practical value, equal-cost benefit or complete behavioral checking. The paper's stronger suggestion that low OP implies uselessness also exceeds what this particular endpoint establishes: earlier-stage selection, cost and a different fault population can give a proxy value under other conditions.

## Population, metrics and costs

The reported main sample contains **361 real faults in 15 Defects4J 2.0.0 projects**, excluding mutation failures and cases exceeding 30 minutes. Scores are calculated on **fixed versions**, because Major does not support the required failed-test handling. Known trigger metadata constructs the comparison; this is not a prospective independent-fault discovery experiment. The published membership table and released data differ, so 361 remains the publication's denominator rather than a reconstructed unique-file count.

Cobertura supplies statement and branch coverage (SC/BC). Major supplies the full mutation score MS and four reduced scores: five selected operator categories (COS), random 30% selection (RMS), dynamically subsuming mutants (SMS), and kill-vector clustering with one random representative per cluster (CMS). The cluster count is the selected SMS count. RMS/CMS are repeated twenty times. These selections use the observed pool's kill information; they are not semantic equivalence proofs.

Under the intended finite kill-set construction, MS and SMS have the same strict-pair sensitivity: an observed mutant killed only by triggering tests has a nonempty minimal kill-set descendant with the same property. This is an **existence argument**, stronger than the paper's assertion that the first witness must itself be subsuming. A correctly retained representative of each minimal class suffices. The released RQ1 rows do agree exactly on MS/SMS; that observation does not verify every property of the subsumption implementation. The relation connects to S173's observed coupling, without adding an independent real-fault replication.

The paper explicitly separates sensitivity from cost. MS/SMS/CMS require all mutant executions in this study; COS retains more than 30% on most programs, while nominal RMS uses 30% but twenty repetitions expose the full set here. SC/BC require no mutant executions. Execution counts are not measured end-to-end time, authoring burden, memory or maintenance effort.

## Positive, null and adverse results

| Published result | Meaning and boundary |
| --- | --- |
| RQ1 project means: MS/SMS .801, COS .638, RMS .580, CMS .424, SC .533, BC .609 | Full mutation scores most often register removal of known triggers in these retained developer pools. These are project means, not pooled fault proportions or future-fault probabilities. Released means broadly agree, with a material RMS discrepancy described separately. |
| Figure 2: MS distinguishes 296 of 361 faults; SC 204; BC 230; 49 distinguishable by none | Preserve both mutation's additional sensitivity and coverage's complementary 16 cases outside MS. This is limited observed sensitivity, not a complete oracle. The publication's Venn counts do not exactly match the pinned CSV population. |
| Table 6: COS/RMS adjusted p = .042; other listed pairwise p values exceed .05 | The retained comparison does not establish a general COS advantage over BC. Nonsignificance does not establish equality or equivalence. |
| RQ2 alternative mutation-based ground truth increases mean OP by reported relative 24–48% | The target changes; these are relative changes, not percentage points or a universal calibration error against real faults. SC falls in two projects. BC and RMS exchange aggregate ranks. |
| RQ3 equal-size comparison: MS .705, SMS .655, COS .547, BC .531, RMS .498, SC .439, CMS .362 | Lower aggregate sensitivity coexists with a mostly stable ordering. Some project/metric values increase. Removing random nontriggers from A changes the pair construction and removes subset ordering; it does not isolate one causal size mechanism. |
| RQ4 automatic pools: MS/SMS .963, BC .958, SC .819, CMS .800, COS .771, RMS .703 | All published project-mean summaries reproduce from the merged files, including project-level exceptions to the overall ranking. EvoSuite's branch objective and retention only of faults with generated triggers constrain transfer. The paper acknowledges this selection. |
| RQ5 fixed-ratio random suites have low reported correlations | This is a different suite population and estimand from full-pool trigger removal. Greater numerical separation under OP is not itself a validation of OP. The released BC missingness prevents reconstructing the published positive BC curves from this snapshot. |
| RQ6 mean PC: MS .867, SMS .834, RMS .700, CMS .581, COS .729, SC .670 | All six reproduce from the released 366-row PC file. This file includes projects absent from the principal experiment; it is not a verified common-population robustness check. |

RQ4's stated 123 generated triggering suites is supported by 123 named test archives. Its merged result files instead contain 131 rows for 121 distinct project/bug keys. Table 10's means nevertheless reproduce. This is a population/weighting correspondence gap, not a reason to erase those reported conditional means or infer a causal manual-versus-automatic effect.

PC maximizes, over goals, the observed fraction of tests hitting a goal that also trigger the real fault. It is a best-goal conditional probability in the available pool, not the probability that a high-scoring suite catches an arbitrary future fault. Using all available tests still does not enumerate the input domain. The paper's exclusion of BC because its chosen representation permits half achievement is a representation-specific limitation; distinct branch outcomes can in principle be binary goals. Repeated PC discussion in Sections 5.5/5.6 is one result, not two replications.

## Mathematical and analysis limits

The article's warning about tied binary fault labels and fixed generic correlation thresholds is useful. Its stronger mathematical claims need qualification.

- From its own Equations 3 and 5, with binary Y and nonconstant X, **tau-C / tau-A = 2(n−1)/n**, approaching two, not one. With balanced binary labels and perfectly separated unique X ranks, tau-C can equal one. The paper's claimed near-equivalence of tau-A and tau-C does not follow.
- For balanced binary Y with n = 2k and unique X ranks, our finite-sample maximum Spearman correlation is **sqrt(3k²/(4k²−1))**. It approaches the paper's sqrt(3)/2 limit but is slightly larger at finite n. The asymptotic argument is useful; it is not a universal exact bound for other tie patterns.
- At n = 1,000 with 500 labels in each class and no X ties, the maximum concordant-pair count is 250,000. Table 3 prints 249,000 alongside a tau-B value consistent with roughly 250,000. These local derivation/table issues do not negate measured selection benefits in S165/S166/S170.

For RQ2, with a fixed mutant subset, strict improvement of the reduced score implies strict improvement of MS. If a comparison credits both simultaneous increases **and simultaneous ties**, its agreement rate equals `1 − OP(MS) + OP(reduced score)`. Several printed rows are compatible with this arithmetic, but the released package has **no separate RQ2 or RQ3 script/output** and it is not an exact match for every row. This is an explicit possible explanation, not a claim that the authors used an inspected tie rule. A changed ground truth, eligible-pair population and tie convention must be specified before interpreting the increase as overestimation.

The [artifact note](S169-assent-artifact-check.md) records further concrete boundaries: RQ1 membership/RMS differences, duplicated rows, RQ5 NaN/sentinel coverage, RQ6's different population, and static source/output correspondence. No silently repaired author program or re-estimated model substitutes for unavailable analysis lineage.

## ISE disposition and continuation

ASSENT supplies a useful reporting structure for Nu/ISE: name the behavioral endpoint, construct comparable cases, and state how observations support that endpoint. Retain its positive conditional mutation sensitivity, coverage complementarity and automatic-pool results. Do not turn proxy agreement into semantic/temporal completeness, equal-cost usefulness, causal architecture benefit or evidence for explicit-case enumeration over a catch-all.

This closes the selected **published-method** gap left by S165/S168, while preserving exact artifact and alternative-analysis gaps. S169 reference 48, *Mutant Reduction Evaluation* (10.1145/3522578), remains the already recorded conditional OP/reduction predecessor, not a new full reading. Other existing adequacy/input-oracle routes remain available by consequence. The next independent priority is **B04/B06's persistent-vector, iterator and transient-update frontier**, because the Nu cost account still needs those actual mechanisms and workloads. No new experiment follows from this reconstruction.
