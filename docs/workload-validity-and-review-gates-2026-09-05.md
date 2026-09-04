# Workload validity and agent review gates

**Date:** 2026-09-05  
**Status:** Governing design note for future paired repositories and autonomous maintainer work. It does not authorize a model run.

## Why one benchmark cannot prove everything

A strictly matched F#/C# repository family is useful for causal attribution, but a heavily controlled synthetic family may not resemble ordinary software maintenance. Native real repositories are representative, but language is then confounded with domain, ecosystem, team practices, architecture, age, and issue selection.

The project therefore uses two non-poolable evidence layers:

1. **Controlled paired layer — internal validity.** The same semantic system, task sequence, external oracle, candidate-visible information, and harness policy are implemented idiomatically in both languages. This estimates a language-representation or language-stack contrast within the frozen benchmark ecology.
2. **Native ecological layer — external validity.** Real F# and C# repositories and naturally occurring maintenance tasks are sampled and stratified by domain, scale, task family, age, test quality, and ecosystem. This asks whether the controlled pattern transfers. It is observational and must not be described as a causal language effect.

A claim becomes stronger when both layers point in the same direction, but their estimates must remain separate.

## Define the estimand before declaring a comparison fair

“Fair” depends on the question.

### Controlled representation estimand

> Given the same semantic workload and a controller-owned tool path, how do the candidate-visible language representations affect comprehension, first-patch correctness, retrieval, repair, and model cost?

This condition neutralizes avoidable restore, audit, network, command-choice, and raw-diagnostic variation. It is the primary condition for E3a and Workstream H.

### Ecological language-stack estimand

> What does it cost to maintain idiomatic F# versus idiomatic C# with their real compilers, project systems, package behavior, language services, and intended development-tool policy?

Language-specific project ordering and compiler latency are part of this estimand rather than nuisances. The intended network/cache/audit policy must nevertheless be explicit and reproducible; the legacy blocked-source audit-on condition is a stress ecology, not a universal default.

### Model-familiarity estimand

> Holding repositories and tools fixed, how much of the difference changes when documentation, exemplars, adaptation, or model capability changes?

This is a separate later treatment. It must not be inferred from a single F#/C# contrast.

## Workload sampling: derive tasks before seeing language outcomes

Create a frozen workload frame before building the large paired repositories.

### Provenance

At least half of task templates should be abstracted from real, accepted maintenance changes in public .NET repositories. Sample source changes from both F# and C# ecosystems so one community does not define what “normal maintenance” means. The remaining templates may be language-neutral domain changes or established benchmark tasks.

Record, without copying project-specific solutions:

- source repository and commit/issue identity;
- original domain and project scale;
- change category;
- files/modules touched;
- dependency-graph distance;
- public API and compatibility obligations;
- test and review evidence;
- why the abstracted task remains realistic after transplantation.

Task abstraction and inclusion happen before any candidate result is observed.

### Balanced task taxonomy

The controlled family should include a preregistered balance of:

- local defect repair;
- additive feature work;
- cross-cutting data/schema or state-model change;
- behavior-preserving refactor;
- public API or backward-compatibility change;
- multi-module integration;
- robustness/error-handling change;
- asynchronous, concurrency, or performance-sensitive work where the domain supports it;
- dependency/toolchain change only in an explicitly ecological stratum.

Do not select only tasks that showcase discriminated unions or only tasks dominated by CLR DTO/nullability interop. Language-affordance tasks may exist, but must be a named stratum rather than silently defining the whole benchmark.

### Realistic difficulty

Freeze a task-size distribution using the source workload frame: touched semantic units, relevant dependency closure, required invariants, and expected review complexity. Do not tune tasks until one language fails at a desired rate. Calibration tasks and confirmatory tasks must be separate, or calibration decisions must use blinded pooled difficulty criteria that do not inspect which language performed better.

## Paired repository construction

### One semantic contract, two native implementations

Use a language-neutral behavioral specification, public protocol, invariant ledger, and hidden oracle. Then author each implementation natively and idiomatically. Do not mechanically translate one language into the other and do not force equal lines of code.

Fairness is evaluated against semantic structure, including:

- public operations and observable behavior;
- domain entities, states, and invariants;
- baseline feature set;
- dependency-graph roles and path lengths;
- number and role of active modules;
- transitive task-relevant closure;
- persistence, concurrency, and failure semantics;
- documentation information content;
- test adequacy and mutation/fault sensitivity.

Exact graph identity is unnecessary and may itself make one language unidiomatic. Material asymmetries must be documented and classified as representation, toolchain, project-system, or benchmark-design differences.

### Independent idiomaticity review

Before freezing a pair:

1. an experienced F# reviewer evaluates only the F# implementation;
2. an experienced C# reviewer evaluates only the C# implementation;
3. a separate reviewer examines the language-neutral contract and paired semantic map without seeing agent outcomes;
4. all P1 findings are resolved or the pair is excluded;
5. P2 differences are recorded for sensitivity analysis.

Reviewers should assess whether a competent maintainer would accept the architecture, naming, type modeling, error handling, project structure, and tests in a real codebase. “Idiomatic” does not mean maximally clever or golfed.

### More than one domain

A serious result cannot rest on OrderFlow alone. Use at least three architectural/domain families, including:

- a .NET-interop-heavy application, where DTOs, JSON, async I/O, and platform libraries are normal;
- a domain-model/state-machine or transformation workload where F# can use discriminated unions, options, and pattern matching naturally;
- a service or library with public API compatibility and multi-module dependencies.

This allows language × domain interaction instead of treating one workload as universal.

## Context-pressure fairness

For Workstream H, report both of the following.

### Same semantic scale

Both languages implement the same modules, behavior, and invariants. This measures practical representational capacity: whether one language fits more of the same software into the source budget.

### Same normalized occupancy

Select observations where each candidate-visible representation occupies the same fraction of the effective source budget. This measures model behavior under equal context pressure.

Do not collapse these views. A language can fit more semantic content yet perform similarly or worse at equal occupancy.

Additional controls:

- exact frozen model tokenizer, not character or line counts;
- identical fixed prefix and output reserve;
- controller-owned source serialization;
- counterbalanced early/middle/late placement of relevant modules;
- no inert filler; every added module is active, tested, and eligible to become task-relevant;
- language-neutral symbol/file mapping for controlled retrieval tools;
- token-bounded chunks rather than line-bounded chunks;
- identical tool schemas and metadata overhead;
- gold relevant-file/symbol closures established before candidate runs;
- compiler/test feedback absent from primary context-density arms and isolated into a separately named repair condition.

## External-validity layer

After controlled results exist, sample native repositories rather than porting everything into the paired family.

Stratify or match on:

- application domain;
- repository and relevant-working-set size;
- age and maintenance activity;
- test coverage/quality proxies;
- task family and touched-module count;
- dependency complexity;
- framework and package use;
- documentation availability;
- issue/commit acceptance evidence.

Use real accepted issues or replayed commits with hidden post-change tests when licensing permits. Report this as ecological validation. Exact F#/C# equality is neither possible nor claimed; the question is whether controlled mechanisms and scale interactions reappear.

## Workload-validity dossier required before model runs

Every new repository family must publish a reviewable dossier containing:

1. the target estimand and named tool/harness ecology;
2. workload provenance and frozen sampling rules;
3. task-taxonomy balance;
4. language-neutral contract and hidden-oracle design;
5. paired semantic/dependency maps;
6. per-language idiomaticity reviews;
7. unavoidable language-specific obligations;
8. exact tokenizer counts for whole repository and task-relevant closures;
9. documentation and dependency exposure;
10. mutation/fault checks showing that the evaluator detects plausible wrong changes;
11. excluded pairs/tasks and reasons;
12. a signed-off P1/P2 review disposition.

No “fair and representative” claim is allowed without this dossier. A benchmark can be accepted as controlled but not representative, or representative but not causally matched; those are legitimate narrower statuses.

## Autonomous agent review cadence

The unit of autonomous progress is **one scientific gate**, not a duration, commit count, or broad phase. An agent may finish all implementation, tests, documentation, and CI repair necessary to make that gate reviewable, but it must not cross the next gate automatically.

### Gate sequence

1. **Question and workload gate** — estimand, sampling frame, task taxonomy, inclusion/exclusion rules, and workload-validity dossier draft. Stop before constructing the full benchmark.
2. **Paired-artifact gate** — one representative paired repository/exemplar, semantic map, idiomaticity review, oracle, and mutation checks. Stop before scaling it into all sizes/domains.
3. **Apparatus gate** — controller, serialization/retrieval policy, accounting, fixtures, model-free tests, clean freeze, and exact-head CI. Stop before any model call.
4. **Calibration gate** — execute only the preregistered non-counting calibration batch, archive and audit every attempt, then stop before changing the design or collecting formal data.
5. **Formal-block gate** — execute one predeclared macroblock or configuration cell at a time. Review protocol validity and infrastructure health without using the direction or magnitude of the language effect to decide continuation.
6. **Analysis gate** — produce the frozen analysis and interpretation report, then stop before modifying tasks, harness, models, or starting the successor experiment.

Design, execution, analysis, and redesign must therefore be separate autonomous tasks. This prevents outcome-driven benchmark tuning and the earlier pattern of apparatus versions multiplying inside one long run.

### Current repository-specific stop point

The next maintainer agent may complete **E3a specification/review/freeze/CI only**:

- scientific definition;
- task selection and evidence rationale;
- shared-prefix patch/repair protocol;
- deterministic fixtures and identities;
- same-context continuation proof or explicit fresh-context label;
- controller commands and diagnostic-packet policy;
- tests, independent review, clean freeze, and exact-commit CI.

It must then return for review. It may not invoke a model, execute E3a, implement E3b/F0, build repair subagents, or start Workstream H.

After explicit authorization, an execution agent may run the complete frozen **non-counting E3a pilot** and archive/audit it, then must return before interpretation or protocol change. Splitting the tiny frozen pilot run-by-run would add little protection; allowing the same agent to redesign after seeing outcomes would add substantial bias.

### Workstream H cadence

Do not allow one agent to construct a million-token family and immediately run it. Use these checkpoints:

1. workload sampling frame plus validity criteria;
2. one small/medium paired exemplar plus dossier;
3. scalable-family generator or construction method plus model-free H0 context-budget/retrieval validation;
4. one non-counting paired calibration at low artificial budgets;
5. one preregistered pressure macroblock at a time;
6. absolute long-context validation only after lower-budget accounting and position controls pass.

## Immediate-stop conditions

Return for review immediately when:

- the estimand, workload sample, task semantics, oracle, candidate-visible information, or tool policy would change;
- a language pair cannot be made both idiomatic and behaviorally equivalent;
- an outcome has been observed before a freeze and could influence task selection;
- a new model, scaffold, context policy, retrieval algorithm, subagent, or ecological stratum is proposed;
- CI or audit is red at a scientific boundary;
- exact context composition or model identity cannot be reconstructed;
- two failures of the same apparatus class occur;
- the current gate’s acceptance criteria are met.

The last condition is deliberate: completing a gate is a reason to stop and review, not permission to begin the next experiment.