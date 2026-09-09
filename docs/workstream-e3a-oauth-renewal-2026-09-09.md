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
