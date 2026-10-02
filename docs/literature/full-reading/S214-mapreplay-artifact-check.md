# S214 — bounded MapReplay source and release inspection

This accompanies the [complete paper reading](S214-mapreplay.md). Source and published-data inspection are passive. No build, install, JVM, author script, trace replay, benchmark or statistical experiment is run.

## Identity, acquisition and coverage

The [public repository](https://github.com/usi-dag/MapReplay) is pinned at **`bf32f5a41830ac695273e9da9f46b156f71a31ce`**, May 6, 2026. Its [commit archive](https://codeload.github.com/usi-dag/MapReplay/zip/bf32f5a41830ac695273e9da9f46b156f71a31ce) is 86,916 bytes, SHA-256 `5f73b13ccc839acec420e9ed669313e43a6a10c3e4785f5776491e5bc283b0e3`, MD5 `fe8ba9aa2e49f01d4d9a0ca952dd27d9`; 26 regular files total 292,134 uncompressed bytes. Native attachment **`UCGN6PUV`v5104** is read back under S214.

The [v0.1.0 release](https://github.com/usi-dag/MapReplay/releases/tag/v0.1.0), published May 6, tags **`463a3a110c2fb5019521b71278f286adc89f2677`**. Its source ZIP is 81,741 bytes, SHA-256 `67522e8b65db60d380ff126a1a9006e99120417482e82a111fa4983d0c413666`, MD5 `8ae801039b38032b485e904858ea6722`, native **`BIIUK7IR`v5106**. All 25 non-README files are byte-identical to the pinned main archive. The README difference removes a nonexistent documentation directory from the displayed tree; remaining links still refer to unavailable documents. Neither package contains the named docs, experiment outputs, capacity patches or analysis scripts. This bounded inventory is not a claim that no further artifact exists elsewhere.

Nine complete source/text files are read, with paths relative to the pin:

- `README.md`;
- `replay/src/main/java/ch/usi/inf/dag/mapreplay/replay/JMHBenchmark.java`;
- `postprocessor/src/main/java/ch/usi/inf/dag/mapreplay/postprocess/TracePostProcessor.java`;
- `tracer/src/native/mapreplay_tracer.c`;
- `tracer/src/java-agent/ch/usi/inf/dag/mapreplay/tracer/agent/TracerActivator.java`;
- `tracer/src/java-base-patch/jdk/internal/mapreplay/NativeTracer.java`;
- `tracer/test/smoke/SmokeHashMap.java`;
- `replay/pom.xml`;
- `trace-format/src/main/java/ch/usi/inf/dag/mapreplay/trace/TraceInstructionCodec.java`.

Selected `tracer/src/java-base-patch/java/util/HashMap.java` ranges **280–336, 417–590, 625–689, 879–933, 1247–1383, 1824–1911 and 2185–2230**, plus identified tracing-call search contexts, cover node/key identity, constructors/copying, lookup/update, compute, iterator behavior and node allocation. The whole HashMap, LinkedHashMap, Event hierarchy and build system are not credited as fully read.

The benchmark ZIP is **1,955,476,099 bytes**; the release declares SHA-256 `29070c8d1b3c08bf7d83d535790b9ab5baacbcd17b12daa7d89c25cfe2ddfae8`. This whole-file hash is **not independently verified**, because only supported HTTP byte ranges were acquired. Its complete outer central-directory inventory is inspected from bytes **1,955,410,542–1,955,476,098**. The inventory contains 46 trace ZIPs, two launch scripts, one replay JAR and README; there are no top-level measured results or statistical scripts. Trace ZIP contents other than the one named below remain uninspected.

Three complete release text members are read: `README.txt` (739 bytes), `bin/run-mapreplaybench` (1,094 bytes) and `run.sh` (145 bytes). Their SHA-256 values are respectively `1c5db019c7be6bcc23420aed2f3bbaf416c51059fa01b16c8fd697a98d04a89b`, `d799afd6911118c9560c0357d22ecac1d1f1c5a01d511008496f666037cef6d5` and `22468fb064a0cb05895c6f02f9349d165752ecfb8450ebae01c61bac906e86ca`. README is native **`BRJ54DVN`v5110**. Ordinary range requests for the scripts were bytes 164–1,689 and 2,566,867–2,568,021; the README was already in the acquired tail. Member decompression and CRC checks pass; scripts are only read.

One complete stored member, `traces/dacapo-chopin-jme.zip`, is acquired through bytes **366,782,976–366,815,964**, verified against its outer-directory CRC, and attached as a clearly identified subset: **31,965 bytes**, SHA-256 `0b6b59ca5f4b291effc7084265e210b033eb9006ad0ea3277462b517e8367db4`, MD5 `b55eb2c1ae6669b764bf9c82f8829bcb`, native **`927PJQ79`v5108**. Its five-member inventory is inspected. Only the two metadata CSVs are fully read; binary operation/key arrays are neither analyzed as a full trace nor replayed. Copyrighted bodies, archives, extracts and acquired byte ranges remain outside public Git.

## What the source establishes

**Pipeline and measurement boundary.** `NativeTracer` uses synchronized event registration around native field writes, and the activation agent enables it after early initialization. Postprocessing removes unsupported spliterator primitives and events without a known constructor, creates map/iterator frees at last use, and recycles array slots. `JMHBenchmark.setup()` creates mock keys and trace arrays at trial scope and explicitly invokes GC. Timed replay creates maps/iterators and uses a Blackhole for selected results. Annotation settings match the paper's five forks and five 10-second warmup/measurement iterations. These are concrete implementation mechanisms; neither the source nor the smoke sequence supplies observed trace equivalence or performance results.

**Cross-map key correspondence has a static counterexample.** `HashMap.nextKeyID` starts at zero in each map (line 445), with new nodes consuming that local counter (2198–2209). Replay interns mock keys globally by `(id, hash)` (114–125), and mock equality is inherited identity equality (32–46). Replay `putAll` uses the source replay map directly (176–177). Consider two fresh maps, each containing one distinct, unequal key with hash 7. Both first nodes have ID 0, so replay gives both entries the same mock object. Merging these maps retains one replay entry where the original merge retains two. This conclusion follows from the inspected definitions; it is not an executed test or evidence that this case occurred in the paper. The byte-identical release source shares the issue. It qualifies universal preservation of key relations and map sizes, leaving the impact on measured comparisons unknown.

**Traversal preservation is narrower than unrestricted API coverage.** Postprocessor lines 311–314 delete `tryAdvance` and `trySplit` events. Iterator coalescing (401–440) tests whether that iterator performs remove; it is not a general check of intervening map mutation. Replay coalesced traversal always uses a fresh key iterator, even for original values/entries. Non-coalesced iterator removals act on the replay traversal order, with no expected-key assertion. These choices may be suitable for subsets of workloads, but the source provides no universal state/control-flow proof. No observed numerical effect is assigned to them.

**State and callback abstractions remain conditional.** All ordinary stored values become the same non-null placeholder. `computeIfAbsent` distinguishes null/non-null mapping results, but a prior stored null becomes non-null in replay; its callback path therefore need not match. An absent null-producing mapping records sentinel hash −1 (HashMap 1355–1360), rather than necessarily the original key hash. Canonical keys eliminate original equality behavior, and keys are retained in the trial array even when maps are freed. Thus hash/collision fidelity and lifetime equivalence require scope beyond the names of retained operations. Exceptions and arbitrary effects are not validated by consuming return values.

These limitations do not erase the method's useful separation of workload acquisition from repeated measurements. They identify assumptions requiring validation before transferring its reported agreement to another runtime, representation or application.

## Released workload and experiment correspondence

The release README states 46 traces, and the inventory confirms them. All 43 paper-table workload names occur; **cassandra, tradebeans and tradesoap** are additional DaCapo traces. The launcher selects every `traces/*.zip` by default, not the paper's 34 retained performance cases. The source/release settings expose a convenient executable package but not the full DIC variant construction, application warmup treatment or bootstrap/correlation analysis used for the paper.

The acquired JME metadata reports **8,603 events**, **463 constructor events** (389 default and 74 with parameters), **463 frees**, and **50 map slots**. Slot count is not cumulative map construction count. Paper Table 1 instead reports **11,189 events and 911 constructors**. The current member is also 31,965 bytes versus the paper's rounded 36K trace size. These differences establish unresolved input/run lineage; they do not establish why the traces differ or invalidate an unacquired original trace. C-jme was excluded from the paper's performance comparison, so this discrepancy does not directly correct a reported timing cell.

Trace inputs, source availability, a smoke sequence and actual reproduced measurements remain distinct. The 24,405,616-byte Linux binary asset is metadata-only, and the full benchmark ZIP/JAR are not run. Exact original input hashes, variant patches, output rows and analysis would settle more of the correspondence; no new experiment is authorized to fill those gaps.
