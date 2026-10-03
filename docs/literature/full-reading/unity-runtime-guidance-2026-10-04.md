# Versioned Unity pooling and collector contracts

Main-agent primary-documentation/source inspection, **2026-10-04 HKT**. This supplements B04/B06/B12 and the empirical [S239](S239-unity-mobile-optimization.md)/[partial S240](S240-endless-runner-pooling-partial.md) readings. It is **normative mechanism and static-source evidence**, not another performance study, a whole-manual reading or a Nu runtime measurement. No Unity project, package, author program or benchmark runs.

## Sources, native records and actual coverage

All five selected pages have native records in **`PKLXQNEE`** before selected reading. Registration checks1266 top-level and260 collection items initially; the two follow-ups check the then-current library by exact versioned URL. Existing keys and memberships are preserved.

| Primary source | Native parent / note | Coverage |
| --- | --- | --- |
| [Unity6000.0 pooling and reuse](https://docs.unity.com/en-us/engine/6000.0/manual/scripting/optimization/performance-optimizing-code-managed-memory/reusable-code) | `AWKW6458` / `265UGZAW` | Complete served article text, both projectile/gun listings and collection examples; no substantive images. Version selector says6000.0; read date binds the revisable documentation. |
| [Unity6000.0 collector overview](https://docs.unity3d.com/6000.0/Documentation/Manual/performance-garbage-collector.html) | `IWFBSQCW` / `6YQ2MIMR` | Complete overview, reallocation and temporary-allocation sections; no substantive images. |
| [Unity6000.0 collector modes](https://docs.unity3d.com/6000.0/Documentation/Manual/performance-incremental-garbage-collection.html) | `8TDKTWJT` / `38G62ANC` | Complete incremental, non-incremental and manual sections; both original profiler images visually inspected. |
| [Unity6000.0 pool constructor](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Pool.ObjectPool_1-ctor.html) | `3B3BQ894` / `VDY5JMSW` | Complete declaration, parameter table and particle-system example. |
| [Unity2020.2 script optimization](https://docs.unity.cn/2020.2/Documentation/Manual/MobileOptimizationPracticalScriptingOptimizations.html) | `BLTGZ67M` / `U3S9IY65` | Selected introductory/profiling and allocation/pooling sections through “Why Object Pooling can be Slower”; opening of the following legacy code listing. Remaining script/physics/rendering examples and two coin illustrations are not read. No complete-page claim. |

The three legacy-host6000.0 pages identify documentation build **76410965, 2026-09-29**. The newer pooling page has a6000.0 selector and a relative update label, without a verified matching documentation commit. Do not assume all page bodies froze at the engine's initial release. The2020.2 page is historical guidance; unrelated simplifications in its general language explanation are not adopted as current C# allocation rules.

The official **UnityCsReference6000.0 branch** resolves to **`0c7f0bfc4f9b21d3d84fffc9ee9001ad82f0fbc4`**, labelled **Unity6000.0.84f1**, committed16 September2026. Its complete untruncated inventory has **5,702 entries**. Read **all178 lines** of [ObjectPools.cs](https://github.com/Unity-Technologies/UnityCsReference/blob/0c7f0bfc4f9b21d3d84fffc9ee9001ad82f0fbc4/Runtime/Export/ObjectPool/ObjectPools.cs), **7,138 bytes**, SHA-256 **`4bf5f1c3f5a5113f04fe1a80a04e1f0627ae5ad333e7f94f163316cf1eaaece9`**. Native linked-source attachment **`YZ76CNGF`** under the constructor record is created before this source read. The reference file is not a reproduced Player build or a whole-engine source review.

## What pooling does and does not promise

The current API separates creating, taking, returning and destroying an instance through caller-supplied callbacks. Reuse requires a behavioral reset policy, including position/health/physics, events, coroutines and other component-specific state. Scene unloading and longer-lived pools need an explicit ownership/lifetime policy. Generic pooling APIs supply storage and callbacks; they cannot establish application-specific state restoration.

The constructor documentation and source distinguish **storage capacity from prewarming**. `defaultCapacity` reserves the internal list's capacity; it does not create that many objects. In the source, `Get` creates an instance whenever no inactive one is available, increments `CountAll`, and then invokes the get callback. It does **not** compare the checked-out count with `maxSize`. The maximum bounds retained inactive instances on return, not concurrent active objects or total process memory. The generic pool invokes an optional destroy callback for excess returns; actually destroying a Unity GameObject depends on the supplied callback.

`Clear` handles inactive storage and resets its accounting; it does not walk an independent list of all active borrowers. Ownership, outstanding returns and scene transitions remain caller obligations. Clearing/reusing collections retains their backing capacity until that representation changes, so fewer allocations can coexist with a larger retained footprint. The historical2020.2 guide explicitly identifies oversized pools and larger live heaps as possible causes of worse collection behavior. This is a vendor-described conditional cost, not a measured universal threshold.

Two documentation/source differences are kept scoped. The current tutorial prints a `Get` overload with a `PooledObject` out-parameter; the pinned source actually returns `PooledObject<T>` and writes the borrowed **T** to the out-parameter. The pages and source comment describe double-release checks as Editor-only, while the selected implementation's visible guard is the runtime `m_CollectionCheck` field without an Editor conditional. The complete Player build path is not inspected or executed, so no general Player-behavior or reproduced-bug claim follows. These details prevent treating explanatory prose as a compiled behavioral oracle.

## Collector work, scheduling and retention

The6000.0 modes page identifies **Boehm–Demers–Weiser**, incremental by default on supported targets, with the web platform outside incremental support. The collector is non-compacting. Incremental operation spreads work across frames; it does not imply less total work. VSync/target-frame-rate slack can absorb some work, so the same average FPS can conceal different scheduling and headroom.

Changed references introduce write-barrier and rescanning work. The guide explicitly allows fallback to a full collection when incremental marking cannot keep up. Disabling collection instead retains unreachable managed allocations until collection resumes, shifting risk to heap growth. Neither option is a measured universally preferable setting here. Retained roots keep objects live: collection cannot release reachable pooled objects or retained versions merely because application code no longer needs their contents.

The two profiler pictures illustrate spread work versus one larger pause. Their vertical scales differ: the incremental example is shown around the16ms/60FPS scale, while the non-incremental picture also marks33ms and66ms. They are documentation illustrations without a released workload, repetition schedule or tail distribution. They do not establish a percentage effect, a worst-case deadline bound or modern Nu behavior. A Unity version and collector configuration must not be silently equated with another .NET runtime because both execute C#.

## Evidence consequence

The empirical papers and this contract inspection now support a coherent distinction: **reuse policy changes allocation traffic and object lifecycle; retained roots change live memory; collector mode changes scheduling and barrier work; rendering can dominate the realized frame rate**. A favorable bundled game result and a larger pool can coexist. More source cases or stronger types do not, by themselves, determine these quantities.

Current Unity collector/pool semantics are no longer an unread mechanism gap at this selected scope. S240's visual evidence remains an access gap. Net effects for Nu, long retained histories, frame tails and actual change effort remain empirical questions with runtime/workload-specific discovery still incomplete. Further literature should target a claim-changing measurement or a consequential alternative; another general pooling tutorial cannot resolve those questions. C05 type/context/multi-turn evidence remains an independent next frontier. No full-paper count is added and all construction holds remain.

## Local source identities

Raw publisher HTML, extracted text and images remain outside public Git. Acquired HTML identities are:

| Page | Bytes | SHA-256 |
| --- | ---: | --- |
| 6000.0 pooling | 1,076,780 | `0f696b9a68d89cfb497ece9a69d3d5b3467940e5b163ffa5dd342975c550e2ae` |
| 6000.0 overview | 15,133 | `dcd99b04f75e0384089206ddb7f79011c68fe857fdc39aa37929e5fbbf3d632f` |
| 6000.0 modes | 22,568 | `a8e6a825b4b7676fdd5fe34004ff8435eb47cc0f47428c75b489d6fae47e608c` |
| 6000.0 constructor | 23,074 | `d09290e17efb10f5a2d361cab7f27c46587085df91590bcf357e82ea524076f2` |
| 2020.2 optimization | 53,491 | `52755c27955bc519bd2f793ce025ed59c97f7f49b7f34e37c7d56fc1d47b30d9` |

The incremental/non-incremental image files contain **34,278 /31,039 bytes** with SHA-256 **`b2d337f33a6279e9396019357e4caffd41f57c9ed8e8abe52c24fe82c5b953e3` / `57b6a5392a644b83ae1f0808483730afc1f14936b353726d132acaa0d7b66a8e`**. Their bytes are inspected locally; no equivalence with older manual illustrations is inferred.
