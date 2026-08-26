# Agentic Language Fitness

Research plan for measuring how programming-language choice changes the lifetime computational cost, reliability, and maintainability of agentic software engineering.

## Core question

> Which programming-language properties minimize the total computation required for AI agents to correctly create, understand, modify, verify, and maintain software over its lifetime?

This is deliberately different from asking which language produces the shortest source or the highest one-shot benchmark score.

A useful first approximation is:

\[
C_{lifetime} = C_{creation} + \sum_i C_{maintenance,i} + C_{defects}
\]

where an agent trajectory may include source/context tokens read, reasoning and output tokens, tool calls, compilation failures, test failures, retries, wall time, and undetected regressions.

## Motivation

Programming languages are representations consumed repeatedly by both humans and coding agents. Language choice can therefore affect:

- source/context size;
- semantic information available per model token;
- model familiarity from pretraining;
- locality of reasoning;
- strength of compiler/type-checker feedback;
- cost of repair loops;
- probability of undetected defects;
- ease of fresh-context maintenance;
- interoperability and ecosystem knowledge.

The working hypothesis is **not** “shorter languages are better.” Code-golf languages expose why that objective is wrong: extreme lexical compression can remove semantic anchors, increase model uncertainty, and create more retries than it saves in source tokens.

The more interesting target is approximately:

\[
\text{Agentic Language Fitness}
\propto
\frac{\text{recoverable semantics + verifiable constraints}}
     {\text{context + reasoning + repair cost}}
\]

## Why F# is an interesting test case

F# is not assumed to be optimal. It is a useful experimental point because it combines:

- concise ML-family syntax;
- strong static typing with type inference;
- discriminated unions and exhaustive pattern matching;
- expression-oriented programming;
- immutability-by-default conventions;
- relatively low boilerplate;
- strong compiler feedback;
- access to the much larger .NET ecosystem and C# knowledge base.

Its obvious countervailing weakness is lower native training-corpus exposure than Python, JavaScript/TypeScript, C#, Java, or C++.

The cleanest primary comparison is therefore **F# vs C#**, because both share .NET, NuGet, CLR semantics, and much of the same library surface. This controls away more ecosystem variation than comparisons such as F# vs Python.

## Main hypotheses

See [`docs/hypotheses.md`](docs/hypotheses.md) for falsifiable versions. In brief:

1. Programming language changes total agent trajectory cost even after controlling for task and model.
2. Raw source brevity is a poor predictor of total agent cost.
3. Semantic compression is beneficial; opaque lexical compression is not.
4. Static verification trades some first-pass difficulty for cheaper and safer repair.
5. Training familiarity dominates more strongly for weaker agents and small tasks.
6. Representation quality matters more as repository size and maintenance depth increase.
7. F# may lose one-shot generation while becoming relatively stronger on fresh-agent repository maintenance.
8. The advantage, if any, should appear most clearly against C# under shared-.NET workloads.

## Experimental program

### Tier 1 — Matched microtasks

Implement identical algorithmic and library-light tasks in several languages.

Candidate languages:

- F#
- C#
- Python
- TypeScript
- Rust
- OCaml

Measure the **full trajectory**, not only the final answer:

- input/context tokens;
- reasoning tokens where observable;
- output tokens;
- compilation attempts and failures;
- test runs and failures;
- tool calls;
- wall-clock time;
- final correctness;
- final source tokens.

This establishes basic language/model interactions and reproduces the style of recent multilingual token-cost work.

### Tier 2 — Parallel repositories

Construct semantically equivalent medium-sized repositories in at least F# and C#, then optionally Python/Rust/TypeScript.

Give agents matched realistic issues:

- add a domain-model variant;
- change serialization;
- propagate an optional field;
- add caching;
- modify validation rules;
- diagnose a regression;
- refactor duplicated behavior;
- alter an API contract;
- change error handling;
- fix concurrency/state bugs.

Measure correctness and the amount of repository state the agent had to consume before making a successful patch.

### Tier 3 — Fresh-agent longitudinal maintenance

This is the central experiment.

Simulate a project history of many changes. For each maintenance task, start with a **fresh agent context** that has no memory of earlier development beyond the repository itself.

Define semantic recovery cost for task \(M\):

\[
SRC(M) = \text{source/context tokens consumed before a correct modification}
\]

Then estimate:

\[
C_{lifetime} = C_{initial} + \sum_{i=1}^{N} C_{maintenance,i}
\]

The key prediction is an interaction between language and repository/history size—not necessarily a universal one-shot winner.

### Tier 4 — Representation ablations

Within the same language, vary representation while preserving behavior:

1. normal descriptive code;
2. formatting-minified but semantically identical code;
3. shortened/opaque identifiers;
4. boilerplate-expanded code;
5. inferred vs explicit types where possible;
6. normal abstractions vs artificially golfed shorthand.

This distinguishes **useful compression** from destructive compression.

### Tier 5 — Familiarity controls

Training exposure is a major confound. Use several approaches:

- compare multiple model families and capability levels;
- run closed-book vs documentation/tool-enabled conditions;
- provide matched language primers;
- use open-weight code models where training data are better characterized;
- if feasible, adapt the same base model on equal token budgets of different languages.

## Primary metrics

Do not collapse everything into a single score initially.

### Correctness

- hidden-test pass rate;
- compile/type-check success;
- regressions introduced;
- static-analysis findings;
- property-test failures.

### Agent computation

- total input/context tokens;
- total generated tokens;
- reasoning tokens where available;
- repeated source-token reads;
- tool calls;
- wall-clock time;
- provider/model cost when meaningful.

### Repair burden

- compiler failures;
- test failures;
- patch iterations;
- reversions;
- failed tool invocations.

### Representation

- source characters;
- tokenizer tokens by model;
- AST node count;
- declaration count;
- dependency edges;
- static type/constraint information;
- repository working-set size needed for a task.

### Maintenance

- semantic recovery cost (SRC);
- tokens read by a fresh agent before first correct patch;
- cumulative lifetime cost across a task sequence;
- defect escape rate after repeated evolution.

See [`docs/metrics.md`](docs/metrics.md).

## Statistical design

A useful initial factorial design is:

- 5–6 languages;
- 4–5 models/capability levels;
- 50–100 matched tasks;
- 3 repository sizes;
- repeated trials per condition.

A mixed-effects analysis can model task and repository as random effects while estimating language, model, repository size, and interaction terms such as:

- language × model capability;
- language × repository size;
- language × maintenance depth;
- language × tooling availability.

The most important preregistered prediction for the F# hypothesis is:

> **F#'s relative performance should improve as the task shifts from small one-shot generation toward large-repository, fresh-context maintenance with compiler/tool access.**

If it does not, the hypothesis loses substantial support.

## Non-goals / guardrails

- Do not assume F# is best before measurement.
- Do not equate character count with tokenizer count.
- Do not use final source length as a proxy for full agent cost.
- Do not treat one proprietary provider's current pricing as a scientific constant.
- Do not hide negative results.

## Repository layout

```text
benchmarks/   matched benchmark projects and tasks
data/         raw/derived result conventions
experiments/  immutable experiment manifests
docs/         hypotheses, metrics, experimental design
```

See [`PLAN.md`](PLAN.md) for the staged implementation roadmap and [`references.md`](references.md) for the initial literature map.
