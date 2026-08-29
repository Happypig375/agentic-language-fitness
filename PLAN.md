# Research plan

> **Canonical continuation plan.** Maintainer agents must read this file before substantial work. `AGENTS.md` is the automatically discovered entry point and routes agents here. Update this plan whenever the current checkpoint, ordering, or decision gates change.

## Current checkpoint — 2026-08-29

Completed:

- scoped and adversarial literature review with a narrowed, defensible research gap;
- executable F#/C# paired pilot on .NET 10;
- cumulative language-neutral black-box evaluation;
- fresh process and container per maintenance task with inherited candidate code;
- isolated Codex command adapter with pinned CLI/image metadata;
- green Linux and Windows CI on commit `8711ea9ebceb39c18abd56659a5bf41e555f62d2`;
- A3 accounting machinery: strict Codex usage validation and summation, stale-sidecar removal, required-usage mode, per-task sidecar preservation, separated timing categories, conservative file-read/revisit telemetry, and the read-only `alf audit` reconciler;
- one historical exploratory F#/C# pair in which both languages completed both tasks.

The historical pair is **not formal study data** at present. Its expected raw directory,
`results/codex-docker-dotnet10-gpt-5.6-luna-seed20260826-rerun3/`, is unavailable, so the checked-in summary cannot be independently reconciled against raw JSONL with the new accounting audit. It must not be included in the planned 10-block variance dataset unless the exact artifacts are recovered and pass `alf audit` without reconstruction.

Even if recovered, the pair remains exploratory because it predates the current accounting/provenance protocol, used one F#-then-C# order, had only one stochastic observation per language, and saturated correctness on a two-task chain.

## Current decision

Remain in **Phase 1: measurement and feasibility**. The immediate objective is no longer to add features or languages; it is to produce a frozen, auditable first experimental cell.

Do not claim an F# advantage, begin confirmatory analysis, or expand to multiple repositories until these gates are met:

1. cross-platform CI is green — **met**;
2. the historical raw run is either recovered and audited or explicitly retired from analysis;
3. usage/event accounting is reconciled against at least one real raw run fixture;
4. protocol, provenance, failure, and inclusion rules are frozen before data collection;
5. repeated counterbalanced pairs quantify stochastic, task, temporal, and order variance;
6. the benchmark is recalibrated if correctness remains saturated.

## Immediate continuation order

### 0. Resolve the historical-run status

Perform one explicit recovery pass for the exact original directory and its task-level raw files. Check the originating host/WSL environment, backups, archived terminal workspace, and any deliberately retained external run storage. Do not recreate raw artifacts from the Markdown totals.

Two valid outcomes:

- **Recovered:** preserve an immutable copy, calculate hashes, run `alf audit`, redact a small representative fixture, and document every discrepancy.
- **Not recovered:** mark the pair permanently as an unaudited legacy smoke test, exclude it from every formal aggregate and power calculation, and use a new calibration run as the first auditable observation.

This decision must be recorded before interpreting the old token numbers further. Recovery failure is a provenance result, not a reason to block the project indefinitely.

### 1. Complete A3 with a real reconciliation fixture

The accounting implementation is materially advanced but not scientifically complete until exercised against actual raw agent output.

Required work:

- verify whether Codex CLI emits incremental or cumulative usage when more than one `turn.completed.usage` record appears;
- reconcile raw `agent.stdout`, parsed `events.jsonl`, copied `usage.json`, embedded task results, and run aggregates;
- confirm from the endpoint/version whether cached input is a subset of `input_tokens`, not an additive quantity;
- preserve input, cached input, cache-write input, output, reasoning output, and tool calls separately;
- test missing, malformed, negative, duplicated, and multi-record usage cases;
- calibrate the conservative file-read/revisit extractor against real command events and document its recall limitations;
- create a redacted raw-run fixture whose `alf audit` result and expected aggregate are unit-tested.

If the historical run is unavailable, perform this step on the non-counting calibration run in step 3.

**Exit:** a real raw fixture reproduces the recorded task and run aggregates exactly, accounting semantics are documented, and any unavailable telemetry remains unavailable rather than zero.

### 2. Freeze protocol and provenance before accepted runs

Create a versioned protocol/manifest for the first variance cell. At minimum record:

- protocol version and repository commit;
- benchmark manifest and task-file hashes;
- model identifier, agent product, CLI version, and exposed settings;
- container tag and immutable image ID;
- Python, Git, .NET SDK, OS, architecture, CPU/memory/process limits, and timeout;
- network and documentation policy;
- fresh-context and inherited-workspace semantics;
- pre-generated paired-block order and block identifier;
- raw-artifact location, file hashes, redaction policy, and retention policy;
- inclusion/exclusion rules and a failure taxonomy covering agent, provider, authentication, host, evaluator, timeout, protocol, and accounting failures;
- retry rules that retain every attempt and never silently substitute a successful rerun.

A nominal `seed` may identify schedule generation and harness randomness. It must not be described as a model seed unless deterministic endpoint seeding is actually exposed.

If the original model/CLI/container combination cannot still be pinned, define a **new experimental cell**. Do not mix a changed backend or scaffold into the old pair as though it were a replication.

**Exit:** a reviewer can determine in advance which attempts enter analysis and can reproduce every accepted aggregate from preserved artifacts.

### 3. Run one non-counting end-to-end calibration block

After steps 0–2, run one paired F#/C# block under the frozen protocol. Its purpose is apparatus verification, not estimation.

The calibration must:

- use the predeclared order for that block;
- require valid usage accounting;
- pass `alf audit` for both language runs;
- preserve raw artifacts and hashes under the new provenance rules;
- verify that fresh processes/containers and inherited task workspaces behave as specified;
- produce a redacted fixture and machine-readable audit report;
- expose any provider, timing, or read-telemetry incompatibility before the 10-block run.

If the protocol or harness changes in response, increment the protocol version and repeat the calibration. The final calibration does not count toward the variance sample.

### 4. Collect the counterbalanced variance pilot

Use the current small chain only to estimate stochastic and order variance. Under one unchanged protocol cell, collect at least **10 complete paired blocks**:

- five blocks in F# → C# order;
- five blocks in C# → F# order;
- order pre-generated, committed or hashed, and interleaved;
- both language runs in a block performed as close together as practical;
- every attempt and timestamp retained to expose provider/load, quota, or temporal drift;
- no inspection-driven changes to prompts, tasks, evaluator, harness, model, scaffold, or toolchain inside the cell.

Primary pilot outcomes, interpreted jointly with correctness:

- full-chain and per-task success;
- input and cached-input tokens;
- output and reasoning tokens;
- agent-process, evaluator, task-total, and run-total wall time;
- tool calls, commands, compiler/test interactions, file changes, reads, and revisitations where observable;
- behavioral regressions and classified failures.

The unaudited historical pair is not block 0 and is excluded from these ten blocks.

### 5. Produce the variance and decision report

Before extending the benchmark, report:

- paired language differences and log ratios by task and aggregate;
- within-language and within-task variance;
- order, block-time, and temporal-trend diagnostics;
- success/failure distributions and reasons;
- agreement between tokens, wall time, navigation, and repair behavior;
- sensitivity to excluding infrastructure/provider failures under the frozen rules;
- simulation-based sample-size estimates for plausible effects, including the approximately 7–8% token effect reported by the closest code-cleanliness predecessor.

Ten blocks are a variance pilot, not a definitive hypothesis test.

Decision gate:

- **Accounting/provenance unstable:** fix the apparatus and start a new protocol cell.
- **Variance overwhelms plausible effects:** increase repetitions, improve blocking, or reframe the study around scaffold/trajectory variance.
- **Measurement stable but correctness saturated:** extend the chain before testing more models.
- **Stable measurable variation:** proceed to benchmark recalibration and multi-configuration feasibility.

## Workstream A — Stabilize and freeze the apparatus

### A1. Cross-platform CI — complete

- [x] Host-independent Windows path tests.
- [x] Full Linux unit, doctor, snapshot, scripted-chain, container-build, and container-validation job.
- [x] Windows unit, doctor, and matched-snapshot validation job.
- [x] Exact .NET SDK pin with feature-band roll-forward disabled.

### A2. Protocol freeze — next after A3 disposition

Complete immediate continuation steps 0–3.

### A3. Usage accounting — implementation complete, empirical reconciliation pending

The code path is now guarded and auditable. The remaining requirement is a real raw fixture and an explicit disposition of the missing historical run.

### A4. Result provenance — not complete

Complete the versioned manifest, hashes, retention policy, failure taxonomy, and inclusion rules before accepted variance runs.

## Workstream B — Estimate stochastic and order variance

Execute immediate continuation steps 4–5. The first formal cell should use one pin-able model/agent/scaffold configuration. The previously reported `gpt-5.6-luna`/Codex CLI `0.149.1` combination may be reused only if it can still be held constant and recorded; otherwise define a new cell rather than asserting continuity.

## Workstream C — Recalibrate the benchmark

The 2/2 versus 2/2 exploratory result indicates that the chain is too small to measure correctness or defect escape. After the variance report:

1. extend the existing application to a **5–10 task chain** before creating many repositories;
2. include additive changes, a cross-cutting schema change, a bug diagnosis, a behavior-preserving refactor, and an API/backward-compatibility constraint;
3. maintain cumulative black-box cases and keep gold/evaluator data outside candidate workspaces;
4. independently review both implementations for idiomaticity and comparable architecture;
5. add at least one within-language matched representation treatment—such as clean/noisy structure or descriptive/anonymized identifiers—to calibrate cross-language effects against ordinary source-form sensitivity;
6. pilot a lower-capability configuration if the strongest configuration remains at 100% correctness.

**Exit:** the chain creates measurable variation without becoming dominated by impossible tasks, and language-neutral equivalence survives independent review.

## Workstream D — Multi-configuration feasibility

Only after A–C:

- test at least three model/agent configurations spanning capability or scaffolds;
- block and randomize language order within each configuration;
- keep one protocol version throughout each cell;
- determine repetitions from pilot variance rather than an arbitrary final count;
- preregister primary outcomes, exclusions, stopping rules, and hierarchical/paired analysis before confirmatory collection.

Analyze language × task, language × model, language × scaffold, language × chain position, and language × order interactions. A universal language ranking is not the target.

## Phase 2 — Matched repository expansion

Create 3–5 independently reviewed paired .NET applications at increasing sizes and architectural shapes:

- pure data transformation;
- command-line application with persistence;
- HTTP service;
- event/state-machine domain;
- library with public API compatibility constraints.

Each receives a preregistered chain of 10–30 changes. Reuse or adapt established language-agnostic benchmark tasks where possible, while retaining native idiomatic implementations and a common black-box oracle.

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

Run preregistered full chains with fresh agents while preserving only repository state. Estimate creation versus maintenance cost, semantic recovery, error compounding, escaped defects, language × repository-size and language × capability interactions, and whether one-shot and lifetime rankings differ.

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

- prior work already performs the same controlled matched-language inherited-maintenance experiment;
- paired implementations cannot be made comparably idiomatic and behaviorally equivalent;
- measurement variance or provider drift overwhelms plausible language effects;
- effects disappear after controlling for model familiarity, toolchain feedback, source cleanliness, or order;
- cross-language differences are no larger or less stable than within-language representation perturbations.

Those outcomes remain scientifically useful: they would show that language choice is a weak lever compared with agent/scaffold, source quality, or stochastic trajectory effects.

## Next milestone definition of done

The next milestone is complete when:

- the historical run is recovered and audited or explicitly retired;
- a real raw fixture passes `alf audit` and guards accounting semantics in tests;
- a frozen protocol manifest and failure/inclusion taxonomy exist;
- a non-counting calibration block passes end to end;
- 10 new counterbalanced paired blocks are preserved under one unchanged cell;
- a variance and power report determines whether and how to extend the chain;
- no language claim exceeds those observations.
