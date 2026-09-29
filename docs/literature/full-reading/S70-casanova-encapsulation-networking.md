# S70 — Generated coordination preserves source organization but leaves runtime and network obligations

**Full publication reading completed 2026-09-30.** Francesco Di Giacomo, Mohamed Abbadi, Agostino Cortesi, Pieter Spronck, Giulia Costantini and Giuseppe Maggiore, *High performance encapsulation and networking in Casanova 2*, Entertainment Computing 20 (2017), pp. 25–41. DOI [10.1016/j.entcom.2017.03.001](https://doi.org/10.1016/j.entcom.2017.03.001). Available online 2017-03-07; accepted 2017-03-01.

The user-supplied publisher PDF is attachment `R2A6BM28` under Zotero `M256NA5R`: seventeen pages, 2,051,278 bytes, SHA-256 `a1b4a6ac47014fcde102553ef27682fe42cfe9a120a3e37a5e37548e64cb224d`. All seventeen pages of text, three figures, three tables, both algorithms, image-based code listings and 45 references were consumed. Rendered PDF pp. 4, 6–8 and 10–17 supplied the consequential diagrams, code and table layout omitted by extraction. The prior IRIS 403 is no longer an access blocker. No compiler/game/network experiment was executed, and the released implementation has not been audited.

The paper identifies itself as an extension of the 2015 CEEC paper *High performance encapsulation in Casanova 2*, DOI `10.1109/CEEC.2015.7332725`, adding related work and networking. Those versions are not independent replications. [S69](S69-casanova-formal.md) is an earlier family member; this paper references the 2013 thesis for the language's formal description. Compiler/edition equivalence across those sources is not assumed.

## Responsibility and generated dependencies

The running example contrasts planets that find incoming enemy fleets by querying the world with routes that directly mutate planets. A later planet-freezing requirement illustrates change propagation: the selected encapsulated version centralizes the update policy, whereas the selected direct-write version spreads it across writers. This is a concrete architectural argument, not a measured developer-maintenance experiment. Other encapsulated implementations or indexing responsibilities are not experimentally eliminated by presenting this pair.

The naive search is described as O(mnk) for m planets, n routes and up to k fleets per route; direct route updates are described as O(nk). The compiler generates indexes and notifications to retain the high-level source organization while changing runtime work. Therefore this contrast includes algorithm selection and generated bookkeeping; it is not a pure effect of interfaces, immutability or dynamic dispatch.

Sections 4–5 optimize predicates that remain unchanged across many frames. The compiler identifies interesting conditions and dependencies, then generates dictionaries and collections for suspended/active rules. Relevant field changes wake a suspended rule during the next frame. Creation populates dependency entries; destruction removes the object's occurrences as key or value; notifications maintain active rules. Queries are transformed into incrementally maintained membership. These mechanisms establish direct predecessors for automatic coordination and lifecycle bookkeeping in games.

The optimization has explicit limits. Interesting conditions must depend wholly on Casanova datatypes because the analyzer cannot infer external libraries' temporal behavior. Predicates affected by an atomic rule are excluded from the relevant structure. Temporal locality is an assumption, and dictionary/notification overhead is acknowledged. Automatic profiling and recompilation to choose profitable optimizations remain future work. The paper asserts semantic preservation, but its two construction algorithms do not by themselves prove all update ordering, alias, destruction, external-call and multi-condition cases. A later implementation comparison must verify those boundaries independently.

## Network ownership is a different consistency problem

Sections 6–7 describe peer-owned entities, predicted remote replicas, connection-specific rules, and reliable versus unreliable send/receive primitives. A tracking server introduces peers and forwards traffic; it is not an authoritative game-state validator. Generated code handles details such as list additions/removals, but programmers still assign ownership, choose which rules run where, decide delivery requirements and choose which state to synchronize.

The example transmits projectile creation/removal reliably and position updates unreliably. It explicitly admits missed collisions and out-of-sync states when position messages are lost. Score remains local because other players' scores are not displayed; adding a shared score would require additional synchronization. The shoot rule's key-release wait prevents repeated firing while a key remains held. These are concrete temporal and product-obligation choices beyond a type-correct local state update.

Predicted replicas are corrected from received updates, rather than every peer having one simultaneous complete world snapshot. No fault-injection, loss/latency distribution, malicious-peer validation, convergence bound or networking-throughput result is reported. The networking evidence is a language/example demonstration and a source-length comparison, not a robustness or productivity trial. The categorical genre/protocol and general-purpose-language claims in the motivation should not be imported as established survey findings from this small evaluation.

## Evaluation and denominator reconstruction

The benchmark spawns entity groups every unspecified K seconds. Entities remain inactive for a random 5–10 seconds, move for 4–8 seconds, then are destroyed; additional timed conditions increase the work. It measures update-iteration time using Unity3D and MonoGame. Rendering is excluded. The paper does not supply the machine, precise engine/runtime versions, entity counts/K, random seeds, run duration, repetition count, summary statistic or uncertainty needed to reconstruct the measurements independently.

Table 2 labels its values **milliseconds**; that printed unit is retained, not silently reinterpreted:

| Platform | Unoptimized Casanova | Optimized Casanova | Selected C# | Ratios calculated from printed cells |
| --- | ---: | ---: | ---: | --- |
| MonoGame | 0.0159 | 0.0098 | 0.0147 | Unoptimized/optimized ≈1.62; C#/optimized =1.50 |
| Unity3D | 0.0257 | 0.0085 | 0.1642 | Unoptimized/optimized ≈3.02; C#/optimized ≈19.32 |

The text's order-of-magnitude claim against unoptimized Unity Casanova is not supported by its printed cells: the larger ratio is against C#. The pattern remains a reported benefit on the selected synthetic workload, with separate comparator and platform effects. It does not establish a universal encapsulation penalty, typical game speedup, 60-Hz worst-case guarantee or Nu result. No correction of the original data is inferred from the discrepancy.

Table 1 reports 45 authored Casanova lines versus 88 C# lines, while generated C# grows from 139 to 327 lines with optimization. This distinguishes authored representation from generated machinery and its maintenance/debugging boundary. Table 3 reports 126 versus 1,257 lines for the multiplayer example, about a tenfold ratio. Neither count measures developer time, defect rate, training effort, comprehensibility or independent all-obligation equivalence. No expert/user study is presented.

## Artifact access and consequential follow-up

The paper's [networking wiki link](https://github.com/vs-team/casanova-mk2/wiki/Networking-extension) did not render through the web reader. A direct read of its raw Markdown succeeded: its entire 70-byte body is a link to `http://med.hro.nl/abbam/Networking_demo/Networking%20alpha.zip`. A HEAD request to that host failed at DNS resolution (`getaddrinfo failed`, error 11001). This verifies the link and the local acquisition failure, not global absence, archive version, contents or behavioral equivalence. The repository is accessible, but its current state is not evidence of the exact benchmark revision. The complete publication reading does not imply a complete artifact audit.

SC06 requested twenty records for six exact family/bibliography titles and returned four: the 2015 predecessor, *Scaling games to epic proportions* (`10.1145/1247480.1247486`), the Network Scripting Language paper (`10.1145/1517494.1517512`) and Metacasanova (`10.1007/978-3-319-49616-0_22`). Only metadata and supplied short/missing abstracts were screened. The monadic-scripting paper and 2013 thesis were not returned by that query, which is not evidence that they do not exist. Primary methods remain open, especially database-style incremental game queries and networking-language predecessors. The 2015 version needs comparison only for consequential lineage/supplement differences, not automatic duplicate full-reading credit.

## Consequences for Nu and ISE

| Claim | Evidence / distinction | Required correction or control |
| --- | --- | --- |
| High-level game code can centralize state responsibilities while avoiding naive runtime scans | Generated indexes, suspended rules and lifecycle notifications in §§3–5 | Established predecessor; compare Nu's actual semantics, external boundaries and generated/runtime work |
| Compact source implies lower total complexity or maintenance cost | Authored source shrinks while generated C# expands; no developer comparison | Account for machinery, training, debugging and behavioral coverage separately |
| Local update consistency extends to distributed gameplay correctness | §§7.3–8 admit stale replicas, lost updates and missed collisions | Specify ownership, delivery, ordering, score/collision obligations and failure outcomes independently |
| Declarative optimization establishes a net runtime advantage | One synthetic update benchmark; temporal-locality assumption, platform-specific ratios and missing distributions | Require workload/adverse cases, lifecycle churn, external dependencies and frame-tail/memory measurements before generalizing |

**Unique:** broad claims about encapsulated declarative games, generated dependency scheduling and networking primitives already have predecessors; Nu's distinct contribution remains unresolved. **Valuable:** fewer scattered edits and less handwritten bookkeeping are plausible benefits, but source counts are not measured net productivity. **Scientifically valid:** the paper helps specify rivals and outcome boundaries, while leaving equivalence, workload breadth, network faults and apparatus accounting unvalidated. No ISE experiment is authorized or reproduced by this reading.
