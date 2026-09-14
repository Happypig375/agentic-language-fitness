# Prospective architecture trade-offs under agent maintenance

**Revised 2026-09-14; proposal pending human disposition.** This is the standalone scientific proposal linked by [PLAN.md](../PLAN.md). The preceding edition is retained at Git commit `d0cd99757c45d2a2322beb4c6f9069efe5667166`. The [focused review](pro-review-design-discrimination-2026-09-14.md) and [source audit](pro-review-design-discrimination-sources-2026-09-14.md) explain this revision. No construction, model call, sample allocation or freeze is created here.

## 1. Question and useful contribution

Can source-grounded predictions about responsibility ownership and interaction boundaries anticipate which future changes a coding agent will implement reliably, and how does inherited code state alter that suitability?

The intended product is a bounded, testable account of **architecture × change demand under a stated agent policy**, not a leaderboard declaring one language, engine or paradigm best. An architectural argument should predict a concrete coordination burden and a possible failure before the candidate acts. A result contradicting that prediction is useful; a post-hoc story explaining whichever package wins is not.

The original motivation included language-enabled abstraction, compact representations and protection of high-level reasoning from repair history. Keep that motivation traceable without substituting one component for the entire hypothesis:

- This proposed same-language case studies organization/package suitability.
- Fixed reference-predecessor comparisons study sensitivity to the inherited starting state.
- A future assigned feedback/history intervention can study repair insulation.
- A future source-budget/scale intervention can study fit and retrieval.

These are related questions, not a required factorial. The completed small-repository work and this proposal do not establish a physical-window limit or a causal training-frequency explanation.

## 2. Closest work and the remaining decision-value question

This is a scoped synthesis, not proof that no prior study exists. Exact versions, reading extents, access limits and deferred leads are in the source audit. Earlier broader ledgers remain relevant.

| Primary predecessor | Consequence for this study |
| --- | --- |
| ALMA, Bengtsson et al., JSS 2004, DOI `10.1016/S0164-1212(03)00080-3`, especially sections 4.3 and 7 | Scenario-based architectural comparison is established. Distinguish likely maintenance from deliberately discriminating stress scenarios and state whose decision is served. |
| Code-cleanliness minimal pairs, arXiv `2605.20049v1`, sections 2–3 and 6 | Controlled source-quality variation already exists and includes changes beyond formatting. Do not claim novelty merely for varying code organization before downstream tasks. |
| CodeThread, arXiv `2606.21804v1`, section 3 | Later maintenance on alternative predecessors with observable preconditions is already studied. Passing a finite predecessor suite is not proof of complete semantic equivalence. |
| SlopCodeBench, arXiv `2603.24755v2`, iterative protocol and construction sections | Fresh conversations with inherited code and evolving specifications are established; our added question must be prospective architectural suitability, not chaining alone. |
| ChainSWE, arXiv `2607.02606v1`, sections 3 and 4.1–4.4 | Oracle prior fixes, fresh/persistent inherited state and subagent interfaces already coexist. Reuse their control logic; neither a clean-predecessor control nor delegation is our invention. |
| Type-Error Ablation, arXiv `2606.01522v2`, sections 3–6 | Detailed current type feedback can help in its small, single-error Shplait setting. Do not equate all diagnostic text with harmful context or treat removal of repair as successful insulation. |
| Complexity Trap, arXiv `2508.21433v3`, sections 3 and 5–6 | Simple observation masking is a strong baseline; its scope, tuning and hybrid/generalization results prevent a blanket rule that summaries or workers must help. |
| Sambu et al., ICSA 2026, DOI `10.1109/ICSA66085.2026.00033` | The official abstract already describes LLM-generated architectural decompositions evaluated against reference systems. Full methods remain unreadable in this pass; do not claim architectural generation/evaluation is unstudied. |

The existing ledgers additionally cover NITR, specification-memory, functional-UI and game-engine benchmarks. They are not discarded; this pass does not upgrade their previously recorded reading/access levels.

The useful remaining question is whether **predeclared responsibility/interaction predictions add explanatory and practical value beyond a fixed package preference, ordinary source-size differences and initial generation reliability**, when common future obligations are implemented over inherited states. A chosen pair can test and falsify these predictions locally. Establishing a portable architectural mechanism needs independent cases or a narrower intervention later.

It is not enough that Nu has not appeared in a benchmark. Before scaling, the case must supply a decision that a maintainer could make differently depending on the outcome, a credible alternative explanation, and an observable result that could contradict the architectural prediction.

## 3. Provisional case and architecture as a bundled treatment

The provisional pair is Nu's F# MMCC and ImSim Breakout examples at `bryanedds/Nu@064f7ae92a8506689cd91aff5e6804a375d6ef3d`:

```text
Projects/Breakout Mmcc/Gameplay.fs
Projects/Breakout ImSim/Gameplay.fs
```

The preceding source review identifies explicit gameplay-model/manual motion responsibilities in MMCC and screen/entity-property plus dynamic-physics responsibilities in ImSim. Both use effectful engine facilities. These are concrete packages, not pure functional versus imperative programming. Sharing language and engine reduces some differences but does not equalize APIs, physics, documentation, authoring quality or the model's familiarity with each idiom.

A0 must re-establish the editable application boundary, read-only engine facilities and live observations on the actual pinned runtime. Nu versus Unity is not the control. Do not substitute a toy physics engine, manufacture an intentionally weak comparator or erase the organizational difference just to make assertions easy.

Common obligations need not require identical floating-point trajectories. They do require meaningful equivalence of the chosen gameplay behavior, with nondeterminism, input timing and tolerance rules decided before inspecting comparative candidate outcomes. The observation seam should expose state/events, not implement the feature or provide the candidate a hidden reference algorithm.

Baseline information must be audited: source, project metadata, comparable documentation, engine API facilities, generated code and defaults. Additional help for an unfamiliar API is a treatment, not a free repair of fairness after results. Match requirements and evidence, not necessary edit effort, file count or state representation.

## 4. Prediction records and manipulation checks

Before implementing each A0 witness, record:

| Field | Required content |
| --- | --- |
| Requirement | Observable change and retained obligations, with provenance and whether expected or stress-selected. |
| Source mechanism | Current owner of the relevant state/invariant, interaction/effect boundary, and plausible coordination path. |
| Prediction | Package A advantage, package B advantage, tie or genuine uncertainty; expected obligations or failure classes, not a guaranteed ranking. |
| Rival | An alternative such as missing API, source size, baseline defect, format burden, guidance or unfamiliar convention. |
| Disconfirmation | What actual source/behavior would contradict the predicted mechanism or show the witness cannot distinguish it from the rival. |
| Evidence timing | Source revision, analyst identity/type, prediction time and any later revision. |

Choose contrasting pressures and identify an adverse or no-differential expectation. This does not require adding a third chain or forcing one win for each package. Where a cheap source-size ranking and the architectural prediction disagree, the disagreement is informative; source size is an explanatory rival, not a correctness criterion. Do not fit a large prediction model to two chains.

A0 witnesses are feasibility evidence, not independent candidate confirmation. If the same authors refine scenarios while building witnesses, retain the original prediction and label the refinement. A1 freezes the final requirements, interpretations and predictions before candidate outcomes; seek a separate challenge reviewer when available and record actual independence. Never invent expert sign-off.

Document the organization actually present at baseline and after edits. Candidate reorganization is an outcome: initial package assignment remains the primary treatment. Do not discard runs that adopt another pattern or reward preservation of a preferred style when behavior is wrong. Unannounced architectural taste cannot enter the hidden oracle. Declared API/structural requirements must be public and allow alternative valid implementations.

## 5. A0 and A1: smallest useful construction

**A0, only after explicit approval:** run both unchanged baselines; produce a responsibility/state/effect map and safe common observation; implement at most two contrasting reference changes per package. This is two baselines and at most four successors, not all future episodes. Return a bounded yes/no/redirect conclusion.

A0 is successful only if the selected obligations are live-testable, the claimed organizational contrast remains real, and at least one consequential prediction is distinguishable from a trivial implementation/API mismatch. Runtime executability alone is insufficient. If a substantial replacement engine, new runner family or task-solving seam is required, stop and redirect rather than growing apparatus.

**A1, separately approved:** propose two four-episode scenario chains, each starting from its own copy of the baseline. Author source-bound requirements before reference successors; record realistic versus stress-selected scenarios. Requirements may introduce new behavior, revise an earlier obligation or impose a future interaction. Use stable IDs and explicit supersession. Do not author all tasks merely to make one architecture's known convenience dominate.

Reference solutions demonstrate feasibility, not unique allowed edits. Add fault/property checks for omissions, state ownership, ordering, lifecycle or error behavior relevant to the chosen contracts. Build and test success is evidence over these obligations, not equivalence for all programs or inputs.

A1 must choose the claim level and controls in section 8, finalize a finite sample/allocation proposal, and return before live execution. More independent cases are required for population claims; repeated seeds of the same two chains are not new architecture samples.

## 6. Proposed candidate policy and information boundaries

The currently proposed minimal policy is **source-only fresh episode context, one submitted edit, no execution feedback and no repair**. Each episode receives the actual safe inherited source, current and earlier requirements, and the same approved engine/documentation exposure policy. Candidate notes are off; source comments are still source. Persistent conversations or notes-on are separate future treatments.

Safe submitted code persists even when noncompiling or behaviorally wrong. The controller does not replace it with gold. Invalid output preserves the previous safe state according to the frozen submission rules. Unsafe content is contained and classified; later unexecuted slots are not fabricated model outputs. A file-replacement or patch interface and its output headroom must be checked for the actual workload before freezing; no language/package should fail primarily because the chosen carrier cannot express the expected change.

Candidates do not receive the architectural predictions, research hypotheses, comparative results, target solutions, future tasks or scoring details that would reveal hidden expected changes. The evaluator observes after submission and never supplies holdout scores, retry decisions or hints. Baselines, code, project files and test programs run under the existing reviewed safety model; credentials/scorer data remain outside candidate control.

One-shot/no-repair is an intentionally restrictive maintenance policy. It does not simulate a developer with isolated compiler repair. A wrong earlier patch may dominate later behavior. This restriction is acceptable only with an explicit policy claim, not as evidence that syntax/tool feedback has been controlled away while its benefits remain.

## 7. Outcome state, obligations and costs

Observed submission completion requires a valid artifact, successful build and all applicable declared obligations. Known failure makes joint completion false; absence of a required observation with no known failure makes it unknown. Compiler failure blocks runtime assertions rather than proving each executed and failed. Distinguish program-caused runtime failure from apparatus inability to observe it.

Keep observed outcome, execution status and assigned-policy utility separate. A predeclared policy utility can give candidate-induced unrun slots zero, but their observation stays `not_run`. Infrastructure missingness remains unknown and enters bounds. Missing tokens never erase a known behavioral score; incomplete usage retains coverage and may pause dispatch when remaining resources cannot be bounded.

For each versioned obligation report:

- new required behavior not implemented;
- a previously passing retained obligation newly lost;
- persistent inherited failure, not counted repeatedly as a new regression;
- recovery;
- explicit supersession/retirement;
- blocked or unavailable observation.

Report joint completion, new-obligation completion, retained obligations and these transitions by episode. Test assertion counts are not independent task samples or weights of requirement importance. Reference/source drift annotations explain possible mechanisms; they cannot by themselves establish the cause of a failure.

Retain first/terminal source identities, safe-state transitions, all assigned slots, actual submissions, provider status/usage and timing. Separate authored source, visible envelope, active context when observable, output, direct controller execution and total cost. Preserve partial/ambiguous attempts; no blind retries or retrospective exclusions. There are no workers in the minimal policy, and no claim that generation-only measurements include all human/maintainer costs.

## 8. Choose the inference level before collecting outcomes

### 8.1 Minimal inherited case

Without another starting-state condition, estimate **architecture-package robustness under the assigned no-repair policy**. Do not claim that latent architectural degradation caused later failures, or that repair-context insulation improved maintenance. Obligations and failure classes diagnose the pattern but do not supply an absent counterfactual.

### 8.2 Recommended control for the stronger inherited-state claim

Predeclare a small set of later sentinel tasks and, for each package and paired block, run the identical requirement from that package's validated canonical reference predecessor as well as its naturally inherited state. Specify sentinel positions before outcomes, include both packages and all assigned histories, and never select only failed or successful candidate predecessors. The inherited arm is not reset or repaired by this scoring control.

At a fixed sentinel, describe both package contrasts:

```text
D_inherited = outcome(A, inherited) - outcome(B, inherited)
D_reference = outcome(A, reference) - outcome(B, reference)
history_sensitivity = D_inherited - D_reference
```

These compare assigned starting-state policies. They do not identify a pure architectural-damage variable, correct for all behavior differences or measure the causal fraction attributable to architecture. A missing feature in the inherited predecessor can explain a gap; report that, rather than relabel it as hidden maintainability. Reference implementations themselves are choices requiring the same contract review.

A1 must either include this bounded control for the stronger claim or explicitly choose the narrower case title/conclusion. It may not collect the minimalist design and later promote its interpretation because the result is attractive. Sentinel generations must be included in the revised allocation, preferably by rebalancing sample size; they are not free additions to 192.

### 8.3 Feedback/context hypothesis remains distinct

Useful evidence about a current error is different from old resolved diagnostics or obsolete source. Type-Error Ablation [6] cautions against stripping necessary information; Complexity Trap [7] supplies simple history-management competitors. ChainSWE [5] already combines sequential state with memory/subagent modes. No generic claim that delegation solves long-horizon maintenance is available to this proposal.

A later economical discriminator is an **identical-source handoff**: both fresh planner conditions see the same corrected source, same next task and same concise resolution facts; one additionally sees authentic resolved repair history. Any masking or summary content, size, placement and permissions are frozen. This isolates history presentation conditional on that source, not the value of performing repair, native persistent hidden state or the quality of a worker's different patch. It remains unallocated and is not added to A0/A1 automatically.

Only a subsequent actual repair-routing comparison can estimate the system benefit of delegation. Keep the same model/authority initially, retain useful current diagnostics, compare a simple deterministic history policy, and record orchestrator, worker and total costs. A lower planner token count is not evidence of lower total cost. These follow-ups need their own novelty/control review and may be unnecessary if the architecture case already answers a useful narrower decision.

## 9. Sampling and analysis proportional to this case

The earlier planning arithmetic is 12 blocks × 2 packages × 2 chains × 4 episodes = 192 generations, plus up to five unrelated integration generations. It is unallocated, not a power result or a promise to execute that many. A0/A1 determine the actual useful contrast, controls and worst-case cost before approval. A narrower sample is legitimate when the decision is feasibility; do not call it confirmation.

Each complete block contains all package/chain trajectories. Counterbalance their chronological order; keep the declared episode order within each chain. Keep resource/model/policy identity fixed, record temporal/provider changes, and pause for a material identity change rather than replacing an inconvenient run. A schedule seed does not seed model randomness.

The default descriptive summaries retain every episode and block. For a declared assigned-policy score Y, the chain score is the mean of its episode scores, the within-block package difference is paired, and any overall summary uses explicit equal-chain weights. These are selected-scenario weights, not estimates of deployment prevalence. Report chain-specific contrasts even if averaging cancels them. For partial blocks provide missing-outcome bounds and coverage rather than complete-case-only rankings.

Prospective prediction agreement is described at the scenario level with contradictions and alternative explanations. Twelve repeated trajectories do not provide twelve independent tests of an architectural theory. With only two chosen chains, do not fit a large architecture × domain × model interaction, claim calibrated predictions or transport a p-value to all software. Degenerate resampling is not certainty; non-significance is not equivalence. No effect-driven extensions.

A result favoring either package can be useful. Evidence is stronger when the predicted responsibility/obligation pattern appears, not merely when a favored name has a larger average score. If only baseline API differences, format failures or a uniform initial-generation advantage explain the result, report the package-policy finding and redirect mechanism claims. A null result is not a reason to search for favorable workloads indefinitely.

## 10. Readiness, research loop and next action

The positioning loop and execution loop are separate. This review supports a bounded **A0 decision**, not an approved executable study. The next packet should show case credibility, pre-witness prediction cards and a limited implementation cost; it should not reopen every historic research direction or require another large literature count.

A0 returns before A1; A1 before apparatus/allocation; B0 before live integration; B1/B2 follow only explicit approvals. Use the existing runner, scopes and five-unresolved-failure rule in PLAN/AGENTS. No additional adapter, engine, proxy, subagent or sample is created by a prose revision.

The latest scite audit recovered close methods and contrary evidence, but a broad discovery prefix and incomplete citation coverage cannot establish global novelty. The ICSA refactoring paper's full methods and graph-derived context-policy neighbors remain specifically deferred. Revisit them before claiming novelty in those subdomains, not before every routine engineering fix.

## Primary source routes

[1] ALMA: https://www.cs.vu.nl/~hans/publications/y2004/alma.pdf

[2] Code cleanliness: https://arxiv.org/html/2605.20049v1

[3] CodeThread: https://arxiv.org/html/2606.21804v1

[4] SlopCodeBench: https://arxiv.org/html/2603.24755v2

[5] ChainSWE: https://arxiv.org/html/2607.02606v1

[6] Type-Error Ablation: https://arxiv.org/html/2606.01522v2

[7] Complexity Trap: https://arxiv.org/html/2508.21433v3

[8] ICSA official abstract: https://conf.researchr.org/details/icsa-2026/icsa-2026-papers/27/LLMs-for-Architectural-Refactoring-An-Exploratory-study-on-Monoliths-to-Microservice

See the source audit for edition checks, selected sections actually read, scite access/graph coverage and excluded/deferred records. These sources motivate the controls; none establishes an ALF architecture effect before the proposed study is run.
