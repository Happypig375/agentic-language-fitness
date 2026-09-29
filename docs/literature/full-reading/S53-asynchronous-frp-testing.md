# S53 — asynchronous temporal testing and specification validity

**Full chapter reading completed 2026-09-29.** Nielsen, Kristiansen and Bahr, *Property-Based Testing for Asynchronous Functional Reactive Programming Using Linear Temporal Logic*, PADL 2026, LNCS 16401, printed pages 39–56, [DOI 10.1007/978-3-032-15981-6_3](https://doi.org/10.1007/978-3-032-15981-6_3). Zotero `5RW44ALL`, attachment `9JA5SQ2D`. The chapter occupies **PDF pages 49–66** in a 228-page proceedings file: 12,898,200 bytes, SHA-256 `0441c00ab47d4fb41eff34dff833d07a1d81151dc15db4bcfab3877c6dc2a0ab`. The attachment was already in the library; it was not downloaded by this session.

All eighteen target pages, sections 1–7, four figures, equations/code and eighteen references were read. Renders of PDF pages 50, 55, 57–60 cover all figures and disputed examples. The rest of the proceedings is not counted as read. The associated source release was inspected as described below; no author code, GUI, test suite or experiment was executed.

## Mechanism and evidence unit

PropRatt targets Async Rattus, a Haskell-embedded language with modal types, delayed computations and clocks represented by sets of input channels. It combines heterogeneous signals into one trace, retaining values, local histories and flags indicating which signals updated. GADTs constrain signal lookups and expression types; temporal predicates express relationships among their values and updates. This gives a concrete asynchronous testing predecessor without establishing that ordinary F# types supply the same temporal guarantees.

The evaluation demonstrates expressiveness using signal combinators and one timer GUI derived from 7GUIs. It is not a controlled maintenance, usability or defect-detection-rate experiment. The displayed faulty-zip example fails after two tests and fourteen shrinks, an illustrative run rather than a sensitivity estimate. The paper summarizes its authors' 2025 thesis, not an independent replication. Ergonomics and useful specification-language extensions are explicitly future work.

The framework merges concurrent signals before checking them. The paper describes this as hyperproperty support; it does not demonstrate a general quantification mechanism over arbitrary independent program executions. That stronger interpretation would require the separate hyperproperty semantics it cites. The introduction's 243 possibilities count three update combinations over five transitions for two signals; it is not the number of tested programs or a measured coverage percentage.

## Time, generators and unfinished obligations

The paper deliberately gives Until a weak interpretation: the awaited right-hand event need never occur if the left condition persists. It also states that unbounded eventuality has no finite counterexample. These choices must not turn a still-pending lifecycle obligation into measured completion. Deadlines or an explicit unknown/truncated result are different policies, each requiring its own specification.

The shown generator chooses a clock cardinality uniformly from one, two or three, then chooses within that cardinality. Thus it is not uniform over seven nonempty subsets: the full three-channel clock has probability one-third, while each singleton or pair has probability one-ninth. Execution chooses the smallest channel in the merged clock. Clock randomness explores relative timing, but neither the paper nor the inspected artifact establishes exhaustive schedules, representative wall-clock delays or fairness within a finite observation window. Three available channels also cannot supply four pairwise-disjoint nonempty clocks. These are concrete generation limits, not objections to asynchronous testing itself.

Shrinking removes chunks and reduces values while carrying stored clocks into rebuilt signals. Preserving clocks is not proof that all original domain preconditions, causal interpretations or physical timing remain valid. History lookups also need a declared reference frame: the artifact retains a signal's previous emitted values, while Next advances the merged trace. A merged step does not guarantee that every signal has emitted another value.

## Printed examples and released source

The [PropRatt 0.2.0.0 source archive](https://hackage.haskell.org/package/PropRatt-0.2.0.0/PropRatt-0.2.0.0.tar.gz) is 13,122 bytes, SHA-256 `e295ca0aa75ff77bbe03cb544e84e54b063dafe7b18f357da72e4980a0fcbc5d`. All eight library modules, both example programs, the test entry point, Cabal metadata, README and changelog were read: fourteen of sixteen archive files. License and setup boilerplate were not part of the methods review. The package identifies the accompanying paper, but no frozen build or raw result archive establishes that it produced every displayed result.

The source check resolves some publication ambiguities and exposes limits that matter before adopting this oracle:

| Issue | Verified publication/source distinction |
| --- | --- |
| Faulty zip | Printed page 49 tests the first input/component while the demonstrated mutation loses the second component. Its displayed counterexample orders the output first. The released `prop_zipWrong` instead tests the second component on the second input's tick, with output first in the trace. The source supplies a coherent version of this example; the printed predicate does not justify that particular displayed failure. |
| Timer fields and vacuity | Printed page 50 identifies the first state field as elapsed time and the second as maximum, but `prop1`/`prop2` use the second field. The release adds a proper elapsed-versus-maximum predicate. Its `prop_timerTicks` retains the second-field antecedent: if the separately tested maximum-equals-slider invariant holds, that antecedent is false, so passing it gives no evidence of increment behavior. |
| Finite eventuality | `evaluate` defaults to one hundred merged steps; insufficient-length inputs may return true without checking the predicate. The released Eventually branch can return false when its condition remains false through the finite end, including `F FF`. That differs from the paper's statement that testing a liveness property always succeeds. Finite failure here is not a counterexample to unbounded eventuality. |
| Previous values/ticks | The release drops an entry from a signal-local history for `Prev`. A global Next can leave another signal with no previous emitted value. The runtime can then report missing history; `Tick (Prev ...)` explicitly raises an error although the publication's shorthand definition constructs that syntax. Well-typed expressions therefore do not by themselves establish a usable temporal oracle. |

These are direct static reconstructions of the inspected edition, not reproduced runtime results or claims about all versions. The release's declared test-suite entry point checks one list-length property; the more extensive examples are separate executables. No publication-wide soundness result follows from that entry point. The source retains growing signal histories for its finite tests; Async Rattus's language guarantees do not independently demonstrate bounded total instrumentation cost.

The timer also needs specification discipline. The [primary 7GUIs task](https://eugenkiss.github.io/7guis/tasks/#timer) stops elapsed time when it is at or above the selected duration and resumes when duration rises above it. It does not require clamping elapsed time downward when the slider decreases. The release's `setMax` does clamp it. Consequently, the release's claim that elapsed time never exceeds maximum is an additional design choice, not a necessary translation of that task. Its constant-unless-reset-or-second predicate also needs reconciliation with a slider-only change that clamps elapsed time. These observations do not establish how the separate modal-GUI paper's implementation behaves.

Key file SHA-256 values are retained for reproducibility:

- `LTL.hs`: `04fe2736ccc41d94b6423454b357caa4c1d0fc13d27edf195053539b5d3ef7c5`.
- `Core.hs`: `0c0b14a277c1fbdf0c355bcf0a0fd3ba00a01ab3658fe8664e8c30b394a385f3`.
- `Arbitrary.hs`: `7e14064cc4319cf4f79973fbe4a5694d8b2ef9b588ecac519dd6f60939a72c41`.
- Combinator example: `9dd442ddf6ce4036899088201d01ba31a2b5a73c7cc8f5abb3638dc5fe47e5ac`.
- Timer example: `0a39e7a1d713f5fdb480fded88261ed03c9eea4fbd9cae16d7c7cb93c8a50e58`.

## Three criteria and follow-up disposition

**Unique:** asynchronous temporal-property testing, typed multi-signal specifications and clock-preserving shrinking are established mechanisms. Broad invention claims remain untenable; this does not establish or refute priority for the specific Nu/F# maintenance contrast. **Valuable:** checking stale values, switching and simultaneous input is useful in principle, but no comparative Nu, developer-effort or agent-benefit estimate is supplied. **Scientifically valid:** validate properties independently of implementation, test vacuous antecedents and intentionally bad behaviors, preserve event identity/order and history boundaries, and distinguish unfinished obligations from failures and successes. Neither GADT typing nor a passing generator establishes complete behavior. Allocation remains zero.

The incoming Scite graph requested twenty edges and returned zero, with a low-coverage warning. An exact `PropRatt` term query requested twenty records and returned zero. A broad mixed phrase/testing query returned twenty results but was overwhelmingly unrelated; the explicit-AND reformulation returned only S53. The reformulated query is exhausted at one indexed result, not the field or citation graph. The existing Rhine dispositions are reused. Four backward identities were checked with a twenty-record DOI request: Async Rattus (`10.1007/978-3-031-52038-9_2`), modal GUI programming (`10.1007/978-3-031-99751-8_5`), temporal-relation testing (`10.1145/1808266.1808281`) and hyperproperty logics (`10.1007/978-3-642-54792-8_15`). These remain conditional on adopting their typing guarantees, GUI comparator, protocol semantics or trace-quantification claim; they were not fully read. The two theses are conditional elaborations, not extra independent evaluations. S46/S47/S50 retain their completed scope.
