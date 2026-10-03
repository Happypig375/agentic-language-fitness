# S87 — Document computation through edit histories

**Complete publisher-paper reading, 2026-10-03.** Tomas Petricek and Jonathan Edwards, *Denicek: Computational Substrate for Document-Oriented End-User Programming*, UIST 2025, article 32, 19 pages, DOI **[10.1145/3746059.3747646](https://doi.org/10.1145/3746059.3747646)**. The verified author order corrects the earlier Scite record listing Edwards alone. Existing native parent **`7F8LQHG9`**, note **`YA7GX6TT`** and user-library PDF **`46RWCE8V`** precede this reading; three collection memberships including `PKLXQNEE` are preserved.

## Source and coverage

The supplied publisher PDF is **3,805,371 bytes**, SHA-256 **`274800c5d8da5f2f770c4e9dc2120e57621e8a73645fa45b532ed84b5bf60efd`**, MD5 **`8c587e95cbe63ef99f1af86c3aff2545`**. All **19 text/visual pages**, nine main sections, **18 figures**, 115 references and **Appendices A and B.1–B.2** are read. Several figures are specification tables or edit listings; there is no separate numbered experimental-results table. Natural column extraction and rendered pages resolve interleaved text and symbols. The figures show demonstrated scenarios, not observations from recruited participants.

The earlier separately acquired author PDF remains a different 19-page edition: 2,740,738 bytes, SHA-256 `108bfa006a318bf1c1ce70a0074ea654b25fcb4c241627198ebdfe1f0616bf9a`. Prior automated text/first-page comparisons identify extraction, affiliation and layout differences; this pass does not claim complete scientific or visual equivalence. The publisher reference [27] retains a placeholder DOI for S73; the already verified S73 identity governs that lineage. Reference [67] reverses Orion Henry's name; S102's own author line governs.

The [author page](https://tomasp.net/academic/papers/denicek/) verifies authorship, UIST identity and source links. Its ACM supplementary-video route returns403. The linked talk/teaser/slides and supplementary videos are not acquired or reviewed in this segment. Paper coverage remains complete; multimedia coverage and reproduction remain separate.

Bounded static inspection uses the latest repository commit before the publication date, **`fb1a90efae7969154e9ff9a973eb3e851a21d44b`**, dated **16 September 2025**, message “Add minimal sample data files.” Its full tree has **76 entries**, without truncation. This date-bounded choice is not certification of the exact submission/demo artifact. The current head **`9118864c064230c3935f3390ea5b75e32f234a14`**, dated 13 September 2026, has 102 entries; its changed implementation is not substituted for the historical pin.

**Eleven complete files, 2,118 lines**, three bounded ranges and the demo file's top-level definition inventory are read. Source identities/coverage appear below. No compiler, package installation, test suite, browser demo, notebook, model or author program is run.

## The represented program and its operations

Denicek represents a program as a **linear sequence of document edits**. Applying the history reconstructs a tree containing data, formulas, results and content. Tagged records have named fields; tagged lists have explicitly identified, ordered elements; primitive nodes contain strings/numbers; reference nodes contain absolute or relative selectors. List “indices” are stable identifiers, not changing ordinal positions. An `All` selector addresses list elements; there is no equivalent wildcard over arbitrary record fields.

The document language is **dynamically typed**, despite the substrate being implemented in F#. Homogeneous lists are an assumption, temporarily violated while constructing items, rather than a statically enforced invariant. Structural edits can update references; the same operations can instead keep references unchanged when used as value edits. A target containing a specific list index cannot request structural reference updating. Transactions that restore invariants after a batch are discussed as an alternative, not a demonstrated static guarantee.

| Primitive | Actual contract and policy |
| --- | --- |
| Apply | Locate a target and perform a supported edit. Structural rename/wrap updates matching references. Wrapping a scalar as a list inserts an `All` selector into affected references. Structural deletion or copying that would leave ambiguous/invalid references is rejected under the stated mode. |
| Merge | Rebase one divergent suffix onto the other after their shared history. Rewrite selectors to reflect earlier structural edits; generate focused extra edits so transformations also reach newly added/copied nodes. The operation is asymmetric when changes conflict. |
| Detect/remove conflicts | Compare edit effects and dependencies over overlapping selector paths. Removing an edit propagates removal to later dependent edits. Reporting, ignoring or removing conflicts are different application decisions. |

Appendix B reconstructs the two parts of merging. `Add`, `Append` and `Copy` can introduce nodes that were absent when an earlier wildcard edit occurred; the merger specializes that earlier edit to the new identifiers. Rename/wrap updates target, copy-source and embedded references. Structural copying can duplicate later changes so they affect both the original and the copy. This is the mechanism behind a recorded “add speaker” action continuing to work after the speaker list becomes a table; the application author still supplies the list-to-table and string-splitting edits.

The substrate deliberately makes edit interpretation independent of the current document value. Conditional selectors or edits would violate that premise. Higher layers inspect the current document and expand a conditional action into ordinary edits. Consequently, an item later introduced through merging need not receive an earlier conditionally expanded action. This is a stated scope boundary, not general concurrent intent preservation.

## Computation, dependencies and replay

Webnicek is the prototype environment co-designed with the substrate. It implements six programming experiences by composing the primitives:

- **Collaboration:** users coordinate rebasing of complete histories. Denicek converges document variants into one structure; it does not let users retain different schemas while importing selected data edits. Selective adoption would require a further retract operation. The conference demonstration can reach the same document through two merge orders while keeping different histories.
- **Programming by demonstration and UI actions:** selected edits and their history hash are stored as document nodes. Replaying them branches from their original base, then merges through later changes. Saved edits/hashes themselves require updating after a merge. Generalizing an action or selecting a condition is manual in Webnicek; automatic inference is suggested future work there.
- **Formula evaluation:** formulas are tagged nodes. Evaluation produces transient edits wrapping the original formula and adding its result. Reference evaluation records source dependencies; builtin evaluation records further dependencies. Formula language and builtin semantics remain an additional implementation layer.
- **Incremental recomputation:** evaluated edits stay at the end of ordinary history. New source edits push through them; conflicts remove affected results and dependent results. Webnicek requires explicit evaluation rather than automatically recomputing all formulas. Invalidation and recomputation are separate actions.
- **Schema/code evolution:** represented references are rewritten when the document structure changes. This updates a formula's path from a list to its wrapped table body. It cannot rewrite arbitrary formula logic that relies on an implicit string format, such as splitting a speaker's name/email at a comma.
- **Debugging and concrete reuse:** retained formula subtrees supply a provenance trace and input highlighting. Copying formulas and later merging a correction from before the copy can update their descendants. The user explicitly manipulates history; no general correctness oracle or automatic explanation-quality result follows.

The paper's §8.2 explicitly says the substrate is **unsuitable for live systems that preserve evaluation state during source-code editing**. The counter example retains increments as constructed formulas and re-evaluates them; this differs from migrating an arbitrary suspended program, stack, event queue or external resource. That distinction is material when comparing Nu's state/history claims with notebook liveness.

## What the evaluation establishes

The design uses **six formative examples**: Counter, Todo, Conference List, Conference Budget, Hello World and Traffic Accidents. They guide development of both Denicek and Webnicek. They are design cases, not six independent evaluations or participant samples.

The authors then build **Datnicek**, a notebook combining code/Markdown cells and interactive grid editing. Its requirements draw on other systems: structure editing, collaboration, contextual completion, invalidation, data-cleaning demonstrations and conversion of transformations into code. A Eurostat example demonstrates loading, cleaning and plotting data. All persistent notebook changes become edits; transient UI state remains outside that history. Grid transformations retain both a sequence of edits and a formula, which the paper identifies as duplication worth removing.

The authors report that uniform primitives let them implement many requirements with little effort and quickly try designs. This is useful primary **qualitative implementation evidence**, supported by the actual prototype and mechanisms. It is not a measured reduction in developer hours, source size, defects or maintenance cost against a separately implemented control. The second system was started after initial substrate design, but shares its designers and deliberately aligned representation; development also uncovered conflict/dependency limitations and prompted optimizations. It is not independent adoption or a frozen-substrate replication.

The complementary evaluation applies Olsen's system criteria and the Technical Dimensions of Programming Systems framework. It argues for expressive fit, composability and flexibility while explicitly leaving empowerment of new participants and scalability unresolved. It is an author-applied heuristic assessment, not a user study or an independent review.

Preserve the reported difficulties:

1. The conflict analysis over-approximates. Even the illustrative two-order conference merge is reported as conflicting although both outcomes agree. Datnicek lacks a suitable conflict-resolution UI; changing two independent method calls can still conflict.
2. Computed results depend on both structure and values. Datnicek development exposed the inadequacy of checking only equal effect kinds; a formally tractable model and correctness proof are future work.
3. Despite some optimizations, the notebook becomes cumbersome with multiple thousands of rows. No calibrated timing, memory/frame distribution or scalability benchmark is supplied.
4. Pointer-based editing, manual generalization/history operations and integration with existing software stacks remain burdens. The systems are not self-sustaining; formula evaluators are not defined from within them.

These limitations qualify the positive capability and author-experience results. They do not establish that the substrate has no benefit or that Nu has a benefit.

## What the pinned source adds

The source confirms the document/edit representation, reference modes, rebase transformations and distinct source/evaluated histories. More specific boundaries matter:

- `merge.fs`389–423 defines effect paths, then **comments out the effect-kind equality check**. The inspected predicate conflicts on overlapping paths regardless of kind. This is broader than §4.2's same-kind rule and consistent with §7.3's later dependency discussion. Add/append effects also target the particular added field/identifier. Do not treat the earlier prose as a complete description of this pin.
- `eval.fs`123–138 records reference and top-level-formula dependencies. A comment explains that finer argument-level dependencies did not work, so the implementation uses the entire top-level formula as an over-approximation. `updateEvaluatedEdits` pushes the new suffix through evaluated edits with `RemoveConflicting`; it does not itself recompute them.
- `webnicek.fs`471–537 uses **`IgnoreConflicts`** for ordinary history merging, then fixes saved interaction hashes/edits and separately invalidates results. This is not an automatic user-conflict-resolution interface. `datnicek.fs`394–611 retains separate source/grid/evaluated histories and implements conditional expansion at the application layer.
- `apply.fs` rejects prohibited reference-changing edits, while its value-edit modes permit temporarily inconsistent structure. Several nonmatching edits have no effect; supported operations, shape assumptions and runtime exceptions remain part of the contract.
- `ordlist.fs` stores members and ordering separately, using maps and a lazy order tree. Explicit identity and predecessor/successor information support the claimed ordering mechanism. This static design does not supply a measured memory or merge-cost result.
- History bookkeeping uses F#'s integer `hash`; `mergeHistories` obtains a common prefix through edit-list comparison, while saved-interaction lookup uses accumulated hashes. “Git-like” does not establish cryptographic identity or collision-free distributed history.
- The complete 416-line test file contains concrete merge/reference/invalidation assertions, frequently using `IgnoreConflicts`. It also retains old call shapes: four-component add/append constructors versus five components in the inspected core, and evaluator calls missing the new builtin argument. The test project directly includes those core files. These are static correspondence limits; no build or failed test is reported. A test file's presence cannot certify this historical snapshot.
- `matcher.fs` is a wholly commented experiment after its module declaration. It is not evidence that an additional matching system is implemented. Package/build metadata targets Fable/JavaScript with a `netstandard2.0` project; this is not a Nu/.NET game runtime benchmark.

The report's formulation, its development reflections and the inspected snapshot therefore retain separate scopes. Later repository code, the exact demo session, all other source files and the multimedia supplements remain outside this bounded inspection.

## Evidence disposition and next action

S87 is a concrete predecessor for combining explicit editable history, reference-aware structural evolution, replayed interactions and dependency invalidation. It narrows generic novelty claims about unifying these capabilities. It supplies qualitative construction evidence and useful tradeoffs; it does not identify a causal F#/C# benefit, a fixed-agent convention effect, arbitrary live-state preservation or net user maintenance savings.

The S73 challenges and S86 operation-based evolution share authors and concepts with S87. Reuse their reconstructed methods to compare **convergence**, **divergence**, compensation and retained history; do not pool these as independent validation. S102's differently versioned document views and S103/S236's writable relational schemas solve related problems under different policies.

The strongest next independent frontier is **modern .NET/game cost and integration evidence** in B06/B07/B10: resume focused primary discovery from the retained C06/C07 routes, targeting allocation/retained history, latency and actual change/adoption work. Broad ECS pages previously returned substantial application noise, so refine by runtime and workload rather than merely taking the next broad page. A missing Nu-specific comparative measurement remains an empirical residual; discovery must resolve actual literature coverage, not promise to infer that measurement. Grove/typed editors and formula correctness are conditional method dependencies if a stronger convergence/type claim is proposed. All construction, compiler/model/worker and experimental holds remain.

## Source identities

All bodies and extracted/rendered material remain in ignored local storage. The following files are at the September 2025 pin; whole-file hashes do not upgrade a bounded range to a complete reading.

| Pinned file | Bytes /lines /coverage | SHA-256 |
| --- | --- | --- |
| [src/doc/doc.fs](https://raw.githubusercontent.com/d3sprog/denicek/fb1a90efae7969154e9ff9a973eb3e851a21d44b/src/doc/doc.fs) | 17126 /397 /complete | `3a4d4a96f41e720e21089cc89d2afae1b3e0847009766c079e32f394dfa83fe4` |
| [src/doc/apply.fs](https://raw.githubusercontent.com/d3sprog/denicek/fb1a90efae7969154e9ff9a973eb3e851a21d44b/src/doc/apply.fs) | 10248 /198 /complete | `c66893277463d396f0392def220b1c54ef4e98da6feb13eba72489b2c7770b52` |
| [src/doc/merge.fs](https://raw.githubusercontent.com/d3sprog/denicek/fb1a90efae7969154e9ff9a973eb3e851a21d44b/src/doc/merge.fs) | 21742 /504 /complete | `85258931528c91d540c597d726be23f2f5477803a2f152b582e4f385fabffa7e` |
| [src/eval.fs](https://raw.githubusercontent.com/d3sprog/denicek/fb1a90efae7969154e9ff9a973eb3e851a21d44b/src/eval.fs) | 8184 /179 /complete | `91e48dee4e79d2d6b623f615bbaa08d9c857cd4d7590489c15dc1500767b4f7e` |
| [src/matcher.fs](https://raw.githubusercontent.com/d3sprog/denicek/fb1a90efae7969154e9ff9a973eb3e851a21d44b/src/matcher.fs) | 2077 /55 /complete | `399ffec9a66d0e52012e34e0f116a2a8c923ad4ddff0301afccc14e9b814f9f9` |
| [src/utils/ordlist.fs](https://raw.githubusercontent.com/d3sprog/denicek/fb1a90efae7969154e9ff9a973eb3e851a21d44b/src/utils/ordlist.fs) | 5023 /145 /complete | `18df7c736e14af8de475ab8fcb053a2d8b6a5bfdfd74fd96daba242a715da668` |
| [src/represent.fs](https://raw.githubusercontent.com/d3sprog/denicek/fb1a90efae7969154e9ff9a973eb3e851a21d44b/src/represent.fs) | 6985 /135 /complete | `5b634550e6bb2c16c1b29ed57db0313ce04043eceac880dd46ac42d75f8a9340` |
| [src/webnicek.fs](https://raw.githubusercontent.com/d3sprog/denicek/fb1a90efae7969154e9ff9a973eb3e851a21d44b/src/webnicek.fs) | 85388 /1606 /444–566 /1606; other matching locator lines only | `20859755d97261de45c128dcd605cccc5ee0a9f1ef6eef861292f5e4756dc155` |
| [src/datnicek.fs](https://raw.githubusercontent.com/d3sprog/denicek/fb1a90efae7969154e9ff9a973eb3e851a21d44b/src/datnicek.fs) | 211176 /1626 /394–611 /1626; other matching locator lines only | `cba2b588bd559ee52393a733a62864b6bd1fec68627d07baf990ba7967b11ffa` |
| [src/app.fsproj](https://raw.githubusercontent.com/d3sprog/denicek/fb1a90efae7969154e9ff9a973eb3e851a21d44b/src/app.fsproj) | 1013 /28 /complete | `b5f90a6fdc3c9e28ce70aee84dd2a85abf76cafed3379cb854b72531cfaf1280` |
| [tests/denicek.fs](https://raw.githubusercontent.com/d3sprog/denicek/fb1a90efae7969154e9ff9a973eb3e851a21d44b/tests/denicek.fs) | 19192 /416 /complete | `dc15ea548e74553234733cda2ce1f541962b939b62c9262b8c5227ff47da0c7d` |
| [package.json](https://raw.githubusercontent.com/d3sprog/denicek/fb1a90efae7969154e9ff9a973eb3e851a21d44b/package.json) | 500 /19 /complete | `33bab9779cbeceecc758aa6d8e24706fa96d2f31daf674a9a98bcd24a20bf97f` |
| [src/demos.fs](https://raw.githubusercontent.com/d3sprog/denicek/fb1a90efae7969154e9ff9a973eb3e851a21d44b/src/demos.fs) | 12103 /293 /1–70 /293 plus top-level definition inventory | `ab57880a5879c7d2e019646c3e58570dbfef4caef938c067420bea15a507253b` |
| [tests/tests.fsproj](https://raw.githubusercontent.com/d3sprog/denicek/fb1a90efae7969154e9ff9a973eb3e851a21d44b/tests/tests.fsproj) | 1287 /42 /complete | `2934dcef06df2bab366d6ae5f51a90e1da4e69bcfcd5a20cfc54ff106e43c66a` |
