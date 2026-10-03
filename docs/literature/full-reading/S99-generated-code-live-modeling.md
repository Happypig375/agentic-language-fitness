# S99 — Fast live edits with a bounded state-transfer contract

## Identity and actual coverage

Mojtaba Bagherzadeh, Karim Jahed, Benoit Combemale and Juergen Dingel, *Live modeling in the context of state machine models and code generation*, **Software and Systems Modeling 20(3), 795–819 (2021)**, DOI [10.1007/s10270-020-00829-y](https://doi.org/10.1007/s10270-020-00829-y). Online publication is **2 November 2020**, distinct from the 2021 issue. Existing native parent/note/PDF **`E8X8DKNI` / `GCPX87Z6` / `DPYD79QQ`** were verified before continuing beyond first-page coverage. Four collection memberships are retained: `PKLXQNEE`, `74BHFBRZ`, `NDU9BTP7`, `MBYQJXUF`.

The user-library publisher PDF has **25 pages, 1,543,628 bytes**, SHA-256 **`b21e4ed40fc6d18dc4b915568e69c8864e5be94f0df69a0ed19f4776d3f41988`**, MD5 `7fab37322446e6ca2ece353556429914`; local/native identities match. **All 25 text pages, seven sections, eleven figures, three tables, two listings, Algorithm 1 and 90 references are read.** Fifteen physical pages are visually inspected: **1, 4, 6–8, 10–14 and 16–20**. There are no appendices. A truncated extraction display of pages 21–22 was recovered separately. The source/data reading below is bounded; no author program, model, transformation, compiler, benchmark, interpreter or test was executed.

The cited 2019 five-page *Live-UMLRT* tool paper and earlier MDebugger publications are related development reports, not independent replications of this journal comparison. Their bibliographic entries are read; their bodies are not newly read here. Prior S85 already reconstructs the constraint-based migration alternative that this paper contrasts with.

## Architecture and useful capability

Live-UMLRT combines **compiled code with an editable runtime representation**. Instrumentation and extended Papyrus-RT generation create state/trigger tables, action pointers and a debugging interface. An Eclipse plugin sends edits to the running program, which updates those tables rather than regenerating and compiling the whole model for each change. Existing action bodies initially execute as compiled C++; editing an action replaces its pointer with a proxy that interprets the changed action until execution ends (Sections 3–4).

This is a concrete alternative to both ordinary recompilation/hot-patching and wholly interpreted models. It avoids depending on the target language's built-in live-update facilities, but still requires language-specific instrumentation, a generator/runtime extension and an action interpreter. The prototype supports arithmetic/logical expressions and sending messages; arbitrary C++ edits are outside that interpreter. Deterministic model execution and suitable control/communication constructs are generality assumptions, not properties obtained from reflection alone.

The UML-RT model consists of active capsules communicating through typed ports. Its state machines support hierarchy but exclude orthogonal regions, fork/join, shallow history, final states and do-actions; transition triggers from the same ordinary state must be disjoint. **Table 1 explicitly limits edit scope:** states, transitions and triggers can be added/removed/updated; variables can be added, but their declarations cannot be removed or changed; capsules, ports and protocols cannot be changed. Variable-value assignment through the REPL is distinct from changing a variable's declaration. Action/guard replacement uses supported addition/removal operations, with no general arbitrary-language editing guarantee.

Instrumentation adds debugging transitions and routing points. A regular debugging message starts a session at the capsule's run-to-completion boundary, after its preceding message finishes. The capsule pauses while other capsules' messages queue. On resumption it normally returns to its former active state. If that state was deleted, the user selects a replacement; if all states were deleted, new states are required before resumption. The external application is assumed to validate requests before sending them, including syntax and model consistency (Section 4.3). The paper's “safe update” therefore includes explicit restrictions, validation and user choice; it does not prove intended application invariants after every edit.

Design-view changes update the runtime model. The implementation does not generally propagate console/runtime edits back to the design model; the action-recording interface has a narrower save/translation route. Persistent source changes and temporary exploratory state thus remain separate obligations.

## What replay retains and what it does not

The trace map retains **the most recent exit from each basic state**, comprising the state, triggering message and variable values immediately before exit. Algorithm 1 follows these latest messages through the current state map to construct a path from a selected source to a destination. It fails on an unvisited state or a loop in the attempted path. On success, it restores the source variables, steers execution there, defers currently queued messages and injects the selected replay messages. Deferred messages require later recall through actions or a debugging command.

This supports the useful debugging operation of revisiting an earlier local step after editing its action. It is not a complete chronological history: latest-per-state records can come from different visits, and loops limit rewind. More decisively, **only the target capsule is restored**. During replay it can send messages to other capsules whose state has not been rewound, and the paper explicitly acknowledges unexpected reactions (Section 4.3.1). Rewinding all relevant capsules is future work. Injecting the target's needed messages does not make those external reactions consistent or undo physical effects.

For Nu, this supplies a clear rival mechanism and a concrete comparison boundary: what is restored, what queued work is deferred, whether replay crosses an edit, and which components/effects share the history. Current-state well-formedness, useful local re-execution and system-wide preservation are different outcomes. Neither this paper nor retained immutable state removes the need to specify the latter.

## Evaluation: retain the large edit advantage and the shifted costs

Six model configurations range from 11 to 350 states; Debuggable FailOver is an instrumented version of FailOver, not an independent domain. Generation/instrumentation and supported edit operations are each measured twenty times, with reported medians. The machine is a 2.2 GHz i7-4770HQ with 8 GB RAM, macOS 10.12 and OpenJDK 8 with a 4 GB heap. Edit timing uses the largest configuration; CPU/peak-memory comparisons use FailOver processing 10,000 requests. This is tool-performance evidence without a controlled developer study.

| Outcome | Reported comparison and interpretation |
| --- | --- |
| Generation/setup | Table 2 gives 46,692 ms extended generation versus 43,623 ms default generation for Debuggable FailOver, plus 6,200 ms instrumentation. The smaller generation times are mixed, from 1,056 versus 1,063 ms to 1,274 versus 1,197 ms. Compile/build time is excluded from this question; setup is not fully measured by these columns. |
| One edit | Across seven operation rows: **1.3–2.1 ms** versus **608 ms** for the authors' regeneration/build/shared-library route. This is a large favorable latency comparison. The maximum also contradicts the prose's universal under-two-millisecond wording. |
| Ten edits across three components | **9.9–18.1 ms** versus **1,192 ms**. Printed row ratios are about 66–120; the summary is about 92-fold. These are edit-operation timings, not end-to-end task completion or general feedback latency. |
| Unedited program CPU | The paper prints **510 ms for its approach and 514 ms default**, while describing its approach as one percent slower. Those values imply about **0.78% faster**, so the sign/assignment is unresolved. Preserve the small printed difference without endorsing either direction as a measured general advantage. |
| Edited action execution | A selected 100-line action is reported **70% slower when interpreted** than compiled. No workload-wide rate follows from this one action. |
| Peak memory | **2,083 kB versus 1,664 kB**, a **25.18%** increase from printed values, consistent with the rounded 25% report. This is peak process memory, unlike S106's binary-size measure. |

Own arithmetic checks all seven pairs of edit rows. For the single remove/update-transition row, **608 / 1.8 = 337.78**, not the printed 377. Ratios of the displayed mean times differ from averaging row ratios; without the underlying observations, the precise “400/405-fold” summary cannot be uniquely recovered. All displayed one-edit comparisons nevertheless favor Live-UMLRT by roughly **290–468-fold**. These localized reporting issues do not erase the substantial latency result.

There is no user-success, repair-correctness, learning or total-integration-time experiment. The authors themselves qualify memory-constrained and time-sensitive deployment. The assumption that results from the largest model safely generalize to all smaller use cases is stronger than the measured coverage, since action content and interaction structure also affect cost.

## Bounded release reconstruction

The [paper-linked Bitbucket release](https://bitbucket.org/moji1/live-umlrt/src/1f8482755390c9a9106b91d48948b80711d95985/) is pinned to **`1f8482755390c9a9106b91d48948b80711d95985`**, **22 April 2020**, commit message “added eval data.” Web page retrieval fails, but the public repository/source API works. The root and eleven selected directory listings are inspected, each in one returned page; **the full recursive repository is not inventoried**. A guessed `umlrt/src` path failed before the actual `umlrts/umlrt` directory was located.

Eight files are fully read; three have the exact partial scopes shown below. All bytes are hashed; assets and extracted bodies stay outside Git.

| Path | Coverage | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `README.md` | Full | 127 | `4b6bcd756aeac7192c66bfe517e47194ff9c60484b2eeecc9e36e881497ca025` |
| `evaluation/generator.sh` | Full | 397 | `dfeedd474e1cc6262158de8b66fda3adc312b624ebb8a223e695d49966c5f641` |
| `evaluation/results.txt` | Full | 3,211 | `915e47521d5ac60429360d9d9b873a4ad84306c657d49286634765f6c9423c15` |
| `evaluation/results2.txt` | Full | 919 | `b770ccba7fb82bbf74cbc0dfd8dba0a206c814bd4ca6bc8da40c57b54ba5b638` |
| `evaluation/server.py` | Full | 628 | `912534608560da19c3a1bf8ab7b355560a485a0e633c003273800453ecb66b79` |
| `transformation/script/PMDPreparation.eol` | Full | 9,319 | `f685dc818d2f29e97f12dbd146b6d59eef22999adc22d542f585fe34760156a4` |
| `transformation/script/RefineForPMD.eol` | Full | 3,499 | `de3234c3d4161f5b603ab00046898de9b35c933ac068238f7aee1e20a1359f03` |
| `papyrusrt/org.eclipse.papyrusrt.rts/umlrts/umlrt/umlrtcapsule.cc` | Full | 12,329 | `b3e137656bceda74095c1a466016a286691cf03a6f736bb1e12fe43149638837` |
| `livemodeling/src/pme_core/ExecHelper.cpp` | Lines 1–208, plus search navigation | 10,732 | `8cde3aa0a94973a8bf424f76a9bcb4a4830a6231a6022e0c2c278a020e791c32` |
| `livemodeling/src/pme_core/ExecContext.cpp` | Lines 150–265 and 390–450, plus search navigation | 21,904 | `0ee3fbe78c2d92abf11ea41cb5db42910f6e53ff9564859a5f05d703128d9557` |
| `livemodeling/src/pme_core/PMEExprVisitorImp.cpp` | Lines 347–442, plus search navigation | 16,545 | `939257c0fb9b54ee7e525ffcb1e3603b3515d3f00c8e12225349852c0e2462db` |

The release adds useful positive correspondence and explicit limits:

1. **All twelve generation timings match Table 2.** The hot-patching components also sum exactly to the two published baselines: `113 + 398 + 97 = 608 ms` and `319 + 512 + 361 = 1,192 ms`. The result file separately lists **1,115 / 1,034 ms detection delays**, which are excluded from those totals. Thus even the comparator timings are not complete edit-to-visible-effect measurements. The file labels operations “average,” while the publication labels its tables medians; twenty original observations per cell are not supplied here.
2. **The stored result packet contains other workloads.** Four transition-count stress rows (1, 100, 1,000, 10,000) report slower lookup/execution times for the extended route and increasing peak-memory costs. These rows are not the final FailOver 10,000-request comparison. Two unlabeled process-timing lines and repeated code-size tables do not settle the final CPU-sign discrepancy. Rover's binary-size rows say it cannot build in both conditions; generation timings can still have been measured. These are historical stored reports, not failures reproduced now.
3. **Source establishes specific runtime-table machinery.** The capsule code implements state/transition insertion and callback-driven editing. The selected visitor routes edits to those callbacks; preparation emits variable/communication support. The helper's function named `replay` interprets a saved command string, while the visitor's replay-message command invokes a defer/recall callback. These are not, by themselves, the complete source-to-destination trace-map algorithm printed in the final paper. A socket/timing block in the inspected helper is commented out. Exact final implementation and timing-harness correspondence remain unresolved within this bounded reading.

No artifact installation or execution is needed to preserve the mechanism and reported benefit at these scopes. The release is available; its incomplete final-run correspondence must not be mislabeled inaccessible evidence or a reproduced failure.

## Consequence for the Nu comparison

For **B03/B04/B05/B06/B08/B10/B12**, this is direct prior evidence that mutable runtime tables plus compiled code can support low-latency live changes. The meaningful architecture contrast concerns editable scope, paused components, retained state, queued work, replayed effects and costs. It is not simply immutable versus mutable, compiled versus interpreted, or presence versus absence of a live-development feature.

Together, S99/S105/S106 distinguish three useful capabilities: modifying a paused running component, searching alternative futures with branch-specific monitor state, and monitoring an actual scheduled trace. None substitutes for the others. Nu's prospective research value depends on a specific improvement in correct completed changes or diagnosis and its total cost, beyond demonstrating these established capabilities. Existing pilot outcomes and adverse compactness evidence remain unchanged.

[S107](S107-remote-concolic-debugging.md) now reconstructs the remote alternative: root reset and mocked-input replay, bounded path suggestions and lower forward overhead, with external effects outside restoration. Consolidate the live-state architecture comparison using these completed methods; retain MIO’s own compensation method as a primary dependency if the comparison relies on its exact I/O contract. Professional S229 access, .NET/game transfer and other B01–B12 discovery/primary gaps remain separately recorded. All construction, experiment and extra-worker holds remain.
