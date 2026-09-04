# Research plan

This is the canonical continuation plan. Workstream D v3 is closed. Workstreams E1, E2, and E2a are complete and accepted within their stated evidence boundaries. The project now separates controlled model/language mechanisms from ecological tool policy before considering repair subagents or a larger replication.

## Scientific checkpoint — 2026-09-05

Completed and preserved:

- Workstreams A–C: accounting/provenance, `variance-v2`, the matched eight-task successor chain, and representation apparatus;
- Workstream D v3: reviewed remote runner, clean freezes, and ten audited non-counting calibrations;
- Workstream E1: archive-only forensic attribution over 10 runs and 80 tasks, report SHA-256 `644273ac0f25a32138d50d919ff15677b6ed9639a23198e0c719d154da94901d`;
- Workstream E2: offline model-free source/toolchain baseline over 18 states and 90 schedule entries, report SHA-256 `2e4381ab67dd4cc7aed24c323e8edbd30bf83dd29bafc58554615bcd6f24c49a`;
- Workstream E2a: exact-command, v3-host-aligned model-free baseline over 1,020 samples in five paired rounds, report file SHA-256 `e392ed7dfeb29732b4a5d5b64b9e9b2cdc090b99ad221bdaf557ef02252d57fe`;
- exact-commit Linux and Windows CI for the accepted implementations and publications.

Authoritative current review:

```text
docs/workstream-e2a-review-and-successor-revision-2026-09-05.md
```

Supporting evidence:

```text
docs/workstream-e1-v3-forensic-disposition-2026-09-03.md
docs/workstream-e2-toolchain-disposition-2026-09-04.md
docs/workstream-e2a-disposition-2026-09-04.md
reports/workstream-e-v3/forensic-report.md
reports/workstream-e2-toolchain-v1/report.md
reports/workstream-e2a-host-aligned-v1/report.md
```

V4–V13 remain apparatus-development history, not scientific families. Do not create v14. Reuse `runner-remote-highmem-local-egress-r1` unless a separately reviewed candidate-visible change is necessary. Scientific changes receive scientific-specification IDs rather than runner-version numbers.

No model or paid run is currently authorized. The next bounded task is E3a specification and independent review only.

## What the current evidence shows

### E1: observable divergence occurs mainly in build and repair behavior

Across the ten v3 calibration runs:

- 25 observable candidate failures were all build failures;
- F# accounted for 23 failed builds versus 2 for C#;
- F# accounted for 17 conservative repair cycles versus 2 for C#;
- identifiable first-post-edit failures were 17 for F# and 2 for C#, while 34 boundaries remained unavailable rather than imputed;
- all five committed project-file changes were F#;
- F# carried nearly all observed compiler diagnostic errors and repeated nullability warnings;
- evaluator duration was approximately twice as large for F# in every configuration.

Observable pre-edit inspection/search differences were comparatively modest. E1 therefore prioritizes first-patch generation, type/compiler interaction, project obligations, and repair amplification. It does not identify hidden reasoning or training familiarity.

Diagnostic line occurrences are output-volume observations, not independent defects. Use failed operation episodes, unique diagnostic codes/categories per episode, and repair transitions as the main units.

### E2a: F# both invoked more tools and paid more per restore/build-capable operation

E2a authenticated all 435 completed v3 command events and 258 benchmark `dotnet` operations, reducing them to 23 semantic forms. The exposure inventory contains 163 F# and 95 C# benchmark invocations. Per configuration:

| Configuration | C# invocations | F# invocations |
|---|---:|---:|
| H | 16 | 29 |
| L | 41 | 72 |
| M | 38 | 62 |

Audit-on command-cell means on the v3 host/profile were:

| Operation | C# mean | F# mean | Absolute gap | Paired ratio |
|---|---:|---:|---:|---:|
| restore | 1.377 s | 7.801 s | +6.424 s | 5.664× |
| build | 1.583 s | 8.065 s | +6.483 s | 4.577× |
| mixed run forms | 0.995 s | 1.404 s | +0.409 s | 1.109× |
| test | 0.664 s | 0.653 s | −0.011 s | 0.985× |
| direct DLL | 0.128 s | 0.131 s | +0.004 s | 1.029× |

These operation means are unweighted command-cell summaries. The frequency-weighted mechanical envelope is the relevant descriptive comparison to v3:

| Configuration | Mechanical F#−C# gap | Observed E1 agent F#−C# gap |
|---|---:|---:|
| H | 113.1 s | 131.2 s |
| L | 286.7 s | 393.3 s |
| M | 209.8 s | 473.2 s |

The envelope is not subtracted from agent time, called mediation, or converted into a causal percent explained. It uses successful gold successors and fresh caches rather than actual intermediate candidate states and cache histories. It nevertheless shows that direct tool exposure is of the same order as a substantial part of the wall-time difference and cannot be treated as negligible.

### NuGet audit is a real ecological amplifier

With audit enabled, F# restore averaged 7.801 seconds; with `NuGetAudit=false`, it averaged 2.076 seconds. Restore-capable F# build/run forms also lost roughly six seconds when audit was disabled, while C# audit effects were approximately zero.

E2a emitted 435 F# `NU1900` lines under audit-on and none under audit-off. The authenticated v3 candidate streams contained 197 F# `NU1900` lines and zero C# lines. These are repeated output lines, not independent defects.

A sizeable compiler/toolchain difference remains after disabling audit. Representative no-restore builds retained roughly 3.2–3.5× F#/C# ratios and absolute gaps around 2.6–2.8 seconds on the v3 host. Pure execution, direct-DLL execution, and test behavior were near parity.

Future reporting must distinguish pure execution from `run` forms that implicitly build or restore. A single `run` category is not mechanistically meaningful.

## Interpretation boundary

The leading bounded pathway is:

```text
lower first-patch reliability / greater type-project uncertainty
  -> more F# build attempts and repairs
  -> more diagnostics and model turns
  -> more model input/output

language-specific compiler and restore/audit behavior
  -> more direct waiting and output per relevant tool operation
  -> amplification of repair-heavy trajectories
```

Static source size and built-program runtime do not explain the observed small-repository gap. E1/E2a do not yet identify whether first-patch difficulty comes from syntax, type inference, .NET interop, project mechanics, or lower model familiarity.

Tool latency cannot by itself explain model tokens. It affects model usage only through additional calls, diagnostics, feedback, and replay. Per-round usage and exact context exposure were not retained in v3.

The repository was only about two thousand source-proxy tokens. It measures a local small-repository ecological gap, not context-window fitness or a language-by-scale slope. Any semantic-density crossover must be observed under genuine retrieval, persistent-history, or compaction pressure.

## Current decision

Revise E3 from a broad three-arm experiment into a staged program:

1. **E3a controlled first-patch and repair pilot** — isolate first-patch validity and bounded repair under a fixed, audit-off, controller-owned tool path.
2. **E3b/F0 deterministic tool-hygiene pilot** — test whether simple tool policy removes the ecological overhead before constructing subagents.
3. **F1 isolated repair worker** — only if meaningful repair/context burden remains after tool hygiene.
4. **F2 persistent orchestrator** — only after F1 demonstrates auditable context separation.

A standalone comprehension arm is no longer co-primary. E1 did not show a large consistent pre-edit navigation difference. Localization may be an auxiliary structured measure or a conditional follow-up if E3a fails to account for the pattern.

## Immediate continuation order

### E3a — Specify a controlled first-patch and bounded-repair pilot

**Next bounded task: specification, deterministic fixtures/identities, independent review, clean freeze, and exact-commit CI only. Do not invoke a model.**

#### Scientific question

Under a fixed controller-owned compile/evaluation path that removes vulnerability-audit and implicit-restore variation:

1. Are F# first patches less likely to compile or satisfy behavior?
2. Which diagnostic categories differ?
3. How much additional model/tool usage arises when bounded repair is allowed?

#### Task set

Freeze a minimal mechanism-spanning set using only E1/E2/E2a evidence:

- one simple, low-diagnostic additive task;
- one type/validation task with observed F# diagnostics;
- one multi-file/project/API task, normally Task 007 or 008.

Use the canonical gold predecessor for each task. Task selection is hypothesis-routing, and the pilot is non-confirmatory.

#### Configuration

Use one exact model/scaffold setting selected for nondegenerate first-patch outcomes. M (`gpt-5.6-luna`, high) remains the provisional default because its archived F# first-build outcomes were mixed; L was near a first-build floor and H had excessive boundary missingness. Confirm the choice from task-level evidence and current availability before freeze. Do not vary model, effort, and harness simultaneously.

#### Common controller path

For both languages and both modes:

1. materialize and verify the matched source-only predecessor;
2. obtain exactly one candidate patch without candidate-visible build/test feedback;
3. preserve and apply the patch once;
4. evaluate in an external controller workspace;
5. perform restore with `NuGetAudit=false` outside candidate interaction;
6. use a fixed no-restore build command;
7. execute the built DLL or another fixed no-build evaluator path;
8. retain full raw output outside candidate context and record exactly what feedback, if any, is supplied to the candidate.

Candidate agents may inspect allowed source but may not invoke arbitrary `dotnet`, test, network, or shell build forms in this controlled mechanism treatment. Default free-tool behavior remains an ecological treatment for E3b/G.

#### Primary modes

1. **One-shot patch**
   - one controller-recorded multi-file patch;
   - no compiler/test feedback before terminal external evaluation.

2. **Controller-mediated bounded repair**
   - the same first-patch contract and external first build;
   - only after the first result, a frozen number of repair rounds;
   - each round receives a bounded, versioned diagnostic packet;
   - no implicit restore, vulnerability-audit output, or unrelated repeated warnings enter candidate context.

A small structured localization response may be embedded before the patch only if independent review concludes that it will not materially alter patch generation. Otherwise defer comprehension/localization.

#### Required per-round evidence

For every model round record separately:

- input, cached input, output, and reasoning tokens;
- process/model wall time;
- patch identity and size;
- controller restore/build/run/evaluator durations;
- raw diagnostic/output identity and volume;
- exact candidate-visible diagnostic packet identity and volume;
- first-build and behavioral outcome;
- unique diagnostic codes/categories;
- repair count and terminal correctness.

This closes the v3 missingness around first patch, first build, and phase usage. One-shot versus repair remains a policy contrast, not an algebraic mediation subtraction.

#### E3a stopping rule

Predeclare task identities, model/effort, sample size, mode order, patch format, controller commands, diagnostic packet policy, retries, exclusions, evidence retention, and stopping. Stop after the non-confirmatory pilot and produce a mechanism decision. Do not expand into a language × model × task × mode factorial.

### E3b / F0 — Deterministic tool-hygiene policy pilot

Run only after E3a shows that repair/tool feedback is a meaningful pathway. Compare a small default ecological single-agent condition with a hygienic single-agent condition while holding model, task, starting state, and repair authority fixed.

The hygienic condition should implement only reviewed deterministic policy:

- perform vulnerability audit once at a controlled boundary or disable it inside the edit–compile loop;
- avoid implicit restore in repeated builds;
- avoid `dotnet run` forms that rebuild when direct/no-build execution suffices;
- bound and deduplicate irrelevant repeated warning output before model feedback;
- preserve full raw output outside model context.

Report separately:

- correctness and first-patch correctness;
- total input/output/reasoning;
- direct tool time;
- tool invocation count;
- raw versus candidate-visible diagnostic volume;
- repair count and terminal wall time.

This simple harness intervention precedes subagents. If it removes the relevant excess without harming correctness, do not build repair-worker infrastructure.

### E4 — Mechanism decision

After E3a and, when justified, E3b/F0:

- first patches differ under the controlled path → prioritize syntax/type/API/project-generation mechanisms;
- first patches are similar but repair cost differs → prioritize diagnostic interpretation and repair amplification;
- audit/tool hygiene removes the ecological gap → treat tool policy as the primary practical intervention;
- comprehension remains unexplained → run a separately reviewed localization/familiarity treatment;
- similar interaction counts but input per round grows with scale → proceed toward Workstream H;
- no stable attribution → replicate only if the required sample remains scientifically and economically justified.

Do not convert these non-confirmatory pilots into a universal language ranking.

## Conditional Workstream F — Context containment and repair delegation

### F1 — Fresh inline versus fresh isolated repair

Run only if meaningful repair/context burden remains after deterministic tool hygiene.

Use the same model for orchestrator and worker first. The harness—not a prompt—must enforce separate processes/contexts and separate accounting. A deterministic controller runs builds/tests. The worker receives the bounded relevant workspace/diff plus diagnostics; the orchestrator receives only a frozen structured result unless a preregistered semantic escalation occurs.

Report total system cost, orchestrator-only cost, worker cost, raw diagnostic volume withheld from the orchestrator, correctness, repair attempts, and escalations.

### F2 — Persistent context only after F1

Only if F1 has auditable per-agent accounting and a meaningful containment result, add persistent inline and persistent delegated conditions. This tests cross-task context pollution.

Do not build recursive agents, dynamic routing, a generic multi-agent framework, or cheaper-worker variants before the same-model containment effect is understood.

## Workstream G — Registered small-repository replication

After causal attribution, register only the harness strata justified by E3/F:

- default ecological single-agent;
- hygienic single-agent;
- delegated repair, only if F1 is viable.

Do not pool them. Primary outcomes should include full-chain correctness, first-patch build/behavioral success, repair burden, paired total input, paired agent time, and per-task cumulative trajectories. V3 calibration observations remain excluded from formal estimates.

## Workstream H — Multi-scale context-pressure study

The original semantic-density hypothesis is tested only here.

Use a matched scalable architecture and preregister realistic source/working-set levels that create navigation and dependency obligations. Do not add inert filler. The evaluator must know the relevant files and symbols.

Use the controlled/hygienic tool path as the primary mechanism condition so a known restore/audit/compiler fixed cost does not swamp the language × scale estimate. A default ecological tool stratum may be secondary.

Measure candidate-visible repository and task-relevant tokens, retrieval recall/precision, architectural distance, interactions, input per interaction, unique/repeated source and tool exposure where available, maximum/terminal context, compaction, fresh versus persistent context, correctness, regressions, and total ecological cost.

A crossover is supported only if observed inside the preregistered scale range under genuine context pressure. Never extrapolate it from the current small-project gap.

## Evidence and claim boundaries

- V3 calibrations are non-counting and excluded from future formal estimates.
- E1/E2/E2a are descriptive mechanism-routing evidence, not causal language inference.
- E2 and E2a are separate ecologies and are not pooled.
- Unweighted command-cell ratios are not frequency-weighted v3 effects.
- The mechanical exposure envelope is not a mediation estimate or quantity to subtract from agent time.
- Audit warnings are repeated output lines, not independent defects.
- Aggregate input is trajectory usage, not unique source memory.
- The current repository does not test context-window fit.
- Fresh-per-task v3 cannot test cross-task context pollution.
- No current result establishes an intrinsic or universal F#, C#, model, or harness ranking.

## Research invariants

- Keep semantic tasks, starting states, evaluator, limits, and candidate authority matched within each treatment.
- Keep candidate agents blind to `AGENTS.md`, `PLAN.md`, hypotheses, prior outcomes, treatment labels, gold states, and hidden evaluator cases.
- Never expose credentials, parent repositories, unrelated host files, future gold, or evaluator cases.
- Record every attempt; never silently replace an ambiguous or potentially billable request.
- Keep scientific specification, runner, environment, model, effort, schedule, and attempt identities separate.
- Separate source exposure, model output, tool feedback, total input, direct tool time, orchestrator cost, worker cost, and end-to-end cost.
- Unsupported telemetry is null/unavailable, never zero.
- Preserve immutable E1/E2/E2a artifacts; corrections belong in addenda or new reports.

## Autonomous stopping rules

- The next autonomous task is E3a scientific specification, fixtures/identities, independent review, clean freeze, and exact-commit CI only.
- It may not execute the pilot or invoke a model automatically.
- After two failures of one apparatus class, stop and report instead of adding another compatibility or recovery layer.
- Stop before changing candidate-visible semantics, model/prompt/task/evaluator, tool-feedback policy, harness memory/routing, or another frozen scientific condition without reviewed authorization.
- Prefer deterministic tool hygiene before multi-agent infrastructure.

## Overall sequence

```text
E1/E2/E2a evidence — complete
  -> E3a controlled first-patch and bounded-repair specification/pilot
  -> E3b/F0 deterministic tool-hygiene policy pilot when justified
  -> E4 mechanism decision
  -> F1 fresh isolated repair only if hygiene is insufficient
  -> F2 persistent context only if F1 works
  -> G registered small-repository replication by named harness stratum
  -> H medium/large language × context-pressure study
```
