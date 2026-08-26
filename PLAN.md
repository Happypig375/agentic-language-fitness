# Research plan

## Phase 0 — Reproduce existing results

Goal: validate the harness before testing novel claims.

1. Reproduce a small subset of multilingual one-shot coding tasks.
2. Record complete trajectories, including failed compilations and retries.
3. Verify that language-dependent token-cost differences are observable.
4. Validate token accounting across providers/models.

**Exit criterion:** repeated runs produce stable enough language/model cost distributions to justify repository-scale experiments.

## Phase 1 — F# vs C# controlled .NET benchmark

Build matched implementations on the same runtime and libraries.

Suggested initial domain: a small service/library with:

- immutable-ish domain model;
- JSON serialization;
- validation;
- collections and transformations;
- persistence abstraction;
- async operations;
- tests;
- a small CLI or HTTP boundary.

Construct 20–30 matched maintenance tasks.

Record:

- successful completion;
- source/context tokens read;
- output/reasoning tokens;
- compile/test iterations;
- elapsed time;
- regressions;
- patch size.

**Primary question:** does F# reduce semantic recovery/context cost enough to offset lower model familiarity and possible repair overhead?

## Phase 2 — Repository-size scaling

Create or derive small/medium/large variants with the same conceptual architecture.

Test whether relative language cost changes as relevant context grows.

**Key interaction:** `language × repository_size`.

## Phase 3 — Fresh-agent maintenance chains

Create deterministic sequences of 50–100 changes.

For every task:

1. reset model context;
2. present only the issue and repository/tool access;
3. require tests to pass;
4. store complete trajectory;
5. advance the repository state only on successful completion.

Compare cumulative lifetime cost and defect escape rate.

## Phase 4 — Semantic compression ablations

Use transformations within one language to distinguish:

- whitespace/presentation redundancy;
- redundant type syntax;
- descriptive identifiers;
- standard high-level combinators;
- artificial shorthand/code golf.

This phase tests the central representation hypothesis independently of language popularity.

## Phase 5 — Familiarity/tooling disentanglement

Conditions:

- no documentation;
- documentation retrieval enabled;
- compiler only;
- compiler + tests;
- language primer in context;
- optional language-specific adaptation for open models.

Estimate how much of each language's performance comes from learned familiarity versus intrinsic representation/tooling properties.

## Phase 6 — Expand language set

Add Python, TypeScript, Rust, OCaml and potentially others only after the harness is stable.

Avoid turning the project into a language popularity contest. Each added language should test a distinct point in the design space.

## Phase 7 — Model lifetime economics

Fit an expected-cost model:

\[
E[C] = C_{creation} + \lambda C_{maintenance} + \mu C_{defects}
\]

where \(\lambda\) represents expected future modifications and \(\mu\) represents the expected cost of escaped defects.

Report Pareto frontiers for different project types rather than one global ranking.
