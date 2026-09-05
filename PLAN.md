# Research plan

**Reviewed:** 2026-09-06. Canonical continuation plan; historical results and frozen protocols are unchanged. Review disposition, working implementation, executable freeze and permission for live consumption are separate states.

## Authority and current checkpoint

Read this file first; `AGENTS.md` is its maintainer router. Current methods live in [experimental design](docs/experimental-design.md), [metrics](docs/metrics.md), [workload validity](docs/workload-validity-and-review-gates-2026-09-05.md), and the future [H design](docs/workstream-h-context-pressure-design-2026-09-05.md). Dated predecessor proposals explain history. An authorized frozen protocol governs its own experiment; conflicts require review rather than retrospective reinterpretation.

A–C and D v3 are closed. E1/E2/E2a are accepted within their recorded boundaries:

| Evidence | Finding | Limit |
|---|---|---|
| [D v3](docs/workstream-d-v3-calibration-disposition-2026-09-03.md) | Ten non-counting eight-task calibrations succeeded; exploratory F#/C# input/time ratios near 1.38. | Five pairs from three configurations, not confirmatory language inference. |
| [E1](docs/workstream-e1-v3-forensic-disposition-2026-09-03.md) | More F# observed build failures, repair cycles and project edits. | Includes dependency/environment failures and missing first-build boundaries. |
| [E2](docs/workstream-e2-toolchain-disposition-2026-09-04.md) | Source proxies/runtime near parity; offline tool timings differ. | Different host/command ecology from v3. |
| [E2a](docs/workstream-e2a-disposition-2026-09-04.md) | Host-aligned replay shows more tool calls, slower builds, and a large blocked-source audit amplifier. | Gold replay is not causal mediation of model tokens/time. |

Keep controlled pre-restored/audit-off, intended online audit-reachable, and legacy constrained-network audit-on ecologies identifiable. Disabling audit in the measured loop is not a recommendation to abandon production dependency auditing. Aggregate input is repeated trajectory usage, not unique source or peak context. The tiny current repository cannot identify a scale slope or future crossover.

## E3a disposition — preparation complete, bounded implementation next

The packet at **`19b1902be59324b98741ccb6c3a8396de962f5f7`** has been read and reviewed in a second AI session. Exact-commit CI run **33972207924** completed successfully on Linux and Windows, including the trusted E3a fixtures. This is not human-expert approval or evidence of an operational API client/sandbox.

**Decision: accept the narrow design for minimal implementation with required corrections.** See [the current disposition](docs/workstream-e3a-review-disposition-2026-09-06.md). Do not repeat packet preparation or expand the scientific design. The original packet remains a reviewed, unfrozen proposal; its implementing successor must update the specification, generated identities and regression tests consistently.

Retain Tasks 001/006/007, one provisional Luna-high setting, four paired repetitions per task, one initial submission and at most two repairs. This gives 24 trajectories, 12 pairs, and at most 72 generation requests. The task sample is deliberately diagnostic and non-confirmatory, not representative maintenance. Accept full-source/no-tools API access as a named scientific scaffold proposal, not historical Codex M or a verified account entitlement.

The task-001 Int32.MinValue holdout is valid under the stated integer contract even though archived F# target code fails it. Preserve the old target and result. Later selected F# predecessors already use safe priority comparison; do not invent an inherited defect or alter their source gratuitously.

### Required pre-freeze corrections

1. **Task completion:** Task 007 preserves behavior while changing architecture. Include its declared live-extraction rubric in task-completion scoring; report build-plus-behavior separately. A missing required rubric judgement is unknown, not a completed refactor. No-op, empty-engine and dead-duplicate implementations must not get completion credit. Accept alternative valid internal naming.
2. **Repair authority:** unsafe project/dependency/framework/path changes remain terminal violations. Safe omitted/duplicate/misordered F# Compile entries are repairable project failures, not terminal policy violations. Preserve the failed first-submission outcome and let the existing repair budget operate.
3. **Feedback limit:** valid diagnostics exceeding the fixed intact-error allowance terminate that trajectory as feedback-budget exhaustion, not an excluded apparatus result or cancellation of unrelated scheduled slots. Genuine controller/security faults still stop the batch. Do not produce feedback after the last allowed submission.
4. **Budget/counting:** reserve before dispatch using the exact retained-chain input count or a demonstrated conservative bound and the intended service tier. Account for applicable cache-write premiums, no silent retries, and ambiguous-request reservations. Resupply fixed instructions on every response-chain call. Optional unsupported telemetry remains null.

At currently documented rates, using a conservative $0.25 per million input reservation and $1.20 output gives a generation envelope of **$1.2976128** for the maximum pilot, within the proposed $2 ceiling, and **$0.0360448** for two integration generations, within $0.05. These are proposals conditional on actual rates/access and successful pre-dispatch enforcement, not spending already incurred or an automatic run authorization. Model-request ceilings and ancillary HTTP/count calls are distinct; record both.

### Next bounded assignment

Implement the minimum E3a request/controller path and isolated evaluator needed for this specification, reusing existing materialization, accounting, pinned toolchain and remote transport. Add no new proxy, daemon, model-routing framework, worker agents or backend matrix.

Use injected mock transport for ordinary tests; do not issue a live model request. Demonstrate the corrected failure/endpoint rules, request lineage and instruction repetition, separate per-round usage, pre-dispatch budgets, complete attempt retention, development/holdout isolation, and fresh-binary evaluation. Perform model-free sandbox checks on the intended environment when available; a trusted local fixture build is not sandbox evidence.

Return with exact implementation/specification identities, regenerated review packet, relevant CI, security and budget tests, remaining live gates, and a short handoff. Ordinary fixes to reach these criteria can proceed in this assignment. Stop for a material new scientific/security requirement or repeated unresolved apparatus failure rather than adding layers.

### First submission, repair, and scoring

Preflight each predecessor against its existing contract before new-task interaction. Pre-restore locked dependencies with audit outside the loop. The candidate sees approved predecessor/current source, earlier/current contracts and allowed feedback, not successor code, future tasks, research findings or final holdout.

Capture a strict file-replacement submission, preserve the raw response, validate authority and apply deterministically. No human/model-side syntax cleanup is free. Format failures consume their submission; forbidden changes terminate as protocol failures; safe source/project mistakes can receive development feedback.

The controller owns the fixed no-restore build and declared development checks. Evaluate only the freshly built binary matching the submitted source. Never execute candidate code/project files with API credentials or writable scorer/host mounts. Maintain network, process, time, memory and output bounds, including descendant cleanup.

Development results alone control repair and stopping. A passing development submission stops even if the final holdout fails. Score first and terminal submissions after interaction against the sealed holdout and task-specific rubric; neither score returns to the candidate. An invalid terminal submission is not credited using an older applied workspace.

Use deterministic diagnostic packets with error codes/locations, intact context, stable ordering/deduplication and a fixed limit. Preserve full raw output separately. Packet length is a policy outcome, not a reason to exclude an inconvenient language observation. No LLM summarizer is part of this initial treatment.

The proposed memory policy is provider-response-chain. Verify actual counting/continuation in the later capped integration. Matching mock IDs proves plumbing only; do not silently fall back to fresh-context or transcript replay and label it equivalent. Record actual model/version information when exposed and do not switch aliases or reasoning settings silently.

### Outcomes and inference

Primary task-completion endpoint: first submission meets format, compilation, holdout behavior and all applicable declared task obligations. Report all components, architecture review availability/type, terminal completion, failure classes and resource phases separately. For task 007, build-plus-behavior alone is not enough. This correction is pre-freeze; historical outcomes are not rescored.

Retain all assigned and started slots, invalid/timeout submissions, budget-limited trajectories and missing scores. Known failure and unknown scoring are distinct. Successful first submissions contribute zero incremental repair cost in unconditional summaries. Conditional repair-only results are selected error populations, not the causal benefit of feedback.

Preserve actual provider usage and distinguish total input/output from their cache/reasoning subsets. Visible payload/source proxies do not claim exact hidden-state size. Report the four pairs per selected task, absolute paired differences and coverage; no universal-language or population-significance claim from three chosen tasks. Do not increase sample sizes after inspecting direction.

## Remaining live gates

The bounded implementation is followed by a separately capped integration, not an automatic full pilot. The proposed integration is at most two generations on an unrelated trivial task and must demonstrate account/model access, exact input counting/lineage, pricing guard, actual continuation semantics, usage reconciliation and intended sandbox evidence. If it changes the scientific policy, revise before freezing or collecting pilot outcomes.

Only after that evidence and explicit approval may the fixed 24-trajectory pilot run. Repository status flags, a review message or a generated hash cannot substitute for working enforcement. No live candidate generations occurred in this review/disposition change.

## After E3a: choose a branch, not every workstream

| Branch | Trigger | Scope |
|---|---|---|
| E3b/F0 | A practical command/feedback policy question remains. | Named policies with equal authority; no need to re-prove the blocked-audit delay. |
| Familiarity/localization | Initial-patch difficulty under clean tools remains unexplained. | Bounded documentation/API/interop/read-only intervention. |
| H | A paired scalable workload and auditable source budget can test the original question. | H0 model-free preparation then separately approved H1/H2 overlap pilot; **does not depend on F or G**. |
| G | Better precision would change a practical conclusion. | Fresh registered replication under a named ecology. |
| F | Evidence motivates orchestrator-context containment beyond deterministic policy. | Same-model inline versus isolated repair first; total and per-agent costs. Persistent history is a distinct later question, not dependent on a favorable fresh-context cost result. |

Use hygienic tools as existing controls without requiring a separate model-backed hygiene study before source-only H work. Do not demand exhaustive causal attribution before an experiment that eliminates repair feedback can test context behavior.

## Workload and governance rules

Broader claims need a defensible sampling frame and independent task/repository/authoring units, not many reruns of one example. F# token savings are hypotheses, not selection criteria. Conservative dependency closures are not proven simultaneous-memory requirements; interfaces and streaming may suffice. Native projects remain observational transfer evidence.

Review type must be explicit: current review is another AI session, not a human language expert. Unavailable evidence narrows the claim; do not invent sign-off or build interception frameworks merely to fill nonessential fields.

For a later authorized frozen batch, automated health checks can cover multiple blocks. Return at a material scientific change, anomaly, resource bound or scheduled handoff. No comparative-effect-driven extension. Reports/frozen protocols remain immutable; corrections are linked addenda. Reuse the canonical runner and keep scientific, code, environment and account-authorization identities separate.
