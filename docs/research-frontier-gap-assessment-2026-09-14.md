# Research frontier, gap and value

**Date:** 2026-09-14 HKT. **Inspected repository:**
`5f919797f746ba5c87c3eea03a28e1c7109004fb`.
**Disposition:** research assessment and proposed direction, not adoption of
new treatments, workloads, models, budgets, an adapter or live execution.
The existing maintenance construction and human-review hold remain unchanged.

## Recommendation

There is a worthwhile research direction, but it is narrower than either
"functional programming is better for AI" or "existing benchmarks ignore
maintenance." The latter is no longer a defensible description of the frontier.
The strongest prospective contribution is:

> Which architectural representations make repeated, agent-performed changes
> more reliable, for which kinds of change and model capabilities, and how do
> language features support or obstruct those representations?

This is a recommendation inferred from the evidence below, not a discovered
universal gap or a result of this repository. F#/modern C# can be an informative
first setting on a shared runtime. The present one authored pair and eight
episodes are feasibility material, not an identified language or architecture
effect. A paper needs a clear contribution beyond adding two languages to an
already active maintainability-benchmark literature.

The [source ledger](research-frontier-gap-sources-2026-09-14.md) records search
boundaries, editions, reading extent, DOI decisions and access failures. This
is a bounded evidence map, not a systematic review, coverage saturation or proof
that no matching study exists. Several close papers appeared beyond the first
20 results. Earlier scoping notes remain history; their non-discovery does not
establish novelty.

## Where the frontier has moved

### From initial correctness to consequences of inherited code

Repeated maintenance, persistent code and separating repository state from
conversation history already have close prior art:

| Closest primary edition | What is already covered | Distinction from the proposed architecture question |
| --- | --- | --- |
| [SlopCodeBench v2](https://arxiv.org/html/2603.24755v2) | Generated first checkpoint, then inherited workspace across changes with fresh conversations; correctness, structural erosion and cost. | Architecture emerges from the agent; there is no matched architectural starting treatment. |
| [ChainSWE v2](https://arxiv.org/html/2607.02606v2), updated 1 September | Real-repository bug chains; gold predecessors versus agent-carried code, with and without transcript memory. | Isolates inheritance/context policies, not specified architectural alternatives. |
| [SWE-EVO v6](https://arxiv.org/html/2512.18470v6) | Release-level changes in mature repositories. | A release task is not an agent-maintained sequence of its constituent PRs. |
| [SWE-Milestone v4](https://arxiv.org/html/2603.13428v4) | Stateful development with dependency-linked milestones across five languages. | Historical architectures are not experimentally varied. |
| [CodeThread v1](https://arxiv.org/html/2606.21804v1) | Two-step matched human-versus-agent inherited implementations; subsequent issue-resolution outcomes. | Varies prior authorship, not a defined architectural property; residual behavioral differences and selection matter. |

CodeThread is particularly important new evidence. Its agent-inherited condition
usually performs worse than the human-inherited condition, but not uniformly.
Initial implementations are filtered through existing tests; that does not prove
complete semantic equivalence. The work already tests downstream consequences
of inherited implementation choices. We must therefore narrow any earlier gap
description: **the opportunity is to test specified architectural mechanisms,
not to discover that inherited code affects later work**.

[SWE-CI v4](https://arxiv.org/html/2603.03823v4) is another iterative neighbor,
but its architect's oracle/test-gap information differs materially from our
candidate-information boundary. It is not a reason to expose future gold.
The ledger records reading extent and the limits of these primary editions.

### From style metrics to targeted, executable architectural checks

[Needle in the Repo, v1](https://arxiv.org/html/2603.27745v1) supplies 21 small
C++ probes across nine dimensions, with starter repositories, functional and
structural oracles, and both micro and inherited multi-step cases. It includes
dependency boundaries, state ownership and side-effect isolation. Its agent
condition restricts access to read-only repository inspection without arbitrary
command execution. Thus supplied architecture, multi-step changes and a
constrained tool surface are not individually new contributions here.

Its structural checks instantiate authored design boundaries; they do not
establish that every preferred pattern lowers future maintenance effort. This
leaves room to test the *downstream consequences* of alternative architectures,
while allowing more than one legitimate implementation family.

### From human readability to model-facing editability

[Code for Machines, Not Just Humans](https://doi.org/10.1145/3793655.3793722)
studies refactoring in 5,000 small Python contest solutions. Its
[v1 methods/results](https://arxiv.org/html/2601.02200v1) associate higher
CodeHealth with fewer behavioral failures for the medium-sized models. The
Sonnet and Claude Code healthy/unhealthy comparisons are not statistically
significant. This is observational source-quality grouping, not random
assignment of equivalent architectures; the agent setup also differs from
single-file direct inference. It motivates model-dependent effects without
proving a parameter-size law, a crossover or a production-maintenance effect.

The August [test-generation extension](https://arxiv.org/html/2608.18645v1)
adds Java and C++, source-token measurements and test effectiveness with one
Qwen model. Associations vary by language and metric. Mutation analysis is
conditional on executable passing baseline tests; the Python adjusted
association is not significant. This strengthens the reason to investigate
structure, but not to assume shorter code or a quality score causes better
maintenance.

### From generic context length to useful semantic information

[Typed-hole contextualization](https://doi.org/10.1145/3689728) already studies
retrieval of relevant types and function headers, separately from correction
feedback, on Hazel/TypeScript MVU tasks. Its
[primary preprint](https://arxiv.org/html/2409.00921v1) also acknowledges small,
purpose-built examples, a simple retrieval baseline and limited TypeScript
implementation. "Types can make context more useful" is therefore a mechanism
with prior experimental evidence, not our novelty claim. The open question for
this project is how architectural organization affects *later changes* and
whether any information advantage explains their outcomes.

### From architectural vocabulary to demonstrated engineering decisions

[SAKE, v1](https://arxiv.org/html/2606.29520v1) assesses architectural knowledge
through multiple-choice questions, explicitly distinguishing that from sound
open-ended design. [ArchBench, v1](https://arxiv.org/html/2603.17833v1) aggregates
architectural tasks such as decisions, traceability and component generation;
its metric and implementation limitations are explicit.
[ToCS, v4](https://arxiv.org/html/2603.00601v4) examines architectural-map
construction under bounded exploration. Its paper reserves revision and
downstream exploitation for future evaluation. These are related capabilities,
not interchangeable measures of successful maintenance. Producing an articulate
design explanation does not establish that subsequent code changes are safe.

### Functional-language evaluation is also established

[FPEval / FPBench, v1](https://arxiv.org/html/2601.02060v1) evaluates algorithmic
generation in Haskell, OCaml and Scala, with Java as a comparator, and uses
language-specific static checks for style/maintainability. This is not repeated
maintenance of independently idiomatic inherited systems. Its reported
non-idiomatic output is a reason to measure familiarity and idiom preservation,
not proof that those idioms improve downstream outcomes. We do not adopt its
description of OCaml as purely functional or treat dissimilar lint tools as a
language-independent maintainability scale.

## What would constitute a defensible gap?

| Candidate claim | Assessment |
| --- | --- |
| LLM coding needs evaluation beyond initial test passing | Important motivation, already extensively represented by close work. |
| Maintain software across multiple episodes with fresh conversations | Useful control, not a novelty claim. |
| Compare later success on differently authored inherited code | Already directly studied by CodeThread; distinguish a new intervention from an authorship comparison. |
| Add F#/C# results to existing evaluation ideas | Potential transfer/resource contribution; one pair is a narrow case, not broad comparative evidence. |
| Estimate effects of specified, plausible architectural alternatives on later maintenance | Strongest candidate contribution, if equivalence, assignment, authoring and replication support identification. |
| Establish how that effect changes across task families or model configurations | Valuable boundary-condition contribution; requires planned contrasts, not post-hoc explanations. |
| Show that architectural compactness causes a context-window advantage | Separate, harder mechanism claim; the present complete-source condition cannot identify it. |

The missing link worth pursuing is a *tested architectural intervention with
future behavioral consequences*. This is not a claim that causal software
studies or downstream maintenance experiments do not exist. The contribution
must be stated relative to their specific interventions and outcomes, rather
than assembled from individually familiar ingredients and called first.

## Turn the language intuition into falsifiable propositions

"Coherence" should refer to observable design properties, not an elegance score
or the number of F# constructs present. Plausible mechanisms include:

- Important domain invariants represented explicitly rather than reconstructed
  from conventions across several locations.
- Clear state ownership and transitions that reduce the number of places a
  change can violate an invariant.
- Stable effect boundaries and extension points that avoid duplicating domain
  rules when adding a feature.
- Consistent representations that make related obligations easier to locate.

These are proposed mechanisms, not established F# advantages. C# records,
pattern matching, interfaces and disciplined mutation can realize overlapping
properties. Conversely, abstraction, indirection or unfamiliar APIs can make
a change harder. Task families matter: adding a new operation and adding a new
variant need not favor the same decomposition. A credible study must not select
only changes convenient for one architecture.

Three separable research questions would be:

1. **Architecture:** for equivalent starting behavior and matched change
   requests, how do specified architectural alternatives affect regression-free
   maintenance under a fixed response policy?
2. **Interaction:** does that architecture contrast vary with the independently
   characterized model/configuration or the kind of change?
3. **Language support:** do comparable design properties behave differently in
   idiomatic F# and modern C#, or is the observed result limited to the complete
   language/architecture/support package?

Do not automatically implement a large factorial study. Select one primary
contrast and outcome first. A within-language architecture comparison is the
cleanest small step toward an architecture claim; an idiomatic cross-language
pair instead estimates a package contrast. The latter remains legitimate if
named honestly. Generalizing to functional versus OO versus procedural requires
more than relabeling F# and C#.

## What the current construction can and cannot establish

The [standalone construction review](maintenance-sim-human-review-2026-09-12.md)
contains the current values and source links. It supplies one authored pair,
eight dependent episodes, complete eligible source, fresh conversations and a
one-submission/no-diagnostic-repair proposal. Safe wrong code persists; it is
not reset to gold after failure. No candidate maintenance adapter or execution
is active.

After appropriate review and separate execution approval, this can show whether
the tasks and evidence pipeline support a bounded package comparison. It cannot
by itself show:

- A language effect independent of architecture, authoring and language/idiom
  familiarity.
- Long-term industrial maintenance or a population of large projects.
- Architecture creation skill: the starting architecture is supplied.
- Effort required to reach success: one submission measures success at a fixed
  opportunity, not a repair-to-success curve.
- A physical context threshold or causal benefit of reduced input length:
  all reference inputs fit one proposed cap.

The F# reference input is larger at every current episode. Preserve that finding.
It does not refute every architecture mechanism, but it rules out using this
construction as evidence that F# already fits more useful code into context.
Do not tune the workload or references until that direction reverses.

Removing tool-call repair transcripts is a useful control for the user's
question. It also restricts the population of workflows represented. Syntax,
type and output-format failures remain legitimate measured outcomes; they must
not be silently repaired or excluded. Report them separately from behavioral
regressions, and label analyses conditional on compiling code as selected
subsets, not unbiased total effects.

## What makes a stronger study valuable

The most useful deliverable is a decision rule with demonstrated boundaries:
when does an architectural organization pay off for repeated agent maintenance,
and when does it not? That can inform supplied seed design, code review,
refactoring investment and model/workflow selection. It would not, on its own,
justify replacing a production language or claiming human maintenance savings.

A proportionate paper-facing design would need:

- Multiple independent workload/authoring units, with credible alternatives
  reviewed by domain and language experts. Repeated generations and eight
  dependent episodes are not independent projects.
- Shared external contracts and prespecified change families. If authors knew
  future changes, disclose that; independent future-task authorship can be a
  separately designed replication, not a retrospective claim of blinding.
- Assignment of architecture variants under matched model/policy conditions,
  with an analysis unit and repeated-episode dependence declared in advance.
  Define the smallest worthwhile effect and plan precision before outcomes;
  this note proposes no sample size or allocation.
- Direct behavioral outcomes: cumulative contract success, regressions in
  earlier obligations, recovery from retained failed state, and final task
  completion. Architectural diagnostics remain separate explanatory measures.
- Full denominators, failed attempts and resource accounting. Success must be
  reported alongside cost; a failed cheap change is not maintenance efficiency.
  Test adequacy needs independent behavioral cases and fault sensitivity, not
  only agreement with the authored reference.

Increasing failures late in a trajectory may reflect harder tasks, accumulated
incorrectness or larger software, not architectural decay alone. Any additional
checkpoint counterfactual must be designed and adopted separately; do not reset
the approved primary trajectory or expose future gold to its candidate.

For a later context study, vary actual information availability using an
outcome-independent policy and retain the same task/model. Measure supplied
bytes/tokens separately from estimated semantic relevance and total usage.
Do not equate a static dependency closure with necessary simultaneous memory,
or condition away code size if size is part of the mechanism being estimated.
No new retrieval engine is required merely to motivate this future question.

Null and contrary results can be valuable: an architectural property might help
only some change families, benefit weaker models more, add no benefit under
complete context, or fail because its idioms are unfamiliar. Publish those
possibilities symmetrically. An F# win is not a prerequisite for research value.

## Next decision

Use this assessment in the existing human review to select the claim: a bounded
idiomatic-package case study, or a separately designed architectural-intervention
study with adequate independent units. Do not begin a new runner or candidate
batch to settle an unresolved claim choice. The existing construction remains
useful preparation under either choice; no scientific amendment is adopted by
this literature investigation.
