# E3a remote sandbox fix and model-free evidence

2026-09-06. The user authorized continued fixes on the reachable remote host
after the [two-failure stop](workstream-e3a-implementation-handoff-2026-09-06.md).
The bounded dependency-export correction and sandbox checks are complete on
that host with the exact specified image. Review here is **self-review and
model-free testing**, not independent implementation approval, scientific freeze,
or permission for live consumption. All attempts used **zero candidate model
calls, zero input-count HTTP calls and zero experiment spend**.

## Diagnosis and minimal correction

The diagnostic attempt reproduced `Could not find the file /work/obj in
container` after a successful restore. `/work` is a tmpfs: Docker's daemon-side
copy did not see the running container's restored files. Docker documents
limitations copying tmpfs/system mounts and recommends working through the
running container. [Docker container cp documentation](https://docs.docker.com/reference/cli/docker/container/cp/).

Trusted preparation now copies `/work/obj` and `packages.lock.json` from inside
the container into one private writable `/seed-out` bind mount. Cleanup makes
only preparer-owned contents removable, including after a failed restore;
host-owned mount roots are excluded. The ready seed/cache identities are
published only after successful export and cleanup. Administrative failures
retain at most 4,096 diagnostic characters.

Candidate evaluation still receives only read-only `/input`, `/seed` and
`/packages` mounts. It never receives `/seed-out`. UID, capabilities, network,
memory, CPU, PID, time and output limits are unchanged. No fallback export path,
new proxy, daemon, remote framework or scientific version was introduced.

## Environment and identities

The remote host was reached using SSH launched from PowerShell. It had Linux
6.8.0-124-generic, Docker 29.1.3 and approximately 503 GiB RAM. A private Python
3.11.15 virtual environment was used, leaving the host's Python and existing
environments unchanged. No model authentication material was staged or read.

The earlier archive search was incomplete. The original
`alf-codex-0.149.1-sha256-0320a60c5b2628ce.tar` was found under the existing
`X:/backup20260827/Archives/SourceRepos/agentic-language-fitness-images/` backup.
Its 630,053,888 bytes hashed identically before and after transfer:
`55ee85f0656cef429d1cd40edced79782d54abb7b2180c9770c14bea06828ddf`.
Loading and inspecting it produced the exact specified image ID:
`sha256:5d3e97d195dbbe7e47e47055e46f8c6f15fb9553be0c7ef19ed0060756fc7116`.
The image, not a replacement SDK tag, was used for the final checks.

Scientific specification canonical SHA-256 remains
`8bc53d30e45dfa72b087225f89c9e5547266f05b47e4306e2b326d951888bc62`.
The [final artifact](../reports/workstream-e3a-sandbox-2026-09-06/e3a-pinned-image-final-04.json)
records LF-normalized hashes of the sandbox, workload helper and check script,
plus Python/host/image identities. The regenerated
[review packet](../protocols/workstream-e3a-v1/review-packet.json) additionally
binds the implementation tests. Git identifies the implementing revision;
these source hashes allow the pre-commit remote check to be matched to it.

## Retained attempts and actual scope

| Attempt | Result and scope |
|---|---|
| [01: diagnostic](../reports/workstream-e3a-sandbox-2026-09-06/e3a-export-diagnostic-01.json) | Reproduced the original Docker copy failure with bounded stderr; no sandbox probe completed. |
| [02: corrected export](../reports/workstream-e3a-sandbox-2026-09-06/e3a-sdk-fixed-export-02.json) | Full model-free sandbox checks passed on the exact CI SDK fixture, not the experimental image. |
| [03: specified image](../reports/workstream-e3a-sandbox-2026-09-06/e3a-pinned-image-03.json) | The same checks passed on the restored specified image. |
| [04: final evidence](../reports/workstream-e3a-sandbox-2026-09-06/e3a-pinned-image-final-04.json) | Passed again with final runtime code and source/spec/host identity recording. |

Both C# and F# restored, exported their dependency seed, built and ran the
positive fixture. Intentionally broken source failed compilation and never ran
or acquired a binary identity. Network denial, credential/scorer/socket absence,
read-only source/seed/cache/root, writable `/tmp` and `/work`, zero capabilities
and no-new-privileges passed. Effective limits were 6 GiB memory with no extra
swap, 2 CPUs and 512 PIDs. Output overflow was stopped, a timed-out descendant
was removed with its container, and cleanup reported no errors.

The memory stress is deliberately a separate **128 MiB fixture**, which recorded
an OOM kill and exit 137. It is not a measurement of an experimental workload
at 6 GiB; that policy was inspected separately. These checks do not establish
language performance or exhaustive sandbox security.

All 25 implementation regressions and 17 workload/controller tests passed on
Windows and remote Python 3.11; the regenerated packet matched. New regressions
cover bounded Docker diagnostics, in-container export, failure cleanup excluding
mount roots, and the absence of writable preparation mounts from evaluation.
The ordinary Linux/Windows CI workflow must also pass on the exact implementing
commit; consult its attached checks, not the earlier failed runs or a different
green revision. The CI sandbox uses its explicitly labelled SDK fixture.

## Remaining boundary

The artifact intentionally retains `intended_remote_environment_verified=false`:
it proves standalone Docker checks on the intended host/image, **not** complete
Windows/API-controller-to-remote orchestration. That model-free wiring check,
account/model access, actual rates and count charges, provider continuation,
count/create agreement and usage reconciliation remain outstanding.

No live call is authorized by this repair. A later integration requires separate
approval for at most **two generations / $0.05** on an unrelated task. The fixed
pilot remains separately proposed at **24 trajectories / 72 generations / $2**.
Neither sandbox success nor passing CI grants either permission. E1/E2/E2a
artifacts, scientific conditions and execution-authorization flags are unchanged.
