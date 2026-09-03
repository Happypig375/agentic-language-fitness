# Post-v3 interpretation and Workstream E successor design

**Date:** 2026-09-03  
**Status:** design draft for independent review; no paid/model run is authorized.

## Evidence boundary

Workstream D v3 performed ten preregistered **non-counting calibration runs** over the eight-task descriptive F#/C# chain:

- H: `gpt-5.6-terra`, medium reasoning — one F#/C# pair;
- M: `gpt-5.6-luna`, high reasoning — primary and reverse-order pairs;
- L: `gpt-5.6-luna`, medium reasoning — primary and reverse-order pairs.

All ten retained runs were protocol-valid, accounting-valid, successful 8/8, and free of agent/evaluator failures. Under the frozen v3 difficulty rule, H was saturated and M/L were too easy in both orders, so formal v3 macroblocks were correctly blocked. The calibration report and raw hashes remain authoritative.

These runs were not designated for language inference. They must not be pooled with future formal observations, described as a confirmatory experiment, or used to claim a universal language ranking.

## What is significant now

### Operational significance: yes

The calibration achieved its preregistered purpose. It shows that the eight-task chain cannot distinguish the selected Terra/Luna configurations by task survival or full-chain correctness: every retained run completed all tasks. The v3 difficulty-based formal schedule is therefore closed, not merely postponed.

### Confirmatory statistical significance: no

There are only five F#/C# pairs, H has no reverse-order replicate, the runs were explicitly non-counting, and no language-effect test over these calibration observations was preregistered. A minimal-assumption two-sided sign calculation for five same-direction pairs is `2 / 2^5 = 0.0625`; even that calculation is post hoc and does not turn calibration data into confirmatory evidence.

### Exploratory scientific signal: strong enough to redesign around

Although correctness was saturated, the cost outcomes were strikingly consistent:

| Configuration | Pair order | F# input | C# input | F#/C# input | F# agent s | C# agent s | F#/C# agent time |
|---|---|---:|---:|---:|---:|---:|---:|
| H | F# first | 940,493 | 719,615 | 1.307 | 633.6 | 502.4 | 1.261 |
| M | C# first | 1,205,991 | 894,451 | 1.348 | 816.9 | 576.8 | 1.416 |
| M | F# first | 1,151,370 | 847,098 | 1.359 | 806.6 | 573.5 | 1.406 |
| L | F# first | 1,115,697 | 786,572 | 1.418 | 671.5 | 476.0 | 1.411 |
| L | C# first | 1,099,273 | 755,512 | 1.455 | 677.5 | 479.8 | 1.412 |

Across the five pairs, the descriptive geometric-mean F#/C# ratios were:

- input tokens: **1.377** (observed range 1.307–1.455);
- agent-process wall time: **1.380** (1.261–1.416);
- output tokens: **1.360**;
- tool calls: **1.306**;
- evaluator wall time: **1.903**.

F# was higher in all five pairs for both input tokens and agent-process time. The M and L direction persisted under reverse language order. The signal therefore does not resemble the large order reversal seen in the earlier two-task `variance-v2` pilot, although five calibration pairs cannot estimate long-run stability.

This is hypothesis-generating evidence that, for the tested models, scaffold, small repository, and task chain, model familiarity/tooling burden may dominate F#'s source-level concision. It is evidence against the simple proposition “shorter source automatically means cheaper agents,” not evidence against every possible large-repository or future-model advantage for F#.

## Why correctness saturation should not end the language-cost study

The central research question is lifetime **agent cost conditional on maintaining correct software**, not solely the capability threshold at which agents fail. When both members of a pair complete the same eight tasks, total input, output, reasoning, tool, and time costs are directly comparable without early-stop censoring.

The v3 calibration rule treated all-success chains as “too easy” because Workstream D was designed as a difficulty-feasibility study. The new scientific specification should change the estimand rather than making tasks harder merely to manufacture failures.

A separate capability-boundary study may later lower model capability or strengthen tasks. It should not be mixed with the successful-maintenance cost study.

## Measurement issues to close before another model run

### Task-level trajectory reporting

The v3 tracked report preserves aggregate values but does not render task-by-task cost curves. Future reports must include per-task and cumulative input, output, reasoning, tools, agent time, evaluator time, compile/test activity, and source/diff metrics. The language-by-chain-position interaction is central to the “read many times” hypothesis.

### Navigation telemetry

All ten v3 reports record zero file reads and revisits despite 30–58 command events per run. This must be treated as **unsupported/unobserved telemetry**, not evidence that agents read no files. Before freeze, either:

1. validate a transcript-free parser against curated real command-event fixtures and report its measured coverage; or
2. change unsupported read/revisit fields to null/unavailable and remove them from primary/secondary estimands.

Do not add syscall tracing or another infrastructure layer unless the simpler event-level path is independently shown inadequate and the scientific value justifies the candidate-observable risk.

### Toolchain baseline

F# evaluator time was about 1.9× C# in every pair. Run repeated model-free build/evaluation timing at every benchmark stage under the pinned environment. Report this ecological toolchain cost separately from model-token cost; do not subtract it from agent time as though the two components were independent.

### Representation and obligation audit

Re-audit each task for language-specific obligations. In particular, F# multi-file compile ordering and explicit project-file edits may differ from C# SDK source discovery. The primary study may intentionally estimate the ecological **language + idiomatic toolchain** package, but it must say so. A later controlled-core variant may neutralize project-file obligations if the goal becomes syntax/type-system mechanism inference.

Record source bytes, lines, lexical units, tokenizer-proxy counts, files, and diff size at every stage. This establishes whether extra agent cost occurs despite a smaller representation or alongside a larger effective repository.

## Workstream E: successful-chain cost replication

### Scientific question

For a fixed eight-task inherited maintenance chain that current agents can complete, what is the paired F#/C# ratio in agent computation, and how does that ratio vary across the H/M/L capability configurations?

### Treatment scope

- canonical descriptive representation only;
- F# versus C#;
- the same eight candidate-visible task specifications and evaluator;
- the same reviewed remote runner and environment profile where still exactly pin-able;
- H/M/L retained as configuration strata, not pooled aliases;
- fresh candidate process/container per task with inherited repository state;
- calibration observations excluded from all formal estimates.

This is a new **scientific specification**, tentatively `successful-maintenance-cost-v1`; it is not apparatus v14. Reuse `runner-remote-highmem-local-egress-r1` unless an independently justified candidate-observable change is necessary.

### Primary outcomes

1. Paired log ratio of full-chain input tokens, `log(F#/C#)`.
2. Full-chain correctness/success, reported separately as a quality outcome.
3. Paired log ratio of agent-process wall time.

Input includes cached input as a component; cached input is never added twice.

### Secondary outcomes

- uncached and cached-input components;
- output and reasoning tokens;
- tool/command and compiler/test counts;
- evaluator, task-total, and run-total time;
- per-task and cumulative cost curves;
- source/diff metrics and classified failures;
- common-exposure-prefix cost if either member of a pair stops early.

### Practical interpretation

Predeclare a multiplicative practical-equivalence region of **0.90–1.10** for the F#/C# cost ratio. Report estimates and uncertainty rather than only null-hypothesis p-values:

- interval wholly above 1.10: materially higher F# cost in that tested cell;
- interval wholly below 0.90: materially lower F# cost;
- interval wholly within 0.90–1.10: practical equivalence;
- otherwise: inconclusive.

This margin is a scientific-design choice and must receive independent review before freeze.

### Formal schedule and sample-size adaptation

Start with the already understood six-permutation H/M/L macroblock structure, but generate a new immutable schedule and identifiers. Complete **six paired blocks per configuration** (18 pairs, 36 language runs), balancing language order 3/3 inside each configuration.

After those observations are complete and audited, a blinded precision calculation may use only within-configuration dispersion—not the direction or mean of the language contrast—to determine whether to extend to a preregistered maximum of **12 pairs per configuration**. The target is a configuration-specific 95% interval half-width no wider than approximately `log(1.10)`. The exact method, multiplicity policy, and maximum must be independently reviewed and frozen before collection.

There is no difficulty-based stop when all chains succeed. There is no early stop based on a favorable or unfavorable F#/C# direction.

### Analysis

- configuration-specific paired log-ratio estimates are primary;
- report a hierarchical/partial-pooling estimate only with the language × configuration interaction visible;
- include language order, chronological macroblock, and time as blocking/diagnostic variables;
- model task-level repeated observations with pair/run/task dependence;
- retain candidate failures as correctness outcomes and use common-exposure-prefix cost rather than rewarding early termination;
- use two-sided inference: the exploratory direction is opposite the motivating F# intuition and must not be converted into a post hoc one-sided hypothesis.

No universal language claim follows. The estimand is conditional on the exact model/scaffold/environment/benchmark family.

## Decision sequence after Workstream E

### If the F# cost penalty replicates

Treat the next question as mechanism identification:

1. decompose per-task compiler/test, reasoning, output, and tool-call burden;
2. run the model-free toolchain baseline;
3. test a matched documentation/familiarity intervention, with an F# primer and a size-matched C# control;
4. compare fresh-context and persistent-context regimes;
5. construct one medium-scale matched repository before multiplying repository families;
6. test whether the cost ratio shrinks, persists, or reverses as repository size and maintenance depth increase.

A replicated small-repository F# penalty would support the practical conclusion that current models are more economical in C# under these conditions. It would not falsify the possibility of a later semantic-density crossover.

### If the signal disappears

Conclude that the v3 pattern was a calibration cluster and that stochastic/provider variation remains dominant. Increase blocking or repetitions only if the required sample remains scientifically and economically worthwhile; otherwise reframe the contribution toward variance and configuration sensitivity.

### If configuration interaction is large

Make model capability/training familiarity central. Do not report a pooled language ranking. Select configuration strata for confirmatory work and consider a lower-effort/familiarity intervention only under a separately reviewed specification.

## Longer-term approach

1. **Replicate cost:** establish whether the 31–46% calibration pattern survives new formal data.
2. **Explain cost:** separate representation size, model familiarity, toolchain friction, reasoning, navigation, and compile/test loops.
3. **Test scale:** move from the current small three-file endpoint to a medium matched repository with real modules and a longer maintenance history.
4. **Test memory:** compare fresh-agent semantic recovery with persistent agent context.
5. **Generalize cautiously:** add another language or scaffold only after the F#/C# mechanism is understood.
6. **Publish a framework, not advocacy:** the final result should map which language/tool/model properties change agent cost and when, including negative or reversed findings.

## Gate

The next bounded task is an **independent review of this design**. Close all P1/P2 findings, then implement only the reporting/measurement changes and scientific-specification files needed for a clean freeze. No model call is authorized by this draft.
