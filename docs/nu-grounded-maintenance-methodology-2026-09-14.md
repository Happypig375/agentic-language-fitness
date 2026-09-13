# A feasible Nu-grounded maintenance study

**Date:** 2026-09-14 HKT. **Inspected ALF source:**
`7800549dd3ed598a4a7cfda235406ed2114f9537`.
**Status:** methodological clarification and unadopted recommendation. No new
engine, workload, comparator, adapter, participant recruitment or live execution
is selected. The existing construction and human-review hold remain unchanged.

## The clarification

The [frontier assessment](research-frontier-gap-assessment-2026-09-14.md) described
conditions for a stronger, generalizable architecture-effect study. They are not
entrance requirements for every worthwhile first paper. In particular, one need
not commission independently randomized architects or find papers certifying
that Nu has a good architecture before studying it.

An attainable first contribution is a **Nu-grounded study of how particular
architectural decisions help or hinder specified maintenance changes**. Existing
source and development history can anchor the case. A later controlled agent
comparison can test concrete hypotheses within that setting. Evidence strength,
scope and terminology must match what is actually done.

The [source ledger](nu-grounded-maintenance-sources-2026-09-14.md) records primary
methods, F# project examples, exact searches, access failures and DOI decisions.

## Research value takes priority over the original comparison

The user's subsequent direction permits changing this analysis to increase
research value for a validated gap. This is permission to reconsider the question
and design, not evidence that a specific replacement experiment is approved.
Neither F#/C# nor Nu should be a fixed requirement if a better-supported and
more identifiable comparison is available. An F# win is not a success criterion.

The [closest-work assessment](research-frontier-gap-assessment-2026-09-14.md)
already narrows the opportunity: inherited-code maintenance and multi-episode
benchmarks exist; even supplied architectural probes are not new. The useful
candidate gap is testing the **downstream behavioral consequences of credible,
specified architectural alternatives**, with costs and failure modes, rather
than treating preferred structure as success by definition. This is a bounded,
source-supported gap assessment, not proof that no overlapping paper exists.

Accordingly, prefer a small same-language/engine contrast if it actually varies
an important design decision. Use Nu history to motivate the mechanism and
change families; treat F#/C# transfer, model-capability interactions and context
limits as optional later questions, not a required factorial programme. A
natural whole-engine comparison remains legitimate, but has a different,
package-level interpretation. A descriptive case alone does not close the
architectural-intervention gap.

Before adopting a study, the feasibility sheet should make one comparison
explicit: what the closest papers already intervene on and measure, what this
proposal changes, and what observation could refute its prediction. Reject or
redirect the proposal if that distinction disappears, if the alternatives cannot
be made credible, or if success is only an architecture-preference score. This
is a proposed selection criterion, not a claim that a publication is guaranteed.

### How MMCC and ImSim could answer that gap

The user's clarification is that Bryan adapted MMCC from MVU and ImSim from
ImGui, and the two Breakout examples are intended to operate the same. Record
that as design lineage and intended parity, not evidence that their maintenance
effects have been validated. The research opportunity is not to rename those
patterns or require literature that already proves the desired result.

A concrete proposed question is:

> Under one fixed agent policy, how does organizing changes through explicit
> messages/state transitions versus immediate-mode interaction processing affect
> regression-free maintenance across coordinated-state and local-interaction
> change families?

This is a comparative mechanism hypothesis. MMCC and ImSim could instantiate
it, but their names alone do not isolate one causal feature. Both are legitimate
Nu application styles; this is not functional versus OO, good versus bad design,
or pure versus stateful code. Identify the actual state ownership, update flow,
effect boundaries and observation points in the selected applications.

Nor are immediate-mode interaction and explicit state machines opposing
principles. The user's DOI correction led to a concrete counterexample:
Thompson et al.'s [adaptive-optics system](https://arxiv.org/html/2407.07207v1)
combines hierarchical state machines, event messages and a Dear ImGui interface
(§§2.4–2.5). Thus the proposed question concerns **where and how responsibilities
are organized in these implementations**, not whether a system has messages
or is immediate-mode at all. MMCC/ImSim are initially package contrasts; isolating
one property would require a separately credible intervention. No four-arm
hybrid experiment follows merely from observing that designs can be combined.

| Closest work | What it already measures | Proposed additional test |
| --- | --- | --- |
| [SlopCodeBench v2](https://arxiv.org/html/2603.24755v2) | Agents' inherited implementations evolve across checkpoints. | Supply credible alternative organizations of the same starting behavior before maintenance begins. |
| [CodeThread v1](https://arxiv.org/html/2606.21804v1) | Later issue resolution on human- versus agent-authored predecessor code. | Vary a declared architectural organization instead of prior authorship. |
| [Needle in the Repo v1](https://arxiv.org/html/2603.27745v1) | Functional correctness plus compliance with authored architectural boundaries. | Test whether either credible design actually improves later behavioral outcomes, without counting the preferred structure as success by definition. |

The new contrast would be architecture **by change family**, not a huge
language/model/architecture factorial. Example predictions, not adopted tasks:

- **Coordinated state rules:** explicit transitions may help keep scoring,
  lifecycle and screen state consistent through a pause/resume or mode change;
  message propagation and effect plumbing may instead introduce omissions.
- **Local interaction changes:** immediate-mode code may keep a new conditional
  control and its response together; implicit processing order or persistent
  widget identity may instead complicate it.

These predictions are deliberately two-sided. A result in which each design
helps different changes could be more informative than an overall winner.
Prediction quality and observed failure paths matter; merely naming a crossover
after seeing scores would not test the proposed interaction.

For an eventual adopted comparison, fix baseline behavior for the selected
contracts, model configuration, accessible information and response policy;
vary the architectural package and prespecified change families. Begin from
inherited working applications, retain their submitted states across episodes,
and measure successful new behavior plus preservation of earlier obligations.
Report resource use and all failure categories alongside success. Treat patch
spread, message additions and dependency changes as explanatory diagnostics,
not cross-style correctness requirements. Keep tool-call recovery chatter out
of the chosen information condition; do not silently repair syntax or discard
format/compile failures. The current no-tools policy is not changed by this note.
Retain architectural drift in the submitted code: the baseline assignment is
the comparison, not a post-hoc subset of runs that preserved our preferred style.
Any mandatory internal-style policy would need separate, explicit specification.

The counterfactual is the same declared change on the other credible baseline.
It is not a claim that every byte outside one architectural feature is equal.
Run randomization can address execution conditions, not authoring confounds;
one Breakout pair estimates this pair, not all MVU or immediate-mode systems.
Later independent applications would test transfer. This first candidate is
worth pursuing only if its baseline/physics differences can be controlled for
the selected scenarios without implementing the requested changes in an adapter
or rebuilding one style into the other. That feasibility remains unverified.

### Lineage is motivation, not inherited proof

MVU does have relevant peer-reviewed formal work: Fowler's ECOOP 2020
[Model-View-Update-Communicate](https://doi.org/10.4230/LIPIcs.ECOOP.2020.14)
formalizes MVU and integrates session typing. This establishes a formal research
connection, not a maintenance advantage or a proof that MMCC satisfies that
calculus. The [official Elm guide](https://guide.elm-lang.org/architecture/)
also describes the pattern as emerging from practice.

Dear ImGui's [maintainer explanation](https://github.com/ocornut/imgui/wiki/About-the-IMGUI-paradigm)
locates the distinction at the application/library API and warns against
equating immediate mode with no retained state. It is primary practitioner
design documentation, not a peer-reviewed causal evaluation. Its proposed
synchronization benefits can motivate falsifiable predictions, not count as
measured savings. No analogy automatically transfers either lineage's properties
to Nu; the source-level mapping must be explicit.

## Choose the study, not the largest possible experiment

| Design | What it can establish | What it does not establish |
| --- | --- | --- |
| Nu architectural/maintenance case study | Source-bound explanations, real change patterns, mechanisms and counterexamples in this project. | An average F# effect or a randomized architecture effect. |
| Matched maintenance trials using Nu and a credible existing alternative | Differences between these complete implementations under declared tasks and model policies. | Architecture separated from language, framework, documentation, maturity and familiarity. |
| A later controlled variant of one architectural decision | A narrower conditional effect, if the variants are credible and behaviorally matched. | General superiority of a paradigm or the whole Nu engine. |

Do not make all three prerequisites for one another. The recommendation is to
start with the source-grounded case and concrete task mapping; add a comparator
only if that mapping is credible. If the study actively assigns artificial
maintenance trials, call that component an experiment/evaluation, not merely an
observational case study. A toy extracted subsystem is a controlled model of a
case, not the original production system.

Runeson and Höst's [case-study guidelines](https://link.springer.com/article/10.1007/s10664-008-9102-8)
support intentional case selection, declared units of analysis and multiple
evidence sources. Baltes and Ralph's [sampling guidance](https://arxiv.org/html/2002.07764v6)
distinguishes purposive sampling from probability sampling and requires honest
limits on representativeness. Neither says every study needs a random sample
of professional architects. These methodological sources do not endorse any
particular Nu comparison; the recommendation is our application of them.

## Nu does not need a prior certificate of architectural quality

The user's Nu experience is useful domain knowledge and a reason the case is
accessible. It is also a disclosed investigator perspective, not an independent
assessment that Nu is better. Treat intentional design as the hypothesis source:
identify the design choice, its expected benefit, the changes that may benefit,
and the changes that may expose its costs. Ask whether the predictions survive
the evidence, including unfavorable cases.

Peer-reviewed/publication evidence is relevant but not a quality seal. There
are substantive published F# architectural systems beyond Nu:

- **Aardvark-related scene-graph architecture:** Steinlechner et al., GRAPP 2019,
  [10.5220/0007372800770088](https://doi.org/10.5220/0007372800770088).
  The [author preprint](https://aardvark-community.github.io/ag-for-scenegraphs/grapp-preprint.pdf)
  describes attribute-grammar semantics and incremental evaluation in a mixed
  F#/C# implementation. This is especially relevant graphics-system work, not a
  controlled longitudinal maintainability result or a purely F# system.
- **MBrace:** Dzik et al., PLOS 2013,
  [10.1145/2525528.2525531](https://doi.org/10.1145/2525528.2525531).
  The indexed [project-hosted paper](https://mbrace.io/mbrace-plos.pdf) describes
  F# cloud workflows and a distributed execution runtime. Only its indexed
  front matter/abstract/introduction and bibliographic identity were inspected;
  this note does not assess its maintainability or current suitability.

Aardvark is not automatically a comparable game engine, and a publication about
a system does not establish every architectural judgment about it. The exact
Scite phrase search for Nu returned no records; broader F# searches were noisy.
This is non-discovery in a bounded search, not proof that no Nu paper exists.

## First decide what is being maintained

Two different questions must not be accidentally merged:

- **Games/applications built with Nu:** does its application-facing architecture
  help maintain an inherited game? The comparable unit is another inherited
  application providing the same selected behavior on its own framework.
- **Nu's engine implementation:** does its internal organization help maintain
  facilities such as lifecycle, events, serialization or scene management?
  The unit is engine source/subsystems. Another engine's scripting language is
  not evidence about the language of its engine internals.

Studying existing engine code does not require asking fresh architects to build
two engines. Conversely, writing a tiny simulation inspired by Nu does not test
maintenance of Nu itself. The present ALF construction remains the latter kind
of feasibility material; it is not retrospectively renamed a Nu experiment.

### A potentially simpler contrast already exists inside Nu

The requested local analysis points to public Nu source at
`064f7ae92a8506689cd91aff5e6804a375d6ef3d`. Its
[README](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/ReadMe.md#L5)
offers both MMCC and ImSim application models, with official
[MMCC](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Nu/Nu.Template.Mmcc.Empty/MyGame.fs#L7)
and [ImSim](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Nu/Nu.Template.ImSim.Empty/MyGame.fs#L7)
templates. This suggests an economical *candidate* comparison: inherited
applications using two supported styles in the same language and engine.
It could reduce framework/runtime confounding without inventing a deliberately
weak architecture or recruiting a population of architects.

The root README also links MMCC and ImSim Breakout examples, which the user
confirms are intended to operate the same. At the pinned source, the ImSim
version uses engine physics while MMCC has model-level movement/intersection
logic. This does not contradict their common game intent, but selected contracts
need verification; identical trajectories/collision timing are not assumed.

The empty templates and Breakout examples are not an already validated
maintenance workload. Equivalent,
credible starting applications and changes would still need construction or
discovery and review. This contrast would test these Nu programming models,
not F# versus C#, engine-internal organization, or functional versus OO in
general. Whether it addresses the user's main claim remains a design choice.

Other concrete public mechanisms include snapshot/restoration support alongside
a mutable [World wrapper](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Nu/Nu/World/WorldTypes.fs#L1939)
and a publisher-neutral [event graph](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Nu/Nu/EventGraph/EventGraph.fs#L49).
These are design evidence, not enforced purity or observed maintenance savings.
The public [stub-world test](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Nu/Nu.Tests/WorldTests.fs#L15)
is a useful feasibility lead, not proof of a working fully headless environment.
No engine was built or run in this investigation.

## Issues and roadmaps: inputs to scenario selection, not matched tasks

[ALMA](https://www.cs.vu.nl/~hans/publications/y2004/alma.pdf) is a particularly
useful methodological precedent. It organizes architecture-level modifiability
analysis around a goal, relevant architectural description, change scenarios,
evaluation and interpretation. It distinguishes likely-change prediction from
deliberate stress/risk scenarios and architectural comparison. Its impact
estimates still depend on judgment; actual executable maintenance outcomes would
be additional evidence, not something ALMA automatically supplies.

Use public issues, accepted PRs and roadmaps to build a bounded scenario pool.
Do not compare raw issue counts, closure times or each engine's conveniently
available bugs as if they had equal difficulty and opportunity. A defect in Nu
may not exist in the comparator; a feature may already exist there. Such tasks
can remain native-case evidence but are not matched head-to-head tasks.

For a proposed common scenario, record:

1. Public source URL/date and the eligible baseline commit for each system.
2. The user-visible change and relevant existing behavior to preserve.
3. Why the change is meaningful and comparably applicable in both systems.
4. Observable acceptance criteria, allowed differences and regression cases.
5. What was adapted from the original issue; whether a public solution exists.
6. Inclusion/exclusion reasons decided before seeing candidate outcomes.

"Shared external contract" means the selected behavior at an observable
boundary, not identical APIs, source structure, internal events or whole-engine
feature parity. These are **illustrations**, not newly mined or selected tasks:

| Change family | Possible behavioral contract |
| --- | --- |
| Object lifecycle and subscriptions | Removing an object prevents later delivery to its expired subscriptions, while surviving objects still receive the specified events. |
| Scene hierarchy changes | Reparenting under the declared policy preserves the required world transform and child relationships, within specified numeric tolerances. |
| Save/load evolution | A new state field round-trips, declared old saves still load, and object references retain their specified relationships. |
| Pause/resume policy | Gameplay state stops advancing while designated UI behavior remains responsive, then resumes without duplicated actions. |

Native adapters may expose state/trace observations for those contracts; they
must not implement the feature for the candidate or force both systems into one
architecture. Graphics, nondeterminism and native dependencies require a real
feasibility check; a deterministic headless path is not assumed to exist.

Separate **typical maintenance** scenarios from **mechanism-discriminating**
stress scenarios. Purposefully selecting the latter is legitimate when labeled;
it does not estimate the average distribution of future game-engine work. Keep
changes predicted to favor either design, and allow the evidence to contradict
the initial predictions. Do not adapt selection after observing a language win.

Historical successor patches can inform the private research-side task audit,
but may not enter candidate context. Preserve as-of issue text, source revision,
public-solution/contamination risks and the distinction between mined and adapted
tasks. Existing future-gold, outcome and holdout restrictions remain in force.

## What independence and randomization actually mean here

Architects, maintainers, reviewers and model runs are different roles. Randomly
sampling architects would concern generalizing over who designs systems. It is
not necessary when the study fixes existing architectures as its objects.

For a future controlled comparison, one can use new isolated maintenance runs
under matched model/settings/information policies, with assignment or execution
order randomized/blocked as appropriate. That helps control trial conditions;
it does not randomize Nu's historical architecture or erase framework/author
confounding. Human participants would introduce expertise and learning effects,
consent/review requirements and additional design work; they are optional, not
an unstated requirement to start an agent-only study.

Multiple engine versions, subsystems or same-lineage predecessors are not
automatically independently authored projects. A second engine can add a
contrasting case without becoming a random sample of engines. Independent
reruns estimate variability on the selected cases; dependent episodes within a
trajectory measure evolution. Neither turns two engines into dozens of engines.
Report per-case/trajectory outcomes and uncertainty at the levels the design
supports; randomizing run order does not justify population-wide language claims.

Expert review means a scoped credibility check, not a panel that certifies the
winning paradigm. Your expertise can support Nu task authoring; a knowledgeable
comparator user/maintainer can check whether its baseline and task interpretation
are reasonable. Seek that review before strong comparative claims. If unavailable,
record the limitation and keep the study exploratory rather than invent approval.
No contact, recruitment or new review gate is executed by this note.

## Automation: execution and accounting are easier than ground truth

The [test-oracle survey](https://discovery.ucl.ac.uk/id/eprint/1471263/) explains
the distinction between running inputs and knowing the correct result. An
outside LLM can draft tests, propose invariants or classify failures, but being
a different model does not make its expected answers correct or independent
of a shared misunderstanding. The survey predates current LLMs; this application
to LLM-assisted evaluation is our methodological inference.

Use reviewed contracts and executable assertions/properties as primary behavior
checks. Validate the checks against trustworthy baseline behavior and deliberately
wrong variants; use independent cases, metamorphic relations or a small reference
model where appropriate. Do not make agreement with one gold implementation,
test count or a judge's architectural preference the sole definition of success.
Keep scorer/test machinery outside candidate write access and execute candidate
code only through an approved isolated path.

Scripts should retain every scheduled run, submission, failure, timeout and
resource debit. An LLM is unnecessary for bookkeeping. If subjective quality
judgments remain, predefine their rubric, reviewer type, disagreement handling
and secondary status. One-submission success is not effort-to-success; adding
repairs, human maintenance or a different context policy is a separate treatment.

## Smallest useful next artifact

Prepare a short **case-and-scenario feasibility sheet**, not another runner:
choose engine internals or inherited games; identify the exact Nu source scope;
map a few publicly motivated change families; and record whether a credible
comparator and behavioral checks exist. A few scenarios are a construction
exercise, not a claim of adequate inferential sample size. The next design can
then be selected on concrete evidence instead of requiring an idealized RCT.

This note supplies an initial source-grounded candidate and research-gap mapping;
scenario selection and behavioral feasibility remain open. No current workload
is replaced, and no live allowance is activated.
