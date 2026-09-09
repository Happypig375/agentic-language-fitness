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
