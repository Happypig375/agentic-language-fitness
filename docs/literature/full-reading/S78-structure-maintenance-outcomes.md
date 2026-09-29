# S78 — Program structure, task dependence and competing maintenance outcomes

**Complete publication reading, 2026-09-30.** Virginia R. Gibson and James A. Senn, *System Structure and Software Maintenance Performance*, Communications of the ACM 32(3), 347–358 (1989), [DOI 10.1145/62065.62073](https://doi.org/10.1145/62065.62073). Zotero parent `GJ5629H8`, user-library publisher PDF `XCRCLMX9`, note `5IHCL3BY`.

All twelve pages, four figures, eleven tables, Appendix A, fifty-two references and author information were read in extracted text and rendered images. The scan contains 1,625,444 bytes, SHA-256 `35897d778ceb5b7c8f37c9f669d1c5b0596a08ba42610939b7f6c43e4a57de61`. Renders resolved substantial OCR errors in names, sample size, table layout and ANOVA quantities; a larger p. 355 render verified the ranking discrepancy below. Printed aggregate arithmetic was checked. No participant-level data, source versions, complete test database or dissertation was acquired, and the experiment was not reproduced. The attachment supersedes the earlier publisher-download failure.

## Design and live relevance

B01/B10/B11/B12 concern actual maintenance outcomes, structural measures, expert judgments, task dependence and the distinction between local failures and regressions. Unlike [S79/S80's maintenance predictions](S79-maintainability-performance-case.md), this study has programmers implement changes and assesses the resulting modifications.

Thirty-six working COBOL programmers, averaging roughly seven years of COBOL and maintenance experience, each performed three tasks. A partially confounded 3×3 repeated-measures design used six blocks of six people, with counterbalanced sequences. Every person encountered each task and each source version once, producing **108 observations and twelve per task/version cell**, not 108 independent participants or all nine combinations per person. The two design replications are parts of this one experiment. The article does not establish a probability sample or fully describe random assignment/recruitment.

All versions derive from one approximately 2,000-line government ISAM file-update program. Version 2 eliminates long jumps and constrains control structures; version 3 further removes redundancy and raises procedural abstraction. Both changes increase other complexity dimensions, such as nesting or call-hierarchy intricacy. The authors call the versions functionally equivalent; independent equivalence tests were not available for this reading. These are compound source restructurings, not a single language feature or a functional/object-oriented contrast.

The tasks move duplicate-record detection earlier, add a missing EXIT operation, and add type/size information to a data dictionary. They are three perfective changes in one application, not independent task families sampled from a maintenance population. Participants received source listings, documentation, a walkthrough and familiarization time. They wrote changes **on paper**, to avoid unequal familiarity with an online environment. Compiler errors were ignored in later scoring. The absence of live build/test feedback is therefore part of the intervention setting and cannot be imported into a tool-using agent policy without qualification.

Time was recorded to the nearest minute. Confidence was self-rated after each task; complexity rankings were collected after all tasks. Modifications were evaluated afterward against test cases developed before the study. The paper does not establish blinded assessment or provide the test database for independent sensitivity/equivalence checks. Repair time after an incorrect submission was not observed.

## Reconstructed outcomes

The following values come from Tables II and V. Each version contributes 36 submissions across the three tasks, with linked observations across people.

| Outcome | Original V1 | Structured V2 | Further abstracted V3 |
| --- | ---: | ---: | ---: |
| Task 1 mean minutes | 38.2 | 28.4 | 36.7 |
| Task 2 mean minutes | 26.9 | 29.5 | 21.5 |
| Task 3 mean minutes | 45.4 | 47.4 | 33.2 |
| Sum of three cell means | 110.5 | 105.3 | 91.4 |
| Serious primary errors | 6 | 9 | 15 |
| Serious ripple errors | 7 | 2 | 0 |
| Errors classified as minor | 14 | 15 | 13 |
| No errors | 9 | 10 | 8 |

The aggregate time reduction is descriptively 4.71% for V2 versus V1 and 17.29% for V3 versus V1. V2 is fastest for task 1 but slowest for tasks 2 and 3. A broad claim that every restructuring improves every task is therefore false even within these means. The portfolio sums combine cell means from the design; they are not each participant's observed time on all three tasks in one version.

Table IV gives a system main-effect F(2,64)=2.88, marked at the .10 level, and a system×task interaction F(4,64)=2.71, marked at .05. Tail probabilities recomputed from the rounded F values are approximately .0634 and .0377. The sums of squares, degrees of freedom and mean-square arithmetic agree to rounding after checking the image. This is aggregate verification, not participant-level reanalysis, assumption testing or new significance claims. The paper's means should not be advertised as a main effect established at .05.

Serious primary errors mean the requested change fails. Serious ripple errors mean the requested change works but breaks an unmodified part of the system. These categories are mutually exclusive in the scoring, so fewer classified ripple errors alone do not establish better all-obligation success. V3 has more serious errors overall (15/36) than V1 (13/36) or V2 (11/36), and fewer completely error-free submissions (8/36 versus 9/36 and 10/36). These are descriptive counts; no independent-binomial significance test is justified by treating the repeated observations as unrelated.

The term **minor** is also consequential. Appendix A explains that twelve task-1 submissions mishandle logically deleted records and cause system failure. The authors classified this as minor because participants were used to a different file system where physical deletion makes that extra check unnecessary. Only three of all 36 task-1 submissions were completely correct. A plausible explanation for failure is not fulfillment of the application's obligation.

Table III's “without serious errors” timing subset consequently includes minor failures. Its cell denominators, reconstructed from Table V, are V1: 3/11/9, V2: 7/10/8 and V3: 5/11/5. It is a selected subset, not fully correct solutions or an estimate including the cost of repairing failures. D1 must preserve all assigned attempts and score new and retained behavior independently.

## Interpretation, metrics and printed discrepancies

The authors prefer ripple reduction because they expect primary errors to be easier to find in subsequent testing. That is a plausible cost hypothesis, not a measured recovery advantage: this experiment did not observe later diagnosis, repair, hidden-regression discovery or lifetime costs. The discussion's assertion that the final restructuring improves every measure overstates the primary-error and no-error counts.

Two further discussion numbers conflict with the tabulated categories. The claimed 42% ripple reduction from V1 to V2 is not the 7-to-2 serious-ripple reduction in Table V; the later statement that only one V3 change introduced a ripple error also differs from Table V's zero serious ripple errors and thirteen errors under the row labeled minor/ripple. The raw records are needed to reconcile these statements; this reading retains the printed table rather than inventing a correction.

Confidence is often high despite failures. Post-task system rankings are dispersed and appear influenced by the task encountered. These are **post-experience ratings**, not a controlled pre-adoption review intervention. Table VII's ranking permutations produce least-complex totals 14/10/12 and most-complex totals 10/12/14; Table VIII and the prose give 14/11/11 and 10/11/15. The difference does not resolve the substantive ambiguity, and exact subjective-rating reconstruction remains limited.

Six complexity measures rank the same three related programs. Halstead effort, cyclomatic complexity, knots and jumps follow lower portfolio time and serious-ripple frequency; nesting and call-hierarchy measures rank other structural costs and primary failures differently. Agreement on these deliberately restructured variants is not held-out predictive validation, proof that source metrics outperform ordinary review, or evidence that minimizing a selected metric optimizes complete maintenance success. The paper itself calls for longitudinal and live-setting evidence.

## Three criteria and follow-up

**Unique:** source-structure interventions, shared maintenance tasks, objective/subjective comparisons and task-dependent tradeoffs have longstanding direct experimental precedents. A broad invention claim for these ideas fails; the narrower Nu/F#/agent question remains unconfirmed. **Valuable:** the observed conflict between speed, local correctness and regressions makes the all-obligation decision concrete, while prevalence, recovery cost and net value for Nu remain unmeasured. **Scientifically valid:** retain within-person dependence, one-application limits, compound interventions, explicit oracle categories, unmatched feedback conditions and selected-subset caveats. This evidence sharpens controls without validating D1's source equivalence or authorizing experiments.

The paper cites Gibson's 1986 dissertation, *A study of complexity metrics as surrogate measures of software maintainability*. A secondary search record suggests the same COBOL system; a primary dissertation copy and exact participant/data lineage remain unverified. Do not count it as replication. SC10 identifies earlier structured-programming critiques, maintenance-metric studies and Weiser's slicing experiment as conditional primary leads. The [author-institution record for Vessey/Weber](https://research.monash.edu/en/publications/some-factors-affecting-program-repair-maintenance-an-empirical-st/) corroborates `10.1145/358024.358057`; only its metadata and abstract were inspected. The new C08 search expands these foundation and contrary-evidence paths. None of these bodies gains full-reading credit from a citation or abstract.
