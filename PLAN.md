# Research plan

This is the canonical continuation plan. Workstream D v3 is closed. Workstreams E1 and E2 are complete and accepted within their stated evidence boundaries. The current phase aligns those measurements before any new model-backed causal pilot.

## Scientific checkpoint — 2026-09-04

Completed and preserved:

- Workstreams A–C: accounting/provenance, `variance-v2`, the matched eight-task successor chain, and representation apparatus;
- Workstream D v3: reviewed remote runner, route shakedown, clean freezes, and ten audited non-counting calibrations;
- Workstream E1: archive-only forensic attribution over 10 runs and 80 tasks, report SHA-256 `644273ac0f25a32138d50d919ff15677b6ed9639a23198e0c719d154da94901d`;
- Workstream E2: model-free toolchain/source baseline over 18 states and 90 schedule entries, report SHA-256 `2e4381ab67dd4cc7aed24c323e8edbd30bf83dd29bafc58554615bcd6f24c49a`;
- exact-commit Linux and Windows CI for the E1 and E2 implementations and publications.

V4–V13 remain apparatus-development history, not scientific families. Do not create v14. Reuse `runner-remote-highmem-local-egress-r1` unless a separately reviewed candidate-visible change is necessary. Scientific changes receive scientific-specification IDs rather than runner-version numbers.

The authoritative synthesis and review is:

```text
docs/workstream-e1-e2-synthesis-review-2026-09-04.md
```

No model or paid run is currently authorized.

## What E1 and E2 now indicate

### Leading observed mechanism: first-pass/compiler-repair burden

E1 found:

- 25 observable failed candidate operations, all builds;
- 23 failed builds under F# versus 2 under C#;
- 17 conservative F# repair cycles versus 2 C# repair cycles;
- 17 identifiable F# first-post-edit build failures versus 2 C# failures, with 34 boundaries explicitly unavailable;
- all five committed project-file changes under F#;
- nearly all observed error diagnostics and repeated nullability warnings under F#;
- approximately twice the evaluator duration under F# in every configuration.

Observable pre-edit inspection/search differences were comparatively modest and cannot identify hidden reasoning or training familiarity. The present evidence therefore prioritizes first-pass generation, type/compiler interaction, repair amplification, and project/toolchain obligations.

Diagnostic occurrences are output-volume observations, not independent defects. Repeated warnings such as `FS3261` must not be counted as hundreds of distinct mistakes. Use failed operation episodes, unique diagnostic categories per episode, and repair transitions as the main units.

### Direct toolchain result: slower F# restore/build, near-parity built-program execution

E2 found source/token proxies near parity and built-program run ratios near 1.0. In its frozen offline environment, however:

- fresh restore paired F#/C# ratio: 8.403;
- fresh build ratio: 3.037;
- repeat build ratio: 3.117;
- fresh restore-through-evaluator composite: 4.490.

The repeat-build result is the cleanest direct compiler/toolchain signal because it excludes restore. Its mean absolute F#–C# gap was about 1.4 seconds per build. This can amplify repair-heavy trajectories but does not by itself explain hundreds of seconds of paired agent-process difference or any model-token difference.

E2 fresh restore is environment-specific. The network-disabled condition emitted 225 F# `NU1900` lines, indicating unavailable package-vulnerability data. The immutable E2 result remains valid for that ecology, but the 8.403 ratio must not be transported to v3 candidate behavior without matching command, package-cache, audit, and source/network conditions.

### Current bounded interpretation

The leading coupled pathway is:

```text
F# first-pass/type/project difficulty
  -> more failed builds and repair cycles
  -> more diagnostics, edits, commands, and model turns
  -> more input replay, output, and wall time

slower F# compiler/toolchain operations
  -> greater direct time per build/repair cycle
```

This is still descriptive routing, not a causal language effect. Static source size and executable runtime do not explain the observed gap. Training familiarity, unique source exposure, per-model-call context, and cross-task context pollution remain unidentified.

The v3 repository was only about two thousand proxy source tokens. It measures a local small-repository ecological gap, not context-window fitness or a language-by-scale slope. A semantic-density crossover can only be tested later under real retrieval, persistent-history, or compaction pressure.

## Current decision

Insert a mandatory model-free **E2a command/environment alignment** before E3.

The earlier plan moved directly from E2 to an E3 model pilot. Review found that this would carry two unresolved interpretation problems forward:

1. E2 restore was measured offline with F#-only `NU1900` output and may not match v3 audit/source reachability;
2. E2 used fixed command forms that may not match the build/restore/run commands actually used by v3 candidates.

E2a corrects those issues without a model call. Only after E2a is reviewed and green may E3 be specified, frozen, and separately authorized.

## Immediate continuation order

### E2a — Exact-command and environment-aligned model-free baseline

**This is the next bounded task. No model endpoint, candidate agent, or paid request is permitted.**

Use the preserved E1 raw archive and classifications to construct a redacted inventory of the bounded command-equivalence classes that actually occurred, by language, task, and configuration.

Required work:

1. Enumerate actual build, restore, run, test, project, and compound-command forms without publishing sensitive raw command text.
2. Collapse only variants with demonstrably equivalent command semantics. Benchmark every semantically distinct compiler/test form and every class with material exposure; do not reproduce incidental shell plumbing merely because its exact spelling differed.
3. Benchmark only materially observed forms against matched baseline/gold states.
4. Match the v3 toolchain, package cache, environment variables, build configuration, audit behavior, and source/network reachability as closely as can be demonstrated.
5. For restore-capable forms, include an otherwise matched `NuGetAudit=false` control to bound vulnerability-audit delay.
6. Keep the accepted offline E2 result separate; do not overwrite or pool it.
7. Report paired absolute seconds and output/diagnostic volume beside every ratio.
8. Compute a mechanical tool-exposure envelope using observed E1 invocation counts and model-free operation timings:

```text
estimated direct tool time(language)
  = sum(command-class count × matched model-free duration)
```

This is an explanatory timing counterfactual, not a subtraction from agent cost and not a mediation estimate.
9. Determine whether `NU1900` or equivalent audit output appeared in the v3 candidate command streams. Absence, presence, or unobservability must be explicit.
10. Preserve unsupported timing or command details as unavailable rather than guessing.

E2a exit criteria:

- exact command classes and frequencies reconcile to E1;
- candidate-aligned and audit-off conditions are explicit and reproducible;
- audit/network mismatch is either resolved or declared irreducible;
- direct tool-latency exposure is compared in absolute seconds with the observed agent-time gap;
- a report states which portion remains explainable only by model interaction/repair behavior;
- independent review and exact-commit Linux/Windows CI pass.

Stop after E2a publication. It does not authorize E3 execution.

### E3 — Bounded causal mechanism pilot

After E2a, create and independently review a new scientific specification. Use matched canonical gold predecessor snapshots so every language/mode begins from the same intended state.

#### Task set

Freeze a minimal mechanism-spanning set using E1/E2 evidence only:

- one simple/low-diagnostic additive task;
- one type or validation task with observed F# diagnostics;
- one multi-file/project/API task, normally Task 007 or 008.

Task selection is hypothesis-routing and the pilot is non-confirmatory. Do not choose tasks after observing E3 outcomes.

#### Configuration

Use one exact model/scaffold setting selected for **nondegenerate first-patch outcomes on the chosen tasks**, not merely the lowest monetary cost or the largest exploratory F#/C# gap. E1 makes M (`gpt-5.6-luna`, high) the provisional default: its observable F# first-post-edit builds were mixed at 10 successes, 3 failures, and 3 unavailable, whereas L was near a floor at 0 successes, 13 failures, and 3 unavailable; H had 6 of 8 boundaries unavailable. Confirm this choice against task-level evidence and current model preflight, document it before outcomes exist, and freeze it. Do not vary model, effort, and harness simultaneously.

#### Modes

1. **Comprehension/localization auxiliary arm**
   - controller-enforced read-only source access;
   - fixed structured response for relevant files/symbols, invariants, and required changes;
   - no build, test, execution, write, or repair feedback;
   - scored against a frozen blinded obligation map.

2. **One-shot patch primary arm**
   - same task and predecessor;
   - exactly one controller-recorded multi-file patch;
   - no candidate build/test feedback;
   - controller applies the patch once and runs the first external build/evaluator.

3. **Monolithic full-repair primary arm**
   - same initial conditions and controller-observed first patch/build boundary;
   - a small frozen inspect/edit/build/test/repair budget;
   - complete usage, diagnostics, commands, and outcomes retained.

The controller-defined first patch/build fixes E1’s 34 unavailable first-build boundaries.

#### Primary mechanism outcomes

- first-patch build success and behavioral success;
- failed-build episodes and unique diagnostic categories;
- repairs required to reach correctness;
- full-condition input/output/reasoning/tool use and wall time;
- paired absolute and relative cost by task family;
- structured comprehension/localization accuracy as a separate outcome.

Treat one-shot versus full repair as a **harness-policy contrast**, not a literal algebraic mediation decomposition. Removing feedback changes the model policy.

#### E3 gate

The E3 specification must predeclare task identities, sample size, model/effort, mode authority boundaries, patch format, external first-build definition, diagnostics, retries, inclusion, evidence retention, and stopping. Obtain independent review, clean freeze, and green exact-commit CI. A separate user/maintainer decision is required before any model call.

### E4 — Mechanism decision

After E3:

- failed first builds and repair cycles explain the gap → prioritize compiler-feedback containment and repair routing;
- comprehension/localization differs while first-pass builds do not → prioritize documentation/familiarity and retrieval support;
- project/toolchain exposure explains a substantial absolute share → retain an ecological study and add a controlled-core project treatment only if worthwhile;
- similar interactions but increasing per-cycle input with scale → proceed to context-pressure work;
- no stable attribution → replicate only if the required sample remains scientifically and economically justified.

Do not convert the non-confirmatory pilot into a language ranking.

## Conditional Workstream F — Context containment and repair delegation

Run only if E3 confirms meaningful repair/tool-output amplification.

### F1 — Fresh-context repair containment first

Compare:

- fresh orchestrator + inline repair;
- fresh orchestrator + isolated repair worker.

Use the same model for orchestrator and worker first. The harness—not a prompt—must enforce separate contexts and separate accounting. A deterministic controller runs the build/tests; the worker receives the current workspace or bounded relevant files/diff plus raw diagnostics; the orchestrator receives only a frozen structured result unless a preregistered semantic escalation occurs.

Report separately:

- total system cost;
- orchestrator-only cost;
- worker cost;
- diagnostic/tool-output volume withheld from the orchestrator;
- repair attempts, escalations, correctness, and regressions.

A result may preserve orchestrator quality while increasing total cost; both must remain visible.

### F2 — Persistent context only after F1 works

Only if F1 has auditable per-agent accounting and a meaningful containment result, add:

- persistent orchestrator + inline repair;
- persistent orchestrator + isolated repair worker.

This tests cross-task context pollution. Do not build a general multi-agent framework, recursive agents, dynamic routing, or a cheaper-worker arm before the same-model containment effect is understood.

## Workstream G — Registered small-repository ecological replication

After causal attribution—and Workstream F if indicated—register a successful-chain replication under explicitly named harness strata.

Primary outcomes should include:

1. full-chain correctness;
2. paired total input under the frozen harness;
3. first-pass build and repair-cycle burden;
4. paired agent-process time;
5. per-task/cumulative trajectory curves.

Interpret total input as model input processed over the trajectory, not unique source memory. Exclude v3 calibration observations from formal estimates. A monolithic and delegated harness are separate treatments, not interchangeable implementations.

## Workstream H — Multi-scale context-pressure study

The original semantic-density hypothesis is tested only here.

Build one matched scalable architecture and preregister size/pressure levels that create realistic navigation and dependency obligations. Do not add inert filler. The evaluator must know the relevant-file/symbol set.

Measure:

- candidate-visible repository and task-relevant token size;
- retrieval recall/precision and architectural distance;
- interaction count and input per interaction;
- unique/repeated source/tool-output exposure where available;
- maximum/terminal orchestrator context and compaction markers where exposed;
- fresh versus persistent context;
- inline versus delegated repair when Workstream F justifies it;
- correctness, regressions, late-chain decisions, and total ecological cost.

The primary target is language × scale. A crossover is supported only if observed inside the preregistered scale range under genuine context pressure. Never extrapolate it from the current small-project gap.

## Evidence and claim boundaries

- V3 calibrations remain non-counting and excluded from future formal estimates.
- E1/E2 are descriptive mechanism-routing evidence, not causal language inference.
- Aggregate input tokens are trajectory usage, not unique source exposure.
- The current small repository does not test context-window fit.
- E2 restore is an offline, audit-sensitive ecological result until E2a establishes transportability.
- E2 repeat-build latency is a real direct toolchain signal but does not by itself explain model-token usage.
- Compiler warning occurrences are not independent defects.
- Current fresh-per-task runs cannot establish cross-task context pollution.
- No current result establishes an intrinsic or universal F#, C#, model, or harness ranking.

## Research invariants

- Keep F# and C# semantic tasks, starting states, evaluator, limits, and candidate protocol matched within each treatment.
- Keep candidate agents blind to `AGENTS.md`, `PLAN.md`, hypotheses, prior outcomes, and treatment labels.
- Never expose gold data, hidden evaluators, credentials, parent repositories, or unrelated host files.
- Record every attempt and never silently replace a candidate or potentially billable request.
- Keep scientific-specification identity separate from runner/environment identity.
- Separate source exposure, model output, tool feedback, total input, toolchain time, orchestrator cost, worker cost, and end-to-end cost.
- Unsupported telemetry is null/unavailable, never a fabricated zero.

## Autonomous stopping rules

- The next autonomous task is only E2a implementation, review, report, and exact-commit CI.
- It may not continue into E3 specification or any model run automatically.
- After two failures of the same apparatus class, stop and report instead of adding another compatibility or recovery layer.
- Stop before changing candidate-visible semantics, model/prompt/task/evaluator, harness memory/routing, or a frozen scientific condition without reviewed authorization.
- Prefer bounded deterministic analysis and reuse of the existing runner over new infrastructure.

## Overall sequence

```text
E1/E2 evidence — complete
  -> E2a command/environment-aligned model-free correction
  -> E3 reviewed first-pass/full-repair mechanism pilot
  -> E4 mechanism decision
  -> F1 fresh repair containment; F2 persistent context only if justified
  -> G registered small-repository ecological replication
  -> H medium/large language × context-pressure study
```
