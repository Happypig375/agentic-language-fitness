# H1/H2 human review before execution

Status: **UNAPPROVED — pre-execution review only**  
Implementation revision under review: source snapshot [`c87df747c783c0649cb66d5c1bbaf9ee11adf9d5`](https://github.com/Happypig375/agentic-language-fitness/tree/c87df747c783c0649cb66d5c1bbaf9ee11adf9d5) (the docs-only publication may be later)  
Specification: [`protocols/workstream-h1-h2/specification.json`](../protocols/workstream-h1-h2/specification.json), SHA-256 `e05213330c400ee2e2e857a43f2730c640d3231669807fa5a1a92804ee079c8c`  
Exact implementing CI: [run 34335495891](https://github.com/Happypig375/agentic-language-fitness/actions/runs/34335495891) (Linux 8m10s; Windows 8m52s)

This document answers what a human must inspect before approving any live H1/H2
integration or pilot. Construction is approved, but no **live H execution**,
OAuth staging, model/count request, candidate run, allocation, or sign-off has
occurred. Trusted fixtures and bounded native loopback probes were executed as
model-free evidence; they are not live H execution. The
specification currently has `execution_authorized=false`,
`user_live_execution_approved=false`, `analysis.human_review_approved=false`,
`approved_integration_dispatches=0`, and `approved_pilot_dispatches=0` ([JSON
fields](../protocols/workstream-h1-h2/specification.json)).

## 1. Question and design

The question is whether two languages can complete the same bounded Task 008
summary-API refactoring under a controlled source/context and interaction policy.
This is a one-authored-family construction with two dependent feature-load levels,
not a language ranking, retrieval experiment, scaling slope, or universal context
claim. The adopted construction is documented in the [bounded overlap proposal](workstream-h1-h2-overlap-design-2026-09-09.md).

| Level | Candidate receives | Gold-only addition | Source of truth |
| --- | --- | --- | --- |
| Core | H0 predecessor and the Task 008 public task | `summary` behavior | [`protocols/workstream-h0/definition.json`](../protocols/workstream-h0/definition.json), [`benchmarks/successor/tasks/008-summary-api/task.md`](../benchmarks/successor/tasks/008-summary-api/task.md) |
| Expanded | Core predecessor plus functioning `reconcile` and `dependencyOrder` features | Task 008 summary while preserving both APIs | [`benchmarks/workstream-h/contract.md`](../benchmarks/workstream-h/contract.md), [`benchmarks/workstream-h/public-examples.json`](../benchmarks/workstream-h/public-examples.json) |

Task 008 adds `summary`, returning integer keys `pending`, `processing`,
`completed`, `cancelled`, and `overdue`. Status matching is case-insensitive;
`overdue` counts pending/processing orders with strict `dueAt < asOf`, overlaps
status totals, and is zero when `asOf` is missing or null. Existing operations,
stateless JSONL I/O, extracted engine architecture, and errors remain intact.
Expanded `reconcile` rejects duplicate IDs within either side; for an ID present
on both sides it selects higher priority, then later creation instant, then the
right record on an exact tie, labels origin, and emits ordinal-sorted output.
`dependencyOrder` returns a
deterministic ordinal topological order or its declared validation error.

The fixed inference is “one authored family, two dependent functioning off-task
feature-load levels” (`workload.inference` in the specification). H2's extra
turns are part of the treatment package; they cannot be interpreted as an
isolated retrieval effect.

## 2. Exact workload sources to inspect

The reviewer should inspect the predecessor/gold pairs below, then verify the
target task, public examples, sealed cases, and rubric separately. Gold and sealed
cases are evaluator-only and must never enter a candidate request.

| Pair | Predecessor | Gold / target implementation | Canonical pair identities |
| --- | --- | --- | --- |
| Core C# | [`benchmarks/successor/representation-v1/transformed/descriptive/csharp/gold/007-query-engine-refactor/`](../benchmarks/successor/representation-v1/transformed/descriptive/csharp/gold/007-query-engine-refactor/) (engine+Program overlay; inherited project is [`.../baseline/OrderFlow.csproj`](../benchmarks/successor/representation-v1/transformed/descriptive/csharp/baseline/OrderFlow.csproj)) | [`benchmarks/successor/representation-v1/transformed/descriptive/csharp/gold/008-summary-api/`](../benchmarks/successor/representation-v1/transformed/descriptive/csharp/gold/008-summary-api/) (stage-8 engine+Program overlay; composed by `workstream_e3a.snapshot`) | predecessor `7bed422fb8ae11147939973bb89bd5fc10ed26856a3aa8502123eee59f909f6f`; gold `5f378f63f9891753736993eaee2b4f7091df7ff4bebedec964ada00c59e4c7aa` |
| Core F# | [`benchmarks/successor/representation-v1/transformed/descriptive/fsharp/gold/007-query-engine-refactor/`](../benchmarks/successor/representation-v1/transformed/descriptive/fsharp/gold/007-query-engine-refactor/) (stage-7 source; selected by [`h0.source_for`](../src/alf/h0.py)) | [`benchmarks/successor/representation-v1/transformed/descriptive/fsharp/gold/008-summary-api/`](../benchmarks/successor/representation-v1/transformed/descriptive/fsharp/gold/008-summary-api/) (all three files; selected by [`h_workload.source_for`](../src/alf/h_workload.py)) | predecessor `53a20231120cd69ed2d540c47b9dff1d5b77a37391381445c8b8ec875ad9495b`; gold `6b8a3de461fd2cd21ff77d8d1341baacf6f504208fc99bc9ac59ca17bc544ede` |
| Expanded C# | [`benchmarks/workstream-h/repos/csharp/expanded/`](../benchmarks/workstream-h/repos/csharp/expanded/) | [`benchmarks/workstream-h/gold/csharp/summary/`](../benchmarks/workstream-h/gold/csharp/summary/) | predecessor `fcf44bbc5f05e525ccd3bb59603ad3d526d897ecd0832d42a261bc033cba5f9d`; gold `35436e5475838723d1d6f8bcd050f16b6bcb3c300ca70294cf4c021bbc6803a3` |
| Expanded F# | [`benchmarks/workstream-h/repos/fsharp/expanded/`](../benchmarks/workstream-h/repos/fsharp/expanded/) | [`benchmarks/workstream-h/gold/fsharp/summary/`](../benchmarks/workstream-h/gold/fsharp/summary/) | predecessor `9ab51cdbca67a5c52f48eb411034d859857361c18d24fb09d9b825bc5bbbd159`; gold `4d04fe0e41497da2167ec19b202a627673a299471e2ed935038219b24de87f65` |

These are canonical filename-to-LF-source mapping hashes from the [source review](../reports/workstream-h1-h2-preexecution-2026-09-09/source-review.md), not concatenated file hashes. Inspect that review's evaluator-only relevance map: `domain_model_in_engine`, `live_dispatch_in_engine`, `program_io_boundary`, and `summary_in_engine`. Required source judgments missing at review time remain unknown.

### Identity labels

| Identity | Value | Meaning / exact location |
| --- | --- | --- |
| Specification canonical JSON | `2c2dde84e6261b2578bf21944a3a0ad932403c89ec0bd4490713f367dbd1a07e` | `canonical_json_hash(spec)` in [`src/alf/protocol.py`](../src/alf/protocol.py) applied to the specification; not a report-byte hash |
| Scientific policy | `ec2638862df05cda74bf415d86a9e1b8dbeb24f9f504ccd00767253daa38d7d9` | `policy_sha` calculation in [`src/alf/h_run.py`](../src/alf/h_run.py); approval/bookkeeping fields excluded |
| Construction report bytes | `eea708fb2e79eba1e96aaf2e25593dfd769d08fb52b6fc11b575509bffd549da` | Raw report-byte hash for [`construction/report.json`](../reports/workstream-h1-h2-preexecution-2026-09-09/construction/report.json) |
| Specification LF source-file bytes | `e05213330c400ee2e2e857a43f2730c640d3231669807fa5a1a92804ee079c8c` | Current LF-normalized specification file bytes; not the canonical JSON hash |
| Workload source canonical hash | `8766bf2da799a351c002a90b23a6443ceff94a8df6b9a15b46a93bce3b04febc` | `workload.source_sha256` in [`specification.json`](../protocols/workstream-h1-h2/specification.json), filename-to-LF mapping |

| Review item | Exact location | What to inspect |
| --- | --- | --- |
| Task and public contract | [`benchmarks/successor/tasks/008-summary-api/task.md`](../benchmarks/successor/tasks/008-summary-api/task.md), [`benchmarks/workstream-h/public-examples.json`](../benchmarks/workstream-h/public-examples.json) | Task 008 behavior, input/output shapes, no accidental successor leakage |
| Expanded operation contract | [`benchmarks/workstream-h/contract.md`](../benchmarks/workstream-h/contract.md) | `reconcile` and `dependencyOrder` behavior and validation precedence |
| Sealed behavioral cases | [`h_workload.cases_for`](../src/alf/h_workload.py) assembles [`benchmarks/successor/manifest.json`](../benchmarks/successor/manifest.json) baseline/Tasks 001–008 plus Expanded additions; `workload.cases_sha256=6bb0c80d42b5a365e788a0164f33a2cf6d6612988426db0d16edf9c782a10e5e` in [`specification.json`](../protocols/workstream-h1-h2/specification.json) | [`h_check.py`](../src/alf/h_check.py) assembles/hashes; trusted evaluation is [`h_fixtures.evaluate_trusted`](../src/alf/h_fixtures.py) / `evaluate_with_sandbox`, with live evaluation routed by [`h_run.py`](../src/alf/h_run.py). [`h_workload.oracle_additions`](../src/alf/h_workload.py) is the independent Expanded oracle. Case material is evaluator-only |
| Architecture rubric | [source-review.md](../reports/workstream-h1-h2-preexecution-2026-09-09/source-review.md), “Evaluator-only rubric and relevance map” | Human final-source review remains separate from AI source review |

## 3. Caps and authored-byte interpretation

The common authored-input caps are **18,432 bytes (low)** and **35,840 bytes
(high)**. The measured maxima are `A_core=16,418` and `A_all=34,163` complete
authored bytes. Applying `ceil((A + 1,024) / 1,024) * 1,024` once gives the two
caps. Instructions are already included in each complete replay; the 1,024 bytes
are one construction headroom allowance, not an extra instruction charge. The
exact governing fields are
`budgets.unit=complete-authored-input-utf8-bytes`,
`budgets.reference_headroom_bytes=1024`, `budgets.reference_rounding_bytes=1024`,
`budgets.cap_low=18432`, and `budgets.cap_high=35840` in the
[specification](../protocols/workstream-h1-h2/specification.json); construction
measurements and derivation are in [`construction/report.json`](../reports/workstream-h1-h2-preexecution-2026-09-09/construction/report.json).

These are authored-byte policy limits, not verified provider context limits.
`budgets.provider_context_limit_verified=false` and the construction report's
`context_accounting.provider_context_limit=null` must remain visible. Native
token proxies, hidden provider bytes, native-added messages, and any provider
serialization are outside this authored-byte measurement; they do not establish
physical fit. No padding or outcome-driven cap choice is allowed.

## 4. All 16 reference envelopes

Each row is one exact file in [`construction/`](../reports/workstream-h1-h2-preexecution-2026-09-09/construction/).
“Initial/full” lists authored UTF-8 bytes for the first map/supplied request and
the largest request recorded in that envelope. H2's full value can exceed the
initial value after later reads; that is a policy outcome after a feasible start.

| Envelope | Level | Language | Policy | Order | Initial/full bytes |
| --- | --- | --- | --- | --- | ---: |
| [01](../reports/workstream-h1-h2-preexecution-2026-09-09/construction/envelope-01.json) | Core | C# | H1 | forward | 15,832 / 15,832 |
| [02](../reports/workstream-h1-h2-preexecution-2026-09-09/construction/envelope-02.json) | Core | C# | H2 | forward | 8,647 / 16,418 |
| [03](../reports/workstream-h1-h2-preexecution-2026-09-09/construction/envelope-03.json) | Core | C# | H1 | reverse | 15,832 / 15,832 |
| [04](../reports/workstream-h1-h2-preexecution-2026-09-09/construction/envelope-04.json) | Core | C# | H2 | reverse | 8,647 / 16,418 |
| [05](../reports/workstream-h1-h2-preexecution-2026-09-09/construction/envelope-05.json) | Core | F# | H1 | forward | 15,621 / 15,621 |
| [06](../reports/workstream-h1-h2-preexecution-2026-09-09/construction/envelope-06.json) | Core | F# | H2 | forward | 8,647 / 16,207 |
| [07](../reports/workstream-h1-h2-preexecution-2026-09-09/construction/envelope-07.json) | Core | F# | H1 | reverse | 15,621 / 15,621 |
| [08](../reports/workstream-h1-h2-preexecution-2026-09-09/construction/envelope-08.json) | Core | F# | H2 | reverse | 8,647 / 16,207 |
| [09](../reports/workstream-h1-h2-preexecution-2026-09-09/construction/envelope-09.json) | Expanded | C# | H1 | forward | 33,116 / 33,116 |
| [10](../reports/workstream-h1-h2-preexecution-2026-09-09/construction/envelope-10.json) | Expanded | C# | H2 | forward | 16,327 / 34,163 |
| [11](../reports/workstream-h1-h2-preexecution-2026-09-09/construction/envelope-11.json) | Expanded | C# | H1 | reverse | 33,116 / 33,116 |
| [12](../reports/workstream-h1-h2-preexecution-2026-09-09/construction/envelope-12.json) | Expanded | C# | H2 | reverse | 16,327 / 34,163 |
| [13](../reports/workstream-h1-h2-preexecution-2026-09-09/construction/envelope-13.json) | Expanded | F# | H1 | forward | 31,630 / 31,630 |
| [14](../reports/workstream-h1-h2-preexecution-2026-09-09/construction/envelope-14.json) | Expanded | F# | H2 | forward | 16,213 / 32,406 |
| [15](../reports/workstream-h1-h2-preexecution-2026-09-09/construction/envelope-15.json) | Expanded | F# | H1 | reverse | 31,630 / 31,630 |
| [16](../reports/workstream-h1-h2-preexecution-2026-09-09/construction/envelope-16.json) | Expanded | F# | H2 | reverse | 16,213 / 32,406 |

## 5. Schedule, feasibility, and interaction policy

The fixed schedule has **32 slots / 16 adjacent language pairs**. The exact
ordering, pair IDs, language order, policy, level, and cap are in
[`construction/schedule.json`](../reports/workstream-h1-h2-preexecution-2026-09-09/construction/schedule.json), with SHA-256 `025d532b275b97419f7b6afa20067b410a8282127e84f0edefe18af0e8af0673`.
The feasibility mask is [`construction/feasibility-mask.json`](../reports/workstream-h1-h2-preexecution-2026-09-09/construction/feasibility-mask.json), SHA-256 `90fb82cbde2ec1505d8362f29ae62efe52ba406b2d7f7b507e229a9c167e69ca`.

There are **28 initially feasible slots**. Only Expanded/H1/low is excluded
(both languages and both orders: four slots, two pairs). Expanded/H2/low starts
from its map-only request; later reads may exhaust the cap and remain a recorded
policy outcome. At most 60 dispatches can arise from the 28 feasible slots; the
proposed 64 ceiling does not create another slot, retry, or replacement.

### H1

All source files are supplied in the authored request. The candidate has one
submission and no feedback or repair. H1/low Expanded is unexecuted infeasibility,
not a model error. Exact policy is `controller.h1` in the specification.

### H2

The candidate receives a finite resident source map, may make at most two atomic
whole-file reads, and then has a final-only submission. Reads are one to eight
distinct eligible root filenames; an over-budget multi-file read is refused
atomically. Resident full text, accepted read actions, and result metadata are
retained in every request. H2 read overflow is terminal authored-budget
exhaustion, with no exposure or further dispatch. Extra H2 turns are an explicit
limitation and treatment component, not hidden context or an isolated causal
factor. Exact policy is `controller.h2` and `controller.memory` in the
[specification](../protocols/workstream-h1-h2/specification.json), with request
examples in each envelope's `requests[].replay_utf8`.

Both policies enforce `submission=...full-file replacements`, no deletions,
maximum eight source files, one isolated fresh-source evaluation, no score
return, `feedback=false`, `repairs=0`, and zero automatic retries or replacements.

## 6. Limits, alarms, scoring, and blinding

| Boundary | Current value / rule | Exact source |
| --- | --- | --- |
| Submission/workspace | 49,152 / 65,536 bytes; replay 131,072 bytes | `authority.max_submission_bytes`, `max_workspace_bytes`, `max_replay_bytes` |
| Files | max source files 8; max total files 8; no deletions | `authority.max_source_files`, `max_total_files`, `deletions` |
| Time | request 120s; trajectory 600s; controller build 60s; development and holdout execution 10s | `budgets.request_timeout_seconds` through `holdout_execution_timeout_seconds` |
| Token alarms | 32,768 input and 8,192 output+reasoning are post-turn alarms, not provider hard caps | `budgets.request_input_tokens`, `request_output_tokens_including_reasoning`, `request_limits_semantics` |
| Controller output | 1,048,576 bytes | `budgets.controller_output_bytes` |
| Byte alarms | Complete authored-input UTF-8 bytes; valid over-allowance terminates that fixed trajectory | `budgets.unit`; `controller.read_overflow`; implementation [`src/alf/h.py`](../src/alf/h.py) |
| Feedback/repair | no feedback, one final submission, no repair, retry, or replacement | `controller.feedback`, `repairs`, `automatic_retries`, `automatic_replacements` |
| Scoring | one fresh isolated evaluation after interaction; no score returned to candidate | `controller.scoring`; [`src/alf/h_sandbox.py`](../src/alf/h_sandbox.py) |
| Null/usage | missing usage remains null; token subsets are not added twice; subscription USD is null | `context_accounting` and `budgets.subscription_usd` in construction report/spec |
| Blinding | reviewers must not see per-slot outcome/cost; unknown required judgment remains unknown | [`source-review.md`](../reports/workstream-h1-h2-preexecution-2026-09-09/source-review.md), rubric section |
| Hard stops | security; unknown/invalid usage; ambiguous dispatch; unexpected native tools/compaction; context rejection; cleanup unconfirmed | `controller.hard_stops` in [`specification.json`](../protocols/workstream-h1-h2/specification.json) |

Holdout scores cannot influence feedback, continuation, retry, or replacement.
For current task completion, missing required architecture rubric evidence remains
null/unknown; known format, build, or behavioral failure makes completion false
([`h_run.py`](../src/alf/h_run.py), completion decision around lines 132–138).
The four required rubric names are `domain_model_in_engine`,
`live_dispatch_in_engine`, `program_io_boundary`, and `summary_in_engine`. All
submissions and attempts must be retained.

## 7. Pinned model, client, catalog, image, SDK, and route

The specification pins requested model `gpt-5.6-luna`, reasoning effort `high`,
backend `local-OAuth-Codex-native-no-tools`, native binary SHA-256
`72cf14453c1879996b970accc7de9aa114bf570e586230799a429d0741bb1959`, and
catalog SHA-256 `c18214b1ba88ab9bd164753115324a7a29c0582e8d071f7b3babf749d892f549`.
`actual_version=null` and `h_live_integration_verified=false` remain explicit
([`model` fields](../protocols/workstream-h1-h2/specification.json)).

The evaluation environment is pinned to image
`sha256:5d3e97d195dbbe7e47e47055e46f8c6f15fb9553be0c7ef19ed0060756fc7116`,
SDK `10.0.302`, framework `net10.0`, Debug, 2 CPUs, 6,442,450,944 bytes,
512 PIDs, and evaluation network `none` ([`environment-profile.json`](../infra/remote-runner/environment-profile.json) and `environment` fields in the specification). Evaluation authentication is false. The runner is [`scripts/h_run.py`](../scripts/h_run.py), using the existing native transport, local OAuth direction, canonical foreground SSH route, and isolated evaluator. No new relay, proxy, listener, image, backend, or generic framework is part of this design.

Candidate execution must have no model credentials, host secrets, or writable
scoring machinery. The evaluator cannot fall back to host execution. OAuth must
not be staged until separately approved; the original local login remains
untouched. Authentication and route implementation is in
[`src/alf/e3a_runner.py`](../src/alf/e3a_runner.py), [`scripts/e3a_run.py`](../scripts/e3a_run.py),
and [`infra/remote-runner/`](../infra/remote-runner/); H's live account, route
behavior, and provider identity remain unverified. CI's read-only activation and
disabled SDK-fixture copy are model-free checks and never grant live permission.

## 8. Validation evidence and limitations

Exact CI [34335495891](https://github.com/Happypig375/agentic-language-fitness/actions/runs/34335495891) passed on the implementing publication. All **19 deterministic artifacts** matched published bytes on both Linux and Windows. The current host/Linux SDK sandbox matrices pass **8/8 positive workload targets and 28/28 fault checks**. The historical exact experimental-image matrix remains **27/28 initially caught**, plus **two independent repaired variants** and **26 unchanged identities**; it must not be relabeled as a historical 28/28 aggregate. See [`evidence/index.json`](../reports/workstream-h1-h2-preexecution-2026-09-09/evidence/index.json), [`fault-identity-comparison.json`](../reports/workstream-h1-h2-preexecution-2026-09-09/evidence/fault-identity-comparison.json), and the [implementation packet](workstream-h1-h2-implementation-2026-09-09.md).

The pinned native loopback fixture has **52/52 bounded probes** over 26 reference
requests. It used zero external provider calls and zero OAuth staging. This is
not universal no-tools proof: the retained `no_tools_verified` field is false.
It is also not real-provider context proof. Evidence is [`native.json`](../reports/workstream-h1-h2-preexecution-2026-09-09/evidence/native.json).

The construction report's pure-audit scope records `dispatches_performed=0`,
`live_execution_performed=false`, `model_free=true`, `native_invoked=false`,
`network_used=false`, and `oauth_staged=false`. Separate trusted fixture and
native-loopback evidence is linked above. Together these establish bounded
model-free preparation only; they do not establish provider behavior, account
access, physical context fit, or subscription cost. `subscription_usd=null`.

Current review findings are conditional: the paired AI source review found no
source-level blocker in the four bundles, subject to trusted behavioral and
mutation checks; both implementations preserve Expanded APIs and keep summary
out of predecessors. The same reviewer had earlier controller involvement, and
the same later AI session repaired both language implementations, so final
authorship is not independent. Human reviewers must make the scientific,
idiomatic, rubric, isolation, and allocation judgments below.

## 9. Human decision questions

Record evidence, not only “looks good,” for each domain:

1. **Workload and idioms:** Are C# and F# ordinary maintainable examples? Are
   Core predecessors free of summary? Do gold sources add only Task 008 while
   preserving earlier behavior? Are public examples and sealed cases adequate?
2. **Interpretation:** Is the dependent Core/Expanded feature-load comparison
   scientifically acceptable? Is H2's extra-turn policy accepted as part of the
   treatment? Is the design explicitly prevented from claiming a language winner,
   retrieval effect, slope, or general context limit?
3. **Caps and selection:** Do the cap derivation, all 16 envelopes, fixed seed,
   pair ordering, 32-slot schedule, and 28-slot mask match the intended question?
   Are authored bytes clearly distinguished from native/provider-hidden bytes?
4. **Interaction and scoring:** Are H1 all-source/one-submit and H2 map/two
   atomic-read/final-only rules understood? Is over-budget atomic refusal clear?
   Are no-feedback, no-repair, fresh-source scoring, null usage, and blinding
   rules acceptable?
5. **Security and provenance:** Are source/spec/report hashes, exact image/SDK,
   no-credential evaluation, isolated evaluator, cleanup, route, and no-tools
   evidence sufficient? Are no secret files or writable scoring paths exposed?
6. **Allocation:** Is a separate live integration authorized, and only after the
   exact reviewed revision and CI? Is a pilot separately contingent on a
   successful matching integration and freeze? Are no retries, extensions,
   replacements, or automatic reissues understood?

## 10. UNAPPROVED human decision form

Reviewer: ____________________________________  Date: ____________________  
Reviewed revision: `c87df747c783c0649cb66d5c1bbaf9ee11adf9d5`  
Exact CI checked: [34335495891](https://github.com/Happypig375/agentic-language-fitness/actions/runs/34335495891)  

| Domain | Findings / required corrections | Accept? |
| --- | --- | --- |
| Workload, predecessors, gold, idioms |  | ☐ |
| Scientific interpretation and H2 policy |  | ☐ |
| Caps, envelopes, schedule, feasibility |  | ☐ |
| Interaction, scoring, nulls, blinding |  | ☐ |
| Isolation, provenance, route, security |  | ☐ |
| CI/evidence and remaining live unknowns |  | ☐ |

Integration allocation (choose one):  
☐ No allocation  
☐ Contingent integration only: **3 planned dispatches**, hard maximum **5**  
☐ Other: ____________________ (must not exceed 5)

Pilot allocation (separate decision; not implied by integration):  
☐ No pilot allocation  
☐ Contingent fixed pilot, only after matching successful integration/freeze,
hard maximum **64 dispatches** across the fixed 32-slot schedule  
☐ Other: ____________________ (must not exceed 64)

No retries, sample extensions, replacements, automatic reissues, or relaxed hard
stops: ☐ acknowledged. Subscription USD: **unknown**.  

Human decision: ☐ remain unapproved  ☐ approve only the checked contingent scope above  
Signature / record: ______________________________________________

This form records a future human choice; completing it does not alter the
specification. Do not treat CI, hashes, model-free probes, or this document as
execution approval. No ready-to-run live command is included.
