# Research proposal: architectural organization and reliable agent maintenance

Date: **2026-09-14 HKT**. Revision base:
`0df55a45b5087a9420807617ea165c01c873f779`.
**For human review; not an adopted experiment.** This revision supplies the
introduction, terminology, literature synthesis, dataset and analytical methods
requested by the user. No construction, recruitment or experimental execution
is authorized by publication. Proposed settings and unresolved choices are
collected in Appendix A.

## 1. Introduction and background

### 1.1 Why study maintenance rather than only initial code generation?

Useful software must accommodate new requirements without losing behavior on
which its users already depend. Here, **software maintenance** means modifying
an existing implementation to repair defects or change its capabilities while
preserving obligations that have not been superseded. **Greenfield development**
starts without an inherited implementation. A **regression** is the loss of a
previously required behavior following a change. These are the working
definitions for this proposal, not a claim that every maintenance category is
covered by the selected tasks.

A system can satisfy today's tests yet organize responsibilities in ways that
make tomorrow's changes easier or harder. Parnas's classic modularization paper
treats modules as assignments of responsibility and compares decompositions by
the changes they accommodate. Its principle of **information hiding** is that a
module should conceal change-prone design decisions behind an interface, rather
than expose their details throughout the system
([Parnas, 1972](https://john.cs.olemiss.edu/~hcc/csci555/notes/localcopy/Parnas_Criteria_Decomposing.pdf)).
This is a design argument supported by examples, not a measured effect size for
modern language-model maintainers.

The practical concern also has empirical motivation. Xiao et al. studied
architecturally connected files and accumulated bug-fixing changes in seven
Apache projects. Their maintenance measure was **churn**—lines changed during bug
fixes—not directly observed developer hours
([Xiao et al., 2016](https://personal.stevens.edu/~lxiao6/papers/ICSE-16-Debt.pdf)).
Besker et al.'s repeated developer reports found substantial time attributed to
technical debt, although that debt was not exclusively architectural
([Besker et al., 2018](https://doi.org/10.1145/3194164.3194178)).
These studies make consequences of inherited design worth investigating; they
do not establish that one programming language or more abstraction always helps.

Large language models (LLMs) now provide another possible maintainer. A **coding
agent** combines a model with instructions, accessible information, actions and
an execution policy. Its success can therefore depend on both the inherited
program and the surrounding tools. SlopCodeBench already follows implementations
across successive changes, and CodeThread evaluates later work on different
predecessors. Neither initial generation nor a clean-looking final snapshot is a
sufficient description of that process
([Orlanski et al., 2026, v2](https://arxiv.org/html/2603.24755v2);
[Patel et al., 2026, v1](https://arxiv.org/html/2606.21804v1)).

The long-term motivation is reliable evolution of substantial software. The
first study proposed here is deliberately smaller: a controlled agent procedure
inside one comparative application case. Four consecutive maintenance episodes
would expose inherited consequences, not reproduce years of industrial work.
That distinction governs the claims and subsequent replication needs.

### 1.2 What architectural organization means here

**Software architecture**, in this study, is the organization of responsibilities,
dependencies and interaction rules relevant to a change. It is not a synonym
for the number of files, a programming language or aesthetic code quality.
Following the change-oriented perspective above and scenario-based architecture
evaluation such as [ALMA](https://www.cs.vu.nl/~hans/publications/y2004/alma.pdf),
we make the following terms operational before comparing implementations:

| Term | Meaning in this proposal |
| --- | --- |
| State ownership | Which component is responsible for a value and its invariants, and where updates are allowed to originate. |
| State transition | A change from one application state to another in response to an input, event or action. |
| Effect boundary | Where transitions interact with external or engine-managed behavior, such as input, timers, audio or entity creation. It need not be a globally pure boundary. |
| Architectural idiom | A conventional way of expressing those responsibilities in a language/framework; expressibility alone does not establish equal clarity or cost. |
| Architectural package | One concrete implementation together with its API use, conventions and documentation. Comparing packages does not isolate a single architectural feature. |
| Behavioral contract | A specification of externally observable obligations. A test oracle decides whether observations meet it; passing finite tests does not prove complete equivalence. |
| Maintenance episode / trajectory | One requested change / the sequence of inherited submissions for one starting implementation. |
| Maintainability outcome | Here, successful cumulative behavior under a fixed response budget. This is not a direct measure of human effort, comprehension or effort-to-success. |

The provisional case uses **Nu**, an F# game engine that supports two application
styles. F# is the language held constant, not the treatment being tested.
**MMCC** means Model-Message-Command-Content: the application organizes a model,
messages, commands and declarative content. Nu describes **ImSim** as its
immediate-mode API derived from ImGui; interaction and content are expressed
through processing code. These names and lineage come from the
[pinned public README](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/ReadMe.md),
not from independent evidence that either style is superior.

**Model-View-Update (MVU)** organizes an application around a model, its
presentation and updates driven by messages; Fowler provides a formal account
and communication extension
([Fowler, 2020](https://doi.org/10.4230/LIPIcs.ECOOP.2020.14)).
**Immediate mode** describes an application/library interface, not a guarantee
about internal storage, rendering or scheduling. Nu's particular processing API
is the subject here; the broader category need not refresh continuously
([Dear ImGui's author documentation](https://github.com/ocornut/imgui/wiki/About-the-IMGUI-paradigm)).
It does not imply that persistent state or messages are absent.
Thompson et al.'s adaptive-optics application combines state
machines, event messages and Dear ImGui
([Thompson et al., 2024](https://arxiv.org/html/2407.07207v1)).
Consequently this is not “state machines versus immediate mode,” “pure versus
stateful,” or “functional versus object-oriented.” The relevant contrast is
where responsibilities are organized in the particular programs.

## 2. Literature review

### 2.1 Architecture and human maintenance: consequences, not universal scores

Three approaches in the established literature inform the study. First,
decomposition arguments connect responsibility boundaries to anticipated change
([Parnas, 1972](https://doi.org/10.1145/361598.361623)). Second, ALMA elicits
change scenarios, analyzes their architectural impact and distinguishes goals
such as comparison, prediction and risk assessment
([Bengtsson et al., 2004](https://doi.org/10.1016/S0164-1212(03)00080-3)).
It supplies a rationale for prespecifying kinds of change rather than selecting
tasks because a favored design handles them well.

Third, empirical debt studies examine consequences in existing systems:
repository history in Xiao et al., and repeated developer self-reports in Besker
et al. They provide complementary observations but different outcomes and
confounders. **Technical debt** denotes design/implementation decisions whose
future consequences can impose additional work; it is not identical to every
static warning or to architecture alone. In a counterweight to simple
“more warnings means more delay” claims, Lenarduzzi et al. did not establish a
robust general increased-delay relationship for SonarQube debt items and issue
lead times in their studied projects. Selected associations and scope limits
remain important
([Lenarduzzi et al., 2021](https://doi.org/10.1109/SEAA53835.2021.00032)).
Therefore churn, warning counts, elapsed issue time and active labor should not
be substituted for one another.

Functional architecture literature supplies possible mechanisms and examples,
rather than the missing effect estimate. GUI Easy describes functional
composition and state ownership over an imperative GUI foundation
([Knoble and Popa, 2023](https://defn.io/papers/fungui-funarch23.pdf)).
Fowler's work is formal; GUI Easy is an experience report; Thompson et al. is a
domain-system report. None establishes the downstream maintenance advantage of
Nu's MMCC or ImSim packages. Their value is to help state testable mechanisms
without treating practitioner lineage as either proof or disqualification.

### 2.2 Architectural lineage, prior comparisons and credible alternatives

**The lineage is established more strongly than the proposed comparison.**
Nu's [dated MMCC documentation](https://github.com/bryanedds/Nu/wiki/Model-View-Update-for-Games-via-MMCC/9cb6d2fe3865c68fd4ac3a945efb81946ef59174)
explicitly generalizes MVU to simulation, separate commands and per-simulant
organization. Its [dated ImSim documentation](https://github.com/bryanedds/Nu/wiki/Immediate-Mode-for-Games-via-ImSim/e657be2c650864c4917fdf81f23e7775e76e9b95)
also calls that API declarative, using scoped identity derived from ImGui.
These are author descriptions, not comparative maintenance evidence.
MVU has a peer-reviewed formal account in Fowler (2020). Sperber and Schlegel's
[2025 functional-UI architecture paper](https://doi.org/10.1145/3759163.3760429)
compares MVC, functional toolkits and MVU through design examples. It identifies
tradeoffs: deriving views can avoid separate update logic, while global state,
UI-local state and message dispatch create modularity problems. Its conclusion
is not that functional organization universally wins. This is conceptual and
implementation-based analysis, not a controlled maintenance effect estimate.
The paper does not directly compare MVU with ImGui.

There is also published immediate-/retained-mode comparison. Zuev et al.'s
[2025 visualization-interface paper](https://doi.org/10.20998/2413-4295.2025.02.08)
describes an immediate-mode implementation and argues for synchronization,
resource and development benefits. Only its abstract is used here; its claims
cannot establish a controlled longitudinal result or absence of additional
methods. Brendel and Liedtke's 2022 mixed-reality workshop paper is another
relevant lead, but primary body access is restricted
([registered DOI](https://doi.org/10.18420/vrar2022_1678)). It is not treated as
a verified direct MVU comparison. Comparing graphics rendering modes alone is
also not a comparison of application state organization.

Across the recorded exact-name, expanded-lineage and cross-comparison searches,
we have **not verified a scholarly head-to-head MMCC/ImSim study**, nor a
controlled MVU/ImGui downstream-maintenance experiment. That is a scoped search
result, not proof that none exists. Acronyms produced many unrelated matches;
body access and search indexing remain incomplete. Practitioner comparisons
are not absent, but they do not supply the missing effect estimate.

**Are these two major architectures?** MVU and immediate-mode interfaces are
recognizable approaches with published analyses and implementations. That does
not make them an exhaustive or mutually exclusive taxonomy, or make Nu's two
variants representative of all game-engine architectures. They address partly
different questions: MVU organizes state transitions and presentation;
immediate mode concerns how application code communicates with an interface.
They can coexist. This proposal therefore selects **two concrete organizations
within an informative case**, not two representatives of the entire functional
and object-oriented paradigms. Population prevalence is not established.

**“Mathematical essence” and “operational semantics” need careful translation.**
The exact two phrases were not located in the bounded public Nu source/wiki
inspection; we retain them as the user's characterization, not a verified author
quotation. The distinction suggests emphasizing domain state/rules versus the
processing steps that enact interaction. This is a useful hypothesis about
representation, not a measured property or a formal classification. In programming
language research, *denotational semantics* assigns mathematical meanings, while
*operational semantics* describes execution by transition rules; the latter is
also mathematical. Indeed, Fowler's MVU calculus explicitly has small-step
operational semantics (§2.2). Conversely, Elliott and Hudak's
[Functional Reactive Animation](https://doi.org/10.1145/258948.258973) gives
time-varying behaviors a denotational account (abstract-level evidence here).
Mathematical modeling is not limited to turn-based interaction, and MMCC is not
thereby identical to continuous-time FRP. Elm's later MVU design departed from
its earlier FRP formulation.

For this study, translate those descriptions into inspectable questions:

| Dimension | What reviewers must locate in both programs | Potential maintenance consequence, not a finding |
| --- | --- | --- |
| Domain representation | State values, invariants and permitted transitions | Can one rule change be expressed without missing dependent obligations? |
| Interaction organization | Where input, conditions and actions are associated | Is a local interaction easy to change, or spread over message/effect wiring? |
| Synchronization | Which state is authoritative and how presentation/entities follow it | Can views or engine state become stale, duplicated or inconsistent? |
| Time and lifetime | Ordering, identifiers, creation/removal, delayed actions and cancellation | Do restart, pause and conditional-content changes preserve lifecycle behavior? |
| Modularity | Boundaries, composable parts and cross-boundary coordination | Does a change remain local, or does dispatch/state plumbing spread it? |

Both programs must be mapped, including hybrid behavior. The pinned
[MMCC gameplay source](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Projects/Breakout%20Mmcc/Gameplay.fs#L85)
updates every frame and calls world audio functions inside its model-update
path; it is neither turn-based nor an enforced pure core. ImSim also has typed
properties and declarative synchronization. Both Breakout samples are real-time.
Neither genre nor API label substitutes for inspection. The proposed
same-game comparison does not vary game genre. Strong separation may help one
change and add coordination for another; compact local code may reduce wiring
yet expose order dependencies. These opposing predictions motivate RQ2.

**Credible** means a defensible implementation of the selected obligations,
not equal code size, identical internals or a claim of equal expected performance.
Public author-maintained examples establish provenance, not validation. Before
either qualifies, Phase A must show both pass the shared selected baseline
contracts, retain their intended idioms, offer genuine variation on the mapped
dimensions, and survive non-author review for avoidable handicaps. Those checks
are currently pending. “Provisional candidate pair” is the accurate current
status; the proposed review criteria appear in §4.2.

### 2.3 How agent research approaches maintainability

Existing agent work tackles at least three different questions: how code evolves
under repeated changes; whether inherited code affects later issue resolution;
and whether an agent can perform a requested structural improvement. Those
questions overlap with this proposal but should not be conflated.

| Approach and primary edition | Intervention or evaluated work | Outcome and remaining distinction |
| --- | --- | --- |
| [SlopCodeBench v2](https://arxiv.org/html/2603.24755v2) | Agents repeatedly extend their own persistent implementations, with fresh conversations. | Correctness, structural erosion and resources, including next-checkpoint associations. Repeated maintenance and cost analysis are already covered; starting organizations are not the proposed assigned pair. |
| [CodeThread v1](https://arxiv.org/html/2606.21804v1) | Later issue resolution on human- versus agent-authored predecessors. | Direct downstream maintenance behavior. The contrast is predecessor authorship, not a declared architectural package; neither contrast equates all source differences. |
| [Needle in the Repo v1](https://arxiv.org/html/2603.27745v1) | Supplied starters and architectural boundaries guide repository edits. | Functional and structural oracles. Supplying architecture is not new; the proposed outcome does not require conformity to one preferred internal design. |
| [SWE-CI v4](https://arxiv.org/html/2603.03823v4) | An architect/programmer loop evolves a repository base toward target-test behavior, with dynamically selected requirements. | Correctness trajectories and regressions already serve as maintainability proxies. Our proposed change chains are fixed in advance, and the assigned starting packages are the contrast. |
| [StaminaBench v1](https://arxiv.org/html/2606.19613v1) | Agents create an HTTP service and maintain it through generated changes; feedback and retries vary. | Black-box correctness and turns survived. It already examines policy effects; it does not supply the proposed two initial architectural packages. |
| [RepoProbe v2](https://arxiv.org/html/2608.04783v2) | Repository-level architecture/comprehension questions answered without code edits. | Weighted textual checklists, not subsequent behavioral maintenance of assigned alternatives. |
| [RepoMod-Bench v1](https://arxiv.org/html/2602.22518v1) | Reimplement source repositories in target languages with freedom over internal design. | Hidden implementation-agnostic tests support functional equivalence; target architecture is chosen by the agent, not an assigned starting architecture followed by maintenance. |
| [SWE-Refactor v1](https://arxiv.org/html/2602.03712v1) | Developer-derived repository refactoring tasks. | Compilation, tests and intended-transformation checks; not subsequent maintenance after assignment to either credible architecture. |
| [SmellBench, Dinu et al., v2](https://arxiv.org/html/2605.07001v2) | Repair of architectural code smells, with expert false-positive judgments. | Repair, judgment and net smell changes. The study warns that a disappearing warning may not represent real architectural improvement. |
| [SmellBench, Lin et al., v1](https://arxiv.org/html/2606.05574v1) | Repair of injected smells with fine-grained evaluation. | Tests and refactoring-quality assessment, including an LLM judge. This is a different paper from Dinu et al., not another edition. |
| [Sambu et al., ICSA 2026](https://conf.researchr.org/details/icsa-2026/icsa-2026-papers/27/LLMs-for-Architectural-Refactoring-An-Exploratory-study-on-Monoliths-to-Microservice) | LLM proposals for monolith-to-microservice architectural refactoring. | The accessible conference abstract reports architectural metrics. Full-methods access limits the strength of any claim about outcomes not studied. |

The cited arXiv benchmark editions are treated as preprints unless a separate
venue is explicitly identified; Sambu et al. has an ICSA proceedings record. A DOI by itself
does not establish peer review. **Refactoring** means changing internal
organization while intending to preserve behavior; successful refactoring need
not demonstrate that future feature changes become easier. Likewise a
**code/architecture smell** is an indicator of a potential design problem, not
an external behavioral requirement.

Adjacent systems-engineering work also uses AI-assisted architectural analysis.
The registered abstract of [Langmead et al. (2026)](https://doi.org/10.1002/iis2.70208)
describes multi-domain dependency models for automotive traceability, security
impact analysis and test prioritization. That is relevant impact-analysis work,
not established evidence for the proposed agent-maintained package comparison;
its body remains inaccessible. Crossref resolves the previously missing identity.

### 2.4 Candidate gap and intended research value

The bounded literature assessment supports investigating this question:
**what happens to later behavioral maintenance when agents inherit credible,
specified alternative architectural organizations?** Human architecture/debt
studies motivate the mechanism, structural agent benchmarks examine
transformations or compliance, and inherited-code benchmarks establish the
importance of downstream evaluation. The proposed combination supplies
alternative starting packages and evaluates their consequences on the same
subsequent obligations, including plausible countervailing kinds of change.

This is not a claim that maintenance, architectural intervention or a similar
experiment has never been studied. The closest-work distinction is conditional
on the identified editions and reading extent; relevant unread leads and access
failures remain in the [source ledger](architecture-maintenance-proposal-sources-2026-09-14.md).
The search is scoping work, not a systematic review or proof of novelty.
A metadata failure is an access problem to resolve through registries and primary
sources, not evidence that a study is irrelevant.

The expected contribution is a reproducible **comparative case** linking
specified organization to observed completion, regressions and failure paths.
A credible null, opposite or task-dependent result is useful. A reusable paired
dataset with contracts and inherited-state records is a second contribution.
The first case cannot establish a general F# advantage, an architecture-mediated
context-window effect, large-project productivity or human-team savings.
Those require separately justified comparisons and replication.

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

## 4. Method

### 4.1 Study design and unit of inference

We propose a **comparative case study with a controlled agent procedure**.
Purposeful selection of an informative case is consistent with case-study
methodology; it is not random sampling of all projects or architects
([Runeson and Höst, 2009](https://doi.org/10.1007/s10664-008-9102-8);
[Baltes and Ralph, 2022](https://arxiv.org/html/2002.07764v6)).
The assigned treatment is the starting architectural package. Language, engine
revision, requested obligations, accessible semantic information and agent policy
are held constant where feasible; residual API/implementation differences remain
part of the package.

A **matched block** contains the four architecture-by-chain combinations run
under the same selected model configuration and a balanced temporal schedule.
A **trajectory** follows one package through one four-episode chain. Repeated
blocks measure variability of the agent procedure within this fixed case, not
variability across independently authored systems. Phase A constructs and
validates the dataset without model calls. Phase B, if separately approved,
collects the exploratory observations.

### 4.2 Dataset: sources, construction and selection

The dataset is **proposed, not already collected**. Its existing source material
and future research artifacts are distinct:

| Dataset component | Proposed unit/count | Current availability |
| --- | --- | --- |
| Initial applications | 2 Breakout implementations in one pinned Nu repository | Public source exists; shared selected contracts and isolated runtime feasibility unverified |
| Change specifications | 2 chains × 4 episodes = 8 contracts applied to both packages | Illustrative families below; executable task definitions not authored |
| Trusted reference continuations | 2 packages × 8 episodes = 16 successor snapshots, plus 2 original baselines | Not constructed for this Nu case; not the earlier simulation's checkpoints |
| Evaluation material | External behavior cases, semantic faults, allowed-file manifests and architecture annotations | To be authored and reviewed in Phase A; case counts not yet fixed |
| Agent observations | Up to 48 trajectories / 192 scheduled episode records | None collected; allocated 0 |
| Provenance and review data | Task origin, rejected candidates, adaptations, reviewer expertise and dispositions | Public-history leads exist; task/expert review not completed |

This is purposive case/task selection, not an export of every GitHub issue.
The bounded public search located 29 unique Nu issue/PR records, followed by
selected relevant commits; only the leads below motivated potential scenarios.
Neither their frequency nor issue-closing time is an outcome measure. The
sampling frame is application-level state/lifecycle and interaction changes
expressible against both styles at the pinned engine revision. Engine migration,
unmatched physics repair and tasks without independent observable contracts are
excluded unless a separately reviewed scope replaces this one.

Public source candidate:
[`bryanedds/Nu@064f7ae92a8506689cd91aff5e6804a375d6ef3d`](https://github.com/bryanedds/Nu/tree/064f7ae92a8506689cd91aff5e6804a375d6ef3d).
The [root README](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/ReadMe.md)
and [MMCC](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Projects/Breakout%20Mmcc/Breakout.fs)
and [ImSim](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Projects/Breakout%20ImSim/Breakout.fs)
applications provide author-maintained candidate alternatives, not yet a
validated experimental pair. Their intended
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

The review packet must justify **credibility and contrast**, rather than merely
ask whether each program “looks idiomatic”:

| Criterion | Required Phase A evidence | Current state |
| --- | --- | --- |
| Shared capability | Both baselines satisfy the same selected externally observed contracts, with physics tolerances justified | Unverified |
| Idiom fidelity | Source-linked mapping of state, transitions, effects, content, identity and lifetime; reviewers identify departures and hybrids | Initial source inspection only |
| No avoidable handicap | Equivalent required API knowledge and documentation; no intentionally broken baseline or unnecessary indirection | Pending review |
| Substantive contrast | At least one change-relevant organizational difference remains after test seams and adaptations | Plausible, not validated |
| Balanced changes | Contract-first task provenance; independent predictions of affected responsibilities for both styles, including adverse cases | Tasks not authored |
| Independent challenge | Non-author review records objections, disagreements, repairs and rejected options before outcomes | Not arranged |

Record expected coordination by **task × responsibility**, not by declaring all
turn-based tasks “MMCC tasks” and all continuous tasks “ImSim tasks.” If review
finds only different physics APIs, a contrived weak variant or no meaningful
remaining organizational contrast, the case fails this purpose. Existing
examples need not already have been evaluated in a paper; their research
credibility must be earned by these checks, not borrowed from their names.

**Reject or redirect this case** if credible shared contracts require replacing
either architecture, the comparison reduces to incompatible physics behavior,
or safe observation needs substantial new engine/runner machinery. Missing
feasibility is not permission to implement a new framework. Changing the pin,
case or treatment must be explicit and reviewed before construction proceeds
beyond the approved scope.

### 4.3 Collection procedure and sample rationale

The proposed exploratory design has 12 matched blocks, each with 2 packages ×
2 chains × 4 episodes: at most **192 candidate dispatches / 48 trajectories**.
Up to five unrelated integration calls would be a separate allowance, making
197 the total possible future ceiling, not a present allocation. Exact model,
resource and sandbox choices remain unfilled in Appendix A.

Twelve blocks are a bounded exploratory ceiling, allowing three repetitions of
four balanced chain/style ordering combinations. This is **not a power
calculation** or evidence that 192 calls establish a general architecture effect.
Freeze the randomized schedule and seed before calls, interleave matched arms
in time, and keep episode order fixed. The blocks sample repeated agent runs,
not independent projects, architects or task families. There is no outcome-driven
sample extension. A later confirmatory replication requires its own precision
justification and independent workload/authoring units.

### 4.4 Candidate information and continuation policy

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

### 4.5 Outcomes and oracle validation

For each scheduled episode retain a record containing block/package/chain/episode
identifiers, request and predecessor identities, raw response, applied source,
format/build/contract statuses, terminal reason and available resource usage.
Store new-feature checks separately from retained-obligation checks. This makes
the measured outcome traceable to both the input state and observable evidence.

The primary checkpoint outcome `Y` is 1 for a policy-valid submission that
builds and passes the current and all prior, non-superseded behavioral contracts.
Observed format, build, behavioral or candidate-policy failure gives `Y = 0`;
retain the separate cause rather than collapsing the raw record. Remaining
scheduled checkpoints after a candidate safety/cap termination have
policy-defined `Y = 0`, labeled **not executed**, not observed model failures.
Provider/controller faults and unknown usage remain **null/unscored**; retain
debits and stop for reconciliation without automatic replacement.

Build and external-contract tests supply primary outcomes, not an LLM's quality
opinion. Reference implementations are witnesses, not the only accepted source
shape. Combine independently expected examples with property/metamorphic checks
where appropriate and verify sensitivity to representative wrong semantics.
An observation adapter must expose equivalent behavior without implementing the
feature for the candidate. Candidate execution must be isolated from credentials,
reference solutions and writable scoring machinery. These mechanisms are not
implemented or validated for Nu yet.

The [test-oracle survey](https://doi.org/10.1109/TSE.2014.2372785) distinguishes
executing a test from determining its correct result. Applying that distinction
to LLM-authored test suites is our methodological inference. A passing trusted
fixture or plausible generated test does not establish an adequate oracle.

### 4.6 Analytical methods

**Primary quantitative analysis (RQ1).** Let `b = 1..12` index matched blocks,
`a` the MMCC or ImSim package, `c` the coordinated-state or local-interaction
chain, and `e = 1..4` its episodes. For complete scored blocks:

```text
A[b,a,c] = (Y[b,a,c,1] + ... + Y[b,a,c,4]) / 4
D[b,c]   = A[b,MMCC,c] - A[b,ImSim,c]
Delta[c] = mean over b of D[b,c]
Delta    = (Delta[coordinated] + Delta[local]) / 2
Gamma    = Delta[coordinated] - Delta[local]
```

`Delta` is the primary equally weighted package contrast; positive values favor
MMCC within this case. Show both chain-specific `Delta[c]` values and every
paired trajectory, rather than only a winner. Episode and chain weights are fixed
before outcomes. Secondary quantities are final cumulative success and first
regression, with their denominators.

**Conditional contrast and mechanism evidence (RQ2).** `Gamma` is an exploratory
comparison of the two chosen chain contrasts. It is not a general family effect:
each family contains only one authored chain. Compare its direction and individual
task failures with predictions fixed during dataset review. Do not adjust away
source size as though it were necessarily unrelated noise; it may be part of the
package. No causal mediation model or large language/model/architecture factorial
is proposed.

**Uncertainty and missingness.** If all 12 blocks are fully scored, report exploratory 95%
percentile intervals from 10,000 resamples of the **12 whole matched blocks**,
with the analysis seed fixed before calls. Each sampled block retains all its
packages, chains and dependent episodes. The independent-run approximation is
conditional to the temporal/model configuration; shared provider drift can weaken
it. Report that limitation. Twelve blocks are not a power justification, and a
non-significant difference does not demonstrate equivalence.

If infrastructure leaves unscored checkpoints, keep them null and report the full
scheduled denominator. Bound each contrast by allowing missing `Y` values in
`[0,1]` according to its signed coefficients; do not replace the raw nulls with
synthetic observations or select complete cases to announce a winner. These
bounds describe missing-data uncertainty, not a confidence interval. A later
confirmatory study needs independent workload replication and a separate
precision/power rationale.

**Failure and resource analysis (RQ3).** Predefine a coding guide for missed
domain obligations, transition/state coordination, interaction/effect wiring,
API-knowledge errors, response-format/build errors and inherited damage. Human
reviewers would inspect source changes and failing contract evidence, permitting
multiple causes and unknown attribution. Record their initial labels and
disagreements before adjudication; report agreement counts. Blinding labels where
practical does not conceal architectural source structure. LLM suggestions are
assistance, not independent human validation or evidence of hidden reasoning.

Report failures, source/patch spread and architectural drift alongside usage,
latency and available cost for **all** assigned attempts, not only successful ones.
Keep missing usage null, report coverage, preserve token subset semantics and keep
OAuth monetary cost null. Separate model time, evaluator time and setup.
One submission per episode measures performance within that policy; it cannot
estimate effort-to-success or human maintenance hours. Fixing an output format
also does not establish its neutrality: Yang's
[abstract-only format study](https://arxiv.org/abs/2607.21674) reports interactions,
but its effect sizes are not imported into this design.

## 5. Validity and reproducibility commitments

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

## 6. Human review and next decision

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

The earlier publication received an AI consistency pass, not human validation.
This revision adds main-agent synthesis and bounded read-only AI metadata/source
extraction. Its checks and corrected metadata are recorded separately in the
[source ledger](architecture-maintenance-proposal-sources-2026-09-14.md); the old
review is not presented as approval of the rewritten document.


## References

Primary editions and reading limits are recorded in the companion ledger.
This bibliography includes explicitly marked access-limited leads; listing a
reference does not mean its full methods were read. Public Nu source and
practitioner documentation are linked at the relevant claims above.

- Parnas, D. L. (1972). *On the criteria to be used in decomposing systems into modules*. Communications of the ACM, 15(12), 1053–1058. [DOI](https://doi.org/10.1145/361598.361623).
- Bengtsson, P., Lassing, N., Bosch, J., and van Vliet, H. (2004). *Architecture-level modifiability analysis (ALMA)*. Journal of Systems and Software. [DOI](https://doi.org/10.1016/S0164-1212(03)00080-3).
- Xiao, L., et al. (2016). *Identifying and quantifying architectural debt*. ICSE, 488–498. [DOI](https://doi.org/10.1145/2884781.2884822).
- Besker, T., Martini, A., and Bosch, J. (2018). *Technical debt cripples software developer productivity*. TechDebt, 105–114. [DOI](https://doi.org/10.1145/3194164.3194178).
- Lenarduzzi, V., et al. (2021). *Technical Debt Impacting Lead-Times: An Exploratory Study*. SEAA, 188–195. [DOI](https://doi.org/10.1109/SEAA53835.2021.00032).
- Fowler, S. (2020). *Model-View-Update-Communicate: Session Types Meet the Elm Architecture*. ECOOP, 14:1–14:28. [DOI](https://doi.org/10.4230/LIPIcs.ECOOP.2020.14).
- Sperber, M., and Schlegel, M. (2025). *Evolution of Functional UI Paradigms*. FUNARCH, 27–38. [DOI](https://doi.org/10.1145/3759163.3760429).
- Zuev, A., et al. (2025). *Algorithm and Software Implementation of Immediate Mode Interface for Visualization Systems*. Bulletin of NTU «KhPI», New solutions in modern technologies, 2(24), 58–65; English title, abstract-only use. [DOI](https://doi.org/10.20998/2413-4295.2025.02.08).
- Brendel, F., and Liedtke, S. (2022). *Exploring the immediate mode GUI concept for graphical user interfaces in mixed reality applications*. GI VR/AR Workshop; metadata-verified lead, body inaccessible. [DOI](https://doi.org/10.18420/vrar2022_1678).
- Elliott, C., and Hudak, P. (1997). *Functional reactive animation*. ICFP, 263–273; abstract-level use. [DOI](https://doi.org/10.1145/258948.258973).
- Knoble, D. B., and Popa, B. (2023). *Functional Shell and Reusable Components for Easy GUIs*. FUNARCH, 20–28. [DOI](https://doi.org/10.1145/3609025.3609478).
- Thompson, W., et al. (2024). *Real-time adaptive optics control with a high level programming language*. SPIE; related arXiv:2407.07207v1. [DOI](https://doi.org/10.1117/12.3020480).
- Orlanski, G., et al. (2026). *SlopCodeBench: Benchmarking How Coding Agents Degrade Over Long-Horizon Iterative Tasks*. arXiv preprint, v2. [DOI](https://doi.org/10.48550/arXiv.2603.24755).
- Patel, S., et al. (2026). *Is Agent Code Less Maintainable Than Human Code?*. arXiv preprint, v1; CodeThread. [DOI](https://doi.org/10.48550/arXiv.2606.21804).
- Zhu, H., et al. (2026). *Needle in the Repo: A Benchmark for Maintainability in AI-Generated Repository Edits*. arXiv preprint, v1. [DOI](https://doi.org/10.48550/arXiv.2603.27745).
- Chen, J., et al. (2026). *SWE-CI: Evaluating Agent Capabilities in Maintaining Codebases via Continuous Integration*. arXiv preprint, v4. [DOI](https://doi.org/10.48550/arXiv.2603.03823).
- Sobal, V., et al. (2026). *StaminaBench: Stress-Testing Coding Agents over 100 Interaction Turns*. arXiv preprint, v1. [DOI](https://doi.org/10.48550/arXiv.2606.19613).
- Yang, Y., et al. (2026). *RepoProbe: Benchmarking Architecture-Aware Repository Comprehension with Checklists*. arXiv preprint, v2. [DOI](https://doi.org/10.48550/arXiv.2608.04783).
- Li, X., et al. (2026). *RepoMod-Bench: A Benchmark for Code Repository Modernization via Implementation-Agnostic Testing*. arXiv preprint, v1. [DOI](https://doi.org/10.48550/arXiv.2602.22518).
- Xu, Y., Yang, J., and Chen, T.-H. (2026). *SWE-Refactor: A Repository-Level Benchmark for Real-World LLM-Based Code Refactoring*. arXiv preprint, v1. [DOI](https://doi.org/10.48550/arXiv.2602.03712).
- Dinu, I. G., Mihăescu, M. C., and Rebedea, T. (2026). *SmellBench: Evaluating LLM Agents on Architectural Code Smell Repair*. arXiv preprint, v2. [DOI](https://doi.org/10.48550/arXiv.2605.07001).
- Lin, F., et al. (2026). *SmellBench: Towards Fine-Grained Evaluation of Code Agents on Refactoring Tasks*. arXiv preprint, v1; distinct from Dinu et al.. [DOI](https://doi.org/10.48550/arXiv.2606.05574).
- Sambu, A., et al. (2026). *LLMs for Architectural Refactoring: An Exploratory Study on Monoliths to Microservices*. ICSA, 268–279; conference abstract and registry metadata. [DOI](https://doi.org/10.1109/ICSA66085.2026.00033).
- Langmead, N., et al. (2026). *Deployment of a Multi-Domain Model DSM based Approach for Automotive System Development: Improving Traceability and Security Impact Analysis*. INCOSE International Symposium, 36(1), 1564–1584; registered abstract only. [DOI](https://doi.org/10.1002/iis2.70208).
- Runeson, P., and Höst, M. (2009). *Guidelines for conducting and reporting case study research in software engineering*. Empirical Software Engineering; online 2008. [DOI](https://doi.org/10.1007/s10664-008-9102-8).
- Baltes, S., and Ralph, P. (2022). *Sampling in software engineering research: a critical review and guidelines*. Empirical Software Engineering; related arXiv:2002.07764v6. [DOI](https://doi.org/10.1007/s10664-021-10072-8).
- Barr, E. T., et al. (2015). *The Oracle Problem in Software Testing: A Survey*. IEEE Transactions on Software Engineering; abstract/front matter only. [DOI](https://doi.org/10.1109/TSE.2014.2372785).
- Yang, Y. (2026). *Output Format x Model Identity: Interaction Effects in Single-Round Coding Agent Performance*. arXiv preprint, v1; abstract-only use. [DOI](https://doi.org/10.48550/arXiv.2607.21674).

## Appendix A. Proposed settings at a glance

These values remain proposals. Phase A and Phase B require separate explicit
approvals; the table is not an executable configuration.

| Setting | Proposed value / current state | Where defined |
| --- | --- | --- |
| Comparison | 2 architectural packages, 1 F# application pair, 1 pinned engine | Sections 3 and 4.2 |
| Workload | 2 separate chains × 4 inherited episodes; 8 task contracts, currently unauthored | Section 4.2 |
| Replication | 12 matched blocks; each block contains both architectures on both chains | Sections 4.3 and Appendix A |
| Candidate dispatch ceiling | 12 × 2 × 2 × 4 = **192**; 48 trajectories. Allocated **0**, used **0** | Sections 4.3 and Appendix A |
| Integration ceiling | Up to **5** unrelated shakedown dispatches, separately approved/charged; allocated **0** | Sections 4.3 and Appendix A |
| Total possible future dispatches | **197**, not 197 plus unused historical balances; no automatic replacements | Sections 4.3 and Appendix A |
| Model / effort / decoding | One configuration; exact identifiers and supported settings **not selected** | Must be filled before Phase B approval |
| Candidate interaction | Fresh conversation per episode; no tools, no compile/test feedback, no repair turn; one submission | Section 4.4 |
| Durable state | Submitted editable application source plus explicitly designated candidate notes; all bytes charged | Section 4.4 |
| Context treatment | Complete eligible source and common information, no context-pressure arm, retrieval or truncation | Section 4.4 |
| Input/output byte caps | Same cap per direction for both styles; proposed reference-fit rule in §4.4. Actual values **unmeasured** | Phase A measurements required |
| Candidate notes | One optional UTF-8 file, maximum **4,096 bytes**, counted within input/output caps | Section 4.4 |
| Wall time / CPU / RAM / process limits | **Not selected**; require measured Phase A envelope and explicit Phase B values | No execution-ready environment claimed |
| Runner / image / environment | No new selection; exact SHA, digest and profile **unfilled** | Phase B freeze required |
| Human review / live flags | **Pending / disabled**; OAuth staging **not authorized** | Section 6 |
