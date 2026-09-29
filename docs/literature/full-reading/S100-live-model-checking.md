# S100 — Live model checking, current-state witnesses and verification boundaries

**Complete publication reading, 2026-09-30.** Joeri Exelmans, Ciprian Teodorov and Hans Vangheluwe, *Integrating Model Checking into a Live Modeling Environment*, SLE 2025, 128–133, [DOI 10.1145/3732771.3742718](https://doi.org/10.1145/3732771.3742718). Zotero parent `M2MTQEN3`, user-library PDF `AT3EY23B`, note `NHS6H968`.

All six publisher pages, Table 1, four numbered figures, the unnumbered property automata, footnotes and twenty references were read. All six page images were inspected. The 733,323-byte PDF has SHA-256 `0df2de973329c59fca8c26cf16bf8dd4ddc7df1947149f558c14a343f2152f81`. A bounded library-source inspection is recorded below; no model checker, application, test suite or author experiment was executed. The anomalous final-page received/revised/accepted dates from 2007/2009 conflict with the verified SLE 2025 publication; they are not evidence of an earlier edition or priority.

## Live question and actual contribution

B03/B04/B07/B08 ask how editing, execution, history and future-behavior verification fit together. This paper adds model checking to the authors' operation-based live-modeling framework, whose fuller predecessor is S101. A model checker starts from the **current execution configuration** and presents a counterexample as a possible future in the same view as execution and edit history. This is an explicit integration of prospective exploration with retained state and model evolution. It is not just replay of a previously recorded failing execution.

The scope is interpreted languages with access to internal elements of both the design model and runtime model. The paper explicitly sets the state-reconciliation problem outside its new contribution. It reuses the earlier framework's treatment of edit/execution conflicts rather than independently solving every migration problem. Arbitrary black-box interpreters, generated programs, native resources and real external effects are not automatically covered by the generic interface.

The motivation is iterative development in which both the model and its formal requirements become more detailed. The paper does not claim that all desired requirements are known, encoded or correct. Reusing an interpreter avoids a separate model-to-verification-language translation, but the interpreter, observer semantics, adapter and model/environment still need validation. Agreement with the same interpreter is not an independent behavioral oracle for that interpreter's own mistakes.

## Running example: distinct obligations

Figures 1–2 trace five successive versions of a two-actor mutual-exclusion model. The user executes a step manually, invokes the checker from the resulting state, edits the model and follows the new witness. This is one author-constructed scenario, not five independent systems or a participant experiment.

| Version | Edit or observation | Remaining failure in the narrative |
| --- | --- | --- |
| 0 | Alice and Bob independently raise a flag and enter a critical section. | Both can enter; mutual exclusion fails. |
| 1 | Add guards that consult the other actor's flag. | Both flags can be raised, producing deadlock. |
| 2 | Bob drops his flag when both are raised. | Bob can repeatedly raise/drop it, allowing an infinite execution in which neither enters. |
| 3 | Add a distinct state remembering that Bob wants entry, plus a new transition. | Alice can repeatedly enter/leave while Bob remains excluded; per-actor eventual entry fails. |
| 4 | Roll back to version 1 and introduce a turn variable and changed guards. | The figure marks all four stated properties satisfied and identifies the solution with Peterson's algorithm. No independent replay of these results was performed here. |

Mutual exclusion, absence of deadlock, eventual entry by someone and eventual entry by each waiting actor are separate obligations. Retaining the current values or eliminating one counterexample does not establish the others. The property automata also make explicit that detecting a forbidden finite state differs from detecting an accepting cycle representing an infinite violation. Fairness assumptions and the exact progress property belong in the specification, not in a generic “correct” label.

## Current-state checking is conditional

Page 129 asks whether checking from the present state establishes a property over all executions from the initial state. It argues that many forever-running systems can eventually reach every runtime state from every other and treats the alternative as deadlock or livelock. This is too strong as a general justification.

**Review inference:** a system can move through a one-time initialization phase into a productive service cycle without ever returning to initialization. It need not deadlock or livelock. From one reached state, exploration may miss another branch that was possible earlier. Thus a pass from the selected checkpoint does not, without additional reachability/property conditions, imply a pass for the complete initial-state behavior. A newly edited retained state may also need a separate reachability/validity argument under the new model.

Temporal obligations can begin before the checkpoint. If a previously issued request still requires a response, a fresh property monitor must either receive the relevant historical progress or rely on a current configuration that encodes it. Merely starting the model from current values does not establish that this obligation survived. This is a control implied by the distinction between history and future exploration, not a reproduced fault in the prototype. Whole-system, current-state, finite-observation and infinite-path conclusions should be reported separately.

## Dependency and checker construction

The inherited framework records two kinds of dependencies. Overwrite dependencies connect writes to the values they replace; read dependencies connect a computation to the values used to produce it. Concurrent writes can conflict, and a concurrent read/write can invalidate an execution step even when the design edits themselves do not overlap. Figure 3 changes an initial variable value after an execution was derived from it, exposing a conflict with initialization and its dependent history.

When no conflict is detected, the framework merges edits and execution changes. That conditional mechanism depends on complete tracking of the relevant reads/writes. It is not a theorem that all real-world behavior is preserved whenever a data-level conflict detector returns no conflict. The S101 predecessor, its dependency semantics and external-state assumptions remain a consequential full reading. S85's constraint/policy approach is presented as complementary when reconciliation requires a new state.

The Semantic Language Interface supplies initial configurations, available actions, stepping and acceptance. The system interpreter is composed with a property interpreter. Safety checking seeks an accepting state; liveness checking seeks an accepting cycle. Figure 4 exposes the adapters and synchronous-product construction rather than erasing them behind the word generic.

Version histories create an important equality problem: revisiting the same semantic state creates a distinct runtime-model version. The paper therefore removes versioning information when comparing visited states while retaining history for the currently explored branch/witness. Such a reduction must preserve the observations and transitions relevant to the checked property. The paper does not provide a general proof that arbitrary history-dependent properties survive arbitrary version stripping. Merging independent exploration branches to avoid all interleavings is proposed as future work, not a measured reduction already delivered by this paper.

## Evaluation and artifact coverage

The evidence is the running example and a described web prototype of a minimal state-transition language. There is no participant count, controlled comparison, maintenance-success denominator, latency/memory benchmark or quantitative measure of reduced mental effort. The abstract's small implementation effort is not accompanied by an effort record. The suggestion that persistent functional structures could simplify or outperform defensive copies is an opinion supported by references, not an experiment in this paper.

The paper links [DOPE source](https://github.com/joeriexelmans/dope/), an [online prototype](https://deemz.org/public/live-soup/) and [Z2MC](https://github.com/plug-obp/z2mc-js). At this check, the DOPE repository fails in the web reader and its direct GitHub commits API returns **404**. The web index still shows the prototype's old JavaScript-required shell, while direct HTTPS now returns **404**. Two exact locator searches return no results. These are current access limits; they do not prove that the artifact never existed or that no other copy is available.

Z2MC remains accessible. The most recent default-branch commit returned at or before the conference end, 13 June 2025, is [`cbb0aad9e21752195487c32c3044908bf013dbbc`](https://github.com/plug-obp/z2mc-js/tree/cbb0aad9e21752195487c32c3044908bf013dbbc), dated 8 December 2022. Six selected files were downloaded and hashed: README, package metadata, `str2tr.js`, synchronous-product semantics, `mc_buchi_ndfs_gs09_cdlp05.js` and its named test file. Their entire text was inspected, with no dependency installation or execution. This dated library snapshot is not verified as the prototype's exact dependency version.

The inspected library has explicit initial/next/acceptance and hash/equality hooks; the nested DFS accepts a canonicalization function. Its synchronous products distinguish state observations from state/event observations and add a stuttering step for deadlocked system configurations. The selected test file compares expected strings for four accepting-state choices on one five-node graph, printing the comparisons. This is neither a run of those checks nor a claim about all other tests. The unavailable application prevents inspection of its actual adapters, selected checker, version-stripping function and UI/witness integration. Source availability of the generic library does not close those gaps.

## Consequences and primary follow-up

**Unique:** integrating live edits, execution history and current-state model-checking witnesses has explicit prior work. S100 extends S101 and reuses model-checking research; it is not an independent replication of that framework or proof of global firstness. Nu's distinguishing claims need a more specific boundary than “preserved state supports interactive verification.”

**Valuable:** the interface offers a concrete way to inspect possible future failures during development. Reduced mental effort, debugging/maintenance success, scalability and net cost remain unmeasured here. Inaccessible application artifacts also prevent independent validation of the demonstration at this checkpoint.

**Scientifically valid:** specify the model/environment, interpreted-state boundary, dependency completeness, checker starting state, retained property history, acceptance/fairness semantics and reduction equivalence. Count unsupported/conflicting/unexplored cases separately. A model-checker pass relative to one formal property and state is not complete application acceptance. No experimental work is authorized by this reading.

S105, *Temporal Breakpoints for Multiverse Debugging* (`10.1145/3623476.3623526`), is the direct temporal-witness predecessor; primary institutional abstract only so far. S106, *Unified verification and monitoring of executable UML specifications* (`10.1007/s10270-021-00923-9`), supplies the interpreted verification/monitoring lineage; its publisher preview explicitly distinguishes abstract environment behavior from real execution. S107, *Remote Concolic Multiverse Debugging* (`10.4230/LIPIcs.ECOOP.2026.27`), adds a later concrete-device, trace/replay alternative; selected primary HTML already states instruction/input-operation bounds. Their complete methods and artifacts remain pending. Other retained leads include user-defined reductions (`10.1145/3550355.3552447`), generated omniscient tracing (`10.1145/2814251.2814262`), AnimUML, operational semantics, and immutable-data versus specialized-trace cost comparisons. They are not replaced by this six-page reading.
