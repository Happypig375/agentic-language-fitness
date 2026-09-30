# S112 — ECS storage, creation and frame-time tradeoffs

**Complete publisher reading, 2026-09-30.** Louis Cox, Benjamin Williams, James Vickers, Davin Ward and Christopher Headleand, *Run-time Performance Comparison of Sparse-set and Archetype Entity-Component Systems*, CGVC 2025, DOI [10.2312/cgvc.20251224](https://doi.org/10.2312/cgvc.20251224). The publisher PDF prints author initials; publisher/institution metadata give James, while the repository README uses Jay. This is one publication, not two author lineages. Zotero parent `XUG4KLIW` existed before intentional PDF reading; attachment `F37ND8XP` and note `QZSEFD2H` were reverified through the native API.

All **nine pages**, seven numbered figures, two tables and 43 references were read. Six inspected page images cover the title/abstract and every figure/table. File: **1,144,634 bytes**, SHA-256 `778d6c8f52814a7828403b5456a2d53331a6079fc1fddbcb160578aadd3cc4a0`. The [publisher CSV supplement](https://diglib.eg.org/server/api/core/bitstreams/11c23581-b821-46c9-8102-840dc9d9cbc0/content) was acquired through the public repository API, attached as `H644DUD5`, and its stored hash verified: **237,682 bytes**, SHA-256 `d041c900330318ffbe8e980fe6b25c15b2b02c68769f6d641f8acc2f5ff0a517`. Three CSVs were parsed completely for a bounded descriptive reconstruction. Fifteen source/configuration files from the cited repository were inspected. No author code was compiled or executed; recomputing statistics from released observations is not reproducing the experiment.

## What this adds to S76/S77

S76 compares selected libraries with an object baseline; S77 compares two hybrid game subsystems. S112 instead supplies two author-built C++20 prototypes, sharing a framework but differing in storage/query mechanisms. This helps B05/B06 distinguish costs within ECS rather than treating ECS as one implementation.

The sparse-set design maps identifiers through paged indices to dense component storage and offers tree-based component queries. The archetype design groups entities by component sets and gathers matching archetype views. Both provide entity/component operations. The benchmark is a Game of Life grid with one `CellData` component per cell, at 100, 1,000, 10,000 and 50,000 cells. The paper specifies single-threaded processing and wrapped grid boundaries. It times **frame updates** and **initial creation with component association/grid placement**. Later component additions/removals, deletion/recreation and transitions among populated archetypes are not separately timed outcomes.

Choosing minimal prototypes reduces some library differences but does not isolate an abstract architecture from implementation choices. Query order, allocation, indexing and bookkeeping remain part of the treatment. The paper itself acknowledges implementation dependence and leaves other optimizations, hardware/workload transfer, memory footprint and parallelization open.

## Observations reconstructed from the supplement

`iter-data-collated.csv` contains **40,000 rows**: eight architecture/size series, each with iterations 1–5,000. The two setup files contain **5,000 distinct entity IDs each**, 0–4,999. There are no independent run/seed/hardware identifiers. These are repeated frames and sequential creations, not 5,000 independent architecture implementations or game workloads.

| Outcome | Archetype | Sparse set | Bounded interpretation |
| --- | ---: | ---: | --- |
| Median frame, 100 cells | 0.7967 ms | 0.7990 ms | Nearly equal recorded centers |
| Median frame, 1,000 cells | 0.7987 ms | 0.7977 ms | Nearly equal recorded centers |
| Median frame, 10,000 cells | 1.72085 ms | 2.9452 ms | Archetype is faster in this series |
| Median frame, 50,000 cells | 7.41015 ms | 13.81910 ms | Archetype is faster in this series |
| Median initial creation | 6,600 ns | 1,000 ns | Sparse-set median is lower; ratio 6.6 |
| Mean initial creation | 6,883.28 ns | 1,093.92 ns | Ratio is about 6.29, not 6.6 |

Setup means, medians, sample standard deviations and extrema reconstruct Table 2. Frame summaries closely reconstruct Table 1. A small precision difference is explicit: the raw 10,000-cell sparse mean is 3.04246624 ms, while the table prints 3.043; rounding each input to two decimals first yields 3.04252. This is compatible with intermediate rounding, not evidence that the difference in centers vanishes.

The paper reports Mann–Whitney p = .490/.376 at the two smaller sizes and p < .001 at the larger sizes and for setup. Its Spearman correlations pool 20,000 frame rows per architecture. This reconstruction checks descriptive summaries, not those p-values. Consecutive frames and creations can share state, scheduling and cache conditions; the paper does not establish independent sampling at that row level. Nonsignificance at small sizes is not an equivalence test, and this two-ECS comparison has no object-oriented arm from which to infer that ECS has no small-project utility.

Figure 6 replaces extreme observations with nearby means for display, without a reproducible cutoff/procedure. The released CSVs retain extreme values. At 50,000 cells, archetype's sample SD is **1.17562 ms** versus sparse-set's **0.80415 ms**; maxima are **85.1639 versus 20.0476 ms**. Between 10,000 and 50,000, archetype's SD grows from about 0.40259 to 1.17562, while sparse-set's grows from 0.40083 to 0.80415. Thus the prose's claim of greater sparse-set variability at high scale does not follow from its unfiltered table/data. Lower typical frame time and smaller tail/dispersion are separate outcomes. The creation “average factor of 6.6” corresponds to the median ratio, whereas the ratio of means is about 6.29.

These qualifications preserve the concrete positive results: the released observations support lower archetype frame centers at the two larger sizes and lower sparse-set initialization cost. They do not measure arbitrary later composition changes, cache misses, developer effort or real-game net benefit.

## Bounded artifact correspondence

The [cited repository snapshot](https://github.com/StaffsUniGames/cgvc25-ecs-comparison/tree/284b1aa8af0b4a53700a5f2e046b43f9eac331e6) is pinned at **`284b1aa8af0b4a53700a5f2e046b43f9eac331e6`**, 2025-06-26. Its four-commit history includes the code upload followed by README edits. Its 231-entry recursive tree is untruncated. The read subset is `App.cpp`, `AppWindow.cpp`, the empty `Project/Test.cpp`, root CMake/presets, engine CMake, `Engine.cpp/.h`, both ECS `World.cpp/.h` pairs, `Archetype.h`, `Query.h` and `SparseSet.h`. Third-party dependencies, most rendering code and remaining engine utilities were not read. Local manifests retain hashes for the fifteen files.

The released `Engine::Init` uses a **250 × 250 grid**, explicitly selects `SparseSetWorld`, marks out-of-bounds neighbors with a sentinel, and skips those neighbors. This differs from the paper's four measured sizes and wrapped-boundary description; the 62,500-cell screenshot does match the demo's size. The visible loop updates a live flag, creates no new components after setup, draws through Vulkan and updates an FPS title. It does not contain the paper's per-frame/setup CSV logging or a 5,000-frame measurement stop. The empty test file supplies no alternate benchmark. Therefore the retrieved demo is not a verified reconstruction of the measurement application.

The source does instantiate the described storage/query ideas. Sparse component payloads occupy a `std::vector<T>`; paging applies to the identifier map. Its query caches entity IDs obtained through set operations and resolves payloads through the sparse mapping. The archetype view indexes component vectors directly. Consequently “sparse” does not mean that payload storage itself must be noncontiguous, and the measured difference cannot be attributed to that shorthand alone. No cache-counter data isolate a cause.

There are further reasons not to certify executable correctness from this bounded read: for example, archetype storage allocates a `std::vector<std::byte>` behind `void*` and retrieves it through casts to other `std::vector<Component>` specializations. Resolving such representation/lifetime assumptions and the actual benchmark version would require a separate code/build validation. This pass neither repairs nor runs that code and does not attribute a measured failure to it.

The presets expose MSVC debug/release choices, and engine CMake enables a Vulkan validation-layer option by default. These are available configurations, not evidence of which binary produced the CSVs. The paper does not specify the machine, operating system, compiler version, optimization settings, graphics/synchronization treatment, initial seeds or run order sufficiently to recover them. No behavioral state comparison establishes equivalence of the measured variants independently.

## Evidence disposition and follow-up

| Criterion | Updated judgment |
| --- | --- |
| Unique | Distinct storage/query choices and context-dependent selection have prior art. S112's own broad first-comparison claim requires earlier thesis/artifact checks; it is not evidence of Nu/ISE priority. |
| Valuable | The available data establish an actionable prototype-specific tradeoff between initialization and typical frame time. Tail behavior, later composition changes and developer maintenance costs remain separate unknowns. |
| Scientifically valid | Preserve frame/creation dependence, operation scope, full distributions and source/data correspondence. Do not transfer the descriptive ratios or reported p-values to abstract ECS categories, F# or agents. The publication is fully understood at this scope; experimental reproduction remains unperformed. |

New consequential bibliography routes include Compton's 2022 *An Investigation of Data Storage in Entity-Component Systems*, Choparinov's 2024 *A Graph-Based Approach To Concurrent ECS Design*, the 2019 *Polyphony* ECS interface paper, and the same group's 2024 forestry comparison (`10.2312/cgvc.20241218`). They can change taxonomy, earlier-comparison coverage and concurrency/UI transfer. They are presently bibliography-level leads; thesis degree labels in S112 are not independently verified. The repository's undergraduate-thesis lineage likewise is not a second empirical replication. S76/S77 are reused, not counted as new readings here. The next coverage priority returns to S108's unresolved reconciliation dependency and C02's incomplete type/evolution screen, with these game-alternative leads preserved for S68's taxonomy work. All experimental holds remain.
