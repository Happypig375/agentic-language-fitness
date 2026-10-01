# S95 — inheritance depth, navigation and reuse during maintenance

Read 2026-10-01 by the main Codex session. Lutz Prechelt, Barbara Unger, Michael Philippsen and Walter F. Tichy, *A controlled experiment on inheritance depth as a cost factor for code maintenance*, [JSS DOI](https://doi.org/10.1016/S0164-1212(02)00053-5), 65(2), 115–126, 2003. Governing file: the [author copy](https://page.mi.fu-berlin.de/prechelt/Biblio/inherit_jss2003.pdf), whose cover says **submission, November 1, 2001**. The author's bibliography explicitly warns that these journal copies can differ in content as well as layout. Correspondence with the final twelve-page journal article is unverified.

Existing native parent **`H7VL7P4E`**, PDF **`QCT4CZNF`**, note **`UUZPIFT3`**; parent/title/DOI and stored file hash reverified before continued reading. PDF **18 pages, 103,195 bytes**, SHA-256 **`506cc928e592329d5186610e934365257438de26b5f38b998733f653ebc017d5`**. Every page text-read and rendered; PDF pages **4, 5, 7, 10, 11, 13, 14 and 16** visually checked, covering all four figures, three tables and garbled mathematical/statistical notation. Both numbered footnotes, author note and sixteen references included. No appendix in this file.

Necessary supplementary work is in the [S189/report and released-data check](S95-S189-inheritance-material-check.md): selected 51 of 177 report pages and bounded package reconstruction, not a full report reading or experimental reproduction. The 1998 report, 2001 submission and 2003 publication share the same two experiments. Neither edition nor a factor-table row is an independent empirical study.

## Decision and mechanism

The concrete decision is whether a deeper inheritance design helps a particular code-change task. Inheritance can reduce repeated edits and allow reuse, while distributing the behavior a maintainer must understand across classes. That mechanism is task dependent; maximum depth or total source size alone need not identify it. The study challenges earlier favorable depth-three findings, preserves a useful depth-five reuse result, and explores alternative explanatory measures.

This is human Java maintenance on one interactive GUI program, not OO versus functional programming, polymorphic-dispatch performance, F# case enumeration, Nu architecture or agent context cost. S93 supplies a broader decomposition rationale; S95 tests a specific representation/task bundle.

## Assignment, programs and tasks — pp. 3–9

Two June 1997 experiments use functionally equivalent versions of **Boerse**, a stock-data display program. The deepest version is the starting design. The depth-three version moves inherited concrete-class code into subclasses, allowing inheritance only from abstract classes; the flat version removes the remaining inheritance and duplicates needed functionality. Unused inherited functionality is omitted. Functional equivalence is an author premise, not independently executed here. No multiple inheritance or essential polymorphic use is tested.

| Version, graduate program | Classes | Methods | LOC | Material distinction |
| --- | ---: | ---: | ---: | --- |
| Depth 0 | 20 | 158 | 2,470 | More duplicated code, local implementations |
| Depth 3 | 27 | 100 | 1,344 | Inheritance from abstract classes |
| Depth 5 | 28 | 80 | 1,200 | Reuse through deeper concrete/abstract hierarchy |

The undergraduate event-handling variant has 2,465/1,317/1,187 LOC and 160/96/79 methods. It replaces older AWT event handling with the JDK 1.1 mechanism. Within each experiment, depth therefore changes locality, duplication and class/method counts together. It is not a depth intervention with those consequences held constant. Subjects receive a single source file, printed listing, inheritance diagram and input files.

There are **57 graduate-course participants** and **58 first-year undergraduates**. The graduate course selects eligible participants through prior exercises; the undergraduate exercise is voluntary with an exam-grade bonus. Block randomization uses exercise performance for graduates and self-reported largest-program size for undergraduates, assigning each ordered triplet across the three versions. The report resolves actual group sizes: **19/18/20** and **20/17/21** at depths 0/3/5. Two undergraduate sessions are pooled. The short Java pretest finds no significant group differences; this does not establish identical ability. Self-reported experience and course preparation do not create a professional-developer arm.

Graduates perform **Task 1, Y2K**, then a combined **Task 2a + 2b**. Undergraduates perform 2a and 2b as separately timed successive tasks. Task 1 changes two-digit dates and dependent substring offsets to four-digit dates: sixteen relevant method changes in depth 0/3 versus eight in depth 5. Repeated edits can be found by search without reconstructing the whole hierarchy. Task 2a adds an arbitrary-interval price table and menu item, borrowing table-display and chart-input behavior. Task 2b adds an interval gain/loss table and can reuse the preceding work.

The authors' assumed straightforward strategy needs **13/16/17 methods understood** for 2a, **0/17/21 hierarchy transitions**, and **17/9/5 cloned or changed methods**. For 2b, the assumed additional understanding is two methods for each design; the solution contains 17/10/5 cloned or changed methods. Depth five can clone the previous class, rename it and change its superclass, with menu integration. These are analytical task counts, not observed individual navigation traces or assigned mediator levels. Real subjects sometimes choose other valid organizations.

## Outcomes and stopping

Subjects decide when to submit or give up and test at their discretion. Handout timestamps, checked at collection and backed by intercepted compiler/run activity, measure task time. The detailed instructions allow changing existing classes or introducing new ones. Structural departures are descriptive choices, not automatically semantic failures. No full release, configuration, regression-testing or diagram-update workflow is required.

Black-box checks and error penalties give graded correctness scores. A percentage of available points is **not the percentage of fully correct solutions**, and the selected checks do not establish a complete temporal oracle. In particular, the detailed report does not deduct certain follow-on errors again when they were inherited from Task 2a. Earlier Daly experiments instead returned work until it was correct, changing the stopping/feedback conditions and therefore the interpretation of elapsed time across studies.

Pairwise bootstrap comparisons are one-sided, using the paper's **p < .1** threshold; no multiplicity adjustment is described. The report uses 10,000 resamples and gives 90% relative-difference intervals. These are the authors' inference choices, not a presumption that .1 equals the conventional .05 threshold. Non-normal raw observations alone do not justify every statistical claim in the report.

## Measured effects — pp. 9–12, report Tables 3.2/3.5

Means below are recomputed from the released task rows; p values are reported values, not independently reproduced bootstrap tests.

| Cohort / task | Depth 0 / 3 / 5 mean minutes | Finding and limit |
| --- | --- | --- |
| Graduates, Y2K | **71.16 / 88.17 / 69.45** | Depth 3 slower than 0 (p=.075) and 5 (.023). Depth 0 versus 5 is nonsignificant; submission says .200, report's untrimmed row says .447. Nonmonotonic time outcome. |
| Graduates, combined 2a+2b | **115.74 / 132.28 / 134.85** | Flat version faster than 3 (.038) and 5 (.005), despite more duplicated/changed code. Depth 3 versus 5: .393. |
| Undergraduates, 2a | **152.35 / 154.06 / 180.86** | Depth 5 slower than 0 (.038) and 3 (.055); 0 versus 3: .456. The .055 comparison meets only the authors' .1 threshold. |
| Undergraduates, observed 2b | **27.00 / 30.93 / 19.13** | Depth 5 faster than 0 (.006) and 3 (.004); 0 versus 3: .263. Only 17/14/16 of 20/17/21 assigned participants have a recorded 2b time. |

Y2K mean grades are 100/90/80% after rounding; the report's distinct fully-correct proportions are **19/19, 15/18 and 14/20**. The report's Fisher comparison of depth 0 versus 5 is .020. Combined-task mean grades are roughly 79/75/80%; no significant grade differences are reported. The report's flat-group combined-task correctness percentage disagrees with its plotted and released count, as documented in the material check. Undergraduate score comparisons are nonsignificant; neither this nor the timing nulls establishes equivalence.

The follow-on reuse benefit is relevant positive evidence and must not disappear because the authors describe its task as unusual. It comes with learning and differential missingness: the released records lack times/scores for **3/20, 3/17 and 5/21** undergraduates, and those missing participants were slower on 2a on average. The report's stated dropout percentages and marked rows differ from these released records. No adjustment here converts selected completers into an unbiased total treatment effect. Trimming slow observations or excluding defective solutions, as the paper explores, also selects on outcomes and cannot repair that problem.

Subjective judgments distinguish another outcome: flat-program participants often think the program uses too little inheritance while more of them believe their solutions correct. Graduate respondents prefer the deepest structure's clarity; undergraduates prefer the shallower designs. Deeper groups report lower concentration in the later task. These observations neither invalidate every judgment nor establish maintenance benefit from perceived elegance.

## Exploratory explanation models — pp. 12–17

The final submission fits **sixteen group means**: six from the new experiments, eight from Daly's experiments and two from Cartwright's replication. They span programs, cohorts, languages and feedback/stopping conditions. Programs and tasks recur across groups; the rows are not sixteen independently randomized mechanism experiments. Graduate means combine 2a+2b, whereas undergraduate means concern 2a. The older released factor table confirms the combined graduate unit and assigns it two additional relevant methods; it has only fourteen rows and cannot reproduce the later sixteen-row models unchanged.

Candidate inputs include program size/depth, assumed task-relevant methods and hierarchy transitions, solution edits and a coarse binary experience label. Models are selected after examining the data and fitted by least squares, mostly linearly. **m** is the default strategy's relevant-method count, **h** the hierarchy-transition count and **d** depth. Representative fits are `t = 6.9m + 28` (R²=.84), `t = 4.5h + 61` (.55), and `t = 7.8d + 70` (.10). Separate low/high-experience slopes give `t = 8.9m_low + 5.9m_high + 24` (.94). Adding depth gives a small negative conditional coefficient, not a causal proof that greater depth helps. Table 3 lists eight fitted variants, two to four coefficients, with R² up to .96.

Figures 3/4 show fit to the same group means, including a 90% mean-response band; they are not held-out predictive validation. High fitted R² does not show that individual observed navigation caused effort, or that a maintainer can know m prospectively. The authors explicitly limit the model to understanding-dominated tasks and call it explanatory: m often becomes known only after the understanding work. Proposed use in choosing designs for anticipated tasks remains a plausible application, not a validated selector.

## Disposition and consequential continuation

**Established mechanism:** task-relevant behavior can be local or distributed; reuse can reduce repeated changes. **Measured effect:** within the tested Java tasks, flat organization helps several understanding-heavy changes, while deep reuse helps a related follow-on task among observed participants. Grade, binary correctness, time, missingness and subjective assessment differ. **Unresolved inference:** general optimal depth, source compactness as a causal benefit, lifetime reuse payoff, modern tool support and Nu/agent transfer remain unmeasured.

Daly's favorable predecessor, Cartwright's opposite-direction replication and the later task-dependent study remain primary-method continuations, not votes counted from S95's related-work prose. Their titles/abstracts and returned snippets do not complete those readings. S189 resolves important task/denominator details but leaves report/data discrepancies and the later model's full input table unresolved. These limits qualify the findings without erasing them.

New native attachments now reopen previously blocked game, type-law, modularity and oracle methods. Continue the newly available **S163 game-testing coverage survey** to strengthen B05/B07 alternatives and observation criteria, then prioritize S140/S90/S184 and the existing S185/type/oracle paths by the claim they can change. No theme is closed and no construction, candidate run, new worker or experiment is authorized.
