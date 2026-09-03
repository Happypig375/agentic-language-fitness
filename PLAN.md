# Research plan

This is the canonical continuation plan. Workstream D v3 is closed at its preregistered calibration stop. The next phase investigates **why** F# cost more in the exploratory calibration before registering a larger language-cost comparison.

## Scientific checkpoint — 2026-09-03

Completed:

- Workstreams A–C: accounting/provenance, variance-v2, the matched eight-task successor chain, and representation apparatus;
- Workstream D scientific design, remote high-memory runner, route shakedown, exact-commit CI, clean v3 freezes, and ten audited non-counting calibrations;
- v3 calibration disposition: H (`gpt-5.6-terra`, medium) saturated; M (`gpt-5.6-luna`, high) and L (`gpt-5.6-luna`, medium) were too easy in both primary and reverse order;
- all ten retained v3 calibration runs were protocol-valid, accounting-valid, successful 8/8, and free of terminal agent/evaluator failure;
- exploratory v3 finding: F# used more input tokens and agent-process time in all five F#/C# pairs, with geometric-mean ratios near 1.38.

V4–V13 remain apparatus-development history, not scientific families. Do not create v14. The reviewed runner/environment identity remains `runner-remote-highmem-local-egress-r1`. Scientific changes receive scientific-specification IDs; they do not trigger another runner-version cascade.

Latest validated pre-mechanism head `af91fffcda41f51030eba1bcb970fd64c570541c` passed Linux and Windows CI. Any new implementation still requires its own exact-commit green CI before use.

## Interpretation boundary

The v3 totals are **ecological trajectory costs**, not direct measurements of source compactness or model memory.

The current harness starts a fresh candidate process and conversation for every task. Therefore:

- tool and compiler history can inflate context within a task;
- that history does not carry from Task 001 into Task 002;
- v3 does not test cumulative cross-task orchestrator context pollution;
- persistent long-horizon memory and repair delegation require separate harness treatments.

Total input tokens can be inflated by generation problems. A faulty patch leads to diagnostics, more tool calls, and repeated cached history, so a syntax/type failure may appear mainly as extra input rather than only extra output.

The final source snapshots are small and similarly sized. The current benchmark does not meaningfully test whether F# fits a large repository into context better than C#.

## Current decision

Proceed to **Workstream E: causal attribution**, not directly to a larger cost replication.

The immediate question is whether the exploratory F# excess came from:

1. static source/tokenization size;
2. pre-edit comprehension or model familiarity;
3. first-pass generation/syntax/type/API errors;
4. compiler/test repair loops;
5. F# project/build obligations and toolchain latency;
6. repeated tool output and transcript replay;
7. a combination of these.

A registered successful-chain cost replication remains valuable, but only after the measurement can explain what its total-token endpoint contains.

No paid/model run is authorized until the causal-attribution design is independently approved, archive-only and model-free analyses are complete, and any new scientific specification is reviewed and cleanly frozen.

## Immediate continuation order

### E0. Independently review the causal-attribution design

Review:

```text
docs/post-v3-interpretation-and-workstream-e-design-2026-09-03.md
```

Review especially:

- distinction between unique source context, generated output, tool feedback, and replayed transcript;
- fact that v3 is fresh-per-task and cannot establish cross-task context pollution;
- diagnostic and command classification;
- controlled use of gold predecessor snapshots;
- comprehension, one-shot, and full-repair modes;
- persistent-orchestrator and delegated-repair design;
- total-system versus orchestrator-only cost;
- anti-overengineering and stopping rules.

Close every P1/P2 finding before implementation. This is the next bounded task.

### E1. Forensically attribute the existing v3 trajectories

Use only the preserved raw v3 archive. Do not issue a model request.

Implement a deterministic, transcript-redacted analyzer that reports per task and run:

- source inspection/search/edit/build/test/project/environment command classes;
- build attempts, first-pass success, first clean build, and nonzero exits;
- compiler diagnostic codes and categories;
- diagnostic/tool-output byte, line, and offline-token volume;
- edit–build and test–edit repair cycles;
- commands and time before/after first clean build;
- output/reasoning/input/cached-input totals;
- source files, bytes, lines, proxy tokens, project-file edits, and diffs at task boundaries;
- unsupported fields as null, not zero.

Do not infer per-model-call usage, peak context, compaction, unique source exposure, or literal file-read counts unless the raw schema exposes them and fixtures validate the parser.

The report must distinguish these signatures:

- lower first-build success and language-skewed diagnostics → generation/syntax/type mechanism;
- more pre-edit inspection/reasoning with similar first-build success → familiarity/comprehension mechanism;
- more failed build/test loops and cached input → repair amplification;
- extra project-file work or successful compiler latency → ecological toolchain mechanism;
- similar interactions but larger input per comparable cycle increasing with stage → static/context-size candidate;
- cross-task context pollution → not identifiable from v3.

**Exit:** all retained v3 tasks have auditable command/diagnostic/repair classifications and an explicit observable/unobservable ledger.

### E2. Establish model-free toolchain and source baselines

Under the pinned environment, repeatedly build and evaluate each F#/C# baseline and gold stage. Record cold/warm timing, output volume, warnings, files/modules compiled, and project-file obligations.

At every stage record:

- source files, bytes, lines, lexical units, and tokenizer-proxy counts;
- project-file changes;
- diff size;
- task-specific obligations.

Treat this as explanatory ecological cost. Do not mechanically subtract it from agent time, because compiler latency can change agent behavior.

Explicitly distinguish:

- **ecological language-stack cost:** idiomatic F#/C# plus their real .NET project/tooling behavior;
- **controlled-core representation cost:** project mechanics neutralized in a later treatment.

### E3. Run a bounded causal mechanism pilot only when E1–E2 justify it

Create a new reviewed scientific specification using matched gold predecessor snapshots, one preregistered model/scaffold configuration, and a small task subset spanning simple, type/validation, and multi-file/API work.

Compare:

1. **Comprehension/localization:** structured relevant files/symbols/invariants/plan; no edits or compiler feedback.
2. **One-shot patch:** source inspection and one patch; no compile-and-repair loop.
3. **Monolithic full agent:** normal inspect–edit–compile/test–repair.

This separates semantic recovery, first-pass output ability, and repair amplification. Use the pilot only to choose the next causal treatment and estimate variance; do not build a large factorial.

### E4. Make the mechanism decision

- Repair errors dominate → test compiler-feedback containment and repair delegation.
- Pre-edit exploration dominates → test documentation/familiarity and retrieval support.
- Project/toolchain obligations dominate → retain ecological study and add a controlled-core variant only if worthwhile.
- Input per cycle grows with source stage despite similar behavior → prioritize repository-scale context pressure.
- No stable attribution → replicate only if the required sample remains worthwhile; otherwise report ambiguity and measurement limits.

## Workstream F — Context containment and repair delegation

Run only if Workstream E shows meaningful repair/tool-output amplification.

### Scientific question

Can an explicit harness keep compiler/test repair chatter out of the strategic orchestrator’s context, and does this change later decision quality or the F#/C# cost ratio?

A routing prompt alone is insufficient. The harness must enforce and separately account for contexts.

### Minimal 2 × 2 harness design

Factors:

- memory: fresh orchestrator per task versus persistent orchestrator across the chain;
- repair routing: inline/monolithic versus isolated repair worker.

Conditions:

| Condition | Purpose |
|---|---|
| Fresh + inline | Existing within-task baseline |
| Fresh + delegated | Tests within-task context containment |
| Persistent + inline | Tests cumulative cross-task tool/repair pollution |
| Persistent + delegated | Tests whether repair isolation preserves strategic context |

Use the same model for orchestrator and worker first. Varying worker model is a later practical intervention.

In delegated runs:

1. the orchestrator interprets the task and makes the initial implementation;
2. a deterministic controller runs build/tests;
3. an ephemeral worker receives the current workspace or relevant files/diff plus raw diagnostics;
4. the worker receives a small frozen repair budget;
5. the orchestrator receives only a structured repair summary unless a preregistered semantic escalation occurs.

Report separately:

- total system cost;
- orchestrator-only cost and available context/compaction telemetry;
- worker cost;
- diagnostic/tool-output volume withheld from the orchestrator;
- repairs, escalations, correctness, task survival, and late-task decision quality;
- language × memory × routing interactions.

A delegated harness may improve orchestrator quality while increasing total cost. Both outcomes must remain visible.

### Anti-overengineering constraint

Do not construct a general multi-agent framework. Implement only the explicit controller required for the four conditions. Reuse the current remote route and runner. If per-agent accounting cannot be audited, stop rather than infer it. No recursive agents or dynamic routing in the first experiment.

## Workstream G — Registered ecological cost replication

After Workstream E—and Workstream F if indicated—register a successful-chain cost study.

Primary outcomes should include:

1. full-chain correctness;
2. paired full-chain total input under the specified harness;
3. first-pass compilation and repair-cycle burden;
4. paired agent-process time;
5. per-task and cumulative trajectory curves.

Interpret total input as **model input processed over the complete trajectory**, not unique source context. Keep configuration strata separate. Exclude v3 calibration observations from formal estimates. A monolithic and delegated harness, if both studied, are separate harness strata rather than silently interchangeable implementations.

## Workstream H — Test the original context-density hypothesis at scale

Build one medium matched repository before multiplying repository families. Pilot repository/context sizes until retrieval or compaction pressure is actually observable.

Measure:

- candidate-visible repository tokens;
- relevant-file/symbol retrieval recall and precision;
- unique/repeated source and tool-output exposure where measurable;
- maximum/terminal orchestrator context and compaction events where exposed;
- fresh versus persistent context;
- monolithic versus delegated repair;
- task success and cost as chain depth grows.

The semantic-density crossover hypothesis is supported only if F# becomes relatively cheaper or more reliable as context pressure increases after repair, tooling, and familiarity pathways are controlled or modeled.

## Decision logic after causal work

### F# excess is mainly first-pass/repair difficulty

The practical conclusion is that current models/tooling make F# more expensive under the tested ecology. Test documentation/familiarity and isolated repair before making a broader language claim.

### Delegation reduces orchestrator pollution but not total cost

Report that harness architecture can preserve strategic context while language-specific repair burden remains. Optimize orchestration separately from total compute.

### Delegation reduces both total and orchestrator cost

Treat repair routing as a major agentic-language interaction and include harness design in future language comparisons.

### Gap appears only under persistent or larger contexts

The original context-density thesis becomes central; move to the medium-repository scale study.

### Gap disappears after attribution controls

Treat v3 as a calibration cluster or toolchain artifact. Reframe toward configuration/harness sensitivity if that is the stable finding.

## Overall sequence

```text
E0 independent review
  -> E1 archive-only forensic attribution
  -> E2 model-free toolchain/source baseline
  -> E3 bounded comprehension / one-shot / repair pilot
  -> E4 causal decision
  -> F explicit memory/routing experiment when justified
  -> G registered ecological cost replication
  -> H medium-scale context-pressure experiment
```

## Evidence and claim boundaries

- V3 calibration is non-counting and excluded from future formal estimates.
- The five same-direction pairs are a strong exploratory signal, not confirmatory significance.
- Aggregate input tokens do not measure unique source memory.
- Zero file-read/revisit values currently mean unsupported telemetry, not literal absence.
- Current fresh-per-task runs do not test cross-task context degradation.
- No result establishes an intrinsic or universal F#, C#, model, or harness ranking.

## Stop and anti-overengineering rules

- Preserve the v3 evidence; do not reopen its blocked formal schedule.
- Do not create v14 for a scientific-analysis change.
- The next autonomous task is only E0 independent review.
- After two failures of one apparatus class, stop and report instead of building another recovery subsystem.
- Stop before changing candidate-visible semantics, model/prompt/task/evaluator, scientific estimands, or frozen conditions without approved design.
- No paid/model call until E0–E2 are complete and any E3 specification is independently approved and cleanly frozen.