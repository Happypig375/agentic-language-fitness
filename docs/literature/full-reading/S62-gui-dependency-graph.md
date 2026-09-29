# S62 — GUI dependency ordering, addendum and comparator limits

**Full paper and addendum readings completed 2026-09-29.** João Paulo Oliveira Marum, H. Conrad Cunningham and J. Adam Jones, *Unified Library for Dependency-graph Reactivity on Web and Desktop User Interfaces*, ACMSE 2020, pp. 26–33, [DOI 10.1145/3374135.3385278](https://doi.org/10.1145/3374135.3385278). Zotero `NS8ISMNF`, main attachment `QI4UTDQI`, addendum `HURK5VXS`. All eight main pages, seven sections, two figures, two algorithms, four tables and 21 references were read; all five pages, three figures, four tables and four references of the July 17, 2020 addendum were read. Main pages 3–7 and addendum pages 2–4 were rendered and inspected. The addendum is a separate author supplement, not a second peer-reviewed experiment or a new full-work count.

| Source | Verified stored file |
| --- | --- |
| [Author-hosted main paper](https://john.cs.olemiss.edu/~hcc/papers/Marum_2020_ACMSE_Unified_Library.pdf) | 627,371 bytes; SHA-256 `065e88ca7628b214c8f5605597450b5331d2347831c328654bb910f20d2f7bc1` |
| [Author addendum](https://john.cs.olemiss.edu/~hcc/papers/Addendum_ACMSE_2020.pdf) | 844,909 bytes; SHA-256 `f23df93c126e8a310834fa3dfacdcbaab5dac73e91d7c83f00a3968a749a048d` |

Library-wide DOI/title checks preceded native-API import and upload. The author HTTPS certificate was expired and HTTP connections reset; two unauthenticated fixed-URL downloads used a request-local TLS verification exception, with no persistent configuration change. Crossref, first-page identities and stored-byte hashes were checked. No publication body is committed.

## Implemented mechanism and test scope

The C# library wraps controls with `IUpdatable`, getter/setter and target-discovery methods. An `IReactive` form supplies its own dispatch method. It constructs a graph from selected controls, checks changes before a reactive event, and directly invokes the affected chain. Cyclic dependencies are excluded from the graph and handled as ordinary events; the claimed ordering therefore does not cover every relationship. The paper explicitly requires balancing reactive and nonreactive work. This is close implementation prior art, not an intervention assigning functional versus imperative architecture to maintainers.

The reported test environment is Windows 10, .NET Framework 4.8, C# 8, Visual Studio 2019, Sodium 2.0 and one i5-5300U computer. Three form scenarios concern a shopping total, geometric calculations/unit conversions, and medical information. Later prose calls scenario 3 a metric converter, leaving that identity inconsistent. Web and desktop implementations are described, but the results do not separate their denominators. The paper gives neither an independent application sample nor a human satisfaction study.

Timing starts at the first button click and stops when the last control executes. That is not a measurement of when the user actually sees the final rendered result. The authors say exceptions/errors would prevent reaching the endpoint but do not fully specify censored/failed timing treatment. Inputs, warmup, run order, raw traces, uncertainty estimates and an exact released experiment build are not provided in these documents. Repeated executions of these forms are not independent applications.

## Reconstructed tables and discrepancies

The startup table values, in milliseconds, are:

| Implementation | Scenario 1 | Scenario 2 | Scenario 3 | Arithmetic mean |
| --- | ---: | ---: | ---: | ---: |
| Sodium, main paper | 29.58 | 30.65 | 31.12 | 30.45 |
| Rx.NET, addendum | 27.58 | 28.65 | 29.12 | 28.45 |
| Plain .NET, addendum | 21.24 | 20.45 | 22.28 | 21.32 |
| Proposed library, both | 51.24 | 55.45 | 58.28 | 54.99 |

The reconstructed mean overheads are 24.54, 26.54 and 33.67 ms respectively. These do not match the main prose's 0.35 seconds over Sodium or the addendum's 0.30/0.35 seconds over Rx.NET/.NET. S59's approximate 55/21 ms summary is consistent with the addendum table and implies about 2.58 times startup, not a net runtime-benefit estimate.

The main paper claims form completion in 10–20% of Sodium's time. Figure 2 labels milliseconds, with series roughly below 1 versus 3–6, while the prose describes seconds. The addendum claims 30% of Rx.NET and 50% of .NET time; its plots show fifty execution positions and do not supply raw values or clear timing units. Do not silently normalize these discrepancies or digitize visual series into an independently reproduced speedup.

Accuracy entries are retained as printed:

| Source and implementation | Cycles per scenario | Total errors, scenarios 1/2/3 | “Avg Errors / Cycle”, scenarios 1/2/3 | Latency in cycles, scenarios 1/2/3 |
| --- | ---: | --- | --- | --- |
| Main: Sodium | 50 | 8 / 6 / 7 | 2 / 1 / 1 | 1 / 1 / 1 |
| Main: proposed library | 50 | 3 / 2 / 3 | 1 / 1 / 1 | 1 / 1 / 1 |
| Addendum: Rx.NET | 500 | 9 / 8 / 10 | 2 / 2 / 2 | 1 / 1 / 1 |
| Addendum: plain .NET | 500 | 12 / 20 / 16 | 5 / 1 / 1 | 3 / 5 / 4 |
| Addendum: proposed library | 500 | 3 / 2 / 3 | 1 / 1 / 1 | 1 / 1 / 1 |

Methods define an average conditional on runs with errors, whereas the column label says per cycle and the relationship between “Total Errors,” affected runs and multiple component errors is unresolved. The prose's roughly 15% Sodium figure is not enough to resolve that denominator. The addendum changes 50 to 500 while retaining the library's error/startup values and displaying fifty timing points; it does not explain whether these are new runs, reuse or a label error. Its reference 3 also gives the VR paper's title with the GUI conference venue. Preserve the document's title/date and its actual scope rather than silently repairing identities or merging results.

All proposed-library rows still contain errors. S59's five-to-one error entry is scenario 1's conditional/mislabeled average; scenarios 2/3 are one-to-one. The addendum's .NET latency entries average four versus one, but cycles have no demonstrated common wall-clock duration. Neither ratio proves a user-perception or maintenance advantage.

## Algorithm and comparator checks

The rendered algorithms contain underspecified steps: initial queues are seeded with one control but no further enqueue operation is shown; variable names alternate (`P`, `cont`, `C`); deletion behavior claimed by the prose is absent from the printed update routine. Calling a breadth-first traversal a valid update order does not by itself establish topological order. For example, edges A→B, A→C, C→D, D→B allow an ordinary BFS to visit B before its prerequisite D. This is a reasoning check on the printed description, not execution of the authors' implementation.

The general claim that .NET events rely exclusively on asynchronous calls is too broad. Microsoft's [C# event guide](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/events/) documents synchronous invocation of subscribed handlers. Queued UI input, an ordinary event invocation, an asynchronous handler, a reactive transaction and a paint operation need distinct boundaries. This does not prove that the benchmark lacked asynchronous work.

A bounded source check also challenges the broad characterization that Sodium lacks dependency scheduling or direct stream composition. The checked snapshot is commit [`66228ccc47ccc6f1e89c6e6bbef5a28d3a4ace22`](https://github.com/SodiumFRP/sodium/tree/66228ccc47ccc6f1e89c6e6bbef5a28d3a4ace22), dated 2020-02-03, selected as the latest dotnet change before March 2020. It is not established as the paper's exact Sodium 2.0 build.

| Checked source | Actual inspection and implication |
| --- | --- |
| [Node.cs](https://github.com/SodiumFRP/sodium/blob/66228ccc47ccc6f1e89c6e6bbef5a28d3a4ace22/dotnet/src/Sodium/Sodium.Core.Frp/Node.cs) | Entire file; links adjust dependent ranks and detect dependency cycles. 4,945 bytes, SHA-256 `9f4f1e27803da7bb79e16f86d59948370ac4ef98219a38a7c3a3915b7aa98f43`. |
| [Transaction.cs](https://github.com/SodiumFRP/sodium/blob/66228ccc47ccc6f1e89c6e6bbef5a28d3a4ace22/dotnet/src/Sodium/Sodium.Core.Frp/Transaction.cs) | Entire file; a rank-prioritized queue is rebuilt after rank changes and drained during transaction close. 12,887 bytes, SHA-256 `d91d1c162e8e0c27cb7d5a0ac3eb27dc1d57d8b529cd837b2e4caa257bd03987`. |
| [Stream.cs](https://github.com/SodiumFRP/sodium/blob/66228ccc47ccc6f1e89c6e6bbef5a28d3a4ace22/dotnet/src/Sodium/Sodium.Core.Frp/Stream.cs) | Only lines 117–169, 259–299 and 423–473 read in context: listening/mapping/merging link nodes and sending schedules callbacks by rank. Whole downloaded file 22,045 bytes, SHA-256 `823e95b005408b237ea4667e9d9805454eb86b7644308f61e760f60b8f127df4`. |

No Sodium source, test or GUI program was executed. These observations do not establish correct handling of arbitrary external controls or the fairness of the paper's particular comparator. They do require inspecting application-level boundaries before attributing its timings/errors to a library's intrinsic inability.

## Three criteria and follow-up

**Unique:** dependency-aware GUI chains and runtime graph updates predate the Nu question. **Valuable:** the authors report promising local timing and ordering results, but residual errors, ambiguous denominators, conflicting units and unmeasured human outcomes limit transfer. **Scientifically valid:** compare faithful implementations under common obligations, validate event/transaction/rendering boundaries, retain failed attempts, and measure startup, recurring and maintenance costs. These limitations do not validate Nu or authorize a new experiment.

The incoming twenty-edge Scite request returned only S59 and flagged low coverage. The exact backward-title request used twenty records and returned two DOI editions of Foust/Järvi/Parent's 2015 multi-way GUI constraints paper (`10.1145/2814204.2814207`, SIGPLAN alias `10.1145/2936314.2814207`). An author-constrained twenty-record reformulation found the 2017 FRP/DOM experience report (`10.1145/3079368.3079405`) plus Gavial and safe boundary APIs. These remain conditional for exact GUI-boundary or multi-way constraint comparisons, not newly full-read support. The current benchmark interpretation can be narrowed using the actual paper, addendum and bounded primary checks above; exhaustive reconstruction of each alternative framework is not claimed.
