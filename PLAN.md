# Research plan

**Reviewed:** 2026-09-05. This is the canonical plan for future work, not an execution authorization. Historical results and frozen protocols are unchanged.

## Start here and document authority

Read this file first. `AGENTS.md` is a short maintainer entry point, not a second scientific plan.

- Current design/analysis rules: [experimental design](docs/experimental-design.md) and [metrics](docs/metrics.md).
- New workloads and review boundaries: [workload validity and review gates](docs/workload-validity-and-review-gates-2026-09-05.md).
- Future context experiment: [Workstream H](docs/workstream-h-context-pressure-design-2026-09-05.md).
- This correction pass: [plan review](docs/plan-review-2026-09-05.md).

Dated E/D proposals and review notes explain earlier decisions; they do not override these current documents. An explicitly authorized, frozen protocol governs its own run. A conflict between that protocol, a new instruction, and this plan requires review, not silent reinterpretation or retrospective changes to collected data. Repository documentation alone cannot authorize experiments.

## Accepted evidence and limits

Workstreams A–C and D v3 are closed. E1, E2, and E2a are complete within their recorded boundaries:

| Evidence | Finding | Boundary |
|---|---|---|
| [D v3](docs/workstream-d-v3-calibration-disposition-2026-09-03.md) | Ten non-counting calibrations completed all eight tasks; exploratory F#/C# input and agent-time ratios were near 1.38. | Five pairs from three configurations, not a confirmatory language estimate. |
| [E1](docs/workstream-e1-v3-forensic-disposition-2026-09-03.md) | F# had more observed build failures, repair cycles, and project-file changes. | Failed builds include dependency/environment failures; first-build boundaries were sometimes unavailable. |
| [E2](docs/workstream-e2-toolchain-disposition-2026-09-04.md) | Source-token proxies and program execution were near parity; offline tool timings differed. | Different host/command ecology from v3. |
| [E2a](docs/workstream-e2a-disposition-2026-09-04.md) | Host-aligned replay confirmed more F# dotnet invocations, slower builds, and a large blocked-source NuGet-audit amplifier. | Gold-state timing replay is not causal mediation of agent time or tokens. |

Reports remain in `reports/`; retain their original hashes and provenance. Do not rewrite historical artifacts to fit the new interpretation.

The leading hypotheses are first-patch source/type/project difficulty, feedback-driven repair, and environment/tool amplification. Inspection counts alone cannot establish equal comprehension. Aggregate input is repeated trajectory usage, not unique source or peak context. Current small-repository observations cannot estimate a language-by-scale slope, a future crossover, or an intrinsic language property. A linear intercept/slope sketch is only intuition, not an identified model from these observations.

Keep three tool ecologies separate: controlled pre-restored/audit-off; intended online audit-reachable development; and legacy constrained-network audit-on. The last is historical/stress evidence, not a universal default. Dependency security checks remain outside the controlled repair loop; disabling audit in a benchmark is not a recommendation to abandon auditing in production.

## Current authorized scope and next handoff

**Next bounded assignment: make E3a review-ready without live candidate-model requests.** Prepare the specification, selected-task audit, minimal deterministic controller fixtures, and model-free validation needed to review feasibility. Reuse existing runner/accounting components. Do not build E3b/F0, a generic agent framework, or Workstream H in this assignment.

Produce a review packet with the proposed task IDs, one model/effort setting, sample and spend ceilings, repair budget, feedback policy, first-patch application rules, analysis table, source/fixture identities, and exact CI status. Resolve ordinary implementation defects within that scope; return when the packet is ready or a material blocker remains. This plan review is not independent approval of an E3a protocol that has not yet been written.

A mock can establish controller behavior and session-ID plumbing, not prove live provider continuation. Mark live continuation and provider-specific usage semantics pending. A subsequent explicitly authorized, bounded integration/calibration stage may verify them; if its result requires a scientific change, stop and revise before collecting the pilot. No self-issued approval or `freeze` file grants permission to run.

## E3a — Controlled shared-prefix first patch and bounded repair

### Question and sampling

For matched canonical predecessor states under one fixed controller policy, estimate first-patch correctness and the subsequent resource burden of bounded repair. This is a mechanism-enriched, non-confirmatory pilot, not representative maintenance or lifetime cost.

Select a minimal set from existing tasks: a low-diagnostic additive task, a type/validation task, and a multi-file/API task. Document archived evidence and all selection decisions. Do not enlarge the set or choose replacements after seeing new language outcomes. Historical Luna-high is a provisional setting only; verify the exposed model/effort and record actual version information before execution. No silent model substitutions.

Candidates may receive the approved predecessor source, including a predecessor obtained from the gold archive. They must not receive the task's target/successor solution, future changes, research instructions, prior comparative outcomes, or final holdout cases. F#/C# syntax cannot be blinded; the research hypothesis and treatment labels can.

### One common trajectory prefix

1. Outside candidate interaction, materialize and preflight the predecessor against its own existing contract, not the new feature tests. Pre-restore the locked dependencies with audit out of the edit loop.
2. Provide identical task information and authority, with language-appropriate paths. Permit only reviewed source-inspection operations. No candidate build/test execution, hidden language-server diagnostics, network access, or unbounded shell bypass in this controlled arm.
3. Capture one submitted patch or workspace diff. Multiple internal edits before submission are permitted only under the frozen protocol; no execution feedback is supplied before submission.
4. Apply it deterministically in a separate sandbox; preserve the original submission. Invalid patch format/application is an output failure, not an uncharged harness repair. Do not manually fix candidate patches.
5. Run the fixed controller build with `--no-restore` and the declared development checks. Remove stale outputs and demonstrate that evaluated binaries correspond to the submitted source. Preflight failures are apparatus failures; a candidate's forbidden dependency/framework changes are protocol violations, not excludable infrastructure accidents. Permit task-required source-file/compile-order changes explicitly.
6. Continue only submissions failing the **development** stopping criterion, for the frozen repair-round and total-resource budget. Return versioned compiler/development-test feedback. A submission passing development checks stops even if it later fails the final holdout.
7. Score the first submission and terminal submission with a separate, sealed final holdout. Holdout outputs, examples, pass/fail bits, and stopping decisions never enter candidate feedback. Run holdout scoring after the trajectory or through an isolated scorer that cannot affect continuation.

The one-shot endpoint is the shared prefix, not a separate stochastic run. Record incremental repair cost as the resources after first submission. This is not a causal estimate of the benefit of feedback versus extra thinking; that would require a separately randomized continuation control. Conditional-on-failure repair comparisons have selected different error populations and are descriptive.

### Feedback, authority, and memory

The specification must partition development-feedback tests from final holdout tests. Public task examples may be in the development set. The holdout needs independent cases and fault/property checks; it cannot be a renamed copy of the feedback set. Score declared API/structural obligations only; never demand canonical internal layout without stating it in the task.

Use deterministic diagnostic extraction, stable ordering, explicit truncation markers, preserved error codes/locations, and a fixed token/size cap. Preserve full raw output externally. Do not use a new LLM summarizer in this first treatment. Add checks that a larger F# diagnostic set is not silently deprived of essential information by the cap.

Freeze the memory treatment: same-session continuation with preserved provider state, explicit transcript replay, or fresh-context repair. These are distinct. Verify live behavior during an authorized integration stage; do not claim hidden-state equivalence from matching text or a thread ID alone.

Candidate-written code and project files are untrusted execution inputs. Evaluation stays sandboxed with resource limits and without model credentials, host mounts, future gold, or writable scoring machinery. Authentication is infrastructure-only, never candidate-readable.

### Outcomes and budget

Use one primary endpoint: **first-submission joint build and final-holdout behavioral correctness**. Separately report patch-format, compilation, declared API, development-test, and final-holdout outcomes; terminal correctness; failure categories; and resource use.

For every trajectory and round retain observable input/cache/output/reasoning categories, submission identity, controller tool time, raw and candidate-visible feedback volume, status, retries, and timeouts. Do not sum provider token subsets twice. Keep unsupported fields null and distinguish provider totals from visible-text proxies. Record actual attempts, including those with invalid accounting.

Before requesting execution, freeze the number of task pairs/repetitions, order schedule, maximum model calls, per-request/per-trajectory output and time budgets, spend or subscription-usage ceiling, retry policy, and stop rules. Finite worst-case usage must be calculable. No live request, including a capability or continuation smoke test, is free merely because it is non-counting.

Report all valid assigned trajectories jointly with correctness. Successful first submissions contribute zero incremental repair cost to the unconditional summary. Retain failed/timeout trajectories and missing observations; do not select only successful chains or repair successes. Use task-paired summaries with uncertainty; three selected tasks do not support a universal language effect.

## After E3a: choose a branch, not every workstream

| Branch | When justified | Scope |
|---|---|---|
| E3b/F0 tool-policy intervention | A practical command/feedback policy comparison would answer a remaining question. | Compare named policies with equal authority; one policy change at a time where attribution matters. No need to re-prove the already measured audit delay. |
| Familiarity/localization follow-up | Initial patch failures remain unexplained under clean tools. | A small specified documentation, API/interop, or read-only intervention; distinguish changed evidence from model capability. |
| H context study | A scalable paired workload and auditable source budget can test the original hypothesis. | H0 model-free preparation, then a bounded context pilot after separate review. **Not dependent on F1/F2 or completion of G.** |
| G small-workload replication | Precision or replication would change a practical conclusion. | Fresh registered data in a named ecology; not a mandatory detour before H. |
| F repair isolation | Evidence specifically motivates orchestrator-context containment and simple policy is insufficient. | Same-model isolated versus inline repair first, with total and per-agent accounting. Persistent context is a later distinct question, not contingent on a favorable fresh-context cost result. |

E2a already motivates hygienic tools for all controlled experiments. Making those controls usable does not require running a separate model-backed hygiene study. Do not require every hypothesis to be explained before testing source/context behavior without repair feedback.

A later repair-routing experiment must separate smaller orchestrator context from lower total cost. Externally retained state, worker calls, summaries, and rereads all cost resources. Do not add recursive workers, dynamic routing, new proxies, or compatibility frameworks speculatively.

## Review and execution boundaries

Use one bounded authorization packet, not an arbitrary duration or commit count. Distinguish review readiness, scientific acceptance, frozen executable identity, and execution permission. Completing one does not imply the others.

For a frozen authorized batch, the agent may execute the agreed batch and produce the predeclared audit/descriptive report. Human review is required at scientific changes, resource limits, integration failures, or the planned end—not automatically after every pair. Operational checkpoints may be automatic; keep comparative results masked from decisions to extend formal collection unless a sequential rule was registered. No outcome-driven sample extension or redesign inside execution.

Ordinary tests and CI fixes can continue within scope. Repeated failures of the same unresolved apparatus class should trigger a stop rather than a new layer. A pending CI run is pending, not success; only applicable checks need to be rerun for documentation-only changes. Experimental execution requires the approved exact code/specification identity and required checks.

## Non-negotiable evidence rules

- Reports and frozen experiments remain immutable; corrections are labelled and linked.
- Matched implementations estimate a particular implementation/model/harness contrast, not pure syntax or an intrinsic language effect.
- Whole-repository size, conservative dependency closure, actual working context, cumulative tokens, and relevant information are different quantities.
- F# token savings and long-context benefits are hypotheses, not inclusion criteria. Near-window success may fail before the hard cap; over-window tasks may be solved by contracts or streaming.
- Native-repository evidence needs a sampling frame and remains observational. A public repository is not automatically representative.
- Development-agent review may be AI-assisted but is not automatically independent human expertise. Record reviewer identity/type, evidence, limitations, and unresolved objections.
- Reuse the canonical runner. V4–V13 are apparatus history; do not restart version inflation. Change frozen candidate-visible policy only through a reviewed new scientific specification.
