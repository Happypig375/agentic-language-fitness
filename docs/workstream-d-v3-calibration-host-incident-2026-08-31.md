# Workstream D v3 calibration host incident (2026-08-31)

The v3 review, CI, and clean-freeze gates completed at commit
`3cfe99b4289036782838b12217022384507b391e` (GitHub Actions `33326196680`,
Linux/Windows green). H used `gpt-5.6-terra` at medium reasoning with resolved
manifest SHA-256
`124a887fd8819383a34927aa026f14ee307f7ecd644a2c3f189b1020169cf82e`,
frozen manifest hash
`ffa03ad5ac578363348027215a2a142dd0c41f1e3e8965b7b0c4c7d120f0028b`,
and image
`sha256:0320a60c5b2628cebeb2c897bbf80da949f3b9bb99fa61f5a3475c7276328756`.

The first H/F# non-counting calibration slot did not produce a frozen candidate
outcome. Both started attempts are retained and classified by the deterministic
v3 rules as protocol-valid, host infrastructure-invalid, retryable, and
`candidate_outcome=false`. No result from either attempt may be used for
configuration selection or a language comparison.

## Evidence ledger

Result and attempt hashes below are SHA-256 values of the retained JSON
artifacts. The raw directories were copied from the detached frozen worktree to
the canonical ignored result root and their complete per-file SHA-256
inventories matched.

| Attempt | Recorded course | Result SHA-256 | Attempt SHA-256 | Raw inventory |
| --- | --- | --- | --- | --- |
| `cal-h-primary-fsharp-01` | Task 001 host probe failed before Docker, authentication, or a candidate process | `c4b09920506954b8c7a8acdaf4ff27acecc741b691b11e6a2a1bb19f9647b0a5` | `20eb168b43cb462bd50d3e8bf21b2e76491463422e2bf1afdfae85f0ca61e898` | 79 files / 3,394,168 bytes |
| `cal-h-primary-fsharp-02` | Task 001 passed with valid usage and evaluation; Task 002 host probe failed, excluding the whole partial chain | `e72cbab66bd64bfae7774004cdde14784e1a49628795fd58738ec69913b09075` | `cb17fc0b0f15a5e392ade4e068d9ef64f05c3f8f2d2eba2a3df0a1580b084c2a` | 122 files / 6,519,765 bytes |

`alf audit` was run on both directories. It failed closed on the task whose
accounting was deliberately unavailable after the explicit host refusal:
Task 001 in `-01` and Task 002 in `-02`. The raw usage sidecars record return
code 75, `host_memory_gate=failed`, zero events and tokens, and the exact failed
probe. The frozen dispositions remain the authority for sequential retry.

## Memory observations

The host reported 8,409,387,008 total physical bytes. Before `-01`, the outer
gate observed 2,315,333,632 available physical bytes, but baseline validation
reduced the immediately-before-Task-001 probe to 2,007,080,960, below the
2,147,483,648 threshold. Docker and authentication were not started.

Before `-02`, a conservative outer gate required 2.5 GiB and observed
2,694,443,008 bytes. The Task 001 probe passed at 2,372,853,760 bytes. Task 001
then completed with valid accounting and evaluation, but the Task 002 probe
observed only 1,334,538,240 bytes and refused before its candidate process.
After the container exited, Docker's WSL VM retained approximately 1.6 GiB with
zero running containers.

Idle Codex terminals were closed, the unused Kali distribution was terminated,
Docker was verified empty, the exact image was retained, Docker caches were
released, and reversible working-set trimming was applied. A scripted waiter
then required 3,758,096,384 physical bytes (3.5 GiB) before it could reserve
`cal-h-primary-fsharp-03`. It took 35 samples over 600 seconds; no sample met
the condition, its highest logged sample was 3,072,167,936 bytes, and it exited
without creating an attempt directory or launching a candidate.

Pre-run command construction checks that did not reserve a run directory,
start Docker, or launch a candidate are not experimental attempts and are not
part of the ledger above.

## Disposition and next action

V3 is not pooled with v1 or v2 and is not interpreted from this partial record.
There is no eligible H/F# predecessor, so the frozen runner correctly prohibits
H/C# and later calibration positions.

Preserve `-01` and `-02`, then copy the exact resolved manifest and complete raw
ledger to a quiescent higher-memory host. The next valid ID is
`cal-h-primary-fsharp-03`; launch it only when the frozen immediately-before-task
memory and concurrency requirements can be sustained. If no suitable host is
available, stop and review a versioned apparatus successor. Do not relax v3's
thresholds or introduce an unreviewed between-task cache or memory intervention.
