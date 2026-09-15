# Predicting architecture-package suitability for coding-agent maintenance

Research proposal for human review · 15 September 2026

## 1. Introduction

A maintainer choosing between two implementations needs to know more than whether each works today. The useful question is whether each implementation will accommodate the changes the application is expected to undergo. When a coding agent performs those changes, a package that initially passes its tests may still be difficult to extend without losing earlier behavior. Existing studies already examine this problem: CodeThread compares later maintenance of human and agent predecessors, SlopCodeBench follows agents through evolving requirements, and ChainSWE compares successive bug fixes under different predecessor and memory conditions. Their results make downstream maintenance an established research subject. [Patel et al., 2026][p04]; [Orlanski et al., 2026][p05]; [Jin et al., 2026][p06].

This proposal asks whether architectural analysis can help make a more specific decision **before the maintenance outcomes are known**: which of two concrete implementation packages is better suited to specified future changes under a fixed coding-agent policy? The proposed explanation concerns where responsibilities reside and which interactions a change must preserve. For example, a change to a temporary gameplay effect may require agreement between the owner of the effect, the update that applies it and the lifecycle operation that removes it. Co-locating those operations might help, but an implicit ordering dependency could offset that advantage. The study must identify such competing expectations before observing an agent's result.

Here, an **architecture package** means the concrete source organization together with the APIs, runtime facilities and conventions on which that organization depends. A **responsibility** is an obligation to own state, enforce a rule or perform an effect. **Coordination demands** are the facts and interactions that an edit must keep consistent across those responsibilities. **Suitability** means observed ability to implement specified changes while preserving applicable behavior, under the declared information, feedback and resource policy. Source size and resource use are measured separately; neither defines suitability by itself.

The intended contribution is a bounded, prospective test of package-choice reasoning. It would show where predictions about responsibility and coordination succeed, fail or cannot be distinguished from simpler explanations. It would also produce explicit change contracts and evidence that another researcher can inspect. A favorable result would support a decision about the selected packages and scenarios; broader architectural, language or programming-paradigm claims would require further cases and stronger controls.

## 2. Related research and the research gap

### 2.1 From architectural descriptions to change predictions

Architecture-level modifiability analysis (ALMA) supplies a close methodological foundation: identify the decision, describe the architecture, elicit change scenarios and assess their impact. This proposal adopts that prospective scenario logic. ALMA's illustrative applications do not, by themselves, establish that an analyst's predictions are calibrated for coding agents. The proposed study therefore records predictions and their possible disconfirmation before implementation. [Bengtsson et al., 2004][p02].

Architectural descriptions and planning are also established in agent research. Sambu et al. evaluate LLM-produced decompositions of monoliths into service partitions; their evaluated outcome is a proposed partition rather than an executed refactoring followed by maintenance. Theory of Code Space evaluates architectural-map construction, and CodePlan combines dependency analysis, impact propagation and repository-level edit planning. These studies motivate examining responsibilities and dependencies, while leaving their different outcomes distinct: a partition score, a graph score and successful application behavior are different forms of evidence. The present proposal uses analyst-only source maps to formulate predictions; it does not introduce a map or planning assistant as a new agent treatment. [Sambu et al., 2026][p01]; [Sapunov, 2026][p12]; [Bairi et al., 2024][p13].

### 2.2 Source quality, inheritance and downstream behavior

The code-cleanliness minimal-pair study compares source variants under matched task behavior. CodeThread studies downstream changes to accepted human and agent predecessors. SlopCodeBench measures correctness, regressions, structural proxies and cost across inherited code, while ChainSWE includes canonical prior fixes and naturally accumulated fixes. Together, these are direct predecessors for source comparisons, maintenance chains and reference-predecessor controls. Their designs and selection rules differ: for example, CodeThread's predecessor acceptance uses both earlier and future tests, while ChainSWE's modes can change source access as well as memory. Those choices cannot be treated as interchangeable controls. [Trivedi and Schmitt, 2026][p03]; [Patel et al., 2026][p04]; [Orlanski et al., 2026][p05]; [Jin et al., 2026][p06].

They also leave several rival explanations relevant to this proposal. A downstream failure may be an ordinary defect in the preceding patch, rather than difficulty extending a correct design. A larger request or a missing API may explain cost or failure without invoking organization. Structural conformance alone is insufficient: Needle in the Repo scores required design structure, but does not establish its future maintenance benefit. Accordingly, this study scores declared behavior and retains valid alternative implementations, including edits that depart from the initial style. [Zhu et al., 2026][p07].

### 2.3 Feedback, information and measurement

An agent's working policy affects what a package comparison means. Type-Error Ablation finds benefits from diagnostic information in some repair settings, with task and model differences. The Complexity Trap compares observation masking and summarization with policy-specific costs and accuracy effects. When the Specification Emerges changes the timing and availability of requirements, and its ProjectGuard intervention also changes state support and restart behavior. These findings motivate fixing information exposure and feedback in the initial comparison. They do not establish that removing feedback reproduces an effective repair workflow. [Krishnamurthi and Flatt, 2026][p08]; [Lindenbauer et al., 2025][p09]; [Yan et al., 2026][p10].

The outcome instrument also needs its own validation. GameEngineBench supplies relevant runtime tasks, but its reported success includes LLM adjudication that can override test outcomes. It therefore cannot validate a new game's behavioral checks by analogy. The proposed case must demonstrate that its observations accept legitimate implementations and detect meaningful faults. Compilation, graph accuracy, import structure and stylistic conformity will not substitute for those observations. [La et al., 2026][p11].

### 2.4 The bounded gap

The reviewed work establishes methods for architectural analysis, dependency planning, source comparison and inherited maintenance. **The remaining question for this project is whether predictions made from concrete responsibility and interaction boundaries can inform a package choice for particular future changes, and survive comparison with API availability, source size and predecessor defects.** This is an opportunity for a focused empirical test, rather than a claim that downstream maintenance or architectural reasoning has not been studied.

The proposed study connects three elements: predictions recorded before implementation, equivalent observable change requirements across two credible packages, and subsequent behavioral outcomes under controlled information exposure. Its added value depends on whether those predictions discriminate between packages in a way that could change a maintainer's decision. If both architectural predictions and a simple size or API explanation always make the same prediction, the case cannot establish their separate value.

This gap assessment draws on thirteen fully read core papers and bounded artifact checks. It is a focused synthesis, not a systematic coverage or novelty claim. The individual reconstructions retain edition differences, private or unavailable artifacts and unresolved methods. No claim of an independently reproduced literature result is required for the proposed local feasibility decision.

## 3. Research questions and propositions

The principal question is: **Can prospective analysis of responsibility and coordination help choose between two architecture packages for specified maintenance changes performed by a coding agent?** Three questions make that objective observable.

| Question | Evidence needed | Interpretation |
| --- | --- | --- |
| **RQ1 — Case feasibility:** Can the packages satisfy common behavioral contracts while presenting a credible, consequential difference in coordination demands? | Working baselines, contrasting reference changes, recorded predictions and validated observations | Determines whether the case is worth studying; does not establish an agent effect |
| **RQ2 — Prospective suitability:** Under a fixed agent policy, where do predeclared package-suitability predictions agree or disagree with new-behavior completion and preservation of earlier obligations? | Frozen scenario predictions and all assigned candidate trajectories, including failures and architectural drift | Tests predictions locally and examines rivals; does not isolate architecture from the entire package |
| **RQ3 — Starting-state sensitivity:** At specified later tasks, how do package outcomes differ when starting from naturally inherited code versus a validated reference predecessor? | Predeclared reference-predecessor comparisons for both packages, without selecting histories by success | Measures sensitivity to the starting-state policy; does not identify a pure architectural-degradation mechanism |

The working proposition is conditional: an organization that reduces the coordination needed for a particular change may improve that change's reliability, provided it does not introduce offsetting ordering, lifecycle or API obligations. Directional predictions will be made for actual scenarios after source inspection. No package is designated the expected overall winner.

The strongest rival is that ordinary predecessor defects and different API or size demands explain the apparent advantage. Evidence against the proposed explanation would include a predicted coordination difference disappearing when the actual engine work is identified, an allegedly adverse change being equally localized in both packages, or candidate outcomes consistently contradicting the frozen prediction. Such observations remain results; they are not reasons to replace tasks until a preferred pattern appears.

RQ1 is the immediate feasibility study. RQ2 requires separately reviewed construction and an allocated candidate study. RQ3 requires the reference condition described below; if that condition is omitted, the study will explicitly leave RQ3 unanswered.

## 4. Methodology

### 4.1 Study design and provisional case

The design is a staged comparison of two concrete packages within one application domain. A model-free feasibility phase, **A0**, tests whether the contrast is meaningful and measurable. After separate review, **A1** would construct and freeze the maintenance scenarios, controls and analysis plan. Controller verification and any model-backed study follow later approval.

The provisional case is the MMCC and ImSim Breakout examples in Nu, pinned to [064f7ae92a8506689cd91aff5e6804a375d6ef3d](https://github.com/bryanedds/Nu/tree/064f7ae92a8506689cd91aff5e6804a375d6ef3d). The relevant application files are:

- [Projects/Breakout Mmcc/Gameplay.fs](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Projects/Breakout%20Mmcc/Gameplay.fs).
- [Projects/Breakout ImSim/Gameplay.fs](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Projects/Breakout%20ImSim/Gameplay.fs).

The existing source assessment identifies explicit gameplay-model/manual-motion responsibilities in MMCC and entity-property/dynamic-physics responsibilities in ImSim. Both use F# and effectful engine facilities. Sharing a language and engine reduces some variation, but leaves API, physics, authoring, documentation and familiarity differences. The study therefore treats them as packages, rather than validated representatives of two paradigms. The [source assessment](nu-form-factors-and-research-leads-2026-09-14.md) records the provenance and provisional status of this interpretation.

The editable boundary is application code; engine and approved library facilities are read-only. A0 must establish that boundary on the pinned runtime and audit the source, project metadata, generated code, defaults and documentation exposed to each package. Shared engine facilities cannot explain an observed package difference without evidence of different use. Nu and F# are provisional choices: an uninformative contrast would lead to a redirect decision, not construction of a substitute engine or selection for a favorable language result.

### 4.2 A0: establish feasibility before scaling

A0 is bounded to **two unchanged baselines and at most two reference change witnesses per package**, giving at most four successor implementations. A witness is a trusted implementation used to establish that the proposed requirement and observation are feasible. It is not a candidate trial or independent confirmation of the analyst's prediction.

The procedure is:

1. **Establish both baselines.** Build and run the pinned examples; identify common externally meaningful behavior, the application boundary and relevant runtime dependencies. Record any baseline defect before selecting a comparison.
2. **Describe responsibilities.** Map the state owners, update/effect boundaries, lifecycle rules and information needed for plausible changes. Separate organizational differences from API and physics differences.
3. **Select contrasting demands and record predictions.** Choose at most two changes that probe different coordination pressures. Record the cards in section 4.3 before implementing either version of each change. Include an adverse, tie or uncertain expectation; do not require one win for each package.
4. **Implement and check the witnesses.** Demonstrate common behavior using a minimal observation seam. Test a meaningful omission, ordering or lifecycle fault relevant to the contract, and an alternative valid implementation where feasible. Record limits where an alternative cannot yet be demonstrated.
5. **Return a yes/no/redirect assessment.** Report whether the observations are sound and at least one consequential prediction is distinguishable from a trivial baseline, size or API mismatch. Preserve contrary evidence and unresolved expertise limits.

Possible demands include a reversible state transition with parent/child ownership, or a change to dynamic identity and lifecycle. These are examples from the source assessment, not selected tasks or established advantages. The actual requirements must be justified by the inspected program and a plausible maintenance decision.

Common behavior need not mean identical floating-point trajectories. Input schedules, tolerances and nondeterminism rules must follow the semantic requirement and be fixed before comparative candidate outcomes. The observation seam may expose state or events, but cannot implement the feature being tested. A broken baseline, a task-solving seam, or a need for substantial replacement infrastructure defeats the proposed case. Successful execution alone does not establish a useful contrast.

### 4.3 Prospective prediction records

Each selected scenario receives a versioned prediction card. Original cards are retained when witness construction causes a refinement.

| Field | Recorded content |
| --- | --- |
| Change and provenance | Required new behavior, retained obligations, reason for selecting it, and whether it represents expected demand or a deliberate stress case |
| Source explanation | State owner, affected responsibilities, ordering/effect boundaries, information to recover, and work already supplied by the runtime |
| Prediction | Package advantage, tie or uncertainty; the expected obligation or failure pattern and why |
| Simple comparators | What source size, baseline correctness and API availability would predict, including disagreements with the architectural prediction |
| Rival and disconfirmation | An alternative explanation and observations that would contradict or fail to distinguish the proposed explanation |
| Provenance and revision | Exact source, analyst identity, timing and all subsequent changes to the prediction |

This is a source-grounded argument, not a new numerical architecture score. Nearby statements do not automatically imply low coordination, and counts of files, abstractions or graph edges do not define the expected outcome. Analyst maps and prediction cards remain outside candidate prompts. Requesting a candidate's own map would change its reasoning and information policy and would require a separate intervention.

### 4.4 A1: construct the maintenance workload

If A0 supports proceeding, the proposed workload is **two four-episode chains for each package**, with each chain starting independently from its package's baseline. An episode is one change request; a chain carries the resulting safe source through successive requests. An obligation is a versioned behavioral requirement. The workload can introduce behavior, retain earlier behavior or explicitly supersede an earlier obligation.

Requirements are written before their reference successors and matched between packages at the behavioral level. Necessary effort, patch size and touched-file count are outcomes, not matching criteria. Scenarios must probe the declared demands, including plausible adverse cases, rather than repeatedly reward one package's known convenience. Expected-use scenarios and stress-selected scenarios remain identifiable; no deployment frequency is inferred from their equal inclusion.

A1 would expand the obligation, semantic-fault and alternative-implementation audit, then freeze the tasks, prediction cards, reference predecessors, accepted information, submission interface, scoring and analysis. A separate challenge review should be sought when available; its actual independence and expertise must be stated. Reference implementation and self-review are not human validation. The formal comparative-case protocol and its conditional methods reading remain A1 prerequisites, rather than completed work in this proposal.

### 4.5 Candidate policy and information exposure

The proposed primary policy is **fresh context for each episode, source-only inheritance, one submitted edit, and no execution feedback or repair**. Every episode supplies the actual safe inherited source, the current requirement, all earlier accepted requirements with explicit supersession, and the approved documentation/API exposure. Candidate notes are off; existing source comments remain source. Research predictions, future tasks, reference solutions and comparative outcomes are withheld.

The proposed policy deliberately measures robustness under a restrictive workflow. It does not represent a developer or agent with interactive compiler repair, and it cannot establish the benefits of an inspector, hot reload, persistent memory or insulated repair. Those would be different research questions and treatments.

Safe submitted source persists even when it does not compile or fails behavior checks. The controller does not replace it with a reference solution. Invalid submissions preserve the previous safe state under a frozen rule; unsafe submissions are contained and classified. The selected submission format must have enough output headroom to express the expected edits in both packages.

The evaluator observes after submission and never returns hidden scores or uses them to trigger retries or continuation. Candidate execution uses the existing reviewed sandbox and accounting boundaries, without model credentials, host secrets or writable scoring machinery. All attempts and safe-state transitions are retained. Initial package assignment remains the comparison condition if the agent reorganizes the code; correct departures from the starting style are not excluded.

### 4.6 Reference-predecessor comparison for RQ3

At a small set of later tasks, chosen before outcomes, each package would be evaluated from both its naturally inherited state and its validated canonical reference predecessor. These **sentinel tasks** use the same requirement, accepted prior obligations, documentation and agent policy. Their reference branch is separate and does not reset or repair the inherited trajectory.

The schedule includes both packages and every assigned block, without choosing predecessor histories because they passed, failed or look interesting. Reference validity is evidence over the declared contracts, not proof of whole-program equivalence. Earlier missing features and ordinary defects remain measured differences between starting states.

For a sentinel, compare the package difference under inheritance with the package difference under the reference condition:

```text
D_inherited = outcome(A, inherited) - outcome(B, inherited)
D_reference = outcome(A, reference) - outcome(B, reference)
starting_state_sensitivity = D_inherited - D_reference
```

This is a contrast between starting-state policies. It does not estimate the fraction of failure caused by architecture or isolate latent architectural damage. Sentinel positions, pairing and all additional calls must be included in A1's finite allocation. If those controls cannot be justified within the proposed study, retain the narrower RQ2 policy claim and report RQ3 as untested.

### 4.7 Outcomes and records

Behavioral completion is primary. Resource measurements and source annotations help describe the result; they cannot turn incorrect behavior into success.

| Measure | Operational definition and record |
| --- | --- |
| Joint completion | A valid submission, successful build and satisfaction of all applicable declared obligations at the episode |
| New behavior | Which newly introduced obligations pass, fail or remain unobserved |
| Retained behavior | Previously applicable obligations, with new regression, persistent inherited failure and recovery recorded separately |
| Supersession | Explicit retirement or replacement of an obligation, rather than an implicit disappearance from scoring |
| Execution status | Submission, build, runtime and apparatus status, including blocked observations and unstarted slots |
| Resources | Observed model input/output usage, elapsed time and direct controller costs, with missing records and accounting coverage retained |
| Source and exposure | Source identities, submitted changes, visible source/documentation bundles and actual request composition |
| Explanatory observations | Responsibility changes, API use and architectural drift compared with the original prediction; these remain annotations rather than hidden success criteria |

A known build failure makes joint completion false but leaves runtime assertions blocked, rather than inventing individual test failures. If a required observation is unavailable and no failure is known, joint completion is unknown. An unstarted slot remains `not_run`. Any predeclared assigned-policy utility that gives a candidate-induced unrun slot zero is reported separately from its observation status; infrastructure missingness remains unknown and enters bounds.

Missing usage does not erase known correctness. Cumulative input tokens, authored bytes, the visible envelope and peak active context are separate quantities. These measurements do not establish a physical context-window effect or total human maintenance cost. The primary policy has no summary/helper workers; introducing them would require additional treatment definitions and complete accounting.

### 4.8 Sampling and analysis

A complete repeated block contains both packages and both chains under the same declared model and policy. Package/chain order is counterbalanced, while episode order within a chain is fixed. The exact model configuration, resource ceiling and schedule are recorded; a material identity change triggers a new disposition rather than an unnoticed replacement. A scheduling seed does not imply seeded model randomness.

Analysis first presents all obligation and episode outcomes, then chain-specific paired package differences within each block. An overall assigned-policy summary, if adopted, uses declared equal-chain weights and retains the separate chain results. Partial blocks retain coverage and missing-outcome bounds. Assertion counts are not independent tasks, and repeated trajectories are not additional architectures or scenario families.

RQ2 compares the frozen predictions with the observed obligation patterns, contradictions and competing explanations. A uniformly stronger package is less informative about change-specific reasoning than a justified distinction between demands, but no crossover is required for a result to be retained. When the architectural and simple-comparator predictions agree everywhere, their separate predictive value remains unresolved. With two chosen chains, the study will not fit a large prediction model or claim calibrated architectural forecasts.

RQ3 reports the sentinel contrasts alongside predecessor defects and missing obligations. Resource comparisons retain correctness outcomes and usage coverage so that early failures or missing records do not create an unexplained claim of efficiency. Any inferential procedure, endpoint, missingness convention and sample count must be fixed in A1 before outcomes; non-significance is not equivalence, and identical repetitions are not population certainty. No favorable-result-driven extension is permitted.

### 4.9 Validity and reproducibility

| Threat | Planned response and residual limit |
| --- | --- |
| API, physics or source size explains the result | Audit these differences and predeclare simple rivals; redirect an uninformative A0 case. The remaining treatment is still a package. |
| Analyst chooses changes to confirm a preference | Record scenario provenance and predictions before witnesses; retain adverse cases and all revisions. A0 remains constructive feasibility work. |
| Inherited defects dominate later tasks | Separate obligation transitions and use predeclared reference sentinels for RQ3. The reference contrast still includes concrete implementation differences. |
| Tests reward one implementation | Validate meaningful faults and legitimate alternatives; make required structural contracts public. Finite tests do not establish universal equivalence. |
| Guidance or probes change the information policy | Fix source, accepted requirements, API help and feedback; keep analyst predictions outside candidate exposure. |
| Small or familiar cases limit transfer | State the selected packages, tasks, model and policy. Additional model repetitions estimate variability on these cases, not general architectural effects. |

The study would release the frozen requirements, permitted source, trusted references, test/fault definitions, prediction history, controller configuration, all permitted submissions and a report with source identities. Secrets and private transcripts are excluded. Existing completed experiments and frozen scores remain identifiable and are not reinterpreted as results of this proposed study.

## 5. Work plan and decisions for human review

The immediate review concerns the introduction-to-method argument above and whether the proposed A0 feasibility test is worth undertaking. Later stages depend on what that test establishes.

| Stage | Deliverable | Decision before proceeding |
| --- | --- | --- |
| **A0 — Feasibility** | Two unchanged baselines, at most four successors, prospective cards, observable contracts and a yes/no/redirect report | Human review of this proposal before any A0 construction |
| **A1 — Workload and protocol** | Proposed two four-episode chains, validated obligations/references, frozen predictions, claim level, sentinel schedule and finite sample/analysis plan | Review A0 evidence and authorize A1 separately |
| **B0 — Apparatus verification** | Minimum controller/reporting changes and model-free safety, accounting and submission checks within the existing system | Review the constructed study and implementation scope |
| **B1 — Integration** | Explicitly allocated unrelated integration checks on the actual approved configuration | Separate live allocation and apparatus approval |
| **B2 — Candidate study** | Fixed comparative batch and predeclared report for the supported research questions | Separate batch authorization; no automatic extension |

The previous arithmetic, 12 blocks × 2 packages × 2 chains × 4 episodes = 192 generations, plus five integration generations, is an **unallocated planning proposal**, not a sample-size justification. It omits the extra reference calls needed for RQ3. A1 must justify and cost the complete design, including controls and worst-case usage, preferably by reallocating repetitions rather than silently adding calls. No model configuration, powered sample, calendar duration or live allocation is finalized here.

Human review should resolve four points:

1. Whether the local package-choice problem and prospective predictions offer sufficient research value beyond established maintenance comparisons.
2. Whether Nu is a credible provisional case, and whether the A0 success and redirect criteria are discriminating enough.
3. Whether the restrictive candidate policy answers a useful question, and whether the intended later claim requires the RQ3 reference condition.
4. Whether to authorize A0 within its two-baseline/four-successor bound, revise that proposal, or redirect the research question.

Current authorization covers proposal preparation and publication. A0/A1 construction, recruitment, adapters, calibration, model/count probes and candidate execution remain on hold. New experimental allocation is zero. Approval of a research direction or completion of A0 would not authorize later stages automatically.

## 6. Expected contribution

The study would contribute a transparent test of prospective package-choice reasoning: source-bound predictions, observable maintenance contracts, contrary cases and outcomes under a precisely stated agent policy. An informative result may favor either package, reveal that the expected advantage depends on the change, or show that simpler API, size or predecessor explanations suffice. An A0 decision to reject the proposed case is also useful if it prevents an uninformative model study.

The contribution is local evidence and a reusable comparison procedure. General language superiority, internal architectural understanding, benefits of repair isolation and physical context-window advantages remain separate questions.

## References

The P-identifiers match the repository's reading records and Zotero queue. Linked arXiv versions are the reviewed editions; publication and preprint editions are not counted as separate studies.

| ID | Reference and reviewed edition | Method and access record |
| --- | --- | --- |
| P01 | Sambu et al. (2026). [LLMs for Architectural Refactoring: An Exploratory Study on Monoliths to Microservices][p01]. ICSA; conference author preprint read. DOI `10.1109/ICSA66085.2026.00033`. | [Reconstruction](literature/full-reading/P01-architectural-refactoring.md) |
| P02 | Bengtsson, Lassing, Bosch and van Vliet (2004). [Architecture-level modifiability analysis (ALMA)][p02]. Journal of Systems and Software. DOI `10.1016/S0164-1212(03)00080-3`. | [Reconstruction](literature/full-reading/P02-alma.md) |
| P03 | Trivedi and Schmitt (2026). [Does Code Cleanliness Affect Coding Agents? A Controlled Minimal-Pair Study][p03]. arXiv `2605.20049v1`. | [Reconstruction](literature/full-reading/P03-code-cleanliness.md) |
| P04 | Patel et al. (2026). [Is Agent Code Less Maintainable Than Human Code?][p04]. arXiv `2606.21804v1`; CodeThread. | [Reconstruction](literature/full-reading/P04-codethread.md) |
| P05 | Orlanski et al. (2026). [SlopCodeBench: Benchmarking How Coding Agents Degrade Over Long-Horizon Iterative Tasks][p05]. arXiv `2603.24755v2`. | [Reconstruction](literature/full-reading/P05-slopcodebench.md) |
| P06 | Jin et al. (2026). [ChainSWE: Benchmarking Coding Agents on Multi-Bug Software Maintenance][p06]. arXiv `2607.02606v2`. | [Reconstruction and v1 differences](literature/full-reading/P06-chainswe.md) |
| P07 | Zhu et al. (2026). [Needle in the Repo: A Benchmark for Maintainability in AI-Generated Repository Edits][p07]. arXiv `2603.27745v1`. | [Reconstruction](literature/full-reading/P07-needle-in-repo.md) |
| P08 | Krishnamurthi and Flatt (2026). [Type-Error Ablation and AI Coding Agents][p08]. arXiv `2606.01522v2`. | [Reconstruction](literature/full-reading/P08-type-error-ablation.md) |
| P09 | Lindenbauer et al. (2025). [The Complexity Trap: Simple Observation Masking Is as Efficient as LLM Summarization for Agent Context Management][p09]. arXiv `2508.21433v3`. | [Reconstruction and matched arithmetic](literature/full-reading/P09-complexity-trap.md) |
| P10 | Yan, Chen and Zhang (2026). [When the Specification Emerges: Benchmarking Faithfulness Loss in Long-Horizon Coding Agents][p10]. arXiv `2603.17104v1`; SLUMP. | [Reconstruction](literature/full-reading/P10-slump.md) |
| P11 | La et al. (2026). [GameEngineBench: Evaluating Coding Agents on Real C++ Runtime Environments][p11]. arXiv `2607.03525v2`. | [Reconstruction and v1 differences](literature/full-reading/P11-gameenginebench.md) |
| P12 | Sapunov (2026). [Theory of Code Space: Do Code Agents Understand Software Architecture?][p12]. arXiv `2603.00601v4`. | [Reconstruction](literature/full-reading/P12-tocs.md) |
| P13 | Bairi et al. (2024). [CodePlan: Repository-Level Coding using LLMs and Planning][p13]. Proceedings of the ACM on Software Engineering, 1(FSE), article 31; publisher PDF. DOI `10.1145/3643757`. | [Reconstruction and preprint lineage](literature/full-reading/P13-codeplan.md) |

[p01]: https://doi.org/10.1109/ICSA66085.2026.00033
[p02]: https://doi.org/10.1016/S0164-1212(03)00080-3
[p03]: https://arxiv.org/abs/2605.20049v1
[p04]: https://arxiv.org/abs/2606.21804v1
[p05]: https://arxiv.org/abs/2603.24755v2
[p06]: https://arxiv.org/abs/2607.02606v2
[p07]: https://arxiv.org/abs/2603.27745v1
[p08]: https://arxiv.org/abs/2606.01522v2
[p09]: https://arxiv.org/abs/2508.21433v3
[p10]: https://arxiv.org/abs/2603.17104v1
[p11]: https://arxiv.org/abs/2607.03525v2
[p12]: https://arxiv.org/abs/2603.00601v4
[p13]: https://doi.org/10.1145/3643757

## Supporting evidence and proposal provenance

This standalone proposal reorganizes the completed reading and scientific position at repository commit `9d3f797ea48c83f283e488f23aa0fe6ffa308f46` for introduction-to-methodology human review. The [full-paper synthesis](literature/full-reading/synthesis.md), [coverage index](literature/full-reading/INDEX.md), [source decisions](literature/full-reading/source-decisions.md) and [arithmetic/artifact validation](literature/full-reading/validation.md) remain the supporting audit. Their reading and reproduction limits are unchanged. The [2026-09-14 proposal](architecture-maintenance-research-proposal-2026-09-14.md) is retained as the preceding formulation.

The proposal and its check are main-session AI work; human scientific review is pending. The [preparation record](research-proposal-review-preparation-2026-09-15.md) identifies this revision's scope and validation. [PLAN.md](../PLAN.md) owns execution authority and subsequent decisions.
