# S57 — dependency-ordered game updates

**Full reading completed 2026-09-29.** Marum, Jones and Cunningham, *Towards a Reactive Game Engine*, IEEE SoutheastCon 2019, [DOI 10.1109/SoutheastCon42311.2019.9020527](https://doi.org/10.1109/SoutheastCon42311.2019.9020527). Zotero parent `T84F55VT`; the newly present publisher PDF `YVRZBRXR` has eight pages, 165,785 bytes and SHA-256 `45c92b927be4dc91aaec452c321a36d0952b70d24b2e18537711e58e19a1d441`. This is an existing library attachment, not a successful download by this session. Its identity, bytes and parent were checked through the native local API.

All eight pages, sections I–VII, figures 1–3, algorithms 1–2 and 36 references were consumed. Page renders 2, 3, 4 and 6 resolved the visual/pseudocode gaps in the [earlier partial reconstruction](../S57-S58-reactive-game-ordering-reading-2026-09-29.md); that note also records the initially partial S58 extension. Column-interleaved sorted extraction was checked against ordinary extraction and page images. Full publication coverage does not mean implementation verification or experimental reproduction. No author code or experiment was executed.

## Evidence and its limits

The paper reorganizes C# component updates in Unity3D rather than comparing functional and imperative languages. Selected scripts implement `IUpdatable.FakeUpdate`; component references determine dependency order, with cycles excluded. Unity/.NET internals and other scripts remain outside this mechanism. Figures 1–2 illustrate value propagation and a permissible update order, not a proof of complete dependency capture.

Expression-tree changes and a small shooting example motivate behavioral checks. The 2019 results report residual miscalculations, including 15% for the proposed framework, without a complete trial denominator, quantitative timing distribution or a developer study. Default Unity and the authors' UniRx implementation are the comparisons. Figure 3's two expressions give expected values −4 and 16, but the released paper does not supply a complete executable oracle or benchmark.

The rendered algorithms both say `while Q is empty` after enqueuing a root; Algorithm 2 also inserts `C1` in a branch where it is null. These are confirmed presentation problems, not demonstrated failures of the authors' implementation. They preclude treating the printed listings as validated executable specifications. The later S58 body changes the loop condition and callback name, so editions must remain separate.

## Implications for Nu

**Unique:** unconfirmed for a specific Nu mechanism. Dynamic update ordering and reactive game coordination have direct predecessors. The distinction worth testing must identify what Nu adds beyond explicit scheduling and dependency capture.

**Valuable:** internal consistency and recovery after structural changes are concrete outcomes; perceived smoothness, maintenance effort and coding-agent success remain unmeasured here. The study supplies motivation and a rival mechanism, not an expected Nu effect size.

**Scientifically valid:** use common old/new obligations, prospective behavior at transition boundaries and credible configured alternatives. Record all attempts and transient failures; distinguish internal inconsistency, externally visible failure and recovery. Independently validate cycles, undeclared dependencies and external-engine effects instead of importing an introductory guarantee. ALF's equivalence, oracle, task diversity and accounting remain unvalidated; allocation is zero.

[S58's extension](S58-dependency-graph-reactivity.md) subsequently received full publication coverage, with its distinct results and baseline limits preserved. S59's generalized pattern is acquired and queued. Earlier VR/FRP and GUI references remain conditional on claiming their exact guarantees; broad reactive-game firstness is already unavailable without reading every historical application. The source-decision ledger records the citation graph's sparse coverage and these follow-up choices.
