# S218 — ReDAC: cyclic calls, quiescence and measured costs

**Identity:** Andreas Rasche and Andreas Polze, *ReDAC — Dynamic Reconfiguration of Distributed Component-Based Applications with Cyclic Dependencies*, ISORC 2008, pp.322–330, DOI [10.1109/ISORC.2008.44](https://doi.org/10.1109/ISORC.2008.44). Crossref, DBLP and the authors' HPI publication list agree on the work. S187 reference 115 and its roster row 61 provide the discovery route.

**Coverage, 2026-10-02: complete available primary-text reading; visual/PDF gap remains.** Native collection `PKLXQNEE` and global holdings were checked by DOI/title before reading: 236 collection parents and 1,230 top-level library items, no match. New parent **`LPNN8V3S`** and note **`SZJVQTUY`** preceded the intentional body reading. No PDF attachment is claimed. The [author-uploaded ResearchGate text](https://www.researchgate.net/publication/221249726_ReDAC_--_Dynamic_Reconfiguration_of_Distributed_Component-Based_Applications_with_Cyclic_Dependencies) is read from title through the end of the 15-entry bibliography, with numbered pages 1–9, sections 1–9, four algorithms, three displayed equations, the timing table, and the extracted text/captions of seven figures. The site's separate references/figures counters are not the paper's bibliography/figure counts.

PDF downloads from the HPI-linked ResearchGate route and its current author-slug form returned HTTP 403. The old HPI/DCL file returned 404, as did CiteSeerX's indexed old route and redirected document route; the ordinary IEEE PDF returned 418. OpenAlex and Semantic Scholar point back to the stale HPI/CiteSeerX locations. Scite's exact-DOI request returned one record with `contentDenied`, without primary full-text passages. The two requested ResearchGate figure pages were unavailable through the web tool. **No visual coverage, verified PDF bytes, publisher-copy correspondence, code execution or model-checker rerun is credited.** In particular, the Petri-net structure, diagram arrows and histogram cannot be certified from mangled extraction. S218 is kept outside the full-publication count pending that gap.

Three ignored web-extraction snapshots preserve the returned text windows; they are not PDFs or publisher originals:

| Returned line window | Bytes | SHA-256 |
| --- | --- | --- |
| 77–940 | 28,545 | `6f0e5cb9e1bd54428dcc8c9c2d67e5385e6dc0312c903020a1b04bfde0f0e889` |
| 669–1450 | 25,004 | `6372e66874c02cd37396edcc9195961b54f8bdd681bb4e4b7043cc3ce6f23a52` |
| 1297–1877 | 26,717 | `9bba020cc44a470e9304cd1d21c25ed72e1a5461de8e0410c98a836ff3ba60e1` |

The paper ends at returned line 1798; later citation-card text is not an extension of its body or a completed forward-citation review. Headers, extraction spacing and window overlap explain why these snapshots are not a clean source edition.

## Mechanism reconstructed from the available text

Sections 3–5 make a deployment component into a runtime **capsule**: an object graph with designated root objects. Every thread must enter the capsule through a guarded root method; inter-capsule references and logical thread identities are part of the application model. A cross-capsule transaction here is a single synchronous method invocation, possibly with nested/reentrant calls. This is not a model of every asynchronous task, external effect or durable application transaction.

Updating a chosen block-set requires its active invocations to drain so that live state does not remain on stacks, in registers or in transit. Blocking every connection immediately can deadlock a cyclic call that must reenter an affected capsule before returning. ReDAC instead maintains each capsule's count of active calls per logical thread. A thread already active somewhere in the block-set may continue nested calls; one with no such call waits. Normal entry increments its count and exit decrements it. Once every relevant count reaches zero, the reconfiguration thread may act and then release waiting threads.

The four printed algorithms cover the global active-call check, guarded entry, guarded exit and the reconfiguration request. The implementation excerpt adds protection against a block request arriving between the first flag check and the counter increment, and uses a reconfiguration generation counter to prevent a delayed signal from triggering a later update incorrectly. These details are material: the pseudocode's simultaneous flags and global observations require an actual synchronization implementation. This reading does not verify its distributed memory, failure or communication behavior.

A further example shows that shared locks can deadlock this protocol: a thread outside the block-set can hold a resource needed by an active thread inside it and then be stopped at entry. The proposed extension includes intervening capsules on paths between members of the block-set. This is a concrete integration obligation on the block-set and dependency model, not permission to ignore ordinary application locks or a demonstrated bound for arbitrary synchronization patterns.

The mechanism establishes a place to apply reconfiguration. Section 6 explicitly delegates the update operations and object-graph state transfer to earlier work. Drained invocations do not themselves prove that a new representation preserves application invariants, that identities/resources survive transfer, or that an urgent replacement has the desired behavior. The introduction's three consistency requirements—structure, mutually consistent capsule states and application invariants—remain distinct obligations.

## What the evaluation establishes

Section 7 reports a .NET Framework 2.0 implementation on Windows XP SP2, a 2.8 GHz Xeon with one active core and 2 GB RAM. Its table gives batches of 1,000 calls, with means and standard deviations over 1,000 separate measurements using the CPU tick counter:

| Invocation | Reported batch duration |
| --- | --- |
| Interface call | 5.96 ± 0.14 microseconds |
| ReDAC | 151.68 ± 2.09 microseconds |
| Reader–writer lock | 324.19 ± 4.28 microseconds |
| Reflection.Invoke | 5.05 ± 0.21 milliseconds |
| .NET Remoting | 346.92 ± 2.11 milliseconds |

Own arithmetic on these printed values gives **145.72 nanoseconds additional time per guarded call** relative to the interface baseline, about **25.45 times its tiny baseline duration**. ReDAC uses **46.79% of the reader–writer-lock batch time**, a reduction of about **53.21%**. Both comparisons matter: a favorable synchronization alternative still has a nonzero per-call cost. These are calculations on reported means, not new timing observations. Reflection/remoting are different invocation mechanisms, and the table is not a matched comparison of complete applications implementing all the same distributed update obligations.

The authors argue that only a small share of application calls cross capsule roots and that useful method bodies take much longer. Those are reasons the absolute overhead can be small in an application; they are not a measured root-call fraction or whole-application slowdown for Nu. The text's separate order-of-magnitude claim refers to its earlier 2003 approach, not the roughly twofold reader–writer-lock contrast above.

The reported blackout experiment uses 500 reconfigurations of a generated configuration with 20 capsules, 10 threads and maximum call depth 20. Methods perform a few arithmetic operations to expose protocol cost. The text reports 80–400 microseconds, mostly below 300. The histogram remains visually unread here. Waiting for long methods, blocking I/O, state conversion, rendering and recovery can change an application's interruption time; this result is not a worst-case bound or a full urgent-update latency.

Section 8 reports successful dynamic updating of PaintDotNet, described as exceeding 133,000 lines, with no overhead noticed during use. It also describes replacing faulty controllers in a remote laboratory. These are useful application reports, but this paper does not supply a controlled PaintDotNet responsiveness/effort result, an exact version-change roster or a common fault-recovery success denominator. **S187's compressed no-overhead table entry should therefore be read as this scoped experience report, not literal zero measured cost.**

## Formal and transfer boundaries

Section 5 describes TimeNET analysis of a specified Petri-net configuration and displays a one-capsule, one-thread recursive model whose recursion depth depends on initial tokens. Its mutual-exclusion invariant forbids simultaneous application/reconfiguration markings; positive stationary expected markings are used to argue progress. More complex configurations are mentioned but not presented. Preserve this reported model analysis without upgrading it to a checked proof for all distributed component topologies, schedules, faults or a general bounded-liveness theorem. The visual/model files have not been inspected and TimeNET has not been run here.

For B04/B08/B10, ReDAC supplies a constructive cyclic-call alternative to global stopping, with explicit root boundaries, logical thread tracking, synchronization and update-set obligations. For B06, its favorable lock comparison and small absolute guarded-call cost coexist with positive overhead and narrow blackout workloads. For B05, PaintDotNet is an interactive application lead, not game-loop/rendering evidence. For B12, method timing, scoped model analysis and application experience are different evidence units. None demonstrates Nu-specific novelty, human benefit or correctness of future F# changes.

The next direct dependency is reference 10, **Rasche and Schult, *Dynamic Updates of Graphical Components in the .NET Framework*, SAKS 2007, pp.219–230**. It is the paper's own route for state transfer and root-call cost details. Resolve its edition and native holdings before reading. Retain the executable S218 access task—obtain a lawful author/publisher PDF and inspect all diagrams/code/plot visually—without blocking independent accessible literature work. No construction or experiment is authorized by this reconstruction.


**Dependency access update:** [S219](S219-gui-updates-access.md) now has a verified native record and explicit failed public routes, but only metadata and a returned traversal passage are available. Its full method remains unread. Continue the independent C02 algebraic-testing method while preserving this concrete access task.
