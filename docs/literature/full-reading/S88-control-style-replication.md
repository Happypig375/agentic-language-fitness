# S88 — A coffee-machine replication with different outcomes and incomplete denominators

**Complete publication reading, 2026-09-30.** Ignatios Deligiannis, Panagiotis Sfetsos, Ioannis Stamelos, Lefteris Angelis, Alexandros Xatzigeorgiou and Panagiotis Katsaros, *Assessing the Modifiability of two Object-Oriented Design Alternatives – A Controlled Experiment Replication*, EUROSIM 2004. The [author-institution publication list](https://people.iee.ihu.gr/~sfetsos/Publications1.html) corroborates the venue/year; the six-page [author-institution PDF](https://sites.uom.gr/achat/public_html/papers/EUROSIM2004.pdf) supplies complete authorship. No DOI was found or guessed. Zotero parent `DZPNJK5D`, PDF `E3WL3NLD`, note `GHV7CVKQ`.

All six pages, five figures, the learning-curve equation and fifteen references were read in text and rendered images. The PDF has 125,216 bytes, SHA-256 `9cd41ca51a1eb8b4c947cb9152e9b2a2f369601fd2f2a09daf8a4da823115662`. Source code, task specifications, raw measurements, scoring rubric and questionnaire were not acquired; no experiment or statistical model was reproduced. Bibliographic spelling variants of Xatzigeorgiou/Chatzigeorgiou do not create another study.

## Why this changes the background

B01/B10/B11/B12 require contrary evidence to a universal recommendation of centralized control for less experienced maintainers. The abstract favors responsibility-driven (RD) correctness among undergraduates. Full reading retains this result with its threshold, scoring and missingness limits; it neither discards the adverse-to-S81 direction nor treats the two studies as commensurate estimates.

Reference [3] explicitly identifies the **2001 Arisholm/Sjøberg/Jørgensen experiment**, `10.1023/A:1011439416657`, as the replication target. That original used Mocca and pen-and-paper changes. S88 changes to Java, compiling/running each task, and an enlarged source-metric set. It does **not** replicate [S81's 2004 professional/student protocol](S81-control-style-experience.md) directly. Both studies reuse the coffee-machine design family, so separate participants do not create an independent application family.

## Assignment, tasks and outcomes

Forty-three second-semester undergraduate students in a Java OO course were randomly assigned to MF (centralized/mainframe, 22) or RD (21). Recruitment deliberately sought capable, motivated volunteers, with a grade bonus. An instructor was available for compiler-related difficulty; the amount and allocation of help are unspecified. There was no fixed completion deadline, although students were asked to work quickly and accurately. These conditions differ from S81's categories, tools, compensation and eight-hour cap.

The MF and RD programs are described as functionally equivalent with common programming style, names and documentation. They have **11 versus 16 classes and 286 versus 391 lines**, respectively, differing from S81's seven/twelve-class versions. Equivalence and source correspondence could not be independently checked. The authors classify the versions as bad/good according to design guidelines; that label is not an observed maintenance outcome.

Each participant performs three ordered changes in one assigned design. Task 1 adds a small method/call change in two classes. Task 2 extends functionality using inheritance/reuse, reported as easier in RD. Task 3 adds a pre-production check, reported as harder in RD because it spans a five-class message path. Full instructions and per-task numerical results are absent. Although the paper labels the design within-subjects, each person receives only one source variant: source design is between groups, with repeated tasks within a participant. It is not a paired within-person comparison of both architectures.

Effort is self-reported minutes for completed tasks. Correctness is described as whether the completed task works, but Figure 3 displays a score with observed values roughly 5–9 rather than a binary complete-chain outcome; the scoring rubric and aggregation are not specified. Do not convert that graph into numbers of entirely correct participants or compare it numerically with S81's 54/78 versus 40/80 success rates.

Figures 1, 2 and 4 label **17 people per design**, while Figure 3 retains **22 MF and 21 RD**. Thus nine of the assigned participants are missing from the reported effort, learning and subjective plots. The reason is not given. These omissions are not established to be random, unsuccessful submissions or simple timing failures; the full-assignment effort effect remains unavailable.

## Reported results and checks against the figures

The authors set **α = .10**, not .05. Figures were inspected directly; precise observations cannot be recovered from the boxplots.

| Outcome | Published analysis | Reading consequence |
| --- | --- | --- |
| Total effort | t test p = .69, 17/17 plotted | No detected total difference; no equivalence test. Per-task reversals are described without their numerical tests. |
| Learning curve | t test p = .863, 17/17 plotted | No detected difference on the paper's first-versus-third-task measure. |
| Correctness score | RD favored, t test p = .09, 22/21 plotted | Meets the declared .10 threshold, not .05; unclear score/rubric prevents complete-success reconstruction. |
| Subjective change complexity | Prose calls a task-3 difference significant; printed p = .669, 17/17 plotted | The reported p-value does not meet .10. A claim of established significance is unsupported as printed. |
| Structural stability | Wilcoxon p = .069; t test p = .114 | Only the Wilcoxon result meets .10. Test units, dependence and metric scaling are not adequately described. |

The learning measure is `(understanding time on c1 − time on c3) / (time on c1 + time on c3)`. The tasks differ substantially, including the five-class check, so this change is not an isolated learning effect with matched task difficulty. Mostly negative plotted scores mean c3 generally takes longer to understand, not that measured learning necessarily deteriorates.

Structural stability compares changes in eight Together-tool metrics: CBO, RFC, two weighted-method measures, LOC, method-invocation coupling, attribute count and operation count. Figure 5 mixes quantities of different units and displays no participant uncertainty. Some RD changes are smaller and others similar or larger; an overall interpretation needs the unavailable aggregation and test specification. The paper does not show that a post-change metric causes performance or provides a validated decision-time selector.

The subjective-complexity and stability paragraphs both refer to H1 while discussing H4/H5. These printed labeling/p-value problems remain documented rather than silently repaired. The authors' mechanisms—reuse aiding extension and distributed responsibilities hindering a cross-class check—are plausible explanations consistent with task descriptions, not separately randomized mediators.

## Three criteria and remaining leads

**Unique:** replication, guideline comparisons and within-language task-dependent architecture effects are established research activities. There is no general firstness claim left for those ideas; a particular Nu/F#/agent result remains unresolved. **Valuable:** a design can help an extension while complicating a coordinated check, and the direction among students differs from S81's headline. Adoption advice needs task/feedback/experience context and measured complete obligations. This paper supplies no Nu effect or net-cost estimate. **Scientifically valid:** preserve all assigned denominators, scoring definitions, threshold choices, task dependence, intervention differences and nonrandom recruitment. Do not pool the coffee studies' incompatible correctness endpoints, infer an expertise threshold, or claim that missing observations favor either architecture.

The earlier 2001 primary experiment remains a consequential lineage/methods target. SC13 already retrieved its DOI; the author-hosted 2001 thesis surfaced through W08 but its experiment chapter has not been read. SC15 requests the review in reference [1] and the maintenance paper in reference [9], with `limit:20`, offset 0. It returns three records: the two requested identities (`10.1023/A:1016392131540`, `10.1109/52.207232`) and a different contextual-help chapter. Metadata only were available; the review could broaden empirical-family coverage, while the maintenance paper could ground the distributed-plan mechanism. Full bodies, author/edition checks and dataset relationships remain pending. The chapter is outside this comparison, not a substitute for either requested source. No broader theme or search family is considered exhausted.
