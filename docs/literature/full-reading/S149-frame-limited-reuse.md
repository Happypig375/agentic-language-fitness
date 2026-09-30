# S149 — frame-limited reuse and the scope of its memory bound

**Complete published-paper reading, 2026-10-01 HKT.** Anton Lorenzen and Daan Leijen, *Reference Counting with Frame Limited Reuse*, PACMPL 6, ICFP 2022, article 103, [DOI 10.1145/3547634](https://doi.org/10.1145/3547634). This closes the immediate B04/B06 dependency raised by S148: what stronger space property can a replacement reuse transformation establish?

## Identity and actual coverage

Native Zotero parent `LM67FLSH`, note `FDMAE6C4`, publication attachment `UB75YUAF`. The [Microsoft-hosted publication](https://www.microsoft.com/en-us/research/wp-content/uploads/2023/07/flreuse.pdf) has 24 pages, 651,593 bytes, SHA-256 `9bc0561d70eb87ee9a16c7b52993d25e8f45e5328922ef8153f90c00640131ff`. All pages, eight figures and the bibliography were read. Pages 5–9, 11–13, 15–18 and 20–21 were rendered and inspected, covering every numbered figure and selected code/proof notation.

The [extended report](https://www.microsoft.com/en-us/research/wp-content/uploads/2021/11/flreuse-tr.pdf), MSR-TR-2021-30, v2 dated March 15, 2022, is attachment `VPTKHEXU`: 54 pages, 795,976 bytes, SHA-256 `7bab587b8d3a3fff9d3b7d6781022efb5af54cec03324989348e636f2ffbad94`. **Only pages 27–30 and 49–54 were read**, including the ARM comparison, borrowing/reuse counterexamples and precision/frame-limit/reuse proof passages. Pages 27 and 51–54 were also visually inspected. The published paper points to appendix C for proofs; this acquired report places them in D. Unread proof dependencies and other report sections prevent a complete extended-edition or independent proof-verification claim.

The named Koka `v2.3.3` and `v2.3.3-old` resolve respectively to `e371bf9d67931f3847288c595fb8095be242e1ee` (2021-11-17) and `97df9e4fe47143062225170963b786483b3fe6e4` (2021-11-07). Their recursive trees contain 1,735 and 1,634 entries without truncation. Fourteen files were read completely: new-release `test/bench/README.md`, `bench.kk`, Koka/C++ `CMakeLists.txt`, Koka `nqueens.kk`, `nqueens-int.kk`, `rbtree.kk`, `rbtree-ck.kk`, `rbtree-fbip.kk`, `rbtree-fbip-ck.kk`, `binarytrees.kk`, C++ `binarytrees5.cpp`, and old-release Koka `CMakeLists.txt` and `nqueens.kk`. The two releases' legacy `run.kk` files were acquired but not read; the README identifies `bench.kk` as the measurement entry point. Ignored manifests preserve every URL/hash. No author code, build, benchmark or installer was run.

## Mechanism and formal distinction

Earlier algorithm K chooses reuse before precise reference counting and can miss a reuse opportunity when another branch still needs the object. Algorithm D delays the object's release until after its final use. In the paper's list example this retains the whole input graph across a call merely to reuse one cell afterward, and the added reference also prevents in-place reuse inside that call. Source inlining can therefore change both opportunity and cost. The extended report supplies a concrete Lean 4.0.0 compiler-IR example at commit `6475e3d5ccaf`; it was read as author evidence, not independently executed.

The replacement first inserts precise reference-count operations, then derives reuse from existing drops of known-sized objects. Dropping children leaves a bounded cell available as a reuse token, instead of retaining an arbitrarily large graph. Tokens are affine, stay within the function and must be released on branches that do not use them. Runtime uniqueness still controls whether storage can actually be overwritten; shared data are preserved. Same-sized constructors may differ in type. The implementation prefers early reuse, then the same constructor and the most unchanged fields. TRMC can additionally turn suitable constructor-tail calls into loops; this does not make arbitrary recursion stack-free.

The strict normalized calculus separates three conditions on the environment retained across a `let`:

| Condition/result | Meaning and boundary |
| --- | --- |
| Unrestricted derivation; theorems 1–2 | Sound terminating evaluation and reachability with reference-count instructions present. A pending drop can still retain an object |
| Garbage-free derivation; theorem 3 | At the specified value/allocation states, heap entries are reachable after reference-count instructions are erased. This weakens S148's observation-point definition and permits moving drops into branches |
| Frame-limited derivation; theorem 4 | The heap splits into reachable storage and additional storage bounded by a constant times the evaluation-context depth. The constant bounds extra retained values; it must remain valid under substitution |
| Drop-guided reuse; theorem 5 | Applying the declarative reuse transformation to a garbage-free derivation yields a frame-limited derivation |

Theorem 5 is a substantive advance over S148's explicit exclusion of optimization proofs. The selected appendix proves it by induction over reuse rules: tokens are small, function bodies start with an empty token environment, and the `let` split adds only bounded retained resources. The model recognizes a drop immediately followed by a matching constructor as reuse, and represents cleared fields with allocated unit values. These are formal modeling choices, not a measurement of allocator bytes.

**The bound concerns additional abstract heap at particular evaluation states, proportional to evaluation depth.** It is neither a constant total heap bound, a fixed fraction of live memory, nor a bound in terms of the optimized machine stack. Tail-call optimization can remove machine frames while the source-level evaluation context still grows. General borrowing can retain whole graphs and does not automatically satisfy the condition; the appendix requires size bounds preserved by substitution. Koka limits borrowing here to primitives and explicit annotations rather than unrestricted inference. Borrow annotations are performance choices, not Rust-style access permissions. Cycles, concurrent reclamation, foreign control flow, allocator fragmentation and frame latency are not certified by these results.

## Positive, null and adverse measurements

Figure 8 uses an AMD 5950X at 3.4 GHz, 32 GiB memory, Ubuntu 20.04, Koka 2.3.3 with GCC 9.4 and customized mimalloc. Comparators include multicore OCaml 4.12, strict GHC 8.6.5, Swift 5.6.1, Java 17.0.1/G1 and GCC 9.4 C++ with libc. Each workload has its own Koka normalizer. The publication does not state the trial count or aggregation procedure in this benchmark section; S148's ten-run description is not imported.

| Workload | Koka seconds / peak RSS labelled mb | No TRMC time ratio | Old Koka time ratio | C++ time / RSS ratio | FBIP time ratio |
| --- | --- | --- | --- | --- | --- |
| rbtree | 0.42 / 166 | 1.18 | 1.62 | 1.19 / 1.18 | 0.90 |
| rbtree-ck | 1.05 / 1,154 | 0.99 | 1.36 | NA / NA | 0.97 |
| binarytrees | 0.89 / 665 | 0.99 | 1.01 | 0.66 / 1.49 | 0.83 |
| deriv | 0.61 / 458 | 0.94 | 1.03 | 1.20 / 2.24 | NA |
| nqueens | 0.49 / 96 | 0.96 | 1.49 | 1.10 / 3.00 | NA |
| cfold | 0.09 / 140 | 1.33 | 1.00 | 3.00 / 2.93 | NA |

No-TRMC RSS ratios are all 1.00; old Koka is also 1.00 except binarytrees at 0.98. The figure labels FBIP RSS as 1.00 even for the three workloads with no FBIP time; these are not treated as three extra measured algorithms. New reuse has material tree improvements and small/null differences elsewhere. The paper explicitly attributes the queens gain to borrowing in `safe`: the old control changes **both reuse and borrowing**. Disabling TRMC slightly improves several other rows. These adverse/null comparisons remain part of the result.

Cross-language observations are useful viability evidence with unequal obligations. C++ uses a mutable map, has no usable checkpoint result, uses bulk memory pools for binary trees, and does not reclaim memory for deriv/queens/cfold. Haskell's binary-tree RSS is 0.62 of Koka, while OCaml's RSS there is unavailable; Koka does not win every memory comparison. Java's unshared-map RSS is 11.14 of Koka under the reported settings, not a language-wide ratio. The extended ARM figure changes several relative outcomes, including near equality with C++ for unshared trees; its separate configuration/results are not pooled into Figure 8 or counted as independent replication.

FBIP rewrites tree traversal around explicit visitors whose storage can reuse unique input nodes. The balanced-tree version also stops balancing at a black node and switches to rebuilding: this is an algorithm change as well as an allocation opportunity. Shared trees initially need zipper allocation, although the newly created zipper can itself be reused. No measured developer/agent effort, Nu workload or external-effect rollback is supplied.

## Released-source correspondence and limits

The [named-release measurement script](https://github.com/koka-lang/koka/blob/e371bf9d67931f3847288c595fb8095be242e1ee/test/bench/bench.kk) defaults to one iteration, runs workloads/languages in fixed order, measures elapsed time and peak RSS using the platform `time` tool, and computes separately sorted time/RSS centers. Its `median` averages the two central values for even sample sizes; for odd counts greater than one, its indexing instead averages the value below the middle with the middle. Its spread is root mean square deviation about that center, not a confidence interval. No actual invocation/raw trials were recovered, so these static observations do not identify an error in the published measurements. The README calls this an average/error interval; neither source label resolves the missing experiment correspondence.

The selected files expose further limits:

- Publication page 20 says queens size **21**; new and old `nqueens.kk` and new `nqueens-int.kk` specify **13**. The new source adds the explicit borrow annotation; the old source does not.
- Tree sources use **4.2 million** insertions, matching S149's description and differing from S148's printed 42 million. Unshared trees use `int32` keys from N−1 down to zero; checkpoint trees use `int` keys from N down to one. The checkpoint comparison changes representation and implementation as well as retention. Dividing 1.05/0.42 seconds or 1,154/166 RSS therefore does not identify a pure retained-history effect.
- Checkpoint sources retain every fifth tree plus the final tree, giving 840,001 list entries for this input. Only the newest tree is folded for the printed result; historical-version correctness, restore operations and generated-code peak liveness remain untested.
- The new binary-tree source already selects the FBIP check and creates eight subtasks plus residual work per depth, whereas the report discusses a coarser depth-level concurrency limit. CMake omits the FBIP tree files and C++ binary-tree files from its selected targets. Thus the available source/configuration does not reconstruct all plotted arms without additional undocumented choices.
- FBIP tree equality branches retain the old value rather than replace it. Descending unique input keys do not exercise those branches, so this is a semantic generalization limit, not evidence of failure on the reported workload.

These are source/version and measurement-reconstruction gaps, not executed failures. Compiler bodies, emitted C, whole-library behavior and exact paper-run configurations remain unverified.

## Consequences and next action

**Unique:** unconfirmed for ISE/Nu; precise drops, bounded reuse and functional source implemented through mutation have established predecessors. **Valuable:** the paper supplies concrete tree speedups, a stronger space-accounting method and useful adverse cases. Nu/.NET/game transfer and net maintenance benefit remain empirical residuals. **Scientifically valid:** the transformation and formal observation boundary are reconstructed, with selected proof dependencies and experimental source correspondence explicitly bounded.

This resolves the immediate question of what replaces S148's unrestricted optimized-retention claim. It does not require recursively reading every memory-management foundation before moving on. S150's already acquired imperative snapshot/restore method is the next consequential B04/B06 comparison. FP² remains conditional on a need for static allocation guarantees; RRB/iterator retention, .NET/game costs, C11 continuation and other B01–B12 gaps remain open. No experimental start or allocation is authorized.
