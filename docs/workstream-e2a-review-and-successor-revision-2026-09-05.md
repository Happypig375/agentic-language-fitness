# E2a review and successor-plan revision

**Date:** 2026-09-05  
**Status:** E2a accepted within its stated bounds. This review changes the successor experiment from a broad three-arm pilot to a staged controlled-mechanism and tool-hygiene program. It authorizes specification work only, not a model call.

## Evidence reviewed

- `docs/workstream-e2a-disposition-2026-09-04.md`;
- `reports/workstream-e2a-host-aligned-v1/report.{md,json}`;
- `protocols/workstream-e2a-host-aligned-v1/{README.md,definition.json,inventory.json}`;
- the accepted E1 forensic report and E2 model-free report;
- exact-commit CI and audit evidence recorded by those dispositions.

E2a authenticated all 435 completed v3 command events and 258 benchmark `dotnet` operations, reducing them to 23 redacted semantic forms. It then ran 1,020 model-free samples in five paired rounds on the v3 remote host/profile. No candidate, Codex process, authentication material, model endpoint, or paid request was used.

## What E2a establishes

### 1. Two effects compound: F# issued more tool operations, and relevant F# operations were slower

Across the ten v3 runs, the E2a exposure inventory contains 163 F# benchmark `dotnet` invocations and 95 C# invocations. The per-configuration counts were:

| Configuration | C# invocations | F# invocations | F#/C# count ratio |
|---|---:|---:|---:|
| H | 16 | 29 | 1.81 |
| L | 41 | 72 | 1.76 |
| M | 38 | 62 | 1.63 |

Thus the wall-time difference is not only a compiler-speed effect. The F# trajectories also chose or required substantially more build/run/restore operations, consistent with E1's failed-build and repair-cycle evidence.

On the same host/profile, audit-on command-cell means were:

| Operation | C# mean | F# mean | Absolute gap | Paired ratio |
|---|---:|---:|---:|---:|
| restore | 1.377 s | 7.801 s | +6.424 s | 5.664× |
| build | 1.583 s | 8.065 s | +6.483 s | 4.577× |
| run, mixed forms | 0.995 s | 1.404 s | +0.409 s | 1.109× |
| test | 0.664 s | 0.653 s | −0.011 s | 0.985× |
| direct DLL | 0.128 s | 0.131 s | +0.004 s | 1.029× |

The unweighted operation ratios describe command cells, not the frequency-weighted v3 experience. For v3 attribution, the command-frequency exposure envelope is the relevant descriptive summary.

### 2. NuGet audit is a major ecological amplifier and was actually present in v3

With audit enabled, F# restore averaged 7.801 seconds; with `NuGetAudit=false`, it averaged 2.076 seconds. Eligible F# build and run forms also lost roughly six seconds when audit was disabled because those forms could perform implicit restore. Corresponding C# audit deltas were approximately zero.

E2a observed 435 F# `NU1900` lines under audit-on and none under audit-off. More importantly, the authenticated v3 candidate streams themselves contained 197 F# `NU1900` lines and zero C# lines. The offline E2 warning was therefore not merely a GitHub Actions artifact: the same audit/source pathway was active in the agent ecology.

These are repeated emitted lines, not independent defects. Audit delay and audit-output replay must be treated as a tool-policy factor, not as evidence that F# syntax is intrinsically difficult.

### 3. A direct compiler/toolchain difference remains after removing audit

Disabling audit does not erase the F# toolchain difference. Representative no-restore builds remained around 3.2–3.5 times C# on the v3 host, with absolute gaps around 2.6–2.8 seconds. Build forms that still performed restore remained roughly 2.7–2.9 times C# with audit disabled.

Pure execution did not show a comparable difference. Direct-DLL execution and test operations were near parity. Most `dotnet run --no-build` forms were also near parity. The expensive `run` forms were those that implicitly restored or built.

Future reports must therefore distinguish:

- pure program execution;
- test execution without compilation;
- build-only operations;
- restore-capable builds;
- run commands that implicitly build or restore.

A single `run` category hides the mechanism.

### 4. Direct tool exposure is large enough to matter for wall time, but it does not explain model tokens by itself

The frequency-weighted mechanical envelope was:

| Configuration | Mechanical F#−C# gap | Observed E1 agent F#−C# gap |
|---|---:|---:|
| H | 113.1 s | 131.2 s |
| L | 286.7 s | 393.3 s |
| M | 209.8 s | 473.2 s |

These quantities are close enough in scale that direct tool waiting and invocation frequency cannot be treated as a minor nuisance. For H, the two gaps are especially close; for M, a much larger difference remains outside the mechanical envelope.

This comparison is not a causal percentage explained. E2a used successful gold successors, fresh caches, and standardized command replay rather than the actual intermediate candidate states and cache histories. A failing compile may finish earlier or later than a successful gold build, and tool latency can alter subsequent model behavior. The envelope must not be subtracted from agent time or called mediation.

Tool waiting also cannot directly explain the input-token difference. It affects model cost only through mechanisms such as additional tool calls, diagnostic text, extra repair turns, and replayed history. E1 and E2a jointly support that pathway, but per-interaction usage was not retained in v3.

## Corrected interpretation

The strongest bounded explanation is now:

```text
lower first-patch reliability / greater type-project uncertainty
  -> more F# build attempts and repairs
  -> more diagnostics and model turns
  -> more model input/output

language-specific restore/audit and compiler latency
  -> more direct waiting per relevant tool operation
  -> more diagnostic output, especially when implicit restore is repeated
```

Static source size and built-program runtime are poor explanations for the observed small-repository gap. E2a still does not identify whether the first-patch difference comes from syntax, type inference, .NET interop, project mechanics, or lower model familiarity.

## Mandatory successor corrections

### P1 — Controlled mechanism work must remove accidental audit and implicit-restore variation

The next causal pilot must not let an incidental vulnerability audit dominate the comparison. For controlled first-patch and repair measurement:

- perform restore outside the candidate interaction with `NuGetAudit=false`;
- use a fixed no-restore build command;
- execute the built DLL or an equivalent no-build evaluator path;
- keep audit-on/default behavior as a separately named ecological treatment rather than an uncontrolled nuisance.

This does not declare audit unimportant. It separates model/language generation behavior from a known tool-policy amplifier.

### P1 — The controller must own the first patch, build, and repair boundary

E1 left 34 of 80 first-post-edit build outcomes unavailable. E3 must make every boundary observable:

1. materialize the matched gold predecessor;
2. obtain exactly one candidate patch without build/test feedback;
3. preserve and apply that patch once;
4. run the fixed external restore/build/evaluator protocol;
5. record diagnostics, bytes, duration, and outcome;
6. only in the repair condition, provide a bounded diagnostic packet and permit a frozen number of repair rounds.

Candidate agents must not choose arbitrary build/run forms in this controlled mechanism experiment.

### P1 — Record each repair round separately

For every model round, retain separate input, cached input, output, reasoning, wall time, patch identity, diagnostic packet identity, and controller tool time. Record full raw tool output outside the candidate context and the exact bounded text supplied back to the candidate.

Without round-level accounting, the study would again be unable to distinguish first-pass output ability from repair amplification and transcript replay.

### P2 — Demote the standalone comprehension arm

E1 did not show a large, consistent pre-edit navigation separation, whereas build/repair separation was substantial. A separate comprehension arm would add an entire treatment before the leading pathway is resolved.

The first E3 specification should therefore use two primary modes:

1. one-shot patch;
2. controller-mediated bounded repair.

A small structured localization response may be embedded as an auxiliary measure before the patch, provided independent review concludes that it will not materially distort patch generation. Otherwise, comprehension/localization becomes a conditional follow-up only if first-patch and repair outcomes fail to account for the cost pattern.

### P2 — Test deterministic tool hygiene before subagents

E2a identifies a simpler intervention than repair delegation:

- disable vulnerability audit inside the edit–compile loop and run security audit once at a controlled boundary;
- avoid implicit restore in repeated builds;
- avoid `dotnet run` forms that rebuild when direct/no-build execution suffices;
- bound and deduplicate irrelevant repeated warning output before it enters model context;
- preserve raw output separately for auditability.

This tool-policy treatment should precede any multi-agent repair worker. If deterministic hygiene removes most of the excess cost without harming correctness, subagent infrastructure is unnecessary.

## Revised successor sequence

### E3a — Controlled first-patch and repair pilot

Use matched gold predecessors, one reviewed model/scaffold configuration, and a minimal task set spanning simple additive, type/validation, and multi-file/project/API work. Luna high remains the provisional configuration because its archived first-build outcomes were mixed rather than at a floor or ceiling.

Primary comparison:

- one-shot patch with no candidate-visible compiler feedback;
- the same controlled first-patch contract followed by a small, controller-mediated repair budget.

The controller uses audit-off restore, fixed no-restore build, and direct/no-build evaluation. The pilot is non-confirmatory and selects the next mechanism treatment; it does not estimate a universal language effect.

### E3b / F0 — Tool-hygiene policy pilot

Only after E3a establishes a meaningful repair/tool-feedback pathway, compare a small ecological default-tool condition with a hygienic single-agent condition. Keep the model, tasks, and starting states fixed. The hygienic condition changes only reviewed tool policy; it does not introduce subagents.

Report total model cost, direct tool time, diagnostic bytes supplied to the model, correctness, and repair count separately.

### F1 — Isolated repair worker, only if F0 is insufficient

Compare fresh inline repair with fresh isolated same-model repair. Enforce separate contexts and separate accounting. Do not add persistent orchestration, cheaper workers, recursive agents, or dynamic routing yet.

### F2 — Persistent context, only after F1

Add persistent inline and persistent delegated conditions only if F1 demonstrates auditable context containment and a meaningful decision-quality or cost effect.

### G — Registered small-repository replication

Treat default ecological, hygienic single-agent, and delegated-agent setups as separate harness strata. Do not pool them. Replicate only the strata justified by E3/F.

### H — Multi-scale context-pressure study

Use the controlled/hygienic tool path as the primary mechanism condition so a known restore/audit/compiler fixed cost does not swamp the language × scale estimate. An ecological default-tool stratum may be secondary. Context-density claims still require real retrieval, persistent-history, or compaction pressure.

## Claim boundary

E2a supports this bounded statement:

> On the v3 host and command ecology, F# trajectories both invoked more `dotnet` operations and paid substantially more for restore/build-capable operations. NuGet audit was a major F#-specific amplifier and appeared in the actual v3 streams; a sizeable compiler/toolchain gap remained with audit disabled. These direct tool effects are large relative to the observed wall-time gap, while the model-token gap still requires extra interactions, feedback, and replay.

It does not identify intrinsic language difficulty, training-corpus familiarity, a causal percentage of agent cost, a context-scale slope, or a universal ranking.