# E3a resumed OAuth shakedown — 2026-09-08

## Explicit allowance

Following parser repair `16737af3f67ccaa0f47671c85f07bdbab7062b7a` and its
successful [Linux/Windows CI](https://github.com/Happypig375/agentic-language-fitness/actions/runs/34239221036),
the user answered `continue` to the request for a fresh bounded shakedown, then
said: “increase dispatch count to 5 in the agentic instructions”.

This raises the resumed integration allocation from two to **five dispatches**.
It is not five mandatory calls or a larger pilot. Use the same unrelated
two-step marker exercise and stop as soon as those two steps pass. Record
every debit across invocations; do not reset the allocation or stack unused
older allowances. An unused balance is not permission to reissue an ambiguous
request or bypass another hard stop.

The existing `DispatchGuard` enforces a **per-invocation** ceiling, not persistent
cross-process accounting. This checkpoint schedules one invocation from zero
resumed debits; its two-step loop can consume at most two. Before any later
invocation, the maintainer/agent must calculate cumulative usage and remaining
allowance from retained journals and obtain whatever decision an intervening
stop requires. A fresh output directory/guard does not renew authorization.

| Allocation | Debited at activation | Ceiling / disposition |
|---|---:|---|
| Original integration, attempt 01 | 1 | Failed, retained and still charged; not promoted or refunded |
| Resumed integration | 0 | 5 new dispatches maximum under this user direction |
| Fixed pilot | 0 | 72 maximum, contingent on successful matching shakedown and freeze |

Subscription USD and unreliable provider-request counts remain null. The
32,768 input / 8,192 output thresholds remain post-turn alarms, not provider
hard caps. The separate five-failed-apparatus-attempt rule is not a live budget
and does not override immediate ambiguity, accounting or cleanup stops.

## Bounded implementation and prerequisites

Only the activation fields and the approved/declared integration dispatch
allowance change in the active specification. The runner validates matching
integer allowances before launch, uses that limit in its existing dispatch
guard and records it in the report. It still requires exactly two successful
steps for the pilot prerequisite and has no new retry path. Pilot limits,
candidate authority, model, prompts, byte/time controls, scoring, native client,
image and environment profile are unchanged. The policy hash changes because
it includes the explicitly authorized integration allowance; this is not a
new scientific treatment or permission to pool old attempts.

Fresh independent validation passed **65 tests**: `test_e3a_run.py` 17,
`test_workstream_e3a.py` 19, and `test_e3a_implementation.py` 29. They were run
sequentially with `.venv\Scripts\python.exe -m unittest discover -s tests -p
<test-file> -v`; fresh output is under ignored
`results/e3a-five-dispatch-activation-2026-09-08/`. `scripts/e3a_check.py`
reproduced the packet with zero candidate calls and `git diff --check` passed.
New regressions cover the five-debit cap, rejection of a sixth debit and
invalid/mismatched/non-integer allowances before transport, while the existing
two-step, immediate-stop, pilot and authorization tests remain in force.

A separate AI-session source review initially raised a cumulative-accounting
concern: a new process creates a fresh guard. On reassessment of the explicitly
single-invocation scope and absent retry path, the reviewer classified this as
an operational limitation rather than a within-run defect and approved the
change with the documentation clarification above. No persistent enforcement
claim, registry or retry system was added. This is not human or live validation.

Exact implementing-commit CI must pass before actual use. The
[prior parser validation](workstream-e3a-startup-parser-fix-2026-09-08.md)
is evidence for that earlier source, not a substitute for checking this change.
New activation identities:

- Specification canonical SHA-256:
  `c24e7e8f82bcb52061f255f3cd1c6ec17342b611dafea3f5a51421f4a22c9de7`.
- Policy SHA-256 (excluding only status/activation):
  `4c5d1345662555563e054b6124c44195382e93412be9c1e6d8dda7bf503f493f`.
- Reviewed normalized source-set SHA-256:
  `923fef01fa5b991f91c05bc1afb165554b4b4dd45217dc6a7e1dbf3e9fcd45cf`.

Compared with `16737af`, the specification diff contains exactly four paths:
`status`, `execution_authorized`, `approved_integration_dispatches`, and
`budgets.integration_dispatch_ceiling`. Prior identities remain in their dated
records and are not rewritten. The full implementing Git SHA and its exact CI
will be recorded with the invocation.

The PowerShell read-only remote preflight found the host reachable with about
435,834 MiB available memory, Python 3.13.5, and the unchanged pinned binary,
catalogue and image. The old failed output directory is not overwritten. A new
private run directory `/tmp/alf-e3a-shakedown-xLRAgY` was prepared from
`16737af` using the unchanged tracked
[`prepare-remote.sh`](../reports/workstream-e3a-oauth-shakedown-2026-09-08/prepare-remote.sh),
Python 3.13.5 and isolated dependencies. Preparation passed model-free packet
checks; its [setup record and output](../reports/workstream-e3a-oauth-shakedown-resumed-2026-09-08/)
retain the exact dependency versions and initial commit. Before invocation,
fetch/check out the exact passing activation commit in this new checkout and
verify it is clean; the setup record's earlier SHA is not the execution SHA.

The OpenAI Docs authentication check confirms the existing
[headless cache-copy pattern](https://learn.chatgpt.com/docs/auth).
It keeps staging scoped to the complete local `auth.json` file, not the rest
of `CODEX_HOME`. Use the existing foreground SSH/CONNECT route and remove the
temporary OAuth file/directory in cleanup; do not print, hash or publish auth
bytes. No API key, relay or native-client replacement is introduced.

## Execution record

No resumed dispatch or OAuth staging has occurred at this preparation
checkpoint. Preserve new raw report/journal, source/spec/runtime identities,
invocation output and scoped cleanup evidence when execution occurs.
