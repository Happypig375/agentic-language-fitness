# E3a OAuth shakedown activation and stopped attempt — 2026-09-08

## Live attempt 01 — stopped

Activation commit `f8b428f479e2fb2d91079330268584b0b4792821` passed exact
[Linux/Windows CI 34231824002](https://github.com/Happypig375/agentic-language-fitness/actions/runs/34231824002).
At 2026-09-08 21:35–21:36 HKT, `invoke-shakedown.ps1` ran once with that
expected commit, remote root `/tmp/alf-e3a-shakedown-hzwkJH`, the existing local
`C:\Users\hadri\.codex\auth.json` file, and new local output directory
`results/e3a-oauth-shakedown-2026-09-08-attempt-01`. It used the unchanged
canonical foreground SSH/CONNECT route and pinned inputs listed below.

The shakedown **failed and stopped after one debited dispatch**, with
`unexpected-cli-sequence`. There was no second dispatch, automatic reissue,
freeze, pilot, applied candidate source or candidate evaluation. The underlying
CLI returned exit code 0 and a completed response, without timeout or capture
overflow; the controller's rejection remains the recorded failed outcome.

Immutable evidence in the linked report directory:

- `attempt-01-report.json`, SHA-256
  `eb1654fe32ec4fd6d3ac19dab109fdedb5c0ed6c006d1aebc9702ce9facec52c`.
- `attempt-01-journal.jsonl`, SHA-256
  `55788fbab52072d782cbeeb3e52b1a5b12f38420fd604326a592b305ae7c070f`.
- `attempt-01-invocation.log`, `attempt-01-cleanup.json`, and `activation-ci.json`.

The retained event order is:

```text
thread.started
item.completed (error: no_tools/single_response under-development warning)
item.completed (error: code-mode host intentionally disabled)
turn.started
item.completed (one agent_message)
turn.completed (usage)
```

Another AI session's read-only incident audit identified the exact mismatch:
`parse_cli_jsonl` rejects every `item.*` outside the turn before examining item
type/content. The native model-free capture checker extracted events more
permissively and did not test this real startup-warning envelope against the
strict adapter. These diagnostics are not observed tool execution. Do not
enable the code-mode host or tools merely to silence them.

Raw terminal CLI usage is **6,427 input and 79 output tokens**; **37 reasoning
tokens are a subset of the 79**, not additional usage. Raw optional cached and
cache-write fields are zero, not independently verified provider telemetry.
The strict adapter's normalized usage fields remain null in the original
report because it rejected the envelope before usage extraction. This raw-field
audit does not overwrite those fields, refund the dispatch, or invent provider
request counts/subscription dollars; those latter measures remain null.
Offline canonical JSON/submission validation accepted the reply as a file
replacement. It remains unapplied and unscored; syntax acceptance is not a build
or behavioral result and does not turn the failed run into a successful step.

The invocation verified removal of its staged temporary remote auth file and
directory. The bounded transport reported its inner auth/container cleanup
confirmed. A subsequent read-only check found zero local port-8888 listeners,
zero remote `172.30.0.1:43128` listeners, and zero `alf-e3a` containers. The
original local OAuth file was not removed. No global credential-absence claim
is made, and no auth bytes were printed, hashed or published.

Live execution is disabled again: `status=shakedown-stopped-awaiting-review`,
`execution_authorized=false`. Held-spec canonical SHA-256 is
`4d4457251726a2381a6a7e6a949a641c9741b02c7e3bf3160005bd2d93a6ed8b`.
Scientific policy/source hashes remain `95b1b7db…` / `9e56068f…`; only activation
metadata and its generated packet change. The failed attempt retains its actual
activation spec SHA `afb6811e…` and runner commit `f8b428f…` unchanged.
A separate validator passed all 72 affected Python tests again in this held
state, plus packet reproduction and `git diff --check`; `held-*` logs are
retained. These were model-free checks, not another invocation.

**Next decision:** bounded model-free repair should admit only the exact pinned
pre-turn diagnostic shapes/messages, retain them separately, continue rejecting
arbitrary pre-turn errors/tools/items, and keep the strict single-turn envelope.
Use this captured trace as a regression fixture, with separate tests/review and
exact CI; do not rewrite the failed attempt or change scientific limits.
No parser repair or further live call was made after this stop. One of the
original two integration dispatches remains, insufficient for a fresh two-step
shakedown. A new bounded shakedown allowance needs direction; the five-failure
apparatus rule does not override this immediate live stop or request ceiling.

## Preparation history

This is continuation of already approved work, not another design/adoption
request. The [resumed implementation](workstream-e3a-oauth-resumed-verification-2026-09-08.md)
was committed and pushed directly to `main` as
`0a25e7a659f0a4c74bdcb4fdc5c5f7adb3134c1c`. Its exact
[CI run 34229097802](https://github.com/Happypig375/agentic-language-fitness/actions/runs/34229097802)
passed on Linux and Windows. No PR, force push or history rewrite occurred.
The initial Git HTTPS fetch/push failed certificate validation; per-command
`git -c http.sslBackend=schannel` succeeded using the Windows trust store.
Certificate verification remained enabled and no persistent Git setting changed.

## Minimal activation and identities

Only two top-level specification fields change from that implementation:
`status` becomes `shakedown-ready-not-frozen`, and `execution_authorized` becomes
`true`. Pilot still fails without `status=frozen` and a matching successful live
shakedown/freeze record. No model, effort, prompt, task, limit, source, scoring,
environment profile or analysis rule changes. No new scientific version is made.

- Activation specification canonical SHA-256:
  `afb6811ebfb2dd95f27c0331c87a75da74bcf360ac7eb7a8a5590fe6414cb42b`.
- Unchanged policy SHA, excluding only status/activation:
  `95b1b7db184236c0b81982160f1c82394225bbc23a86762925a5c0a84771c13b`.
- Normalized reviewed source-set SHA:
  `9e56068f5eefe8ca96c8d1957f242863815fdf4a6992b8e7251fd454c3c5b0e8`.
  Changes concern activation-independent tests and the explicitly model-free
  sandbox checker below; experimental runner sources/native patches are unchanged.

The schedule test now checks that both activation states produce the same
fixed schedule and budgets. Separate authorization-denial and pilot-freeze
regressions remain. A separate read-only validator passed all four affected
modules: `test_workstream_e3a.py` 19, `test_e3a_run.py` 14,
`test_e3a_codex.py` 10, `test_e3a_implementation.py` 28: **71 tests**.
Packet reproduction and `git diff --check` passed. No native or unrelated
global unit suite was rerun locally. CI runs its ordinary full checks.

Before publication, integration inspection found that the sandbox checker used
the active authorization flag when creating a CI/stress fixture. Its evaluator
correctly forbids substitute images in a live specification. The checker now
uses a deep copy with only `execution_authorized=false`, records both the active
and model-free specification hashes, and never edits the active file. This
applies only to that model-free command. Production fixture rejection remains
unchanged and has a regression test; the test also verifies complete policy
preservation and deep-copy isolation, independent of future activation state.
The changed implementation-test module passed **29/29**, and the packet-dependent
review module passed **19/19** again after regeneration. Together with the
unchanged 14 runner / 10 adapter checks above, the final affected manifest is
**72 passing tests**. Earlier passing logs remain alongside the `-02` reruns.

The first targeted schedule-test run was 18/19 because its packet had not yet
been regenerated. Windows PowerShell's initial UTF-8 output introduced a BOM,
which the JSON loader correctly rejected. Regeneration as UTF-8 without BOM/LF
resolved this; no loader relaxation was made. These were model-free preparation
failures, not experimental dispatches. The packet's own
`execution_authorized=false` remains intentional: generating a review packet
never grants live permission; the CLI reads the active specification and gates.

## Remote preparation and reproduction

Evidence and operational scripts live in
[`reports/workstream-e3a-oauth-shakedown-2026-09-08`](../reports/workstream-e3a-oauth-shakedown-2026-09-08/).
SSH/SCP were invoked from PowerShell with strict host-key checking, batch mode,
and port 830. The existing `/home/user/agentic-language-fitness` checkout was
left untouched. `prepare-remote.sh <exact-commit>` created
`/tmp/alf-e3a-shakedown-hzwkJH`, with a clean detached clone of `0a25e7a…`,
an isolated venv and the exact `tiktoken==0.14.0` dependency.

Host `/usr/bin/python3` is 3.10.12, below the project's >=3.11 requirement.
The existing `/home/user/miniconda3/bin/python` is 3.13.5 and was used only to
create the isolated venv, not to modify the shared Conda environment. The full
resolved Python dependency list and setup output are retained. Python hosts the
controller; candidate execution keeps the same pinned SDK/container. The new
checkout will be fetched and checked out at the exact passing activation commit
before invocation. The unrelated local `uv.lock` is preserved, excluded from
commits, and not copied to this clean checkout.

Native SHA-256 `72cf14453c1879996b970accc7de9aa114bf570e586230799a429d0741bb1959`
and catalogue SHA-256 `c18214b1ba88ab9bd164753115324a7a29c0582e8d071f7b3babf749d892f549`
match at their recorded `/tmp/alf-e3a-native-build-zavnIH` paths.
The exact candidate image is
`sha256:5d3e97d195dbbe7e47e47055e46f8c6f15fb9553be0c7ef19ed0060756fc7116`.
`alf-internal` remains an internal bridge at `172.30.0.1`, network ID
`a21f4952ad3edf2e6551abca91ecef384e81af948aa6f9832d0bbfd1179938bb`.

The initial preparation script unnecessarily inspected the absent
`alf-codex:0.149.1` tag with `|| true`, leaving its image field empty. This is
retained in `setup.stdout.log` / `setup-record.txt`, not called image evidence.
`setup-image-addendum.txt` verifies the actual immutable image ID used by the
runtime. The reproduction script was corrected to inspect that exact ID and
exit on inspection failure; cloning/installing was not repeated. The deployed
checkout's `scripts/e3a_check.py` passed with zero candidate calls.

The unexecuted invocation script also received another-AI operational review.
Pre-staging checks now compare the exact native/catalogue hashes and image ID,
in addition to clean commit, active flags, packet and new-output checks.
A local transcript begins before preflight and survives missing remote run
output; primary failure, credential cleanup and output retention are reported
separately. Earlier script drafts had a parent-directory error, a nonexistent
venv path, an unsupported CLI argument, and fragile PowerShell quoting; these
were corrected before any invocation or credential staging. The final script
uses the existing CLI's actual arguments and reads public specification JSON
for its preflight rather than embedding a remote Python program.
The narrowed separate-AI rereview approved the operational fixes and model-free
fixture isolation with no actionable findings; this was not human or provider
validation. A deliberate negative preflight used the all-zero expected commit
and a public fixture JSON file, not a credential. It exited 1 at the first
commit mismatch, before staging, proxy launch or dispatch; `invocation.log`
retained both the primary reason and the expected absent-output notice.
This is a successful rejection test, not a failed live shakedown attempt.

## Activation boundary (before attempt 01)

At this activation checkpoint no OAuth file has been staged and no live model
dispatch, shakedown or pilot has occurred. Publish the activation revision and
verify its exact Linux/Windows CI before use. The operational invocation merely
composes `infra/remote-runner/run.ps1` with `scripts/e3a_run.py --phase shakedown`;
there is no new proxy, service, retry loop or candidate treatment.

Copy only the complete local `auth.json` file to a private temporary remote
directory, mode 0600, then remove that exact file/directory in `finally` and
verify absence. The existing wrapper independently cleans its per-dispatch
auth copy and container. Never copy the rest of `CODEX_HOME`, hash auth bytes,
or publish credentials. This follows the official
[headless authentication guidance](https://learn.chatgpt.com/docs/auth);
the OpenAI Docs check influenced credential handling, not scientific design.

One invocation permits at most **two dispatches** on the unrelated marker
exercise, with raw journal/report retained. Ambiguity, unverified cleanup,
context rejection or an accounting alarm stops without reissue. Usage alarms
remain 32,768 input / 8,192 output after a turn, not hard provider caps.
Subscription cost and unreliable provider-request counts remain null.
Only a successful matching shakedown permits a tracked freeze and the already
approved 24 trajectories / 12 pairs / at most 72-dispatch pilot.
