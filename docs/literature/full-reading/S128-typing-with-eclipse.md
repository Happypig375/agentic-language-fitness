# S128 — API work with Eclipse, documentation and ordinary names

**Complete publication reading, 2026-10-01 HKT; printed-data reconstruction, no experimental reproduction.** Pujan Petersen, Stefan Hanenberg and Romain Robbes, *An Empirical Comparison of Static and Dynamic Type Systems on API Usage in the Presence of an IDE: Java vs. Groovy with Eclipse*, ICPC 2014, pp. 212–222. DOI [10.1145/2597008.2597152](https://doi.org/10.1145/2597008.2597152).

## Identity and coverage

Zotero parent `MPSKWSQR`, PDF `3NZ6ZHJI`, note `XPTMXAPJ` preceded body reading. The publisher/library file has **eleven pages, 273,068 bytes**, SHA-256 `ae87fea25f4314c3e79d075781b5dbdf99dbea5da560c1292012199cee224e53`. All eleven pages, eight figures, eight tables and 31 references were read. The opening and PDF pp. 3–9 were visually inspected, covering the complete code example, allocation, all plots and every numerical table. Both raw tables were reconstructed across all 23 participants. No IDE/source/test/log packet was acquired, installed or executed.

The B02/B08/B10/B12 question is whether earlier favorable typing results persist with richer tooling and information. This is a new partial replication, unlike S117/S126's shared data. It tests a Java/Eclipse versus Groovy/Eclipse package, not an isolated checker, IDE feature or D1 convention.

## What changed, and what remained bundled

The experiment adds Eclipse with its Groovy plugin, JavaDoc-style class/method documentation and parameter/variable names allowed to reveal types. These three changes occur together. Eclipse was chosen partly because prospective participants were trained with it. The authors explicitly describe weaker type inference/completion in the contemporary Groovy tooling and acknowledge that IDE maturity could account for observed differences. A common IDE name does not establish equal capabilities. These are historical installation claims, not statements about present tooling.

Task 1 reuses the largest S117 class-identification task, and task 2 is newly constructed to be comparable in size. Both involve applying an unfamiliar API, with small solutions and no required loops/conditionals. They were selected because IDE completion was expected to matter. This targets an API-information mechanism; it is not a representative distribution of maintenance, game changes or error repair.

The 23 available bachelor/master students had passed programming lectures. The printed allocation has twelve Java-first and eleven Groovy-first participants; an explicit randomization procedure and detailed experience distribution are not supplied. Each participant completes both tasks in both languages, with sequences:

| Group | Four task/language exposures in order |
| --- | --- |
| Java-first | Java task1 → Groovy task2 → Groovy task1 → Java task2 |
| Groovy-first | Groovy task1 → Java task2 → Java task1 → Groovy task2 |

The changed sequence aims to reduce carryover but does not show that all learning is absent. Task2 already follows another API task in the first round, and the second round repeats tasks. The earlier endpoint is time until a solution passes supplied unit tests; no independent held-out behavioral oracle is established. All 92 task-time cells are present. The paper gives no explicit timeout/attrition accounting or exact Eclipse/plugin version; absence of blank cells does not resolve those reporting gaps.

## Positive timing evidence

Every participant is faster in Java on task1. Twenty-one of 23 are faster on task2; the two exceptions (22/23) encountered that task in Java first. All 23 have lower total Java time. Recomputed descriptives from the displayed measurements are:

| Task | Java mean / median seconds | Groovy mean / median seconds | Author-reported paired 95% interval, Java minus Groovy |
| --- | --- | --- | --- |
| 1 | 1,057.52 / 1,076 | 2,430.91 / 2,164 | −1,768 to −979 seconds |
| 2 | 729.00 / 656 | 1,496.87 / 1,406 | −1,012 to −524 seconds |

The paper reports p<.001 for both paired timing comparisons. Mean differences also favor Java in each task/order subgroup. This is substantial favorable evidence under the richer combined environment, and it challenges an explanation that the old minimal editor or missing documentation was necessary for the prior advantage. It does not estimate the separate contribution of Eclipse, names, documentation, checking or participant familiarity.

Table2's 23 rows contain 207 numerical cells. Fourteen displayed differences and eleven displayed totals differ from arithmetic on their displayed components by **one second only**, consistent with possible independent rounding; unrounded logs were not recovered. Those small discrepancies do not change any direction above. They are recorded without silently replacing the printed values or asserting a known rounding procedure.

## Exploration measurements and source limits

Table4 adds 552 cells: counts of file switches, IDE searches, completion-menu openings and seconds in completion menus, each by task/language with a displayed difference. All count differences are exact. Twelve completion-time differences differ by at most one second. Useful descriptive results survive separately from the paper's inferential correspondence problems:

| Measure | Task1 Java / Groovy means | Task2 Java / Groovy means | What it shows |
| --- | --- | --- | --- |
| File switches | 33.48 / 69.26 | 25.09 / 49.83 | Java has fewer switches for 19/23 and 20/23 participants. |
| IDE searches | 1.00 / 4.87 | 0.26 / 8.78 | Medians are 0/3 in both tasks; positive Groovy-minus-Java ranks are 18 and 17. |
| Completion-menu openings | 18.43 / 23.52 | 19.96 / 21.78 | Count differences are small relative to the claimed task2 interval below. |
| Completion-menu seconds | 90.91 / 150.65 | 66.43 / 111.91 | Paired median Java-minus-Groovy differences are −53 and −4 seconds, not roughly a minute in both tasks. |

The lower search/switch and aggregate completion-time measurements support a scoped exploration association. They do not identify navigation as a causal mediator: longer or harder attempts permit more exploration, and information/checks/tool quality co-vary. The authors explicitly call these analyses exploratory and uncontrolled (§6); measured menu time is far too limited to explain the entire timing gap on its own.

**Completion-count contradiction:** §5.3/Table7 reports no task1 count effect (p=.21) and a task2 effect (p=.002) with a Java-minus-Groovy interval of **−95 to −25 openings**. Under Table4's printed task2 count headings, every paired difference lies between **−15 and +14**, with mean **−1.826**. A paired mean interval as described cannot have the printed center of −60. The count heading/data and inferential summary are therefore unresolved; no guessed exchange with another metric/task is adopted. Table7's caption itself says file switches, while the surrounding subsection analyzes completion counts.

**Time summary and labels:** §5.4 calls both median differences about a minute. Table4 gives separate medians of 69/107 and 63/65 seconds, and paired-difference medians of −53/−4. Neither interpretation supports that blanket statement. Table8 is captioned search times although its subsection concerns completion time. The narrative also says only two Groovy participants did not search on task1, whereas its rows contain three (4/14/23). These discrepancies require source reconciliation; they do not erase the timing outcome or the correctly reconstructed descriptive exploration pattern.

No full ANOVA/Wilcoxon pipeline was rerun. Direct paired means, standard errors and t statistics were calculated for arithmetic checks, not treated as corrected original inference. Nonsignificant group/normality tests do not prove no carryover or exact normality; the paper's claim that separate rounds cannot contain learning is stronger than this sequence warrants. Multiple exploratory comparisons and paper/data correspondence limit the mechanism claim.

## Recovery, implications and next sources

Two focused web queries for this DOI's data/correction returned thirteen distinct search routes; the publisher landing open failed. The [institutional record](https://bia.unibz.it/esploro/outputs/conferenceProceeding/An-empirical-comparison-of-static-and/991006493190301241) lists a Scopus abstract link, while the [author's publication entry](https://se.informatik.uni-due.de/team/stefan-hanenberg/?limit=2) supplies citation/DOI metadata. Neither examined entry provided an original data or correction packet. This bounded unsuccessful recovery does not prove no packet exists. Incidental author-page entries and returned citation fragments were not counted as full-paper screens.

S129's acquired documentation comparison remains the next specific information control. The existing C02/citation queue preserves contrary dynamic-task design, optional typing, generic/cast burden and modern tool-support comparisons. API documentation/learning and code-completion practice in the bibliography remain conditional primary routes if prevalence or mechanism claims depend on them. The returned Ampersand schema-migration/prototyping leads may inform B02/B04, but only citation fragments were inspected here; their editions and methods are not credited.

**Unique:** unresolved; favorable API timings have a partial replication with richer tools and information. **Valuable:** the selected human timing benefit is large and concrete; a general paradigm, Nu or agent gain is unmeasured. **Scientifically valid:** primary timing directions and exploratory descriptives are reconstructed; separate treatment contributions, completion-count correspondence and causal navigation remain unresolved. No ISE feasibility, behavioral oracle or experimental start is validated.
