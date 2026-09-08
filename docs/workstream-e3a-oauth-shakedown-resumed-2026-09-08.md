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

## Attempt 02: successful live execution

Commit `5e9eac2ea59188be63191d81240b51f714325180` passed exact
[Linux/Windows CI 34242289358](https://github.com/Happypig375/agentic-language-fitness/actions/runs/34242289358),
then the new remote checkout was verified clean at that SHA. The existing
PowerShell invocation ran once against `/tmp/alf-e3a-shakedown-xLRAgY` using
only a temporary copy of the complete local `C:\Users\hadri\.codex\auth.json`.
The two distinct marker exercises both passed: valid JSON replacements were
applied, freshly built in the pinned sandbox and executed for values 1 then 2.
Both responses completed with the exact admitted startup diagnostics, no
observed tool items, timeout, overflow, accounting alarm or batch stop.

| Step | Input tokens | Output tokens | Reasoning subset of output |
|---|---:|---:|---:|
| 1 | 6,427 | 104 | 62 |
| 2 | 6,651 | 99 | 57 |
| Total | 13,078 | 203 | 119 |

This consumes **2 of 5 resumed integration dispatches**, leaving **3**. The
original failed attempt remains separate and debited; there has been no pilot
dispatch at this checkpoint. Raw provider zero cache/cache-write fields remain
normalized to null; subscription cost and reliable provider-request count are
unknown, not zero. This unrelated shakedown is not F#/C# research evidence.

Immutable evidence in the linked report directory:

- `attempt-02-report.json`, SHA-256
  `0e65abb968770adeae04c4781ee458f8a06bbf91a2ce33b96b42494f2251f07d`.
- `attempt-02-journal.jsonl`, SHA-256
  `00740bbbf83e9230ef9ec12101506282fc85c552c39da9e7658daba9e7ae00b1`.
- `attempt-02-invocation.log`, `attempt-02-cleanup.json` and exact-commit
  `activation-ci.json`.

The new resumed/pilot evidence directories disable Git text conversion in
`.gitattributes`: raw JSON/report/journal hashes must survive a Windows checkout
unchanged. This was caught before publication; original capture bytes and
hashes are preserved rather than normalized or retrospectively rewritten.

Both bounded transport captures report `cleanup_confirmed=true`; the outer
invocation separately verifies deletion of its staged remote auth file and
directory. A subsequent read-only check found no local port-8888 listener,
no remote port-43128 listener, and no `alf-e3a` containers. The original local
OAuth file remains untouched. The report has no invented top-level cleanup
flag; this is scoped cleanup evidence, not proof of global credential absence.
The publication check found no bearer/token-shaped strings in these retained
artifacts; no auth bytes were printed, hashed or copied into reports.

A separate AI-session offline audit checked report/journal hashes, live commit
and CI, source/policy/native/catalogue/image/profile identities, replay,
submission and sandbox outcomes, usage and recorded cleanup. It found no
actionable issue and accepted this as input to the existing freeze gate. That
is artifact review, not a second live invocation, human review or independent
provider/global-secret-absence proof.

## Freeze and pilot transition

The tracked [`freeze.json`](../protocols/workstream-e3a-v1/freeze.json) binds the
successful report above to frozen specification SHA-256
`d33b0f7ed317b4f1792ab22bdf82086bb25a11cebf93781aedd6ebfff5701996`.
Only specification `status` changes from ready to `frozen`; policy SHA
`4c5d1345…` and reviewed controller/source SHA `923fef01…` remain unchanged.
Observed access/usage/sandbox evidence lives in the successful report; the
specification's descriptive pre-run verification flags are not rewritten.

The existing operational `invoke-shakedown.ps1` gains only a validated optional
`-Phase shakedown|pilot` (default `shakedown`), corresponding ready/frozen status
preflight and phase-aware CLI invocation/log label. Authentication, transport,
pins, isolation, cleanup and output-retention behavior are unchanged. Its
historical default invocation remains reproducible from the original commit;
no raw archived report/journal is edited. There is no new execution service.

Fresh independent freeze-transition validation passed **36 tests** (runner 17,
review packet 19), packet reproduction, `git diff --check`, and the existing
`verify_pilot_prerequisite` against the actual retained report and new freeze.
The core source identity still matches `923fef01…`. PowerShell AST syntax and
invalid-phase parameter rejection passed without a valid launcher invocation,
SSH or auth staging. Fresh output is under ignored
`results/e3a-pilot-freeze-2026-09-08/`. A separate AI-session source review
approved the freeze and constrained phase/status mapping; credential and
transport boundaries are unchanged. Phase is normalized once after validated
binding so case-insensitive PowerShell values map to the exact CLI choices.

The pilot's fresh private run root is `/tmp/alf-e3a-shakedown-XsZF3c`; its
legacy preparation-root prefix is not the execution phase. Preparation used
the same script, Python and pinned dependencies, initially at `5e9eac2`.
The [pilot setup record and output](../reports/workstream-e3a-oauth-pilot-2026-09-08/)
are retained. Before use, move only this clean checkout to the exact passing
freeze commit; the previous successful shakedown's output/root are untouched.

After exact freeze-commit CI, run the already
approved fixed 24-trajectory / at-most-72-dispatch pilot through that same
route with `-Phase pilot`, a fresh private run root and new output directory.
No extra integration call is required. Task 007 build/behavior alone is not
architecture completion; missing required rubric review remains unknown and
cannot influence continuation or be represented as a successful refactor.
