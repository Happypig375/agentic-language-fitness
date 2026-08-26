# Experimental design

## Principles

1. Use identical functional requirements across languages.
2. Keep tests and hidden acceptance criteria language-neutral where possible.
3. Record complete trajectories.
4. Randomize task/language/model run order.
5. Use repeated trials because agent trajectories are stochastic.
6. Pin model versions, compiler versions, dependencies, and prompts.
7. Keep temperature/reasoning settings explicit.
8. Treat provider cost as metadata, not a timeless scientific metric.

## Primary controlled comparison: F# vs C#

Both use:

- the same .NET version;
- equivalent NuGet dependencies;
- the same external test oracle/behavior;
- equivalent I/O and domain requirements.

This comparison is intended to isolate representational and language-tooling differences while minimizing runtime/ecosystem confounds.

## Repository sizes

Suggested initial targets:

- small: ~5k–10k conventional LOC;
- medium: ~25k–50k;
- large: ~100k+ or a dependency-expanded equivalent.

LOC is descriptive only. Store bytes, tokenizer counts, AST counts, and dependency structure as primary representation measures.

## Task families

- local bug fix;
- cross-cutting domain-model change;
- API evolution;
- serialization/schema change;
- error-model change;
- refactor;
- performance/caching change;
- concurrency/state fix;
- new feature spanning multiple modules;
- test-driven diagnosis with misleading surface symptoms.

## Agent conditions

At minimum:

1. source search/read + edit + compiler/tests;
2. same plus documentation retrieval;
3. optional language primer;
4. multiple model capability levels.

The agent must not be given hidden-test details.

## Fresh-context protocol

For longitudinal tasks, every maintenance task begins in a clean model context. The repository is the durable state.

This approximates:

- a new agent session;
- a future developer/agent with no conversational memory;
- context compaction that discarded earlier reasoning.

It directly measures how well the programming representation preserves intent for later recovery.

## Analysis

Suggested mixed-effects model:

`metric ~ language * model + language * repo_size + language * maintenance_depth + tooling + (1|task) + (1|repository)`

For binary correctness, use a logistic mixed model; for skewed cost metrics, consider log transforms or suitable generalized models.

Report effect sizes and confidence intervals, not only p-values.

## Failure criteria for the F# thesis

The hypothesis should be weakened if, under strong tool-using agents:

- F# remains more expensive than C# across repository sizes;
- F# does not improve relatively with maintenance depth;
- lower source size does not reduce semantic recovery/context cost;
- compiler/type information fails to reduce defects or repair cost enough to compensate for unfamiliarity.

A negative result is useful: it would imply training familiarity/ecosystem conventions dominate representational advantages more strongly than expected.
