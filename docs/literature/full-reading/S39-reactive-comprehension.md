# S39 - Reactive programming and human comprehension

**Full reading completed 2026-09-29.** Guido Salvaneschi, Sebastian Proksch, Sven Amann, Sarah Nadi and Mira Mezini, *On the Positive Effect of Reactive Programming on Software Comprehension: An Empirical Study*, IEEE TSE 43(12), 2017, pp. 1125-1143, DOI [10.1109/TSE.2017.2655524](https://doi.org/10.1109/TSE.2017.2655524). Read all 19 pages of the [author-hosted IEEE-formatted manuscript](https://www.rescala-lang.com/assets/pdf/2017%20Empirical%20RP%20Comprehension.pdf), including sections 1-9, references and biographies. Figures 1-12, tables 1-5 and the scoring/statistical expressions were inspected. Reader: the main Codex session; no independent human review or reproduction.

Zotero parent `95DFRAQD`, PDF `AZU7KZDN`; SHA-256 `7d5434bf480880ee208a3d07d067fe21bbc7749eb99703e8092348da8f263f25`. The title, authors and 127-person extended study match the bibliographic record. The manuscript is numbered 1-19; binary equivalence to the publisher's final PDF was not checked. PDF pages 3-11 were rendered with Poppler. Its missing Symbol font erased Figure 11's scatterplot dots; MuPDF rendered page 10 correctly and the actual point distribution was inspected. No unresolved figure-reading gap remains.

## Comparison and denominators

Sections 3-4 describe ten author-developed reactive programs: four synthetic dependency tasks, three animations and three interactive applications. Each has a Scala Observer-pattern version and a REScala signal/event version. Participants answer multiple-choice behavioral-comprehension questions; they do not implement changes or repair a repository. Browser search and syntax highlighting are available, but execution, debuggers and ordinary IDE assistance are excluded.

The study randomly assigns fourth-year software-engineering students to between-subject groups at login: 62 REScala and 65 Observer participants. The 127 participants comprise 38 from the earlier 2014 study and 89 added in 2015; the conference predecessor and journal extension are not independent replications. Participants have Scala coursework and prior Java/Observer experience, plus two 1.5-hour RP lectures and two assignments estimated at eight hours each. Calling this only three hours of exposure omits the assigned homework.

The correctness outcome sums ten answers per participant. Reported means are 8.13 for RP and 7.05 for Observer; Table 1 reports a Mann-Whitney difference and Cliff's delta magnitude 0.36. The printed `p = 0.000` is rounded reporting, not a probability literally equal to zero. Task-specific correctness and timing analyses use nominal 0.05 tests. Tasks have five- or ten-minute limits. Tables 3 and 4 separately analyze all available answer times and times for correct answers; their varying denominators must remain visible. No raw participant/timing dataset was independently obtained or reanalyzed here.

## What the results support

The study supplies controlled evidence for improved comprehension scores under this language, training, task and tool policy. It does not isolate brevity, declarative dependencies or automatic propagation as the causal mechanism: these change together. The 89-person second-round questionnaire supplies perceptions and possible explanations, including reduced boilerplate, but no randomized mechanism comparison.

Sections 5-7 retain adverse mechanisms: unfamiliar combinators, hidden propagation, imperative/reactive integration and learning costs. Generalization to Rx is explicitly speculative. The authors acknowledge small tasks, student participants, one RP implementation and the restricted environment. Nonsignificant results do not establish equal time or skill independence; a correlation significant in one group and nonsignificant in another is not itself a test of the difference between correlations. Preserve task-level variation and participant dependence instead of treating 1,270 answers as independent assignments.

## Bounded reporting discrepancies

Rendered Tables 2-5 and Figures 9/12 do not justify copying every prose number uncritically. Task 8 has 60/62 correct RP answers and 61/65 Observer answers: the raw count is lower for RP, but its proportion is higher, contrary to the adverse-task interpretation in section 4.1. Task 4 prints 60 correct and 98.80%; 60/62 is approximately 96.77%. Figure 12 shows 23+44=67 Q4 endorsements among 87 answers, while the prose says 77 subjects (77%). These are local reporting discrepancies, not a retraction of the overall comparison. The unmatched timing denominators and exact scoring logs remain reconstruction gaps.

## Consequences and live follow-ups

| Claim or control | Disposition |
| --- | --- |
| Functional/reactive organization can help human comprehension | Supported for this bounded comparison; do not claim that no empirical evaluation exists. |
| Nu, F# or immutable state generally makes maintenance easier | Unresolved: population, intervention and endpoint differ. A causal Nu claim needs behavioral maintenance outcomes and realistic common tool access. |
| Shorter source explains the advantage | Unisolated rival. Measure actual obligations and allow adverse integration/combinator cases. |
| D1 exhaustive matches improve coding-agent evolution | Not tested. Keep the source-equivalence, common-feedback and independent temporal-oracle requirements in PLAN. |

S41's readability-metric counterpoint, S40's API usability study, and S43/S49's debugger studies are consequential follow-ups: they can change what outcome is credible and whether tool access modifies the apparent paradigm advantage. Reference 67's Scala/Java multicore comparison is a conditional counterexample to generic productivity claims; its result is not credited from this secondary mention. No new experiment or worker is authorized.

**Unique:** general reactive-comprehension evaluation already exists; D1 priority remains unconfirmed. **Valuable:** human comprehension has measured evidence here, while Nu/agent maintenance benefit remains unmeasured. **Scientifically valid:** this read informs controls and limits; it does not validate ISE's proposed apparatus.
