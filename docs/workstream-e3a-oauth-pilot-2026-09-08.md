# E3a OAuth pilot: pre-dispatch attempt 01 — 2026-09-08

**Later checkpoint (2026-09-09):** pilot attempt 02 reached a model dispatch,
then stopped on complete multi-message assistant output. Its retained evidence,
ordinary parser repair and live-continuation boundary are in the
[complete-response record](workstream-e3a-complete-response-fix-2026-09-09.md).
The preparation and successful shakedown history below does not authorize
another live invocation after that stop.

## Retained attempt

The already approved fixed pilot was invoked once after exact freeze-commit
[Linux/Windows CI 34245181125](https://github.com/Happypig375/agentic-language-fitness/actions/runs/34245181125)
passed on `7575343466741caa8b51c9770959bf9cbc4f7773`. It used the canonical
PowerShell launcher with `-Phase pilot`, the clean remote checkout at
`/tmp/alf-e3a-shakedown-XsZF3c`, and an ephemeral copy of the complete original
local OAuth `auth.json` file. The transcript records 23:39:58–23:40:11 HKT.

The runner stopped with `batch_stop=ValueError` before any model dispatch:
**24 assigned slots, zero started slots, zero attempted rounds and zero
dispatches**. The journal contains only `batch-assigned`, `batch-interrupted`
and `batch-finished`. No candidate response or score exists. All 24 slots
remain unstarted in the immutable report; they are not completed observations.
Unknown usage and subscription charges remain null, not invented zeroes.

The original failed integration attempt and successful resumed shakedown are
unchanged. The resumed integration allocation remains **2 of 5 used, 3
remaining**; this pre-dispatch pilot attempt used none of the separate
72-dispatch pilot allowance. Do not silently reissue a live request, change
the frozen treatment, overwrite this attempt or relabel it as success.

Evidence under
[`reports/workstream-e3a-oauth-pilot-2026-09-08/`](../reports/workstream-e3a-oauth-pilot-2026-09-08/):

- `attempt-01-report.json`, SHA-256
  `0759588f35da2c07d007ea1a172ba62a2d5219d55739fac4eb53ec46ff3935a9`.
- `attempt-01-journal.jsonl`, SHA-256
  `d3cb8c4099f96a275db11d9cce5782e8430ea78a4c936be693e37aa543709db3`.
- `attempt-01-invocation.log`, `attempt-01-cleanup.json`, `freeze-ci.json`
  and the earlier setup record/output.

The report records frozen specification SHA-256
`d33b0f7ed317b4f1792ab22bdf82086bb25a11cebf93781aedd6ebfff5701996`
and reviewed core source SHA-256
`923fef01fa5b991f91c05bc1afb165554b4b4dd45217dc6a7e1dbf3e9fcd45cf`.
Native binary, catalogue, image and environment identities match the successful
[shakedown and freeze record](workstream-e3a-oauth-shakedown-resumed-2026-09-08.md).

## Cleanup

The wrapper verified deletion of its owned temporary OAuth file/directory and
copied the failed output before exiting with status 1. Independent successful
read-only checks found no local port-8888 listener, no remote port-43128
listener and no running `alf-e3a` containers; the original local auth file
still exists. An earlier Docker check had a quoting error and is explicitly
not counted as successful evidence. No auth contents were printed or hashed.
These are scoped checks, not proof of global credential absence.

## Model-free diagnosis and repair boundary

Another AI session reproduced the exception locally without credentials,
Docker or a model request. The CLI loaded `benchmarks/successor/manifest.json`
as a plain dictionary using `read_json`. This discarded the existing
`Manifest.manifest_parent` metadata. During construction of all initial
candidate payloads, `artifact_plan` therefore assumed `benchmarks/pilot` was
the artifact root and correctly rejected the actual successor gold path:

```text
ValueError: gold source escapes its root
source: benchmarks/successor/gold/fsharp/001-priority/Program.fs
root:   benchmarks/pilot
```

The small repair is to use the existing `alf.config.load_manifest(ROOT,
spec["manifest"])` loader in the CLI. Path-containment validation, candidate
visibility, the scheduled slots, prompts and all scientific/security controls
remain unchanged. Add a regression through the real CLI loading path and
construct the selected task/language payloads model-free. This is an apparatus
bug, not a failed candidate or a reason for a new scientific version.

The loader repair changes the reviewed source identity, so the earlier
successful shakedown cannot be claimed as an exact-source integration test
of the repair. Preserve its report and freeze history, temporarily return
only the activation status to shakedown-ready, and reproduce the generated
packet. After affected model-free checks, review and exact-commit CI, a fresh
two-step unrelated shakedown fits within the **three remaining** resumed
integration dispatches. It must retain its own debits and cleanup evidence.
Only a successful matching report can replace the active freeze binding.
No pilot request has been issued or ambiguously reissued; no observation is
being replaced or pooled across runner revisions.

## Repair validation and reproduction

The CLI fix is one loader substitution and import. The regression drives
`e3a_run.main()` through its actual manifest-loading path while replacing
transport/dispatch with a test double, then materializes every successor
task/language payload (eight tasks, two languages). It would reproduce the
original path error with the plain-dictionary loader. It does not execute
candidate code or call a provider.

Fresh independent validation passed **66 tests**: `test_e3a_run.py` 18,
`test_workstream_e3a.py` 19 and `test_e3a_implementation.py` 29, each selected
sequentially with `.venv\Scripts\python.exe -m unittest discover -s tests -p
<filename> -v`. `scripts/e3a_check.py` matched the packet with zero candidate
calls and `git diff --check` passed. Logs are retained under ignored
`results/e3a-manifest-loader-fix-2026-09-08/`. An initial diagnostic assertion
incorrectly expected the shorthand status `ready`; its corrected exact-status
assertion passed. Both logs are retained; that assertion failure was not a
product test failure or a model attempt.

The repair's identities are:

- Ready specification: `c24e7e8f82bcb52061f255f3cd1c6ec17342b611dafea3f5a51421f4a22c9de7`.
- Unchanged scientific/authorization policy: `4c5d1345662555563e054b6124c44195382e93412be9c1e6d8dda7bf503f493f`.
- Reviewed normalized source set: `71e7510d33f77031116288da7d4ca853790983e178b3d2c6bf00276c64794108`.

Another AI session approved the loader/authority diff, actual failure evidence,
regression and activation/source-binding transition. This is source/artifact
review, not independent live verification or human review. Publication scanning
found no token-shaped fields/strings in the new pilot artifacts; raw report
and journal bytes remain unchanged, with Git text conversion disabled.

The recorded model-free helper
[`check-predecessors.py`](../reports/workstream-e3a-oauth-pilot-2026-09-08/check-predecessors.py)
checks the six selected task/language initial payloads against the replay-byte
cap and runs each approved predecessor against its existing development
contract in the exact-image evaluator. Its task IDs resolve to manifest stages
0, 5 and 6, not positions 0, 1 and 2 within the selected subset; an initial
helper draft's index mistake was caught and corrected before any Docker use.
It emits preparation/evaluation evidence and always calls the evaluator's
owned cleanup. It creates no auth, transport or model session and reads no
holdout. These checks supplement, not replace, the live unrelated shakedown.

Run it with the isolated remote environment's Python and an absolute clean
checkout path:

```text
<venv>/bin/python <repo>/reports/workstream-e3a-oauth-pilot-2026-09-08/check-predecessors.py <repo>
```

The fresh private remote preparation root is `/tmp/alf-e3a-shakedown-1Vk2qm`,
initially checked out at `7575343` by the unchanged preparation script. Before
verification/live use, advance only this new checkout to the exact repair
commit and verify its clean tree. Old attempt roots and outputs are retained.
Exact repair-commit CI and actual six-predecessor verification remain required
before the next live invocation; source tests alone do not establish them.

## Exact-source remote predecessor verification

The repair was pushed directly, without a PR, as
`5a88afab5dff1595e274e4c770cfe9e40f96200e`. The fresh remote checkout was
advanced to that exact commit and independently checked clean. On 2026-09-09
HKT, the recorded helper passed all six predecessor build/development checks
on the original pinned image, using manifest stages 0, 5 and 6:

| Selected task | C# replay bytes | F# replay bytes | Predecessor build/development |
|---|---:|---:|---|
| 001 | 6,204 | 5,917 | Both pass |
| 006 | 13,301 | 13,210 | Both pass |
| 007 | 16,299 | 15,928 | Both pass |

All payloads are below the fixed 131,072-byte allowance. These are encoded
visible replay sizes, not full provider-context token counts or measured
candidate outcomes. Dependency preparation and evaluator cleanup completed;
a subsequent successful `docker ps -q --filter name=alf-e3a` query was empty.
No model, auth or holdout interaction occurred.

The first invocation piped a PowerShell here-string to `bash -s`; its BOM and
CRLF framing broke the header and appended a carriage return to the final
repository argument. It stopped before any sandbox evaluation. The retained
`remote-predecessor-preflight.log` records that invocation error. The corrected
invocation passed the Python command/root as ordinary SSH arguments (still
launched only from PowerShell), with no code or scientific change. Its
`remote-predecessor-preflight-attempt-02.log` retains all successful operations
and the final exact-commit/specification report. Both are PowerShell-captured
logs, not claimed byte-for-byte remote stdout files, and neither was overwritten.

Exact repair-commit CI
[34248390590](https://github.com/Happypig375/agentic-language-fitness/actions/runs/34248390590)
must finish successfully before the next OAuth staging/live dispatch.

The first CI attempt passed all Linux and Windows test/validation steps, but
the Windows artifact upload failed during `FinalizeArtifact` with an HTTP 403
from an intermediary, after blob upload. This is retained in
`loader-fix-ci-attempt-01.json` and `.log`. The failed Windows job was rerun
under the same run and exact source commit using `gh run rerun 34248390590
--failed`; Linux was not rerun. No test, workflow, scientific or security
setting was changed, and no live call was made while this CI gate was failed.

The second CI attempt succeeded: Windows in 7m43s, with the successful Linux
5m15s result retained. `loader-fix-ci-attempt-02.json` records the exact commit
and completed successful gate before OAuth staging. The first failed CI
attempt remains retained, not relabeled as a successful run.

## Repaired-source shakedown, attempt 03 (2026-09-09 HKT)

The same canonical wrapper then ran once on clean `5a88afa` using only the
temporary complete local OAuth file and the existing SSH/CONNECT route. Both
unrelated marker replacements were applied, freshly built and executed
successfully. The report has `passed=true`, no batch stop and exactly two
dispatches. Usage was 6,427 input / 98 output for step 1 and 6,651 input / 76
output for step 2: **13,078 input / 174 output**, with 90 reasoning tokens
already included in output. Cache/cache-write fields, subscription cost and
reliable provider-request counts remain null under the existing policy.

This brings the resumed integration allocation to **four of five dispatches
used, one remaining**. The original failed integration dispatch remains
separately charged. The zero-dispatch pilot still consumes no pilot allowance.
The two successful unrelated shakedowns are apparatus checks, not F#/C# results.

New immutable evidence lives alongside the earlier resumed shakedown:

- `attempt-03-report.json`, SHA-256
  `8a3fa5dca1c3ab1809389db325a86356d10ad538d91b7cb0fc2744df15e414aa`.
- `attempt-03-journal.jsonl`, SHA-256
  `cbb05e2a0b52f8bf75a89e8b9b9e035096fb5a6b36282043398b3d49a419b9a3`.
- `attempt-03-invocation.log` and `attempt-03-cleanup.json`.

Both responses confirmed cleanup; the wrapper separately verified removal of
its staged auth file/directory and copied output. Fresh successful checks at
16:21:54–16:21:56 UTC (00:21:54–00:21:56 HKT on September 9) found no selected
proxy listeners or running E3a containers. The original local auth file is
untouched. A publication scan found no token-shaped fields/strings. As before,
these are scoped cleanup checks, not proof of global credential absence.

## Renewed freeze and pilot handoff

Another AI session audited the actual attempt-03 report/journal hashes, CI,
runtime identities, ordered debit/response/step lifecycle, visible replay,
startup diagnostics, applied replacements, fresh sandbox evaluations, usage
and cleanup evidence. It found no actionable issue and accepted this report
for the existing freeze gate. This is offline artifact review, not independent
live-provider or human review.

The active `freeze.json` now points to attempt 03 and its raw report hash.
Only specification status returns to `frozen`: specification SHA-256 is again
`d33b0f7ed317b4f1792ab22bdf82086bb25a11cebf93781aedd6ebfff5701996`, policy
remains `4c5d1345…` and repaired source remains `71e7510d…`. Historical freeze
bindings and reports are preserved in Git and their dated records. No prompt,
model, scoring, budget, account, sandbox or scientific version changes.

The next pilot root is `/tmp/alf-e3a-shakedown-uJ169U`, freshly prepared from
`5a88afa` with the same script, Python, dependencies and pinned inputs, without
auth staging. Advance only this new checkout to the exact passing freeze
commit before use. The previous failed pilot and both shakedown outputs are
not overwritten. After renewed freeze validation and exact-commit CI, invoke
the existing wrapper once with `-Phase pilot`, that fresh root and a new
output directory. The fixed 24 slots / 72 dispatches and all immediate stops
remain unchanged. Task 007 missing rubric judgement remains unknown.

Fresh independent renewed-freeze validation passed **37 tests** (runner 18,
review packet 19), packet reproduction, `git diff --check` and the existing
`verify_pilot_prerequisite` against the actual attempt-03 report/runtime.
Exact frozen specification, unchanged policy and repaired source identities
matched; every command exited 0. Logs are under ignored
`results/e3a-renewed-freeze-2026-09-09/`. No model, auth, network or Docker
operation was part of this validation. Exact renewed-freeze commit CI remains
required before pilot invocation.
