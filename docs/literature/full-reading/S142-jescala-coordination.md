# S142 — JEScala coordination, semantics and costs

**Full publication reading, 2026-10-02 HKT.** Jurgen M. Van Ham, Guido Salvaneschi, Mira Mezini and Jacques Noyé, *JEScala: Modular Coordination with Declarative Events and Joins*, MODULARITY 2014, pp. 205–216, DOI [10.1145/2577080.2577082](https://doi.org/10.1145/2577080.2577082). JEScala integrates explicit, implicit and composed events with join patterns at object granularity. Its examples demonstrate less handwritten event emission and some smaller programs; its performance results depend strongly on workload, compilation and scheduling. These are mechanism and prototype observations, without a measured maintenance benefit or general concurrency-safety result.

Native Zotero **`Z8CPMTIR` / note `4HLXKAWX` / PDF `R7E38U3P`** existed before reading and were reverified at versions **3615/3612/3613**. The [author-hosted proceedings-layout copy](https://www.rescala-lang.com/assets/pdf/2014%20JEScala.pdf) is **twelve pages, 620,061 bytes**, SHA-256 `3411fd9d15b36dbacd21df28a0dc0334c3edd481962ca2a449bceba10cdb9bc6`. All twelve pages, all sections and 36 references were read as text. Visual pages **1–3,5–11** cover all thirteen numbered figures, including the two tabular figures, grammar fragments, code listings and graphs. Pages 4/12 are text-only. No appendix or separately numbered table is present; no official-publisher byte comparison or author-code execution is claimed.

## What the mechanism changes

Ordinary join languages coordinate arrivals on several channels: a reaction becomes eligible when all its required arrivals are available, and competing reactions select one set. JEScala adds EScala's composable event model. Events are object members/values; the event source, handlers and bindings can reside in different objects. Multiple listeners provide implicit invocation, and binding can change at runtime. An emission can therefore reach several independent consumers rather than one method body.

The main event forms have different contracts:

| Form | Meaning and obligation |
| --- | --- |
| Imperative event | Explicitly emitted; `sync` or `async` is declared at the source, with synchronous default |
| Implicit event | Observes entry/exit of a named method, with synchronous/asynchronous variants. External observation is limited to methods exposed through the class interface |
| Declarative event | Composes other events using union, filtering or mapping; inherits the triggering occurrence's synchronicity |
| Forced asynchronous expression | `!!` moves the composed event to asynchronous handling |
| Join/disjunction | Waits for a combination, consumes its participating arrivals within that disjunction and emits a new composable result event |

An abstract event has no declared synchronicity because an override can be primitive or composed. A composed event's execution mode can depend on the occurrence reaching it. Thus event identity and a static declaration alone do not establish where every handler runs or whether it can block. A synchronous handler can itself start asynchronous work.

Disjunctions are explicit groups, and a class can contain more than one. Sharing an event among alternatives creates competition within that group; separate groups are not one global consuming pool. A subclass may replace a disjunction as a whole, but cannot add an alternative to an existing inherited group. This restriction addresses interference between inherited and added reactions; it does not prove deadlock freedom for arbitrary compositions.

The running web-server example moves observation of request entry and token generation out of the application bodies into coordination expressions. State is represented by pending `free`/`busy` events; handlers re-emit a state event to maintain the intended invariant. A later version uses separate request/grant events, timestamps and filters to distribute admission opportunities and reject expired tokens. Expiration here is application logic, not an implemented general time-window algebra or a guarantee of bounded retained queues.

Dynamic registration lets a statistics component attach to the state-transition events without changing the rate limiter. Explicit enable/disable handlers and a flag prevent intended duplicate registration. This illustrates separable instrumentation, while subscription identity, appropriate removal and mutable statistics state remain program obligations. The paper supplies no object-destruction policy that automatically proves all event references and pending work have been released.

## Propagation, blocking and selection

The implementation maintains a graph of event dependencies. Triggering a primitive event traverses reachable nodes depth first, evaluates filters and collects handlers, then executes the collected handlers sequentially. An asynchronous occurrence uses a separate execution thread; thread-local collection buffers and protection of handler lists support concurrent activity on the graph. Deployment/undeployment skips graph nodes with neither outgoing dependencies nor handlers.

Each disjunction maintains a queue per participating event. An unmatched arrival remains queued. A match removes the participating arrivals and fires the result event; competing eligible patterns are selected nondeterministically. The implementation randomly chooses among matching patterns as a fairness measure. This is not a demonstrated deadline, starvation bound or deterministic replay policy.

For a synchronous unmatched arrival, the caller blocks and its thread is stored with the arguments. When a pattern matches, its first synchronous participant's thread executes the result handlers. Queue insertion normally becomes a deferred handler so collecting other handlers need not block immediately. The paper does not provide a complete operational proof covering every combination of blocked callers, concurrent graph changes and application effects; its conclusion explicitly retains deadlocks from mixed synchronous/asynchronous events as a challenge.

Three optimizations move the costs:

- A thread pool reuses workers instead of creating a thread for every asynchronous occurrence. Work can wait when workers are occupied; asynchronous execution alone is not a latency guarantee.
- If an asynchronous event only propagates to disjunctions, insertion can occur during collection without a separate queue-insertion handler/thread.
- Parameterless asynchronous events can use counters instead of storing argument records. Synchronous arrivals still need their waiting threads represented.

The counter paragraph first restricts the optimization to asynchronous events, then names a synchronous primitive in its parenthetical example. That is a printed inconsistency, not verified implementation behavior. Released-source access would be needed to settle the actual condition. At publication, the implementation is a **library**, with compiler support still planned for a stable Scala 2.11 release. Surface-language examples and the available prototype should not be assumed to be identical compiled artifacts.

## Compactness evidence and the actual comparison

The authors construct 34 small example rows, including synchronization patterns, single-/multi-threaded variants, simulations and web-server versions. Their **JL** comparison is a restricted JEScala subset encoding a hypothetical Polyphonic Scala style. It is not a separately recruited team, an independently optimized library or a direct production-language maintenance experiment. The authors deliberately choose small synthetic coordination examples to expose the mechanisms.

Figure 8 reports CLOC source lines excluding comments/whitespace, event declarations, handlers and explicit triggering sites. Our passive arithmetic over all printed rows gives:

| Count | JEScala lower / equal / higher across 34 rows | JL total | JEScala total |
| --- | --- | --- | --- |
| Source lines | 31 / 2 / 1 | 2,764 | 2,532 |
| Event declarations | 10 / 12 / 12 | 324 | 320 |
| Handlers | 23 / 9 / 2 | 223 | 101 |
| Imperative triggering sites | 34 / 0 / 0 | 302 | 118 |

These figures substantiate a consistent reduction in explicit emission sites and substantial movement of logic from handlers into event expressions. They also preserve exceptions: the multithreaded token-ring row is one line larger; two rows have more handlers; twelve have more event declarations. Totals across related synthetic variants are descriptive sums, not independent observations or a statistical effect estimate.

The table does not measure time to understand or modify a program, residual faults, missed event notifications or implementation effort. Moving an emission to an implicit/composite expression removes that particular handwritten call; it still requires choosing the correct observation, filter, mapping and composition. The mechanism is useful without assuming that authors or coding agents cannot omit a necessary dependency. Existing adverse E/H compactness observations remain unchanged.

## Runtime evidence, including the unfavorable comparisons

The reported environment is a two-core 2.66GHz MacBookPro6,2, 8GB RAM, OS X 10.6.8, Java 6 and Scala 2.10. These are historical measurements, not present-day product performance or Nu workload estimates.

**State-machine throughput:** Figure 9 compares Scala Joins, JEScala, Esper, JoCaml and Cω using an automaton, varying one to five states. The dedicated-compiler systems have much higher throughput in the displayed benchmark. The prose says JEScala slightly outperforms Scala Joins, but the plotted JEScala bar is **lower**. With no raw values or recovered benchmark package, that small relative ordering remains a figure/prose discrepancy. Preserve the broader observed ranking without selecting the favorable wording.

**Pattern complexity:** Figure 10 varies both pattern/disjunction size from two to six and normalizes each system to its own size-two throughput. All decline; Scala Joins drops especially sharply, while JEScala retains more of its own baseline. This is evidence about scaling for the constructed patterns. It does not compare equal absolute starting rates, independently isolate expressivity, or measure all concurrency workloads. Compiler, runtime, matching and feature differences coexist.

**Rock-paper-scissors:** two players in separate threads generate 50,000 games. Figures 12a/b compare queue/counter optimizations and thread pooling. Pooling is the largest improvement for JEScala, and the additional optimizations improve its pooled version. The Scala Joins reference is shown both with a dummy event parameter, disabling its counter optimization, and without one. The parameterless Scala Joins counter version is faster than the fully optimized JEScala bars in the plot; pooling lets JEScala outperform the slower parameterized comparator. The no-pool bars are not monotonic under every added optimization.

No repetition count, uncertainty distribution, warmup protocol or complete dependency/version matrix is reconstructed from the paper. The plots supply scoped throughput/timing observations, not a causal law that more expressive languages must be slower. They also do not measure tail latency, queue growth, allocation/retention, fairness, deadlock frequency or migration cost.

## Relation to Mogemoge and Nu

[S121](S121-join-token-mechanism.md)/[S122](S122-join-token-evaluation.md) describe a different tradeoff: a global token pool with explicit ignition, ordered matching and retained/consumed role tokens. JEScala instead uses object-level events, explicit competing groups, queued occurrences, synchronous waiting and nondeterministic selection. Mogemoge's token replacement and preservation rules cannot be inferred from JEScala's queues, and JEScala's concurrency cannot be attributed to Mogemoge's deliberately sequential game execution.

Both are prior mechanisms for expressing interactions outside a single participating object's method body. They differ in scheduling, ownership, occurrence history, observability and the costs placed in the runtime. Nu comparisons should name those properties and the intended obligations, rather than treat every declarative event system as a functional world, a pure-state model or automatically replayable history. Neither publication establishes live-state migration, arbitrary-effect rollback, complete temporal checking or a coding-agent maintenance advantage.

## Access, fuller account and continuation

The [institutional project page](https://www.stg.tu-darmstadt.de/research_stg/projects_stg/past_projects_stg/jescala_stg/index.en.jsp) still exposes historical links for source, benchmark and example archives. All three web downloads miss cache. Ordinary native HTTP redirects each exact link to the current group's homepage, returning the same 26,365-byte HTML document rather than gzip. No source archive, library binary or benchmark was therefore acquired, attached or executed. The old publication's generic research URL also fails through the web tool. This is a current access failure, not evidence that the artifacts were never released.

W341–W345 identify the author's 2015 joint dissertation, [S205](S205-jescala-dissertation-access.md), as a fuller method dependency, including state-machine alternatives and event monitors. An existing/new native record was checked/created before any selected body reading. Its primary HAL abstract is read, but Darmstadt/HAL PDF requests return HTML; no full dissertation or chapter reading is credited. Indexed excerpts and duplicate bibliographies do not resolve the full timing/semantics questions or count as another empirical replication.

The immediate twelve-page mechanism read is complete. **Next action:** continue the acquired S188 HotBugs.jar method for B07/B08's temporal repair and oracle frontier while retaining the precise S205/source-access dependencies. Return to those dependencies if a lawful renderable copy or released archive becomes available. Ordinary event coordination, time-critical repair, persistence costs and type evolution remain separate survey questions; no experimental work is authorized by this reconstruction.
