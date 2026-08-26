# Research plan

## Phase 0 — Harness validation

1. Keep F# and C# projects behaviorally matched through black-box JSON tests.
2. Run the `scripted` adapter in CI to validate workspace creation, chained state, builds, evaluation, and artifact production.
3. Unit-test trajectory parsing and repository metrics.
4. Record exact Python, Git, .NET, OS, model, and agent versions.

**Exit criterion:** clean CI runs produce equivalent passing results for both languages and deterministic result schemas.

## Phase 1 — Feasibility pilot

Run at least three agent/model configurations across both languages and both pilot tasks.

- fresh process/context at every maintenance step;
- inherited workspace state;
- randomized language/run ordering;
- at least 10 stochastic repetitions per cell;
- identical task text and behavioral oracle;
- exact token and trajectory capture where available.

Primary feasibility outcomes:

- completion rate;
- total input, cached input, output, and reasoning tokens;
- build/test iterations;
- elapsed time;
- escaped regressions;
- source/context footprint.

**Exit criterion:** the tasks are neither saturated nor impossible, token accounting is reliable, and language effects can be estimated with uncertainty.

## Phase 2 — Matched repository expansion

Create 3–5 paired .NET applications at increasing sizes and architectural shapes:

- pure data transformation;
- command-line application with persistence;
- HTTP service;
- event/state-machine domain;
- library with public API compatibility constraints.

Each repository receives a preregistered chain of 10–30 changes covering additive features, cross-cutting schema changes, refactors, bug fixes, performance constraints, and compatibility requirements.

**Exit criterion:** matched external behavior and comparable task difficulty are established by independent review and black-box tests.

## Phase 3 — Representation ablations

Separate language syntax from other mechanisms:

- normal formatting versus losslessly compacted formatting;
- descriptive versus anonymized identifiers;
- explicit type annotations versus inferred types where legal;
- idiomatic versus mechanically translated implementations;
- compiler/test feedback enabled versus disabled;
- documentation retrieval enabled versus disabled.

This phase tests whether any effect comes from semantic density, tokenizer behavior, static verification, training familiarity, or coding style.

## Phase 4 — Longitudinal study

Run the full chain with fresh agents, preserving only the repository state between tasks. Analyze:

- creation cost versus cumulative maintenance cost;
- language × repository size interaction;
- language × model capability interaction;
- failure compounding across inherited changes;
- semantic recovery cost for a fresh agent;
- defect escape and repair burden.

Use mixed-effects or hierarchical models with task, repository, model, and run as appropriate effects. Report distributions and uncertainty rather than a single “best language” score.

## Phase 5 — Generalization

Add languages chosen to separate mechanisms:

- Python: high familiarity, low static verification;
- TypeScript: high familiarity, gradual typing;
- Rust: strong verification, higher type-system interaction cost;
- OCaml: ML-family representation with a smaller ecosystem;
- a deliberately compact or transformed representation.

The aim is a mechanism map and Pareto frontier, not a universal ranking.
