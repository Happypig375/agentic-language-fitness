# Maintenance simulation construction record

**Status:** construction validated; trusted model-free preparation and human-review checkpoint only.

## Authority and scope

The user replied **"continue"** to the explicit maintenance-first construction
question at publication `abdc68cc1eef24f0aca080bc151714f930ef8f27` (exact
Linux/Windows CI `34675819811` passed). This adopts one idiomatic F#/modern-C#
pair and eight inherited maintenance episodes from the
[design packet](maintenance-context-design-review-2026-09-12.md). It does not
adopt initial architecture creation, a large-project sample, a live runner,
scientific freeze or an experimental dispatch allocation.

All H approvals remain false and allocations zero. No OAuth staging, count/model
request, experimental candidate execution or remote/proxy change is included.
The pre-existing untracked `uv.lock` is unrelated and must remain untouched.

## Construction boundary

- Shared seed requirements and separate episode documents live under
  [benchmarks/maintenance-sim](../benchmarks/maintenance-sim/contract.md).
- The two seed implementations are authored separately against the shared
  contract, not translated into one another. This is AI-assisted original
  authoring, not independent human language-expert validation.
- Trusted reference successors are incremental patches outside each seed tree,
  not nine complete duplicate projects and not a runtime version family.
- The construction check assembles trusted predecessors for offline envelope
  audits only. It is not a live controller and must never reset a candidate
  repository to reference gold.
- New checking code can run checked-in, reviewed trusted fixtures on the host.
  This is not sandbox evidence for arbitrary candidate code. Any future live
  runner needs a separately reviewed integration with the existing isolation
  boundary; the old general runner's host evaluator remains unsuitable.

## Decisions resolved during construction

The precise behavioral contracts are newly authored under the approved themes;
their numeric/input choices are construction choices, not established research
findings. Parent integration review precedes language implementation. Preserve
this distinction at the next handoff.

The first contract draft had ambiguous tick ordering, snapshot migration and
replay errors, and researcher-facing content in shared guidance. These were
identified before candidate activity or acceptance of either implementation.
The repair direction is explicit queued-command ordering, atomic effects/state
on failure, externally testable legacy snapshot import, deterministic interacting
entities and cancellation, a restricted fast-forward operation and atomic replay.
Candidate guidance must exclude author/reviewer instructions and research claims.
Missing prior capabilities are failures to classify, never exemptions from later
cumulative requirements.

Reference snapshots and private evaluator cases stay outside candidate-visible
source. The seed contract contains no future episode descriptions. A constructed
envelope contains only the eligible predecessor, current task, prior public
obligations and charged domain/language guidance. Full source exposure is audited;
no physical provider context limit is inferred.

## Checks and corrections so far

The constructor's initial comparison used Python equality, which can accept
`true` as equal to `1`. It now compares JSON types recursively. The initial
envelope loop also needed to associate episode N with predecessor N-1, not
successor N. The source and task remain separately identified, and the exact
JSON serialization is the charged artifact. Neither a passing mock nor an
unexercised guard is evidence of a real request or sandbox.

An independent AI validator ran all nine current `tests/test_maintenance.py`
tests with `.venv\Scripts\python.exe -m unittest discover -s tests -p
test_maintenance.py -v`: nine passed. That pass did **not** cover all requested
invariants: explicit predecessor/current-task content, malformed runtime JSON,
line counts, timeouts and seed-only reconstruction still need targeted coverage.
Do not describe the nine-test pass as complete apparatus validation.

One trusted C# seed build with eight independently specified cases initially
passed six. It accepted an ID ending in newline and checked a numeric value
before a different field's invalid type. Strict whole-string ID matching and
an up-front operation shape phase repaired both. The identical independent
eight-case rerun passed build, runtime and behavior. Repaired source SHA-256:
`Program.cs=bd815731aeb495ffcaf17d066e6ac5fe8fb35cbcfb6ca79d2bf29831ace434f5`,
`Simulation.csproj=1f638de8c09974d0ca7dda36c16d766c24398e36a538dd5a5a8e1af128526234`.
This is a smoke check, not complete seed equivalence or candidate evidence.

The first hand-derived private case draft also contained oracle defects:
incorrect queue effects/errors, live mover fields confused with snapshot fields,
overflow inputs outside the spawn domain, and omitted snapshot-schema
supersessions. It is undergoing an independent contract-based correction before
reference acceptance. Neither implementation is to be changed to satisfy an
incorrect expected result. The case author did not inspect either language's
source; that separation did not guarantee correct arithmetic or interpretation.

Both authors performed trusted seed builds during preparation; those host builds
are not candidate-isolation tests. Their generated seed-directory build outputs
are being removed from the flat source bundles. The constructor injects the SDK
pin in owned temporary build directories; it must not count or accept another
unreviewed seed `global.json`.

F# initially passed six of the same eight cases: mixed shape/value ordering and
boolean count classification were wrong. Its first repair introduced an
indentation error and failed compilation (zero cases executed). After a syntax
repair, the identical independent eight-case rerun passed build/runtime/behavior.
Repaired `Simulation.fs` SHA-256 is
`43a9669e7184f50a5067ef36db5f82cc6a567997638287504761aaec653f8916`;
`Simulation.fsproj` is
`5cc8c353cf25358615df7f9996b8b57fdc3a8cbf469c41b5c9b08324b13f831e`.

The oracle audit corrected the initial expected-output defects and explicitly
retained identical behavior across snapshot-shape supersessions at episodes
4, 5 and 6. An absent `through` means episode 8, not only the introduced stage;
the initial reviewer's contrary interpretation was corrected against the helper
and cumulative-obligation design. This is an AI contract audit, not human review.

Episode 7 also needed a pre-freeze arithmetic clarification: repeated ticks can
stay in range even when `count * velocity` alone exceeds int64 and the starting
position cancels that excess. The fast-forward contract now allows exact wider
intermediates and checks final state ranges, preserving its stated equivalence
to repeated ticks. This was found analytically before reference acceptance or
candidate outcomes, not selected from a language performance result.

The final static AI review found nested-operation classification holes. Episode
1 now states the intended pre-freeze boundary explicitly: only currently
introduced names are recognized; unsupported recognized operations validate
their immediate fields/types before rejection, but do not execute or inspect
nested payload semantics/world references. Supported spawn/remove retain full
shape/domain checks. This prevents a future operation from leaking into an
earlier stage and avoids treating an unsupported operation as a second evaluator.
Both language lineages need matching introducing-stage repairs and regressions.

Episode 4's exposed queue order also required an explicit allocation rule:
enqueue uses the maximum **currently pending** order plus one, or zero for an
empty queue. Import/load accepts a valid `Int64.MaxValue` order; overflow occurs
only if a later enqueue needs its successor. Drained historical orders are not
hidden snapshot state. This pre-freeze clarification is now in the public task
and has contract-derived import/drain/re-enqueue witnesses.

The constructor's expanded affected-test manifest now has **19 passing tests**
under the exact focused unittest command above. It covers strict runtime JSON,
line counts, timeouts, typed equality, patch encoding/newline behavior and all
16 predecessor/current-episode envelope mappings. The token proxy is explicitly
`tiktoken==0.14.0`, `o200k_base`; a misleading temporary package/encoding label
was corrected. Reference-output measurements include an empty
`architecture_notes` field and remain lower bounds excluding actual notes and
native/model framing, not measured candidate outputs.

There are **70 hand-derived cases** after the independent oracle corrections
and a separate ten-case import/boundary addition. The latter author read the
contracts, not either language implementation, and checked malformed pending
imports, maximum ordinals, nonempty policy and async-ledger restoration,
inconsistent imported references, and overflow-safe follower comparison.
Two further contract-derived regressions cover deferred removal canceling future
removes and detaching follower targets across ID reuse. Their author again did
not inspect implementation code. The 70-case raw file SHA-256 is
`2eda8ac85b61b41a8ec29d5d6ad02727415a770f1c419c86ff72fa8fcd9c34ed`.
One reviewed literal input/output example was copied into each episode, and
matching case inputs (including their later schema variants) were marked public.
No expected behavior changed in that visibility/formatting edit. Those examples
must never be misrepresented as hidden evaluation tests.

Retained cumulative construction checks:

- [First reference attempt](../results/maintenance-construction-first-reference-check/report.json):
  both seeds passed ten cases each; later stages failed before execution because
  PowerShell had emitted UTF-16 C# diffs and BOM/CRLF F# diffs. Direct Git
  `--output` exports and per-call `core.autocrlf=false` corrected the transport.
- [Second reference attempt](../results/maintenance-construction-reference-check-02/report.json):
  all tested checkpoints built and ran. C# lost queued state at operation commit;
  F# omitted successful due-command effects. C# follower wire fields were also
  missing at episode 3, and saved pending work was lost. The contracts, not the
  implementations' agreement, adjudicate these errors.
- [F# prefix recheck](../results/maintenance-construction-fsharp-prefix-check-03/report.json):
  19 unit tests and the ten-case seed passed. The claimed inner-effect repair
  still failed in episodes 1/2; episodes 3/4 also reset many valid requests to
  `invalid_shape`. Build/runtime success did not establish semantic validity.

These `results/` paths are local retained development outputs, not yet a public
evidence archive. Preserve them during repair and curate the needed records for
the eventual handoff. No reference successor is accepted merely because it
compiles. Known gaps in snapshot/policy code and patch integration are ordinary
unfrozen construction defects, not candidate failures or scientific revisions.

The [C# prefix recheck](../results/maintenance-construction-csharp-prefix-check-04/report.json)
now passes checkpoints 0 through 4 with 10/13/16/20/27 applicable cases.
Checkpoint 5 passes 29/31: the two remaining failures show normal movement
bypassing an assigned clamp before the follower phase. This narrow scope does
not accept later episodes, prove all possible inputs or validate a live runner.
The C# repair now resolves an entity's assigned registry **name** to its policy
kind, rather than comparing the name to `clamp10`. F# repair also removed an
import-parser filtering bug that silently dropped malformed pending entries;
every imported entry must validate before the snapshot is accepted. Corrected
prefixes are awaiting the strengthened 68-case independent check; successful
author builds alone do not close that gate.

The strengthened prefix-05 checks retained separate
[C#](../results/maintenance-construction-csharp-prefix-check-05/report.json) and
[F#](../results/maintenance-construction-fsharp-prefix-check-05/report.json)
reports. Both languages passed checkpoints 0–3. C# had one wrong import error
classification in 4/5; F# still omitted snapshot mover kind tags, wrapped imported
int64 arithmetic and misclassified a nested unknown command. These were repaired
at episode 4 and propagated. Further C# inspection found deferred-removal
cleanup missing at episodes 2/3; those fixes were moved to the correct introducing
patches rather than first appearing in episode 6.

The validator's prefix-05 final message accidentally quoted the older 58-case
hash. The retained F# report correctly records the 68-case raw hash
`5a95aff8deeb4fc82b9f917a00b0a2eed48bfe9ce26d6124401d5bf67a643f8d`;
the C# report omitted a top-level fixture hash and cannot independently establish
that field. Neither report was rewritten. The next shared report must record
the raw fixture and checker/patch identities explicitly.

The [70-case prefix-06 report](../results/maintenance-construction-prefix-check-06/report.json)
records all 14 serial isolated trusted targets with raw fixture, checker, seed,
patch and reconstructed-source identities. C# checkpoints 0–6 pass
10/13/17/22/31/37/44 cases (174 total applicable checks). F# passes 0/1;
the two new deferred-removal witnesses expose missing cleanup in its separate
due-command path. The author repaired cancellation at episode 2, detachment at
episode 3 and propagated through episode 8. Those new patches still require an
independent rerun, not acceptance from compilation alone.

The [separate reference review](../reports/maintenance-sim-construction-2026-09-12/reference-review.md)
then requested consolidated fixes for nested-operation classification and exact
follower/snapshot validation. It did not inspect evaluator cases or measurements.
Its old F# source identities were partly superseded during concurrent repair;
that limit is explicit and no unbound approval is claimed. The seed-only approval
does not approve these later references. Both authors are repairing the
introducing stages while a contract-only author adds targeted regression cases.

The original separate language authors retained their temporary histories and
stopped after unresolved cumulative implementation gaps. Separate senior AI
repair passes now own each reference lineage. F#'s author and repairer have not
been instructed to translate C# code. The C# senior repairer had previously
audited the oracle without language-code access; later implementation access
limits independence of any subsequent C# review by that same agent. Final review
must state that provenance, not call all authoring and review independent.

A separate seed-only AI review inspected both unchanged seeds, the seed contract
and guidance, but no future episodes/reference code, evaluator cases, outcomes
or size measurements. It found no externally testable seed defect or P0/P1
blocker, and found both idiomatic starting points plausible. It identified more
explicit architectural support in F# guidance. Before any candidate outcomes,
common guidance now gives both languages the same ownership/transition/effect
boundary advice; C# guidance also names encapsulated state, owned collections
and private helpers. This is supported maintenance, not unaided architecture
discovery. The review's visibility/style observation does not mandate a seed
rewrite: JSONL is the only public task contract, not a particular source API.

The common guidance now also distinguishes the archived `architecture_notes`
impact explanation from durable Markdown files explicitly submitted in `files`.
Only the latter persist as candidate repository state and all supplied bytes
are charged. No uncharged researcher summary or automatic transcript memory
is introduced. These construction clarifications remain subject to the human
review packet; they do not activate a candidate controller.

The targeted static-review regressions bring the fixture set to **80 cases**.
They check operation-name availability at each introducing episode, immediate
shape checks before unsupported-command rejection, null follower input targets
and atomic snapshot entity-validation precedence. Their author did not inspect
language implementation code. Raw case-file SHA-256:
`7131882aa7fac3b6f5305ea75c7080de18c5bec22dbd86be60036c4a9433f2f5`.

## Future runner boundary (not implemented or authorized here)

A read-only source scout identified the small adaptation surface:

- [h_sandbox.py](../src/alf/h_sandbox.py) currently materializes an OrderFlow
  baseline. Simulation needs a separately reviewed baseline/project descriptor,
  including `Simulation.fs` rather than assuming `Program.fs`; do not silently
  mutate the prepared H definition or call its existing checks proof of the new
  source family.
- Reuse the isolation boundary in [e3a_sandbox.py](../src/alf/e3a_sandbox.py):
  exact image, credential-free candidate execution, network disabled, read-only
  protected mounts and bounded scratch space. The trusted host constructor is
  not that boundary.
- Reuse the guarded full-file submission validation in
  [workstream_e3a.py](../src/alf/workstream_e3a.py) and accounting/no-tools adapter
  in [e3a_codex.py](../src/alf/e3a_codex.py), after reviewing their task-specific
  assumptions. Durable notes must be charged ordinary candidate state.
- A maintenance-specific finite controller must retain safe wrong/noncompiling
  code across eight fresh one-submission conversations, record malformed
  submissions without applying them, and never consult private scores for
  continuation. Existing stop-on-failure/general host-evaluator paths do not
  implement this policy.

That future adapter needs focused state-retention, protected-project/path,
no-tools/no-reissue, dispatch/usage/byte/time and model-free sandbox integration
tests. No adapter, model allocation or live permission is supplied by this
construction record. Constructor bounds are not experimental candidate limits.

## Historical pre-check-02 evidence plan (superseded)

This pre-check-02 plan is retained for history; its pending language is
superseded by the final validated checkpoint below.

The bounded fault audit will use four explicit, compile-successful behavioral
mutations per language: lost due-command effects (episode 1), omitted future
remove cancellation (episode 2), bypassed named policy (episode 5), and leaked
temporary replay registry (episode 8). Each requires an identified contract case
that passes on the reference and fails on the mutant. These eight witnesses are
not exhaustive mutation coverage or an architectural quality score. Mutations
apply only to owned trusted fixture copies; reference patches remain unchanged.

The applicability audit will distinguish fixed no-op and malformed-response
fixtures (unchanged source), an intentionally noncompiling predecessor, a
missing-feature predecessor and a compile-successful wrong-behavior predecessor
at the episode-1-to-2 transition. A separate correct episode-2 control can show
recovered cumulative behavior without erasing the earlier failure; it is not an
actual candidate repair or a gold reset. Running the unchanged seed against a
named current-obligation witness from each later episode will also check that
the public tasks remain externally evaluable with missing prior features.
Record prerequisite/current correctness separately and leave both unknown when
evaluation cannot run; causal attribution remains unknown without a witness.
These are workload-applicability checks, not evidence that a future candidate
controller already enforces persistence or malformed-submission handling.

1. Two functioning seeds and eight reference deltas per language, with exact
   source and task identities.
2. Shared public and evaluator cases covering cumulative semantics, explicit
   contract supersessions, boundary inputs and snapshot/replay equivalence.
3. Compile-successful semantic fault witnesses in both languages, distinguished
   from compiler/runtime failures.
4. Applicability checks on unchanged, non-compiling, missing-prerequisite and
   wrong-behavior predecessors, with separate disposition/prerequisite/current
   correctness/evaluation-availability classifications. These are constructed
   fixtures, not candidate trajectories or observed architecture decay.
5. Complete authored-input and full-file-change output audits, an identified
   optional offline token proxy, and language-symmetric proposed budgets.
6. Independent AI contract/language/implementation review with findings and
   limitations; no fictional human sign-off.
7. Focused affected tests and trusted builds, followed by exact-publication CI.

The single pair/eight episodes establish at most construction feasibility. A
larger sampling frame, main-study horizon and live quotas remain unset. A fast
large-count arithmetic witness is not a comparative performance result. New
context and output caps will be proposed after measurements, not silently copied
from H or selected to favor one language.

Before the complete size audit, the proposed common-budget rule is recorded:
round **1.25 times the largest complete reference input envelope** up to a
4,096-byte boundary for input; for output, add a 4,096-byte serialized-note
allowance to the largest empty-note reference replacement, multiply by 1.25 and
round up likewise. Apply the same rule to the pooled language/episode set. This
is an openly chosen feasibility allowance, not an optimal threshold or provider
token limit. Any candidate growth beyond it remains an explicit policy outcome.
Numeric proposals await the audit; no candidate protocol or cap is activated.
Offline lower-cap coverage can be tabulated without redispatching identical
prompts. Actual information-availability interventions and a larger project
sample remain separate design decisions, not implied by these byte measurements.

## Historical resumable checkpoint before complete-check-02 (superseded)

Everything in this section describes the state before complete-check-02 and is
historical only; it is not the current construction status.

The first complete check is retained at
[complete-check-01](../results/maintenance-construction-complete-check-01/report.json).
All nine C# checkpoints passed 304 applicable case evaluations; F# had eight
mismatches across checkpoints 2–8, all involving future-remove cancellation.
Seven fault witnesses qualified; F# cancellation did not, because its reference
baseline was wrong. The F# recovery control likewise failed rather than being
credited as recovery. These are construction outcomes, not language-performance
observations from an experiment.

A fresh senior repair session traced the missed state flow: `tickWorld` retained
the due command's updated `current.Pending`, then overwrote it with the earlier
`later` list. Episode 2 also lacked cancellation on its direct-remove path. Both
were repaired at episode 2 and propagated through 8; the original seed/episode 1
and all four fault patches stayed unchanged. Both cancellation cases now pass
author diagnostics at checkpoints 2 and 8, and the deliberate cancellation
mutant still compiles and fails. Full independent revalidation remains separate.

The validation launcher also had an assistant execution-management error: a
completed orchestration cell was mistaken for an exited shell command, and a
second identical model-free check was started. Read-only process inspection
proved both alive. Only the verified duplicate tree (PowerShell PID 9056,
started 15:36:49 HKT on 2026-09-12) was stopped; the original Python PID 29144
was left to finish under a scripted wait and produced the retained report.
No unrelated process or file was removed. A nested command `session_id` means
still running and must be polled; absent output/report is not retry permission.

The apparatus review also required raw checker/helper/test/fault-manifest hashes
in emitted provenance. That repair and POSIX-relative path keys are now covered
by a new regression: 27 focused tests pass in the author's check. The original
26-test independent pass and complete-check-01 report remain unchanged; the
repaired full check uses a new output directory and a single invocation.

Both ten-case seed checks and 19 apparatus tests passed. All eight reference
deltas now exist in each language and author reconstruction/build checks pass.
They are not all semantically accepted: the final cancellation repair and
provenance changes were undergoing independent complete-check-02 validation.
Final measurements, review and exact CI remain. Do not publish
the current construction as completed workload evidence at that historical checkpoint.
Contract clarification and model-free construction are active. Do not publish
incomplete scaffolding as completed evidence. Resolve ordinary defects, validate
the bounded artifacts and return with a standalone review packet listing actual
values, source locations, checks and the specific safe runner adaptation still
needed. Keep construction, scientific approval and live allocation separate.

## Final validated checkpoint

The complete trusted audit passed: 80 cases, 18 targets, 608 applicable checks,
16 envelopes, 8 semantic faults, 12 failure-transition scenarios and 16
missing-feature witnesses. Raw byte-preserving artifacts are indexed [here](../reports/maintenance-sim-construction-2026-09-12/evidence/index.json)
with [report](../reports/maintenance-sim-construction-2026-09-12/evidence/report.json)
SHA-256 `ab6e5a53023929b7d731a6675a455c3c877f1b42064b9d258c84bce152f2fea5`.
The independent AI validator reported 27/27 tests; CI on the implementing
publication is pending and baseline green is not reused. This is trusted
model-free construction only: no provider/model/candidate claim, approvals
false, allocations zero, proposed caps 86,016 input / 61,440 output bytes, and
the future isolated adapter is not implemented. F# inputs remain larger at all
eight episodes.

Exact validation commands were:
`.venv\Scripts\python.exe -m unittest discover -s tests -p test_maintenance.py -v`
and
`.venv\Scripts\python.exe scripts/maintenance_check.py --build-fixtures --audit-failures --output-dir results/maintenance-construction-complete-check-02`.
