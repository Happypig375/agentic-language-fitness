# S76 — Entity references, validity checks and ECS runtime tradeoffs

**Complete thesis reading, 2026-09-30.** Hugo Hansen and Oliver Öhrström, *Benchmarking and Analysis of Entity Referencing Within Open-Source Entity Component Systems*, Malmö University bachelor's thesis, Computer Science/Game Development, 15 credits, dated 2020-06-17. [Institutional PDF](https://www.diva-portal.org/smash/get/diva2%3A1479942/FULLTEXT01.pdf). Existing Zotero parent `KKVZ9EHQ`, user attachment `BD6BQCHE`, note `6XTTHP3P` were checked before continued reading through Zotero 10's native API.

All **34 PDF pages** were read, including front matter, ten figures, eight tables, four pseudocode blocks and 23 references. Eleven page images cover every figure/table and the complete pseudocode page. Blank extraction lines were removed for legibility; no substantive text was omitted. Printed pagination runs through 33 after the cover. The verified file has **530,371 bytes**, SHA-256 `53ed7fb136385ae9d0b8b184945d601cd30cf5f7634faadd0332d72421f779d3`. No author benchmark, library or candidate was executed. The library analysis below is reconstructed from the thesis, not an independent inspection of its three codebases.

## Question, mechanisms and scope

B03/B05/B06 need to distinguish the efficient bulk iteration associated with ECS from the work needed to follow references to other entities. This study compares linear updates, updates reading a randomly chosen target, and target-reading updates that first check whether the target is alive. The latter separates some reference-validation cost from lookup cost; it does not test all lifecycle obligations.

The authors selected three libraries from five highly starred GitHub search results using C++, MSVC support and installation/creation/update documentation as criteria. These are **EnTT**, **EntityX**, and the specifically named **redxdev/ECS** library. They excluded ecst for compiler support and Kengine because it is an entire engine. The bibliography identifies snapshots `6006917`, `13b01f9` and `5f74e19` respectively. The comparison is of those selected 2020 implementations and one author-written object-oriented baseline, not all ECS designs or current releases.

The thesis describes EnTT's index/version entity identifiers, packed component arrays and sparse-set lookup. EntityX also uses index/version identifiers, but its component lookup follows a type-indexed array and entity-indexed storage. The redxdev library keeps a per-entity component hash map and resolves an entity identifier with a **linear search**. A lookup is therefore O(N) for this library; doing one per entity produces O(N²) total work. The thesis's discussion occasionally confuses the lookup and whole-loop complexities; its methods distinguish them. Its slow result must not be generalized to the ECS pattern.

The baseline uses a base class with position and a virtual update, a derived object containing velocity and a target reference, and iteration over pointers to objects. Raw target pointers implement the unsafe variant; standard-library weak pointers implement the safe variant. The text also describes shared ownership of objects. Without the benchmark source, exact owner-container/allocation details remain unverified.

For EnTT and EntityX, the described validity check compares identifier versions. Release-mode assertions do not supply automatic runtime validation. A live entity also does not by itself prove that a requested component is present or that a cross-entity relationship is semantically correct. The ECS library's missing-entity lookup returns null, while the raw-pointer baseline lacks a validity test. These are prior safety mechanisms and explicit obligations, not measured rates of fault prevention.

## Actual experiment and observations

The machine is a Windows 10 x64 system with an eight-core i9-9900K at a reported 4.8 GHz, hyperthreading enabled and 32 GB of 3200 MHz memory. The project uses MSVC release mode, reported `/O2x`, CMake, and vcpkg/direct Git linking. Exact compiler/package versions and benchmark source are not supplied by the thesis. Exact-title and author searches did not recover that benchmark; the cited repositories are libraries and other authors' benchmarks.

Each configuration uses 1,000, 10,000, 100,000 or 1,000,000 entities and **50 repeated timings**. Each run constructs entities and assigns random targets using a fixed seed before timing just the update loop with `std::chrono`. Position and velocity each contain three floats. Linear updates compute a new position from velocity; access updates compute velocity from the target and current positions. Thus a linear/access ratio changes the arithmetic and memory operation together, rather than isolating one added dereference. No entity deletion, invalid-target frequency or runtime component-change workload is described in the timed test.

The tables report mean microseconds per entity and relative standard deviation. Representative endpoints from the fully examined tables are:

| Implementation and entity count | Linear | Unsafe target access | Safe target access |
| --- | ---: | ---: | ---: |
| EnTT, 1,000 | 0.004906 | 0.022634 | 0.022958 |
| EnTT, 1,000,000 | 0.00512007 | 0.08884 | 0.0913204 |
| EntityX, 1,000 | 0.03958 | 0.07923 | 0.08049 |
| EntityX, 1,000,000 | 0.038351 | 0.161994 | 0.164747 |
| redxdev/ECS, 1,000 | 0.123272 | 0.43055 | 0.42998 |
| redxdev/ECS, 100,000 | 0.172149 | 58.5479 | 58.8688 |
| Object baseline, 1,000 | 0.002358 | 0.002744 | 0.01103 |
| Object baseline, 1,000,000 | 0.00765473 | 0.0185698 | 0.0421883 |

The redxdev library's **1,000,000-entity cells are N/A**, not zero or completed failures. They are omitted from cross-library plots; its available results remain in its own table/figure. The thesis gives time concerns for limiting benchmark scale but does not separately document a completed million-entity run for this library. Do not turn the nominal 4 × 3 × 4 grid into 48 completed configurations; the tables contain 45 populated configuration means.

The baseline is fastest for all reported reference-access comparisons and for linear updates at the two lower sizes. **EnTT is fastest for linear updates at 100,000 and 1,000,000 entities.** At one million, EnTT's reported linear time is about one third lower than the baseline's; its safe target-access time is about 2.16 times the baseline's. These are specific favorable and adverse observations, not a universal winner. EntityX is slower than both in this workload. The authors cannot explain all of EnTT/EntityX's difference from the conceptual design alone.

EnTT, EntityX and redxdev/ECS show small safe/unsafe mean differences in their available results. The baseline's weak-pointer variant has a substantial additional cost: at one million its mean is about 2.27 times the raw-pointer variant's, while remaining faster than the tested ECS alternatives for target access. The authors' phrase “no significant difference” relies on differences being within reported standard deviations; they supply no inferential test or equivalence margin. Credit the descriptive observation, not statistical equivalence or free safety. The 50 timings are repeated executions of a narrow fixed-seed workload, not 50 independent games or architecture implementations.

## What the measurements establish and leave open

The results demonstrate a workload-dependent tradeoff: packed linear iteration can be favorable while indirect target access has a different cost. Cheap version checks are a concrete alternative to unvalidated references, and the chosen reference-counting baseline has a measurable cost. This is useful positive mechanism evidence even though it does not quantify maintainability, source-evolution success or agent performance.

The authors explicitly call the tiny payloads best-case data layouts, particularly favorable to their object baseline, and acknowledge that they do not represent a realistic game comparison. Their suggestion that reference overhead is independent of component size is not isolated by this design: layout, footprint, access order and cache behavior can interact. Setup/allocation costs are outside the timer; frame-time tails, retained memory, throughput under concurrent work and total production costs are not outcomes.

**Cache misses were not measured.** Tables 1–4 assign entire working-set sizes to cache tiers using reported 512 kB/2 MB/16 MB capacities, without establishing per-core data-cache capacity or actual residency. The apparent aggregate-cache assumption therefore remains a qualification to the explanation; this pass does not certify its “fits in L1” labels. Hardware search results suggested the need to distinguish instruction/data and private/shared caches, but the attempted official family datasheet redirected to an inaccessible 404 route. Intel's accessible support page explains how to inspect totals, not this machine's per-core topology. No replacement numerical cache claim is inferred from secondary hardware pages, and no hardware probe was run. The timing observations survive without treating cache causation as measured.

The final recommendations about ease of use, modularity and when a design is suitable are author interpretations. There is no developer study, maintenance task, measured debugging success, or runtime add/remove experiment. The future-work section explicitly leaves component/entity changes, larger workloads, other compilers and other hardware open. Figures 1–3 illustrate a particular inheritance/composition example; they do not demonstrate that ordinary object-oriented composition cannot solve it.

## Consequences and consequential follow-up

- **Unique:** iteration, generational identifiers, explicit validation and reference-cost tradeoffs are established alternatives to a single world-state representation. This does not establish or refute priority for Nu's complete combination or D1's local agent question.
- **Valuable:** S76 supplies measured benefits for EnTT's large linear workload and for the object baseline's target-access workloads, alongside low observed version-check overhead. It sharpens the relevant cost dimensions; ISE/Nu net maintenance benefit remains unmeasured.
- **Scientifically valid:** classify actual operation mix, component presence, live/dead references, implementation snapshot, initialization and timing units separately. Do not import these ratios, nominal cache bins or 50 repetitions as an isolated architecture effect. The paper's method is now understood; unmeasured effects remain empirical dispositions rather than unfinished reading.

S77's simplified migration benchmark omits production nation/event relationships; S76 shows why that omission can matter for operation mix, without supplying a measured migration penalty. The **2025 direct citer S112**, *Run-time Performance Comparison of Sparse-set and Archetype Entity-Component Systems*, DOI [10.2312/cgvc.20251224](https://doi.org/10.2312/cgvc.20251224), now has a Zotero record before intentional PDF reading. It was already an unassigned W02 lead and offers author code plus a CSV supplement. Its indexed iteration/instantiation results and broader composition-change claims need a full methods check. The 2026 paper *The Semantics of Entity Component System*, DOI `10.1145/3828534.3828535`, is a metadata/shortened-abstract lead, not a read method.

S76's bibliography also supplies Fontana et al.'s EDA comparison, Lange et al.'s wait-free lookup method, Nilsson/Björkman's 2019 engine thesis, benchmark repositories and industry talks. They are distinct discovery routes, not newly credited effects. S112's nearer storage comparison, S68's taxonomy and the unresolved S108/C02 type/evolution coverage determine subsequent priority. No experiment or new model allocation follows from this reading.
