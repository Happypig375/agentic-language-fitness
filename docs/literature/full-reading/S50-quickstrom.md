# S50 — Quickstrom: temporal oracles, ambiguity and measured test effort

**Full reading completed 2026-09-29.** Liam O'Connor and Oskar Wickström, *Quickstrom: Property-based Acceptance Testing with LTL Specifications*, PLDI 2022, DOI [10.1145/3519939.3523728](https://doi.org/10.1145/3519939.3523728). The edition fully read is [arXiv 2203.11532v1](https://arxiv.org/abs/2203.11532v1), 22 March 2022. This addresses how Nu-related temporal obligations could be judged independently, and the difference between observed failures, presumptive success and complete behavioral correctness.

## Edition, coverage and provenance

Read all **13 preprint pages**, sections 1–6, all thirteen figures, two tables and forty references. MuPDF renders of PDF pages 2–10 recovered temporal symbols omitted by Poppler's text extraction and covered all figures, inference rules, specification examples and tables. Zotero parent `HWFNCEKV`, primary attachment `4FIPRX47`; 741,637 bytes; SHA-256 `baef63e9f6efc66590664696d2683dbddaf08d37da80b7f4e20a4bfe0f2a4da8`.

Also acquired the [Edinburgh peer-reviewed manuscript](https://www.pure.ed.ac.uk/ws/portalfiles/portal/282105145/Quickstrom_OCONNOR_DOA25022022_AFV.pdf): fourteen PDF pages including repository cover, 816,601 bytes, SHA-256 `dac99a15637213a7b59294dc5193577242f2663ce92f1937d3abef015ad0f214`. Checked its cover and rendered table pages 10–11; they retain the discrepancies described below. This is not a second full reading. The cover identifies a peer-reviewed version and final proceedings pages 1025–1038; whole-edition equivalence to the published fourteen-page article is unverified.

Inspected selected public artifact files, without running Quickstrom, Selenium, a browser test, an author notebook or any candidate program. Recomputing released CSV aggregates is separate from reproducing the experiment.

## Method and temporal semantics

Quickstrom observes user-facing state and chooses actions from a specification using Selenium WebDriver. Its checker evaluates QuickLTL formulas; the executor performs actions, detects events and reports state. Specstrom also defines queries, allowed actions, guards and timeouts. Thus implementation-language independence does not mean an oracle without design effort, observable-state assumptions or instrumentation.

QuickLTL distinguishes definitive truth/falsity from presumptive truth/falsity on finite **partial** traces. Required-next operators request more observations; weak/strong next default to true/false when stopping is permitted. Numeric temporal annotations control minimum exploration before a presumptive answer. They do not turn finite testing into proof of an infinite property. Formula progression and simplification determine when to stop; the paper notes potential formula growth, bounded in its examples by relatively short traces.

The egg-timer example separates permitted transitions from eventual progress. Preventing endless user interference requires a declared action restriction: the stronger time-expiry check excludes the stop action. State counts, elapsed-time timeouts, user actions and asynchronous events are distinct. Moving between those notions without an explicit assumption would change the question being tested.

The executor rejects an action based on a stale trace version. This is a concrete synchronization control, not a guarantee that every external game effect is observed. The only production-ready executor described is the WebDriver one; a communicating-process model executor aids interpreter testing, while other application domains remain proposed work. The authors have not established a complete formal relationship between QuickLTL and conventional infinite-trace temporal logics.

## Evaluation reconstructed

The study tests **43 selected implementations of one TodoMVC application**, at repository revision `41ba86d` (February 2020), against an approximately 300-line specification. These are implementations of one task family, not 43 independent domains or randomly assigned architecture conditions. Exclusions include nonstandard/streaming variants, an application that did not start, incompatible markup and unavailable compiled artifacts. Such exclusions do not justify dropping blocked ISE attempts after assignment.

Table 1 reports 23 passing and 20 failing implementations: 9/8 beta and 14/12 mature, respectively. These are results for this specification and exploration, not proof that the passing programs are correct. There is no controlled comparison of developer effort, ordinary testing, languages, functional organization or coding agents. Similar selected beta/mature failure proportions do not establish equivalence.

The authors explicitly make some judgment calls while formalizing the English specification: preserving pending input across a filter change is assumed; the filter selected after removing every item is left unspecified. The transient empty-list behavior in angular-dart is called debatable because the English specification does not forbid it. Some failures are missing UI elements/features, some simple programming mistakes, and others require longer interaction sequences. **Persistence across reloads is not tested**, despite being part of the official application specification. The demonstrated TodoMVC properties are safety properties; the timer illustrates liveness, but the reported fault-finding evaluation is not a liveness-sensitivity study.

For the runtime experiment the paper reports ten repeats per implementation at each temporal subscript, on a 2020 M1 MacBook Pro with 16 GB RAM. Its false-negative calculation conditions on implementations expected to fail; timing uses implementations expected to pass. Stopping at the first safety counterexample makes these different timing populations. Neither curve measures total specification-writing and maintenance effort or sensitivity to all undiscovered bugs. The source's approximate 42-second default run is not an ISE budget recommendation.

## Table and artifact checks

Both read manuscripts assign problem 4 to four implementations in Table 1, while Table 2 gives its count as one. Problem 7 appears twice in Table 1 but has count four in Table 2. Do not silently correct one table from the other or infer a new total defect population. The current repository's pending notes associate duel/lavaca with pending-input loss, but do not independently adjudicate every table label.

The project site links to the public repository. Inspected its complete 191-entry tree and selected files at commit [`5eafc223c54a5c1752b510ad63b6eb1055e502f2`](https://github.com/quickstrom/quickstrom/tree/5eafc223c54a5c1752b510ad63b6eb1055e502f2): root README, `todomvc.md`, benchmark pin, main TodoMVC specification, measurement/run/shared drivers, notebook source and textual outputs, six measurement CSVs and aggregate CSV. Other modules, histories, alternate specification files and the embedded notebook plot were not fully audited. The benchmark pin expands to `41ba86db92336c11e56d425c5151b7ec2932be9a`.

The released measurements contain **2,579 rows**, six subscripts and Firefox runs. Five settings have 430 rows; subscript 10 has 429 because Vue has nine recorded repeats. Each setting labels 22 implementations expected-failed and 21 expected-passed, unlike the paper's 20/23: the additional expected-failed names are aurelia and emberjs. The notebook computes unexpected passes over all expected-failed rows, including error outcomes in the denominator; those errors must not be interpreted as confirmed bug detections.

Independent standard-library calculations reproduce the released aggregate CSV:

| Subscript | Unexpected passes / expected-failed rows | Error outcomes across all rows | Geometric mean seconds for expected-passed rows |
| --- | --- | --- | --- |
| 1 | 220/220 | 0 | 12.84 |
| 5 | 197/220 | 0 | 13.22 |
| 10 | 142/220 | 0 | 14.40 |
| 50 | 67/220 | 2 | 26.40 |
| 100 | 47/220 | 1 | 40.99 |
| 500 | 18/220 | 6 | 149.13 |

The notebook calls this quantity “false positives”; its actual filter is expected-failed/observed-passed, corresponding to false negatives in the paper's bug-detection terminology. It uses a geometric mean for duration and ordinary sample standard deviation. These labels, population differences and the missing row remain explicit; no adjusted paper result is invented. The aggregate CSV hashes to `f4a4dd1761f9d79e2ec3d4a81c6c707d23a93eb69ae0e3726d70eda775a59a6b`; all selected downloads have scratch provenance/hashes.

Two further version limits matter for reproducibility. The current measurement driver records its subscript argument in the CSV but does not pass it to the checker; the main specification has a fixed subscript of 100. Manual edits or a different historical driver would be needed to reconstruct the recorded sweep. Also, the current nested editing specification uses `until`, while the paper's sketch uses release. Neither observation proves how the historical runs were made or that the paper is generally invalid. They prevent claiming an unchanged current-artifact reproduction. The separate run driver retries expected failures up to five times; it is distinct from the ten-repeat measurement driver.

## Three criteria and implications

**Unique:** declarative behavioral acceptance testing and temporal state-machine specifications already have direct implementations and evaluated applications. Nu would not invent those mechanisms. The narrower source-convention/agent-evolution question retains its separate unresolved priority.

**Valuable:** the study demonstrates author-reported discoveries of nontrivial interaction faults, while exposing specification and runtime costs. It does not establish Nu-specific benefit, cost superiority or a language/architecture ranking. One application with many implementations does not establish task diversity.

**Scientifically valid:** specify retained/new obligations independently, document ambiguous cases and accept legitimate alternatives; freeze input opportunities, event/timeout meaning and stopping semantics. Keep presumptive success, concrete counterexamples, missing observations and infrastructure errors separate. Validate oracle sensitivity on relevant fault families without assuming that longer traces or a published framework suffice. Do not import source-specific exclusions, current expected labels or a geometric timing summary into ISE automatically. No new executor or testing framework is authorized.

S46/S47 remain the closest functional-system lineage; S53 is the asynchronous temporal-testing follow-up. The cited RV-LTL/LTL3 works (DOIs `10.1093/logcom/exn075`, `10.1145/2000799.2000800`), reactive temporal logic (`10.4204/EPTCS.322.6`) and ALEX's TodoMVC study (`10.1007/978-3-319-68270-9_7`) were identity-screened after this read. Their methods remain conditional on adopting a particular temporal semantics or claiming tester superiority; no new logic or superiority claim is needed for the current Nu question. They are not counted as full readings.
