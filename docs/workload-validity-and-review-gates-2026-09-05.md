# Workload validity and review gates

**Revised:** 2026-09-05. Living companion to [PLAN.md](../PLAN.md); no experiment is authorized by this document.

## Fairness is relative to a claim

A controlled pair can test the contrast between two specific implementations under one model/harness policy. It does not isolate an intrinsic language property: architecture, idioms, library choices, author skill, and model familiarity remain bundled unless manipulated separately. A native open-source sample is not automatically representative either; selection, licensing, buildability, available tests, and ecosystem composition bias what can enter it.

Use separate layers with explicit scope:

- **Controlled paired:** the same behavioral contract and task, language-appropriate implementations, a common oracle, and controlled candidate authority. Causal claims concern assigned implementation/policy treatments under stated controls, not language in the abstract.
- **Native ecological:** sampled real repositories and accepted maintenance tasks. Stratification can improve comparability but does not remove all confounding. Report transfer evidence separately.

Tool/network treatments also remain distinct: hygienic pre-restored controls; intended online audit-reachable development; historical constrained-network audit-on. Formal strata can be modelled together only with explicit treatment terms and a justified target population, never silently collapsed into one language score.

## Sampling and practical scope

Define the target workload first: for example, maintenance of tested .NET business services, not all software engineering. List the source population, discovery/inclusion rules, exclusion reasons, and sampling unit. Use accepted issue/commit histories from both language ecosystems when feasible; record the information available before the fix, not just the final solution.

There is no scientifically established requirement that exactly half the tasks be real-derived or that every pilot include three domains. Replace those earlier quotas with a justified sampling frame, a provenance table, and an explicit limit on generalization. Equal F#/C# source-task counts are a balanced design, not an estimate of real-world prevalence. Freeze weights before outcomes if reporting a population-weighted result.

E3a deliberately samples a few diagnostic task types from OrderFlow. It may proceed as a mechanism pilot with a compact limitations record; it need not first construct a multi-domain representative suite. Broader claims later need independently authored families and suitable domain coverage, including both interop-heavy and native domain-model workloads. Do not select only tasks favorable to one language or choose pairs because F# happens to tokenize shorter.

Task records should include provenance/license constraints, domain, semantic change, API/compatibility requirements, relevant modules, error/concurrency/performance obligations, available documentation/tests, and transplant limitations. Newly authored tasks must be labelled as such. Public historical solutions may have entered training; record this contamination risk, hide future history/solutions during the run, and use untouched task/repository holdouts when practical. Renaming identifiers does not prove decontamination.

Calibration may guide a later explicitly exploratory design. Confirmatory data and outcome-driven task construction must stay separate. Many repetitions of one chosen task reduce stochastic uncertainty for that task, not uncertainty about the whole software population.

## Constructing and auditing pairs

Start from one language-neutral contract and independently implement it in ordinary, maintainable styles. Do not force equal lines, equal patch size, identical internal types, or identical graphs merely to appear fair. Do not let an idiomaticity argument excuse avoidable gratuitous complexity in either implementation.

Audit:

1. behavior, invariants, error handling, compatibility, and any declared nonfunctional requirements;
2. domain/module roles and meaningful dependency paths, distinguishing unavoidable language affordances from arbitrary author choices;
3. documentation information, library/API exposure, build inputs, and helper code visible to the candidate;
4. source and serialized-request size under a declared tokenizer/proxy;
5. equivalent oracle sensitivity to plausible semantic faults;
6. material asymmetries, authoring provenance, and what the comparison can actually identify.

A strict structural check is legitimate only for an explicit API/architecture requirement. Otherwise accept alternative correct implementations. Tests passing is evidence over the tested contract, not proof of equivalence for every possible input. Add property, differential, metamorphic, boundary, and fault/mutation checks where relevant; independent expected behavior is needed because both versions can share the same bug.

Keep the first candidate-visible state small enough to review. Scale one validated exemplar before building a large family. For population inference, later replicate across independently authored repositories, not only many sizes emitted by one generator. Generator descendants and repeated trajectories are correlated observations.

## Review evidence without fictional reviewers

Prefer language-expert review of each implementation and a separate paired-contract review, with reviewers unaware of new agent outcomes. Language itself cannot be blinded. Record reviewer identity/type, scope, criteria, findings, disposition, and limits on independence.

For a feasibility pilot, a documented AI-assisted review plus executable checks can be a provisional gate; call it that. It does not count as experienced human language-review evidence. Missing expert review limits external/idiomaticity claims rather than requiring agents to manufacture a sign-off or endlessly recruit unavailable reviewers. Broader claims should seek genuine expert scrutiny.

Classify findings by consequence: validity/security/measurement blockers must close before the affected run; material uncertainties require an explicit maintainer disposition or a narrowed claim; cosmetic suggestions do not block unrelated work. Merely assigning a P1/P2 label is not a substitute for explaining its impact.

## Information separation

Candidate-visible material consists of the approved predecessor, current task, public/development examples, and permitted tools. The candidate must not see the current target/successor gold, future tasks, research hypotheses/results, or final holdout examples.

Development feedback and final scoring are different systems. A final hidden test's pass/fail bit can leak through whether the controller requests another repair, even if its assertion text is never shown. Therefore both feedback and stopping use development checks only; holdout scoring never changes the trajectory. Final-case identities and outputs remain unavailable to candidate code and prompts.

Evaluation runs candidate code and build files in a restricted sandbox. Store the scorer outside it; do not mount secrets, target code, or the full research repository. Authentication needed by the model adapter must not be readable by candidate shell/code. Record the actual isolation mechanism, not just an instruction to behave.

## Context-study fairness

Use the [H design](workstream-h-context-pressure-design-2026-09-05.md). The primary paired contrast fixes the semantic task and budget. Occupancy is measured, not enforced by making one language solve a larger task. Equal-occupancy plots across different semantic scales are descriptive unless task difficulty is separately controlled.

Task-relevant annotations are reviewed evidence sets, not a unique minimal transitive closure. Interfaces, valid alternative solutions, and compact summaries may remove any need to load entire implementations. Source relevance metrics should allow multiple sufficient paths and report annotation uncertainty.

Preserve meaningful names. Evaluation-only semantic mappings must not give the candidate an oracle telling it where the change belongs. Retrieval tools use comparable indexing, token caps, and access; preprocessing and language-service advantages are measured, not assumed equal.

## Proportionate review packet

For E3a, reuse the existing contract and predecessor artifacts. Add only: task/selection rationale; known pair asymmetries; development/holdout split; fault checks; candidate authority; continuation policy; observability; budget/schedule; failure rules; and unresolved review findings.

For a new H family, additionally provide the sampling frame, one paired exemplar, provenance, task/reference maps, representation measurements, evidence for realistic scaling, and bounded construction/run costs. Extend the packet as claims grow; a twelve-part dossier is not required as a separate document for every minor fixture change. A completed dossier is evidence, not a certificate of representativeness.

## Autonomous progress and review cadence

Use bounded work packets tied to decisions:

| Packet | Allowed progress | Handoff |
|---|---|---|
| Design/preparation | Current specification, small exemplar/fixtures, model-free checks, risk and budget proposal | Before live candidate requests or large implementation expansion |
| Approved implementation | Minimum apparatus for an accepted design, tests, independent review when available, immutable identities | Before experimental execution |
| Authorized integration/calibration | Only capped registered probes/batch, audit, fixed descriptive report | Before design changes or formal collection |
| Authorized formal collection | Agreed frozen batch with automated protocol/resource checkpoints | At its declared endpoint, anomaly, or budget limit |
| Analysis | Frozen analyses and clearly labelled exploration, reviewable interpretation | Before a successor treatment or unregistered extension |

The user may authorize several operational blocks under one immutable protocol. Human review after every pair or macroblock is not inherently required and can increase temporal/provider drift. Block boundaries still support automated validity checks and checkpoints. Keep comparative effects out of extension decisions unless a valid sequential rule was preregistered. A run agent may produce the fixed audit/report; it must not tune the benchmark from that report.

Review readiness, scientific approval, executable freeze, and permission to spend model quota are separate statuses. Record what is actually established. Mocked sessions test plumbing; a real backend continuation/telemetry check requires a separately capped authorization. Existing maintainer reasoning is not a forbidden experiment, but extra model jobs and new review agents still need an authorized budget.

## Current assignment and stops

The next task is E3a review-ready preparation, as specified in PLAN.md. No live candidate run is authorized. Keep ordinary tests/CI repairs inside that assignment; do not broaden into tool-policy trials, multi-agent routing, or H execution.

Return for a new scientific condition, unknown material measurement semantics, unavailable required permissions, exhausted budget, data leakage, unsafe execution, or repeated unresolved apparatus failures. Stop when the packet is review-ready. A missing nonessential telemetry field should narrow a claim, not trigger an elaborate interception framework. If the missing field is essential to the intended estimand, do not run that treatment until it is resolved.
