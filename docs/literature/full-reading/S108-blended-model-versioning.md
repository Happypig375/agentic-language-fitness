# S108 — Dependency-aware versioning for blended models

**Complete publication reading, 2026-09-30.** Joeri Exelmans, Jakob Pietron, Alexander Raschke, Hans Vangheluwe and Matthias Tichy, *A new versioning approach for collaboration in blended modeling*, Journal of Computer Languages 76 (2023), 101221; online 17 June, August issue. [DOI 10.1016/j.cola.2023.101221](https://doi.org/10.1016/j.cola.2023.101221). Zotero parent `IXAXLQI6`, PDF `I3IXVFWT`, complete note `S94ASSGT`.

The existing [author-hosted publisher PDF](https://joeri-exelmans.page/papers/comlang23.pdf) was reverified before further reading: eighteen pages, 2,975,356 bytes, SHA-256 `4018d4dd1a3e52564ccf568509cee4fcfb31d0d6928509ac02390563174519ce`. All pages, twenty figures, Table 1, footnotes and 44 references were read. Fourteen page images, PDF pp. 2–15, cover every figure/table and the implementation's hash description. Text extraction and rendered layouts were reconciled. A separately hashed deployed JavaScript bundle received the bounded static inspection below; no application or author tests were executed.

## Claim, lineage and demonstrated capability

B02/B03/B04/B08 need the core dependency and conflict rules delegated by [S101](S101-operation-based-live-models.md). S108 versions an abstract model, its concrete representations and their correspondence separately, while preserving enough edit history to propagate and reconcile changes. This is concrete prior art for combining multiple views, history and conflict information. It extends the 2022 workshop *Optimistic versioning for conflict-tolerant collaborative blended modeling*, not S101's different 2023 live-model conference predecessor. S101 subsequently adds runtime interpretation and read dependencies; neither is demonstrated by the original S108 method alone.

The running Statechart example deliberately contains only state nesting: at most one parent per state and no containment cycles. It excludes transitions, initial states, orthogonal regions and execution semantics. A visual concrete syntax uses rectangle containment; an introductory textual syntax is assumed already parsed. Alice adds a nested state while Bob deletes its parent. Merging rectangle edits can appear geometrically acceptable while the abstract parent relationship conflicts. A versioned correspondence model makes that semantic discrepancy visible. This favorable example is an important capability, not a measured reduction in developer error.

The final demonstrator has two visual concrete syntaxes of the same kind. Textual editing and the broader partially overlapping-model case remain future extensions. Figure 20 locates the approach among state/operation-based versioning, persistent dependencies, model versioning and blended modeling. That author taxonomy and the related-work comparisons are not an independent comparative evaluation.

## Graph, operations and valid versions

Node identities are immutable and globally unique; recreating a deleted node uses a fresh identity. Primitive values are immutable and always available. An outgoing edge is identified by its source node and label, and targets a node, a primitive value or null. Incoming references to a deleted node must be cleared. Lists, sets and richer objects require graph encodings; their desired semantics do not follow from the primitive graph automatically.

| Primitive | Recorded prerequisite or conflict role |
| --- | --- |
| Node creation | Introduces a fresh identity with no earlier operation dependency. |
| Edge update | Depends on creation of the source and any new node target, and on the previous update of that same edge. Competing overwrites conflict. |
| Node deletion | Depends on node creation and the necessary edge updates. Incoming references must already have been removed; §6.1.3 also describes dependence on the most recent outgoing updates. Deletion conflicts with concurrent uses/deletions of the node. |

Table 1 enumerates write/write, delete/require and delete/delete cases. Primitive deltas form level zero; transactions group them at higher levels. A group must not introduce an internal conflict or dependency cycle. Semantic dependencies differ from the user's temporal edit order. Append-only version history can branch through undo and subsequent edits without erasing the recorded operations.

Crucially, a valid version is both **dependency-closed** (the paper's left-closure condition in §4.1) and nonconflicting. The operations can then be replayed in a dependency-respecting topological order under the stated primitive semantics. Conflict inheritance is implicit through this closure condition; an operation depending on an excluded conflicting operation cannot simply survive on its own.

§4.3 describes a merge as the union of input operations followed by alternative maximal nonconflicting subsets. Read that shorthand with §4.1's closure requirement. Maximal does not mean a unique intended outcome, maximum cardinality or minimum human effort. The paper does not give a general proof or measured complexity bound for enumerating every alternative. The deployed-code check below explicitly finds dependency checks; it is inappropriate to diagnose a missing-closure implementation bug from the shortened prose alone.

These are write/structural dependencies. Computations that read values require additional dependencies, made explicit by the later S101 correction. A conflict-free S108 graph does not by itself certify interpreter behavior, application invariants or external effects.

## Correspondence and integration obligations

The correspondence graph includes concrete and abstract elements plus links connecting rectangles/states and the information that gives rise to a parent relationship. Parser and renderer transformations consume earlier versions and deltas and produce new versions/deltas. The correspondence records both sides together. When deletion would otherwise violate a correspondence dependency, a context-specific replacement delta adds the required ordering; the original operation remains available in its own model. This supplies S101's later override mechanism without rewriting the original history.

Rendering can require a human layout choice because many concrete representations fit one abstract model. The prototype accepts a choice only when parsing it agrees with the target abstract model. Persisted transformation inputs/outputs allow further edits while a choice is pending. This supports delayed resolution; it does not establish bounded response latency or that the abstract model expresses the user's intended behavior. The described merge strategy propagates participating branches into a common concrete syntax and merges correspondence versions, exposing layout and abstract conflicts together.

Incremental parsers and renderers remain language-specific obligations. The example uses roughly 300 TypeScript lines, described as tedious to author. It temporarily clones concrete, abstract and correspondence graph states, mutates the clones while recording operations, then discards them. The demonstrator also simplifies Figure 4's metamodel: it omits explicit parent-correspondence nodes, intermediate parent-link nodes and type edges. Its success should not be attributed to implementing every illustrated structure unchanged.

The reusable core retains immutable operations and versions but mutable materialized `GraphState`/`NodeState` objects updated by execution and reversal. Immutable history therefore does not mean the entire application is immutable. History retention, transformation work, graph reconstruction and alternative presentation have no comparative time/memory or maintenance-effort measurements here.

## Publication prototype versus currently deployed artifact

The 2023 publication describes a React/D3 single-threaded local demonstrator. Undo/branching and delayed propagation **simulate concurrency**; there is no evaluated multiuser transport, delivery/recovery protocol or server. Serialization of deltas/versions is explicitly not yet implemented. The authors report a working merge function, but no merge/conflict-alternative UI at that checkpoint. Four demonstrations show primitive graphs, concrete syntax, correspondence and two visual syntaxes. They do not constitute a participant study, scalability benchmark or independent correctness test.

The printed [repository](https://msdl.uantwerpen.be/git/jexelmans/onioncollab) and [demo](https://sp2.informatik.uni-ulm.de/onioncollaboration/) remain inaccessible through the attempted web routes. The [author's current page](https://joeri-exelmans.page/) points to the relocated [Onion demo](https://deemz.org/public/onion/). Ordinary HTTPS retrieved its 196-byte HTML shell and its [bundle](https://deemz.org/public/onion/bundle.js): **5,303,026 bytes**, SHA-256 `08042113803134333fe6547c6efb3d729d3becadb6c4dcbb9905dcffca694e96`. The bundle embeds revision `0dd80918bd1eb6d4f75528def1239c0a6cc3d2cb`; this is self-reported build provenance, not an independently recovered repository commit/date.

Static inspection covered the complete bundled `DeltaRegistry` and `Version`/`VersionRegistry` modules (module IDs 5563 and 8752), plus selected surrounding primitive/graph declarations and the revision/navigation strings. The remainder of the bundle, dependencies, full application and tests were not read. Three findings sharpen the reconstruction:

- The deployed `newEdgeUpdate` hash includes the serialized target, as well as overwritten edge, reads and later-read dependencies. The paper's §6.1.1 enumerated example omits the target. That prose omission is **not evidence of a collision defect in this deployed build**; exact 2023 source correspondence is still unavailable.
- `createVersion` checks prerequisite presence and conflicts. The merge traversal skips operations with missing prerequisites and constructs candidates through that checked function. This gives direct bounded implementation evidence for closure, without a proof that all intended maximal alternatives are enumerated or that every application annotation is sound.
- The bundle includes read dependencies, serialization/parsing routines, live-model navigation and merge/history tabs absent or unfinished in the 2023 description. Their presence establishes version drift, not successful operation or a retroactive 2023 implementation claim. No network behavior or serialization correctness was tested.

The code check resolves the immediate interpretation of two core details. Recovering the historical source or validating the current implementation remains a separate artifact task, rather than grounds to hold the complete publication reading open.

## Consequences, leads and evidence disposition

**Established mechanism:** recording dependencies across abstract/concrete/correspondence models can expose conflicts missed by a single-view merge, preserve layout choices and postpone resolution. The demonstrated graph core and explicit assumptions close S101's missing-method reading dependency. They qualify broad novelty claims about automatically reconciling state and source.

**Measured outcome:** none for user effectiveness, comparative latency, memory, integration effort or net maintenance benefit. This is an unresolved empirical outcome, not evidence that the demonstrated mechanism is ineffective. Runtime/state validity, user intent, complete dependency capture, pending work and external effects remain different obligations.

The bibliography supplies specific conditional follow-ups: event-structure foundations (`10.1007/BFb0013026`), earlier operation-based merging (`10.1145/142882.143753`), graph-modification conflict definitions (`10.1007/978-3-642-15928-2_12`), incremental/global consistency (`10.1007/s10270-022-00984-4`), the blended-tool study (`10.1007/s10270-022-01010-3`) and the projectional-editing controlled experiment (`10.1145/2950290.2950315`). These could change formal scope, performance comparisons or the introduction's usability motivation; their primary methods are not credited from this paper's summaries. Search fragments additionally identify conceptual-model historization, model-management practice and a feature/benchmark survey, with full identities/methods unresolved. The 2022 workshop and 2024 presentations/vision work require edition and contribution checks before being counted as separate evidence.

Immediate continuation returns to the unfinished C02 screen and S68 taxonomy, rather than automatically promoting this entire citation neighborhood. **Unique:** generic dependency-aware reconciliation has prior art; Nu/D1 priority is unconfirmed. **Valuable:** useful conflict/provenance capabilities are concrete, with comparative benefit and cost unmeasured. **Scientifically valid:** the literature supplies explicit conditions to test, not validation of ISE equivalence, its oracle or experimental feasibility. All experimental holds remain.
