# S94 — change effort, incomplete tasks and structural stability

**Complete journal and appendix reading, 2026-10-01 HKT.** Erik Arisholm, Dag I. K. Sjøberg and Magne Jørgensen, *Assessing the Changeability of two Object-Oriented Design Alternatives—a Controlled Experiment*, Empirical Software Engineering 6 (2001), 231–277, [DOI 10.1023/A:1011439416657](https://doi.org/10.1023/A:1011439416657). This is the Mocca/paper predecessor of the coffee-machine studies reconstructed in [S81](S81-control-style-experience.md) and [S88](S88-control-style-replication.md).

## Identity, coverage and reconstruction

Existing Zotero parent `LBU2LYQD`, user-library PDF `YQYEDXHR`, note `PYWNYI4F`. Native identity, attachment relationship and hash were reverified before continuing. The journal has 47 PDF pages, 652,062 bytes and SHA-256 `c7098420a5e33c8aacad9d01c5c83ccc60d522481801e0638ec7ea88c3e54fc9`. All pages, nine figures, eighteen tables, six appendices A–F, four endnotes, nineteen references and author information were read.

Poppler recovers the main text more faithfully than the previously corrupted PyMuPDF extraction, but still loses some signs/ligatures. Visual checks cover PDF pp. **6, 11–20, 22, 27–28, 30, 34–44**: 26 distinct pages, including every figure/table, the questionnaires and image-only code fragments. Rotated Appendix D/F pages and enlarged Table 5 establish their actual orientation, values and negative learning scores. A renderer color-profile warning did not prevent the inspected pages from rendering. Extraction alone is not the coverage claim.

Appendix F supplies **36 participant rows** for summary effort, calibration and each of three changes. Local scripts parse those printed rows, preserve missing `*` values, check row counts and calculate descriptive means, counts and score-based eligibility. These are limited arithmetic checks of the published tables, with the relevant pages visually verified. They are not a rerun of the authors' original programs, scoring, hypothesis tests, random allocation or experiment. Raw PDF/text/data copies remain outside Git.

## Assigned source and task opportunity

Both versions implement the same small coffee-machine requirements according to the authors. The mainframe/control-oriented (MF) version has seven classes; the responsibility-driven (RD) version has twelve. MF concentrates drink selection, prices and dispensing in `FrontPanel`; RD distributes work through products, recipes and ingredient/dispenser registries. Both use similar naming, comments and style, with sequence diagrams supplied. No independent whole-program behavior equivalence was established by this reading; Appendix E contains fragments, not both complete source trees.

RD was adapted from a design already restructured after changes such as bouillon. The researchers removed that functionality to make it a later task, and deliberately left the initial drink price in `FrontPanel`. This historical preparation and the actual modified baseline matter when interpreting a generic design label. The assignment varies a package of source properties, not coupling alone.

Table 1's mean non-library outgoing coupling is 4.7 MF versus 2.8 RD, but system totals are **33 versus 34**. Library invocations total 8 versus 16, methods 11 versus 22, and SLOC 77 versus 107. Lower per-class coupling and smaller classes do not establish lower whole-system interaction or less work. The RD version follows the selected guidelines more closely, but “good” and “bad” are treatment descriptions, not empirical outcome labels.

Mocca is a Java-like restricted language with no inheritance, interfaces or explicit casts, three elementary types, and only String/Vector library classes. An ATM logging calibration task trains participants and measures a common skill proxy. Coffee changes are then done **with pen and paper** in one fixed sequence:

1. Add a return-money menu option, using an existing `CashBox` operation.
2. Add bouillon, with a dispenser and a different price.
3. Check all required ingredients before dispensing; preserve the opportunity to choose another drink or recover money.

An extra customizable-drink task keeps early finishers occupied but is excluded from analysis because few complete it. Each task includes an example trace for manual checking; the paper explicitly acknowledges that this is not execution of a real test. Later tasks should not be inspected until the preceding questionnaire is completed. Appendix B provides concrete prices and traces, while C records phase effort, confidence, perceived difficulty and self-described strategy.

## Pilot and main experiment are separate

The pilot recruited twelve graduate students/professionals from a course. It used three one-hour sessions and calibration-score blocking followed by random assignment within blocks. Only **eight of twelve** attended the final session, upsetting the intended balance. Most did not complete c3; the pilot's approximately 30% extra RD effort concerns c1+c2. The pilot informed materials and directional hypotheses for the main experiment. It is not twelve complete observations or an independent application family.

The main study used a separate, mostly undergraduate volunteer sample, paid to participate. In one three-hour session, roughly one hour covered procedures/training and two hours covered calibration plus changes. Random assignment, including arriving unregistered volunteers, yielded **17 MF and 19 RD** participants; no calibration blocking was possible within that session. Each person receives only one design, so the design comparison is between people and the three changes are repeated, ordered observations within a person.

Mean calibration effort is reported as 46.24 versus 50.37 minutes. Its nonsignificant difference is not proof of identical skill. The later balance check repeatedly drops observations to produce fourteen per design, with seven in each calibration-time stratum. Six random subsets from 95,040 possible selections retain the effort direction. These overlapping subsets are sensitivity checks on the same people, not six replications or a replacement randomized study.

## Effort: a supported scoped difference, with incomplete outcomes

The paper uses one-sided unequal-variance t tests for directional effort/learning hypotheses and median tests for ordinal outcomes. It specifies familywise **α = .10**, with Holm thresholds across fifteen tests; structural stability is assessed descriptively. Preserve that declared threshold rather than silently interpreting every headline as familywise .05 evidence.

| Reported measure | MF n / mean minutes | RD n / mean minutes | Published p / Holm threshold |
| --- | --- | --- | --- |
| c1+c2 total | 17 / 26.88 | 19 / 38.30 | .0004 / .0067 |
| c1+c2+c3 total | 16 / 49.20 | 18 / 59.22 | .0072 / .0083 |
| Understanding, all three | 16 / 16.03 | 17 / 26.06 | .0006 / .0071 |
| Coding, all three | 16 / 27.13 | 15 / 27.77 | .42 / .0143 |
| Manual checking, all three | 16 / 6.09 | 14 / 6.36 | .43 / .0200 |

The published totals imply approximately 42.5% extra RD effort for c1+c2 and 20.4% for all three, using MF as denominator. Appendix arithmetic recovers the direction, denominators and rounded main summaries: c1+c2 means 26.8824/38.2632; all-three means 49.1875/59.2222. The strongest phase difference concerns understanding how to make the change; coding/checking differences are not supported under the reported procedure. None of these nulls establish equivalence.

All participants finish the first two tasks, but only **16/17 MF and 8/19 RD** report fully finishing c3. Table 4 nevertheless includes all-three effort for 18 RD participants, including nearly finished work with checking still outstanding. Total-time coverage is therefore not completion or success. One missing total per design and different component denominators also prevent summing phase means as if they described the same participants. This is evidence of higher observed RD work under the time limit, not a clean estimate of time to successful completion for every assignment.

## Correctness, learning and the selected structural result

The first author grades paper solutions on a six-point scale, ranging from very incomplete to correct against the example. Grade 5 allows small output deviations without logical errors; grade 4 allows small logical errors deemed easy to fix. No independent or blinded grading, inter-rater reliability or broad behavioral fault-sensitivity check is reported.

Correctness has **17/19 graded MF/RD observations on c1, 16/19 on c2 and 16/9 on c3**. Published median tests detect no difference after the stated adjustment. The nine RD c3 grades differ from the eight self-reported complete tasks. Nonsignificance in these changing observed subsets does not establish equally correct complete chains or remove correctness as a possible concern in interpreting effort.

Using the printed rows and the paper's grade-at-least-5 convention, **six MF participants (2, 5, 10, 15, 22, 29) and three RD participants (24, 26, 28)** have qualifying scores on all three tasks. Missing grades leave one additional MF participant (36) and three RD participants (14, 21, 32) potentially eligible if those missing grades qualified. These are this reading's descriptive score checks, not a newly validated behavioral endpoint or an imputation of missing work as failure.

That calculation exposes a specific unresolved method issue. Section 2.6.5 says structural metrics use five randomly selected solutions per design, eligible only if all three tasks score 5 or 6. The published main-study data contain only **three RD participants with observed scores meeting that rule**. The identities of the five selected cases or a clarified eligibility/data source are not supplied. Do not silently relax the rule or assume missing scores pass.

Figure 6 nevertheless reports smaller increases in class size and non-library import coupling for RD; the authors entered selected solutions, compiled/tested them and parsed structural measures. This is author-reported processing, not our reproduction. Figure 7's separate change-size pattern is supported by descriptive arithmetic among each task's qualifying grades: MF/RD means are approximately **3.31/3.57 lines for c1, 13.90/11.57 for c2 and 28.70/15.50 for c3**. That positive RD locality result concerns selected correct task solutions. It does not establish lower subsequent maintenance effort, slower lifetime decay or a benefit across all assignments. The paper itself says the structural difference is not reflected in the external quality outcomes it observes.

The learning measure is `(understanding c1 − understanding c3)/(understanding c1 + understanding c3)`. Table 5's means are **−.096 MF and −.103 RD**, confirmed against images and raw rows; p = .52. Tasks differ in difficulty and the measure assumes early learning, so the null does not resolve long-run familiarization. RD confidence on c3 is lower under the reported adjusted test, while c3 difficulty's p = .033 fails its .0091 Holm threshold. Printed p = .000 is rounded, not an exact zero.

## Mechanism, replication and the next source decision

Distributed message paths offer a plausible explanation for higher comprehension work, particularly the cross-class ingredient check. Exploratory analyses relate self-reported strategy to c2 effort: RD has nine exploratory, eight mixed and only two systematic participants; MF has seven, seven and three. Strategy is reported after the assigned work and is not randomized. These small observational groups cannot validate a prospective strategy/architecture selection policy or a causal training benefit. Source size and nesting also change together. The admitted incorrect sequence number in one RD diagram remains an information-quality limitation; the authors' preliminary think-aloud impressions do not quantify its effect in this experiment.

The main study, its pilot, S81's later Java/professional study and S88's Java/student replication share the coffee problem lineage but differ in participants, execution tools, source versions, time limits and correctness endpoints. S88 explicitly replicates this 2001 study; it is not a direct replication of S81. The present appendix resolves the original paper's method/data dependency without automatically requiring a full dissertation reading. It does not recover the complete source variants or S81's unavailable technical-report material.

The authors contrast their result with the favorable Briand/Bunse design-document/guideline studies. Those primary methods are now selected as **S155** (`10.1109/32.926174`) and **S156** (`10.1023/A:1009720117601`) to check which systems, tasks and documentation actually vary and whether related publications share data. Native records were created/reused before intentional body reading. Their earlier abstract screening is not new full-method evidence. S95's acquired inheritance-depth method remains the subsequent comparator; broader metric and think-aloud leads remain conditional on a specific unresolved claim. See the [background ledger](../nu-background-searches-2026-09-30.md) for current acquisition states.

**Unique:** unconfirmed; within-language source organization, ordered maintenance and replication are established predecessors. **Valuable:** a meaningful comprehension/locality tradeoff is observed, with neither lifetime advantage nor Nu transfer measured. **Scientifically valid:** the original randomized main assignment and useful appendices support a scoped comparison; unequal completion/grading, selected structural outcomes, one task family, paper-only feedback and unresolved eligibility limit broader claims. Preserve all assignments and separate diagnostic opportunity, behavioral completion, source structure and later costs in any separately authorized experiment. No experimental hold changes.
