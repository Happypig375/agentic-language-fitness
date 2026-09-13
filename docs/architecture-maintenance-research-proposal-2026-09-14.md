# Research proposal: architecture under inherited maintenance

Date: **2026-09-14 HKT**. Repository base:
`4757a6c5cbbd0f764f9c39b596c5517cc024f48b`.
Status: **assistant proposal for human review, not an adopted experiment**.
The user authorized further research and publication of this proposal.
Construction, recruitment, adapter implementation and experimental execution
are not authorized by its publication. No live allocation is made here.

## 1. Recommendation and research value

Study whether a supplied architectural organization helps an agent preserve
existing obligations while implementing a sequence of changes. Begin with a
bounded, within-language comparative case, provisionally Nu's MMCC and ImSim
Breakout applications. Treat these as **architectural packages**, not an isolated
language feature or a functional-versus-object-oriented contrast.

The useful contribution is evidence about **when an architecture helps later
behavioral maintenance**, including contrary results, costs and failure paths.
It is not another ranking of generated code by conformity to a preferred design.
A reusable paired workload, externally specified behavioral oracles and complete
inherited-state records would also be valuable research artifacts. Neither a
publication nor an architectural advantage is guaranteed.

This first case would concern four successive maintenance episodes per
trajectory, not years of industrial maintenance or large-project productivity.
It can motivate later independent-case replication. F#/C#, model capability,
context boundaries and whole-engine comparisons are deferred, not erased from
the theory. Nu is a feasibility candidate, not a non-negotiable choice.

## 2. What the literature leaves worth testing

The supported candidate gap is the **downstream behavioral effect of credible,
specified architectural alternatives under a fixed maintenance policy**.
Architecture, inherited code and multi-episode agents are already studied:

| Closest evidence | Already covered | Distinction proposed here |
| --- | --- | --- |
| [SlopCodeBench v2](https://arxiv.org/html/2603.24755v2), DOI `10.48550/arXiv.2603.24755` | Successive changes to agents' inherited implementations, including next-checkpoint costs. | Assign alternative starting organizations, rather than only observing the structure agents accumulate. |
| [CodeThread v1](https://arxiv.org/html/2606.21804v1), DOI `10.48550/arXiv.2606.21804` | Downstream issue resolution on human- versus agent-authored predecessors. | Compare declared architectural packages, not prior authorship; neither comparison isolates every source difference. |
| [Needle in the Repo v1](https://arxiv.org/html/2603.27745v1), DOI `10.48550/arXiv.2603.27745` | Supplied starters, architectural boundaries, functional and structural oracles. | Judge subsequent behavior without making compliance with one preferred structure the definition of success. |
| [SWE-Refactor v1](https://arxiv.org/html/2602.03712v1), DOI `10.48550/arXiv.2602.03712` | Repository refactoring tasks; compilation, tests and intended-transformation checks. | Measure later change completion, not just successful restructuring. |
| [SmellBench, Dinu et al., v2](https://arxiv.org/html/2605.07001v2), DOI `10.48550/arXiv.2605.07001` | Architectural-smell repair, expert false-positive judgments and net smell changes. | Maintenance consequences of two credible alternatives, neither designated defective beforehand. |
| [SmellBench, Lin et al., v1](https://arxiv.org/html/2606.05574v1), DOI `10.48550/arXiv.2606.05574` | Injected smells, behavioral tests and fine-grained refactoring evaluation, including an LLM quality judge. | Behavioral downstream obligations as the primary outcome, not a quality-judge score. These are two different SmellBench papers. |
| [Sambu et al., ICSA 2026](https://conf.researchr.org/details/icsa-2026/icsa-2026-papers/27/LLMs-for-Architectural-Refactoring-An-Exploratory-study-on-Monoliths-to-Microservice), DOI `10.1109/ICSA66085.2026.00033` | The conference abstract describes monolith-to-microservice proposals evaluated with architectural metrics. | Later behavioral maintenance differs from the reported metric target; full methods were not accessible, so this distinction remains qualified. |

This is a **bounded scoping assessment**, not proof of novelty or a systematic
review. The newer benchmark sources above are preprints, except the identified
ICSA proceedings paper. The [source ledger](architecture-maintenance-proposal-sources-2026-09-14.md)
records exact queries, pagination, DOI decisions, primary editions, selected
sections read and unresolved access. Relevant unread leads remain open; before
a confirmatory study or novelty claim, update the closest-work search and resolve
material overlaps. A zero-edge Scite citation graph does not establish absence.

The methodological bridge is scenario-based architectural evaluation, not a
claim that Nu needs prior certification. [ALMA](https://www.cs.vu.nl/~hans/publications/y2004/alma.pdf),
DOI `10.1016/S0164-1212(03)00080-3`, motivates explicit change scenarios and impact
analysis. Here, predicted impacts would be compared with observed behavioral
results. Purposeful case selection is legitimate if its inference boundary is
explicit; it does not require randomly recruiting architects.
See [case-study guidance](https://doi.org/10.1007/s10664-008-9102-8) and
[sampling guidance](https://arxiv.org/html/2002.07764v6), journal DOI
`10.1007/s10664-021-10072-8`.

Published architectural examples support mechanisms, not superiority:
[GUI Easy](https://defn.io/papers/fungui-funarch23.pdf), DOI
`10.1145/3609025.3609478`, is an experience report about functional composition,
state ownership and an existing imperative GUI layer. Fowler's
[MVU formalization](https://doi.org/10.4230/LIPIcs.ECOOP.2020.14) is not a maintenance
experiment or a proof about Nu. The user-corrected adaptive-optics paper,
[primary preprint](https://arxiv.org/html/2407.07207v1), proceedings DOI
`10.1117/12.3020480`, combines state machines, messages and Dear ImGui. Thus
explicit state and immediate-mode interaction are not mutually exclusive.

## 3. Questions, predictions and what would refute them

**RQ1:** For the same inherited application obligations and fixed agent policy,
how does the assigned architectural package affect regression-free completion
across a prespecified maintenance chain?

**RQ2:** Do the differences on the selected coordinated-state and
local-interaction chains agree with the predicted placement of state ownership,
transition logic and interaction/effect wiring?

**RQ3 (descriptive):** What failures and resource costs accompany those outcomes?
Do failures arise from coordinating obligations, local wiring, API knowledge,
format/build errors or prior inherited damage?

Before execution, reviewers would map those responsibilities in each baseline
and record task-specific predictions without seeing candidate results:

- Explicitly organized transitions may help coordinate lifecycle obligations;
  additional message/effect plumbing may instead introduce omissions.
- Locally expressed interaction may simplify a conditional control; implicit
  processing order or persistent identity may instead create regressions.
- No meaningful difference, an opposite difference or different directions for
  the two chains are all admissible outcomes. Repeated contradictions weaken
  the proposed mechanisms; they are not reasons to replace tasks or models.

A package difference would not identify the isolated causal effect of messages,
immutability, syntax or coherence. Failure-path inspection can corroborate a
mechanism; it is not a causal mediation analysis. With one chain per family,
RQ2 is conditional on those two chains, not a population-level family effect.

## 4. Candidate case and model-free feasibility gate

Public source candidate:
[`bryanedds/Nu@064f7ae92a8506689cd91aff5e6804a375d6ef3d`](https://github.com/bryanedds/Nu/tree/064f7ae92a8506689cd91aff5e6804a375d6ef3d).
The [root README](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/ReadMe.md)
and [MMCC](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Projects/Breakout%20Mmcc/Breakout.fs)
and [ImSim](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Projects/Breakout%20ImSim/Breakout.fs)
applications provide real, supported design alternatives. Their intended
player-visible parity is user-supplied intent, **not executed equivalence**.
They share a language and engine revision but use different engine APIs and
physics implementations: MMCC manually advances model state; ImSim uses dynamic
physics bodies. Do not require identical trajectories or call this a controlled
single-feature intervention.

The neighboring Nu analysis was used for source discovery only. Its private
conversation archive is not research data for publication. Public history
provides the following concrete leads, not ready-made matched tasks:

| Lead | Observable concern | Suitability and boundary |
| --- | --- | --- |
| [Screen-selection issue #1374](https://github.com/bryanedds/Nu/issues/1374) and [August resolution](https://github.com/bryanedds/Nu/commit/6890bcf4f101501a1e1552cbcddf55f6a5de6548) | Selection and screen lifecycle | Cross-style motivation, but the resolution changes engine/API and application code after the July source pin. Do not transplant it as an application-only task. |
| [Selected-screen guard](https://github.com/bryanedds/Nu/commit/a22fe112e209dae806482c821fe32bf63d0dc5bf) | Gameplay should not advance on an inactive screen | Application/template fix already inherited at the pin; derive a new contract, not a memorized replay of the patch. |
| [Ball reset velocity](https://github.com/bryanedds/Nu/commit/edec18e27bb9b43adb93404a8a50d54392ce6946) | Initialization and reset behavior | Real application maintenance, but physics surfaces differ. Reject exact physics-repair matching without a valid shared contract. |
| [Conditional MMCC content](https://github.com/bryanedds/Nu/commit/39d5dc97321c7b7af75f05b5fb11c2fe7b40a0b7) | Content lifetime follows gameplay state | Useful lifecycle motivation; the concrete expression is style-specific. |

If separately approved, **Phase A** would construct one feasibility packet,
not a generic engine benchmark or a new remote layer:

1. Fix editable application files, read-only engine/dependencies, common
   behavioral observations and any minimal test seams. Record every deviation
   from the pin. Reject seams that implement the requested feature, privilege
   one design or replace the architecture being studied.
2. Verify shared selected baseline contracts in an isolated trusted build/run.
   Headless feasibility, asset/native dependencies and candidate-safe evaluator
   integration are currently **unverified**. A source-level stub-world test is
   not proof that either application can run in the existing sandbox.
3. Author two four-episode chains from externally stated requirements. Each
   chain starts independently from its assigned original baseline; state then
   persists for its four episodes. Illustrative coordinated-state changes are
   pause/resume, restart cleanup, delayed-action cancellation and outcome/screen
   coordination. Illustrative local-interaction changes are conditional
   controls, input rebinding, interaction feedback and shared control behavior.
   These eight sketches are **not task specifications or mined issue counts**.
4. Distinguish realistic anticipated changes from deliberate stress scenarios,
   as in ALMA. Record provenance and selection/rejection reasons. Write contracts
   first, then both reference continuations and independent oracle cases;
   reference implementations are witnesses, not the sole definition of truth.
5. Obtain two human reviews, collectively covering Nu/domain behavior and both
   idioms; at least one reviewer must not have authored the tasks/references.
   Record expertise, affiliations, disagreements and changes. No reviewers are
   recruited or confirmed. AI assistance is labeled and cannot substitute for
   those human judgments. Random architect recruitment is not proposed.
6. Require both reference chains to pass cumulative contracts; demonstrate
   semantic-fault detection and inherited-failure handling. Measure complete
   reference envelopes, timing and sandbox resources without model calls.

**Reject or redirect this case** if credible shared contracts require replacing
either architecture, the comparison reduces to incompatible physics behavior,
or safe observation needs substantial new engine/runner machinery. Missing
feasibility is not permission to implement a new framework. Changing the pin,
case or treatment must be explicit and reviewed before construction proceeds
beyond the approved scope.

## 5. Proposed exploratory execution settings

These are reviewable recommendations, **not executable settings or allocations**.
Phase B would need its own source-bound packet and explicit live approval after
Phase A. No new controller is implemented by this document.

| Setting | Proposed value / current state | Where defined |
| --- | --- | --- |
| Comparison | 2 architectural packages, 1 F# application pair, 1 pinned engine | Sections 3–4 |
| Workload | 2 separate chains × 4 inherited episodes; 8 task contracts, currently unauthored | Section 4 |
| Replication | 12 matched blocks; each block contains both architectures on both chains | This section |
| Candidate dispatch ceiling | 12 × 2 × 2 × 4 = **192**; 48 trajectories. Allocated **0**, used **0** | This section |
| Integration ceiling | Up to **5** unrelated shakedown dispatches, separately approved/charged; allocated **0** | This section |
| Total possible future dispatches | **197**, not 197 plus unused historical balances; no automatic replacements | This section |
| Model / effort / decoding | One configuration; exact identifiers and supported settings **not selected** | Must be filled before Phase B approval |
| Candidate interaction | Fresh conversation per episode; no tools, no compile/test feedback, no repair turn; one submission | Policy below |
| Durable state | Submitted editable application source plus explicitly designated candidate notes; all bytes charged | Policy below |
| Context treatment | Complete eligible source and common information, no context-pressure arm, retrieval or truncation | Policy below |
| Input/output byte caps | Same cap per direction for both styles; proposed reference-fit rule below. Actual values **unmeasured** | Phase A measurements required |
| Candidate notes | One optional UTF-8 file, maximum **4,096 bytes**, counted within input/output caps | Policy below |
| Wall time / CPU / RAM / process limits | **Not selected**; require measured Phase A envelope and explicit Phase B values | No execution-ready environment claimed |
| Runner / image / environment | No new selection; exact SHA, digest and profile **unfilled** | Phase B freeze required |
| Human review / live flags | **Pending / disabled**; OAuth staging **not authorized** | Section 8 |

Twelve blocks are a bounded exploratory ceiling, allowing three repetitions of
four balanced chain/style ordering combinations. This is **not a power
calculation** or evidence that 192 calls establish a general architecture effect.
Freeze the randomized schedule and seed before calls, interleave matched arms
in time, and keep episode order fixed. The blocks sample repeated agent runs,
not independent projects, architects or task families. There is no outcome-driven
sample extension. A later confirmatory replication requires its own precision
justification and independent workload/authoring units.

### Information and continuation policy

Each episode receives the current inherited editable source, current and prior
requirements, designated notes, and a frozen, symmetric set of necessary engine
API evidence. Define exact file manifests in Phase A; do not assume the entire
Nu engine fits. Both styles receive the same accessible semantic information,
not identical source bytes or artificial padding. Balanced orientation explains
both idioms without recommending a winner. Record its authorship and extent.

No earlier conversation, tool errors, compiler diagnostics, future task, gold,
holdout case, source-history patch or research document enters candidate context.
This excludes tool-recovery chatter by construction but measures a restricted
no-tools maintenance policy, not ordinary autonomous IDE work. It still permits
format, syntax and API-knowledge failures; they must be reported, not hidden.

Use a strict, declared file-response format. A safe, well-formed submission
replaces its allowed files and persists **even if it does not compile or pass**.
A malformed response applies nothing; retain its bytes and the previous source.
Do not reset to gold, manually repair code, silently reissue a model call or
discard a run because its architectural style drifts. Compare baseline
assignment, including later drift. Unsafe edits terminate the trajectory under
the published safety rule. Scoring tests remain outside editable machinery.

For each direction, propose a cap of the maximum complete serialized trusted
reference envelope across both styles/episodes, multiplied by 1.25 and rounded
up to a multiple of 4,096 bytes. Include the full notes allowance and all wrapper
text in the measurement. Freeze actual caps before Phase B; do not tune them
after candidate outcomes. Future source growth beyond the input cap terminates
only that trajectory as a policy-boundary outcome, with no truncation. These
authored-byte caps **do not establish a provider context-window limit**. The old
simulation's 86,016/61,440-byte proposals are not Nu measurements or defaults.

## 6. Outcomes, analysis and verifiability

Primary checkpoint outcome `Y` is 1 only when the new behavior and **all prior
obligations** pass the frozen external contracts; otherwise 0 for an observed
candidate/policy failure. Report new-feature and regression failures separately.
Remaining scheduled checkpoints after a candidate safety/cap termination have
policy-defined `Y = 0`, explicitly labeled **not executed**, not observed model
failures. Provider/controller faults and unknown usage are **unscored**, not
candidate failures; retain debits and stop for reconciliation, without replacement.

For block `b`, architecture `a`, chain `c`, define trajectory completion
`A[b,a,c] = mean(Y[b,a,c,1..4])`. Report the matched package difference per chain,
then the equally weighted mean over the two chosen chains. RQ2 reports the
difference between those two chain-specific contrasts. Do not treat the eight
dependent checkpoints as independent samples. Show every paired block and
trajectory; an exploratory 95% interval may resample **whole matched blocks**
(10,000 resamples, seed frozen before execution), never individual episodes.
With 12 blocks, uncertainty will be substantial and conditional to this case.

Unscored checkpoints remain null. If infrastructure prevents complete blocks,
report their full denominator and worst/best-case contrast bounds, not a
complete-case winner or a synthetic zero. Do not claim equivalence from a
non-significant contrast. No multiplicity-heavy model leaderboard or post-hoc
best subgroup is proposed.

Secondary reporting includes first regression, final cumulative success,
format/build/behavior/policy failures, changed files/bytes, submitted drift,
input/output usage, wall time and available cost. One submission per episode
does **not** estimate effort-to-success or human maintenance hours. Record all
attempts, missing usage as null and OAuth cost as null; token subsets are not
added twice. Execution-time differences remain conditional to the pinned route
and environment.

Verification is not delegated to an LLM's opinion. Build and external-contract
tests supply primary outcomes. Combine independent expected examples with
metamorphic/property checks where appropriate; test representative wrong
semantics, not only reference solutions. Any style-specific adapter must expose
the same observations without doing the maintenance work. Correct alternative
implementations must be accepted. The [test-oracle survey](https://doi.org/10.1109/TSE.2014.2372785)
distinguishes execution from knowing the right result; applying that distinction
to LLM-authored tests is our methodological inference, not its empirical finding.

Human-reviewed failure coding is explanatory. Predefine categories, retain
multi-cause/unknown labels, blind condition labels where practical without
claiming source can conceal its architecture, and disclose outcome visibility.
LLM suggestions may assist coding but are neither independent human review nor
the primary success oracle. Do not infer latent reasoning from generated prose.

## 7. Validity and reproducibility commitments

The main limits are one purposeful application pair, one source lineage,
investigator Nu familiarity, different APIs/physics, two chosen chains,
short trajectories, a restricted policy and possible public-source familiarity.
Balanced task review reduces avoidable bias; it cannot make those factors vanish.
Public historical fixes motivate new contracts, not copied solutions. More
replication of the same pair improves run-level precision, not project coverage.

Retain four separate identities: scientific specification; runner Git SHA;
environment/image profile; and invocation/attempt ID. Publish the selected
contracts, manifests, task provenance, reference/oracle sources, orientation,
sampling schedule, raw attempts, dispatch ledger, usage/null reasons and analysis
code once release and candidate-isolation requirements are satisfied. Record
repository bases and every adaptation, including failed feasibility checks.
Check source/asset redistribution permissions before building a public derivative.
Never publish OAuth material, secret hashes or private analysis transcripts.

Do not create another scientific version for a deployment typo. A future
candidate-observable treatment correction is reviewed and source-bound; existing
attempts remain identifiable and are not silently pooled across revisions.
No new proxy, generic framework or remote orchestration layer is proposed.

The completed F#/C# maintenance construction remains intact and unexecuted by
this proposal. Its larger F# reference envelopes at every episode are retained,
not optimized away. Existing H/E3a protocols, results, balances and holds are
not superseded or carried into this proposed study.

## 8. Human review and next decision

Review this document, not agent context, for the requested decisions:

| Decision | Recommendation | Current disposition |
| --- | --- | --- |
| Research claim | Behavioral maintenance of specified architectural packages; no language/paradigm superiority claim | Pending human review |
| Initial setting | Test Nu Breakout feasibility; reject/redirect if shared contracts erase the difference | Pending human review |
| Next authorized scope | **Phase A only**, one model-free pair/two-chain feasibility packet and subsequent review | Not yet authorized |
| Human validation | Two complementary reviewers, including a non-author; recruitment/availability unresolved | Not yet arranged |
| Future exploratory scale | 192 candidate + up to 5 separate integration calls, no old-balance carryover | Proposed; allocated 0 |
| Model and resources | Fill exact model, timing, byte, sandbox and environment settings after feasibility | Unselected; blocks live approval |
| Execution | Keep disabled until a separate source-bound Phase B review and explicit allocation | Disabled |

Human decision record: **not supplied**. Reviewer/date: **unfilled**. Approving
the research direction alone does not approve construction, recruitment or calls;
name the intended phase. A feasible negative or mixed result remains valuable.
If the contribution is no longer distinguishable from close work, or the case
cannot test it credibly, revising or abandoning it is the correct outcome.

Research preparation here used a Scite/primary-source review, one bounded
read-only AI extraction of public Nu history, main-agent methodological
self-review and a separate AI consistency pass on counts, inference and
authorization boundaries. That pass reported no important findings in its
limited scope; it was not independent source verification or human validation. The companion
[search/source ledger](architecture-maintenance-proposal-sources-2026-09-14.md)
records provenance and the limits of what was actually read or checked.
