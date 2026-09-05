# E3a review packet: shared first submission and bounded repair

**2026-09-05 — proposal, not a freeze or execution permission.** Prepared and
self-reviewed by the current Codex maintainer session (AI). No independent AI
session, language expert, or human has approved this specification. No candidate
model request, live continuation probe, or paid review agent was used.

The [specification](specification.json) and generated [review packet](review-packet.json)
contain the proposed identities, exact schedule, source/payload hashes, archived
selection observations, and budget calculation. `review-packet.json` is a drift
check, not a certificate or a second protocol. Source text identities normalize
checkout line endings to LF; JSON identities use the existing canonical hash.
The implementing Git commit and its CI checks are separate from the scientific
specification hash. This packet does not create an executable candidate runner.

## Question and selected workload

For a fixed predecessor, what is the correctness of one submitted patch, and
what additional resources accompany at most two development-guided repairs?
The first submission is the common prefix of the same trajectory, not a second
random draw. There is no randomized no-feedback continuation control, so repair
improvements cannot be attributed causally to feedback rather than extra work.

| Existing task | Predecessor | Reason for inclusion | Material pair differences |
|---|---|---|---|
| `001-priority` | Baseline, stage 0 | Small additive ordering task; relatively low source-diagnostic burden in archived M, not a claim that every first patch succeeded. | C# LINQ ordering and nullable properties versus F# records, generic comparison, and nullable interop. |
| `006-transition-validation` | Through task 005 | Validation-order, null handling, record/API/type changes; archived M F# contains both a failed and a successful observed first build. | C# class/record response types versus F# overlapping record fields and explicit annotations. |
| `007-query-engine-refactor` | Through task 006 | Multi-file model/dispatch extraction; all five archived F# runs changed the project here. | Explicit ordered F# Compile entries versus implicit C# file discovery. |

These are repository-authored synthetic OrderFlow business-service changes, not
transplanted issues from a sampled ecosystem. There is currently **no selected
repository license**; do not describe this packet as a third-party license grant.
All tasks are sequential JSON-line services using the .NET standard library;
no concurrency, throughput target, external database, or production deployment
obligation is added. Earlier error, ordering, response-shape, and statelessness
contracts remain in force. The modules are `Program`, the project, and (only
after extraction) `OrderFlowEngine`. Public task text and approved predecessor
source are the candidate's documentation; no research narrative is supplied.

Selection used [E1's archived report](../../reports/workstream-e-v3/forensic-report.json),
not new agent outcomes or token savings. The packet retains each selected task's
ten archived observations, including null first-build boundaries. In M, task
006's failing F# attempt records FS0001/FS0039/FS0764/FS1129/FS3566 plus warnings
and NETSDK1064; its other F# attempt has an observed successful first build.
Task 007's historical failed builds include dependency failures, not necessarily
source or compile-order errors. Task 001's two M C# observed first builds passed;
one M F# boundary passed and one is unavailable, with dependency repair evidence.
None of these fields is a count of independent compiler bugs.

Task 008 was not added: task 007 already supplies the required multi-file/API
role. No replacements or extra tasks may be chosen after new outcomes. This is
a mechanism-enriched feasibility pilot on three related tasks, not a sample of
all maintenance, pure syntax, native idiomaticity, or a language-by-size slope.
Previous solutions are public and may be contaminated; withholding them at run
time does not prove they were absent from model training. Repetition reduces
within-task stochastic uncertainty, not this workload-selection uncertainty.

### New reference limitation, preserved as an addendum

The new contract-derived priority holdout combines Int32 extremes, missing priority,
equal instants with different time-zone offsets, ordinal ID ties, and excluded
statuses. The archived F# task-001 target negates the priority in its sort key;
negating Int32.MinValue overflows. The trusted fixture asserts that this archived
target fails that boundary while the C# target passes. It does **not** weaken the
holdout, edit the archived target, or recalculate E1/E2/E2a.

The task contract says integer priority and does not exclude that value. The
proposal therefore keeps the case for both languages. Gold is a source archive,
not the final oracle. An independent reviewer must disposition this finding and
the new expectations before collection. An accepted alternative implementation
must satisfy the contract; matching the archived algorithm is not required.

## Candidate information, patch, and controller

The candidate receives only [instructions](candidate-instructions.md), a small
[baseline contract](baseline-contract.md), earlier task contracts, the current
task text, and the complete approved predecessor snapshot as inline LF source.
At repair it receives the current applied snapshot and development feedback.
There is no repository mount, filesystem inspector, shell, language server,
network tool, or candidate-side execution. Language syntax is necessarily
visible, but experimental labels, hypotheses, prior outcomes, future tasks,
target gold, manifest, and holdout are absent from the payload.

The proposed backend is **local Responses API, Luna-high, no tools**. This is a
named new scaffold proposal, not the historical Codex M treatment and not a
claim that subscription access implies API access. The existing adapter permits
shell execution and the Docker wrapper supplies authentication in that execution
environment. They cannot be silently reused as E3a's authority boundary. This
packet adds no API client, dependency, authentication handling, proxy, or remote
launcher. Acceptance of this scaffold and a minimal implementing adapter is a
maintainer decision before integration.

The fixture policy is deliberately small:

1. Materialize stage 0/5/6 and preflight **its existing** cumulative contract,
   before presenting the new task. Pin dependency locks and pre-restore them;
   keep vulnerability auditing outside the measured edit loop. This controlled
   ecology is distinct from both intended online audit-on and legacy blocked
   audit-on development.
2. Retain the exact response/status/usage before parsing. Accept only one JSON
   `files` object of complete file replacements. Unmentioned files persist; no
   deletions, traversal, other file types, duplicate keys, case collisions, or
   automatic syntax cleanup. The source/response byte and file-count caps are
   in the specification. An invalid submission consumes its round unchanged.
3. Validate project policy before building. Dependencies/framework/build targets
   stay fixed; F# may change simple Compile entries, each source exactly once,
   `Program.fs` last. This allows the stated engine extraction. A forbidden
   change ends the trajectory as a protocol violation, not an apparatus exclusion.
4. Build in a **fresh isolated evaluation workspace** with copied locked restore
   metadata/cache, no old `bin` or configuration intermediates. Use the exact
   fixed `dotnet build --no-restore --no-incremental` command; only a successful
   fresh build's direct DLL may run. Record applied source and binary identities,
   lock identity, exit status, stdout/stderr and timing. A build failure never
   falls back to an older binary. Compile errors are candidate outcomes; timeout,
   invalid patch, API/structure failure, and setup failure are separate categories.
5. Development checks are the existing baseline plus cumulative manifest cases
   through the selected task: **5 / 77 / 79 cases**. Extraction additionally
   checks the declared engine filename and F# compile order. Warnings alone do
   not fail a build. No canonical helper/class/method spelling is required.
6. Stop immediately on development success. Otherwise allow at most two repairs
   within the total budgets. An output-format failure receives only its format
   error. A request with incomplete/ambiguous status is retained and ends the
   batch without retry; a refusal is retained as an output failure. Completed
   submissions with missing/invalid total usage can still be scored, but no next
   request is issued. Optional unreported token subsets stay null.
7. After the trajectory, independently rebuild/score the **first submitted**
   and **terminal submitted** states with holdout only. An invalid terminal
   submission is not credited using the last applied workspace. No applied patch
   is scored when the submission is incomplete. Validity/correctness failures
   count as failures; unavailable scoring from apparatus failure stays unknown.
   Neither holdout scores nor cases can affect continuation, feedback, or sampling.

Sandbox enforcement is **pending**, not established by pure Python validation.
The intended evaluator reuses the pinned existing image/remote compute path,
2 CPUs, 6 GiB RAM, 512 PIDs, no network, non-root, dropped capabilities,
read-only root/cache, bounded writable workspace and `/tmp`, and no credentials,
full repository, target source, or scorer mount. Locks and image/SDK must agree.
The scoring process stays outside candidate execution; only a batch's stdin
cases reach the program during scoring, after interaction has ended. No scoring
results return to the model. Authentication remains local infrastructure-only;
no remote auth cache is needed for a local API call. Any later approved credential
staging must still be ephemeral and cleaned. Existing SSH/proxy policy is unchanged.

The host fixture script runs only fixed repository-owned code and explicit small
faults. It is **not safe for arbitrary candidate code**, does not establish the
remote sandbox, and is not a substitute for that integration gate.

## Development feedback and holdout separation

`e3a-diagnostics-v1` preserves full raw output outside the candidate payload.
Use the pinned SDK's English plain-text diagnostics with fixed `/work` paths.
A compiler error/warning header starts a diagnostic block; continuation lines
stay with it. Sort exact distinct blocks with errors first, then lexical order;
never reorder or shorten lines inside a diagnostic. Development failures use
`ERROR <case-name>: expected <JSON>; received <JSON>` blocks, in the same policy.
The packet records raw/visible UTF-8 bytes, visible hash, block counts, omissions,
and a truncation marker. Its cap is **8,192 UTF-8 bytes**, not a claimed exact
provider token count. All returned feedback also counts toward request input.

If a distinct error block cannot fit intact, retain evidence and stop the batch
as a feedback-cap apparatus failure. Do not silently give F# a shortened error
or dynamically enlarge one language's cap. Many repeated/large F# diagnostics,
multiline type context, warning overflow, and C# errors have deterministic tests.
Review a cap change before execution; no new scientific version is needed for
ordinary pre-freeze fixture corrections.

The [new holdout](holdout-cases.json), authored by this same maintainer session
from the task contracts, plus the fixed 5×5 status-transition
matrix, contains **2 / 39 / 39 cases**. Inputs are disjoint from development;
cases compose boundaries/properties rather than merely rename a feedback case.
Examples include validation precedence under multiple simultaneous faults,
case-sensitive selection among null/case-neighbor orders, four allowed edges
and all other status pairs, repeated transitions in one process, offset boundary
queries, and VIP eligibility/order composition. The fault fixtures reverse
priority or change transition rejection behavior in the actual compiled source;
both language holdouts reject their corresponding faults. They are finite
sensitivity checks, not proof of exhaustive equivalence.

For task 007, report architecture separately using the declared rubric: models
and live dispatch in the engine file; Program only IO/JSON/error adaptation and
engine call; F# compilation order. File existence and passing behavior cannot
prove live architecture. Do not reuse old string checks as that proof or reject
alternative correct internal names. A reviewer blinded to new costs/behavioral
scores must examine first/terminal source under this rubric; unavailable review
is null. It never triggers model repair and is not silently folded into the
primary behavioral endpoint.

## Memory, accounting, schedule, and proposed ceilings

The memory treatment is `provider-response-chain`: request 0 starts a new
response chain; repairs identify the preceding response, retain provider state,
and supply fixed instructions/current source/feedback. No replay/fresh-context
fallback, compaction, transport retry, or different model is permitted. Matching
mock IDs proves plumbing only, not actual retained state or hidden-state
equivalence to a Codex session. The official [conversation-state documentation](https://developers.openai.com/api/docs/guides/conversation-state)
describes response chaining and billing of retained input; live behavior and
account settings remain unverified here.

Use the requested alias `gpt-5.6-luna`, effort `high`; record returned model/version,
backend configuration, response IDs and request IDs (when exposed), SDK/transport
revision and usage. A missing snapshot identifier is null, not an invented pin;
collection requires a reviewed disposition of that reproducibility limit. The
[model documentation](https://developers.openai.com/api/docs/models/gpt-5.6-luna)
lists high effort and, checked 2026-09-05, standard input/output rates of
$0.20/$1.20 per million tokens. Account access, actual backend version, exact
input counting and current prices must be verified before an authorized batch.
No subscription-to-dollar conversion is asserted.

| Ceiling | Proposed value, not authorized consumption |
|---|---|
| Sample | 3 tasks × 4 paired repetitions × 2 languages = 24 trajectories / 12 pairs |
| Order | Seed 20260905; shuffled tasks per repetition, adjacent language pairs; each language first twice per task |
| Repairs / calls | ≤2 repairs; ≤72 model requests, no automatic reissue |
| Per request | ≤32,768 input tokens including retained chain; ≤8,192 output tokens including reasoning; 120 s |
| Per trajectory | ≤600 s from first dispatch through final scoring; refuse work that cannot fit remaining budget |
| Controller operations | Build ≤60 s; development batch ≤10 s; holdout batch ≤10 s; preflight outside trajectory and separately timed |
| Pilot token upper envelope | 2,359,296 input + 589,824 output; subsets not added again |
| Pilot spend | Formula ≤$1.179648 at the checked uncached rates; **hard authorization ceiling proposed: $2**, not an entitlement |
| Separate integration proposal | ≤2 model requests on an unrelated trivial task, same per-request limits, ≤$0.05; no pilot included |
| Authorized now | **0 candidate requests; $0 experiment spend** |

The input ceiling is a **pre-dispatch requirement**, not merely an after-the-fact
usage assertion. The future adapter must demonstrate a conservative bound or
supported exact count over wrappers and the entire retained chain, reserve the
worst-case request cost before dispatch, enforce output/deadline limits, and
stop rather than truncate context or silently fall back. The current fixtures
only check arithmetic and stop on reported overruns; they do not implement a
provider budget guard. A chain that cannot fit ends budget-limited and stays in
the assigned sample. The small output budget may truncate a high-effort response
before code; this is retained failure, not permission to resample. Official
[reasoning documentation](https://developers.openai.com/api/docs/guides/reasoning)
states that the output limit includes reasoning and that incomplete responses
can incur usage without visible output.

For each attempted round preserve status, submission/raw response, source hash,
model request wait, controller operations/time, feedback bytes/hash, input total,
cached-input subset, output total, reasoning-output subset, raw provider usage,
retries (zero), timeouts and completeness. Cache and reasoning are **subsets**,
never extra tokens to add to their totals. Missing/invalid accounting does not
erase correctness or the attempt; aggregate totals are null when any contributing
round lacks that measure, with coverage and any explicitly labelled known sum.
Separate visible payload/source bytes and optional labelled tokenizer estimates
from provider input and unavailable context occupancy. No estimate is reported
as actual provider usage. The packet uses the existing `tiktoken==0.14.0` /
`o200k_base` source and serialized-payload proxy, not an asserted backend tokenizer.
There are no workers/orchestrator candidate agents;
maintainer preparation is outside benchmark cost and not inferred to cost zero.

## Predeclared descriptive report

| Endpoint / resource | Rule |
|---|---|
| **Primary** | First-submission joint compilation and final-holdout behavioral correctness, all assigned attempts |
| Separate outcomes | Format, compilation, development, final holdout, declared architecture, terminal correctness, failure categories and missing scoring |
| Resource phases | Initial request/evaluation; subsequent repair requests/evaluations; final scoring; setup; end-to-end separately (no overlapping sums) |
| Repair burden | Successful first submission has zero incremental repair; failure-conditioned repair is a labelled selected subset |
| Pair summaries | For each task show all four language-paired correctness differences and token/time differences, mean and min/max; report coverage |
| Overall summary | Equal weight to each of the three selected tasks; descriptive correctness/resource summaries, never successful-only filtering |
| Limits | Min/max shows observed variation, not a confidence interval; no population inference or significance claim from three chosen tasks |

Ratios are secondary, undefined at a zero denominator, and reported alongside
correctness and absolute values. No invocation-duration envelope is subtracted,
no mediation percentage is calculated, and no results are pooled with legacy M,
E2 or E2a. All scheduled slots remain visible; a preflight failure records a
setup attempt without a candidate request and may be repaired before proceeding
to that same slot. An ambiguous potentially billable request is never replaced.
Stop the batch on unsafe output/execution, usage uncertainty, an unresolved
repeated apparatus failure, deadline/spend ceilings, or scientific deviation.

## Checks and handoff

```text
python -m unittest discover -s tests -p test_workstream_e3a.py -v
python scripts/e3a_check.py
python scripts/e3a_check.py --build-fixtures --output results/e3a-review-fixtures.json
```

The model-free checks cover submission policy, mock lineage and request count,
feedback truncation, usage missingness/subsets, schedule/budget, disjoint holdout,
payload boundaries, and packet drift. Trusted fixtures build predecessor, target,
and semantic fault for each task/language (**18 builds**) using SDK 10.0.302,
pre-restore/audit-off, a fixed no-restore build and direct-DLL execution. They
seed/remove a stale binary and verify source/lock identities. They explicitly
assert the archived priority defect, not universal reference correctness.

Both existing Linux and Windows CI jobs run these checks plus the existing suite;
generated fixture evidence is uploaded with each exact-commit CI run. The
[CI history](https://github.com/Happypig375/agentic-language-fitness/actions/workflows/ci.yml)
is not itself a claim that this head passed: inspect the check attached to the
exact implementing commit. No local result establishes remote isolation or
live continuation. The delivery records the exact commit and actual CI status.

Self-review findings resolved in these fixtures: preserve multiline diagnostics,
reject case-colliding paths, retain invalid/null usage, allow task-required F#
compile entries, and keep terminal format failure distinct from last applied
source. The archived target defect and scaffold limitations remain explicit.

**Next decision:** independent protocol review and maintainer disposition of
the task/oracle limitation, API/no-tools scaffold, budget, and architecture
rubric. Only after acceptance should the smallest adapter/isolated evaluator be
implemented and checked. A separately authorized two-request integration must
then demonstrate provider continuation/usage, account/model access, budget
enforcement and sandbox boundaries before any pilot authorization/freeze. If
those checks change the scientific policy, review again before collection.
This packet stops here; E3b/F0, H and generic routing remain out of scope.
