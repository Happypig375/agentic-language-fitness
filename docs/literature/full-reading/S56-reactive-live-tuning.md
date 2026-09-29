# S56 - From reactive debugging to live tuning

**Full reading completed 2026-09-29.** Ragnar Mogk, Pascal Weisenburger, Julian Haas, David Richter, Guido Salvaneschi and Mira Mezini, *From Debugging Towards Live Tuning of Reactive Applications*, LIVE 2018. All six pages, sections 1-7, 21 references and figures 1-3 were read. MuPDF renders of pages 2-4 verified the dashboard listing and two debugger screenshots. The [author-hosted PDF](https://www.rescala-lang.com/assets/pdf/2018%20Debugging%20towards%20Tuning.pdf) is 558,338 bytes, SHA-256 `db56e8eadf7b14032808fc4c4355649fb291546123a1197ae0163b6b1e0ed0b0`. The workshop's [program](https://liveprog.org/all-programs.html) identifies the same six-author paper. A related SPLASH poster listing is not an independent experiment. No DOI was verified or invented; exact-title Scite retrieval requested 20 records at offset 0 and returned zero. Reader: the main Codex session, not independent human review.

Zotero parent `QS8SC5ZE`, stored PDF `6LHFCP35`, completion note `5FE3BDQ5`; parent/title, topical memberships and stored PDF hash were independently verified through the local API.

## What is actually demonstrated

This is a design and early-experience workshop paper extending Reactive Inspector. It presents a REScala sensor dashboard: incoming temperatures are filtered, recent values retained, and an aggregation function and display selection may change. Figure 2 shows a Chrome debugger extension, whereas S43's evaluated implementation was an Eclipse plugin. The 2016 experiment cannot be relabeled as a test of this later live-tuning implementation.

Sections 3-4 distinguish three operations:

- **Inspect history:** visualize recorded graph states while the application continues and new events are recorded. This neither pauses nor restores the application.
- **Modify current values:** inject inputs through normal reactive propagation, or force changes to intermediate nodes for developer investigation. The latter can intentionally make displayed aggregates inconsistent with their underlying history.
- **Restore a snapshot and explore:** reinstate a prior graph state, change values and follow an alternative execution. The text explicitly leaves avoidance of resulting inconsistencies to the developer; it does not establish reversal of arbitrary external effects.

Propagation consistency is consequently narrower than satisfaction of all application requirements. Type-correct changes also need not preserve domain constraints. This distinction follows directly from the forced-average example and the stated restoration responsibility, rather than from a reproduced failure.

Section 5 proposes a spectrum of tuning controls for domain experts: typed input widgets, developer-supplied finite choices of behavior, restricted reconnection of dataflow nodes, and developer-defined domain languages. Direct visual rewiring is described as planned work. Developers must choose the permitted modifications and connect them to the graph; the runtime does not infer valid application behavior from a type alone. These are relevant precedents for a bounded editor/reload capability, not a guarantee that arbitrary code changes can be accepted safely.

## Evidence limits and Nu implications

There is no controlled user comparison, task denominator, error-rate measurement, net-cost estimate or formal correctness proof for the proposed tuning framework. The paper describes a planned live demonstration. The video and running extension were not inspected, and no code was installed, built or executed. Its screenshots and examples support the architectural account at that scope. Earlier comprehension and debugger papers cited in the introduction are prior evidence, not new evaluation of tuning.

The snapshot implementation is attributed to *Fault-tolerant Distributed Reactive Programming*, reference 17, DOI [10.4230/LIPIcs.ECOOP.2018.1](https://doi.org/10.4230/LIPIcs.ECOOP.2018.1). That primary method remains a conditional follow-up if Nu's distinction depends on snapshot cost or consistency under failures. Other cited predecessors include Tardis, Elm's debugger, object-centric debugging, live tuning and RxFiddle. Their bibliographic presence establishes a follow-up route, not full reading or a transferable performance result.

**Unique:** reactive graph inspection, runtime value changes and snapshot-based exploration precede the proposed Nu formalization. Missing Scite indexing is not a novelty result. **Valuable:** developer-controlled tuning may be useful, but this paper measures neither Nu's benefit nor the cost of defining and preserving tuning boundaries. **Scientifically valid:** keep observation, replay/restoration and code modification as separate claims. Any later temporal oracle must cover the chosen state/effect boundary and domain obligations; compile/type acceptance and graph propagation cannot substitute for it. D1's existing complete-behavior endpoint remains appropriate. No experimental allocation changes.
