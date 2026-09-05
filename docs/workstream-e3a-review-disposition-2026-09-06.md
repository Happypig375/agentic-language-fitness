# E3a review disposition and implementation handoff

**Reviewed:** 2026-09-06. **Input commit:** `19b1902be59324b98741ccb6c3a8396de962f5f7`.

## Decision

Accept the narrow first-submission/bounded-repair design **for minimal implementation with the corrections below**. Preparation is no longer the next assignment. This is a second AI-session review of the Codex-authored packet, not human language-expert sign-off, proof of live integration, or authorization to run the 24-trajectory pilot.

The user requested continuation after the E3a review. Continue repository implementation within this bounded design; do not interpret that as evidence that account access, sandboxing, provider continuation, or the proposed spending guard already work. No candidate-model request was issued in this review.

The original `protocols/workstream-e3a-v1/` packet remains an identifiable reviewed proposal. It was not an executable freeze. Apply the specified pre-freeze corrections to the specification, fixtures, and generated packet together in the implementation change; retain this reviewed commit as provenance. Do not create a new remote runner or rewrite E1/E2/E2a or archived gold.

## What passed review

The proposed three tasks (001, 006, 007), one provisional Luna-high setting, four pairs per task, one initial submission and at most two repairs are a proportionate mechanism pilot. Keep its exploratory task selection explicit. There is no reason to add languages, more tasks, subagents, or another broad methods-review cycle now.

The shared initial submission, full-source/no-tools candidate boundary, separate development stopping and sealed final scoring, preserved invalid attempts, null missing telemetry, and distinction between mocks and live evidence are appropriate. Complete file replacements are acceptable for this tiny fixture, but the output format/scaffold is a treatment and results must not be pooled with historical Codex runs or generalized to economical patch editing.

GitHub Actions run `33972207924` on the reviewed commit completed successfully. Both Linux and Windows passed the E3a packet/trusted-fixture step and their required checks. This validates the checked-in fixtures, not an unimplemented API client or remote candidate sandbox.

## Oracle finding: accept the boundary, not the archived answer

Retain the task-001 Int32.MinValue holdout in both languages. The contract specifies integer priorities without excluding this value. The old F# target's negated sort key is a reference implementation defect, not evidence that the expected ordering should change. The existing trusted fixture correctly preserves and asserts this failure.

The suspected inherited defect in the later selected predecessors is **not present**: stage 005 uses `compare (priorityOf right) (priorityOf left)` and explicit ordinal tie-breaking instead of negation. The trusted target checks for stages 006/007 also pass this holdout. Do not add gratuitous predecessor patches or exclude the boundary to make archived targets all green. Add an explicit inherited-contract check at the selected predecessor boundary when regenerating the fixtures so this conclusion remains testable.

Gold names an archive, not a correctness oracle. Record a compiler-valid, contract-correct alternative for task 001 as a positive scorer fixture if needed; it is evaluator-only and must not become candidate-visible target code.

## Required corrections before an executable freeze

### R1 — Refactor completion must be observable in the task endpoint

Task 007 changes architecture while preserving behavior. Its predecessor can already pass the inherited behavioral holdout. `structural_development()` checks only filename/Compile order; an empty `OrderFlowEngine.cs` passes its C# filename check even when all dispatch remains in Program. The packet acknowledges that limitation but excludes architecture from the primary endpoint. Thus behavioral success alone must not be called successful completion of Task 007.

For the selected-task completion endpoint require all declared obligations: valid submission, build, behavioral holdout, and the task-specific contract. For Task 007 this includes the stated live extraction/IO-boundary rubric. Preserve build-plus-behavior as a separately reported endpoint comparable across tasks. A missing required architecture judgement makes task completion unknown, not true; a definite violation makes it false even if behavior passes. Cases with an already-known failing obligation are failures regardless of another missing component.

Use the already described blinded source rubric; record reviewer type and preserve first/terminal source. Do not invent a human reviewer or impose new private method/class names. A static check can cover declared file/order conditions but is not proof of live delegation. Scoring occurs after the trajectory and must not feed holdout information back into repair stopping.

Required regressions: unchanged predecessor; predecessor plus empty engine file; duplicated dead engine code with live dispatch still in Program; and an alternative genuinely extracted implementation with different valid internal names. The first three must not be credited as completed refactors; the last must remain eligible.

### R2 — Allow repair of safe project/compile-order mistakes

`apply_submission()` currently raises terminal `PolicyViolation` whenever F# Compile entries omit an allowed source, contain duplicates, or do not put Program last. That treats an ordinary F# implementation mistake differently from an ordinary C# compilation error and suppresses the very project-repair mechanism being measured.

Split safety from correctness. Unsafe external paths, imports/build targets, package/framework changes, property expansions, case collisions, and forbidden files remain terminal policy violations. A simple Compile entry referring to an approved root-level source but missing a file, duplicating it, omitting a required include, or putting it in the wrong order is a **repairable project failure**. Preserve the safe submitted snapshot and return deterministic development feedback within the existing repair budget. Do not compile known-invalid or unsafe project inputs merely to discover the error.

Apply this distinction also to malformed-but-repairable output versus forbidden XML constructs. Do not broaden the permitted project language beyond simple root-level source inclusion. Task-required engine extraction remains permitted; no manual repair of the candidate's project file is allowed.

Required regressions: omitted engine Compile entry, wrong safe order, duplicate safe include, and missing safe source are repairable; traversal, property expansion, extra targets/imports/dependencies, and changed framework remain terminal. First-submission project failure still counts as first-submission failure; a later repair does not retroactively turn it into success.

### R3 — Feedback exhaustion is not a reason to erase or stop unrelated observations

A valid diagnostic set can exceed the fixed feedback cap because of the candidate's output. That is a policy-resource limit, not automatically an apparatus malfunction. Keep the reviewed cap and intact-error rule, but terminate that trajectory as `feedback-budget-exhausted`, retain its known first/terminal outcomes and usage, and allow the remaining scheduled slots to proceed under the same rules. Do not exclude it or dynamically increase only one language's allowance.

A genuinely malformed controller packet, broken serialization, unsafe output handling, or unexpected provider behavior still stops the batch as an apparatus/safety issue. Keep these distinct.

Do not construct or test a feedback packet after the last permitted submission: there is no next recipient. The current simulator can otherwise change a final repair-budget stop into a batch-level feedback-cap incident for an unused message. Log raw output, but finish at the declared repair limit.

Required regressions: oversized valid diagnostic on an early round; the same output on the final round; warning-only overflow; and controller-format failure. Preserve every assigned slot and actual request count.

### R4 — Make the proposed ceilings real, without assuming cache writes are free

The reviewed arithmetic is correct at $0.20 input/$1.20 output per million: 72 requests capped at 32,768 input and 8,192 output yield $1.179648. It is an uncached-rate envelope, not a universal billing bound. Current official Luna documentation also lists cache-write charging at 1.25 times the uncached input rate. Reserving $0.25 per million for all input gives **$1.2976128**, still below the proposed $2 pilot ceiling; two integration requests give **$0.0360448**, below $0.05. These are candidate generation envelopes, not maintainer/reviewer/compute costs or confirmation of account access.

Implement Decimal-based pre-dispatch reservations with a pinned intended service tier and verified rate assumptions; retain an ambiguous request's worst-case reservation and never replay it automatically. If billing conditions cannot be bounded or rates change, fail before dispatch. Provider input/cache/output subsets must not be double-counted in observed usage.

The Responses input-token count endpoint accepts `previous_response_id`. Prefer a matching count over the exact instructions, new input, tools and retained chain rather than treating the `o200k_base` proxy as an exact cap. Resupply the fixed instructions on every chained request; the API does not carry prior instructions forward automatically. Verify count/create agreement in the later live integration, including effective reasoning-context behavior. Count endpoint/network calls separately; the 72 ceiling denotes generation requests, not every HTTP request.

Do not raise sample or per-request limits to consume the unused part of $2. If the authorized account cannot support this API model, stop rather than switching to a subscription-backed/scaffold variant silently.

## Bounded next implementation

Implement only the minimum no-tools request/controller path and isolated evaluator required by this packet, with transport injected/mocked in tests. Reuse source materialization, accounting, fixed toolchain image, and the existing remote transport. No new proxy, daemon, recursive agent, generic framework, or alternate backend matrix.

The implementation may update the still-unfrozen proposal and regenerated review identities to incorporate R1–R4. The original review packet's input commit is retained above. Do not leave a changed scientific specification with an old generated packet hash. Give the eventual executable a distinct code identity from the scientific specification and account authorization.

Required non-live evidence:

- a complete mock trajectory with initial and repair requests, no tool declarations, fixed instructions on every call, correct lineage, no silent retries, and separate round usage;
- development stopping unaffected by any holdout score, including malformed final submissions;
- safety-versus-project-correctness and Task 007 completion regressions above;
- pre-dispatch count/cost/deadline guards, reservation exhaustion, malformed usage and ambiguous timeout cases;
- no evaluator path fallback to trusted host execution; successful builds use only the new binary for the submitted hash;
- model-free sandbox probes for network, credentials, scorer visibility, source/cache write permissions, subprocess cleanup, time, memory and output bounds, on the actual intended environment when available;
- fixed report generation with all scheduled/started/unstarted slots and scored/missing/failed dimensions preserved;
- exact implementation-commit CI and a short evidence/limitations handoff.

Separate preparation from measured repair. Pre-restore against frozen dependencies outside candidate interaction; keep per-task/round cache and fixed-path policy explicit. Never mount target gold, scoring machinery, host credentials or the whole research repository into candidate execution. Candidate source and project files remain untrusted even when the model has no tools.

A network-disabled local environment may test pure helpers/mocks but cannot establish remote isolation. Report that limitation without changing the host profile or calling a local result a remote integration.

## Handoff after implementation

Stop after the minimum implementation and its model-free evidence are ready. The next live gate is at most the proposed two-request integration on an unrelated trivial task, with separately recorded account access, price/usage/counting semantics, response chaining and actual sandbox evidence. This disposition does not launch or certify it. Successful integration is not itself authorization for 24 pilot trajectories.

A completed E3a pilot, when separately approved, remains 3 tasks × 4 pairs × 2 languages, at most two repairs per trajectory. Its findings guide the next branch; H does not need to wait for subagent experiments or an aggregate-cost replication.

## Review evidence and limitations

Read through PLAN/AGENTS, the full packet and specification, candidate instructions, `src/alf/workstream_e3a.py`, `scripts/e3a_check.py`, and the relevant F# stage-005 predecessor. Verified reviewed-commit CI jobs, including trusted fixture validation, through GitHub. Locally reproduced the empty-engine filename acceptance and terminal missing-Compile classification using extracted decision-function probes and checked the budget arithmetic. Those probes were not a full local repository test run and did not execute candidate code.

This change records disposition and advances the canonical handoff. **R1–R4 are required implementation changes, not claims that the current pure helpers have already been corrected.** No new language-result inference, live model observation, or human review is claimed.

Primary API references rechecked 2026-09-06:

- https://developers.openai.com/api/docs/models/gpt-5.6-luna — documented rates and cache-write multiplier, not account entitlement;
- https://developers.openai.com/api/reference/resources/responses/subresources/input_tokens/methods/count — count request fields including retained-response ID and instruction handling;
- https://developers.openai.com/api/docs/guides/token-counting — pre-generation counting, not a substitute for pinned-account integration evidence.
