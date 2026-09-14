# Architectural organization as an input to agent maintenance

## A comparative-case proposal with prospective change scenarios

**Status, 2026-09-14:** reviewed and revised research proposal; not an adopted replacement experiment. New construction, recruitment, adapters and live allocations remain unauthorized. The immediate proposed decision is Phase A0 feasibility, not the full model study. This revision incorporates the [AI review](pro-review-2026-09-14.md). The [pre-review manuscript](history/architecture-maintenance-proposal-pre-review-2026-09-14.md) preserves the earlier full background and methods verbatim; its source ledger remains available [here](architecture-maintenance-proposal-sources-2026-09-14.md).

## Abstract

Coding-agent studies already show that inherited code, source quality, structural constraints and interaction history can affect subsequent work. A worthwhile next question is not whether maintainability matters, or which language is universally best. It is whether **specific alternative organizations of responsibilities, state and effects produce predictable differences in behavioral maintenance under specified future changes**. We propose a bounded comparative case in which two credible implementations start from a common observable contract, receive the same ordered changes, and pass their edited source to fresh candidate contexts. Before candidate execution, the study records both favorable and unfavorable change scenarios for each package and the source-level reasons for those predictions. Outcomes distinguish new-feature implementation, retained behavior, newly introduced regressions, inherited failures and recovery. A same-language Nu MMCC/ImSim pair is provisional; its different physics and interaction APIs are explicit package components, not controls that disappear merely because both programs use F#. A model-free feasibility gate must establish runtime execution, pair credibility and an oracle before construction of full chains. The eventual fixed-policy experiment would support a local package comparison. Stronger claims about latent maintainability or causal mediation require a prespecified clean-predecessor control or another intervention; they cannot be inferred from cumulative failure counts alone.

## 1. Problem and intended value

Maintenance changes a functioning system while preserving obligations that remain valid. Architectural organization determines which responsibilities, state owners and interaction paths a maintainer must understand or coordinate. This makes an architecture valuable relative to a set of likely changes, not by an unconditional complexity or brevity score. Architecture-level modifiability analysis, ALMA, explicitly distinguishes predicting ordinary maintenance effort, identifying risks and comparing alternatives through discriminating change scenarios [1].

For coding agents there are two separable practical questions. First, does the assigned implementation make the next required change easier to complete correctly? Second, does the state an agent leaves behind make later changes more fragile? An initial generation error, a missing dependency, an awkward submission format and architectural coupling can all increase later cost, but they are not the same mechanism. Existing ALF E1/E2/E2a/E3a results must not be relabelled as a clean estimate of architecture or training familiarity.

The revised project should produce an actionable conditional result: under a declared maintenance policy and set of changes, which responsibilities are easier to preserve in each package, where do failures first appear, and what later obligations recover or deteriorate? It need not produce a winner. An opposing pattern across scenario chains, a null pattern, or a finding that API/runtime differences dominate can all change an engineering decision.

The contribution is therefore **prospective architectural predictions checked against inherited behavioral outcomes**, not the mere novelty of the names MMCC and ImSim. It is initially a comparative case, not a population estimate of functional programming, F#, UI architecture or game engines. Neither Nu nor the earlier F#/C# pair is mandatory if a more credible case is needed.

## 2. What the closest literature already establishes

The earlier literature work remains useful. This review updates the overlap at the level of treatments, starting states, feedback and outcomes rather than counting keywords or citations. Version identifiers below matter; current preprint text must not be combined with statistics from a different indexed edition.

| Work and inspected edition | Established method relevant here | Consequence for this proposal |
| --- | --- | --- |
| **Does Code Cleanliness Affect Coding Agents?**, v1 [2] | Behaviorally matched, same-language repository variants; source quality is manipulated before independent tasks. Methods include hotspot and multi-module tasks, plus insensitive controls. Reported token/navigation differences did not imply a measured general improvement in task success. | Controlled code-representation effects are already studied. Its transformations include factoring and local structural changes, so do not claim that all architectural structure was absent. The proposed distinction is credible alternative responsibility/state packages, prospective trade-offs and inherited changes, not “we vary code.” |
| **SlopCodeBench**, v2 [3] | Agents repeatedly extend their own code under evolving requirements and fresh conversations. Behavioral, regression, structural and cost outcomes already coexist; the paper distinguishes stricter cumulative and more isolated task views. | Neither sequential maintenance, fresh agents nor cumulative cost is new. Add explicit obligation histories and scenario predictions rather than another undifferentiated success total. |
| **CodeThread / Is Agent Code Less Maintainable Than Human Code?**, v1 [4] | A later task is evaluated from human or agent predecessor implementations. Predecessors meet the paper's observable test preconditions before comparison. | Downstream effects of inherited code are already studied. Our no-reset policy also carries obviously broken code, so its result is not automatically the same latent-maintainability estimand. |
| **Needle in the Repo**, v1 [5] | Authored multi-file and multi-step probes combine functional and structural oracles for specific maintainability pressures. | Architectural constraint preservation is already evaluated. Package fidelity is not a valid substitute for behavioral downstream evidence in our comparison. |
| **When the Specification Emerges**, v1 [6] | Progressive versus upfront requirements and external project-state support are explicit interventions; structural faithfulness is a declared scored dimension. | Persistent specification tracking and notes are not incidental controls. Keep our primary source-inheritance policy separate from notes or persistent conversations. |
| **GameEngineBench**, v1 [7] | Real engine projects, scoped source changes, runtime tests and post-solve judge auditing. Its published setup includes an LLM judge and differing wrappers. | Game-runtime evaluation is not new. It supports demanding a real runtime witness, not borrowing a judge verdict as a certified Nu oracle or comparing wrapper-confounded model scores. |
| **ALMA** [1] | Change-scenario elicitation and analysis depend on whether the aim is maintenance prediction, risk or alternative comparison. | Predeclare credible countervailing scenarios; do not force equal edit effort, since that can remove the architectural difference of interest. |
| **Evolution of Functional UI Paradigms** [8] | Conceptual/example-based analysis of update consistency, modularity and state/view organization, including limitations of pure MVU. | Useful mechanism hypotheses, not an experiment proving MMCC superiority over ImSim or equating either Nu package with MVC/MVU. |

SWE-CI, StaminaBench, repository modernization, refactoring and smell studies remain in the [existing evidence ledger](architecture-maintenance-proposal-sources-2026-09-14.md) with their recorded versions and reading limits. They are not erased from prior art merely because the table emphasizes the nearest design decisions. Human maintenance and technical-debt studies retained in the earlier manuscript provide context, not transferable agent effect sizes or a prior that cleaner-looking code must win.

The scoped gap is: **a prospective, source-grounded comparison of credible alternative packages under common inherited changes, judged by behavioral obligations and interpreted against task-specific predictions and competing failure pathways**. We did not establish that no such study exists anywhere. The search audit records incomplete graph coverage, unexamined search ranges and access-limited leads. A proposal cannot earn significance merely by choosing a combination of conditions no one has named before.

## 3. Research questions and claim hierarchy

**RQ1 — Assigned-policy outcome.** Under the same finite candidate policy, do the two starting packages differ in how often successive submissions satisfy all applicable behavioral obligations?

**RQ2 — Prospective trade-offs.** Do differences follow the predeclared responsibility/state-interaction predictions for the selected change scenarios? A coordinated-state chain and a local-interaction chain are provisional examples, not validated categories or representative distributions.

**RQ3 — Failure pathways and resources.** Where do output/application, compilation, new-behavior, retained-obligation and runtime/environment failures occur, and what resources accompany them? These are observed pathways, not access to hidden reasoning or proof of training-corpus causation.

Three claim levels must remain separate:

1. **Feasibility:** the packages and oracle can be compared under a reproducible runtime.
2. **Bounded package outcome:** assigned baselines differ under the tested task/policy sequence, with credible common requirements and measured uncertainty. This bundles organization, APIs, idioms, documentation and model familiarity.
3. **Specific mechanism:** an architectural property causes later maintenance differences. This needs a corresponding intervention/control and cannot be obtained simply by naming the packages or correlating source size with results.

The first two are attainable goals for the minimal case. The third is a conditional later claim, not an automatic interpretation of a positive result. Architectural drift is an outcome; enforcing the initial style by rejecting otherwise valid submissions would change the treatment into a style-conformance experiment.

## 4. Candidate case and the limits of matching

### 4.1 Provisional Nu case

The source anchor remains `bryanedds/Nu@064f7ae92a8506689cd91aff5e6804a375d6ef3d`, particularly `Projects/Breakout Mmcc/Gameplay.fs` and `Projects/Breakout ImSim/Gameplay.fs` [9]. The review rechecked their initial gameplay/state and update sections. MMCC stores explicit gameplay records and advances ball motion in its update logic; ImSim uses screen properties, a processing loop and dynamic engine bodies. Both contain real-time behavior and effectful engine interactions. Their use of different motion/physics facilities is material.

Thus the comparison is an **application organization plus API/runtime package**, not an isolated functional/imperative contrast. Operational semantics is itself mathematical; no mathematical-versus-operational dichotomy is claimed. A source-level state-owner map must precede any hypothesis that a particular change is naturally local or cross-cutting.

The earlier public change-lead inventory remains a provenance starting point, not eight ready-made tasks. An engine-level fix requiring a later engine revision cannot be transplanted into a pinned application-only task without a separately reviewed scope change. Private Nu chat and personal analysis may suggest leads, but cannot become unlicensed published task material or independent experimental evidence.

### 4.2 Match required behavior, not implementation effort

Both packages must meet the same baseline obligations and receive the same new requirement, relevant earlier contracts and comparable engine documentation. Do not equalize line counts, helper counts, internal state types, reference-patch size or the number of responsibilities that must change. Those can be outcomes or mechanisms.

Conversely, an arbitrary API omission, a broken baseline, different public functionality, unequal documentation or privileged helper code is not an architectural advantage. Record every material asymmetry and whether it is an intended package component or a construction defect. If only collision-backend familiarity explains the planned contrast, narrow the claim or select different scenarios; do not label it a pure organization effect.

A neutral observation seam may expose existing inputs and events to tests. It must not implement the requested feature or replace the engine with a toy interpreter. Exact floating-point trajectories need not be equal when not part of the behavioral contract. Common tolerances, deterministic input traces and lifecycle observations must be justified before outcomes, not loosened for whichever package fails.

## 5. Phase A: construction only after approval

### A0 — Small feasibility witness before full-chain investment

The proposed first authorization covers only:

- both unmodified baselines running in the intended isolated environment, with native dependencies, assets and licenses identified;
- editable application files versus immutable engine/framework and scoring assets;
- a source-grounded map of state ownership, lifetime, effect paths and documentation;
- a symmetric observation interface and baseline contract/fault checks;
- at most two contrasting change witnesses per package, derived from documented requirements and designed to expose different coordination obligations;
- an explicit verdict on whether a credible package comparison survives the necessary test seams.

This is at most the two baselines plus four successor witnesses, not the entire proposed eighteen-checkpoint construction. A mock runtime, compilation alone or a source string assertion is not a real execution witness. Check repeated deterministic replays and retained lifecycle state; distinguish runtime nondeterminism from implementation faults. Test flakiness must be characterized under a fixed policy before candidates are involved.

A0 stops for review. If the case needs an alternative engine, broad new shim, private knowledge or a large new infrastructure layer to look comparable, reject or reframe the case rather than continue apparatus construction. Existing E/H components may be reused only where their assumptions actually fit this runtime.

### A1 — Two independent scenario chains, conditional on A0 acceptance

The full design still proposes two four-episode chains, each starting from its own copy of each accepted baseline. Later episodes depend on earlier source, but one chain must not inherit the other. Author the requirements and oracle before reference implementations; keep future requirements absent from candidate input.

For each scenario record:

| Field | Required content |
| --- | --- |
| Provenance | Public source change or explicitly authored requirement; what was known before the fix; license and transplantation limits. |
| Common obligation | Observable behavior, lifecycle/ordering and error rules, plus explicit API/nonfunctional constraints. |
| Prospective prediction | Which package responsibilities must coordinate, expected failure opportunity and a competing explanation. No guaranteed winner. |
| Opposing case | A plausible change that stresses the other package or a reason neither has an expected advantage. |
| Reference witness | At least one valid implementation for each package; no canonical internal spelling requirement. |
| Oracle adequacy | Baseline cannot already satisfy the new requirement; valid alternatives pass; semantic faults fail; retained obligations and explicit supersessions are identified. |
| Exposure audit | All scored requirements are inferable from current/earlier candidate-visible contracts and approved API information. |

Separate anticipated ordinary changes from deliberately discriminating stress scenarios. An enriched set can be valuable, but it estimates neither real-world frequency nor a general scenario-family interaction. One chain of each kind cannot identify a population effect of “coordinated” versus “local” work. Repetition does not solve that sampling limitation.

An independent challenge should cover domain validity, both package idioms, the behavioral contract and oracle. Prefer actual competent nonauthor review where available, and record reviewer identity/type and scope. Two people are not a statistical guarantee; one person must not be counted twice under different roles. Missing relevant expertise limits acceptance and claims and must be dispositioned, not replaced by invented human approval. A0 can expose feasibility limits without recruiting reviewers automatically; no recruitment is authorized now.

## 6. Proposed candidate policy

The later protocol must select one exposed model/effort, backend, resource policy and exact source identities. Historical model names or unused quotas do not establish current availability or authorization. Proposed policy:

- One fresh candidate context and one submitted edit per episode, without compiler/test feedback, repairs, source tools or successor access.
- Supply the complete permitted current source, earlier/current contracts and the approved engine information bundle. No research predictions or architecture labels beyond unavoidable source content.
- Persist safe submitted source even when it does not compile or satisfy the task. Preserve an invalid submission as a failed submission; the prior safe source remains the next predecessor. Unsafe changes terminate according to the declared policy.
- Do not reset to reference gold, remove inconvenient histories or transform drifted code back into its initial package. Initial package is the assigned treatment; later drift is an observation.
- **Proposed primary memory is source-only:** no separate candidate-authored notes are carried across episodes. Source comments naturally remain source. A 4,096-byte notes channel, proposed earlier, would be a distinct memory intervention; adopting it requires an explicit change and matching interpretation.
- Require a demonstrated edit/submission interface with enough output headroom for both reference implementations. Complete-file replacement, structured edit operations and unified diffs impose different generation burdens; freeze the chosen policy and retain format/truncation failures separately. No post-hoc change to make one package's outputs pass.

This controls execution feedback rather than representing normal tool-using development. It cannot establish benefits from a repair subagent or persistent orchestrator. A later ecological policy may answer that question, but it must not be pooled with this arm.

Reference envelopes and fault fixtures should be used to check that caps permit intended valid work, not to make a reference multiplier such as 1.25 an allegedly scientific threshold. Declare input/output/elapsed/build/runtime limits and the treatment of safe source growth. Report cap hits as policy outcomes. If ordinary valid construction approaches a cap, revise it before outcomes rather than impose unequal truncation or repeatedly expand it during collection.

## 7. Outcome model: what happened, what remained, and what was observed

Every scheduled slot needs separate fields for dispatch, response completeness, safe application, submitted-source identity, build, current-task obligations, retained obligations, termination, and accounting coverage. A single `success` flag is insufficient.

**Observed submission completion** is true only when the valid submitted artifact builds and meets all active declared behavioral/API obligations. A known failing requirement establishes failure even when another component is unknown. Missing evaluation because of an apparatus fault is unknown. If compilation fails, joint completion is false, but individual runtime assertions are `blocked_by_build`, not fabricated assertion failures.

**Missing usage never automatically un-scores correctness.** A complete safely evaluable submission can be scored when token accounting is unavailable. Its cost remains incomplete. Pause new dispatch if remaining allocation cannot be bounded; do not manufacture zero cost or erase a valid outcome. Retain known usage and coverage separately from totals.

**Unrun is not failed code.** After a candidate-induced policy stop, later scheduled slots have no observed submission. A preregistered assigned-policy utility may assign those slots zero to represent inability to complete the planned chain; retain `not_run` in observed fields and state the scoring convention. Infrastructure-unobserved slots remain unknown and contribute to bounds rather than automatic losses for one package.

### Versioned behavioral obligations

Give each obligation a stable identity, introduction episode, supersession/retirement rule, severity rationale and oracle cases. Per obligation distinguish:

| Transition | Interpretation |
| --- | --- |
| Newly introduced and not met | Failure to implement the new requirement, not a regression. |
| Previously observed passing, still required, now failing | A newly lost retained obligation. |
| Already failing and still failing | Persistent inherited failure, counted as persistence rather than another distinct regression. |
| Failing to passing | Recovery. |
| Superseded or no longer applicable | Not a regression; preserve the explicit contract revision. |
| Build/runtime apparatus prevents observation | Unknown/blocked, not an inferred behavioral transition. |

Report stricter cumulative completion and new-obligation performance side by side. Partial case counts diagnose behavior; they do not turn many correlated assertions into independent tasks. Final scoring occurs outside candidate interaction and never changes feedback, retries, order or the decision to add episodes.

Architecture annotations may explain responsibility movement, abstraction bypass and drift, but style fidelity does not decide the primary behavioral score. Declared public API or architecture obligations must be visible in the task; an unannounced preferred implementation is not an oracle.

## 8. Inherited defects versus latent maintainability

A no-reset chain answers a practical question: how robust is the assigned package under this sequence of fallible edits? Its cumulative outcome includes obvious build failures, missed features and format limits. If an early broken submission makes every later checkpoint fail, that is real policy evidence but not by itself proof that a once-correct architecture was harder to modify.

CodeThread's observable predecessor checks [4] and SlopCodeBench's distinct cumulative/isolated views [3] make this distinction important. Do not “fix” it by analyzing only successful histories; that selects different populations after treatment.

Before the live protocol is frozen, choose one of two honest scopes:

1. **Keep the minimum inherited case and narrow the claim** to fixed-policy behavioral robustness, with the obligation-transition diagnostics above; or
2. **Predeclare a small clean-predecessor sentinel control:** at specified later episode(s), independently run the same task, package, model and policy from that package's validated reference predecessor. Compare against the assigned inherited-state arm with uncertainty and full cost. Reference targets and final outcomes remain hidden. Choose sentinels before new outcomes, not only where one package fails.

This control distinguishes a starting-state intervention from the intrinsic difficulty of the later requirement, but still does not isolate a single architectural primitive or training familiarity. It must have a finite explicitly approved allocation, preferably by revising the proposed sample within its envelope, not silently adding calls. It is not required to call the minimal work a comparative case; it is required to make claims its absent counterfactual cannot support.

## 9. Sampling, analysis and resource decisions

The earlier arithmetic remains a planning option: 12 blocks × 2 packages × 2 chains × 4 episodes = 192 candidate generations, 48 trajectories. Up to five unrelated integration generations would be separate. **Allocated now: zero.** The number 12 is not a power calculation. Final task choices, sentinel decision, caps, model availability and sample are settled only after A0/A1.

Each block contains the four package/chain trajectories. Freeze an order schedule balancing package and chain over time and across chronological positions; preserve whole blocks for paired summaries. A balanced four-sequence order repeated three times is one model-free planning option, not proof of randomized model seeds or elimination of backend drift. Task order within each chain stays fixed. Record date, load, configuration and any backend changes; do not replace failed cells based on the package difference.

For a complete block `b`, package `a`, chain `c`, episode `e`, let `Y[b,a,c,e]` be the **declared assigned-policy completion score**. Observed outcomes and policy-imputed zeros remain separate in the data. Then:

```text
A[b,a,c] = mean over the four episode scores
D[b,c]   = A[b,MMCC,c] - A[b,ImSim,c]
Delta[c] = mean over blocks of D[b,c]
Delta    = mean of the two chain-specific Delta values
```

These define equal weighting of the selected chains, not their real-world prevalence. Publish each episode, chain and block value. The contrast between the two chain differences is exploratory and describes only those chains. It is not an identified architecture × scenario-family population effect.

If any completion scores are unknown, calculate lower and upper bounds by allowing the unknown values in [0,1] with their actual signed weights. Do not discard incomplete blocks and announce a complete-case winner. Score known behavior despite missing cost. Cost differences require matching coverage; report partial known sums and coverage without labelling them complete totals.

A block bootstrap may describe within-case stochastic uncertainty under its assumptions; it cannot estimate variation across new architectures, independent applications or unobserved requirements. With twelve identical block differences, a percentile bootstrap collapses to a point. That is an empirical resampling limitation, not certainty or practical equivalence. Show the raw counts and exact degeneracy, avoid a confirmatory confidence claim, and use model-free operating-characteristic checks before registering any confirmatory test or adaptive stopping rule.

If a future confirmatory study is proposed, select a meaningful effect/precision target, independent unit, sample ceiling and valid analysis before collecting it. Repeating this one pair until a p-value crosses a threshold is not a route to general research value. No post-hoc favorable scenario replacement, effect-driven extension or pooling with historical E/H outcomes is permitted.

Resource reports separate model input/output and their subsets, direct tool time, preparation, human/AI review effort, and end-to-end elapsed time. A lower cost from an early stop is not cheaper successful maintenance. Neither source bytes nor tokens equal human effort, physical model memory or currency. All candidate, integration, judge, worker and summary generation requests require explicit allocation and retained debits; there is no free reviewer hidden in the design.

## 10. Research loop, go/no-go decisions and limitations

The [research-loop procedure](research-loop-and-scite.md) governs future literature passes. The present pass paged targeted Scite searches, challenged closest methods, checked graph coverage, and used primary text when Scite returned no readable content. It is a bounded critical review, not a new systematic review of the entire field. Search totals, generated citation reports and an absence of graph edges cannot certify novelty.

Before construction, the literature-to-method record must answer: what comparable intervention already exists, what this design changes, which observation would challenge its interpretation, and what decision follows? New papers that merely repeat a known general claim need not spawn another workstream. High-priority unresolved predecessors remain explicit; do not silently exclude them to preserve a gap.

**Proceed to request A0 approval** because the revised question is concrete enough to test feasibility, not because its effect or publishability is established. Do not execute A0 during this documentation review.

**Proceed from A0 only if** both packages run under a common observable contract, different responsibilities can be described without paradigm caricatures, the observation seam preserves the intended difference, and contrasting change witnesses are plausible. Reviewable null predictions are acceptable.

**Reframe or reject the case if** equivalence requires erasing the package contrast, physics/API differences overwhelm the intended interpretation, realistic tasks cannot be scored, or the construction cost is disproportionate. A different domain or package pair is allowed. Do not force Nu or the previous language hypothesis to survive.

**Proceed to live data only if** the frozen protocol identifies its claim level, actual environment/model, memory and feedback policy, safe inheritance, obligation tracking, finite allocation, uncertainty treatment and operational stop rules. Any pilot result remains local unless independent package/task/model replication supports transfer.

The earlier F#/C# construction and its larger F# envelopes stay preserved. The current same-language study does not test language-token compression or a context-window crossover. A later context or repair-routing intervention is conditional and separate; it is not a prerequisite to every architecture case and must not be smuggled into the current comparison.

## References used for the revised argument

These are primary-source anchors with specific reading extents recorded in the [review source audit](pro-review-sources-2026-09-14.md). Further background and earlier study versions remain in the existing ledger and archived manuscript; they are not counted as newly read studies.

1. Bengtsson et al. **Architecture-level modifiability analysis (ALMA)**. DOI [10.1016/S0164-1212(03)00080-3](https://doi.org/10.1016/S0164-1212(03)00080-3). [Author-hosted paper](https://www.cs.vu.nl/~hans/publications/y2004/alma.pdf), especially scenario elicitation and alternative-comparison sections.
2. Trivedi and Schmitt. **Does Code Cleanliness Affect Coding Agents? A Controlled Minimal-Pair Study**, arXiv v1. [10.48550/arXiv.2605.20049](https://arxiv.org/html/2605.20049v1), §§2–3 and §6.
3. Orlanski et al. **SlopCodeBench: Benchmarking How Coding Agents Degrade Over Long-Horizon Iterative Tasks**, arXiv v2. [10.48550/arXiv.2603.24755](https://arxiv.org/html/2603.24755v2), evaluation and inherited-state methods. Do not import older counts from search snippets.
4. **Is Agent Code Less Maintainable Than Human Code?** (CodeThread), arXiv v1. [10.48550/arXiv.2606.21804](https://arxiv.org/html/2606.21804v1), predecessor construction/filtering and downstream comparison.
5. Zhu et al. **Needle in the Repo: A Benchmark for Maintainability in AI-Generated Repository Edits**, arXiv v1. [10.48550/arXiv.2603.27745](https://arxiv.org/pdf/2603.27745v1), diagnostic-probe and oracle construction.
6. **When the Specification Emerges: Benchmarking Faithfulness Loss in Long-Horizon Coding Agents**, arXiv v1. [10.48550/arXiv.2603.17104](https://arxiv.org/html/2603.17104v1), §§2–3. Emergent-specification and project-memory evidence, not an assigned code-architecture experiment.
7. La et al. **GameEngineBench: Evaluating Coding Agents on Real C++ Runtime Environments**, arXiv v1. [10.48550/arXiv.2607.03525](https://arxiv.org/html/2607.03525v1), §5 and limitations.
8. Sperber and Schlegel. **Evolution of Functional UI Paradigms**. DOI [10.1145/3759163.3760429](https://doi.org/10.1145/3759163.3760429). [Author PDF](https://www.deinprogramm.de/sperber/papers/funarch-ui.pdf), architecture/MVC, MVU and conclusion sections; conceptual trade-offs, not a coding-agent trial.
9. Nu pinned application artifacts: [MMCC Gameplay](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Projects/Breakout%20Mmcc/Gameplay.fs) and [ImSim Gameplay](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Projects/Breakout%20ImSim/Gameplay.fs). Repository evidence, not a peer-reviewed paradigm comparison.
10. Wohlin et al. **Successful combination of database search and snowballing for identification of primary studies in systematic literature studies**. [10.1016/j.infsof.2022.106908](https://doi.org/10.1016/j.infsof.2022.106908), introduction and search-strategy definitions. This review uses a bounded combination, not a claim to have completed their systematic procedure.
