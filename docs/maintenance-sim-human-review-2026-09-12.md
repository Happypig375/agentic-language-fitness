# Maintenance simulation: standalone review packet

**Status: construction validated; human-review checkpoint; not approved for execution.**

This packet concerns one supplied F#/modern-C# architecture pair and eight
inherited maintenance episodes. It does not replace the prepared H1/H2 packet
or authorize its execution. The user adopted model-free construction, not an
experimental sample. No candidate has been dispatched or evaluated here.

## Current values and their sources

| Item | Actual value | Source to review |
| --- | --- | --- |
| Workload | One original-authored headless simulation pair, eight episodes | [Construction metadata](../benchmarks/maintenance-sim/construction.json) |
| Starting architecture | Supplied separately authored seeds, not model-generated greenfield code | [F# seed](../benchmarks/maintenance-sim/seed/fsharp/Simulation.fs), [C# seed](../benchmarks/maintenance-sim/seed/csharp/Program.cs) |
| Toolchain | .NET SDK **10.0.302**, no added dependencies | [F# project](../benchmarks/maintenance-sim/seed/fsharp/Simulation.fsproj), [C# project](../benchmarks/maintenance-sim/seed/csharp/Simulation.csproj), [constructor](../src/alf/maintenance.py) |
| Shared observable interface | Independent JSONL requests; deterministic state, effects, errors and named snapshots | [Seed contract](../benchmarks/maintenance-sim/contract.md) |
| Maintenance policy | Fresh conversation, no tools, one submission per episode, no diagnostic repair feedback | [Shared candidate guidance](../benchmarks/maintenance-sim/guidance/common.md), [adopted design](maintenance-context-design-review-2026-09-12.md#clean-episodes-inherited-software) |
| Inherited state | Safe wrong/noncompiling code persists; malformed submission applies nothing; no gold reset | [Adopted lifecycle and classification policy](maintenance-context-design-review-2026-09-12.md#clean-episodes-inherited-software) |
| Durable notes | Markdown explicitly submitted in `files` persists and is charged; `architecture_notes` is an archived impact explanation, not automatic memory | [Shared guidance](../benchmarks/maintenance-sim/guidance/common.md) |
| Input | Complete eligible source, guidance, seed/current/past public requirements and serialization; no future tasks or reference solutions | [Envelope serializer](../src/alf/maintenance.py) |
| Input/output limits | **Unset** for a candidate protocol; constructor safety bounds are not scientific caps | [Construction metadata](../benchmarks/maintenance-sim/construction.json), [audit limits](../src/alf/maintenance.py) |
| Offline proxy | `tiktoken==0.14.0`, `o200k_base`; **not** provider context accounting | [Measurement implementation](../src/alf/maintenance.py) |
| Architecture diagnostics | Exploratory, separate fields; no weighted elegance/F# preference score | [Review dimensions](maintenance-context-design-review-2026-09-12.md#what-consistent-design-would-mean-operationally) |
| Human expert approval | **false**; domain/language review not started | [Construction metadata](../benchmarks/maintenance-sim/construction.json) |
| Scientific freeze | **false** | [Construction metadata](../benchmarks/maintenance-sim/construction.json) |
| Live approvals | `live_execution_approved=false`, `user_live_execution_approved=false` | [Construction metadata](../benchmarks/maintenance-sim/construction.json) |
| Integration / pilot / used dispatches | **0 / 0 / 0** | [Construction metadata](../benchmarks/maintenance-sim/construction.json) |
| New candidate runner | **Not implemented**; host fixture builds are trusted construction checks only | [Future adaptation boundary](maintenance-sim-construction-2026-09-12.md#future-runner-boundary-not-implemented-or-authorized-here) |

No earlier E3a balance or H proposed ceiling carries over. A review signature,
passing test or Git commit is not live allocation.

The numeric budget proposal is **86,016 input bytes / 61,440 output bytes**,
not an activated candidate limit. The rule, recorded before the complete size
audit, rounds 1.25 times the largest complete reference input up to a
4,096-byte boundary. For output it first adds 4,096 serialized note bytes to the
largest empty-note full-file replacement, then applies the same multiplier and
rounding. Both use the pooled language/episode maximum, not a language-specific
threshold. This allowance
does not establish a physical context limit or guarantee room for arbitrary
candidate-grown code. Identical prompts fitting several offline cap labels must
not be dispatched repeatedly as different treatments.

## Workload and fairness review

Read the seed contract and each language's guidance alongside its seed:
[F# guidance](../benchmarks/maintenance-sim/guidance/fsharp.md),
[C# guidance](../benchmarks/maintenance-sim/guidance/csharp.md).
Common ownership/transition/effect advice is supplied to both. C# may use records,
pattern matching, encapsulated mutable state and generic collections; F# may use
records, unions, maps and small functions. Neither a mutable field nor a class
is a defect by definition. Equal behavior does not require equal private layout,
source length or the reference patch.

| Episode | Required maintenance pressure | Exact public task |
| --- | --- | --- |
| 01 | Deferred commands and deterministic ordering | [01.md](../benchmarks/maintenance-sim/episodes/01.md) |
| 02 | Removal and cancellation across deferred work | [02.md](../benchmarks/maintenance-sim/episodes/02.md) |
| 03 | Interacting follower behavior and entity lifetime | [03.md](../benchmarks/maintenance-sim/episodes/03.md) |
| 04 | Snapshot migration, validation and round trips | [04.md](../benchmarks/maintenance-sim/episodes/04.md) |
| 05 | Registered movement policy and extension ownership | [05.md](../benchmarks/maintenance-sim/episodes/05.md) |
| 06 | Deterministic request/cancel/complete and stale events | [06.md](../benchmarks/maintenance-sim/episodes/06.md) |
| 07 | Quiescent batched hot path with equivalent final state | [07.md](../benchmarks/maintenance-sim/episodes/07.md) |
| 08 | Atomic replay across earlier features | [08.md](../benchmarks/maintenance-sim/episodes/08.md) |

Check whether these are plausible changes to an inherited codebase and whether
the contracts can be satisfied after a prior implementation failure. They are
not a sample of large production projects or decades of unanticipated change.
Authors knew the planned chain. A separately scoped seed-only AI review reduces
but cannot remove that hindsight limitation.

The [seed-only AI review](../reports/maintenance-sim-construction-2026-09-12/seed-review.md)
records exact hashes, what was inspected and actual blinding. It found both
seeds plausible, requested equivalent architectural guidance and rechecked that
correction. It is **not human F#/C#/domain expert approval**.

## Evidence completed for the construction handoff

### Exact reference-envelope measurements

These are the complete UTF-8 serialized inputs and empty-note full-file-change
outputs for the current authored references, not provider usage or candidate
outcomes. Input episode N contains predecessor N−1, never reference N.

| Episode | C# input bytes | F# input bytes | C# replacement bytes | F# replacement bytes |
| --- | ---: | ---: | ---: | ---: |
| 01 | 19,907 | 20,393 | 13,153 | 14,134 |
| 02 | 25,051 | 26,225 | 13,326 | 14,593 |
| 03 | 26,844 | 28,304 | 15,555 | 16,830 |
| 04 | 32,928 | 34,396 | 21,312 | 27,408 |
| 05 | 40,880 | 47,169 | 25,867 | 32,500 |
| 06 | 47,986 | 54,812 | 31,332 | 38,882 |
| 07 | 55,017 | 62,760 | 32,625 | 40,930 |
| 08 | 58,350 | 66,848 | 34,595 | 43,928 |

The proposed input cap follows `ceil_to_4096(66,848 × 1.25) = 86,016`;
output follows `ceil_to_4096((43,928 + 4,096) × 1.25) = 61,440`.
The output columns exclude actual impact-note text and native/model framing;
they are replacement lower bounds, not guaranteed model output requirements.

**This authored pair does not show the hypothesized F# compactness advantage.**
Its F# inputs are larger at every episode. This is implementation- and
framework-specific construction evidence, not a population language result or
a test of model decision quality. Do not rewrite a reference simply to reverse
that direction. The fully supplied-source condition cannot by itself establish
that extra available context causes better decisions or long-term maintainability.

### Behavioral and review evidence

The [construction record](maintenance-sim-construction-2026-09-12.md) retains
failed checks and repairs; the final audit now completes the evidence claim:

- All 18 trusted checkpoints passing cumulative public/evaluator cases.
- Compile-successful semantic faults detected in both languages, without
  mistaking compiler failures for semantic sensitivity.
- Applicability evidence for no-op, malformed, noncompiling, missing-prerequisite
  and wrong-behavior predecessors; separate evaluation availability and recovery.
- All 16 exact predecessor/current-task input envelopes and full-file-change
  output measurements; common numeric budgets proposed before model outcomes.
- Source-bound final architecture/contract AI review.

Exact-publication CI is separate and remains outstanding at this local
construction checkpoint; it is not included in the completed evidence above.

The fixture checker is [maintenance_check.py](../scripts/maintenance_check.py)
and its focused tests are [test_maintenance.py](../tests/test_maintenance.py).
The executable examples and private-by-role evaluator inputs live in
[cases.json](../benchmarks/maintenance-sim/fixtures/cases.json), with visibility
and provenance explained in the [fixture README](../benchmarks/maintenance-sim/fixtures/README.md).
They are public repository artifacts but must be withheld from candidate input
except the cases explicitly marked public. This is not a claim of secrecy or
absence of pretraining contamination.

## Next decision, not implicit execution permission

With the evidence complete, human reviewers should review workload realism and
idioms, support symmetry, contract/error precedence, inherited-failure policy,
context/output measurements and exploratory architectural diagnostics. Approving
this construction does not by itself approve a main-study horizon or live quota.

The next implementation boundary is a small maintenance-specific adapter to the
existing no-tools client and isolated evaluator. It must demonstrate retained
safe failed state, no score-dependent continuation, charged durable notes,
dispatch/usage bounds and candidate isolation on the actual Simulation projects.
The old general runner evaluates on the host and is unsuitable. Do not add a
new proxy, backend, generic framework or numbered apparatus family.

Only a separately adopted candidate protocol, functioning reviewed adapter,
exact-source integration evidence and explicit live allocation can open an
execution gate. All approval fields above remain unapproved.

## Validated construction checkpoint

The final trusted model-free audit passed: 80 cases, 18 targets, 608 applicable
checks, 16 envelopes, 8 faults, 12 failure-transition scenarios and 16
witnesses. See the [evidence index](../reports/maintenance-sim-construction-2026-09-12/evidence/index.json)
and [raw report](../reports/maintenance-sim-construction-2026-09-12/evidence/report.json),
whose SHA-256 is `ab6e5a53023929b7d731a6675a455c3c877f1b42064b9d258c84bce152f2fea5`.
The independent AI validator reported 27/27 tests using its recorded command;
raw unit stdout is not archived. CI on the implementing publication remains
pending. Proposed caps remain 86,016 input / 61,440 output bytes; approvals
false, allocations zero, and no provider/model/candidate claim is made.
