# Research plan

> **Canonical continuation plan.** Maintainer agents must read this file before substantial work. `AGENTS.md` is the automatically discovered entry point and routes agents here. Update this plan whenever the current checkpoint, ordering, or decision gates change.

## Current checkpoint — 2026-08-26

Completed:

- scoped and adversarial literature review with a narrowed, defensible research gap;
- executable F#/C# paired pilot on .NET 10;
- cumulative language-neutral black-box evaluation;
- fresh process and container per maintenance task with inherited candidate code;
- isolated Codex command adapter with pinned CLI/image metadata;
- one accepted paired run with `gpt-5.6-luna`, two tasks per language, and all cumulative cases passing;
- tracked preliminary summary in `docs/preliminary-results-2026-08-26.md`.

The first accepted pair is **infrastructure and variance evidence, not language-effect evidence**:

- F# and C# both completed 2/2 tasks, so correctness is saturated in this tiny chain;
- aggregate input tokens were nearly tied;
- the task-level direction reversed sharply between `001-priority` and `002-overdue`;
- F# ran first and C# second, so order was not counterbalanced;
- there was only one stochastic observation per language.

The latest failed CI run did not reach benchmark validation. A unit test simulated Windows tokenization on Linux but compared the preserved Windows backslashes against a host-native POSIX path. Treat this as a portability-test defect, not an experimental failure. The continuation begins by restoring a green cross-platform baseline.

## Current decision

Remain in **Phase 1: measurement and feasibility**. Do not claim an F# advantage, begin a confirmatory study, or expand to many repositories until the following gates are met:

1. CI is green on Linux and Windows;
2. token and event accounting is independently reconciled against raw JSONL;
3. repeated counterbalanced pairs quantify stochastic and order variance;
4. the pilot is recalibrated if correctness remains saturated;
5. accepted-run and infrastructure-failure rules are frozen before further collection.

## Workstream A — Stabilize and freeze the apparatus

### A1. Restore and broaden CI

- Fix the host-dependent Windows path assertion.
- Keep the full Linux job: unit tests, doctor, benchmark validation, scripted chain, container build, and container validation.
- Add a Windows job for unit tests, environment checks, and matched benchmark validation.
- Do not start paid/model experiments while `main` is red.

**Exit:** the same commit is green on both operating systems and the scripted pair passes.

### A2. Freeze a protocol version

Before the next accepted real-agent run, define a dated protocol version and record:

- benchmark manifest hash and commit SHA;
- model identifier, agent product/CLI version, and relevant settings;
- container tag and immutable image ID;
- Python, Git, .NET SDK, OS, architecture, CPU/memory limits, and timeout;
- network/documentation policy;
- language order and pre-generated block identifier;
- every attempt, including infrastructure failures and timeouts.

A nominal `seed` may identify run ordering and harness randomness, but must not be described as a model seed unless the model endpoint actually exposes deterministic seeding.

### A3. Audit usage accounting

Before interpreting the preliminary token totals:

- verify whether Codex emits one aggregate `turn.completed` usage record or multiple records that must be summed;
- reconcile every task's raw JSONL, `.alf/usage.json`, task result, and run aggregate;
- document whether cached input is a subset of input or an additive category for this endpoint/version;
- preserve input, cached input, cache-write input, output, and reasoning output separately;
- distinguish agent-process wall time, evaluator time, and total run time;
- add validation that rejects inconsistent or missing usage artifacts rather than silently treating them as zero;
- derive file-read and file-revisit telemetry where command events permit it, because semantic recovery cannot be inferred from tokens alone.

**Exit:** a fixture from an accepted raw run reproduces the checked-in aggregate exactly, and parser behavior is unit-tested.

### A4. Formalize result provenance

- Keep credentials and unrestricted raw transcripts out of Git.
- For each accepted run, track a redacted manifest, aggregate summary, result-file hashes, and the external/raw-storage location.
- Retain failed attempts; never replace a failed run with a successful rerun without recording both.
- Classify failures as agent, evaluator, provider, host, authentication, timeout, or protocol failures using rules fixed before viewing language differences.

**Exit:** a reviewer can determine exactly which attempts entered each analysis and reproduce every reported aggregate from preserved artifacts.

## Workstream B — Estimate stochastic and order variance

Use the current tiny chain only as a **variance pilot** before adding more tasks.

### Fixed first cell

Hold constant the accepted-run configuration:

- model: `gpt-5.6-luna`;
- Codex CLI: `0.149.1`;
- image: `alf-codex:0.149.1` with the recorded immutable ID;
- .NET SDK: `10.0.302`;
- fresh ephemeral process and container per task;
- identical task text, evaluator, resource limits, network policy, and timeout.

Run at least **10 paired blocks**:

- five blocks in F# → C# order;
- five blocks in C# → F# order;
- pre-generate and commit/hash the order schedule;
- interleave blocks rather than completing all runs of one language first;
- retain every attempt and timestamp to expose provider/load or quota drift.

Primary pilot outcomes, evaluated jointly with success:

- complete-chain success and per-task success;
- total and cached input tokens;
- output and reasoning tokens;
- agent and total wall time;
- tool calls, commands, builds/tests, file changes, reads, and revisitations where observable;
- escaped behavioral regressions.

Use paired differences and log ratios with uncertainty intervals. Ten blocks are for estimating variance and planning sample size, not for a definitive significance claim.

**Exit:** token reconciliation remains stable, no unmodeled order effect is evident, and a simulation/power analysis can estimate the repetitions needed for larger cells.

## Workstream C — Recalibrate the benchmark

The current 2/2 versus 2/2 result indicates that the chain is too small to measure correctness or defect escape. After the variance pilot:

1. extend the existing application to a **5–10 task chain** before creating many repositories;
2. include additive changes, a cross-cutting schema change, a bug diagnosis, a refactor with unchanged behavior, and an API/backward-compatibility constraint;
3. maintain cumulative black-box cases and keep gold/evaluator data outside candidate workspaces;
4. have both implementations independently reviewed for idiomaticity and comparable architecture;
5. add at least one within-language matched representation treatment, such as clean/noisy structure or descriptive/anonymized identifiers, to calibrate any cross-language effect against ordinary source-form sensitivity;
6. pilot with a lower-capability configuration if the frontier model remains at 100% success.

**Exit:** the chain creates measurable variation without becoming dominated by impossible tasks, and language-neutral equivalence survives independent review.

## Workstream D — Multi-configuration feasibility study

Only after A–C:

- test at least three model/agent configurations spanning capability or scaffolds;
- block and randomize language order within each configuration;
- use the same protocol version throughout a cell;
- determine repetitions from pilot variance rather than an arbitrary final sample size;
- preregister primary outcomes, exclusions, stopping rules, and the hierarchical/paired analysis before collecting confirmatory data.

Analyze language × task, language × model, language × scaffold, language × chain position, and language × order interactions. A universal language ranking is not the target.

## Phase 2 — Matched repository expansion

Create 3–5 independently reviewed paired .NET applications at increasing sizes and architectural shapes:

- pure data transformation;
- command-line application with persistence;
- HTTP service;
- event/state-machine domain;
- library with public API compatibility constraints.

Each receives a preregistered chain of 10–30 changes. Reuse or adapt established language-agnostic benchmark tasks where possible, while retaining native idiomatic implementations and a common black-box oracle.

**Exit:** task difficulty, architecture, and external behavior are defensibly matched across languages.

## Phase 3 — Mechanism ablations

Separate the language label into candidate mechanisms:

- formatting and lossless compaction;
- descriptive versus anonymized identifiers;
- inferred versus explicit types where legal;
- idiomatic versus mechanical translation;
- compiler/test feedback enabled versus restricted;
- documentation retrieval enabled versus disabled;
- tokenizer fertility and source/context footprint;
- native corpus familiarity and shared .NET API transfer.

The aim is to explain an effect, not merely rank languages.

## Phase 4 — Confirmatory longitudinal study

Run the preregistered full chains with fresh agents while preserving only repository state. Estimate:

- creation cost versus cumulative maintenance cost;
- semantic recovery cost for a new agent;
- error compounding and escaped defects;
- language × repository-size and language × capability interactions;
- whether one-shot and lifetime rankings differ.

Use mixed-effects or hierarchical models that respect paired runs and dependence within evolving chains. Report distributions and uncertainty, not a single “best language” score.

## Phase 5 — Generalization

Add languages chosen to separate mechanisms:

- Python: high familiarity, weak static verification;
- TypeScript: high familiarity, gradual typing;
- Rust: strong verification with higher repair interaction cost;
- OCaml: ML-family representation with a smaller ecosystem;
- a deliberately compact or transformed representation.

The final deliverable should be a mechanism map and Pareto frontier for agentic software engineering, not advocacy for F#.

## Stop, reframe, or negative-result conditions

Reframe or stop if:

- prior work is found that already performs the same controlled matched-language inherited-maintenance experiment;
- paired implementations cannot be made comparably idiomatic and behaviorally equivalent;
- measurement variance or provider drift overwhelms plausible language effects;
- effects disappear after controlling for model familiarity, toolchain feedback, source cleanliness, or order;
- cross-language differences are no larger or less stable than within-language representation perturbations.

Those outcomes remain scientifically useful: they would show that language choice is a weak lever compared with agent/scaffold, source quality, or stochastic trajectory effects.

## Next milestone definition of done

The next milestone is complete when:

- Linux and Windows CI are green;
- usage accounting is reconciled and guarded by tests;
- a frozen run manifest and failure taxonomy exist;
- 10 counterbalanced paired blocks of the current cell are preserved;
- a variance and power report determines whether and how to expand the chain;
- no language claim is made beyond what those observations support.
