# S168 — suite size, predictive adjustment and selection tradeoffs

## Identity and coverage

Zeyu Lu et al., *Understanding the Potentially Confounding Effect of Test Suite Size in Test Effectiveness Evaluation*, ACM TOSEM35(5), article 129, April 2026, [DOI10.1145/3748504](https://doi.org/10.1145/3748504). Crossref and the supplied final PDF agree on title, authors and edition:54 pages,67,404,947 bytes,SHA-256 `2caded496d79eedef322521a63e3d5930cf17ceb89f39fe93e6e23465685c13b`. Received 2023-11-30, revised 2025-03-28, accepted 2025-07-07; Table 1's own-study year 2023 is not the final publication year.

Native parent/PDF **`UVZ6NCSS`/`VPAZE53N`**, original note **`CC439SXZ`** and refresh note **`PNG9QCLI`** existed before body reading; DOI, collection`PKLXQNEE`, file bytes and current versions were reverified. The original note receives this reconstruction; the historical refresh note and memberships are preserved.

**All 54 pages, eight figures,26 tables, Algorithm 1,24 numbered equations and 120 references are read.** Visual pages 6,7,9,10,13,14,15,17,18,20,21,22,23,24,25,27,28,29,30,31,32,33,34,36,37,39,41,45,46 cover every structured result. Truncated text from pp.38–39 was explicitly reread before completion. The [Figshare v5 supplement](https://doi.org/10.6084/m9.figshare.24598707.v5), deposited 2025-02-23, is attached as **`CHMX4VQ6`**. Its seven-page PDF is fully read, including twelve tables and visual pages 2–7; all three READMEs are read. Its placeholder DOI and earlier date make it a distinct artifact version, not assumed byte-equivalence to the final article. Exact identities and bounded passive checks are in the [artifact note](S168-artifact-check.md). No author analysis, tests, models or simulations were executed.

## Question, sample and generated suites

The study asks whether test-suite size accounts for part of the association between statement/branch coverage or mutation score (**X**) and detection of a known defect (**Y**), and whether a size-adjusted score helps prediction, reduction or prioritization. Size **Z** is primarily the number of test methods; test LOC and assertion counts provide alternative analyses. These quantities are not interchangeable with developer work, execution cost or independent behavioral obligations.

The source is Defects4J2.0.0. The retained sample is **565 defects in 16 projects**, after mutation/analysis failures and a 20-hour processing deadline. Supplement Table 2 lists 4 mutation-tool failures,44 mutation failures and 209 analysis failures:257 in these categories. The selection is operationally constrained, not random sampling of all faults. Do not infer coverage of every original defect from the retained count.

Instrumentation/mutation targets the classes changed by each developer fix, using information from that fix. Coverage is collected on fixed versions with Cobertura; Major supplies eight operator categories. Uncovered mutants are excluded and equivalent mutants remain unresolved. Coverage and mutation values are normalized against what the relevant developer-test pool can attain, rather than all potentially executable program behavior. The pools contain a known triggering test; they range from 1 to 4,011 methods (mean 450, median 230), totaling 254,122 test occurrences across versions and 290,422 mutants.

Suites are generated toward twenty 5%-wide criterion intervals. A random proposed test is accepted only when it adds a goal; overshoot restarts and repeated failure can abandon an interval. Up to two suites per interval are produced. Thus criterion, selected tests, attained score and size are jointly determined by the selection procedure. This is not random size assignment with otherwise fixed behavior. The printed Algorithm 1 omits updating the previous score after acceptance; the released mutation generator **does update it**, so the omission is not evidence that the implementation lacks the update.

| Selection criterion | Released suite rows | Rows detecting the known defect | Detection fraction |
| --- | ---: | ---: | ---: |
| Statement coverage | 17,603 | 3,613 | 20.52% |
| Branch coverage | 18,044 | 4,225 | 23.41% |
| Mutation score | 19,229 | 5,564 | 28.94% |

Own arithmetic reproduces all 54,876 rows and labels. They are multiple suites from 565 defects, not 54,876 independent faults. The mean selected sizes are 6.44%,6.79%,8.01% of their full pools. Even the highest-score bins have detection probability below.71. This preserves useful selection information while rejecting score completeness as a behavioral oracle.

## What the confounding analysis establishes

Sections 3–4 model a size–score association and a score/size–detection association. The paper argues that size is not a mediator because greater coverage need not require greater size, using examples of different test sets. **Our inference:** absence of a deterministic monotonic relation does not rule out a mediated process or identify a causal graph. Selection targets, test content and source/fault structure remain possible joint determinants. A regression coefficient change alone cannot decide that interpretation.

There is also a specific mathematical problem on p.9. Equation 3 fits `X = i + aZ + eX`; Equation 5 algebraically solves it forZ and calls the result the regression ofZ onX. Equation 7 then asserts `c = c′ + b/a`. **Own derivation:** for ordinary least squares with nonzero variance and slope, the reverse-regression slope is `Cov(X,Z)/Var(X) = r²/a`, not`1/a`, except at perfect correlation. The inverted error term remains associated withX, so substitution does not turn it into the residual of the marginal regression. For a linear outcome, the usual omitted-variable identity would use the separately fitted reverse slope. Logistic conditional and marginal coefficients introduce a further scale issue.

The article recognizes logistic scaling and proposes standardization, citing mediation methods. [S209](S209-logistic-mediation.md), its reference 84, is now fully reconstructed: it explicitly distinguishes the product and difference estimators, their scales and causal assumptions. Its simulations support selected product-based estimators under specified models, not inversion of the wrong regression or automatic confounding removal. [S210](S210-mediation-confounding-access.md), reference 67, now has all nine original-journal pages reconstructed from the supplied native PDF. Its Equations 1–3 estimate the third variable on the predictor, confirming the direction required for the OLS coefficient-difference/product identity. Its worked arithmetic is checked; causal interpretation and the external simulation supplement remain separate.

The paper reports PROCESS with 5,000 percentile bootstrap samples, plus bias-corrected and Monte Carlo comparisons. The released package contains neither the R/PROCESS syntax nor the residual-producing analysis. Consequently the p.9 derivation can be challenged directly, but **we cannot establish that the published estimates were actually calculated as`b/a`** or silently replace them with invented corrected effects.

Reported significance occurs in 11/16 statement,10/16 branch and 11/16 mutation project analyses. Cli, Gson and Mockito are null for all three; JacksonDatabind has a negative indirect/suppression direction. Selected significant-project aggregate fractions are 12.19%,12.62%,10.85%; all-project aggregates are 11.03%,10.63%,9.17%. The selected subsets differ:480/403/414 faults and 15,069/12,881/14,149 suites. Absolute-valuing the negative term when constructing a positive fraction also changes its interpretation. These are not percentages of independently established causal benefit.

Alternative size definitions yield different significant-project counts: LOC10/11/9 and assertions 9/9/6. Preserve these and the null projects; do not select only a favorable common sample after seeing significance.

## Residual scores and prediction

Equation 9 defines an adjusted score by subtracting fitted size contribution and intercept. OLS residuals are orthogonal to the fitted size regressor **in that fitted sample**; this does not establish statistical independence, remove every size-related pathway or recover a causal effect. A subsequent near-zero linear indirect-effect check on those residuals is not independent validation of the causal claim.

The released adjusted files match `X − aZ + intercept`, differing from Equation 9 by twice the intercept. Their global files use a fit to the combined selected-project sample, not concatenated project-specific residual values. Own arithmetic confirms both correspondences. The constant shift preserves correlations and disappears under ordinary within-dataset centering/standardization, so it is a specification discrepancy **without evidence of a reversal of the reported prediction results**.

Seven classifiers are compared with a random 80/20 suite split stratified on the defect label, and five-fold tuning inside the training portion. This is not a held-out-fault or held-out-project evaluation; suites from a fault may contribute to both portions. Project selection and published residual construction precede that split. The inspected script scales the full training portion before its internal cross-validation; it correctly transforms the held-out portion using the training scaler. The released statement script additionally selects columns absent from its four-column CSV, uses macro scoring where the paper displays binary formulas, and has an LR setting differing from the supplement. These are static reproducibility limits, not observed failed runs.

Reported prediction generally falls after adjustment; adding explicit size improves many comparisons. Mean F1 increases with added size by 3.92%,1.13%,.10% for raw statement/branch/mutation scores and 9.88%,9.48%,6.70% for adjusted scores. The raw mutation G-mean change is−.01%, which must not be erased. Figure 5's absolute performances remain below.7. The reported mutation>branch>statement order is across different selected populations and generated suites, not a common-population intervention ranking.

The Wilcoxon comparisons use seven algorithms' validation/test summaries as fourteen pairs. These are dependent analyses of shared data, not fourteen independent sampled faults. RQ5 uses mutation score as the response for seven regressors; reported meanR² is.5935/.6865 for statement/branch and MSE.0313/.0245. This is a proxy-prediction result, not additional known-fault sensitivity evidence; combining negative MSE andR² into fourteen pairs does not make them interchangeable independent outcomes.

## Reduction and prioritization: benefits with their costs

Optimization uses significant-project subsets and excludes JacksonDatabind for processing cost: **10/9/10 projects,418/341/352 faults**, with five tie-breaking repetitions. Mutation additionally filters the candidate tests to ones covering mutants. These comparisons therefore differ in opportunity as well as criterion. The raw greedy minimum variant retains more tests and detects more faults than the raw maximum variant despite common adequacy: criterion satisfaction leaves consequential selection choices.

The main adjusted comparison uses an **adequacy-preserving reset rule**. Penalizing every proposed one-test addition by the same size slope does not itself change that iteration's ranking; reaching the adjusted threshold triggers a local-coverage reset, with global-uncovered goals prioritized and a raw-greedy fallback. This changes the selection procedure and often retains more tests. It is distinct from simply stopping early at an adjusted threshold, which can lose raw adequacy.

| Criterion | Raw → adjusted proportion removed | Raw → adjusted fault-detection loss | Repetition rows |
| --- | ---: | ---: | ---: |
| Statement | .85937 → .80509 | .36651 → .29474 | 2,090 |
| Branch | .85095 → .79866 | .32082 → .26100 | 1,705 |
| Mutation | .81861 → .78417 | .16136 → .11648 | 1,760 |

Own released-data means support these directions. Detection-loss improvements are about 7.18/5.98/4.49 percentage points while the retained test fraction increases 5.43/5.23/3.44 points. A ratio of these two differently meaningful fractions above 1 is a declared tradeoff, not measured economic cost-effectiveness or dominance at equal execution cost. Measurement/analysis overhead is not included. Some projects are null or adverse: branch-based JacksonCore loss rises.23846→.26154. Lang's printed reduction median/delta do not match its released data; the aggregate favorable detection direction survives.

Prioritization uses APFDc with LOC, assertion or execution-time costs. Its aggregate coverage-based changes are positive and small, while **mutation-based changes are adverse on all three cost variants**:

| Criterion | LOC APFDc, raw → adjusted | Assertion APFDc | Time APFDc |
| --- | ---: | ---: | ---: |
| Statement | .84479 → .84940 | .83933 → .84490 | .86148 → .86664 |
| Branch | .8334 → .8356 | .8284 → .8329 | .85603 → .85878 |
| Mutation | .7838 → .7779 | .7649 → .7634 | .81903 → .81478 |

These are repeated known-fault tasks, not prospective fault populations. Project win/loss counts and aggregate magnitudes answer different questions. Own arithmetic reproduces the directions; minor last-decimal correspondence differences are retained in the artifact note rather than claimed as exact reproduction of every printed value.

## Coupling, transfer and disposition

The coupling analysis reports adequate-suite averages near.46 for statement and.85 for mutation on different 480/414 fault populations. Unlike S165's maximum over the represented test universe, the released methods compute maxima within selected suites, then average; the statement code additionally averages class-by-suite maxima. Both scripts include JacksonDatabind in their directory lists, whereas optimization excludes it. No matching released PC output or complete suite trace closes the figure/data correspondence; the statement script also mixes parsed lists with string operations. Its statistic must not be equated with prospective detection probability or compared as a pure criterion effect on a common population.

**Credited evidence:** a substantial published suite dataset, relationships between size/score/detection, useful selection variants, lower average reduction loss at greater retained size, small favorable coverage-prioritization changes, and adverse mutation-prioritization outcomes. **Unsupported extension:** that residualization has identified and removed causal confounding, that one criterion has a universal real-fault ranking, or that these results validate a complete temporal oracle, Nu benefit or D1.

For ISE, preserve assigned architecture/feedback opportunity, intermediate edits/tests/size, independent outcome and missingness as separate variables. Do not condition the primary total-effect comparison on post-assignment success, output size or selected significant cases and call the result a pure mechanism effect. A useful reduction heuristic can remain useful without its causal explanation being established. [S169 ASSENT](S169-assent-proxy-evaluation.md) now closes the selected ground-truth/agreement dependency with a complete 32-page final-journal reading; its earlier 2022 v1 remains partial. Its conditional proxy sensitivity and source/data limits reinforce the need to distinguish the target, comparison construction and agreement rule. Continue the independent persistence/runtime frontier. S174/S175/S177/S178 and the independent persistence/runtime/type frontiers remain open. No experiment or new worker follows from this reading.
