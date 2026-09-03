# E1/E2 synthesis review and corrected successor gate

**Date:** 2026-09-04  
**Status:** E1 and E2 evidence accepted; successor design approved only after the mandatory model-free E2a alignment step below. No model call is authorized.

## Review scope

This review asks what Workstreams E1 and E2 actually establish, which earlier interpretations require correction, and what the smallest next experiment should be.

Reviewed evidence:

- `reports/workstream-e-v3/forensic-report.{md,json}`;
- `docs/workstream-e1-v3-forensic-disposition-2026-09-03.md`;
- `reports/workstream-e2-toolchain-v1/report.{md,json}`;
- `docs/workstream-e2-toolchain-disposition-2026-09-04.md`;
- the E1/E2 analyzers, protocols, command definitions, missingness ledgers, and exact-commit CI records.

The immutable E1 and E2 reports remain unchanged. This document qualifies their joint interpretation and controls the successor design.

## Accepted evidence

### E1: repair and compiler interaction are the leading observed pathway

E1 reconciled all ten v3 runs and 80 tasks. Among observable candidate operations:

- all 25 failures were build failures;
- F# accounted for 23 failed builds and C# for 2;
- F# accounted for 17 conservative repair cycles and C# for 2;
- first-post-edit build outcomes contained 17 identifiable F# failures and 2 C# failures, with 34 task boundaries remaining unavailable rather than imputed;
- all five committed project-file changes were F#;
- F# carried almost all observed compiler diagnostic errors and repeated nullability warnings;
- evaluator duration was approximately twice as large for F# in every configuration.

Observable pre-edit inspection/search activity was much less separated than the build/repair signal: the low-capability configuration was equal on the reported inspection/search counts, the medium configuration differed modestly, and the high configuration had substantial first-build missingness. E1 therefore prioritizes first-pass generation, compiler/type interaction, repair amplification, and ecological project/toolchain obligations. It does not identify hidden deliberation or training familiarity.

Diagnostic **occurrences** are not independent mistakes. In particular, 450 warning occurrences were repeated `FS3261` output. Future analysis must use failed build episodes, unique diagnostic codes/categories per episode, and repair transitions as the main units; emitted-line counts remain output-volume measures.

### E2: F# toolchain setup/build is slower in the frozen offline ecology; built-program execution is not

E2 completed all 18 states and 90 schedule entries, with every command and all 180 cumulative evaluator invocations passing. Across 45 paired stage-by-round observations:

- fresh restore means were 6.410 s for F# and 0.763 s for C#; paired ratio 8.403;
- fresh build means were 2.107 s and 0.706 s; paired ratio 3.037;
- repeat build means were 2.102 s and 0.674 s; paired ratio 3.117;
- built-program run time was near parity: paired ratios 0.988 fresh and 0.984 repeat;
- source and whole-tree token proxies were near parity over the nine states;
- Task 007 imposed an explicit F# project compile-order obligation that C# SDK discovery did not.

The repeat-build result is the cleanest evidence of a direct F# compiler/toolchain latency difference in this apparatus because it excludes restore. It is still an ecological language-stack measurement, not a pure syntax or type-system effect.

### Joint interpretation

The strongest current explanation is a coupled pathway:

```text
lower first-pass reliability / greater type-project uncertainty
    -> more failed builds and repair cycles
    -> more diagnostics, edits, commands, and model turns
    -> more replayed/cached input, output, and wall time

slower F# build/evaluator operations
    -> each additional repair cycle is also slower
```

This is more consistent with the evidence than a static source-size explanation. The checked-in F# and C# representations were similarly sized, while the behavioral difference was concentrated in failed builds, diagnostics, repair cycles, and command output.

Toolchain latency alone should not be assumed to explain the approximately 38% model/agent cost gap. The direct repeat-build difference is about 1.4 seconds per invocation, whereas paired agent-process gaps were commonly hundreds of seconds. Exact contribution requires the command-aligned exposure calculation specified in E2a. The toolchain can also change agent behavior, so even that calculation is descriptive rather than a valid subtraction.

## Mandatory corrections

### P1 — The 8.403× restore ratio is not transportable to v3 as currently measured

E2 deliberately disabled network access and observed 225 emitted F# `NU1900` lines. `NU1900` means NuGet could not retrieve package vulnerability data from a configured source. NuGet auditing runs during restore and can be disabled with `NuGetAudit=false`.

Therefore the E2 restore result is valid for the frozen offline ecology but is entangled with package-audit/source behavior. It must not be used as a direct estimate of the restore cost experienced by v3 candidate agents unless the candidate command, package cache, audit settings, and network/source reachability are shown to match.

**Correction:** run the model-free E2a command/environment alignment before E3.

References:

- https://learn.microsoft.com/en-us/nuget/reference/errors-and-warnings/nu1900
- https://learn.microsoft.com/en-us/nuget/concepts/auditing-packages

### P1 — E2 command shapes are not yet aligned to the commands observed in E1

E2 used a frozen sequence of explicit restore, Release `--no-restore` build, and direct program execution. Candidate agents may have used plain `dotnet build`, implicit restore, `dotnet run`, project-specific variants, compound commands, or other configurations.

A model-free timing ratio is explanatory only for operations actually encountered by candidates. Applying the E2 ratio to a different command mix would confound command semantics with language.

**Correction:** extract the exact bounded E1 command-equivalence classes and benchmark only the relevant model-free forms under an explicitly matched environment profile.

### P1 — E2 host and resource conditions are not the v3 execution profile

E2 ran in a GitHub-hosted Ubuntu Actions container, while v3 candidate trajectories ran through the reviewed remote high-memory profile. Absolute compiler and restore timings can depend on CPU, storage/filesystem, container image, package-cache placement, memory/CPU/PID limits, and host load even when the .NET SDK version is the same.

**Correction:** execute E2a on the v3 remote host/profile when safely reproducible, or explicitly bound every remaining mismatch. Do not treat GitHub-hosted timing as a direct component of remote candidate wall time.

### P1 — E3 must make first-pass boundaries controller-observable

E1 could identify only 46 of 80 first-post-edit build outcomes; 34 remained unavailable because v3 was not designed around a controller-defined first patch and first build. Repeating that event ambiguity would defeat the main causal question.

**Correction:** in E3 one-shot and full-repair modes, the controller must define and preserve the first submitted patch, apply it once, run the same external first build/evaluator, and only then permit repair in the full condition. The first-build result and diagnostics are thus directly observed rather than reconstructed.

### P2 — Ratios must always be paired with absolute effects

Large ratios can arise from small subsecond baselines. E2 reporting is retained, but successor reports must place paired absolute seconds, output bytes, and invocation counts beside ratios. Practical significance should be expressed in total per-task/per-chain exposure, not operation ratios alone.

### P2 — Warning/output volume must not be interpreted as defect count

Repeated compiler warnings can appear in restore, build, and evaluator output. Count separately:

- failed operation episodes;
- unique diagnostic codes/categories per episode;
- repeated emitted lines/bytes/tokens;
- edit–build and test–edit transitions.

### P2 — E1 cannot establish training familiarity or context pollution

More observed inspection can suggest a comprehension pathway but cannot identify pretraining familiarity or hidden reasoning. Fresh-per-task v3 cannot show cross-task context accumulation. Those require controlled comprehension and persistent-context treatments.

### P2 — Full-minus-one-shot is a policy contrast, not literal mediation

Removing compiler feedback changes model behavior. Differences between one-shot and full-repair conditions may quantify the consequence of permitting repair, but they are not an algebraic decomposition of one fixed trajectory. Do not label the difference as a causally identified token contribution without stronger mediation assumptions.

### P2 — Repair delegation should be staged, not implemented as a general framework

First test fresh-context inline repair versus fresh-context isolated repair. Only after separate-context accounting works and shows value should persistent orchestrator conditions be added. Use the same model for orchestrator and worker initially. A cheaper worker is a later practical treatment.

## E2a — Command- and environment-aligned model-free baseline

This is the next bounded task. It uses no model endpoint.

### Inputs

- the preserved E1 command classifications and raw command metadata outside Git;
- the matched baseline/gold repository states;
- the reviewed v3 runner image/toolchain and the accepted E2 measurement code where reusable.

### Required conditions

1. Reconstruct a redacted frequency table of actual build/restore/run/test command-equivalence classes by language, task, and configuration.
2. Collapse only variants with demonstrably equivalent command semantics. Replay every semantically distinct compiler/test form and every class with material exposure, without reproducing incidental shell plumbing merely because its spelling differs.
3. Replay only command forms that materially occurred in E1.
4. Execute on the v3 remote host/profile when it can be reproduced safely, matching the container image, CPU/memory/PID limits, storage/filesystem path, package cache, environment variables, build configuration, network/source reachability, and audit behavior. If any component cannot be matched, predeclare it and limit transportability.
5. For restore-capable command forms, add one explicit `NuGetAudit=false` counterfactual while holding all other conditions fixed.
6. Preserve the existing offline E2 result as a separate ecology; do not overwrite or pool it.
7. Report paired ratios and absolute deltas, diagnostic/output volume, and uncertainty.
8. Compute a mechanical exposure envelope:

```text
estimated direct tool time(language)
  = sum over command classes [observed E1 invocation count × model-free duration]
```

This estimate is a timing counterfactual only. It is not subtracted from agent cost and does not identify behavioral feedback effects.

### E2a exit criteria

- exact E1 command forms and their frequency are auditable without publishing sensitive raw commands;
- audit/network/source and host/resource/filesystem conditions are matched or explicitly bounded;
- the `NU1900` contribution is bounded by the audit-on/audit-off contrast;
- direct tool-latency exposure is compared with the observed agent-time gap in absolute seconds;
- the report states what remains attributable only to model interaction and repair behavior;
- independent review and exact-commit Linux/Windows CI pass.

## Corrected E3 mechanism pilot

E3 is designed only after E2a. It remains small, non-confirmatory, and uses matched gold predecessor snapshots.

### Task selection

Select and freeze a minimal set using only E1/E2 mechanism evidence:

- one low-diagnostic/simple additive task;
- one type/validation task with observed F# diagnostics;
- one multi-file/project/API task, normally Task 007 or 008.

Selection is hypothesis-routing, not a language-effect estimate. Document the task-level evidence before any new outcome exists.

### Configuration

Use one exact model/scaffold setting selected for **nondegenerate first-patch outcomes on the chosen tasks**, not simply the lowest monetary cost or largest exploratory language difference. E1 makes M (`gpt-5.6-luna`, high) the provisional default because its observable F# first-post-edit builds were mixed at 10 successes, 3 failures, and 3 unavailable; L was near a floor at 0 successes, 13 failures, and 3 unavailable; H had 6 of 8 boundaries unavailable. Confirm the choice from task-level evidence and current preflight, document it before E3 outcomes exist, and freeze it. Do not vary model, effort, and harness simultaneously.

### Modes

1. **Comprehension/localization auxiliary arm** — controller-enforced read-only source access; fixed structured answer for relevant files/symbols, invariants, and obligations; no compiler/test feedback. This can identify observable comprehension differences, not pretraining familiarity.
2. **One-shot patch primary arm** — same task/source state; exactly one controller-recorded patch; candidate receives no build/test feedback; controller performs the first external build and evaluation.
3. **Full-repair primary arm** — same initial state and first-patch contract, followed by a small frozen repair budget with normal compiler/test feedback.

### Primary mechanism outcomes

- first-patch build and behavioral success;
- failed-build episode and diagnostic-category incidence;
- repairs required to reach correctness;
- total input/output/reasoning/tool use in the full condition;
- paired absolute and relative cost by task family;
- structured comprehension/localization accuracy as a separate outcome.

The one-shot/full comparison is interpreted as a harness-policy contrast. It is not a literal mediation subtraction.

### E3 stopping rule

Stop after the preregistered pilot sample and produce a mechanism decision. Do not expand into a language × model × task × mode factorial. Two repeated apparatus failures of one class require a stop report rather than another compatibility layer.

## Conditional Workstream F — context containment and repair delegation

Run only if E3 confirms meaningful repair amplification.

### F1 first

Compare **fresh + inline** with **fresh + delegated** repair. Enforce separate processes/contexts and account for orchestrator and worker separately. The orchestrator receives only a frozen structured repair summary unless a preregistered semantic escalation occurs.

Report:

- total system cost;
- orchestrator-only cost;
- worker cost;
- raw diagnostic/tool-output volume withheld from the orchestrator;
- correctness and repair/escalation outcomes.

### F2 only if F1 is viable

Add persistent orchestrator conditions to test cross-task pollution:

- persistent + inline;
- persistent + delegated.

Do not build persistent orchestration before F1 demonstrates auditable context separation. No recursive subagents or dynamic routing are authorized.

## Successor sequence

```text
E1/E2 synthesis review — complete
  -> E2a exact-command/host/environment model-free alignment
  -> E3 reviewed one-shot/full-repair mechanism pilot
  -> comprehension/familiarity follow-up as indicated
  -> F1 fresh repair containment, then F2 persistence only if justified
  -> registered small-repository ecological replication
  -> medium-scale language × context-pressure study
```

## Claim boundary

The current evidence supports only this bounded interpretation:

> In the tested small-repository ecology, F# incurred more observable build failures, diagnostics, repair cycles, project work, model usage, and time than C#. A slower F# toolchain amplified that pathway. Static source size and built-program runtime do not explain the observed gap, while hidden model familiarity, unique source exposure, persistent context effects, and exact cross-host timing attribution remain unidentified.

It does not establish an intrinsic language ranking, a training-corpus cause, a context-density slope, or a crossover.