# Idiomatic F# and C#: comparability, architecture and maintenance

Literature synthesis, 2026-09-13. Research interpretation and design recommendations,
not an adopted treatment or execution approval. The accompanying
[DOI and source ledger](idiomatic-language-comparison-sources-2026-09-13.md)
records editions, reading extent, access limitations and search provenance.

## Conclusion

Allowing F# and C# implementations to diverge architecturally need not make a
comparison unfair. It changes what the comparison can explain. The appropriate
primary question for an idiomatic maintenance study is whether particular
language-supported implementation strategies sustain the same external obligations
under the same maintenance conditions. It is not whether syntax alone causes the
difference. Architecture can be an intended mechanism of a language's usefulness;
forcing the same decomposition in both languages may remove that mechanism before
it can be observed.

The evidence supports investigating this possibility, but does not establish an
F# advantage. Classic modularity work explains how boundaries can localize changes;
human studies show that interface organization, type information, documentation and
experience can affect task performance. They also show costs and null results.
These are plausible mechanisms, not estimates of contemporary F#/C# model-assisted
maintenance outcomes.[^1][^2][^5][^6][^7][^8]

A direct historical comparison does include F# and C#: Nanz and Furia's Rosetta Code
study found a conciseness advantage in its small-program corpus. Its measurements
used a 2014 snapshot and older toolchains, not modern C# architectures, provider
tokens or longitudinal maintenance.[^10] Recent coding-agent work separately
demonstrates the importance of repository state and context composition, but in
Python workloads rather than a matched F#/C# architecture experiment.[^16][^17][^18]

The defensible working hypothesis is therefore conditional: some idiomatic designs
may keep more task-relevant relationships accessible within a limited input, leading
to better preservation of behavior over successive changes. Both links must be
tested. Less text alone is insufficient, and additional abstraction may instead
increase the knowledge needed to interpret that text.

## 1. Three different comparisons

The object of comparison must be named before deciding which differences to remove.
Behavioral equivalence is not structural equivalence, and neither guarantees equal
maintenance difficulty. The following distinctions are methodological recommendations
derived from the evidence, not results reported by any one paper.

| Comparison | What is deliberately comparable | What may differ | Defensible interpretation |
|---|---|---|---|
| A particular language mechanism | Behavior, architecture, dependencies and maintenance obligations, as far as the chosen intervention permits | A specified representation or construct | The effect of that implementation choice under those constraints; not the language as a whole |
| Idiomatic maintenance architecture | External behavior, workload, resource and support policies, acceptance criteria | Module boundaries, representations and composition strategies | The performance of the supplied language-and-architecture strategies |
| Language/ecosystem package | Product obligations and operational requirements | Architecture plus language-specific libraries/frameworks and their support requirements | The performance of the whole package, including its dependency and knowledge burden |

For example, a compact domain description that delegates behavior to a substantial
library may be a genuinely useful engineering solution. It does not show that the
language alone eliminated that complexity. The library contract, configuration,
documentation, version and relevant failure behavior become part of the package
that must be reproducible. Conversely, disallowing all distinctive abstractions can
turn an intended practical comparison into a constrained translation exercise.

There is consequently no universally correct amount of F# specificity. Include an
idiom because it fits a declared product and maintenance problem, not because it
makes the language look distinctive. Permit an equally serious C# solution, including
records and pattern-based designs where appropriate. Neither side should be forced
into a caricature: F# need not maximize functional constructs, and C# need not use
an unnecessarily ceremonial class hierarchy.

The phrase "consistent design" is a hypothesis about maintenance, not a scoring
rule. It can motivate questions about repeated conversions, dispersed rules,
incompatible representations and the number of contracts needed to understand a
change. An outcome metric should not award points simply for using the vocabulary
of one language. If an F# design uses fewer representations but makes their
semantics harder to discover, that tradeoff belongs in the result.

## 2. Architecture can reduce change scope, but abstraction has costs

Parnas contrasts two decompositions of the same KWIC indexing problem. His argument
is that modules organized around hidden design decisions can contain changes that
spread across modules organized around processing stages. This is an analysis of
design alternatives, not a randomized maintenance experiment; the paper also discusses
efficiency costs and interfaces that reveal too much.[^1] Its relevance is the
mechanism: identical behavior can be implemented with different obligations for a
future maintainer.

MacCormack, Rusnak and Baldwin provide empirical structural evidence using dependency
matrices for Linux and Mozilla, including Mozilla before and after redesign. Their
propagation-cost measure falls substantially after the redesign. It measures
potential reachability through extracted dependencies, however, not actual maintenance
time or successful repairs. Two products and static call relationships cannot
establish a universal modularity benefit, much less an F# effect.[^2]

Ko and colleagues observed developers maintaining an unfamiliar Java application.
Their analysis describes substantial work spent finding, following and recovering
relevant code relationships. The analyzed group comprised ten experienced participants
working on a small program in one IDE; this is evidence about human navigation,
not a measurement of model attention or large-project maintenance.[^3] Together,
these papers motivate examining what a change requires a maintainer to connect,
rather than counting source lines as if every line had the same significance.

There is also a countermechanism. Green and Petre's Cognitive Dimensions framework
describes tensions among abstraction, visibility, hidden dependencies and resistance
to change. Hiding details may simplify one activity while making another harder.
The framework is a vocabulary for task-sensitive analysis, not a validated numerical
architecture score or an established theory of LLM behavior.[^4]

API organization provides a concrete example. In Stylos and Myers's small Java study,
participants completed object-combination tasks faster when the class they naturally
started from exposed a reference to the needed helper. The authors also discuss a
tension between discoverability and encapsulation. The study did not measure
longitudinal repairs and used ten Java programmers.[^5] An interface can be
well encapsulated yet difficult to discover; an easily discoverable interface can
expose relationships that later make change harder.

The synthesis is a testable architectural hypothesis, not "more abstraction is
better." A useful boundary should reduce the knowledge required for the relevant
change without merely hiding indispensable knowledge elsewhere. Possible diagnostics
include the actual dependency paths needed for a change, repeated domain-rule edits,
and representation conversions. They require language-aware validation: file count,
call-graph reachability and unfamiliar-looking syntax are not interchangeable measures
of architectural quality.

## 3. Technical know-how is part of the comparison

Endrikat and colleagues crossed static typing with API documentation in a small Dart
experiment. Static typing had a significant main effect on total development time;
documentation did not meet the conventional .05 threshold for that outcome
(p=.075), although it did for coding time after reading time was removed. The
typing-by-documentation interaction was not significant. This does not establish
that documentation universally strengthens a type-system advantage. It highlights
why reading cost and coding cost should not be collapsed without explanation.[^6]

Hanenberg and colleagues studied Java and Groovy maintenance tasks. Static typing
helped with several unfamiliar-class tasks and type-error repairs, but the two
semantic-error tasks showed no significant time difference. Their navigation
analysis was exploratory rather than proof of a causal mediator.[^7] Since both
F# and C# are statically typed, this study cannot choose between them. Its useful
lesson is task specificity: evidence about one class of error does not establish
superiority on all maintenance work.

Uesbeck and colleagues offer contrary evidence about a particular advanced construct.
Their randomized comparison of C++ lambdas and iterators found no demonstrated
performance benefit for lambdas in the tested collection tasks, with student
difficulties and more compiler-error work in the lambda condition. Experience mattered;
professionals completed the tasks in both conditions. The authors explicitly restrict
generalization across languages and uses of lambdas.[^8] This is not evidence against
F# functions. It is evidence against assuming that a construct's expressive appeal
guarantees lower effort for its users.

For a maintenance study, three sources of know-how should therefore remain separate.
The first is expertise used to construct the initial architecture. The second is
support supplied to a maintainer: API documentation, examples, conventions and
architecture notes. The third is the maintainer's prior familiarity. Supplying an
expert-designed baseline answers a different question from asking a model to invent
that baseline. Training or documentation changes the maintenance condition; it is
not an invisible setup convenience.

For models, underlying training exposure to each language is not known or controlled
merely by using the same model. Standardized support can make a comparison more
interpretable, but cannot guarantee equal internal knowledge. Model identity,
version, support contents and access policy should accompany any claim. Human
experience effects motivate this concern; they do not quantify an LLM familiarity
effect.

As a proposed review practice, record why each nontrivial idiom or library is used,
what a maintainer must know to use it, and where that knowledge is provided. Give
both implementations comparable opportunities for qualified review. Symmetric
opportunity does not mean equal documentation length: relevant language-specific
support should be visible in the accounting. Any decision about whether those
materials consume an input allowance must be fixed before an experiment, not changed
after one language struggles.

Creation cost and maintenance cost also answer different questions. A supplied
expert architecture can support a conditional maintenance claim even if its creation
was expensive. A claim about lifetime engineering value would additionally need
creation, learning, dependency upkeep and maintenance costs over a stated horizon.
The present construction does not provide that lifetime accounting.

## 4. What language comparisons establish—and what they do not

Prechelt compared implementations of one problem in seven languages. Variation among
individual implementations and programmers was substantial. The language groups were
not drawn from an identical randomized participant population, and the study did not
include F# or C#.[^9] It remains relevant as a warning against treating one authored
program per language as a representative sample of the language's possibilities.

Nanz and Furia compared Rosetta Code solutions in eight languages, including F# and
C#. Their RQ1 uses nonblank, noncomment lines of compilable solutions, paired by task;
the main table aggregates by the shortest solution for each task. Table 5 reports
a normalized median ratio of 2.6 in F#'s favor for the C#/F# comparison. That number
is not a token multiplier or a maintenance effect. The 2014 snapshot, small tasks,
contributor selection and older Mono toolchains limit transfer to contemporary
architectures. It should not be reconstructed from the unpaired total line counts,
which cover different numbers of tasks.[^10]

Large observational studies do not automatically solve attribution. Ray and
colleagues related language categories to defect-fixing activity in GitHub projects,
with statistical controls and explicit validity threats. Berger and colleagues'
repetition and reanalysis challenged data handling, categorization and modeling,
leaving much smaller and fewer associations in their analysis.[^11][^12] The
original authors disputed the interpretation, and a further reply followed. Those
rebuttals are acknowledged here at abstract level, not independently adjudicated;
they are not additional independent datasets.[^13][^14]

The methodological conclusion is narrower than either "language determines quality"
or "language never matters." Observed differences can depend on task selection,
implementation authors, libraries, project history, labels and analysis choices.
The coding-language label alone is not a controlled intervention on all of these.
For the present problem, a well-described paired experiment can improve internal
interpretability, while independent implementations and projects would still be
needed for broader generalization.

One architecture per language bundles architecture choice with language choice. More
episodes reveal how those particular architectures evolve; more stochastic model
runs reveal variability on those architectures. Neither creates additional independent
architecture pairs. Consecutive episodes are dependent observations, not eight
independent replications of a language effect.

## 5. Useful context is not the same as short context

Lost in the Middle manipulated the placement of relevant information in long-context
question-answering and key-value tasks. Performance often depended on position even
when the material fit within the nominal window. These were not coding or
maintenance tasks, and the result is not a claim about every subsequent model.[^15]
The relevant caution is that physical capacity does not by itself establish usable
access to the information needed for a decision.

REPOEXEC supplies a coding-specific counterweight to "shorter is always better."
Its Python repository-level function-generation experiments compare different
dependency-context representations. Full context performs best overall, while a
smaller representation can outperform a medium one whose format misleads the model.
Its dependency-invocation metric concerns reuse, not architectural maintainability;
the evaluation does not carry a candidate codebase through years of change.[^16]

These results support investigating context composition, relevance and interpretability
alongside size. A shorter source file that omits a crucial contract is not necessarily
a better input. Nor is a larger file necessarily useful: irrelevant material, awkward
placement and unfamiliar abstractions may make essential relationships difficult to
use. This is an inference to test, not a validated universal context-density score.

For this research question, distinguish authored source bytes, complete supplied
input bytes, measured tokens when actually available, and behavioral outcomes. They
are different measurements. A proposed authored-byte cap neither discovers a provider
limit nor equalizes tokenizer behavior across languages. Relevant documentation and
interface definitions can consume the space apparently saved by a compact source
representation. Missing token measurements should remain missing, not estimated as
verified provider usage.

The proposed no-tools, fresh-conversation maintenance setting addresses a specific
confound: failed tool calls and their self-repair transcripts cannot fill later
inputs if they are not part of the candidate interaction. It does not eliminate
language syntax difficulty, incorrect edits, output-format failures, or inherited
bad code. Those can still be meaningful outcomes. Apparatus failures must remain
distinguishable, and diagnostic evidence can be retained for analysis without being
fed back into the candidate's context.

This controlled setting also narrows ecological validity. It studies maintenance
with supplied inputs, not an autonomous developer searching an arbitrary repository
with tools. A later tool-using comparison would be a separate treatment, not a
drop-in way to improve whichever language performs poorly.

## 6. Maintenance must preserve consequences over time

SWE-EVO evaluates release-sized changes in existing Python repositories rather than
isolated small functions. The reviewed v6 has 48 release transitions across seven
projects and supplies release-note-centered tasks with linked PR/issue information
in its default setting. An instance is a release transition, not a sequence that
inherits the evaluated model's previous candidate patch. Its failure classification
and agent performance do not establish an F#/C# effect.[^17]

ChainSWE is more directly relevant to inherited state. Its reviewed v2 uses 100
chains containing 304 issues across 54 Python repositories, distinguishes reference
predecessors from sequential candidate state, and separately tests conversation
carryover. It reports substantial sequential-state degradation and a small overall
benefit from retaining conversation history. Selection includes a model-based
solvability screen; chains are short and some tests or issue requirements are noisy.
It does not demonstrate that resetting conversation always helps, nor that the same
effect transfers to the present workload.[^18]

The proposed contribution should therefore not be "the first maintenance benchmark"
or "the first persistent-code/fresh-chat evaluation." A more specific contribution
could be a carefully controlled comparison of language-supported architectures under
bounded, useful maintenance context. That requires showing what remains correct after
changes, not just whether one current issue passes a narrow test.

In an inherited chain, an early failure can influence every later episode. Retaining
that consequence is appropriate when durability is the question; silently replacing
the predecessor with a successful reference would answer another question. Equally,
an absent downstream score is not proof that the new task's architecture was wrong.
The continuation policy, applicability of later checks and handling of missing
evidence must be specified beforehand. Passing a functional test alone also need not
demonstrate a requested architectural refactoring.

Different change families would be needed to test a general durability claim:
extension of domain variants, new operations, altered invariants, representation
changes and dependency evolution may favor different designs. This is a proposal
for a future sampling rationale, not permission to add episodes to the existing
pair. A sequence selected solely to reward one representation would establish only
that representation's fitness for the selected sequence.

## 7. Disposition for the existing construction

At source `72b6cf56509364ace74d16b5ef75c6be5ee30338`, the repository retains
one supplied F#/C# architecture pair and eight inherited maintenance episodes.
The [construction review packet](maintenance-sim-human-review-2026-09-12.md)
contains the exact artifacts, proposed policies, unactivated budgets and evidence.
F# reference input envelopes are larger at every episode in this pair. That finding
must remain visible: this construction does not demonstrate a compactness advantage,
and the workload should not be tuned to make it do so.

The result also does not settle architectural durability. Byte size, successful
maintenance and future change burden are different outcomes. A larger implementation
could perform better, worse or similarly; none of those model outcomes has been
established by trusted model-free construction. The eight episodes are a finite
simulation of evolution, not observed years of industrial maintenance or a population
of large projects.

The smallest useful next step remains human review of the supplied artifacts. This
synthesis recommends clarifying the intended claim and checking the pair's plausibility,
not implementing a new experiment framework. Review should determine whether each
architecture is a credible idiomatic solution to the same obligations; whether
support and dependencies are explicit; and whether the workload unfairly presupposes
one decomposition. Any substantive revision should have its rationale and source
identity retained before candidate outcomes exist. Human qualification and actual
review status should be recorded, not inferred from an AI review.

If independently idiomatic maintenance remains the chosen question, architectural
divergence can be accepted while the claim stays conditional on the supplied pair.
If distinct external libraries are introduced, their versions, contracts and support
requirements should be recorded and the claim broadened to a package comparison.
If a pure feature effect is wanted instead, a narrowly controlled follow-up would be
needed; adjusting for architecture after observing outcomes would not automatically
identify that effect.

No additional allocation, adapter, context policy, library, protocol version or
execution approval is adopted by this report. The proposed byte caps remain
unactivated, current execution flags remain disabled, and historical results remain
unchanged. The literature adds a rationale and limits for review; it does not replace
that review.

## 8. Evidence limits and a falsifiable hypothesis

The reviewed sources cover several different kinds of evidence: conceptual design
arguments, small human experiments, observational repository analyses, historical
language comparisons and recent Python-agent benchmarks. Their outcomes cannot be
pooled into a numerical estimate of F# versus modern C# maintenance. No reviewed
study directly establishes the complete language–architecture–usable-context–durability
chain proposed here. That is a limit of this bounded corpus, not proof that no such
study exists.

A useful hypothesis should permit adverse and mixed findings. F# could produce
shorter code without better maintenance, or better maintenance without shorter code.
Benefits could depend on supplied expertise, particular change families or a specific
model. C# could match or outperform it. Library-specific success could be valuable
without identifying a core-language benefit. A convincing study would preserve those
possibilities, report its conditional scope, and resist retrofitting the workload
to a preferred ranking.

## Sources

Reference numbers correspond to R01–R18 in the accompanying DOI ledger. Publication
DOIs identify articles; arXiv DOIs identify preprints and do not certify peer review.
Related versions are recorded in the ledger rather than counted as independent studies.

[^1]: David L. Parnas (1972). *On the Criteria To Be Used in Decomposing Systems into Modules*. Communications of the ACM 15(12), 1053–1058. [DOI 10.1145/361598.361623](https://doi.org/10.1145/361598.361623).
[^2]: Alan MacCormack, John Rusnak and Carliss Y. Baldwin (2006). *Exploring the Structure of Complex Software Designs: An Empirical Study of Open Source and Proprietary Code*. Management Science 52(7), 1015–1030. [DOI 10.1287/mnsc.1060.0552](https://doi.org/10.1287/mnsc.1060.0552). Author working-paper copy consulted.
[^3]: Andrew J. Ko, Brad A. Myers, Michael J. Coblenz and Htet Htet Aung (2006). *An Exploratory Study of How Developers Seek, Relate, and Collect Relevant Information during Software Maintenance Tasks*. IEEE Transactions on Software Engineering 32(12), 971–987. [DOI 10.1109/TSE.2006.116](https://doi.org/10.1109/TSE.2006.116).
[^4]: Thomas R. G. Green and Marian Petre (1996). *Usability Analysis of Visual Programming Environments: A “Cognitive Dimensions” Framework*. Journal of Visual Languages & Computing 7(2), 131–174. [DOI 10.1006/jvlc.1996.0009](https://doi.org/10.1006/jvlc.1996.0009).
[^5]: Jeffrey Stylos and Brad A. Myers (2008). *The Implications of Method Placement on API Learnability*. FSE 2008, 105–112. [DOI 10.1145/1453101.1453117](https://doi.org/10.1145/1453101.1453117).
[^6]: Stefan Endrikat, Stefan Hanenberg, Romain Robbes and Andreas Stefik (2014). *How Do API Documentation and Static Typing Affect API Usability?* ICSE 2014, 632–642. [DOI 10.1145/2568225.2568299](https://doi.org/10.1145/2568225.2568299).
[^7]: Stefan Hanenberg, Sebastian Kleinschmager, Romain Robbes, Éric Tanter and Andreas Stefik (2014; online 2013). *An Empirical Study on the Impact of Static Typing on Software Maintainability*. Empirical Software Engineering 19(5), 1335–1382. [DOI 10.1007/s10664-013-9289-1](https://doi.org/10.1007/s10664-013-9289-1).
[^8]: Phillip Merlin Uesbeck, Andreas Stefik, Stefan Hanenberg, Jan Pedersen and Patrick Daleiden (2016). *An Empirical Study on the Impact of C++ Lambdas and Programmer Experience*. ICSE 2016, 760–771. [DOI 10.1145/2884781.2884849](https://doi.org/10.1145/2884781.2884849).
[^9]: Lutz Prechelt (2000). *An Empirical Comparison of Seven Programming Languages*. Computer 33(10), 23–29. [DOI 10.1109/2.876288](https://doi.org/10.1109/2.876288). Author submission dated 2000-03-14 consulted.
[^10]: Sebastian Nanz and Carlo A. Furia (2015). *A Comparative Study of Programming Languages in Rosetta Code*. ICSE 2015, 778–788. [DOI 10.1109/ICSE.2015.90](https://doi.org/10.1109/ICSE.2015.90). Main article and selected measurement definitions in [arXiv v4](https://arxiv.org/pdf/1409.0252v4) consulted.
[^11]: Baishakhi Ray, Daryl Posnett, Vladimir Filkov and Premkumar Devanbu (2014). *A Large Scale Study of Programming Languages and Code Quality in GitHub*. FSE 2014, 155–165. [DOI 10.1145/2635868.2635922](https://doi.org/10.1145/2635868.2635922).
[^12]: Emery D. Berger, Celeste Hollenbeck, Petr Maj, Olga Vitek and Jan Vitek (2019). *On the Impact of Programming Languages on Code Quality*. ACM Transactions on Programming Languages and Systems 41(4), article 21, 1–24. [DOI 10.1145/3340571](https://doi.org/10.1145/3340571).
[^13]: Baishakhi Ray, Prem Devanbu and Vladimir Filkov (2019). *Rebuttal to Berger et al., TOPLAS 2019*. arXiv:1911.07393v1, 2019-11-18. [DOI 10.48550/arXiv.1911.07393](https://doi.org/10.48550/arXiv.1911.07393). Abstract-level acknowledgement only.
[^14]: Emery D. Berger, Petr Maj, Olga Vitek and Jan Vitek (2019). *FSE/CACM Rebuttal²: Correcting A Large-Scale Study of Programming Languages and Code Quality in GitHub*. arXiv:1911.11894v1, 2019-11-27. [DOI 10.48550/arXiv.1911.11894](https://doi.org/10.48550/arXiv.1911.11894). Abstract-level acknowledgement only.
[^15]: Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni and Percy Liang (2024). *Lost in the Middle: How Language Models Use Long Contexts*. Transactions of the Association for Computational Linguistics 12, 157–173. [DOI 10.1162/tacl_a_00638](https://doi.org/10.1162/tacl_a_00638).
[^16]: Nam Le Hai, Dung Manh Nguyen and Nghi D. Q. Bui (2025). *On the Impacts of Contexts on Repository-Level Code Generation*. Findings of NAACL 2025, 1496–1524. [DOI 10.18653/v1/2025.findings-naacl.82](https://doi.org/10.18653/v1/2025.findings-naacl.82).
[^17]: Tue Le, Minh Vu Thai Pham, Dung Nguyen Manh, Huy Nhat Phan and Nghi D. Q. Bui (2025–2026). *SWE-EVO: Benchmarking Coding Agents in Long-Horizon Software Evolution Scenarios*. arXiv:2512.18470v6, 2026-05-22. [DOI 10.48550/arXiv.2512.18470](https://doi.org/10.48550/arXiv.2512.18470). [Version consulted](https://arxiv.org/html/2512.18470v6).
[^18]: Qirui Jin et al. (2026). *ChainSWE: Benchmarking Coding Agents on Multi-Bug Software Maintenance*. arXiv:2607.02606v2, 2026-09-01. [DOI 10.48550/arXiv.2607.02606](https://doi.org/10.48550/arXiv.2607.02606). [Version consulted](https://arxiv.org/html/2607.02606v2).
