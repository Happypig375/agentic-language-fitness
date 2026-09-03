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

The final source snapshots are small and similarly sized—roughly two thousand offline proxy tokens and two or three source/project files. Repository capacity was not a meaningful limiting factor. The agent could inspect the whole project without choosing among a large set of distant modules, although the current telemetry does not prove that every file was included in every model request.

### Small-repository intercept versus context-scale slope

Use the following as a conceptual decomposition, not a claim that cost is literally linear:

\[
C_L(S) = A_L + B_L S,
\]

where:

- `C_L(S)` is agent cost for language `L` at repository/context scale `S`;
- `A_L` is the small-project overhead from model familiarity, first-pass generation, compiler/type interaction, project mechanics, repair behavior, and fixed toolchain cost;
- `B_L` is the marginal cost of recovering and maintaining additional source, dependencies, tool history, and architectural state as the relevant working set grows.

The current small, correctness-saturated benchmark primarily provides exploratory evidence about the **intercept**:

\[
A_{F\#} > A_{C\#}
\]

under the tested models, scaffold, tasks, and .NET ecology. It does not estimate either language's scale slope. In particular, it does not establish whether:

\[
B_{F\#} < B_{C\#},\quad B_{F\#} = B_{C\#},\quad\text{or}\quad B_{F\#} > B_{C\#}.
\]

A delayed semantic-density crossover remains possible if F# has a higher fixed overhead but a lower marginal context/recovery cost. In the simple conceptual model, the crossover would occur at:

\[
S^* = \frac{A_{F\#}-A_{C\#}}{B_{C\#}-B_{F\#}},
\]

but no crossover may be reported from extrapolation. It must be observed or tightly bounded in a preregistered scale experiment with real retrieval, context, or compaction pressure.

The tasks being easy enough for every retained run to succeed is useful for **equal-exposure cost measurement**: both languages completed the same eight changes, so neither appears cheaper because it failed early. It is not evidence that easy tasks inherently make F# expensive. Rather, the lack of context pressure gives source compactness little opportunity to offset familiarity, generation, repair, and tooling overhead.

Accordingly, maintain two separate questions:

1. **Small-repository ecological cost:** which language currently costs more when the whole relevant project is comfortably manageable and both chains succeed?
2. **Scale-dependent context efficiency:** how does the relative cost and reliability change as repository size, relevant working set, persistent history, retrieval burden, and compaction pressure grow?

Workstream E attributes the first question's overhead pathways. Workstream H estimates the second question's language-by-scale interaction and tests for a crossover.

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

Treat this as attribution of the current small-repository overhead `A`, not yet as a test of the scale-dependent term `B`.

A registered successful-chain cost replication remains valuable, but only after the measurement can explain what its total-token endpoint contains. A repository-scale experiment remains necessary even if the small-repository penalty replicates.

No paid/model run is authorized until the causal-attribution design is independently approved, archive-only and model-free analyses are complete, and any new scientific specification is reviewed and cleanly frozen.

## Immediate continuation order

### E0. Independently review the causal-attribution design

Review:

```text
docs/post-v3-interpretation-and-workstream-e-design-2026-09-03.md
```

Review especially:

- distinction between unique source context, generated output, tool feedback, and replayed transcript;
- distinction between small-repository intercept and context-scale slope/crossover;
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
- interaction count and input/output per comparable interaction where the event schema permits it;
- unsupported fields as null, not zero.

Do not infer per-model-call usage, peak context, compaction, unique source exposure, or literal file-read counts unless the raw schema exposes them and fixtures validate the parser.

The report must distinguish these signatures:

- lower first-build success and language-skewed diagnostics → generation/syntax/type mechanism;
- more pre-edit inspection/reasoning with similar first-build success → familiarity/comprehension mechanism;
- more failed build/test loops and cached input → repair amplification;
- extra project-file work or successful compiler latency → ecological toolchain mechanism;
- similar interactions but larger input per comparable cycle increasing with stage → static/context-size candidate;
- cross-task context pollution → not identifiable from v3.

The stage trend is descriptive only. Because the current project remains tiny at every stage, a growing per-task gap cannot by itself estimate the repository-scale slope `B`.

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

The comprehension condition estimates small-project semantic recovery, not context-window pressure. It becomes a context-density test only when repeated at preregistered repository/working-set scales in Workstream H.

### E4. Make the mechanism decision

- Repair errors dominate → test compiler-feedback containment and repair delegation.
- Pre-edit exploration dominates → test documentation/familiarity and retrieval support.
- Project/toolchain obligations dominate → retain ecological study and add a controlled-core variant only if worthwhile.
- Input per cycle grows with source stage despite similar behavior → treat it as a candidate scale mechanism, then test it under real repository pressure in Workstream H.
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

This workstream tests transcript containment, not source semantic density by itself. A smaller persistent-orchestrator F#/C# gap under delegation would show that repair history mediates part of the ecological gap; it would not establish a source-size crossover.

### Anti-overengineering constraint

Do not construct a general multi-agent framework. Implement only the explicit controller required for the four conditions. Reuse the current remote route and runner. If per-agent accounting cannot be audited, stop rather than infer it. No recursive agents or dynamic routing in the first experiment.

## Workstream G — Registered small-repository ecological cost replication

After Workstream E—and Workstream F if indicated—register a successful-chain cost study on the current benchmark.

This workstream estimates the current regime's paired small-project overhead. It should not be described as a test of which language uses a large context window more efficiently.

Primary outcomes should include:

1. full-chain correctness;
2. paired full-chain total input under the specified harness;
3. first-pass compilation and repair-cycle burden;
4. paired agent-process time;
5. per-task and cumulative trajectory curves.

Interpret total input as **model input processed over the complete trajectory**, not unique source context. Keep configuration strata separate. Exclude v3 calibration observations from formal estimates. A monolithic and delegated harness, if both studied, are separate harness strata rather than silently interchangeable implementations.

A replicated F# penalty would support `A_F# > A_C#` for the tested ecology. It would not determine the relative scale slopes or rule out a later crossover.

## Workstream H — Test the original context-density hypothesis across scale

The current repository is too small to test whether concise or semantically dense source preserves agent memory. Build one matched, scalable repository architecture before multiplying independent repository families.

### Scientific question

How does the paired F#/C# cost and reliability ratio change as the candidate-visible repository, task-relevant working set, architectural distance, persistent history, and tool-output burden grow?

The primary target is the **language × scale interaction**, not the average language coefficient.

### Scale design

Use several preregistered size/pressure levels generated from one reviewed matched architecture, for example:

1. current small baseline;
2. medium multi-module repository;
3. large repository with distributed but known relevant dependencies;
4. a pressure level at which retrieval omissions, compaction, or working-set tradeoffs are actually observed.

Do not inflate size with inert filler. Added modules must create realistic navigation or dependency obligations, and the evaluator must know the gold relevant-file/symbol set. Keep external behavior and task families matched across languages.

Pilot only enough to locate meaningful pressure levels, then freeze the scale points before formal collection. If every level remains comfortably retrievable with no compaction or relevant-context tradeoff, the study has not tested the context-density hypothesis and must not report a null crossover conclusion.

### Context regimes

Separate rather than silently combine:

- fresh context per task;
- persistent orchestrator context across the chain;
- inline repair;
- delegated repair when Workstream F establishes an auditable implementation.

Do not begin with the full factorial. First choose the smallest set needed to estimate the language-by-scale interaction under the practical baseline; add memory/routing strata only when justified by Workstream F.

### Required measurements

- candidate-visible repository and task-relevant token size;
- relevant-file and symbol retrieval recall/precision;
- architectural distance between task entry point and affected code;
- unique and repeated source/tool-output exposure where measurable;
- number of model interactions and input per interaction;
- maximum/terminal orchestrator context and compaction events where exposed;
- diagnostic/tool-output volume;
- fresh versus persistent context state;
- orchestrator and worker cost separately when delegated;
- task success, escaped regressions, and late-chain decision quality;
- total ecological cost as chain depth and scale grow.

Unsupported telemetry remains unavailable rather than estimated.

### Analysis

Use paired, configuration-specific models that expose the interaction, conceptually:

```text
log(cost) ~ language * log(repository_or_relevant_working_set_tokens)
            + task + order + time + configuration
            + (1 | matched_pair) + (1 | task_family)
```

Model correctness/retrieval with suitable hierarchical binary or ordinal models. Report observed scale-specific ratios and uncertainty before any fitted crossover.

A semantic-density crossover is supported only when:

- the language × scale interaction is stable across preregistered tasks/blocks;
- F# becomes relatively cheaper or more reliable as genuine context pressure increases;
- repair, toolchain, and familiarity pathways are measured or modeled;
- the estimated crossover lies inside the observed scale range or a narrowly supported interpolation range.

Do not claim a crossover from extrapolating the small-project intercept. If F# remains more expensive at all observed scales, report the range over which no crossover was found rather than claiming none can ever exist.

## Decision logic after causal work

### F# excess is mainly first-pass/repair difficulty

The practical conclusion is that current models/tooling make F# more expensive under the tested small-project ecology. Test documentation/familiarity and isolated repair before making a broader language claim.

### Delegation reduces orchestrator pollution but not total cost

Report that harness architecture can preserve strategic context while language-specific repair burden remains. Optimize orchestration separately from total compute.

### Delegation reduces both total and orchestrator cost

Treat repair routing as a major agentic-language interaction and include harness design in future language comparisons.

### F# relative cost improves with real scale/context pressure

The original context-density thesis gains support. Estimate the observed slope and crossover range rather than generalizing beyond the tested models, repositories, and harnesses.

### F# small-project gap persists without scale improvement

Conclude that model familiarity, generation, repair, and/or tooling dominate semantic-density benefits throughout the observed range. This remains conditional on the tested ecology.

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
  -> G registered small-repository ecological cost replication
  -> H preregistered multi-scale context-pressure experiment
```

## Evidence and claim boundaries

- V3 calibration is non-counting and excluded from future formal estimates.
- The five same-direction pairs are a strong exploratory small-repository signal, not confirmatory significance.
- Aggregate input tokens do not measure unique source memory.
- The current result primarily concerns fixed small-project ecological overhead, not the marginal context-cost slope.
- Easy/all-success tasks provide equal exposure for cost comparison but do not test capability boundaries or context pressure.
- Zero file-read/revisit values currently mean unsupported telemetry, not literal absence.
- Current fresh-per-task runs do not test cross-task context degradation.
- A later crossover remains possible but unestablished; it must be tested across observed pressure levels rather than inferred from source concision.
- No result establishes an intrinsic or universal F#, C#, model, or harness ranking.

## Stop and anti-overengineering rules

- Preserve the v3 evidence; do not reopen its blocked formal schedule.
- Do not create v14 for a scientific-analysis change.
- The next autonomous task is only E0 independent review.
- After two failures of one apparatus class, stop and report instead of building another recovery subsystem.
- Stop before changing candidate-visible semantics, model/prompt/task/evaluator, scientific estimands, or frozen conditions without approved design.
- No paid/model call until E0–E2 are complete and any E3 specification is independently approved and cleanly frozen.
