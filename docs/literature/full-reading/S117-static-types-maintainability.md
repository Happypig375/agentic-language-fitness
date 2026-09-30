# S117 — Static typing and maintenance: task-specific benefits, order effects and publication lineage

**Complete conference-publication reading, 2026-09-30; printed-data reconstruction, no experimental reproduction.** Sebastian Kleinschmager, Stefan Hanenberg, Romain Robbes, Éric Tanter and Andreas Stefik, *Do Static Type Systems Improve the Maintainability of Software Systems? An Empirical Study*, ICPC 2012, DOI [10.1109/ICPC.2012.6240483](https://doi.org/10.1109/ICPC.2012.6240483).

## Identity, coverage and live question

Zotero parent `SKF3GVU4`, PDF `CULNIS7E`, note `7L5MQ839`. The record preceded intentional reading. The [author PDF](https://pleiad.dcc.uchile.cl/papers/2012/kleinschmagerAl-icpc2012.pdf) is **10 pages, 228,496 bytes**, SHA-256 `ccf92eba924cdfbed6463903226c0d0c1847cd0b47db18ac292b2bcee69aa460`. All ten pages, five figures, seven tables, examples and 23 references were read. Visual inspection covered PDF pages 1/3/4/5/6/7/9/10, including every figure/table. Printed pages are **157–166**, whereas catalog/author-list pages are 153–162; publisher-edition equivalence remains unchecked.

This is B02/B10/B12 evidence about human maintenance outcomes and their possible mechanisms. It tests Java with explicit types/checking against a restricted dynamically typed Groovy variant. It does not test explicit current F# cases against an initially equivalent catch-all, coding agents, or successive domain changes.

The [author publication list](https://pleiad.cl/research/publications) explicitly identifies this conference paper as superseded by *An empirical study on the impact of static typing on software maintainability*, DOI `10.1007/s10664-013-9289-1`, ESE 19(5), 1335–1382, 2014; online 11 December 2013. That article is now S126, with a record and both author/publisher PDFs. The subsequent [complete S126 reading](S126-static-types-maintainability-journal.md), on 1 October, confirms that all 33 timing rows are identical and reconstructs the added exploratory measurements. Preserve the conference reconstruction as historical evidence, **not a second independent empirical case** or an adequate substitute for the journal's analysis.

## Assignment, tasks and observation

Thirty-six volunteers began; 33 completed both rounds and appear in the raw table. The recruitment description lists thirty students, three researchers and three industry participants, summing to the initial 36; it does not identify the retained composition or reasons for the three incomplete participants. The analysis therefore concerns completers, not an established all-assigned-attempt result.

Language order was randomized: the printed data contain **17 Groovy-first and 16 Java-first** completers. Two practitioners were Java-first and all three researchers Groovy-first. Each participant performed the same nine task forms in each language, with an unscored warm-up. Language order changes, but within-language task order does not. Small nonstudent groups, learning and repeated task structure remain consequential.

The game-derived base application has thirty classes, 152 methods and roughly 1,300 lines. It was translated to Groovy with type information removed; the Java task variant was renamed into an email domain with corresponding structures. Type declarations/checks and domain identifiers therefore differ. Field/parameter names were deliberately changed to synonyms so that names would not directly reveal types. Participants had Java familiarity. Groovy was used as a dynamically typed Java-like language, without exploiting its larger idiomatic feature set. This narrows syntactic differences but does not independently randomize type documentation, checking, annotation effort, domain cues or familiarity.

The custom Emperior environment supplies a simple editor, highlighting, a file tree and compile/test execution. It intentionally omits mature IDE assistance. Participants can run provided tests, but cannot inspect their bodies. Task time ends when those tests pass. Fresh files/environment are supplied for each task; subsequent tasks are unavailable. This provides a common feedback endpoint, **not an independent final behavioral oracle or proof of complete correctness**. Repair failures, alternative correct behavior and later regressions are not separately measured.

Five class-identification tasks (CIT1–5) require constructing object relationships using respectively two, four, six, eight and twelve classes. Two type-error fixing tasks (TEFT1–2) repair a wrong object where a string is expected and swapped constructor parameters, with runtime failures displaced from their causes in Groovy. Java initially exposes compiler errors. Two semantic-error tasks (SEFT1–2) repair the wrong mail/cursor job and a missing removal after moving an object, which leaves a duplicate reference. They are small, deliberately loop/recursion-free operations. The actual order is CIT1, CIT2, CIT3, SEFT1, SEFT2, CIT4, TEFT1, CIT5, TEFT2; increasing CIT size is not an independently randomized dose.

## Positive, mixed and order-dependent results

The following descriptives were reconstructed from all 33 rows of printed Table VII (PDF p. 10). All eighteen task times per row and both totals were parsed; **all 66 row totals equal their nine constituent times**. Means, medians and sample standard deviations reproduce rounded Table III. This checks publication arithmetic, not experimental execution, raw interaction logs or the inferential analysis.

| Task | Mean Java / Groovy seconds | Median Java / Groovy seconds | Completers faster in Java |
| --- | --- | --- | --- |
| CIT1 | 535.18 / 817.58 | 480 / 575 | 24/33 |
| CIT2 | 780.91 / 669.42 | 567 / 562 | 21/33 |
| CIT3 | 812.61 / 1,182.42 | 711 / 1,010 | 26/33 |
| CIT4 | 827.15 / 1,026.18 | 716 / 880 | 23/33 |
| CIT5 | 690.52 / 1,112.18 | 671 / 1,046 | 31/33 |
| TEFT1 | 235.85 / 928.06 | 197 / 813 | 32/33 |
| TEFT2 | 146.91 / 849.24 | 116 / 750 | 32/33 |
| SEFT1 | 1,111.48 / 813.52 | 1,015 / 639 | 15/33 |
| SEFT2 | 507.45 / 428.70 | 293 / 282 | 15/33 |
| All nine tasks | 5,648.06 / 7,827.30 | 4,892 / 7,349 | 28/33 |

The paper's PDF p. 5 statement that nobody was slower overall in Java conflicts with its printed raw data. Subjects **21, 23, 26, 27 and 33** have Java/Groovy totals of 9,300/5,804; 10,695/7,908; 6,177/4,072; 8,631/7,349; and 8,142/7,281 seconds respectively. All five are Java-first. The lower Java aggregate mean is retained; the universal participant claim is not.

The strongest positive pattern is the two type-error repairs, favoring Java in both orders. Groovy-first means are Java/Groovy 172.53/757.88 and 126.82/788.00 seconds; Java-first means are 303.12/1,108.88 and 168.25/914.31. CIT5 also favors Java in both order groups. These are useful effects under the supplied tasks and diagnostic asymmetry, not evidence that every apparent benefit is an artifact.

Semantic repairs strongly reverse with order. For Groovy-first participants, Java/Groovy SEFT1 means are 638.82/1,022.35 seconds and SEFT2 means 237.35/538.59. For Java-first participants, they are 1,613.69/591.62 and 794.44/311.94. In each group the second language is faster. CIT2 also gives mixed summaries: more participants are faster in Java while its mean is higher. Aggregate language means alone conceal skew and sequence effects.

## What the statistical analysis establishes and leaves open

The authors analyze each round with task as a within-subject factor and language as a between-subject factor, using Greenhouse–Geisser correction for sphericity. Task and task-by-language interactions are significant in both rounds; the language effect is not significant in round one (`p > .76`) and is significant in round two (`p < .001`). Reported partial eta-squared values for task are .275/.246 and interactions .181/.172. The interaction supports task dependence, not one universal maintenance effect.

Table IV also compares each task within each order group using Wilcoxon tests. All nine favor Java in the Groovy-first group. In the Java-first group, CIT5 and both TEFT tasks favor Java; CIT2 and both semantic tasks favor Groovy; CIT1/3/4 do not reject the null. Displayed `.000` values are rounding, not zero probabilities. The paper combines these significance patterns into a favorable interpretation for four of five CIT tasks and both TEFT tasks, with no claimed semantic advantage.

Different significance outcomes across groups are not themselves a pooled treatment estimate or a formal test of equality between effects. No explicit multiplicity adjustment or equivalence margin is supplied for this taskwise decision rule. A learning effect could hide another effect, but that does not establish that the hidden effect is small. The semantic results therefore provide mixed/order-dependent evidence, **not equivalence or proof of no typing benefit**. Class count, task identity, domain and sequence are linked; there is no established monotone class-count benefit.

## Implications and consequential follow-up

For the broader survey, the defensible positive result is faster repairs on two selected type-error tasks and favorable results on several class-identification tasks. Static declarations can supply navigational/documentary information while compiler errors locate invalid operations; these mechanisms are bundled here. Deliberately weakened names/documentation and a basic editor make ordinary source cues and IDE assistance substantive rival explanations for transfer. A game-domain fixture is not itself evidence about ongoing game evolution or temporal correctness.

For D1, retain common source/tool opportunity, separate diagnostic sites from behavioral obligations, and preserve task/attempt dependence. Both proposed baselines can already be compiler-exhaustive. This paper cannot justify choosing only future changes that make an explicit match useful, excluding adverse cases, or treating a warning count as the outcome. No empirical effect transfers automatically from humans changing Java/Groovy to a fixed F# coding agent.

The completed bibliography and incoming Scite traversal exposed necessary next readings, recorded in the [background ledger](../nu-background-searches-2026-09-30.md): S126's superseding journal analysis; S127 `10.1145/2577080.2577098` on type names without checking; S128 `10.1145/2597008.2597152` with Eclipse; and S129 `10.1145/2568225.2568299` on documentation and typing. Records precede their intended full readings. All four now have PDFs; S126 has since been fully read, while S127–S129 retain opening-only coverage. S127's newly attached library PDF closes the initial publisher-access gap. The dynamically favorable task-design study `10.1109/ICPC.2016.7503719`, annotation burden, optional/gradual typing and later type-information use remain explicit contrary/transfer routes, not completed methods. The 2011 Kleinschmager thesis in reference 12 remains unacquired.

**Unique:** unresolved; this is direct human maintenance evidence with a different treatment, and its revision/close follow-ups require account. **Valuable:** concrete task-specific benefits coexist with adverse/order-sensitive results; prevalence, net cost and Nu/agent transfer remain unmeasured. **Scientifically valid:** the conference procedure, raw-table arithmetic and limits are reconstructed; the subsequent S126 reading resolves shared timing-data lineage while attrition and generalization remain open. No author experiment was rerun, and no ISE feasibility or experimental work is authorized by this reading.
