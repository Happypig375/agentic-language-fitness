# S143 — CHAMP representation and measured collection costs

**Reading completed 2026-10-01 HKT.** Michael J. Steindorfer and Jurgen J. Vinju, *Optimizing Hash-Array Mapped Tries for Fast and Lean Immutable JVM Collections*, OOPSLA 2015, 783–800, [DOI 10.1145/2814270.2814312](https://doi.org/10.1145/2814270.2814312). The Notices DOI `10.1145/2858965.2814312` denotes the same paper lineage, not an independent evaluation or a substantive correction. This addresses B04/B06/B12: which persistent-structure costs can be reduced, what the comparisons measure, and what remains outside their scope.

## Acquisition and coverage

Native Zotero parent `34J3MDAP`, PDF `6SIYJNYL` and note `RX46EDUI` preceded intended body reading. The [CWI institutional PDF](https://ir.cwi.nl/pub/24029/24029B.pdf) is eighteen pages, 562,242 bytes, SHA-256 `1bb08cc704281dcb0432d666aa37a9259f7ed69c6a1f30068459c165e34be436`. All eighteen pages, seven figures, four tables, six listings and 32 references were read. PDF pages 1/3/5/9/11/14/15/16 were visually checked for layouts, algorithms, plots and tables. No appendix is present. Native attachment bytes were verified; the PDF and extracted text remain outside Git.

The advertised artifact URL resolves through the author's site to the renamed [public artifact repository](https://github.com/msteindorfer/research-paper-oopsla15-artifact/tree/f6e37eeaab74146f68657b394b75863909b8fe2d). The inspected commit is `f6e37eeaab74146f68657b394b75863909b8fe2d`, dated 5 January 2016. Its untruncated tree contains 781 entries. Thirteen selected files were downloaded individually, without cloning the repository or executing its programs. The README, map/set benchmark classes, footprint calculator/helper, dominator harness and two launch scripts were read completely; the R analysis was read selectively for loading, aggregation, filtering and ratios. The collection implementations, graph binary, generated plots and remaining repository are not fully inspected.

## Mechanism and assumptions

A hash-array mapped trie routes on successive chunks of a hash. A persistent update copies the affected path and shares unchanged branches. CHAMP changes the representation inside that family: separate bitmaps describe inline payloads and child nodes; one compact array stores payloads from one end and child references from the other. It removes null partners and some indirection, improves contiguous iteration, and retains compact singleton payloads after deletion. Canonical structure allows bitmap, subtree-identity and content comparisons to reject or accept equality with less traversal. Full-hash collisions still require content comparison, and valid hash/equality behavior remains an input obligation.

The iteration discussion's reduction from `O(m+n)` to `O(n)` concerns visited trie nodes, where `m` counts payloads and `n` child references. Enumerating `m` values still requires at least `m` outputs. With fixed branching width, this is a representation/traversal improvement, not sublinear enumeration of all elements.

Incrementally maintained collection hashes can occupy otherwise unused alignment space under the stated compressed-reference JVM layout. That layout argument is conditional, not free metadata on every runtime. Eager map-value hashing can be expensive for complex values. MEMCHAMP instead retains individual hashes in an extra array and omits the incremental collection hash; this is a distinct cost tradeoff, not an invariably better CHAMP.

The printed aggregate inequality relating branch size to child/payload arity is weaker by itself than requiring every child subtree to contain at least two payloads. A parent with child sizes one and three satisfies the aggregate bound. This is a limit of that isolated stated invariant; the update algorithm may maintain the stronger condition. No implementation defect is claimed from the inequality or pseudocode alone.

These mechanisms optimize immutable collections. They do not compare immutability with mutation, measure retained version histories, specify external-effect rollback, or prove safe live-state migration.

## What the measurements establish

The setup is JDK 8u25, Scala 2.11.6, Clojure 1.6.0, Fedora 20/kernel 3.17, an i7-2600 at 3.4GHz and 16GB RAM. Microbenchmarks use a 4GB heap, ten one-second warmup iterations and twenty one-second measurements, with collection between iterations. Five seeded collections are generated for each size. Random integers approximate uniform hashes; expensive hash/equality functions and adversarial collisions are outside that workload.

Eight selected operands exercise lookup/update operations. Every update in the inspected harness starts from the same collection and consumes its result through JMH's blackhole; it does not accumulate an application update history. Iteration consumes every yielded value. Independent and structurally shared equality cases are separate. The set-derived case inserts then deletes a new element; the pinned map-derived case changes an existing key's value and restores it. They are not identical update histories. Debug `main` methods use different settings from the actual launch scripts; the latter request one fork per seeded configuration.

The cached microbenchmark file has **9,120 unique rows**, exactly 24 sizes × five seeds × four implementations × nineteen operations: ten map and nine set operations. Each operation/size/implementation group has five rows. The R pipeline takes the median of the supplied per-row medians, then compares implementations. Its size filter excludes size one, leaving the paper's 23 sizes, `2^1` through `2^23`. These are equally represented sizes, not a sampled application operation mix. Cached relative MAD has median 0.08135% and maximum 4.9121%; low measurement dispersion does not establish representative workload or compilation context.

Independent Python arithmetic over the authors' cached numbers reproduces the principal comparisons below. Positive entries are median time savings across those 23 sizes, calculated as `100 × (1 − CHAMP/baseline)`.

| Operation | Maps vs Clojure | Maps vs Scala | Sets vs Scala |
| --- | ---: | ---: | ---: |
| Successful lookup | 72.39% | 22.60% | 12.52% |
| Insertion | 23.98% | 15.52% | 13.34% |
| Deletion | 31.81% | 25.22% | 17.06% |
| Key iteration | 82.68% | 48.29% | 22.05% |
| Equality, independently constructed | 95.92% | 81.39% | 66.22% |
| Missing-key lookup | 54.86% | 0.55% | −7.19% |
| Missing-key deletion | 43.60% | −13.34% | −12.71% |

The adverse cells are part of the result. Individual Scala comparisons are worse than the medians: set insertion is up to 27.88% slower, missing lookups about 24.5% slower, and small set iteration up to 4.22% slower. Near-100% rounded savings for derived equality mean a very large speedup, not zero runtime. MEMCHAMP's added memory and update/lookup costs violate the authors' stated tolerance in several comparisons; its favorable iteration/equality results do not erase those costs.

The two cached footprint files each have 960 rows. Their flags correspond to compressed versus uncompressed references in the launch script, not two independently described hardware systems. The footprint helper excludes `IValue` payload objects and measures collection overhead reachable from one root. Recomputed CHAMP map savings are 16.10%/23.46% versus Clojure and 67.98%/65.15% versus Scala for the two reference widths; set savings are 30.44%/41.49% and 52.16%/50.33%, respectively. MEMCHAMP maps instead use a median 14.98% more space than Clojure with compressed references. These detailed figure/data comparisons should not be silently substituted for differently summarized introductory percentages. They are not peak heap, allocation traffic or retained-history measurements.

## Application comparison and accounting boundaries

The application is a direct fixed-point dominator calculation over selected WordPress control-flow graphs, with nested collections and complex keys. It is a useful positive case, not an application-population sample or a comparison with the fastest dominator algorithm. Thirty cached rows cover five implementations/hash policies and six nominal graph counts, with ten measured executions per row.

Recalculation reproduces Tables 2/3. At nominal size 4,096, the original means are Clojure 1,685.70s, Scala 2,653.81s and CHAMP 169.65s: speedups of 9.94 and 15.64. Across sizes, the original speedups range from 9.94–28.13 against Clojure and 15.64–26.52 against Scala. They combine representation and hash-policy effects: Scala recomputes collection hashes, Clojure caches lazily, and CHAMP maintains them incrementally.

With all three using lazy collection hashes, the largest-case CHAMP time is 565.07s versus Scala 1,021.77s and Clojure 1,685.70s. The corresponding gains are 1.81 and 2.98; across all six sizes, roughly 1.81–1.90 and 2.88–3.17. This preserves a substantial scoped benefit while showing why the larger headline cannot be attributed entirely to locality or canonical structure.

The pinned artifact exposes three provenance/accounting limits:

- Its dominator script requests a **12GB heap**, whereas the microbenchmark script requests 4GB and the README mentions a 4GB requirement. Do not describe all artifact workloads as identically configured.
- Its graph sampling loop continues while the selected-index count is `<= size`, which would select **size + 1** distinct graphs from the stated 5,018-entry corpus. Published/cached labels remain nominal sizes; without identifying the exact historical measurement revision, this static observation does not prove the original timed counts.
- Cached footprint rows mark both CHAMP variants' staged-mutability flag false, whereas the pinned calculator passes true. That label does not enter the inspected ratio calculation. It does show that current source and cached measurement provenance should not be assumed identical.

Table 4 samples last-level-cache misses for the largest size and supports a locality explanation within that measurement. It is not a complete account of all cache events or an interactive latency bound. Qualitative ablation observations and authors' bug-avoidance claims are not controlled maintenance outcomes.

## Reconstruction provenance and implications

The microbenchmark CSV is 2,152,899 bytes, SHA-256 `7a576e0d94a11f50e991a39bc22d3be255f2040b3b54af81dcfc803851d5113b`; the dominator CSV is 3,607 bytes, SHA-256 `0eab3c6832f96d6d66f25fc658a32fa084c413ac42ac78e94a01be69659f2ada`. The compressed-reference footprint file is 61,737 bytes, SHA-256 `7b3135e87c64d55c450d7e16dceb25cd8d79869286e9ba3ecdea6e504aadf5dd`; the uncompressed file is 61,935 bytes, SHA-256 `016ec3ae7b25e2f9f91a9c533c980f10e9ceff8d673f75017d9b14366fe25cb6`. All are pinned under the repository's `oopsla15-benchmarks/resources/r/` directory. Local manifests retain thirteen source-file hashes. Arithmetic reconstruction of published data is **not** independent measurement reproduction; no Java, R, shell artifact, benchmark or author test was executed.

The result supports a concrete Nu-background inference: representation, hash policy, operation mix, sharing and runtime machinery can materially change the cost of functional state. A comparison must charge the relevant policy and retained roots, rather than assign a single cost to “immutable data.” These JVM results do not establish modern .NET, Nu, ECS, real-time, maintenance or agent effects.

**Unique:** established persistent-collection representation methods narrow any broad innovation claim; Nu/D1 priority remains unresolved. **Valuable:** substantial measured collection and selected-application benefits coexist with real adverse operations; whole-system benefit and history/latency costs remain distinct empirical questions. **Scientifically valid:** complete publication and bounded cached-data/source reconstruction; exact historical source correspondence, general workload transfer and newer measurement counterevidence remain qualified.

G18/SC77–80 and the primary web routes are tracked in the [background ledger](../nu-background-searches-2026-09-30.md). S144's collector and S145's reference-count/reuse methods are acquired and unread. [S146](S146-jvm-benchmark-context.md) is now fully read: it supplies context-sensitivity counterevidence without rerunning CHAMP. [S147](S147-benchmark-practices-partial.md) is partially reconstructed: its impact experiment excludes CHAMP, and released warning counts substantially include bundled JMH classes. These checks narrow negative as well as positive extrapolations. RRB vectors, persistent iterators, heterogeneous tries and compiler uses remain consequential conditional leads. No theme or experimental hold is closed.
