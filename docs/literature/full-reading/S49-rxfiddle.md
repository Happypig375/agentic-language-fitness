# S49 - RxFiddle: data-flow debugging and selected-completion timing

**Full paper reading completed 2026-09-29, with explicit figure gaps.** Herman Banken, Erik Meijer and Georgios Gousios, *Debugging Data Flows in Reactive Programs*, ICSE 2018, DOI [10.1145/3180155.3180156](https://doi.org/10.1145/3180155.3180156). All 12 pages, sections 1-10, 52 references, Table 1 and available components of figures 1-4 were read. All 12 pages were also inspected as MuPDF renders because text extraction corrupts ligatures. Reader: the main Codex session, not independent human review.

The author-hosted PDF is Zotero parent `9YYUZNYJ`, attachment `2ZSDZTEN`, SHA-256 `3c4bcd69b25ddf2c1e31e6944680218455a987190c54ea8c7dd9b1cac4337fe6`. Figure 1c and figures 4b/4d have captions but blank panels in this file. Poppler independently confirmed the blank result plots. A [TU Delft repository copy](https://pure.tudelft.nl/ws/files/38856517/paper.pdf), 13 pages including a generated cover, 840,916 bytes, SHA-256 `ab8bf201a6ad3449c7a8777bc62be2d29fc4e0b9039a3e52957280f7f5946bf3`, has the same gaps at PDF pages 4 and 9. Its cover labels the deposit final published version; this does not establish a separate publisher-file equivalence check. The ACM PDF route returned 403. The repository cover and those two pages were inspected, not relabeled as a second full reading. Selected matching artifact plots were inspected separately below.

The additional stored repository PDF is `3J4V6C2G`; completion note `E7HKGADH`. Both parent linkage and the additional stored PDF hash were independently verified through Zotero's local API.

## Intervention and evidence units

RxFiddle combines a simplified graph of Observable/Observer relationships with dynamic marble diagrams that expose event values, ordering and lifecycle. Instrumentation and rendering are separate; the implemented evaluation concerns RxJS. The tool records reactive flow events, not every program state or external effect. Other-language support, graph scalability and nonintrusive breakpoint behavior are partly future work.

The design starts with interviews of **five professional developers at two companies**, four from one company, plus selected books/documentation. These identify practices and problems; they do not estimate industry prevalence or independently establish a benefit. Four interviewees did not test Rx logic specifically, whereas the fifth used the library's testing facilities. This variability matters to any claim that notation automatically provides effective verification.

The user experiment compares **tools on reactive code**: Chrome/console debugging versus RxFiddle in a browser interface. It uses a tutorial/warm-up and four authored tasks. T1/T2 request output/comprehension facts. T3 asks which event causes a mocked service failure; T4 asks for a textual diagnosis and proposed solution to out-of-order responses. They do not implement and independently test a series of maintenance patches. Offline participants received a talk; online participants received videos derived from it. Some had already encountered the tool during piloting.

**111 people started**: 13 offline and 98 online. Ninety-eight completed the preliminary questionnaire, and 89/74/67/58 started T1/T2/T3/T4. The paper then analyzes only answers classified correct. Its combined timing table has much smaller, changing denominators:

| Task | Started, both groups | Console / RxFiddle in timing comparison | Reported p | Reported Cliff's delta |
| --- | ---: | --- | ---: | ---: |
| T1 | 89 | 34 / 36 | 0.540 | 0.0866 |
| T2 | 74 | 32 / 31 | 0.780 | -0.0424 |
| T3 | 67 | 23 / 28 | 6.19 × 10^-6 | 0.702 |
| T4 | 58 | 13 / 12 | 0.347 | 0.231 |

Only T3 supplies a reported significant advantage. The more-experienced subgroup again has a significant T3 result; it is a subgroup of the same experiment, not an independent replication. Failure to reject a difference for the other tasks does not establish equivalence. Similar reported dropout percentages do not establish absence of motivation or attrition bias. Correct-answer timing cannot by itself identify an all-assigned-attempt or fixed-budget success effect.

## Bounded artifact inspection

Reference 4 links [Zenodo 814981](https://zenodo.org/records/814981), a 2017 thesis/release artifact, not a separately verified 2018 experimental revision. `RxFiddle-thesis-doi.zip` was acquired through the public API: 7,849,447 bytes, published MD5 `dd86f363498a774416d5d68d8be35633` verified, SHA-256 `06f938fff525ef384b75d2a74d819fccda9309dab155848d4a07530c3034f28e`. Its complete inventory contains 398 entries. No archived code or analysis script was executed.

Actual inspected members: root and `doc/` READMEs; `doc/chapters/6.evaluate.tex` and `7.results.tex`; `doc/images/resultPerTask.R`, `timePerTask.R`, `wilcox-cliffs.R`, `shared.R`; both `doc/tables/wilcoxonPerTask*.tex` tables; rendered `resultPerTask.pdf`, `timePerTask.pdf`, `timePerTaskRx.pdf` and `marble-diagram.pdf`; selected allocation/submission/checker/timeout portions of `app/src/experiment.ts`, `experiment/samples.ts` and `experiment/testScreen.ts`. The appendix file merely supplied its plot reference; its extra subgroup plot and the rest of the thesis/source were not fully read.

The two released tables match the paper's denominators and statistics. The separate plots show the reported T3 timing contrast and other tasks' overlapping distributions, but do not fill the blank conference panels by proven file equivalence. The task-outcome plot distinguishes correct, incomplete, unstarted and passed states; its rounded percentages cannot be assumed to reconstruct every timing denominator. Analysis scripts omit missing per-task correct times and load `current.arff` from an external local path. That dataset is absent from the acquired archive, so participant-level statistics and classification cannot be reproduced from these materials.

The client code contains both a random initial choice and a numeric-reference parity assignment route; actual assignment histories and the deployed experimental version were not recovered. The task UI supplies timeouts and retry/pass behavior. T4's client completion check requires the expected movie title and nonempty diagnosis/solution fields, rather than executing a proposed repair. A subsequent manual judgment may differ, but the mapping to the published correct-answer field is not supplied by the inspected archive. Do not substitute client completion for independently verified correctness.

## Implications and remaining scope

The authors report that graphs from larger applications could become too large to render in real time, that timing/control dependencies can be confused with data dependencies, and that long histories challenge the visualization. These are concrete adverse cases for a claim that more runtime context is always useful. Their post-release usage counts and anecdotes are adoption observations, not a controlled user-owned-code evaluation. The tutorials, released thesis PDF, external dataset and full implementation were not evaluated here.

**Unique:** reactive lifecycle/dataflow visualization and tool comparisons are established prior art. **Valuable:** there is a bounded task-specific human timing result, alongside attrition, unsuccessful attempts and scalability costs; no Nu, coding-agent or general maintenance benefit follows. **Scientifically valid:** preserve all assigned attempts, distinguish started/completed/correct and retain exact stopping/scoring rules. A tool intervention must be named separately from D1's source convention, with common source/tool opportunity and independent complete behavioral obligations. S40 remains the direct API-usability counterpoint; S50/S51 address temporal oracles and the game-debugging field. Allocation remains zero.
