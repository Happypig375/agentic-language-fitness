# S145 — reuse, borrowing and the cost of retaining versions

**Successor check, 2026-10-01:** [S148 Perceus](S148-perceus-precise-reclamation.md) is now fully reconstructed. It formalizes core reference-count insertion, while leaving later optimization proofs outside its scope. This advances the precise-reclamation dependency without supplying the missing whole-compiler/reuse proof for this S145 edition. Its runtime evidence also preserves a case where reuse retains extra memory; S149 is selected for the stronger space-bound follow-up.

**Complete reading, 2026-10-01 HKT.** Sebastian Ullrich and Leonardo de Moura, *Counting Immutable Beans: Reference Counting Optimized for Purely Functional Programming*, IFL’19, [DOI10.1145/3412932.3412935](https://doi.org/10.1145/3412932.3412935). This B04/B06/B12 reading reconstructs a runtime alternative to tracing collection and directly examines retained functional versions. Conference year2019, the manuscript's2020 reference format and the preprint revision date are distinct.

## Source identity and actual coverage

Zotero parent `JPGFLE52`, PDF `7T475K65`, full note `U9NS75IB`. The [KIT author PDF](https://pp.ipd.kit.edu/uploads/publikationen/ullrich19counting.pdf) has twelve pages,621,450bytes, SHA-256 `357f5e70164cdba0c0ba2ea1fbf6e0f51306468956cfff9486d4930a05e11589`. Every page, all seven figures including the two numerical tables, formal rules, examples and28 references were read. Pages4–7 and10–11 were rendered and visually checked; the black-square dummy-location symbol lost by extraction is visible. [arXiv metadata](https://arxiv.org/abs/1908.05647) identifies v3 dated2020-03-05; its PDF bytes and earlier versions were not compared with the KIT edition.

The paper's [IFL19 source tag](https://github.com/leanprover/lean4/tree/c7e85e3cec929ac3e90e6126305e65200d6bfc06/tests/bench) resolves to `c7e85e3cec929ac3e90e6126305e65200d6bfc06`,2020-03-05. An untruncated2,499-entry repository tree was inspected for benchmark/configuration paths. Fourteen files were acquired; thirteen were read completely: benchmark README, Makefile, `cross.nix`, `report.py`, five `rbmap_checkpoint` implementations, `lean-gc.py`, `ocaml-gc.py`, `perf.py` and `disable-st.patch`. `cross.yaml` was read at lines191–275 plus selected option/context lines; the rest remains unread. Compiler IR bodies, remaining benchmark implementations and the whole repository were not read. The obsolete lowercase compiler-path footnote is resolved to the actual `src/Init/Lean/Compiler/IR/` directory, without claiming an implementation audit.

No saved `.bench`/CSV/TeX measurements or generated report directory are present under the pinned benchmark tree. No author code, compiler, dependency installer, benchmark or measurement tool was run. Independent arithmetic below uses the paper's rounded numbers, not recovered trial data or reproduced experiments.

## Mechanism and its assumptions

The language and simplified IR are eager, purely functional and unable to construct cyclic value graphs. The paper therefore avoids one ordinary reference-counting limitation by a language restriction. It does not establish cycle handling for unrestricted object graphs; the conclusion proposes that extension. Reference counting can also produce an unbounded deletion cascade, so this is not a response-time guarantee.

Owned references represent counted lifetime obligations. Passing, returning or storing one can transfer the obligation without an increment/decrement pair. Borrowed references avoid counter traffic but rely on a surrounding owner keeping the object alive. A count of one alone does not authorize destructive reuse through a borrowed parameter.

`reset` tests whether an owned constructor is unique. If unique, it releases the old children and returns its allocation as a reusable cell; otherwise it consumes its reference and returns a dummy token. `reuse` either overwrites a compatible cell or allocates a new one. Separating the two operations lets a recursive traversal release an outer node's ownership of its children before testing their uniqueness. A later uniqueness test cannot simply replace the saved reset decision because intervening code can change counts. Reused storage must have the required size, and the token must be consumed appropriately on every path.

The insertion pass looks for dead matched variables and compatible later constructor allocations. Borrow inference starts with borrowed parameters and marks owned uses to a fixed point; wrappers handle escaping partial applications. Reference-count insertion handles duplicate arguments and simultaneous borrowed/owned use. A refinement avoids trailing decrements that would destroy tail calls. These are specified transformations and worked examples; **the paper explicitly leaves a formal correctness proof of its compiler as future work**.

Reusable list/tree cells do not make every called function allocation-free. Inlining or deliberately threading a spare constructor through red-black balancing exposes additional reuse opportunities. The paper provides inspection/instrumentation techniques to check inserted reuse and runtime sharing. This is a constructive programming technique with source-shaping obligations, not automatic free performance for arbitrary pure code.

The runtime distinguishes thread-local, shared and permanently retained objects. It avoids atomic counter operations on thread-local values, recursively marking reachable values before sharing them through task primitives. The graph invariant and immutability make that transition manageable, but task creation can traverse a large reachable graph. Here “persistent” denotes immortal initialization values, not the general data-structure notion of keeping old versions. A64-bit constructor header uses16bytes and a list cell32bytes; representation, counter traffic and reclamation work remain real costs.

## Experiments: preserve both gains and regressions

The paper reports arithmetic means of50 runs on an i7-3770/16GB/Ubuntu18.04 system, with Clang9.0.0 compiling Lean's emitted code. Comparators are GHC8.8.3, OCaml4.10, MLton20180207, MLKit4.4.2 and Swift5.1.1. The chosen workloads emphasize compiler/prover operations, with a parallel binary-tree benchmark and array examples. They are not an interactive game or general workload sample.

Figure6 disables reuse insertion, inferred borrowing or thread-local counter specialization. Builtin borrow annotations still apply in the borrowing ablation. The following ratios divide each ablated time by its **own workload's full-optimization time**, computed from rounded published entries. The paper instead normalizes all three map variants by the unshared map baseline.

| Workload | Without reuse | Without inferred borrowing | All counters atomic |
| --- | ---: | ---: | ---: |
| Binary trees | 0.98 | 1.14 | 1.22 |
| Differentiation | 1.00 | 1.16 | 1.42 |
| Constant folding | 1.64 | 0.90 | 1.23 |
| Parser | 1.00 | 1.00 | 1.68 |
| Quicksort | 1.00 | 1.00 | 1.13 |
| Unshared map | 3.23 | 1.07 | 1.71 |
| Save every tenth map | 2.43 | 1.02 | 1.63 |
| Save every map | 1.15 | 0.95 | 1.70 |
| Union-find | 1.41 | 1.00 | 2.31 |

Reuse has substantial positive effects on several selected workloads, but near-null and slightly adverse observations also occur. Inferred borrowing improves differentiation/binary trees while its removal speeds constant folding and the most shared map row. The nine-row geometric means of these within-workload ratios are approximately1.398,1.023 and1.524. The paper's1.74/1.27/1.89 column means include the shared-map normalization; its base column is1.24, not one. These summaries equally weight related workloads and are not independent population estimates. Squiggled digits encode the authors' stated dispersion convention, not confidence intervals or proof of a significant difference for each cell.

Saving every tenth/every tree raises full-optimization Lean time to1.49/4.72 times its unshared map time. Reuse still helps the fully retained case:5.42/4.72≈1.15 for disabling it. In Figure7 the fully retained row is4.72 for Lean versus14.66 GHC,9.20 OCaml,4.43 MLton,15.50 MLKit and12.76 Swift, all against Lean's **unshared** map time. Lean therefore remains competitive while MLton is slightly faster in that case. This is a useful retained-history result, not evidence that sharing eliminates every reuse opportunity or that retained state is free.

Other favorable comparisons coexist with exceptions: constant folding strongly favors Lean over the selected GHC/OCaml/Swift versions, while MLton/Swift quicksort times are0.54/0.64 of Lean. Integer boxing, compiler optimization, evaluation strategy, language support and source translations differ. Quicksort compares pure/copy-on-write implementations with explicitly destructive ones; it does not isolate purity or GC. Binarytrees uses selected Benchmark Game implementations, with absent SML measurements and an unavailable OCaml GC fraction preserved as missing.

GC accounting is asymmetric. Lean's sampled deletion functions exclude inlined increment/decrement costs; Swift includes counter operations and deletion, while other runtimes supply different GC measures. Constant-folding prose says17% Lean deletion, but Figure7 says13%; the discrepancy is unresolved. Cache misses are reported **per second**, not per completed workload. Higher miss rate during a faster run cannot alone rule out lower total misses or identify the cause of a speedup. No peak-retained-memory or frame/response-tail comparison is supplied.

## What the pinned source resolves

The Makefile uses two million descending, distinct integer-key insertions for each map variant, with save frequencies1/10. Five language implementations confirm this selected history workload. Saving the final root again yields2,000,001 or200,001 list entries; these are root entries, not independent versions/cases. The output traverses the newest tree and inspects each saved root. The Haskell source adds strict bindings to avoid inadvertently retaining all intermediate trees in thunks. This is a meaningful effort to align the retention treatment, not a proof of equivalent optimization or behavior across languages.

`cross.nix` separately pins the compiler to `21ca3709612ff7a05f0e5aa0849d776c1bc6d751`; the benchmark tag and compiler revision are different identities. Its patches specify the ablations, including changing thread-local header tags to shared tags. Compiler/launcher options differ across languages and include special binarytrees flags. The inspected `cross.yaml` fixes min/max50 measured runs, discards the first run and discards a program block's data on error. It enables block shuffling, but Makefile targets invoke separate measurement commands; this is not evidence of globally interleaved variant trials. Optional machine isolation in the README is not evidence that the reported run used it.

`report.py` confirms arithmetic per-row means and the common unshared-map normalizer, followed by geometric column aggregation. Its “deviation” aggregation is a geometric mean of per-row standard deviations, not propagated uncertainty for a geometric mean. The profiling helpers confirm differing GC fractions and cache-miss rates. These bounded reads clarify interpretation; missing run data prevents checking trial exclusions, dispersion and exact source-to-result correspondence.

## Implications and next source

**Unique:** reference-counted destructive reuse and borrowing are established alternatives, with explicit older predecessors. No Nu firstness follows. **Valuable:** controlled compiler ablations support concrete allocation/throughput benefits, including a scoped retained-history comparison; workload-sensitive regressions and source/runtime obligations qualify them. **Scientifically valid:** the proposed transformations and measurements are reconstructed, but the compiler proof is unfinished in this paper, raw trials are absent here, and cross-language differences do not isolate a memory-management cause.

S148 Perceus is promoted for the direct soundness, precise-reclamation and reuse successor; its extended PDF is acquired but unread. Frame-limited reuse, fully in-place programming, lifetime inference, modal OCaml, cyclic collection and laziness remain named conditional methods in the runtime screen. Nu/.NET history retention, concurrency boundaries, frame latency and maintenance cost remain distinct empirical/coverage questions. All experimental holds remain.
