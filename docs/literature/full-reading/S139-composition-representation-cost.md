# S139 — Flattened datatype composition and residual runtime cost

**Reading completed 2026-10-01 HKT.** Hirotada Kiriyama, Tomoyuki Aotani and Hidehiko Masuhara, *A Lightweight Optimization Technique for Data Types à la Carte*, MODULARITY Companion / LaMOD 2016, pp. 86–90, [DOI 10.1145/2892664.2892677](https://doi.org/10.1145/2892664.2892677). This addresses B05/B06: S137 establishes selectable composition but leaves representation costs unmeasured. S139 reports a concrete optimization and compares it with both nested composition and a plain algebraic datatype.

## Acquisition and actual coverage

Existing Zotero parent `XSKN5NCY` preceded body reading. The [author PDF](https://prg.is.titech.ac.jp/papers/pdf/lamod2016-alacarte.pdf), attachment `HEU9M6VB`, has five pages, 151,969 bytes, SHA-256 `c2286e3e60e630ce224a759a003997ff8594c729d53340eb9557f7cc7f7f99a5`. The native API confirmed the parent identity and attachment bytes. All five pages, nine figures and six references were read; every figure was visually checked. Figure 8 contains two plots; there are no result tables or appendices. Note `5XWG2Q6L` stores this reconstruction.

No author code, benchmark or compiler was run. The paper and primary author bibliography supply no located implementation/raw-data link. The bibliography redirects to the lab's `prg.comp.isct.ac.jp` domain and still identifies the same paper. Targeted web searches and a public GitHub code search for `compType` in Haskell found no source artifact; GitHub returned zero results with `incomplete_results:false`. This is an **unlocated artifact**, not proof that none exists or an access-denied claim.

## Mechanism and required integration

S137's list-like sum of signature functors uses nested left/right constructors. Inspecting a constructor may traverse several wrapper layers; adding components can increase indirection, allocations and algebra dispatches. S139 flattens the selected sum into one new signature functor with a distinct constructor corresponding to each original constructor. It retains the recursive fixed-point wrapper, so the existing polymorphic fold/evaluator interface still applies.

The compile-time generator takes names for the generated signature, the selected sum and the requested algebra classes. It generates the flat datatype, injections from each original component, and operation instances that translate a flat constructor into its original component constructor and delegate to the original algebra. Smart constructors keep using component membership constraints. A consumer chooses the flat representation by changing its concrete type annotation. Thus constructor and operation definitions can remain modular while a selected configuration has a closed flat representation.

This is a concrete optimization opportunity, with explicit assumptions. Reusable functions must remain polymorphic in the signature and use the provided component constraints; code that depends directly on coproduct order or a concrete representation is outside that unchanged-source argument. A changed configuration needs generated declarations and a new concrete type choice. The article demonstrates the algebra-function pattern, not a fully specified transformation for arbitrary type classes, GADTs, effects or every projection operation. No live-value migration or dynamic extension protocol is given.

The intended correspondence is clear for the example: each flat constructor carries the same fields and delegates to the same component algebra. The paper provides this construction rather than a machine-checked semantic-preservation proof. Its reported constant cost concerns removal of composition-depth overhead per dispatch, not constant time to evaluate an entire tree or constant cost for every possible operation.

## Evaluation reconstructed

| Design element | What the article actually reports |
| --- | --- |
| Workload | One family of arithmetic-expression evaluators over perfect binary trees of height 20 |
| Variation | Number of composed constructor/functor alternatives; displayed horizontal axis spans 0–100 |
| Semantics | One integer-literal component and many distinct binary-addition components with the same addition behavior |
| Treatments | Linear DTC, balanced DTC, generated flat `compType`, and a non-DTC algebraic datatype |
| Environment | Linux kernel 4.0.1; Intel Core i7 3.3 GHz; 32 GB RAM; GHC 7.10.1 with `-O2`; Criterion, reference version 1.1.0 |
| Endpoint | Mean evaluation time and time normalized by the plain datatype; no reported compilation, edit, allocation or GC measurements |
| Missing detail | Raw observations, exact source revision, random seeds, sample counts, uncertainty intervals, Criterion forcing/setup details and exact constructor-count schedule |

The height/base-case sketch implies 2^20 leaves and 2^21−1 total nodes if height counts edges to a leaf; all leaves are one and all internal operators add, giving an expected result of 2^20. These are deductions from the printed construction, not recovered benchmark logs. The many added constructor names stress representation depth while preserving the same arithmetic, rather than sampling diverse new behavioral requirements.

Figure 8a shows the important positive result: linear DTC time grows strongly with the number of alternatives, whereas the generated representation and plain datatype stay approximately flat over the displayed range. The linear curve approaches roughly 1.25 seconds near the right end; the flat curves are only a few hundredths of a second. These are plot readings, not raw-data estimates or independent reruns.

Figure 8b prevents equating flat scaling with zero overhead. The optimized red curve is near the plain datatype initially, then roughly **1.3–1.5 times its time** over much of the remaining range. Balanced DTC is roughly **2–4 times** the plain datatype, with visible steps. The baseline is normalized to one. Thus the plot supports a substantial benefit relative to both composition alternatives and residual overhead relative to a plain datatype. It does not establish statistical equivalence or universal equal efficiency. No exact speedup confidence interval is available.

The paper attributes costs to allocation/GC as well as extra dispatch. Those mechanisms are plausible from the representation, but the reported endpoint does not separate their contributions. Compilation work, generated code size, rebuild latency, developer effort and retained live-state behavior remain unmeasured. Finite curves alone do not prove an asymptotic bound across arbitrary compiler versions or workloads.

## Printed-code and artifact limits

The article's illustrative code cannot substitute for the executed experiment. Two material checks locate the boundary:

- The `exp2` source is an addition of `exp1` and its negation. Expanding the shown expression gives eight semantic nodes; one sum-wrapper dispatch per node makes sixteen algebra applications before optimization. The accompanying prose instead contrasts sixteen with six plain-evaluator calls. Six matches the earlier, different expression using a literal five. This is an example/count inconsistency, not a measured runtime discrepancy.
- Figure 9 selects `k` from `(0,len)` and indexes a list whose length is `len`. The [standard random-1.1 API](https://hackage.haskell.org/package/random-1.1/docs/System-Random.html) defines integer range endpoints inclusively and `randomRIO` through that range operation. Used literally, the printed upper endpoint permits an out-of-bounds list index. The actual benchmark's random-library version/source is not supplied. The figure is also schematic in its datatype families and generator invocation; no claim is made that the authors ran this exact snippet.

Minor identifier/prime and generator-arity differences also prevent treating the printed fragments as a released build. None of these observations demonstrates that the plotted measurements were fabricated or that the executed implementation had the same errors. They identify why the source and raw dataset are needed for reproduction. No local corrective implementation or substitute experiment was constructed.

## Implication for the survey

**Unique:** unconfirmed for the ISE proposal. Modular datatype construction and representation optimization have established predecessors; S139 itself credits worker/wrapper ideas. A Nu/F# mechanism cannot be declared new from the absence of a matching phrase in a sparse graph.

**Valuable:** a useful cost tradeoff is measured under a stated synthetic workload. The generated representation greatly improves scaling relative to linear DTC and improves over balanced DTC, while retaining overhead over the closed baseline in much of the plot. This supports preserving a credible closed-representation comparator. It supplies no maintenance or interactive-development effect estimate.

**Scientifically valid:** construction, workload and both plots are reconstructed, including the favorable trend and adverse residual cost. Source/data correspondence, forcing policy, uncertainty and wider workload transfer remain unresolved. Reported evidence is not an independent replication.

G13 finds only one incoming DOI, `10.1145/3412932.3412943` (*Deriving compositional random generators*), and flags the seed's low coverage. Its earlier S137 title disposition is reused; SC66 adds exact metadata but no abstract/body. The fallback SC67 query returns five records against reported total eight; SC68 at effective offset five returns zero. That count discrepancy and noise do not certify recall. The [ledger](../nu-background-searches-2026-09-30.md) records the queries and new citation audit.

Continue acquired S138's practical composition/fusion comparison, retaining the 2014 composing/decomposing method behind the balanced alternative and the worker/wrapper foundation as conditional dependencies. Then return to S118 views, S116 practice and the broader background frontiers. All experimental holds remain.
