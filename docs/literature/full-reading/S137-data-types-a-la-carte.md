# S137 — Selecting datatype components and interpreting effects

**Reading completed 2026-10-01 HKT.** Wouter Swierstra, *Data types à la carte*, Journal of Functional Programming 18(4), 423–436 (2008), [DOI 10.1017/S0956796808006758](https://doi.org/10.1017/S0956796808006758). This resolves the B02/B05 distinction raised by S115's incoming citation: selecting components for a datatype differs from adding cases to a globally open datatype. Its effect examples also inform B03/B07.

## Acquisition and coverage

Zotero parent `WDPKGNBP` was established before body reading. The attempted Utrecht author URL returned HTTP 404; the [Tufts university copy](https://www.cs.tufts.edu/~nr/cs257/archive/wouter-swierstra/DataTypesALaCarte.pdf) supplies the 14-page publisher-formatted paper, 100,281 bytes, SHA-256 `fdb9bdee98efbe21b7dab589a746b7f92edee91f6bd07f14cef2efa0022bd887`. Native attachment `NRSNX3HZ` was uploaded and hash-read-back; note `NHD8B4KN` stores this reconstruction. The publication identifies first online publication on 18 March 2008 and July issue pagination; search-engine crawl ages are not publication dates.

All 14 pages, including all ten references, were read. There are no numbered figures, empirical tables or appendices. Code-heavy PDF pages 5, 6, 8, 10, 11 and 12 were visually checked against extraction. References below use printed pages 423–436. No supplied program, compiler, library or benchmark was executed; the examples and arguments are reconstructed from the paper.

## Datatypes and operations as selectable components

Instead of defining one recursive sum with all constructors, the paper separates a one-layer signature from the recursive knot. A signature for integer constants ignores its recursive argument; a signature for addition contains two recursive positions. A fixed-point wrapper ties those positions back to the entire chosen expression type. A binary coproduct combines signatures. This permits both a value/addition/multiplication language and a value/multiplication language that omits addition.

That selection is the concrete difference from [S115](S115-open-data-functions.md). Components and operations can be reused in several assembled expression types, with the selected signature appearing in the type. S115 instead gives an open datatype the constructors contributed by the whole assembled program. Neither approach automatically converts existing running values, preserves external effects, or establishes a maintenance-time advantage.

For operations, the signature is a functor so recursion can be factored into a fold. Each component supplies an algebra for an operation such as evaluation; the coproduct algebra dispatches to the appropriate component. Adding multiplication therefore supplies a signature, its functor instance, its evaluation algebra and a smart constructor. Existing value/addition definitions are reused. Adding a new operation instead supplies its component instances and composition rule.

The recursive pretty-printer illustrates another important boundary: an operation's one-layer input must permit children drawn from the **whole selected signature**, not only from the current component. A too-specific method type would require an addition's children to be additions as well. The corrected type quantifies the children's signature under the operation constraint. Thus modular recursion is designed explicitly; merely distributing constructor declarations does not obtain it.

Under the supplied instance scheme, evaluating a selected signature needs evaluation instances for its components. This makes missing operation support a type-class obligation. It does not verify the arithmetic or intended semantics of those instances, guarantee termination, or turn every component-local match into a complete behavioral specification. The paper supplies constructions and examples, not a compiler metatheory or arbitrary-program safety proof.

## Injection, matching and composition costs

Raw nested coproduct constructors are cumbersome and depend on the signature's arrangement. The paper hides them behind smart constructors and a two-parameter membership/injection class. Three instance schemes cover identity, injection into the left component, and recursive search down the right side. They require overlapping instances beyond Haskell 98.

The search deliberately does not backtrack into arbitrary nested left components. A component can therefore have a mathematically valid injection into a left-nested sum that these instances do not find. Right-associative, list-like signatures avoid the demonstrated failure. Explicit type signatures select the intended assembled type; the compiler cannot infer a unique choice among all possible supersets from an unconstrained smart-constructor expression.

Repeated component types introduce multiple possible injections. The paper's evaluator is insensitive to that choice because both sides of a coproduct dispatch to the same component algebra. This is a property of that consumer, not a general coherence guarantee for arbitrary operations that inspect coproduct position. It also does not establish compatibility of conflicting instances supplied by independent libraries.

For nested pattern inspection, a partial inverse projects a selected component into `Maybe`. The distributivity example first projects a multiplication and then an addition child, returning no rewrite when the required shape is absent. The paper omits the projection-instance bodies and sketches folding the rewrite through a term. That illustrates selective pattern inspection; it does not establish exhaustive checking of all intended rewrite obligations. No wildcard/default policy or new-case maintenance experiment is conducted.

| Capability | Required machinery | Evidence limit |
| --- | --- | --- |
| Reuse a chosen subset of constructors | Signature functors, fixed point and coproducts | Demonstrated source construction, no adoption or effort measurement |
| Add operations and constructors | Component classes/instances and composition rules | Correct behavior still depends on the provided implementations |
| Hide coproduct injections | Smart constructors, annotations and overlapping membership instances | Restricted search shape and overlapping-instance assumptions remain |
| Inspect nested shapes | Partial projection and explicit failure handling | Missing instance details; no complete pattern-analysis result |
| Generalize to richer datatypes | Bifunctors for polymorphic types; higher-order encodings for GADTs/nesting | Discussion only, with acknowledged complexity and extra language extensions |

The paper acknowledges upfront boilerplate and extra representation layers but provides no timings, allocation measurements, user study, task sample or compilation benchmark. Claims of low overhead or practical ease must be checked in later methods; absence of such measurements here is not evidence of no benefit.

## Effect descriptions and their interpreters

The second construction separates a pure result from one suspended operation whose children continue the computation. With a functor signature, this is a free monad. Coproducts of signatures therefore combine these free-monad descriptions. The paper explicitly restricts this argument: it is not a generic recipe for composing arbitrary monads. The state and list monads are named counterexamples to being free monads of this form.

The calculator example describes memory operations as syntax, then interprets them into a state transformation. Increment stores a value and continuation; recall stores a function from the recalled integer to the continuation. A fold chooses the interpretation. The printed tick example returns the old memory value and the incremented state. Under the supplied interpreter, recall-only syntax does not change the memory; increment-only syntax cannot choose its **returned value** from the initial memory, although its final memory still depends on the initial value. Preserve that result/state distinction.

The I/O example similarly distinguishes teletype operations from filesystem operations. A type selecting only teletype syntax cannot directly request the filesystem constructors; the supplied interpreter maps teletype constructors to their matching primitives. This is a useful capability boundary. It relies on the interpretation assigned to those constructors. A signature containing a filesystem component can allow both reading and writing even when a particular program only reads, so the type identifies permitted operation categories rather than an exact execution trace. Filesystem and coproduct interpreter instances are omitted from the article.

Pure descriptions permit additional interpretations and reasoning, but they do not restore the external world when interpreted twice. Moreover, some operation nodes contain Haskell functions as continuations. From that representation, it does not follow that arbitrary terms can be serialized or every future branch enumerated. These are transfer limits derived from the shown representation, not measured failures of a replay system. The cited *Beauty in the beast* supplies a concrete follow-up for functional models of I/O, state and concurrency; its body remains unread.

## Benefit, novelty and next evidence

**Unique:** unconfirmed for the ISE question. Component selection, modular folds, extensible operations and pure effect descriptions are longstanding mechanisms. The author explicitly builds on fixed points, modular interpreters and free-monad foundations. This does not establish Nu-specific equivalence or agent-maintenance priority.

**Valuable:** the source-level capability is concrete: the same components support different assembled datatypes and interpreters. Annotation, instance and representation costs remain. No practical net benefit is measured in this paper.

**Scientifically valid:** the construction and its membership, polymorphism and effect-interpretation assumptions are reconstructed. No full implementation certification, arbitrary-monad composition theorem, measured runtime result or behavioral-maintenance effect is claimed by this pass.

The [composition screen](../nu-background-composition-screen-2026-10-01.md) distinguishes 287 indexed incoming DOI nodes, duplicate/edition routes, title-only exclusions and targeted metadata reading. The first 200-edge graph was truncated; expansion to 1,000 returned 287 edges without truncation. This resolves that retrieval cap, not field completeness. Eleven unchanged S115 decisions are reused, not reported as new screening. No new theme is closed.

Two earlier C02 leads now become concrete cost dependencies: **S138**, *Compositional data types*, and **S139**, *A Lightweight Optimization Technique for Data Types à la Carte*. Both have verified Zotero records/PDFs before further reading; bodies remain unread at this checkpoint. Reconstruct their machinery, workloads, compiler assumptions and outcomes before transferring performance claims. S118 pattern views, S116 practice, EML's modular checks, and the wider Join Token/persistence/oracle frontiers remain active. All experimental holds remain.
