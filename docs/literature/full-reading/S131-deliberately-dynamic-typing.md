# S131 — Deliberately favorable dynamic-typing tasks still give mixed results

**Complete publisher reading, 2026-10-01 HKT; printed-data reconstruction, no experimental reproduction.** Sebastian Okon and Stefan Hanenberg, *Can We Enforce a Benefit for Dynamically Typed Languages in Comparison to Statically Typed Ones? A Controlled Experiment*, ICPC 2016. DOI [10.1109/ICPC.2016.7503719](https://doi.org/10.1109/ICPC.2016.7503719).

## Identity and actual coverage

Zotero parent `VWPVVGE7` preceded reading. The user-library publisher attachment `VHM8K8L2` closes the earlier access gap: ten pages, 1,482,557 bytes, SHA-256 `8489383300c0d378bcb3894a3cf58024b01539d0d43731062aedb9da36afc90f`. All ten pages, eight figures, four tables, task code and 23 references were read. The opening and all figure/table pages were visually checked. Full note `XG4877T5` retains this edition. No source implementation, participant session, statistical test or author analysis was rerun; the arithmetic below reconstructs the printed table only.

## Question, selection and treatment

The authors deliberately seek tasks favorable to dynamic typing, including artificial cases rather than a representative sample of development. Community requests through Stack Overflow, Lambda the Ultimate and Reddit yield two related collection examples. An interface-completion argument from Costanza motivates another task; the authors add a class-replacement task. Failure to elicit more examples is not evidence that such benefits are rare. The selected tasks already produce effects in both directions.

Java and Groovy run in Eclipse with a Groovy plugin. Exact language, compiler and IDE versions are not reported. Participants are volunteer students at least in their fifth semester, with Java as their main instructional language; a ten-minute warm-up introduces Groovy. The comparison changes language, checking, annotation requirements and tool support together. It does not hold type information constant as S130 attempts, or isolate source names as S127 does.

Task 1 flattens nested collections while preserving the concrete collection kind. Task 2 extracts media from a gallery through nested generic sequences and variance. The Java assignments add compile/use/type constraints and generic return requirements that are absent from the Groovy assignments. These are concrete examples of annotation/expressiveness burden, but not two language implementations under identical deliverable obligations.

Task 3 replaces Photographer with Paparazzo from a different third-party API, including changed personal-data structure and a coordinate representation change. Java exposes 46 compiler-error sites while the paper describes four required Groovy edits. That larger error count does not measure larger total effort. Compatibility with the old class is explicitly unnecessary; this is not D1's independent retained-and-new behavior comparison.

Task 4 completes a class implementing ViewItem, whose 26 methods include five actually needed by the application. Participants do not know which five in advance. Java requires interface completion; Groovy can encounter missing methods when they are called. The task operationalizes a tradeoff between up-front interface obligations and use-triggered discovery, while the paper's explanation involving stubs is not an independently isolated intervention. It is more elaborate than the three-method motivating example.

## Assignment, stopping and missingness

Participants are randomly allocated to Java-first or Groovy-first groups. Everyone receives tasks 1–4 in fixed order in the first language, then renamed versions of tasks 1–2 in the other language. Tasks 1–2 therefore have paired observations and period/carryover exposure; tasks 3–4 have only a between-group comparison. Random order allocation does not remove fixed task order or the asymmetry of prior Java experience.

Time runs from assignment delivery until the supplied tests pass. Test source is hidden. This is a feedback/stopping criterion, without a separately established independent post-assessment of intended behavior. At sixty minutes an unfinished task receives 3,600 seconds **as if completed**. Those observations retain useful budget information but are censored attempts, not observed successful completion times.

Twenty-one people start; five perform only the first four tasks and are excluded from the entire analysis, including their earlier work. The prose therefore implies sixteen retained participants and groups of eight. Table II instead contains **fifteen rows**, IDs 1 and 3–16, with eight Java-first and seven Groovy-first participants. Its displayed language means agree with those fifteen rows. No missing ID 2, sixteenth trajectory or excluded-participant result is invented.

## Results and reconstruction

All fifteen printed rows were transcribed: **90 direct timing entries and 30 printed paired differences**, not 120 independent times. Language means, medians and sample deviations were recomputed, together with phase differences and caps.

| Task | Visible Java / Groovy n | Recomputed mean seconds, Java / Groovy | Recomputed median seconds, Java / Groovy | Supported direction in these tasks |
| --- | --- | --- | --- | --- |
| 1, collection flattening | 15 / 15, paired | 1,089.67 / 505.40 | 843 / 457 | Groovy faster for 14 of 15 |
| 2, media extraction | 15 / 15, paired | 789.40 / 363.13 | 632 / 260 | Groovy faster for 14 of 15 |
| 3, class replacement | 8 / 7, between groups | 876.13 / 1,710.71 | 859 / 1,863 | Java group faster |
| 4, interface completion | 8 / 7, between groups | 2,258.00 / 3,302.86 | 1,979 / 3,536 | Java group faster; caps retained |

Table II's difference column has material inconsistencies. For task 2, ID 4 prints 891 although 570−204 is 366; ID 16 prints 743 although 639−260 is 379. The printed difference-column mean is 486 seconds and median 420; subtraction from the displayed direct times instead gives mean **426.27** and median **366**. Table IV's reported mean difference of 426 agrees with the direct-time calculation. This does not identify which original cells or processing step caused the discrepancy. Task 1 also prints 8 rather than 7 for ID 5, a one-second discrepancy that could involve unreported rounding. Its recomputed mean paired difference is 584.27 seconds.

Task 1's exception is ID 13 (639 Java, 715 Groovy), despite a reversed sentence about this person in the prose. Task 2's exception is ID 15. The main favorable directions survive these printed inconsistencies. The caps occur in task 4: one visible Java participant (ID 8) and three Groovy participants (5, 11, 15). They must not be counted as four observed successful completions.

The reported mixed ANOVA gives a language-by-task interaction, p<.001, partial eta-squared .627; the overall language term p=.487 is not equivalence. First-phase between-group tests report p=.009/.04/.004/.021 for tasks 1–4, with the last two favoring Java. Second-phase task 1/2 tests report p=.001/.021, again favoring Groovy. The paired-results prose describes Wilcoxon signed-rank tests with p<.001, while Table IV is captioned Mann–Whitney and prints .001/.001. These labels/rounding remain unreconciled. No new inferential replication is claimed from the printed cells.

## What the evidence does and does not settle

The study supplies positive evidence for dynamic typing on the two chosen generic-API construction tasks, and positive evidence for the Java bundle on replacement/interface tasks. Neither should be discarded because it is inconvenient to a preferred theory. Conversely, their combination is not a representative net lifecycle estimate or a universal winner. The paper's claim that construction savings are lost by API users draws on other studies, not a joint measurement of authors and users of these artifacts.

Task sampling, unequal typing obligations, completer exclusion, missing-row correspondence, capped attempts and bundled tools limit transfer. The authors acknowledge that other static type systems differ. No result here estimates F# versus C#, an agent effect, future-constructor handling, a catch-all convention effect or Nu's combined architecture. Counting required edits or compiler errors would miss the demonstrated timing direction in task 3.

## Artifact search and consequential leads

W101's two exact DOI/title data/correction queries returned seventeen distinct search URLs. W102 followed institutional and personal author locators; W103 followed the author's online-experiment repository. No S131 correction or raw-data packet was recovered. This is a bounded search result, not proof that none exists or that repository history has been exhausted.

The complete [README at pinned revision `c6ec21a`](https://github.com/shanenbe/Experiments/blob/c6ec21a8938d987450bce34b726d55cf4fe797c9/README.md) has 6,417 bytes, SHA-256 `1623babf8a6f11574e0170c25ca6e2fa9d972e456455cbc2474ce93f1ff1cdd9`. It describes newer N-of-1 experiment definitions and deliberately separate versions of their runtime library. Its 2026 constructor-call heading supplies an artifact route for the already recorded conditional study, with a title variation to reconcile; it is not the 2016 dataset. The root also exposes a Rust-readability route whose relationship to the recorded ownership study is unverified. No experiment was launched and no dependencies were installed. Incidental linked studies were not read or credited from the README.

The full bibliography preserves Costanza's interface argument as a conditional primary dependency; S117/S126–S130 already cover several checking/information comparisons. S132's earlier contrary development study remains acquired but unread beyond its opening because text extraction is broken. Two new search fragments, Krueger's community-question work and a UNLV dissertation, are conditional methodology leads, not primary outcome evidence. S119's compositional checker and S115/S118's extension mechanisms remain concrete B02 dependencies before another broad human-typing expansion.

**Unique:** unresolved; task-dependent typing benefits and burdens have direct predecessors. **Valuable:** both dynamic construction gains and static maintenance gains are observed within selected tasks, while prevalence, net lifecycle cost and Nu/agent transfer remain unmeasured. **Scientifically valid:** this method and visible arithmetic are reconstructed; all-assigned outcomes, raw-data correspondence and a common-obligation causal contrast remain unresolved. All experimental holds remain.
