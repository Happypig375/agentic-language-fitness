# E3a bounded implementation handoff

2026-09-06. Implements the [second AI-session disposition](workstream-e3a-review-disposition-2026-09-06.md)
of proposal `19b1902be59324b98741ccb6c3a8396de962f5f7`, pulled at `5c10d13`.
Implementation review is **self-review and model-free testing**, not independent
implementation approval, human language-expert review, a freeze, or live permission.

**Historical checkpoint, superseded by the [authorized remote fix and sandbox evidence](workstream-e3a-remote-sandbox-fix-2026-09-06.md).** The user subsequently permitted model-free fixes on the reachable remote host. The two failures and original stop below remain the record of this earlier checkpoint; the later report corrects the archive-availability finding. Neither checkpoint authorizes live calls.

**Status at this checkpoint: implementation present; sandbox validation blocked.** Stop after two
dependency-preparation failures. No further preparation attempt or live call is
authorized by this checkpoint. The documentation-only stop commit skips CI so
that publishing this boundary does not launch a third sandbox attempt.

## Delivered boundary

- `src/alf/workstream_e3a.py`: safe submission application, development-only
  repair control, source-bound post-trajectory completion scoring. R1–R3 are
  applied without changing the selected tasks, sample, engine-file obligation,
  feedback allowance or repair count.
- `src/alf/e3a_api.py`: one injected Responses path, exact-context count request,
  repeated instructions, explicit all-turns reasoning context, Decimal
  pre-dispatch reservations, usage/lineage/model/tier checks and no retries.
  The optional HTTPS helper is killable at its deadline; credentials are supplied
  explicitly over its private stdin, never request evidence or candidate mounts.
  It does not read a key automatically. Default/live-authorization gates remain closed.
- `src/alf/e3a_runner.py`: finite 24-slot controller, append-only/fsynced attempt
  journal, first/terminal scores, usage coverage, all assigned/unstarted slots,
  paired differences and complete-data descriptive means. Ambiguous dispatches
  keep their reservation. Reports do not equate reservations to observed billing.
- `src/alf/e3a_sandbox.py`: Linux Docker evaluation only. Fresh tmpfs work and
  `/tmp`, read-only root/source/restore-seed/cache mounts, no network, UID 1000,
  dropped capabilities, no-new-privileges, 6 GiB memory/no swap, 2 CPUs, 512 PIDs.
  Trusted offline preparation uses the pinned SDK's library pack outside the
  candidate loop. Fixed no-restore builds run a newly hashed DLL only; failed
  builds cannot reuse output. Every exit removes the owned container and its
  descendants. Candidate code never executes directly on the host.

No new proxy, daemon, remote routing implementation, candidate tools, subagents,
backend matrix, protocol family, or historical-result rewrite was added. The
existing foreground SSH transport is unchanged. The API and evaluator are
injectable components, **not an end-to-end verified Windows-to-remote launcher**;
that deployment connection still belongs to the intended-environment integration.

R1 architecture judgements must name the exact submitted source hash, reviewer
ID/type and three required obligations. Missing judgement remains unknown;
known failure dominates it. Scripted fixture labels cannot score live outcomes.
The scorer has no route back into model continuation or feedback. R2 retains
safe invalid projects for repair without executing them. R3 feedback exhaustion
ends only its trajectory, never silently excluding it or cancelling other slots.

Raw provider replies and bounded controller output are retained. Combined
stdout/stderr beyond 1 MiB terminates that operation and is explicitly unavailable.
Compiler/program operations share the trajectory deadline; Docker administrative
and cleanup operations have separate bounded waits (15 seconds per operation),
and cleanup can outlast the candidate deadline. Reports must not hide that wall time.

## Evidence and identities

Scientific specification canonical SHA-256:
`8bc53d30e45dfa72b087225f89c9e5547266f05b47e4306e2b326d951888bc62`.
The regenerated [packet](../protocols/workstream-e3a-v1/review-packet.json) records
LF-normalized implementation/test hashes separately from that specification.
Implementation identity: `9168153f0cc788fe03ddd6596f4c32eaa8b0af93` (the later
stop-checkpoint commit changes documentation only). Its
[exact-code CI run](https://github.com/Happypig375/agentic-language-fitness/actions/runs/33992404283)
is **not green**. Uploaded artifacts, not a generated identity, establish scope.
The Windows job completed successfully; the Linux sandbox-preparation step failed.

Local Windows checks include strict doctor (Python 3.12.2, .NET 10.0.302),
focused mock/controller tests and **27 trusted fixture builds**. The fixtures
preserve the archived F# Int32.MinValue defect, check a widened-integer positive
alternative, explicitly check stage-005/006 inherited priority behavior, and
compile eight architecture regressions. They are not arbitrary-code sandbox
evidence or language-performance observations.

The local full suite passed 343 tests at initial implementation `a558c82`.
Its first Linux CI sandbox attempt (run `33992030653`) stopped during trusted
cache preparation: UID 1000 could not chmod the host-owned mount root. The
follow-up limits permission cleanup to preparer-owned contents (`find -mindepth 1`)
and adds a regression. Candidate UID, capabilities and read-only mounts are
unchanged. The absence probe checks actual research/auth paths rather than
rejecting the approved image's empty `/workspace` directory. These are ordinary
runner fixes; the scientific specification and authorization do not change.

The second Linux attempt at `9168153` passed **344 unit tests and 27 trusted
builds**, then failed on `docker cp <owned-container>:/work/obj <private-seed>`.
The cache-permission correction had passed. The sandbox artifact has
`passed=false`, empty `checks`/`evaluations`, zero model/count calls, and no
reported cleanup failure. **No network, memory, output or other sandbox probe
completed.** The administrative helper retained the failed command but not its
stderr, so the precise export cause is not established. Do not claim a proven
tmpfs or ownership diagnosis from this message alone.

This is the second failure in the dependency-preparation apparatus class.
Stop here under the repository rule; do not retire the scientific specification,
increase a version, add a fallback or silently rerun it. If continuation is
approved, first capture bounded Docker-export diagnostics model-free and choose
one direct trusted seed-export path. Preserve candidate mount/privilege limits.

Reproduction and CI scopes:

```text
python -m unittest discover -s tests -v
python scripts/alf.py doctor --strict
python scripts/e3a_check.py
python scripts/e3a_check.py --build-fixtures --output results/e3a-review-fixtures.json
python scripts/e3a_sandbox_check.py --output results/e3a-sandbox.json
```

Linux CI adds `--ci-sdk-fixture` after pulling the exact SDK base from
`Dockerfile.codex-agent`. It checks effective container settings, network denial,
credential/scorer/socket absence, read-only mounts, writable tmpfs, fresh binary,
failed-build non-execution, output/time bounds and descendant removal. A bounded
128 MiB fixture stress checks cgroup OOM enforcement; it is **not** a 6 GiB
experimental workload measurement. The effective 6 GiB policy is inspected
separately. Fixture image and scope are explicit in its artifact. Do not run
arbitrary candidate code in the ordinary repository image: that image contains gold.

On this host, Docker Desktop's engine is stopped. The intended remote Linux
server is reachable over the existing PowerShell SSH path, but its pinned image
`sha256:5d3e97d195dbbe7e47e47055e46f8c6f15fb9553be0c7ef19ed0060756fc7116`
is absent (no images listed). No compatible local archive was found. No remote
candidate or sandbox execution was claimed, no image was silently substituted,
and no remote credentials were staged or left to clean up.

## Next decision and spending boundary

Current authorization and consumption: **zero candidate model/count calls,
zero experiment spend**. Mock dispatch counters are not external HTTP requests.
Maintainer assistant work is outside the experiment and is not asserted free.

The OpenAI Docs check informed the input reserve: documented Luna input/output
rates and the cache-write premium give conservative generation envelopes of
**$1.2976128 for 72 generations** and **$0.0360448 for two**.
[Official model rates](https://developers.openai.com/api/docs/models/gpt-5.6-luna).
The matched input-count payload includes the retained-response ID and resupplied
instructions. [Official count schema](https://developers.openai.com/api/reference/resources/responses/subresources/input_tokens/methods/count).
Ancillary count-call pricing/account conditions remain unverified: mocks use an
explicit zero-rate fixture, not a claim that the endpoint is free. A live rate
card must bound these charges within the total authorization.

**Immediate next decision:** whether to authorize resuming that bounded,
model-free preparation diagnosis. Sandbox validation must pass before advancing.

After it passes, restore/verify the intended image and evaluate the existing transport connection
without widening candidate mounts or authority. Then obtain separate approval
for **at most two generations / $0.05 on an unrelated trivial task**, verifying
actual account/model access, rates, count/create agreement, response chaining,
effective reasoning context, usage and intended sandbox behavior. Do not call a
model to discover those conditions without approval. The later fixed pilot is
separately proposed at **24 trajectories / 72 generations / $2**; successful
integration is not pilot permission. Stop here pending that decision.
