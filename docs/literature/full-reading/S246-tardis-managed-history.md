# S246 — Tardis: managed snapshots, replay and their costs

Earl T. Barr and Mark Marron, *Tardis: Affordable Time-Travel Debugging in Managed Runtimes*, OOPSLA2014, pp67–82, [DOI10.1145/2660193.2660209](https://doi.org/10.1145/2660193.2660209). Main-agent reading,2026-10-04: **all16 author-edition pages, text and visuals; five figures, four tables, four algorithms, all sections and55 references**. No appendix. This supplies a complete chosen-publication reconstruction, not runtime reproduction or a developer-benefit trial.

The positive result is a practical snapshot/replay construction with low measured overhead on eight selected small-heap programs. Its optimized collector integration reduces every reported program's recording overhead and compressed history rate relative to its baseline. The represented-state, native-call, scheduling, runtime and workload conditions are central to transferring that result to an interactive engine.

## Identity and acquisition

Native DOI/title/edition checks cover **1,277 top-level /271 collection records**, with no match. Parent **`TPCBU87N`5508** and note **`RKGBAGBI`5509** precede selected body reading. Verified PDF **`4YPC4DZ7`5511** comes from [Microsoft Research's author copy](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/04/TimeTravelDbg.pdf): **691,924 bytes**, SHA-256 **`efe0687da4de8ad7400670017d6ed05bbd46cc30e7d099a4a75e7ff495764ba6`**, MD5 `5dbf7077e3635710d9449a63f3d988a6`. Extraction covers16 pages and every rendered page is inspected; the PDF and dumps remain outside public Git.

The [official landing page](https://www.microsoft.com/en-us/research/publication/tardis-affordable-time-travel-debugging-in-managed-runtimes-2/) explicitly identifies an author version. Its predecessor URL initially fails in the web cache, then ordinary HTTP resolves the `-2/` redirect. The main page links the PDF and BibTeX, without an inspected source/data release. No final publisher-PDF byte equivalence is claimed.

SC163 requests20 and returns both conference and SIGPLAN records. Crossref explicitly marks **10.1145/2714064.2660209** as identical to the conference work, with matching authors/title/pages/date; Scite's “new edition” label is not evidence of a new experiment. Three supplied outgoing edges point to **10.1145/1134760.1220164**, *Framework for instruction-level tracing and analysis of program executions*, reference4. They contain no snippets and are distinct from incoming tally counts. Primary target metadata is checked; that target body is unread. The source paper's actual tracing/native/related-work passages are read in context.

## What is retained and how a past state is reconstructed

Algorithms1–3 (§§2–3.1, PDF pp3–5) combine periodic snapshots with logs of nondeterministic inputs. Snapshots include globals, call frames, local/evaluation state, live reachable heap objects and allocator information. Type information and managed roots permit copying live objects instead of an entire address space. A logical `TraceTime`, together with the program counter, identifies the intended visit; it is not wall-clock time.

To travel backward, restore a preceding snapshot and replay its log forward to the target. Near the target, collect a more expensive full trace to make subsequent nearby steps inexpensive. This stores selected checkpoints plus information needed to reconstruct intermediate states; it does not keep a complete immutable world root for every step. Algorithm2's printed loop uses a conjunction of two inequality tests while its prose describes reaching both target components. That pseudocode detail is retained without silently correcting it or asserting an observed implementation failure.

§3.2 reduces snapshot costs in four ways:

- Coordinate a due snapshot with a copying/compacting collection, optionally triggering collection slightly early. A contiguous live range avoids another heap walk; pinned/stationary objects still need copying, and a fallback walk remains necessary.
- Walk the nursery and use object write barriers to record changed old objects. Partial snapshots depend on earlier snapshots, with a map locating old-object values. This changes recording and restoration work together.
- Compress snapshots and write them from a helper thread when spare CPU resources exist. Compression, raw generation and stored history are distinct quantities.
- Adjust the interval with a proportional controller targeting about10% recording cost, bounded to a selected interval range. Longer intervals can reduce recording costs while increasing the distance replay must cover. The interval sweep is not a separate measured validation of every adaptive-controller trajectory.

The method exploits existing mutability information and runtime services; it does not require the source program's heap to be immutable. Its representation and cost depend on live size, object survival, writes and checkpoint spacing, not just allocation traffic or source-code size.

## Files, native state and compatible code

§§3.3–3.4 (pp6–8) specialize file history using access modes and read dependencies. Mixed reads/writes retain old byte values with logical timestamps in512-byte blocks. Reads/writes that do not create a relevant dependency and unchanged writes can avoid history entries. File operations retain enough names/content/positions for reversal; exclusively read files can be reused instead of copying every input byte into the log.

This requires control over the environment. The implementation's broker coordinates TTD writers and permits non-TTD processes only as readers of shared files; unsupported external writes/IPC are outside its captured history. Network/timer inputs return logged values; replay suppresses sends and other non-idempotent/redundant outputs. It can update its represented UI/environment, but replaying observations does not reverse arbitrary effects in other systems.

Threads are multiplexed on **one logical CPU**, with explicit switches/events logged. This sacrifices task parallelism and excludes some races; it is not an evaluated multicore schedule-preservation solution. Native calls may not mutate environment state also accessed through the managed runtime. Their results are logged, but memory behind `IntPtr` is neither snapshotted nor restored and is marked uninspectable during replay. This matters directly to a game engine with native graphics/resources: a managed world snapshot alone does not establish coverage of those effects.

The author reports a custom72-call external API layer,1,215 implementation lines and448 added logging/replay lines. Those figures illustrate a bounded integration surface, not engineer-hours or an unrestricted standard-library compatibility claim.

§4 (pp8–9) additionally reconstructs debug-state views from optimized execution, assuming compiler correctness. Builtin operations/trace clocks must preserve order across safe points and argument values; heap stores must remain compatible; recovery maps must reconstruct locals/globals at the required points. Scalar replacement is restricted when object lifetime crosses a snapshot point. This concerns compatible optimized/debug builds of the same program, not arbitrary successor source, type evolution or a migrated running game.

## Evaluation and favorable results

§5 uses CCI rewriting, debugger/frame hooks, replacement **GenMS allocation/GC**, rewritten libraries and the **32-bit JIT/CLR on Windows8**. Hardware is a3.6GHz Sandy Bridge Xeon,16GB RAM and a7,200RPM SATA drive. One application core and one compression/write helper core are used. The comparison baseline passes through the rewriter without TTD code/instrumentation/hooks; it is not an unmodified current CoreCLR deployment.

Eight programs cover FileIO and Wikipedia HTTP processing plus C# ports of BH, Health, DB, Raytrace, Compress and LibQuantum. Their ordinary live heaps are **below20MB**. Measurements average ten runs after discarding minimum and maximum times; the paper reports dispersion below8% and a second stopwatch measure within10% of runtime-derived overhead. No participant debugging task or maintenance outcome is measured.

At a fixed **0.5-second snapshot interval**, Tables2–4 report:

| Program | Baseline overhead% | Optimized overhead% | Baseline GZip MB/s | Optimized GZip MB/s | Mean/max reverse latency,s |
| --- | ---: | ---: | ---: | ---: | --- |
| BH | 18 | 5 | .9 | .4 | .37/.68 |
| Compress | 6 | 4 | 1.2 | .4 | .23/.45 |
| DB | 22 | 11 | 5.6 | .6 | .41/.62 |
| FileIO | 5 | 4 | .8 | .1 | .27/.41 |
| Health | 15 | 6 | 4.1 | 1.3 | .29/.48 |
| Http | 11 | 9 | 1.1 | .4 | .23/.52 |
| LibQuantum | 14 | 9 | .2 | .1 | .21/.45 |
| Raytrace | 15 | 8 | 2.7 | 1.0 | .23/.51 |

The author headlines optimized **7% overhead /0.6MB/s history /0.68s maximum reverse latency**. Our arithmetic checks all64 numeric cells of Tables2–4: printed equal-weight overhead means are13.25% and7%; compressed-rate means2.075 and.5375MB/s; mean of the latency means.28s and largest sampled latency.68s. The baseline raw/compressed aggregate ratio is approximately2.78, consistent with the stated2.8-fold reduction. Unrounded raw runs and the precise headline aggregation are unavailable; the stated baseline14%/2.2MB/s and optimized0.6 headline are kept attributed rather than silently replaced by reconstructed table means.

Figure4 varies intervals from0.1 to2 seconds and exposes the cost/latency trade-off. Very frequent snapshots cost substantially more; lower-allocation LibQuantum has fewer piggyback opportunities, while rapidly allocating BH/Health benefit more. The paper reports at most one additional GC in a benchmark run, but no GC-pause distribution or frame-deadline measurement.

Figure5 separately varies Health's maximum live heap from10 to50MB. At50MB,0.5-second snapshots cost just under25% overhead;0.25-second snapshots approach50%, while2-second snapshots stay below10%. These are meaningful adverse scaling observations. Larger100MB-to-multi-GB heaps remain future work, explicitly acknowledged in §6. The graph varies live heap and interval, not total retained-history duration.

Table4 samples reverse operations at ten random target points. Its maximum is the largest observed result in that sample, not a universal worst-case bound. Safe-point delays, restoration and replay add to checkpoint distance. A near-zero follow-up step applies to the locally reconstructed trace, not every future reverse request. Logging rate is not retained managed-heap size or total storage over an unspecified recording lifetime.

## Limits, alternatives and next action

This is positive feasibility and runtime evidence with an explicit small-to-moderate-heap scope. The paper's25%/one-second “affordable” targets are motivated by earlier usability guidance; it supplies no direct estimate of developer adoption, bugs repaired or net effort. Its commercial-tool comparisons rely on cited public statements/marketing restrictions, not a matched experiment against those products.

The official page and one exact artifact-oriented query return no verified implementation/raw evaluation packet. The17 displayed search blocks are screened at title/bounded-excerpt scope; this is a bounded acquisition gap, not proof no artifact exists. Our work extracts, renders, checks metadata and computes table arithmetic; it executes no author code, compiler, benchmark or model.

For B04/B06, Tardis establishes **checkpoint-plus-replay as a concrete alternative to retaining every world version**, together with native/effect obligations and favorable/adverse costs. It does not quantify Nu's modern CoreCLR history cost. Reuse the exact [Fsge](S245-fsge-access-and-source.md) and [DATAS](coreclr-datas-guidance-2026-10-04.md) boundaries when connecting source-state mechanisms to graphics, live roots and frame outcomes.

The next consequential primary is **HistOOry: Executing code in the past: efficient in-memory object graph versioning**, [DOI10.1145/1640089.1640118](https://doi.org/10.1145/1640089.1640118),18-page conference work. It directly addresses Tardis's persistent-object alternative. Tardis's secondary “about3×” overhead account cannot substitute for that method's version granularity, lifetime/reclamation rules, observation contract and actual comparator. SC164's full-title lookup returns0; SC165's shortened title returns three records at limit20, separating the18-page work, SIGPLAN alias and a two-page companion. Native record/edition checks precede its intended body reading. Independent modern-runtime, game-change, type and empirical-benefit gaps remain open; all holds persist.
