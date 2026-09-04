# E2a exact-command and host-aligned disposition

**Date:** 2026-09-04  
**Status:** Complete and published; independently reviewed within the stated evidence boundaries. No candidate, Codex process, authentication, model endpoint, or paid request was used.

## Scope and identities

E2a completed 1,020 model-free samples in five paired rounds. It reconstructed the redacted command-equivalence inventory observed in E1, benchmarked the materially distinct restore/build/run/test/direct-DLL forms, and added an otherwise matched `NuGetAudit=false` restore control. The accepted offline E2 result is a separate ecology and is not pooled with E2a.

The frozen identities are:

| Artifact | SHA-256 or commit |
|---|---|
| scientific definition | `8e1f417f2355c169102b68495dc083a0c61e0ea3e180914568be7603651448df` |
| command inventory | `794591e97d150bdc13d7a9079cee72cbd92f3057a639f71addc71c3f5fad4de3` |
| schedule | `c1e4b3c97c03b910f02fe39d19be9eaa608005359e81174b96acbf4c69b70308` |
| measurement runner commit | `901260d7473648f67ee6dd9e469a922023866e2c` |
| analyzer portability commit | `b0a524578d1887b5e455ff5ee236a16636612166` |
| measurement artifact | `dac51cddf1be7b6b3d4457ec53f4dc700328bb4094e4a12fab0f8f51514dd791` |
| raw inventory | `33b584ca1b0635572e3f0a803c9de68b5142d0be1b9c697b59a8aa69e0584db9` |
| report semantic content | `66e37e1086159e462aafee684108f3cda431368da1daa1900971bfdfe88a0aeb` |
| report file | `e392ed7dfeb29732b4a5d5b64b9e9b2cdc090b99ad221bdaf557ef02252d57fe` |

The published aggregate is [the E2a report](../reports/workstream-e2a-host-aligned-v1/report.md), with machine-readable evidence in the adjacent `report.json`. The redacted inventory preserves the observed frequency classes without publishing raw commands, paths, transcripts, or output.

## Results

Aggregate audit-on unweighted paired command-cell/round means are shown with absolute effects and output bytes:

| Operation | C# mean s | F# mean s | F#−C# gap s | F#/C# geomean | C# output B | F# output B |
|---|---:|---:|---:|---:|---:|---:|
| restore | 1.377 | 7.801 | +6.424 | 5.664× | 217 | 433 |
| build | 1.583 | 8.065 | +6.483 | 4.577× | 282 | 943 |
| run | 0.995 | 1.404 | +0.409 | 1.109× | 1094 | 1118 |
| test | 0.664 | 0.653 | −0.011 | 0.985× | 0 | 0 |
| direct DLL | 0.128 | 0.131 | +0.004 | 1.029× | 961 | 961 |

The audit control isolates a large F# restore/audit effect: F# restore was 7.801 s audit-on versus 2.076 s audit-off. Eligible F# build was 11.628 versus 5.430 s, and eligible F# run was 12.252 versus 6.371 s; corresponding C# deltas were approximately zero. F# emitted 435 `NU1900` lines audit-on and zero audit-off. The authenticated v3 candidate streams contained 197 F# and zero C# `NU1900` lines. These are repeated emitted lines and ecology-dependent output-volume observations, not independent defects. Parsed diagnostic occurrences in the aggregate command summaries were zero; `NU1900` is reported separately.

The mechanical invocation-count × matched-duration envelope, beside observed E1 agent seconds, was:

| Configuration | Language | Invocations | Mechanical seconds | Observed E1 agent seconds |
|---|---|---:|---:|---:|
| H | C# | 16 | 20.6 | 502.4 |
| H | F# | 29 | 133.7 | 633.6 |
| L | C# | 41 | 48.1 | 955.8 |
| L | F# | 72 | 334.8 | 1349.1 |
| M | C# | 38 | 48.9 | 1150.3 |
| M | F# | 62 | 258.7 | 1623.4 |

This envelope is a mechanical timing counterfactual. It is not subtracted from agent cost, called mediation, or expressed as a percent explained. Remaining differences include model interaction and repair behavior.

## Host, CI, and numerical evidence

The benchmark used the v3 remote host/profile, pinned image/toolchain, and reviewed resource/storage configuration. Separately, host Python 3.10.12 completed the full E1 plus raw audit, and the pinned `alf-codex:0.149.1` image (Python 3.12.3) passed a network-none/read-only audit with the same report hash. Exact-commit analyzer CI is [Actions run 33890449685](https://github.com/Happypig375/agentic-language-fitness/actions/runs/33890449685): Linux and Windows succeeded; the E2 job was intentionally skipped. A `1e-12` tolerance applies both relatively and absolutely, and only to finite derived summary floats. Measurements, identities, raw evidence, structure, and each report self-hash are exact.

## Bounds and disposition

E2a uses canonical gold successors rather than intermediate candidate edits; fresh caches rather than the unknown within-task cache history; semantic shell replay rather than incidental shell text; and observed, not controlled, host/page-cache load. Candidate/authentication behavior is deliberately absent. Therefore E2a aligns and bounds direct tool exposure but does not reproduce a candidate trajectory or identify a causal decomposition.

Together with E1, E2a strengthens the coupled hypothesis that first-pass/type/project difficulty produces more failed builds, repairs, diagnostics, commands, and model turns, while slower compiler/audit operations amplify each extra cycle. Near-parity test, direct-DLL, and most built-program run behavior remain consistent with that interpretation. The result is descriptive and local to this ecology; it is not a causal or universal F#/C# ranking.

E2a publication is the end of the current bounded task. The next separately reviewed step is an E3 scientific specification. No model call is authorized without a separate maintainer/user decision. Do not create v14.
