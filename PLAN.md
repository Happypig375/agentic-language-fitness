# Research plan

This is the canonical continuation plan. Workstream D v3 is closed at its preregistered calibration stop; no further v3 model run is authorized.

## Scientific checkpoint — 2026-09-03

Completed:

- Workstreams A–C: accounting/provenance, variance-v2, the matched eight-task successor chain, and representation apparatus;
- Workstream D scientific design, remote high-memory runner, route shakedown, exact-commit CI, clean v3 freezes, and ten audited non-counting calibrations;
- v3 calibration disposition: H (`gpt-5.6-terra`, medium) saturated; M (`gpt-5.6-luna`, high) and L (`gpt-5.6-luna`, medium) were too easy in both primary and reverse order;
- every retained v3 calibration run was protocol-valid, accounting-valid, successful 8/8, and free of agent/evaluator failure.

V4–V13 remain apparatus-development history, not scientific families. Do not create v14. The reviewed runner/environment identity remains `runner-remote-highmem-local-egress-r1`; a new scientific question requires a new scientific specification, not another apparatus-number cascade.

## Interpretation of the new results

### What is established

The v3 calibration achieved its operational purpose and triggered the frozen stop condition. The selected configurations cannot be differentiated by full-chain correctness on this eight-task benchmark. Formal v3 macroblocks 1–6 remain permanently unauthorized.

### What is not established

The ten runs were non-counting calibration observations. They provide five F#/C# pairs, only one H pair, and no preregistered language-effect test. They do not establish statistical significance, a universal language ranking, or an F# disadvantage.

### Exploratory signal that changes the next design

Across all five pairs, F# used more input tokens and more agent-process time:

- input-token F#/C# ratios: 1.307, 1.348, 1.359, 1.418, 1.455;
- agent-time ratios: 1.261, 1.416, 1.406, 1.411, 1.412;
- geometric means: 1.377 for input and 1.380 for agent time;
- M and L retained the same direction under reverse language order.

The corresponding geometric-mean ratios were 1.360 for output tokens, 1.306 for tool calls, and 1.903 for evaluator time. This is a strong hypothesis-generating signal that current model familiarity/tooling burden may dominate F# concision in the current small repository. It is not confirmatory evidence. See `docs/post-v3-interpretation-and-workstream-e-design-2026-09-03.md`.

## Current decision

Proceed to **Workstream E: successful-chain cost replication**, by design and review first.

Do not make the benchmark harder or lower capability merely to force failures. All-success paired chains are useful for the central cost question because both languages receive equal task exposure. A separate capability-boundary study may later investigate failure thresholds.

No paid/model run is authorized until the Workstream E design is independently approved, measurement gaps are closed, the new scientific specification is implemented and reviewed, CI is green, and a clean freeze exists.

## Immediate continuation order

### E0. Independently review the successor design

Review `docs/post-v3-interpretation-and-workstream-e-design-2026-09-03.md` for:

- the distinction between operational, exploratory, and confirmatory significance;
- cost-focused use of a correctness-saturated chain;
- practical-equivalence margin;
- configuration strata and paired estimands;
- sample-size/precision adaptation;
- task-level reporting and early-stop handling;
- ecological language-toolchain versus controlled-core interpretation;
- mechanism-study ordering.

Close every P1/P2 finding before implementation. This is the next bounded task.

### E1. Close measurement/reporting gaps without changing candidate semantics

Before freezing a new scientific cell:

1. add deterministic task-level and cumulative cost tables/curves to tracked reports;
2. treat zero file-read/revisit values as unsupported unless a curated real-event fixture demonstrates parser coverage; prefer null/unavailable over false precision;
3. add model-free repeated build/evaluator timing for every F#/C# benchmark stage;
4. record candidate-visible source bytes, lines, lexical units, files, tokenizer-proxy counts, and diffs at each stage;
5. audit language-specific task obligations, especially F# project-file/compile-order work in Tasks 007–008;
6. preserve the distinction between model compute, ecological toolchain cost, and total wall time.

Do not add syscall tracing, another remote route, or another apparatus version unless independent review finds the simpler event/reporting path insufficient.

### E2. Freeze a new scientific specification, not v14

Tentative scientific family ID: `successful-maintenance-cost-v1`.

Reuse the existing reviewed runner and environment profile if their candidate-visible identity remains exact. The formal family uses:

- canonical descriptive representation only;
- F# versus C# on the eight-task inherited chain;
- H/M/L as separate configuration strata;
- fresh process/container per task and inherited candidate workspace;
- calibration observations excluded from formal estimates;
- a new immutable, counterbalanced schedule.

Primary outcomes:

1. paired log ratio of full-chain input tokens;
2. full-chain correctness reported separately;
3. paired log ratio of agent-process wall time.

Predeclare a reviewed practical-equivalence region, provisionally F#/C# = 0.90–1.10. Use two-sided inference.

### E3. Collect a registered replication/precision stage

After independent review, implementation, green CI, and clean freeze:

- complete six paired blocks per configuration;
- use all six H/M/L order permutations;
- balance language order 3/3 within each configuration;
- total: 18 pairs and 36 language runs;
- complete the stage regardless of observed language direction;
- retain every attempt and preserve/audit raw evidence.

After all stage-1 runs are complete, a preregistered blinded calculation may use within-configuration dispersion only—not the mean or sign—to decide whether precision requires extension to a maximum of 12 pairs per configuration. The exact rule and multiplicity handling must be frozen in advance.

Correctness failures remain valid outcomes. If one language stops early, report terminal-stop cost and common-exposure-prefix cost rather than treating the failed run as cheaper success.

### E4. Produce the Workstream E report

Report:

- configuration-specific paired input/time ratios and uncertainty;
- full-chain success and task survival;
- per-task/cumulative trajectories and chain-position interaction;
- language-order, chronological, provider, and configuration diagnostics;
- output/reasoning/tool/compiler/test decomposition;
- model-free F#/C# evaluator/build baseline;
- source-representation metrics;
- practical-equivalence classification;
- whether the observed v3 direction replicated in new formal data.

Do not pool v3 calibration, difficulty-v1, variance-v2, historical Luna, or retired apparatus attempts into formal Workstream E estimates.

## Decision after Workstream E

### F# cost penalty replicates

Prioritize mechanism identification:

1. decompose cost by task and tool/compile/test behavior;
2. run a matched documentation/familiarity intervention, using an F# primer and size-matched C# control;
3. compare fresh-context and persistent-context regimes;
4. create one medium-scale matched repository with real modules before creating several families;
5. test whether the F#/C# ratio shrinks, persists, or reverses with repository size and maintenance depth.

The practical conclusion would be limited to the tested model/scaffold/environment: current agents are more economical in C# on this small benchmark. It would not falsify a future or large-repository semantic-density crossover.

### Signal disappears

Treat the v3 pattern as a calibration cluster. Re-estimate stochastic/provider variance and continue only if the required sample is scientifically and economically justified. A valid outcome is that scaffold/trajectory variance dominates language.

### Large language × configuration interaction

Make model capability/training familiarity central. Report stratified effects; do not publish a pooled language ranking.

### Toolchain difference explains most wall time but not tokens

Separate ecological language-stack cost from model-compute cost. Follow with a controlled-core task family that neutralizes project-file and compiler obligations only if that mechanism question is worth the additional complexity.

## Longer-term approach

1. **Replicate cost** on successful fixed-exposure chains.
2. **Explain cost** through model familiarity, compiler/tooling, source representation, task obligations, and navigation/reasoning behavior.
3. **Test scale** with one medium matched repository and a longer maintenance history.
4. **Test memory** with fresh versus persistent agent contexts.
5. **Generalize cautiously** to another language or scaffold only after the F#/C# mechanism is understood.
6. **Publish a mechanism map**, including negative or reversed findings, rather than advocacy for F# or any universal best language.

## Stop and anti-overengineering rules

- Preserve the v3 evidence; do not reopen its blocked formal schedule.
- Do not create v14 or another route/runner layer for a scientific-analysis change.
- The next autonomous task is only E0 independent design review.
- After two failures of the same apparatus class, stop and report rather than building another recovery subsystem.
- Stop immediately before any candidate-visible or scientific-treatment change not covered by an approved specification.
- No paid/model call until E0–E2 are complete and cleanly frozen.
