# When does architecture analysis improve coding-agent maintenance choices?

**Proposed revision, 2026-09-15; input `78c2eea477b04ae890f64b500db628c9dc89750a`.** This is a prospective research design, not an adopted experiment. [PLAN](../PLAN.md) owns authority; [the iteration review](three-criteria-iteration-2026-09-15.md) explains changes and [the source audit](three-criteria-iteration-sources-2026-09-15.md) records new retrieval and reading limits. Previous wording remains in Git. All construction and execution holds remain in force.

## 1. Problem, decision and intended contribution

A maintainer selecting between existing implementations needs to know which is more suitable for anticipated changes, not merely which looks cleaner or has fewer tokens. A responsibility-and-coordination analysis might identify relevant state owners, ordering constraints and cross-boundary obligations. But it might also rationalize a preference, reward an available API, or require more effort than choosing a reliable default. The question is whether its recommendations earn **additional behavioral decision value** under a specified coding-agent workflow.

The proposed decision is a starting-package choice between two credible implementations that satisfy the same selected baseline obligations. The decision maker sees the approved source/API information, declared change profile and target agent policy. It does not see future candidate trajectories, reference patches or final evaluation results. A profile may contain known planned requirements; this is conditional suitability, not an ability to forecast future demand. If only coarse demands would realistically be known, the selector must not receive the exact hidden future task sequence instead. A1 must freeze that information frontier.

The intended contribution is a reproducible evaluation of a specified **source/profile-to-package selection procedure on profiles not used to develop it**, using later observable behavior and credible comparator policies. This is a proposed incremental distinction, not a claim to invent architecture evaluation, recommendation, policy evaluation, source contrasts or maintenance chains. A single tailored prediction on one pair supports a local advice case; a transferable selection method needs additional profile and package-family evidence.

The initial beneficiary is a maintainer making an adoption choice between already available packages under known maintenance demands. Building both alternatives, migration costs, runtime performance and human analysis time are not free in deployment. The first study must state what already exists and report analysis effort separately. It cannot claim labor savings or positive return on investment from model-token counts alone.

## 2. Evidence and defensible boundary from prior work

The [full-reading synthesis](literature/full-reading/synthesis.md) and [A01–A03 reconstruction](proposal-novelty-value-validity-sources-2026-09-15.md) are reused evidence. This revision does not certify those PDFs anew. Sixteen documented readings still do not cover the entire field.

| Closest evidence | What is already established or evaluated | Residual question, not a novelty certificate |
| --- | --- | --- |
| ALMA, `10.1016/S0164-1212(03)00080-3`; Lassing et al. 2003, `10.1016/S0164-1212(02)00056-0` | Scenario-based architectural analysis/comparison and comparison of prior expectations with later changes | Does a declared analysis select an implementation with better *agent-executed behavioral maintenance outcomes* than credible defaults on new profiles? Prospective validation itself is prior art. |
| Code cleanliness, CodeThread, SlopCodeBench, ChainSWE; P03–P06 | Controlled source/predecessor contrasts, later issues, regression/cost, inheritance, memory/interface conditions | Does the frozen selection rule add useful information rather than merely discover a generally better package? Neither chaining nor a reference-state control is new. |
| ToCS, CodePlan; P12/P13; ArchBench `10.48550/arXiv.2603.17833` | Maps, architectural outputs, dependency planning and several architecture/code tasks | Architecture-output quality is not automatically the realized value of a choice between starting packages. Some ArchBench tasks include behavior; do not misdescribe all existing evaluation as non-executable. |
| Pattern recommendation, `10.1007/978-3-031-66336-9_19`; MicroRec, `10.1145/3643991.3644916` | Direct recommendation predecessors identified; the first author abstract reports architecture-pattern prediction against labelled cases | Full decision inputs, baselines, splits and outcomes remain to be reconstructed. Do not claim all recommendation work lacks downstream evaluation from abstract-only access. |
| GenAI architecture review, publisher `10.1016/j.jss.2025.112607`, related preprint `10.48550/arXiv.2503.13310` | A wider evidence map of design support and evaluation, with dated search coverage and validity limitations | Use its primary-study trail to test the residual distinction; a review's historical gap is not evidence that no later study filled it. |
| P08–P10 and A03 | Current diagnostics can be useful; memory policies bundle information changes; repeated failure can reflect ordinary compounding | A no-repair policy does not isolate architecture or protected repair. Direct state-policy controls are more honest than an unexplained residual labelled architectural damage. |

A01's 117 logged requests were reduced to 56 functional changes after excluding implementation bugs. Its retrospective complexity categories and one developer's labels do not become prospective executable success labels. ALF keeps implementation errors when its target policy includes them. P04's acceptance filtering uses future tests; ALF must not select inherited histories using future outcomes. The existing reading notes further qualify P06 interface changes, P09 matched denominators and P11 judge-based outcomes. These are design constraints, not reasons to dismiss close work.

New selected primary HTML readings distinguish ArchBench's task metrics, a conceptual Spec Growth Engine proposal and MAAD's architecture-artifact/practitioner evaluation. They are not new complete PDF readings or evidence of ALF's claimed benefit. The narrow Scite query was paged through all 50 returned records; a truncated citation graph and other vocabularies remain incomplete. Novelty is **unresolved**, with an explicit claim to test rather than an assertion of firstness.

## 3. Questions and contribution levels

**RQ1 — Case and decision feasibility.** Can the selected packages implement common, consequential maintenance demands, and can a frozen responsibility analysis make a useful, falsifiable choice that is not merely an API/size or general-package preference?

**RQ2 — Added selection value.** On predeclared evaluation profiles and a fixed agent policy, how does the outcome of the architecture procedure's chosen package compare with always-A, always-B, size/API rules and an appropriate ordinary-review alternative?

**RQ3 — Starting-state sensitivity.** For predeclared later tasks, how do package and recommendation contrasts change between naturally inherited source and validated reference predecessors? This is a state-policy comparison, not isolated architectural mediation.

There are three legitimate levels of conclusion:

1. **Local advice case:** a few frozen, possibly construction-informed recommendations on the selected pair. No general predictive-method claim.
2. **Procedure value on new profiles:** an auditable method is fixed using development cases, then applied to separate profiles not used to tune it. This is the intended stronger target.
3. **Portable mechanism:** independently authored package families and a suitable intervention or robust rival analysis support transfer. This is later work, not something repetitions on Nu establish.

Choose the level before candidate data. Do not execute level 1 and promote it to level 2 or 3 after a favorable result.

## 4. Selection procedure and credible alternatives

### 4.1 Make the advice reproducible

Define the analyst or model, provided materials, permitted tools, budget and sequence: extract current obligations; identify owners and relevant state/effect/ordering paths; note domain-local difficulty and engine work already provided; compare change coordination and rivals; then choose A, B or abstain under declared adjudication rules. Do not invent an unvalidated scalar 'architecture score' merely to appear quantitative.

Archive the source evidence, reasoning summary, uncertainties, choice, timestamp and procedure version. The procedure is frozen before it sees evaluation profiles; its choices are frozen before reference solutions or candidate outcomes are revealed. One fixed recommendation per profile evaluates those particular recommendations. It does not estimate the variability or reliability of the analyst/model itself unless that dimension is separately sampled.

A candidate-visible architectural plan would change implementation support. In this **choice-only** study, recommendations and analyst maps remain outside candidate prompts. Both packages receive the same task information and comparable API/documentation authority.

### 4.2 Baselines that prevent an easy but uninformative win

| Policy | Definition and role |
| --- | --- |
| Always A; always B | Fixed-package reference choices. If the architecture method always picks the globally stronger package, it adds no scenario-sensitive choice beyond the matching constant. |
| Development-selected default | A single package selected using only development evidence and frozen before evaluation; a realistic fallback. |
| Size | Smaller initial eligible source bundle under a stated byte/token definition, with tie rules. Never use the successful patch or future trajectory. |
| API fit | Predeclared required facilities, mixed-advantage and tie rules using initial source and known demands. Do not tune the rule to lose. |
| Ordinary review | Same source/profile evidence and comparable analysis budget, without the special responsibility-analysis procedure. Required for a claim that the procedure itself adds value over ordinary attention; otherwise limit the claim to the named simple comparators. |

The evaluation-data best constant can be shown as an optimistic descriptive reference, not selected and relabelled as a prospective default. Comparing against both constants uses the already observed package outcomes and needs no additional candidate runs. An ordinary-review condition may need additional analyst/model work and is separately budgeted; this document does not authorize it.

Each abstaining policy needs a frozen fallback for its primary all-profile value. Alternatively report bounded value and selective coverage without claiming superiority over an undefined decision. Do not omit hard abstained profiles from the main comparison. Ties, disagreements and all-profile results remain visible.

### 4.3 A useful implication requires a real decision margin

Before data, state a decision-relevant minimum improvement and acceptable failures/resource costs for the beneficiary. Do not adopt an arbitrary percentage because it is convenient for a power calculation. Keep terminal correctness, interim regression burden and costs separate unless a stakeholder-defined utility is explicitly frozen.

Record one-time analysis effort, per-profile advice cost and any repeated adaptation. A later break-even calculation may use stated values for a successful outcome and reuse count; without those measured or justified inputs, no economic-benefit claim follows. A well-bounded null can discourage unnecessary analysis; an imprecise null is only inconclusive.

## 5. Workload construction and two holdout boundaries

### 5.1 Provisional Nu case

Nu MMCC and ImSim Breakout at `bryanedds/Nu@064f7ae92a8506689cd91aff5e6804a375d6ef3d` remain optional:

```text
Projects/Breakout Mmcc/Gameplay.fs
Projects/Breakout ImSim/Gameplay.fs
```

They share F# and an engine but differ in state organization, manual/dynamic physics, APIs and pattern familiarity. The treatment is the actual package, not pure functional versus imperative architecture. Do not compare Nu against Unity as though only language changed. Match declared behavior and available information, not required coordination, file count or patch size; those can be outcomes of the package.

### 5.2 A0 is development, not method confirmation

After explicit approval, A0 may run both unchanged baselines and construct at most two contrasting reference changes per package. Before each witness, record the requirement, source mechanism, expected choice/tie, constant/size/API predictions, rival and disconfirmation. Track revisions caused by implementation.

A0 must demonstrate a live common oracle, safe observation boundary, meaningful faults and alternative correct implementations. Tolerance/nondeterminism policy follows semantic obligations, not which implementation needs relief. A wrapper cannot implement the task. No substitute engine or new runner family is justified just to rescue the pair.

Disagreement-selected witnesses can efficiently diagnose a hypothesis, but cannot estimate the prevalence of recommendation opportunities. Include an adverse/tie expectation when meaningful; never require a win for each architecture. A0 can redirect the case if API mismatch, generation carrier, runtime limitations or uniformly equivalent choices dominate.

### 5.3 New profiles test transfer; hidden tests test behavior

For a **selection-method** claim, reserve new change profiles not used to write/tune the procedure or choose advantageous scenario patterns. Hold out whole profiles/chains, not episodes that share the same planned change or predecessor. Prefer a different scenario author and a selector restricted to the approved decision information. Record actual role/knowledge independence; another AI invocation is not independent if given the author's solutions. Without credible separation, retain the local case claim.

The selector may receive the new profile as an input after the procedure is frozen; that is not leakage. Receiving its reference solution, evaluator answers or outcomes and then altering the rule is leakage. The exact information that would realistically be known at adoption time must be fixed.

Separately, final behavioral holdouts are isolated from candidate prompts, feedback and continuation. Public/development checks and hidden scoring have separate purposes. Unknown hidden pass/fail bits must not control repair or acceptance. Neither the profile split nor the test split replaces the other.

A1 may keep the proposed two four-episode chains as a **local diagnostic panel**, or revise within a finite budget to include genuine evaluation profiles. Two chains and twelve repeats are not enough by arithmetic to establish a reusable selector. Do not spend many repeats before showing that the profile-level contrast exists.

## 6. Candidate policy and inherited-state control

The current proposed candidate policy remains fresh episode context, source-only inheritance, one submitted edit and no execution feedback or repair. This is a diagnostic restrictive-policy comparison, not the normal workflow of an interactive agent or a planner insulated from build fixes. No change to this policy is adopted here.

Before a study claims practical maintenance-choice value, A1 must justify that policy for the beneficiary or separately specify a bounded hygienic development-feedback policy with the existing controller, fixed authority/budget and sealed final holdout. Active diagnostics may be useful. A subagent is not necessary merely to obtain ordinary repair, and no generic framework is authorized.

Each episode includes actual safe inherited source, the current and earlier accepted requirements with explicit supersession, and declared documentation. Notes are off; source comments remain source. Safe wrong/noncompiling code persists; invalid output preserves the prior safe state; unsafe changes are contained. Document the submission format and demonstrate enough output headroom for both packages. Initial package assignment remains the treatment after valid reorganization.

For RQ3, predeclare later sentinels in both packages and every assigned block from both the natural inherited state and its validated canonical predecessor. Do not select histories by success or silently reset the main chain. Compare the inherited and reference package differences, with their difference labelled starting-state sensitivity. Missing earlier features and overt defects remain part of that contrast; no pure damage or percentage-explained claim is identified.

## 7. Outcomes and policy-value analysis

The proposed primary decision endpoint is terminal **joint build and all active declared behavioral/API obligations**. This means completion by the end, not successful uninterrupted operation. Each episode's first/joint completion, new behavior, retained obligations, new regression, persistent failure, recovery and supersession remain mandatory secondary evidence. If the beneficiary needs continuous correctness, choose a different primary utility before data, not whichever endpoint later looks best.

Final outcome is false when a known applicable requirement fails, unknown when required evidence is unavailable without a known failure, and true only when all requirements are demonstrated. A build failure blocks individual runtime assertions; it does not make them executed failures. Candidate-induced future unrun slots can contribute zero to a declared policy utility, while remaining `not_run` observations. Infrastructure missingness is bounded, not automatically zero. Known correctness survives missing usage; accounting may still stop further dispatch.

Let c index an evaluation profile/chain, b a temporal paired repetition, and a the package. Let Y[b,a,c] be the declared terminal policy outcome. With prespecified weights w[c] summing to one and a fixed selector pi:

```text
V_hat(pi) = sum_c w[c] * mean_b Y[b, pi(x[c]), c]
Delta_hat(pi,h) = sum_c w[c] * mean_b (
    Y[b, pi(x[c]), c] - Y[b, h(x[c]), c])
```

Both packages run under the same allocated candidate policy in isolated trajectories, so several fixed choice rules can be evaluated from this outcome panel without new candidate calls. This is full-information evaluation conditional on the panel, not an off-policy estimator requiring propensity machinery. Separate runs are not the same random model counterfactual; temporal blocking limits drift but does not create shared random seeds. Prevent cross-trajectory contamination and retain all attempts.

When pi and h choose the same package, their difference is **identically zero**, including when that shared outcome is unknown. Individual values can remain unknown. Missing-outcome bounds must reuse each Y once with its algebraic coefficient, rather than invent independent values for the same submission. For differing choices, preserve the pair and bound missing components. Never select each block's better observed package and call it the predicted decision.

Always-A/B show whether a demanding method merely identifies a general package winner. Beating a development-selected default is prospective evidence on the evaluated profiles. Claiming improvement over every constant requires appropriate joint uncertainty; do not estimate a new 'best' baseline and ordinary p-value from the same outcomes. A1 must name the primary comparator, secondary hierarchy and multiplicity/interval procedure before collection.

Equal profile weights describe this panel, not deployment frequencies. Provide profile-specific contrasts and sensitivity to reasonable declared weights rather than infer an unknown demand distribution. Outcome-based task reweighting and selective abstention are prohibited.

The independent unit for performance on this panel is the paired trajectory/block, but generalization of the **choice method** needs new profiles; architectural portability needs independent package families. Episode counts, assertions and stochastic repetitions cannot supply those units. Use methods proportional to the number of independent levels; do not fit a large mixed-effects model to two chains. Do not pool old E calibrations, maintenance-sim construction or native ecological studies as identical observations.

## 8. Failure modes, decision rules and resource limits

| Observation | Honest conclusion and next decision |
| --- | --- |
| One package wins every profile; the selector always chooses it | Potentially useful package choice, no demonstrated need for profile analysis. Compare analysis cost with the fixed default. |
| Selector improves over a weak size rule but not the corresponding constant | No added scenario-sensitive value from that comparison. Do not strengthen the headline. |
| Frozen selector outperforms credible defaults on new profiles, with useful precision | Local support for the procedure under this package/model/policy; independent-family replication is the next generalization question. |
| Selector and comparator agree | Zero incremental choice difference on those cases; explanations may still be informative, but that is a different endpoint. |
| A richer rubric only beats a less-informed or lower-budget review | Extra information/effort is a rival; do not attribute the gain to the rubric alone. |
| Package gap changes between reference and inherited states | State-policy sensitivity, not pure architectural decay. |
| Mostly format/build cascades under no repair | Report the diagnostic policy; reconsider deployment relevance before increasing repetitions. |
| Wide intervals or unresolved oracle/access | Inconclusive or blocked claim; no equivalence, novelty certificate or unlimited search for favorable cases. |

The previous 12 blocks x 2 packages x 2 chains x 4 episodes = 192 generations, plus five unrelated integration calls, remains unallocated illustrative arithmetic. It omits ordinary-review and sentinel requests and is not a power justification. Define exact profiles, policy, primary comparator, meaningful difference, precision goal, worst-case requests/output/time/spend and stopping rules before authorization. No outcome-driven extension; any adaptive design needs its own predeclared and validated analysis.

A0 addresses case and choice feasibility. A1 settles the selector/holdouts/policy and finite design. B0 implements only approved controls using the existing runner; B1 is separately capped integration; B2 is the authorized frozen batch and report. Return at each scientific boundary. A feedback, language or physical-window experiment is a conditional successor, not a compulsory factorial.

## 9. Evidence still needed and research value

The most decision-critical incomplete literature is direct architecture-pattern recommendation and microservice selection, followed through the verified architecture-review evidence map. Reconstruct their predictors, train/test boundaries, baseline choices and whether outcomes are labels, expert judgments or later executable changes. If they already evaluate the same practical target, remove the novelty claim and state a justified replication or a substantively different estimand. Do not preserve novelty merely by changing the engine.

This iteration supports a narrower and more rigorous **research question**, not proven empirical value. Its reusable output would be an auditable selection procedure, transparent opportunities/limits, paired behavioral evidence and falsified or retained responsibility predictions. A negative but precise result can show when ordinary defaults are sufficient. A small imprecise case cannot establish that architecture never matters.

Primary/reference provenance is available through the existing [full-reading index](literature/full-reading/INDEX.md), [synthesis](literature/full-reading/synthesis.md), [earlier follow-up ledger](proposal-novelty-value-validity-sources-2026-09-15.md) and [this iteration's source record](three-criteria-iteration-sources-2026-09-15.md). New primary HTML inspection is selected-section evidence only; no new full-PDF or Zotero completion is claimed. The controlled experiment is situated in a software case, not automatically a naturalistic case study. Current review is assistant self-review, not independent human approval.
