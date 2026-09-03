# Post-v3 causal attribution and successor design

**Date:** 2026-09-03  
**Status:** design draft for independent review; no paid/model run is authorized.

## Evidence boundary

Workstream D v3 produced ten preregistered, non-counting calibration runs over the eight-task descriptive F#/C# chain. Every retained run was protocol-valid, accounting-valid, successful 8/8, and free of terminal agent/evaluator failure. Across the five F#/C# pairs, F# used more total input, output, tool calls, and agent-process time, with geometric-mean F#/C# ratios near 1.38 for input and agent time.

Those totals are an **ecological trajectory-cost signal**, not an explanation. They do not distinguish:

- static source/context size;
- first-pass generation ability;
- syntax/type/API error rate;
- compiler and test feedback loops;
- project-system/toolchain obligations;
- model familiarity and exploratory behavior;
- repeated transcript/tool-output replay;
- context compaction or loss;
- harness architecture.

The v3 observations remain non-counting and excluded from future formal estimates. They are appropriate for deciding what to measure next, not for claiming a language effect.

## Critical interpretation correction

The current benchmark launches a **fresh candidate process and conversation for every maintenance task** while retaining only repository state. Therefore:

- diagnostics and tool history from Task 001 do not occupy the model conversation for Task 002;
- v3 can reveal within-task interaction/repair amplification;
- v3 cannot test whether compile loops accumulate across an eight-task persistent orchestrator and degrade later strategic decisions;
- “long-horizon context pollution” requires a separate persistent-context treatment.

Also, total input tokens are not unique source tokens. In an agent loop, a faulty patch can cause compiler output, further tool calls, and repeated cached prefixes to be presented to later model calls. A generation problem may therefore appear predominantly as extra **input** cost.

The final descriptive snapshots are only about two thousand offline proxy tokens and are similar in size. This small benchmark does not meaningfully test whether F# fits a large repository into model memory better than C#.

## Causal model

The successor work treats total trajectory cost as the endpoint of several pathways:

```text
language
  ├─> source representation / tokenizer fertility ─────────────┐
  ├─> model familiarity / idiom recall ─> initial patch quality│
  ├─> syntax + type-system interaction ─> compiler diagnostics  │
  ├─> project/build obligations ────────> tool calls + latency   │
  └─> documentation/search needs ───────> inspections            │
                                                               v
failed or uncertain step -> more edits/builds/tests/tool output -> longer transcript
                                                               |
harness memory/routing -----------------------------------------┘
                                                               v
total input/output/time, context pressure, and final correctness
```

A language may have compact source yet cost more today because the model repairs it more often. Conversely, an agent-friendly harness may contain repair chatter outside the strategic orchestrator while still incurring total worker cost. Both are scientifically relevant, but they answer different questions.

## Workstream E: attribute the existing cost gap

Workstream E precedes a registered cost replication. Its purpose is to determine what the v3 totals actually measure and which causal experiment is justified.

### E0 — Independent review

Review this design before implementation. Close all P1/P2 findings concerning:

- separation of comprehension, generation, repair, toolchain, and memory effects;
- use of non-counting v3 traces for mechanism discovery only;
- diagnostic classification and unsupported telemetry;
- controlled task-state construction;
- harness-routing estimands;
- anti-overengineering and stop rules.

No model call is authorized by this draft.

### E1 — Archive-only forensic attribution

Use the preserved raw v3 trajectories; do not issue new model requests. Add a deterministic, transcript-redacted analysis command/report that records, per task and run:

1. **Command classes:** source inspection, search, edit/patch, build, test/run, project configuration, environment, and other.
2. **Compilation:** number of build attempts, first-attempt success, first clean build, nonzero exits, and time to first clean build.
3. **Diagnostics:** compiler error/warning codes; diagnostic byte/line/offline-token counts; categories such as parse/indentation, type/inference/overload, pattern matching, missing symbol/API, project/compile order, nullability, and unclassified.
4. **Repair:** edits after failed builds/tests, build–edit cycles, test–edit cycles, and commands before/after first clean build.
5. **Testing:** behavioral and structural check attempts, failures, and output volume.
6. **Trajectory volume:** command output bytes, event bytes, agent-message/output tokens, reasoning tokens, total input/cached input, and task time.
7. **Source evolution:** files, bytes, lines, lexical units, proxy tokens, project-file edits, and diff metrics at each task boundary.
8. **Missingness:** mark per-model-call usage, peak context, compaction, and unique source exposure unavailable unless actually exposed. Never infer them from aggregate totals.

The report must preserve only derived counts, diagnostic codes/categories, hashes, and redacted excerpts needed to validate classification. Raw transcripts remain outside Git.

#### Attribution signatures

Interpret the forensic report through preregistered signatures rather than a single correlation:

| Candidate cause | Expected signature |
|---|---|
| Static context size | Similar interaction counts and first-pass accuracy, but larger input per comparable model/tool cycle, increasing with source size/stage |
| First-pass output ability | Lower first-build success, more initial patch/output tokens, and language-skewed syntax/type/API diagnostics |
| Repair amplification | More failed builds/tests, edit–build cycles, diagnostic volume, cached input, and commands after the first patch |
| Model familiarity/comprehension | More inspection/search/reasoning before the first edit even when first compilation succeeds |
| Toolchain/project obligations | Extra project-file operations or successful build/evaluator latency, concentrated in tasks such as the multi-file refactor |
| Context pollution | Cannot be established from fresh-per-task v3; requires the persistent-context experiment below |

The first report is descriptive and causal-hypothesis generating. It must not use post-hoc p-values to declare a mechanism.

**E1 exit:** every retained v3 task has an auditable command/diagnostic/repair classification; unsupported fields are null; the report identifies which mechanisms are observable and which require new treatments.

### E2 — Model-free language/toolchain baseline

Under the exact pinned environment, repeatedly build and evaluate every F#/C# baseline and gold stage. Record cold and warm distributions for:

- restore/build/evaluator wall time;
- project-file parsing and compilation;
- emitted warnings;
- files/modules compiled;
- output volume;
- final artifact size where useful.

This estimates ecological toolchain cost independently of model behavior. Do not subtract it mechanically from agent time: compile latency can alter agent decisions and retry behavior. Report it as an explanatory pathway.

Audit candidate-visible obligations task by task. In particular, record that F# multi-file compile order may require explicit project-file edits while ordinary C# SDK source discovery does not. Decide whether the primary estimand is:

- **ecological language-stack cost** (language plus idiomatic toolchain obligations), or
- **controlled-core representation cost** (project mechanics neutralized).

The first remains the main practical question; a controlled-core variant is a later mechanism treatment.

### E3 — Minimal controlled mechanism pilot

Only after E1–E2 and review, define a new scientific specification using matched **gold predecessor snapshots** so each task starts from identical intended state rather than inherited candidate drift. Use one preregistered model/scaffold configuration initially and a small task set spanning simple change, type/validation logic, and multi-file/API work.

Evaluate three modes:

1. **Comprehension/localization:** inspect source and produce a structured list of relevant files/symbols, invariants, and planned changes; no editing or compiler feedback. Score against a frozen language-neutral obligation map.
2. **One-shot patch:** permit source inspection, then exactly one patch; no compile-and-repair loop. Measure output/reasoning, first-pass build, behavioral correctness, and diagnostic categories.
3. **Monolithic agentic repair:** the current inspect–edit–compile/test–repair loop. Measure total trajectory and repair amplification.

The contrasts answer different questions:

```text
comprehension mode      -> semantic recovery / localization
one-shot mode           -> generation and first-pass language ability
full agent mode         -> ecological cost after feedback and repair amplification
full minus one-shot     -> approximate repair-loop contribution (descriptive, not literal subtraction of independent components)
```

Do not run a large factorial initially. Use a bounded pilot to choose the next causal treatment and derive variance. Stop after two repeated apparatus failures of one class.

### E4 — Causal decision gate

After E1–E3:

- **F# excess dominated by failed compilation/type/syntax repair:** prioritize compiler-feedback and isolated-repair harness experiments.
- **F# excess dominated by pre-edit inspection/reasoning with similar first-pass accuracy:** prioritize model-familiarity/documentation and retrieval interventions.
- **Gap concentrated in project-file/build obligations:** separate ecological and controlled-core studies.
- **Similar interactions but larger per-cycle input growing with stage:** prioritize repository-scale context experiments.
- **No stable attribution:** replicate only if the required sample remains scientifically and economically worthwhile; otherwise publish the ambiguity and apparatus limits.

## Workstream F: test context containment and repair delegation

This workstream is conditional on E showing meaningful repair/tool-output amplification. It is a **harness experiment**, not part of the pure language treatment.

### Why routing matters

A monolithic persistent agent may accumulate raw compiler diagnostics, test output, failed patches, and repair reasoning. A repair worker can keep this material out of the strategic orchestrator’s context. That may improve later decisions even if total system tokens do not fall.

A prompt telling an agent to “use a subagent” is not sufficient for causal inference. The harness should enforce separate processes/contexts and account for each independently.

### Initial routing design

Use the same model for orchestrator and repair worker first, so routing is varied without simultaneously changing model capability. Compare a compact 2 × 2 design:

- memory: fresh orchestrator per task vs persistent orchestrator across the chain;
- repair routing: inline/monolithic vs isolated repair worker.

This yields:

| Condition | Meaning |
|---|---|
| Fresh + inline | Current benchmark baseline; within-task repair only |
| Fresh + delegated | Tests within-task context containment |
| Persistent + inline | Tests cumulative tool/repair pollution and long-horizon degradation |
| Persistent + delegated | Tests whether isolated repair preserves strategic context |

In the delegated condition:

1. the orchestrator understands the task and produces the initial implementation;
2. a deterministic controller runs build/tests;
3. on failure, an ephemeral worker receives the current workspace or relevant files/diff, the task contract, and raw diagnostics;
4. the worker has a frozen small repair budget;
5. the orchestrator receives only a structured summary: pass/fail, diagnostic classes, files changed, tests run, and unresolved semantic issues;
6. raw repair transcripts and diagnostics are not inserted into the orchestrator context unless a preregistered escalation condition is met.

A later practical arm may use a cheaper repair model, but only after the same-model routing effect is understood.

### Routing outcomes

Report separately:

- total system input/output/time across orchestrator and workers;
- orchestrator-only input, output, and context/compaction telemetry where exposed;
- worker cost and number of repair attempts;
- raw diagnostic/tool-output volume withheld from the orchestrator;
- correctness, task survival, and late-chain decision quality;
- escalations and semantic regressions;
- F#/C# interaction with memory and routing.

A useful routing result may be:

- lower orchestrator context and better late-task decisions;
- unchanged or higher total system cost;
- a smaller F#/C# gap in the orchestrator but a persistent gap in total worker cost.

That would show mitigation of strategic-context pollution without pretending the underlying language/tooling burden vanished.

### Routing stop rules

Do not build a general multi-agent framework. Implement only the minimal explicit controller needed for the four reviewed conditions. Reuse the existing runner/environment. If separate per-agent usage cannot be audited, stop rather than inferring it. No recursive subagents, dynamic model routing, or autonomous planner hierarchy is authorized in the first study.

## Workstream G: registered ecological cost replication

A registered successful-chain cost replication remains useful, but it follows causal telemetry rather than preceding it.

Use canonical descriptive F#/C# repositories and configuration-specific strata. Primary outcomes should include:

1. full-chain correctness;
2. paired full-chain total input under the frozen harness;
3. first-pass compile rate and repair-cycle burden;
4. paired agent-process time;
5. per-task/cumulative trajectory curves.

Total input is interpreted as **ecological model input processed over the trajectory**, not unique context size. Predeclare a practical-equivalence margin only after review of the mechanism metrics. Keep v3 calibration excluded.

If a delegated harness becomes the practical target, report it as a separate harness stratum rather than silently replacing the monolithic baseline.

## Workstream H: test the original context-density hypothesis at scale

The current repository is too small to test whether concise source preserves agent memory. Build one medium matched repository before creating many repository families. Pilot multiple repository/context sizes until retrieval or compaction pressure is observable.

Measure:

- repository and candidate-visible token size;
- relevant-file/symbol recall and precision;
- unique versus repeated source/tool-output exposure where measurable;
- maximum/terminal orchestrator context and compaction events where exposed;
- fresh versus persistent context;
- monolithic versus delegated repair;
- task success and cost as maintenance depth grows.

The predicted semantic-density crossover is supported only if F# becomes relatively cheaper or more reliable as repository/context pressure increases after repair/tooling/familiarity pathways are controlled or modeled. A small-source one-shot cost difference cannot establish that claim.

## Overall next-step sequence

```text
E0 independent review
  -> E1 forensic attribution of existing v3 traces
  -> E2 model-free toolchain/obligation baseline
  -> E3 bounded comprehension / one-shot / repair pilot
  -> E4 mechanism decision
  -> F harness memory/routing experiment when justified
  -> G registered ecological cost replication
  -> H medium-scale context-pressure experiment
```

## Scientific claims permitted by possible outcomes

- **More F# repair loops:** current models have greater first-pass or toolchain difficulty in F# under the tested setting.
- **More F# pre-edit exploration:** model familiarity or semantic recovery is a leading mechanism.
- **Delegation helps orchestrator but not total cost:** context containment improves strategic agency while repair burden remains real.
- **F# gap shrinks under persistent delegated work or at larger scale:** harness/context interactions matter and simple small-task rankings are misleading.
- **F# remains costlier across modes and scale:** current language/tool/model ecology favors C# under those tested conditions.
- **No stable difference:** stochastic/configuration effects dominate language in the measured regime.

None supports a universal language ranking without broader models, scaffolds, repositories, and time periods.

## Gate

The next bounded task is an **independent review of this causal-attribution design**. After approval, implement only E1’s deterministic archive analyzer/report and E2’s model-free timing/source audit. No new model call, subagent framework, or scientific cell is authorized yet.