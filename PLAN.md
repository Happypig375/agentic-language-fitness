# Research plan

> **Canonical continuation plan.** Maintainer agents must read this file before substantial work. `AGENTS.md` is the automatically discovered entry point and routes agents here. Update this plan whenever the current checkpoint, ordering, or decision gates change.

## Current checkpoint — 2026-08-29

Variance-v2 status (2026-08-29): complete. The clean frozen cell, audited
calibration, 10 counterbalanced paired blocks, external raw archive, and
reproducible variance/power reports are summarized in
`docs/variance-v2-results-2026-08-29.md`. Accounting and provenance are stable,
but near-saturated correctness plus order/stochastic variance overwhelm a
plausible 7–8% effect at n=10; no language advantage or significance claim is
supported. The next milestone is Workstream C benchmark recalibration.

Completed:

- scoped and adversarial literature review with a narrowed, defensible research gap;
- executable F#/C# paired pilot on .NET 10;
- cumulative language-neutral black-box evaluation;
- fresh process and container per maintenance task with inherited candidate code;
- isolated Codex command adapter with pinned CLI/image metadata;
- green Linux and Windows CI on commit `7dda2bd232376b84968bd616a79d8043699c48c7`;
- A3 accounting machinery: strict Codex usage validation and summation, stale-sidecar removal, required-usage mode, per-task sidecar preservation, separated timing categories, conservative file-read/revisit telemetry, and the read-only `alf audit` reconciler;
- exact recovery and hash-preservation of the historical exploratory F#/C# pair, with its legacy audit failure and exclusion recorded;
- a derived, redacted two-task real-output fixture whose raw stdout, event copies, usage sidecars, task envelopes, run aggregates, timings, and source hashes reconcile exactly under `alf audit`;
- a tracked `variance-v1`/`variance-v2` protocol apparatus plus fail-closed validation, clean-freeze, image-archive verification, pinned resource/authentication enforcement, attempt reservation, retry, classification, and inclusion machinery;
- independent protocol review with no remaining P1/P2 findings and a model-free validation checkpoint; the v1 freeze was followed by the completed v2 clean freeze, calibration, formal paired cell, archive, and variance report (see the result document for hashes and outcomes).

The historical pair is **not formal study data**. The exact raw directory was recovered and hash-preserved on 2026-08-29, but its legacy artifacts fail the current `alf audit` schema checks; see `docs/historical-run-recovery-2026-08-29.md`. It remains excluded from the planned 10-block variance dataset.

Even if recovered, the pair remains exploratory because it predates the current accounting/provenance protocol, used one F#-then-C# order, had only one stochastic observation per language, and saturated correctness on a two-task chain.

## Current decision

Cross-platform CI is green at the variance-v2 frozen commit
`5363e4be8fa6e6ebbcafe24e31f1ec152353b10e`.

Remain in **Phase 1: measurement and feasibility**. The frozen-cell and
variance milestone is complete. The immediate objective is Workstream C
benchmark recalibration: design, review, and implement a longer matched chain.

Do not claim an F# advantage, begin confirmatory analysis, or expand to multiple repositories until these gates are met:

1. cross-platform CI is green — **met at `5363e4be8fa6e6ebbcafe24e31f1ec152353b10e`**;
2. the historical raw run is either recovered and audited or explicitly retired from analysis — **met: recovered, hash-preserved, legacy-audit failure recorded, excluded**;
3. usage/event accounting is reconciled against at least one real raw run fixture — **met for the recovered one-record-per-task evidence**;
4. protocol, provenance, failure, and inclusion rules are frozen before data collection — **met for variance-v2**;
5. repeated counterbalanced pairs quantify stochastic, task, temporal, and order variance — **met: 10 paired blocks; see the variance report**;
6. the benchmark is recalibrated if correctness remains saturated — **next: Workstream C**.

## Immediate continuation order

### 0. Resolve the historical-run status — complete: recovered, legacy audit failure

The explicit recovery pass found the exact original directory and task-level raw files in the original project mirror and preserved immutable/hash-checked copies. Search scope and hashes are recorded in `docs/historical-run-recovery-2026-08-29.md`. No raw artifact was recreated from Markdown totals.

The recovered copy runs through `alf audit` but reports `ok=false` for the documented legacy-schema discrepancies. It is therefore retained as hash-preserved exploratory evidence, excluded from every formal aggregate and power calculation, and not counted as a variance block. A new calibration run remains the first auditable observation.

This decision must be recorded before interpreting the old token numbers further. Recovery failure is a provenance result, not a reason to block the project indefinitely.

### 1. Complete A3 with a real reconciliation fixture — complete for recovered evidence

The accounting implementation is materially advanced but not scientifically complete until exercised against actual raw agent output.

Completed work:

- reconciled raw `agent.stdout`, redacted event copies, copied `usage.json`, embedded task results, timings, and run aggregates for both recovered F# tasks;
- confirmed from the official usage definition that cached input is a subset/breakdown of input rather than an additive quantity;
- preserved input, cached input, cache-write input, output, reasoning output, and tool calls separately;
- retained tests for missing, malformed, negative, duplicated, and multi-record usage cases, and made accepted protocol accounting require exactly one derived terminal record per ephemeral task;
- documented the conservative file-read/revisit extractor's grammar and recall limitations;
- committed a redacted real-output fixture whose `alf audit` result and exact aggregate are unit-tested.

Each recovered task has exactly one terminal usage record. The pinned Codex 0.149.1 schema and implementation identify the terminal counters as the turn's `ThreadTokenUsage.total`, but the recovered evidence cannot validate a multi-record aggregation rule. The accepted protocol therefore requires exactly one derived terminal record per one-turn ephemeral task; zero or multiple records make token accounting invalid and force protocol review rather than a guessed sum.

**Exit met:** `tests/fixtures/a3-redacted-run` reproduces the recorded task and run aggregates exactly; `docs/accounting-reconciliation-2026-08-29.md` records semantics and limitations.

### 2. Freeze protocol and provenance before accepted runs — complete for variance-v2

The completed cell is defined by `protocols/variance-v2/definition.json`. It pins `gpt-5.4`, medium reasoning, Codex CLI/image `0.149.1`, the immutable image ID and verified archive, .NET `10.0.302`, explicit Docker limits, one non-counting calibration, and ten pre-generated balanced formal blocks. It is not continuity with either the retired v1 attempt or the historical Luna pair. The harness now fails closed on dirty or changed Git state, mismatched benchmark/task hashes, probes, image/archive, model/settings/limits, schedule position, attempt identity, retry eligibility, or inclusion disposition.

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

**Current status:** `variance-v1` remains retired after its provider-invalid calibration attempt. `variance-v2` is now the completed cell: clean freeze, calibration, 10 formal paired blocks, archive, and decision report are retained. The result document records the exact provenance and exclusion rules.

### 3. Run one non-counting end-to-end calibration block — complete for variance-v2

After the v2 clean freeze, run one paired F#/C# block under the frozen protocol. Its purpose is apparatus verification, not estimation.

The calibration must:

- use the predeclared order for that block;
- require valid usage accounting;
- pass `alf audit` for both language runs;
- preserve raw artifacts and hashes under the new provenance rules;
- verify that fresh processes/containers and inherited task workspaces behave as specified;
- produce a redacted fixture and machine-readable audit report;
- expose any provider, timing, or read-telemetry incompatibility before the 10-block run.

If the protocol or harness changes in response, increment the protocol version and repeat the calibration. The final calibration does not count toward the variance sample.

The v1 calibration was attempted but was provider-invalid before any candidate outcome; v2 calibration passed and is non-counting evidence only.

### 4. Collect the counterbalanced variance pilot — complete: 10 paired blocks

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

### 5. Produce the variance and decision report — complete

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

### A2. Protocol freeze — complete for variance-v2

Commit the reviewed protocol apparatus, generate the resolved manifest from that clean HEAD, then complete calibration. The freeze must continue to fail closed if the commit, image, archive, toolchain, or host facts differ.

### A3. Usage accounting — real-output reconciliation complete

The code path is guarded and auditable, the historical run has an explicit disposition, and the checked-in derived/redacted fixture reconciles the authentic single-record-per-task evidence. Accepted protocol runs fail accounting closed unless each ephemeral task has exactly one derived terminal usage record.

### A4. Result provenance — complete for variance-v2

The versioned definition, hashes, retention policy, failure taxonomy, metric-specific inclusion rules, retry rules, and attempt reservation exist. Generate and retain the resolved manifest only from a reviewed, committed, clean checkout before any accepted run.

## Workstream B — Estimate stochastic and order variance — complete

The variance-v2 formal cell is complete. Do not pool it with the retired v1 attempt or describe it as a replication of the previously reported `gpt-5.6-luna` pair. Use its decision report to guide Workstream C.

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

## Completed variance-v2 milestone definition of done

The milestone was completed when:

- the historical run is recovered and audited or explicitly retired;
- a real raw fixture passes `alf audit` and guards accounting semantics in tests;
- a frozen protocol manifest and failure/inclusion taxonomy exist;
- a non-counting calibration block passes end to end;
- 10 new counterbalanced paired blocks are preserved under one unchanged cell;
- a variance and power report determines whether and how to extend the chain;
- no language claim exceeds those observations.

The immediate steps 2 (freeze), 3 (calibration), 4 (paired pilot), and 5
(variance report), plus Workstream A2/A4 and Workstream B, are complete for
variance-v2.

## Workstream C next-milestone definition of done

The benchmark recalibration is complete when a matched cumulative 5–10-task
chain includes additive change, a cross-cutting schema change, bug diagnosis,
a behavior-preserving refactor, and an API/backward-compatibility constraint;
at least one within-language representation treatment is implemented and
independently reviewed; cumulative black-box cases remain language-neutral with gold data
outside candidate workspaces; both implementations pass idiomaticity and
behavioral-equivalence review; and the longer chain produces measurable,
non-dominated correctness and trajectory variation in a frozen difficulty
pilot. The chain, treatment apparatus, golds, and reviews must be complete
before that new protocol cell is designed and frozen; the pilot follows the
freeze and precedes any confirmatory run.

## Workstream C gate status (current)

The implementation-ready eight-task contract is in
`docs/workstream-c-benchmark-design-2026-08-29.md`. Its material
legacy-behavior clarification standardizes exact language-neutral serialized
errors for unknown operations and missing/null `asOf`. Limited independent
review is approved with no P1/P2 findings: retained C#/F# Task 002
`ArgumentException` parameter casing differs, while the suffix-free exact
strings are symmetric; Task 001/002 remain unchanged. The
language-equivalence/error review gate is closed. **C1 and C2 are complete.**
C2 delivered the eight-task cumulative chain and 90 final cases per language,
legacy/multi-file golds, workspace checks, fail-closed paths, and exact pilot
baseline/Tasks 001/002 retention. Evidence includes 126 unit tests, strict
doctor, legacy/successor validation and scripted matrices, serialized Task
007/008 checks, focused path suites, 18 isolated gold builds, and independent
harness-security and gold/equivalence reviews with no P1/P2 findings. **C3
design is preregistered and independently approved with no remaining P1/P2
findings; implementation is next:** see
`docs/representation-treatment-v1-2026-08-29.md`. The protocol freeze,
difficulty pilot, and paid/model runs remain blocked. CI for C2 commit
`4e58677e0bfff18c2104298ad35fc4e801bbd052` is green: GitHub Actions run
`33258119571` (Linux 2m20s, Windows 2m23s; Node 20 deprecation warnings only).
Historical fixtures and variance cells remain unchanged
and excluded.
