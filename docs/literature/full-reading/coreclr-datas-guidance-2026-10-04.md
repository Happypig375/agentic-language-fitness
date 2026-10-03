# CoreCLR DATAS: memory, throughput and pause observations

Main-agent source inspection, 2026-10-04. This is **official documentation and an architect's technical report**, not another peer-reviewed paper, independent replication or runtime reproduction. It complements the [Unity contract check](unity-runtime-guidance-2026-10-04.md), whose collector/runtime cannot stand in for CoreCLR.

Native parent **`BS5APE7A`5495** and note **`JBM56ZAF`5496** were created after DOI/title/URL checks of1,276 top-level/270 collection records and before selected DATAS reading. Earlier search snippets are bounded automatic exposure. The public-source record groups the Learn contract with its dated architect companion; their evidence roles remain separate.

## Source identity and actual coverage

| Source | Inspected extent and identity |
| --- | --- |
| [Microsoft Learn: DATAS](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/datas) | Entire technical text and both linked figures. Pinned [Markdown](https://github.com/dotnet/docs/blob/641989c37ca888cab4dbee859c8d57aa7109c95d/docs/standard/garbage-collection/datas.md), **`641989c37ca888cab4dbee859c8d57aa7109c95d`**,3,652 bytes, SHA-256 **`c25dc87809142283a1442e4eab5121115b28235694511160a14572cc11189b45`**. Source metadata date9August2024 differs from rendered page's13August update label. |
| Learn figures | `workingset.png`,17,762 bytes, SHA-256 **`8aa6f882160d556406095953d9d049869856930adf0b4ee0c30ceba8a3a21599`**; `gen0-gc.png`,56,991 bytes, SHA-256 **`436a53e1a8fec88a9672bef28b04cdac26d8b90ef038e50329e2363d0e19e2fc`**. Both viewed at full supplied resolution. |
| [Maoni Stephens: Preparing for the .NET10 GC](https://devblogs.microsoft.com/dotnet/preparing-for-dotnet-10-gc/) | Dated8October2025; entire technical article through DATAS Events, all four tables and all eight figures, including the final two-panel figure. Web pagination recovered the second customer case/end. Reader comments are not credited evidence. Captured HTML307,410 bytes, SHA-256 **`33112d029fffed93c7859c751b2a6886cf031895b4400baaddd716bd8c02e672`**; eight figure hashes retained locally. |

The locally assembled **14-member** source/figure bundle is native **`K8Z58LUW`5501**,404,880 bytes, SHA-256 **`969807cee2aa0e6c7e697481dba527ed5d624de4f98c770c4b449260c7f4780c`**, MD5 `e18a6466f83992400303e851ec8d3609`. Stored bytes are hash-verified. No published benchmark, tracing tool, GC configuration or application is run or changed.

## Contract and measured trade-offs

Learn describes an adaptive **server-GC** policy, opt-in in.NET8 and default from.NET9. It bounds allocation budgets using long-lived data, adjusts actual budgets for throughput, varies heap count from one, and can compact to control fragmentation. Its48-core Linux TechEmpower JSON/Fortunes report combines **over80% working-set reduction with2–3% maximum-throughput loss**. The first figure is labeled **P90 working set**, not a latency percentile; the second plots collection counts per second. These remain version/workload-specific author results.

The architect's later report supplies a counterweight: one customer's defaults reduce working set10% but throughput6.8%, prompting disablement. Another staging case improves pauses after tuning and shrinking client load. Its tuned plots use more heap than default DATAS, preserving a cost trade-off. TCP includes pauses and allocation waiting; its2% default is an aggregate cost target, not a maximum-pause guarantee. Startup, allocation shape, live data, heap-count overrides and tuning matter. The case traces and formulas illustrate mechanisms without supplying a released matched trial/uncertainty packet.

## Consequence for Nu and evaluation

The source observations support separating **allocation traffic, live reachable data, managed heap, process working set, collection frequency, individual pause duration and end-to-end frame time**. The axes also differ: dates and GC indices are not interchangeable elapsed-time or frame denominators. More frequent smaller pauses can change event-weighted distributions while leaving a different amount of application time affected.

For Nu, retaining additional world roots could change the live-data workload as well as allocation/reclamation opportunities. This is a mechanism inference, **not a measured DATAS or Nu result**. DATAS applicability requires the actual deployment's runtime and effective GC mode/configuration; no claim that the pinned Nu build uses it is made here. Neither report varies immutable-history depth or measures game frames, new/retained behavior, maintenance effort or source-convention effects.

B04/B06's runtime gap is therefore more precise: seek a primary retained-history/interactive measurement with bound runtime/configuration, represented state and elapsed-time/frame observations. Reuse these positive/adverse trade-offs when interpreting it. [S245 Fsge](S245-fsge-access-and-source.md) now supplies a complete favorable sprite-workload comparison; its renderer differences, missing matched raw measurements and absence of a history-depth contrast preserve the transfer boundary. Construction and runtime/model holds remain unchanged.
