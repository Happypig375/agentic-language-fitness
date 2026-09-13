# Verifiability of idiomatic-language maintenance comparisons

The literature supports studying the consequences of architectural decisions
across successive changes. It does not establish that idiomatic F# produces
better LLM maintenance outcomes than modern C#, or that shorter source reliably
produces better decisions. Those remain testable hypotheses, not premises that
the benchmark should be constructed to confirm.

The present construction is suitable groundwork for an auditable **bounded
maintenance case study**. It is not yet a running candidate experiment and does
not identify an architecture-mediated context advantage. The central distinction
is between verifying what happened to retained software, estimating a repeatable
difference between two supplied implementations, and explaining why that
difference occurred. Each requires additional evidence beyond the preceding
one. The existing human-review and execution holds remain unchanged.[^1]

## Literature support and limits

### Architecture and subsequent maintenance

There is empirical motivation for connecting architecture to later changes.
Le and colleagues studied 466 versions of ten Apache Java systems, using
recovered architectural smells to predict issue- and change-proneness. Their
outcomes are issue/commit-derived labels, not observed maintainer time. The
within-system evaluation uses random ten-fold cross-validation; the
cross-system evaluation holds out a system. Neither should be described as a
prospective intervention proving that removing a smell reduces maintenance
cost. This is useful predictive evidence, with a narrower population and
interpretation than a language-independent causal law.[^2]

There is also important counterevidence to treating structural preferences as
maintenance outcomes. Sjøberg and colleagues report six professional developers
working on three maintenance tasks across four functionally equivalent Java
systems. None of twelve investigated smells was significantly associated with
increased effort after adjustment for file size and changes. This result is
available here through the publisher's abstract, not a full-methods replication.
It limits an automatic smell-to-effort inference; it does not show that
architecture never matters or that an adjusted association is a total causal
effect.[^3]

These results are not a simple vote for or against architecture. They concern
different structural measures, populations and endpoints. A language comparison
should therefore observe the success and consequences of actual changes, while
reporting structural diagnostics separately.

### Closest iterative-coding precedents

SlopCodeBench is especially close prior art. In v2, agents start from scratch,
then extend their own code under external specifications without prior
conversation or hidden-test feedback. Its Python evaluation reports degradation
using complexity-concentration and rule/clone-based verbosity measures, not
observed maintenance effort. It does not test F# against C#.[^4]

Persistent code, fresh conversations and externally checked iterative design
therefore cannot individually be claimed as new here. A supplied idiomatic
cross-language seed pair with tool-free maintenance differs from that design;
priority for this combination is not established.

The previously examined ChainSWE separates persistent repository state from
conversation memory in sequential bug repair. SWE-EVO studies repository
evolution from release-level requirements. These remain relevant neighbors,
not interchangeable datasets or independent confirmations of an F# effect.
Their pinned editions are v2 and v6 respectively.[^5][^6]

### Context usefulness rather than code length

ReCUBE v1 reconstructs masked Python files using repository context and evaluates
both internal and cross-file behavior. Its larger-context extension keeps the
same target files while expanding surrounding repository information. Results
vary by model and access method: additional context helps some settings, while
others suffer context-length errors. Its caller-coverage analysis is stratified
and observational, not a general causal estimate of relevant information.
Gold-derived tests include implementation-specific checks, so its oracle cannot
simply be copied into an architecture-free F#/C# comparison. The benchmark's
Python-only, predominantly LLM-related repositories further limit transfer.[^7]

The implication is conditional: representation size, relevant information,
ability to use that information, and output feasibility are distinct variables.
A smaller program might retain more useful evidence under a fixed allowance;
it might also omit helpful explicit structure. A larger program might improve
decision quality while consuming more space. Both possibilities must remain
reportable.

### Evidence strength

| Proposition | Assessment from the examined evidence |
|---|---|
| Successive modifications and inherited design decisions deserve evaluation | Well-motivated; contemporary benchmarks already address this problem. |
| Architecture-related properties can predict later maintenance problems | Supported in particular empirical settings; not a universal causal relationship or interchangeable with effort. |
| Context composition can affect repository-level coding performance | Directly investigated, with model-, task- and access-dependent results. |
| F#'s coherent idioms improve maintenance through better use of context | Plausible proposed mechanism; not established by the examined studies. |
| The present pair represents large-project, long-term maintenance generally | Unsupported: one authored pair and eight dependent episodes are a feasibility case. |

These are qualitative assessments of relevance and identification, not
meta-analytic confidence grades or a count of favorable papers. No direct
modern F#/C# LLM-maintenance effect was established in the inspected evidence;
that statement is not a claim that no such paper exists.

## Current construction and observable contract

The inspected repository state is
`cea02738a4c40a1a903d1f7293964c9627569c31`. Its construction evidence has its own
earlier source identities, retained without relabeling. The
[standalone construction packet](maintenance-sim-human-review-2026-09-12.md)
contains exact settings and artifacts. The following assessment concerns that
construction, not a proposed replacement experiment.[^1]

| Question | Available evidence or setting | Identification limit |
|---|---|---|
| Can the trusted fixtures satisfy the external obligations? | 80 cases, 18 trusted targets and 608 applicable evaluations; 27 focused tests. | Verifies trusted construction, not any candidate's maintenance ability. |
| Does the checker detect known faults and distinguish inherited failure states? | Eight semantic faults, 12 applicability scenarios and 16 downstream witnesses. | Four fault families exercised in both languages, not eight independent classes of real maintenance defects. |
| What actually fits in the authored envelope? | Sixteen canonical envelopes; source/component bytes, hashes and an offline token proxy. | Exact serialization measurements, not measured provider context capacity or useful-information content. |
| Is context availability experimentally varied? | One complete-source condition. Proposed input cap 86,016 bytes; largest reference input 66,848. | Every reference input fits. A cap label alone creates no different information exposure. |
| Is architecture quality measured? | Proposed invariant ownership, effect composition, boundary, findability and convention diagnostics. | Exploratory prose, not an implemented or validated composite architecture score. |
| Can live maintenance outcomes be produced now? | No maintenance-specific candidate adapter or isolated evaluator; allocation remains zero. | Trusted fixture execution is not candidate execution readiness. |

The F# reference input envelope is larger at every episode. At episode eight,
the C#/F# inputs are 58,350/66,848 bytes. The corresponding reference
changed-file replacement objects are 34,595/43,928 bytes, before real
architecture notes and model framing. The proposed output allowance is 61,440
bytes, also inactive. Those measurements provide a verifiable negative finding
for a compactness advantage **in this authored pair and serialization**. They
do not establish that either language is generally larger, or predict which
implementation a model will maintain more successfully.[^1]

Candidate-written source and explicit file-based notes could grow beyond these
reference measurements. That would be a policy outcome to retain, not evidence
that the current references already constitute a context-pressure experiment.
The `architecture_notes` explanation is archived, not automatically supplied as
memory; only approved durable files enter the inherited repository.

## Verifiable outcomes

### A bounded maintenance result

A defensible initial question is:

> For these supplied idiomatic implementations and this prespecified change
> sequence, how reliably does a fixed model preserve and extend the public
> behavioral contract under a fixed information and submission policy?

After explicit design adoption and an isolated adapter, this can yield an
independently recomputable result. A reader could reconstruct every predecessor,
input and submission, run the pinned evaluator, and verify each applicable
obligation and trajectory summary. Stochastic model responses need not reproduce
byte-for-byte for the retained scoring to be reproducible. A repeated live
experiment is a separate replication, with its own usage and model-version
uncertainty.

The existing proposed outcomes already distinguish cumulative-obligation
correctness, first regression, recovery, strict-chain completion and unknown
evaluation. Keep those distinctions. Before allocation, select one primary
summary and its denominator; do not select it after seeing a language advantage.
The scheduled trajectory should remain visible even when later states cannot
be evaluated. Candidate noncompilation, malformed output, input/output policy
failure and evaluator unavailability must have separate statuses. Unknown
behavior is not silently successful, and an apparatus outage is not silently a
language defect.[^1]

An informative outcome need not favor F#. Better behavior with larger F# inputs
would support a maintenance advantage for this package, but not a
more-code-fits explanation. Smaller inputs with equal tested behavior would
support a representation-efficiency result within the policy, not better
decisions. No discernible difference is also a valid result if uncertainty is
reported; it is not evidence of equivalence without a prespecified equivalence
margin and adequate independent replication.

### Oracle adequacy

The behavioral oracle is more directly auditable than a stylistic score, but a
finite passing test set is not proof of general correctness. Just and colleagues
found a relationship between mutation detection and real-fault detection using
357 faults in five Java programs, while also identifying faults not coupled to
the generated mutants. That evidence supports testing an oracle's sensitivity;
it does not validate this project's eight hand-authored faults as a
representative sample of future defects.[^8]

Before treating the case study as research evidence, human review should connect
each important public obligation to discriminating checks and examine whether
the expected outputs encode behavior rather than a preferred implementation.
Targeted additional independent cases or state-machine properties may be useful
where a specific gap is found. They would require a traceable construction
change before candidate outcomes, not holdout tuning after inspecting failures.
Do not turn this into an unbounded mutation-testing project or require structural
similarity to gold.

## Architecture and context attribution

### The package-versus-mechanism distinction

The intended explanation is a chain: language idioms influence representation
and architectural conventions; these influence usable evidence and the burden
of coordinating a change; better decisions then preserve more obligations.
The current construction observes the endpoints and some byte-level properties,
but does not separately manipulate or validate every link.

One F# implementation and one C# implementation bundle language, initial
architecture, authorship, naming, documentation, model familiarity and selected
idioms. That is acceptable if the treatment is explicitly the two supplied
idiomatic packages. It cannot isolate a pure language effect or prove that
architecture mediates the difference. More runs of the same pair estimate
model-run variation within that pair; they do not create additional independent
architecture pairs. The eight episodes and their many checks likewise are not
eight independent projects or hundreds of language samples.

Furia and Torkar's omitted-variable analysis illustrates why more observations
do not repair an inadequately identified effect, including a programming-language
example. Its causal diagrams and sensitivity methods require substantive
assumptions; fitting an extra regression to this tiny construction cannot
recover missing counterfactuals.[^9]

Keeping modern C# records and patterns idiomatic is important. Requiring a
line-for-line translation would remove part of the architectural choice under
study. Conversely, adding an F# framework or expert-authored abstraction changes
the package and its support burden. Neither should happen informally during
execution. Seed-only review by competent practitioners can assess plausible
idioms and over-specialization, but cannot eliminate the author's knowledge of
the full episode sequence.

### Context availability

The no-tools, fresh-conversation policy removes tool-call correction transcripts
as a source of context consumption. It therefore addresses the specified
tool-repair confound. It does not remove language familiarity, JSON/full-file
output failures, differences in explanatory guidance, or accumulated defects
in inherited code. Those remain part of this policy's outcome and limit
generalization to tool-using coding agents.

For a causal context claim, there must be a real contrast in the information
available to the same fixed model, not just two sufficiently large ceilings.
A prospective comparison could supply complete context versus a prespecified
bounded context from the same eligible predecessor and public history. It would
need to record exactly which source and obligations are visible, use a common
selection rule, and keep output allowance and interaction policy fixed.
Selection cannot use future gold, future requirements, outcomes, or knowledge
of which language wins. This is a possible new treatment requiring review,
not a change authorized by the present literature assessment.

Even then, an architecture package advantage and a context-policy advantage are
not automatically the same mechanism. A fixed byte allowance defines an
authored-information policy, not equal provider tokens or equal effective model
capacity. Output feasibility must be reported separately: requiring full-file
replacement can exhaust a generation allowance despite sufficient input
information. Secretly increasing one language's output allowance would not fix
that attribution problem.

### Architecture diagnostics

Sjøberg and Bergersen recommend connecting constructs to explicit
operationalizations, checking representation bias and narrowing a claim when
available indicators do not adequately represent it. A maintainability label
does not make an arbitrary metric a validated measure of maintainability.[^10]

The most useful exploratory diagnostics here would be tied to particular
changes: where an invariant is enforced, whether a new behavior requires
coordinated edits to multiple semantic responsibilities, whether effects retain
one explicit owner, and whether an earlier obligation breaks after an extension.
Reviewers should cite actual predecessor/submission locations and observable
consequences. Candidate explanations are evidence to inspect, not ground truth.

Fewer edited files can reward a monolith; lower complexity can move work into
library calls; shorter code can hide conventions. Do not combine these into a
language-ranking score without validation. Cross-language responsibility units
and idiom judgments need expert review, with disagreements retained. Where
possible, reviewers should not know later scores while assessing an earlier
architecture, although language itself cannot realistically be blinded.

Later failures alone do not prove architectural erosion: later episodes can be
harder, the repository can be larger, and an earlier functional error can
propagate. The paired schedule holds the requested change sequence common
between languages, but it does not identify which of these mechanisms caused a
trajectory's decline. A mechanism study needs an explicitly justified
counterfactual, not a post hoc narrative about ugly code.

## Recommended disposition

Retain the current pair as feasibility material and preserve its unfavorable F#
size finding. Do not redesign it to produce an expected winner. The next review
should select the claim before selecting an adapter or a live allocation.

For the smallest defensible continuation, review a bounded package-comparison
case study: confirm the public contract and oracle, independently assess both
seeds' idioms, settle the primary trajectory summary and failure denominator,
and then consider a model-free isolated adapter. This can produce useful
auditable behavior and resource observations without claiming to explain their
cause. No budget is selected here.

If the intended paper requires the stronger claim about architectural coherence
and usable context, decide prospectively on a genuine context contrast and
independent architecture/workload replication. Do not treat repeated calls on
this pair as that replication. Evidence from larger inherited systems is needed
before extrapolating to large-project maintenance; eight episodes are not
calendar years of maintenance.

The main contribution worth investigating is therefore not “F# is cleaner” or
“maintenance benchmarks do not exist.” It is whether explicitly characterized,
idiomatic language architectures differ in externally verified maintenance
outcomes under controlled information policies, and whether those differences
survive serious attempts to distinguish representation, expertise, output
burden and task selection. The current construction advances that investigation
but does not yet answer it.

## Sources

[^1]: *agentic-language-fitness*, [standalone maintenance review packet](../docs/maintenance-sim-human-review-2026-09-12.md), [construction configuration](../benchmarks/maintenance-sim/construction.json), [measurement implementation](../src/alf/maintenance.py), and [retained evidence index](../reports/maintenance-sim-construction-2026-09-12/evidence/index.json), inspected at `cea02738a4c40a1a903d1f7293964c9627569c31`. Exact source locations and historical identities are recorded in the [companion evidence ledger](maintenance-research-verifiability-sources-2026-09-13.md).

[^2]: Duc Minh Le, Suhrid Karthik, Marcelo Schmitt Laser, and Nenad Medvidovic. “Architectural Decay as Predictor of Issue- and Change-Proneness.” *ICSA*, 92–103, 2021. DOI [10.1109/ICSA51549.2021.00017](https://doi.org/10.1109/ICSA51549.2021.00017). [Author preprint, v1](https://arxiv.org/pdf/2102.09835v1), §§III–V.

[^3]: Dag I. K. Sjøberg, Aiko Yamashita, Bente C. D. Anda, Audris Mockus, and Tore Dybå. “Quantifying the Effect of Code Smells on Maintenance Effort.” *IEEE TSE* 39(8), 1144–1156, 2013; online 2012. DOI [10.1109/TSE.2012.89](https://doi.org/10.1109/TSE.2012.89). [Publisher abstract](https://ieeexplore.ieee.org/document/6392174/); abstract-only use.

[^4]: Gabriel Orlanski et al. “SlopCodeBench: Benchmarking How Coding Agents Degrade Over Long-Horizon Iterative Tasks.” Preprint, **v2, 7 May 2026**. DOI [10.48550/arXiv.2603.24755](https://doi.org/10.48550/arXiv.2603.24755). [Pinned primary text](https://arxiv.org/html/2603.24755v2), §§2–3. The earlier indexed edition is not used for current counts.

[^5]: Qirui Jin et al. “ChainSWE: Benchmarking Coding Agents on Multi-Bug Software Maintenance.” Preprint, **v2, 1 September 2026**. DOI [10.48550/arXiv.2607.02606](https://doi.org/10.48550/arXiv.2607.02606). [Pinned primary edition](https://arxiv.org/abs/2607.02606v2). Methods/limits retained in the [earlier ledger](idiomatic-language-comparison-sources-2026-09-13.md), R18.

[^6]: Minh V. T. Thai et al. “SWE-EVO: Benchmarking Coding Agents in Long-Horizon Software Evolution Scenarios.” Preprint, **v6, 22 May 2026**. DOI [10.48550/arXiv.2512.18470](https://doi.org/10.48550/arXiv.2512.18470). [Pinned primary edition](https://arxiv.org/abs/2512.18470v6). Methods/limits retained in the [earlier source ledger](idiomatic-language-comparison-sources-2026-09-13.md).

[^7]: Jiseung Hong, Benjamin G. Ascoli, and Jinho D. Choi. “ReCUBE: Evaluating Repository-Level Context Utilization in Code Generation.” Preprint, **v1, 26 March 2026**. DOI [10.48550/arXiv.2603.25770](https://doi.org/10.48550/arXiv.2603.25770). [Pinned primary text](https://arxiv.org/html/2603.25770v1), §§3–5, Table 4, and Limitations.

[^8]: René Just, Darioush Jalali, Laura Inozemtseva, Michael D. Ernst, Reid Holmes, and Gordon Fraser. “Are Mutants a Valid Substitute for Real Faults in Software Testing?” *FSE*, 654–665, 2014. DOI [10.1145/2635868.2635929](https://doi.org/10.1145/2635868.2635929). [Author-hosted paper](https://www.cs.ubc.ca/~rtholmes/papers/fse_2014_just.pdf), §§1, 3.2–3.4.

[^9]: Carlo A. Furia and Richard Torkar. “Mitigating omitted variable bias in empirical software engineering.” *Empirical Software Engineering* 31, article 123, **21 April 2026**. DOI [10.1007/s10664-026-10851-1](https://doi.org/10.1007/s10664-026-10851-1). [Publisher text](https://link.springer.com/article/10.1007/s10664-026-10851-1), §§1, 3–4.

[^10]: Dag I. K. Sjøberg and Gunnar R. Bergersen. “Construct Validity in Software Engineering.” *IEEE TSE* 49(3), 1374–1396, 2023; online 2022. DOI [10.1109/TSE.2022.3176725](https://doi.org/10.1109/TSE.2022.3176725). [Author-uploaded accepted manuscript](https://www.researchgate.net/publication/360817259_Construct_Validity_in_Software_Engineering), §5.1 and Table 5; manuscript pp. 14–16.
