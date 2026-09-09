# E3a renewed live allocation — 2026-09-09

## Authority and accounting

The maintainer was asked to approve a fresh two-dispatch shakedown and, if
successful, a fresh fixed 24-trajectory/72-dispatch pilot, preserving previous
attempts and charges. The reply was **"continue and increase that limit to 5"**.
This record interprets that answer as five newly authorized integration
dispatches and the proposed contingent fresh pilot, not an increase in candidate
repairs, a reset of historical accounting, or permission for unlimited batches.

The new allowances begin at 0/5 integration dispatches and 0/72 pilot dispatches.
The shakedown remains the existing two-step unrelated marker task; five is a
ceiling across this allocation, not a requirement to issue five calls. Reconcile
all retained debit events before another invocation because the existing guard
is per invocation, not a persistent authorization ledger. No new registry is
introduced. Unused earlier balances are superseded, not added to these limits.

Prior usage stays charged: original failed shakedown 01 used one dispatch;
resumed shakedowns 02 and 03 used two each; pilot 01 used zero and pilot 02 used
one. Thus six historical dispatches precede this renewal: five integration and
one pilot. The old remaining integration one and pilot 71 cannot be stacked
with the fresh allowance. Reports, null scores and failure classifications remain
unchanged; do not resume, selectively replace, retrospectively score or pool the
stopped pilot with the fresh batch. This explicitly approved fresh batch is not
a comparative-effect-driven sample extension; no paired language result exists.

## Implementation and execution sequence

The minimal complete-response parser repair is commit
`bc0006261ea20e0e47ba333ff6c793147dcfe1a0`, with 81 affected tests and another-AI
source review passed. Exact [CI 34254599635](https://github.com/Happypig375/agentic-language-fitness/actions/runs/34254599635)
passed on Linux (5m57s) and Windows (8m51s). The new activation changes only
the active specification status from `frozen` to `shakedown-ready-not-frozen`
and regenerates its packet. Existing numeric ceilings already equal 5 and 72;
scientific policy and candidate controls remain unchanged. The older freeze is
retained as history and cannot validate the repaired source.

Publish activation directly without a PR, verify its exact CI, prepare a fresh
private remote checkout, and invoke the existing wrapper once for the two-step
shakedown. Only matching success permits a new freeze and the contingent fresh
pilot. Preserve the old freeze's exact bytes in the renewal evidence before
updating the active pointer. Publish and verify the freeze commit before pilot
execution. Retain every invocation, raw report/journal, known usage and scoped
cleanup check; fix confirmed ordinary bugs without a scientific version bump.

Use only the complete local `C:\Users\hadri\.codex\auth.json` file through
the existing canonical foreground SSH reverse-forward route, launched from
PowerShell. Stage the file in a private temporary remote memory-backed directory,
never print/hash/publish its bytes, and verify owned credential cleanup after
each invocation. The original local cache stays untouched. This preserves the
documented [OpenAI authentication pattern](https://learn.chatgpt.com/docs/auth)
without introducing an API key, alternate backend, relay or new native client.

Keep the fixed tasks/model/effort, two repairs/three submissions, byte/time
controls, sandbox, null subscription USD and missing-usage rules. The five-failure
apparatus rule does not override immediate safety, unknown-usage, overshoot,
cleanup, accounting or other explicit hard stops. A later failed live batch is
not automatically authorized for another fresh replacement.

At this documentation checkpoint, no new OAuth staging or live dispatch has
occurred. Live results and exact source/environment identities must be recorded
from the actual execution, not inferred from these approvals or model-free tests.

## Activation checks

Fresh separate validation passed 37 selected tests: `test_e3a_run.py` (18) and
`test_workstream_e3a.py` (19), sequentially with
`.venv\Scripts\python.exe -m unittest discover -s tests -p <filename> -v`.
`scripts/e3a_check.py` matched the packet with zero new model calls;
`git diff --check` passed. Another AI session approved the activation diff.
The packet's `execution_authorized:false` is intentionally model-free metadata,
separate from the hashed active specification. No generator change is needed.
Fresh logs are in ignored `results/e3a-oauth-renewal-2026-09-09/activation-validation/`;
two preliminary identity-helper assertions queried nonexistent budget keys,
were retained, and the corrected helper passed without a product change.

Activation specification SHA-256:
`c24e7e8f82bcb52061f255f3cd1c6ec17342b611dafea3f5a51421f4a22c9de7`.
Scientific policy SHA-256:
`4c5d1345662555563e054b6124c44195382e93412be9c1e6d8dda7bf503f493f`.
Repaired runner source-set SHA-256:
`8b549b678337ade391ef7b95a3c484413589c6031f3e50998ebe88856ff12164`.
The remote native/catalogue/image identities still match their pins; the local
proxy port is free and no selected E3a container was running. These are preflight
observations, not live completion evidence. Exact activation-commit CI remains
required before staging credentials or invoking the shakedown.

## Renewed shakedown 01 — successful

Activation commit `a724694d66ff6566c76b207dd08496369b2067dc` passed exact
[CI 34293286434](https://github.com/Happypig375/agentic-language-fitness/actions/runs/34293286434)
(Linux 6m10s; Windows 8m1s). The existing `prepare-remote.sh` created a clean
private checkout/venv at `/tmp/alf-e3a-shakedown-xvOD44`; retained setup captures
include the resolved Python/dependency, image and Docker-network identities.

The actual local PowerShell invocation was:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File reports/workstream-e3a-oauth-shakedown-2026-09-08/invoke-shakedown.ps1 `
  -Phase shakedown `
  -ExpectedCommit a724694d66ff6566c76b207dd08496369b2067dc `
  -RemoteRunRoot /tmp/alf-e3a-shakedown-xvOD44 `
  -LocalAuthFile C:\Users\hadri\.codex\auth.json `
  -LocalOutputDirectory results/e3a-oauth-renewal-2026-09-09/shakedown-01
```

It exited 0 after two completed, applied, freshly built and sandbox-tested
marker replies (values 1 then 2), with `passed=true` and null batch stop. Both
native turns had known usage and no tool item, timeout, overflow or accounting
alarm. The second step used visible replay. Total usage was **13,078 input /
188 output tokens**; 5,632 cached input and 104 reasoning output tokens are
subsets, not additional tokens. Cache-write counts, provider-request count and
subscription USD remain null. These are unrelated integration exercises, not
language-comparison observations.

The fresh integration allocation is now **2/5 used, 3 remaining**. All six prior
dispatches remain separately charged. No pilot dispatch used this fresh allocation.
Another AI session audited the actual report, raw journal/replay, identities and
cleanup evidence and accepted the unchanged freeze gate; this is not human review
or a global no-tools guarantee.

Raw evidence is preserved under
[`reports/workstream-e3a-oauth-renewal-2026-09-09/`](../reports/workstream-e3a-oauth-renewal-2026-09-09/):

- `shakedown-01-report.json`, SHA-256
  `516cb4a0e6492a6c7d261923a1ff2511ad6825242e8102bc5c5224928bef4439`.
- `shakedown-01-journal.jsonl` (byte-identical to raw `attempts.jsonl`), SHA-256
  `418f2d11f6b0604c40512490f63cba6e9354ecbe8a5081421d9c402248579384`.
- Invocation, setup, exact-CI and cleanup records. The prior freeze's exact saved
  bytes are `prior-freeze.json`, SHA-256
  `a19ddc0b4c102fdc4d86dcfc3ef0362573734fef281bf04104cd51a6e98bd395`.

The wrapper verified temporary staged-auth deletion and copied its output.
Successful scoped checks at 00:13:37–00:13:41 UTC (08:13 HKT) found no selected
proxy listener or running E3a container; the original local auth file remained.
The publication token-pattern scan found zero matching files. These checks are
scoped evidence, not proof about all credentials on either host.

The tracked freeze now points to this report for the unchanged scientific policy
and repaired source identity. Frozen specification SHA-256 is
`d33b0f7ed317b4f1792ab22bdf82086bb25a11cebf93781aedd6ebfff5701996`.
Fresh freeze validation passed the same 37 selected tests, packet and diff checks,
plus the real offline `verify_pilot_prerequisite` against the published report.
The source/policy and raw report hashes match. Another AI session approved the
freeze/evidence diff; fresh logs are retained in the `freeze-validation` result
subdirectory. Publish this freeze and verify its exact CI, then execute the already
approved fresh fixed 24-trajectory/72-dispatch pilot once. No automatic later
replacement, additional shakedown or old-slot resumption is authorized.

## Renewed pilot 01 — fixed collection finished

Freeze commit `91b43b8161347d35be03ba7fb71bb1b7d73ccf19` passed exact
[CI 34294549110](https://github.com/Happypig375/agentic-language-fitness/actions/runs/34294549110)
(Linux 5m37s; Windows 8m24s). The existing setup script prepared a separate clean
checkout at `/tmp/alf-e3a-shakedown-jnEI0G` with the same resolved dependencies,
native client, catalogue, image and network. The directory prefix is the existing
launcher's legacy name; this invocation used `-Phase pilot`.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File reports/workstream-e3a-oauth-shakedown-2026-09-08/invoke-shakedown.ps1 `
  -Phase pilot `
  -ExpectedCommit 91b43b8161347d35be03ba7fb71bb1b7d73ccf19 `
  -RemoteRunRoot /tmp/alf-e3a-shakedown-jnEI0G `
  -LocalAuthFile C:\Users\hadri\.codex\auth.json `
  -LocalOutputDirectory results/e3a-oauth-renewal-2026-09-09/pilot-01
```

The wrapper exited 0. All **24 unique scheduled trajectories finished** (three
tasks, two languages, four paired repetitions), with **32 dispatches** and a
null batch stop. Every trajectory eventually passed development checks. This
does not imply first-submission or architectural success. An independent AI
artifact audit reconciled 32 sequential pre-launch debits, 32 complete native
captures, 24 preflights/slot finishes and 48 first/terminal score events. No
tool item, timeout, overflow, invalid/missing total usage, accounting alarm or
automatic relaunch was found. This is bounded retained evidence, not proof of
all provider-side request activity.

Aggregate observed usage is **302,266 input / 62,915 output tokens**; 21,028
reasoning tokens are an output subset. Cached input is known on 10 rounds
(43,520 observed subset tokens), but the aggregate cached and cache-write totals
remain null because coverage is incomplete. Do not turn missing optional counts
into zero or add subsets twice. Maximum observed turn totals were 15,786 input
and 4,174 output, below the adopted post-turn alarms. Subscription USD and
reliable provider-request counts remain null.

The immutable raw endpoint counts, before architecture review, are first
completion **10 true / 7 false / 7 unknown**, and terminal completion **16 true /
8 unknown**. Task 007 requires the separate source-bound architecture rubric;
neither operational success nor build-plus-behavior fills that missing judgement.
A later blinded review is an explicitly identified addendum, not a rewrite of
these raw scores or a reason to issue another candidate request.

The evidence directory now also retains:

- `pilot-01-report.json`, SHA-256
  `d05da3205fa26c9fc41156182802435c6ab0400d149ddcaf8ed9a6375f02571a`.
- `pilot-01-journal.jsonl` (raw `attempts.jsonl` bytes), SHA-256
  `a14b9c0e112d2715a687b9cc61d303cb76c17eeade24a7c027878d577e642e94`.
- `pilot-01-invocation.log`, `pilot-01-cleanup.json`, setup captures and
  `freeze-ci.json`. The publication token-pattern scan found zero matching files.

The wrapper verified staged-auth deletion and retained-output copying. Successful
scoped checks at 01:01:49–01:01:54 UTC (09:01 HKT) found zero selected listeners
and running E3a containers; the original local auth file remained untouched.
The fresh allowances now stand at **2/5 integration and 32/72 pilot used**.
Together with six separately retained earlier dispatches, the recorded lineage
contains 40 dispatches. Unused 3/40 balances authorize neither a larger sample nor
another batch. No further live candidate calls are needed for this pilot.

## Post-run architecture addendum and reproducible analysis

The [descriptive analysis](../reports/workstream-e3a-oauth-renewal-2026-09-09/analysis.md)
and its [machine-readable companion](../reports/workstream-e3a-oauth-renewal-2026-09-09/analysis.json)
are derived artifacts, not replacements for the immutable raw report or journal.
The small `analyze-pilot.py` consumer reuses the frozen `score_submission` and
`summarize` functions. It neither executes candidate source nor sends model
requests. It rejects a specification that does not match the report's identity,
keeps exact-file and canonical-JSON hashes distinct, and never uses an earlier
applied source to salvage an invalid endpoint.

A fresh **AI session**, `/root/review_task007_architecture`, reviewed seven
distinct source snapshots at 01:08:55 UTC. Its input contained only language,
source and source hash, plus the adopted rubric. Slot/repetition/endpoint mapping,
behavioral results and resource measurements were withheld; source language was
not blinded. The separate [review packets](../reports/workstream-e3a-oauth-renewal-2026-09-09/review-packets.json),
[judgements](../reports/workstream-e3a-oauth-renewal-2026-09-09/architecture-reviews.json)
and [endpoint mapping](../reports/workstream-e3a-oauth-renewal-2026-09-09/endpoint-to-source-hash.json)
preserve that boundary and the file/function evidence. All three architectural
obligations were judged satisfied for each supplied snapshot. The F# project
compile order is checked separately by the existing structural rule.

Review applies only to matching first/terminal source hashes. The invalid first
Task 007 submission has no applied source and receives no inferred architecture
credit. Repeated identical snapshots share a judgement, not an extra independent
observation. This is source-only AI assessment, not human-expert review or a
behavioral proof. Review findings were never returned to candidates and caused
no repairs, reissues or sample extension. Maintainer review/analysis consumption
is outside the candidate dispatch/token totals; its cost is not assumed zero.

Reproduce the addendum from this publication revision, preserving its pinned
specification and source files:

```powershell
python reports/workstream-e3a-oauth-renewal-2026-09-09/analyze-pilot.py `
  --report reports/workstream-e3a-oauth-renewal-2026-09-09/pilot-01-report.json `
  --spec protocols/workstream-e3a-v1/specification.json `
  --reviews reports/workstream-e3a-oauth-renewal-2026-09-09/architecture-reviews.json `
  --output-dir results/e3a-oauth-renewal-reproduction
```

The output directory is deliberately separate from published evidence. Generated
files use deterministic LF line endings. Omitting `--reviews` produces the
source-only review packets and the original missing-review analysis; this is
the packet-preparation mode used before the blinded review. Supplying the saved
judgements reproduces their application, not an independent repeat of the AI's
subjective judgement. The implementing pilot commit remains `91b43b8`; neither
the scientific specification nor runner source-set identity changed for this
post-run reporting work.

### Descriptive findings

The addendum yields **17/24 first-submission completions and 24/24 terminal
completions**. All 24 assigned slots remain in the denominator. Original raw
Task 007 nulls remain visible alongside the reviewed scores.

| Measure | F# | C# |
|---|---:|---:|
| First task completion | 6/12 | 11/12 |
| Terminal task completion, with AI architecture addendum | 12/12 | 12/12 |
| Initial / repair dispatches | 12 / 7 | 12 / 1 |
| Initial input / output tokens | 101,388 / 28,297 | 101,448 / 19,780 |
| Repair input / output tokens | 87,466 / 12,888 | 11,964 / 1,950 |
| Total input / output tokens | 188,854 / 41,185 | 113,412 / 21,730 |

Five first submissions failed strict patch format (four F#, one C#); they were
not applied or compiled, and their holdout results stay unknown. The other two
failed first submissions were F# behavioral failures despite successful builds.
One F# trajectory then had a build failure on its first repair and succeeded on
its second. No response text or candidate source was manually corrected.

The report gives all four paired differences per task, coverage, means and
ranges. Differences are **F# minus C#**, ordered by repetition. Equal-task mean
differences are -0.4167 first-completion proportion, +6,286.83 total input tokens,
+1,621.25 total output tokens and +34.82 seconds per trajectory including scoring.
Initial input differs by only -5 tokens on that mean; incremental repair input
differs by +6,291.83. Those observed components reconcile arithmetically, but do
not identify a causal contribution from any specific language feature or tool.
No overlapping phase durations are summed or unrecorded timings imputed.

This diagnostic result favors C# first completion and lower observed resources
for these tasks, this provisional Luna-high setting and this strict no-tools,
visible-replay treatment. Three selected tasks and four repetitions do not
support a universal language ranking, population-significance claim, scale
crossover, or precision-based sample extension. Successful repair is not an
estimate of the causal benefit of feedback. No earlier stopped pilot is pooled.

### Analysis validation and next decision

The final affected-test manifest is only `tests/test_e3a_renewal_analysis.py`:
**11 tests passed** in a separate validator's actual terminal log. Packet checks
still match with zero candidate model calls; `git diff --check` passes. Another
AI session approved the final analysis source after fixes for report/spec binding,
raw-versus-derived rendering, exhaustive outcome counts and per-trajectory
initial/repair partitioning. Regression tests also cover source-hash review
binding, duplicate-key rejection, invalid-terminal non-salvage, missing rubric
evidence, exact raw-file hashing and deterministic output line endings.

Three earlier focused test invocations failed on synthetic fixture/schema and
deduplication assertions; their ignored diagnostic directories (`analysis-validation`,
`analysis-validation-retry-01`, `analysis-validation-final-01`) are retained.
Several ad hoc validator inspection helpers also failed or produced inaccurate
prose about test counts, phase counts or optional `derived_scores` fields. Those
summaries are not analysis evidence. The final test log in
`analysis-validation-final-02/01-test.txt` and the maintainer's successful
`final-artifact-check.py` assertions establish 24 initial plus eight repair
dispatches, the asymmetric language split, all effective endpoint counts, seven
source-bound reviews, 16 architecture endpoint mappings (15 applied, one null),
unchanged blinded packets, and unchanged raw files/scores. These are model-free
reporting corrections, not a runner or scientific-treatment revision.

Publish this evidence and analysis directly without a PR, then verify the exact
publication commit's Linux/Windows CI. That completes the authorized E3a pilot
assignment. Unused integration/pilot balances still do not authorize new samples.

The next step is the plan's **workstream-selection decision**, not another E3a
run or apparatus rewrite. The recommendation is **H0 model-free preparation**:
one paired exemplar, an explicitly labelled exact/proxy serialization audit and
synthetic source-budget/eviction checks. This addresses the original source and
context question without requiring optional F/G studies. H0 has not been selected
or started by this report; its exemplar/accounting choices need a bounded next
assignment, and any H1/H2 model-backed pilot remains separately gated. Retain
the other conditional branches in `PLAN.md` rather than launching all of them.
