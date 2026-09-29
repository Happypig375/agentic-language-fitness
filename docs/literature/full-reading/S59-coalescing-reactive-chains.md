# S59 — coalescing reactive chains and evidence lineage

**Full publisher reading completed 2026-09-29.** João Paulo Oliveira Marum, H. Conrad Cunningham, J. Adam Jones and Yi Liu, *Following the Writer’s Path to the Dynamically Coalescing Reactive Chains Design Pattern*, Algorithms 17(2), 56, 2024, [DOI 10.3390/a17020056](https://doi.org/10.3390/a17020056). Zotero `BZY6F54Z`, attachment `WRQUJ9S2`; [publisher PDF](https://mdpi-res.com/d_attachment/algorithms/algorithms-17-00056/article_deploy/algorithms-17-00056.pdf): 39 pages, 1,519,180 bytes, SHA-256 `a32aee1778a4f3924234fe64014ece21083d8e5636fd44879683e53d1cf96860`. All pages, sections 1–15, appendices A/B, seven main figures, two appendix figures and 64 references were read. Renders of pages 5, 10, 11, 14, 15, 17, 29 and 31 cover all figures. No implementation, experiment or author test was executed.

## Contribution and independence

The paper codifies a pattern from the authors' earlier GUI and Unity research using an eleven-step writing method. Its two research questions concern documenting the pattern and following that method. Three of the four authors participated in the earlier cases; adding a reviewer does not create an independent empirical evaluation. The generalized GUI in section 13 is an augmentation/design argument, not a separately implemented benchmark. The work develops material from Marum's 2021 dissertation.

The relevant lineage is [S57](S57-reactive-game-ordering.md), [S58](S58-dependency-graph-reactivity.md), and the GUI paper and addendum now fully read as [S62](S62-gui-dependency-graph.md). These are connected results, not four independent confirmations. S59 contributes a useful account of applicability, forces and implementation decisions. It supplies neither a formal correctness proof nor measured maintenance effort, complexity or user perception. JavaFX and CryEngine generalizations remain prospective.

## Mechanism and applicability

The pattern identifies components whose state changes affect other components, constructs a directed acyclic dependency graph, and coalesces selected updates into directly invoked chains. It rebuilds relevant graph information when the component structure changes. S59 directs a dependency edge from a dependent toward its source; do not silently substitute the opposite edge convention used in another presentation.

Its stated context matters: fair but nondeterministic implicit invocation, a dynamic component hierarchy, an independently operating presentation mechanism, transitional inconsistency, encapsulated state accessible through interfaces, and runtime metadata/reflection. Neither C# nor a game engine alone establishes these conditions. They must be checked in the specific Nu implementation and comparison.

| Decision | Limit that a later design must preserve |
| --- | --- |
| Dependency discovery | References, reflected parameter types and names are clues, not a proof that every runtime instance, event and data dependency is captured. The paper does not establish complete discovery for arbitrary programs. |
| Cycles and exclusions | The DAG requires pruning cycles. A behavior-preserving rule is not fully specified. Unmodifiable framework/third-party components and expensive or delayed relationships may be excluded; their obligations remain part of public behavior. |
| Identity and lifetime | Comparing type and name does not establish correct handling of a replacement instance with the same identifiers. Destruction, replacement and retained references need independent checks. |
| Mutation boundary | The prose varies between checking before updates and after a larger event. Page 22's description revisits controls referenced by the previous graph while also claiming new nodes are handled. The discovery scope and visibility of new objects need an explicit implementation contract. |
| Atomicity | Coalescing callbacks does not itself make rendering atomic or guarantee acceptable latency. The paper acknowledges remaining turbulence from independent display behavior. |
| Cost | Startup construction, recurring checks/rebuilds and extra library/application code remain costs. Hiding code in a wrapper does not remove its maintenance obligations. |

These are specification and evidence limits. No runtime defect in an uninspected implementation is asserted.

## Quantitative claims traced to their source

Page 24 summarizes approximately 55 versus 21 milliseconds startup, half the execution time, five versus one errors per cycle in one scenario, and an average four versus one recovery cycles. Those quantities come from the earlier GUI study and its separate .NET/Rx.NET addendum, not a new S59 experiment. The [S62 reconstruction](S62-gui-dependency-graph.md) now preserves the actual tables, ambiguous error denominators, 50 versus 500 cycle labels, timing-unit discrepancies and unavailable raw trial data. The five-to-one entry applies to one of three scenarios; the other two .NET entries are one-to-one. It is not a universal 80% reduction in error incidence.

Appendix A's broad accuracy statement also cannot replace S58's actual Unity results: all compared implementations had zero visible errors in the reported dynamic scenarios, despite internal errors and recovery differences. S59's repeated claim that Unity supplies no ordering mechanism remains qualified by S58's acknowledged class ordering and the primary Unity documentation already checked in that reading. No new Unity experiment or platform survey is claimed here.

## Bounded platform check

Page 23 describes overriding a control `Update()` and a `form_start()` hook. Microsoft's [.NET Framework 4.8.1 `Control.Update` documentation](https://learn.microsoft.com/en-us/dotnet/api/system.windows.forms.control.update?view=netframework-4.8.1) specifies a nonvirtual repaint method. Its [`Form.Load` documentation](https://learn.microsoft.com/en-us/dotnet/api/system.windows.forms.form.load?view=netframework-4.8.1) describes an event before initial display. A custom handler may be named `form_start`, but the named hook and generic business-update override are not established by those APIs. S62 instead describes implementing a custom interface method. An executable integration must distinguish the library's methods from platform members. This bounded check does not show that the authors' original implementation was broken.

## Three criteria and disposition

**Unique:** dynamic dependency discovery and coalesced component updates have direct GUI/game predecessors; documenting the pattern strengthens that overlap. A narrower Nu comparison remains unconfirmed. **Valuable:** stale state and propagation delays are concrete concerns, but the pattern's tradeoffs and residual errors prevent assuming net maintenance or user benefit. **Scientifically valid:** preserve evidence lineage, platform/event semantics, dependency and lifetime boundaries, rendering versus internal state, adverse cases, and total implementation/runtime cost. No experimental allocation follows.

The incoming Scite graph requested twenty edges and returned none with a low-coverage warning. Exact DOI/title requests used twenty-record pages; the backward title query returned S59, S62, Reactor Design Pattern (`10.18421/tem101-03`) and REFRAME's preprint/publisher identities (`10.2139/ssrn.4534457`, `10.1016/j.softx.2023.101571`). S62 was promoted because it supplies the numerical evidence used here. Reactor and REFRAME remain conditional if an exact framework or pattern comparison becomes necessary; their methods are not credited as fully read. The dissertation and pattern-writing literature remain conditional for details not needed to establish the current evidence distinction. Sparse topology does not establish priority or field completeness.
