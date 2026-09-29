# S69 — Casanova combines world-state rules, scripts and generated optimization

**Full reading completed 2026-09-30.** Giuseppe Maggiore, Alvise Spanò, Renzo Orsini, Michele Bugliesi, Mohamed Abbadi and Enrico Steffinlongo, *A Formal Specification for Casanova, a Language for Computer Games*, EICS 2012, pp. 287–292. DOI [10.1145/2305484.2305533](https://doi.org/10.1145/2305484.2305533).

The user-supplied six-page publication PDF governs this note: Zotero parent `GFRLS35S`, attachment `UTSHL7TK`, 499,164 bytes, SHA-256 `4edc92bc68d610e81ae3aebbc5b7e99ddc44a494fef6ffd196e0b60120e57da3`. All six pages, syntax/type/translation boxes, both line-count charts on p. 291, the runtime table on p. 292 and eighteen references have been consumed. A separately acquired [CiteSeer copy](https://citeseerx.ist.psu.edu/document?doi=2b0ab16b01c3b8ebe0e3f4f966890dcf7476edae&repid=rep1&type=pdf) has 325,228 bytes and SHA-256 `1da9812bbac49fcd18c9343514bb83ce41d9baebfece58629bf39776825faedb`. Its text was read first, followed by relevant renders and all six user-PDF renders. Layout, examples and reported measurements agree on inspection; byte and raster equality do not hold. The user copy improves extraction of spaces, arrows and chart labels. They are two copies of one work, not independent studies. No compiler, game, released artifact or author experiment was executed.

## Mechanism and scope

Sections 2–3 define a game as a world of typed entities, field-update rules, an initial state and main/input scripts. The generated update traverses the world and evaluates rules; drawing collects known drawable entities into batches. Rules receive the game state, owning entity and elapsed time. Mutable `var` values and references are permitted; references are not recursively updated through every incoming link. Effectful computations are represented as scripts, with coroutine suspension and composition for behavior spanning ticks.

The central consistency mechanism is double buffering. Rules read current values and write next values, followed by a swap. The compiler targets potentially mutable F# representations rather than allocating an entirely fresh world on every tick. A global buffer index and reusable mutable collections reduce swapping/allocation work. Query optimization introduces indexes; parallel evaluation relies on rules having distinct write locations. This is a predecessor for declarative world updates, explicit temporal behavior and controlled mutation. It is not evidence that immutable allocation alone is efficient or that every external subsystem participates in the same snapshot boundary.

The traversal excludes functional terms and scripts. Scripts are stepped separately and may have effects. The presentation supplies syntax, selected typing rules and a translation outline, without an end-to-end proof that all gameplay, script and external-effect obligations are preserved. A consistent view of rule-managed fields is a narrower property than complete behavioral correctness, reversible effects or persistent historical versions.

At publication the compiler was still under construction. An F# library used optimized reflection and XNA; a C++ template library used DirectX 10. The library did not support every language feature and required specialized rule datatypes. The Galaxy Wars account reports a student-developed project exceeding 100,000 lines and supporting up to eight players. It is an author capability account, not an independent maintenance comparison or a representative adoption sample.

## Evaluation reconstruction

The two p. 291 charts compare infrastructure, three small games and selected snippets in Casanova, its F# library and idiomatic C#. Counts exclude brace-only lines and some trivial property declarations. The contrast bundles language, generated traversal, rendering/game APIs and implementation choices. Shorter code establishes neither lower maintenance effort nor identical behavioral coverage; there are no developer tasks, errors, timings or independent equivalence checks from which to infer either.

The runtime table tests optimization variants within one RTS example:

| Variant | Reported FPS | Interpretation limit |
| --- | ---: | --- |
| None | 0.375 | Unoptimized baseline; not a representative production implementation |
| Fast rule swap | 0.387 | About 3.2% above baseline; the printed 103% column is a ratio expressed as a percentage, not a 103% increase |
| No reallocation for lists | 0.387 | Same printed value; separate uncertainty/repetition data absent |
| Rule threads | 0.782 | About 208.5% of 0.375, whereas the table prints 203%; denominator/rounding cannot be reconciled from this table |
| Query | 213 | Algorithm/index change dominates; not an isolated language-paradigm effect |
| All together | 233 | Combined optimization result; cannot assign its gain separately to each mechanism |

The accompanying claim that unoptimized generated F# stays within 5% of equivalent C# is not supported by a displayed per-comparator timing table here. Hardware, repetition distributions, uncertainty and detailed workloads are insufficient for independent reconstruction. FPS does not establish frame-tail deadlines, allocation cost or developer productivity. No speedup is transferred to Nu.

## Printed-example qualifications

Visual inspection confirms two notation problems: the general return typing rule on p. 289 ends in `Script Unit` despite taking an arbitrary value, and p. 290 gives `yield` two type parameters although the preceding `Script` datatype has one. The coroutine example described as moving for ten seconds instead tests position against ten. These are printed-example discrepancies, not executed failures of the released implementation. Any later executable reuse requires a versioned source check and independent behavioral tests.

## Claim consequences and follow-up

| Live claim | Primary evidence / limit | Consequence |
| --- | --- | --- |
| Functional game architectures first combine global state, rules and temporal behavior | §§2–3 already combine those ideas in 2012, including an F# route | Withdraw broad firstness; compare Nu's actual ownership, update/effect and tool boundaries |
| State consistency makes maintenance behavior correct | Rule-managed current/next consistency has a defined boundary; scripts and external effects remain | Keep temporal, retained and external obligations independent of compilation/snapshot consistency |
| High-level organization requires accepting poor runtime performance | Generated indexing, buffers, reuse and rule scheduling are plausible countermechanisms | Compare generated algorithms and data layout, not language labels alone |
| Smaller source yields useful net maintenance benefit | Selected line-count charts and one-game performance variants do not measure maintenance | Value remains plausible and unmeasured; preserve API/training/tooling and task-family rivals |

**Unique:** Nu-specific priority remains unconfirmed; this is direct prior art for several broad mechanism claims. **Valuable:** world-update consistency and avoiding handwritten optimization are concrete concerns, with no measured Nu maintenance effect. **Scientifically valid:** any later comparison needs equivalent obligations, clear buffer/script/effect boundaries, independent implementation families and algorithm/runtime accounting. This paper validates no ISE apparatus.

S70 is the immediate family follow-up for encapsulation, dependency maintenance and networking; it is related work, not independent replication. Bibliography leads include *Monadic Scripting in F# for Computer Games* (2011), *Scaling games to epic proportions* (SIGMOD 2007), the 2011 Casanova design paper and the cited component/OO game-architecture studies. Their consequential primary methods and family lineage remain to examine. The [background ledger](../nu-background-searches-2026-09-30.md) retains the wider open frontier and actual search ranges.
