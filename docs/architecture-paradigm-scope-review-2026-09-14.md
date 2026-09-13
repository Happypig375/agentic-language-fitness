# Research scope: languages, architectures and paradigm labels

**Date:** 2026-09-14 HKT. Research advice, not an adopted treatment or execution approval.

**Inspected source:** `2f4cb784b17d7e94db1030750f1025259de5bf52`.
The user asked whether F#/C# restricts research value, suggested functional,
object-oriented and possibly procedural architectures, and requested examination
of the vsynchronicity blog and a connected-Scite DOI record. This extends the
[architecture-first assessment](architecture-maintenance-slopcode-assessment-2026-09-14.md).
The [standalone construction review](maintenance-sim-human-review-2026-09-12.md)
still owns actual settings and open approvals.

## Recommendation

Restricting the initial study to F#/C# limits **generalization**, not necessarily
research value. A credible, explicitly bounded case study can test a useful
mechanism. Adding language names does not repair an unclear mechanism or a
confounded comparison. The present same-SDK, dependency-free .NET construction
reduces some platform variation; it does not equate compilers, representations,
authored designs, model familiarity or language support.

Broaden the theory to:

> Which architectural choices support reliable maintenance under evolving
> requirements, and how does a language's support for those choices affect
> their usefulness to an LLM maintainer?

Keep three questions separate:

| Question | Contrast needed | What the current pair cannot separate |
| --- | --- | --- |
| Architecture | Plausible architecture alternatives within a language | An F# design versus a different C# design changes both factors. |
| Language support | A comparable architectural policy across languages | Differences can still include syntax, guarantees, guidance and model familiarity. |
| Language–architecture fit | Whether the architecture contrast differs across languages | One architecture package per language cannot estimate that interaction. |

The third question preserves the user's concern about F#'s coherent design.
Replacing it with a generic functional-versus-OO contest could lose that concern:
a feature being expressible in two languages does not establish that it has
equal conventions, guarantees, composition costs or learning demands. Conversely,
calling C# features “bolted on” is a hypothesis about those consequences, not a
measurement of them.

This is a proposed scope of inference, not a claim that such an interaction has
already been demonstrated. “Better fit” must ultimately predict witnessed
maintenance outcomes, not merely reviewer preference for syntax.

## What the blog contributes—and what it does not

The three selected essays were read as opinion and experience reports, not as
controlled evidence. Dates below are displayed publication dates; some pages
also show later updates. Authorship is the site's `vsynchronicity` byline, not
an independently verified identity or an assertion about writing tools.

- **B1:** [Jon Blow's Seeming Dismissal of Functional Game Programming](https://vsynchronicity.wordpress.com/2025/03/22/jon-blows-seeming-dismissal-of-functional-game-programming/),
  22 March 2025, displayed update 11 August 2026. It motivates immutable-state
  designs through undo/redo, hot reload and state provenance, while acknowledging
  performance, garbage-collection and dependency constraints. Addendum 3 argues
  for the coherence of the ML language family, beyond isolated functional
  features. This usefully distinguishes language design from architecture.
  The author's interpretation of a Blow clip is not a verified statement of
  Blow's complete position. Nu's reported implementation/performance was not
  independently tested here.
- **B2:** [10 Ways Object-Oriented Code is More Complex than Functional Code](https://vsynchronicity.wordpress.com/2023/05/22/10-ways-object-oriented-code-is-more-complex-than-functional-code/),
  22 May 2023. Its list supplies candidate mechanisms: mutation, coupling,
  control flow, identity, lifecycle and testing dependencies. Its
  order-of-magnitude complexity assertion has no presented measurement method,
  dataset or controlled comparison. Do not repeat it as an empirical 10× result.
- **B3:** [MVU Rescues Procedural Programming from the Belly of the Event-Based Whale](https://vsynchronicity.wordpress.com/2023/08/15/mvu-rescues-procedural-programming/),
  15 August 2023, displayed update 14 January 2025. It frames MVU as recovering
  direct procedural reasoning within interactive software and discusses
  model-diffing costs. Its own framing illustrates that functional and procedural
  organization can coexist; it does not establish a universal MVU advantage.

The [homepage's](https://vsynchronicity.wordpress.com/) *Nu Game Engine on the
Holodeck* explicitly stages an AI-generated imagined discussion. Its simulated
remarks are not quotations or endorsements by the named computing researchers.
It is used only to establish this source boundary, not as expert consensus.

My inference from the essays and the existing workload is that state ownership,
transition visibility and effect boundaries are useful hypotheses. Logical
entity identity, cancellation and stale-event obligations still exist in a
data-oriented implementation: changing representation can reduce aliasing or
relocate obligations, not make the domain's lifecycle disappear. The existing
episodes 02, 03 and 06 already supply related obligations without needing to
copy the blog's engine or add its libraries.

## Why paradigm labels are insufficient treatments

Language, programming paradigm, architectural organization and architectural
quality are different constructs. F# itself supports objects and interfaces
([official language overview](https://learn.microsoft.com/en-us/dotnet/fsharp/what-is-fsharp)).
Cook's conceptual analysis uses immutable objects and does not make inheritance
a requirement of object orientation. In that paper, **ADT means abstract data
type**, not algebraic data type. Its discussion of complementary extension
axes is not an assertion that all F# unions are the opposite of all C# classes
([D3, §§1–3 and practical duality discussion](https://www.cs.utexas.edu/~wcook/Drafts/2009/essay.pdf)).

For a future intervention, define policies such as:

| Dimension | Concrete distinction to document | Avoid assuming |
| --- | --- | --- |
| State and aliasing | Who owns mutable state; which references may observe changes; deep versus shallow restrictions | A record or read-only reference guarantees an immutable reachable graph. |
| Effects and transitions | Explicit transition/effect values versus effects coordinated through component methods | Functional code has no domain effects, or OO must hide them. |
| Control and extension | Central transition dispatch versus delegated behavior; adding operations versus representations | Centralization is always bad, or delegation always good. |
| Boundaries | Hidden change-prone decisions, exposed representations and cross-module obligations | More classes/modules automatically mean better modularity. |
| Language support | Enforced guarantees, conventions, escape hatches, documentation and dependency burden | Identical feature names or equal LOC establish equivalent usability. |

Parnas motivates boundaries around hidden design decisions, rather than merely
steps of processing; this is not a functional-only principle. Hughes supplies
a functional modularity argument through higher-order composition and laziness,
not a controlled maintenance effect size. Its laziness argument is not
automatically an F# result. Coblenz et al. distinguish immutability, read-only
access and assignability and report practitioner needs; those distinctions help
define a treatment precisely. [D1](https://doi.org/10.1145/361598.361623),
[D2](https://doi.org/10.1093/comjnl/32.2.98),
[D6](https://doi.org/10.1145/2884781.2884798).

## What the empirical sources allow us to say

**D4, Arisholm and Sjøberg (2004):** the abstract describes 99 professional
consultants and 59 students performing changes on alternative Java designs.
More-skilled maintainers performed better with delegated control; novices did
better with centralized control. This is particularly relevant because the
language and nominal OO paradigm stay the same while architecture and expertise
matter. It does not show that LLMs behave like novice humans, or experimentally
establish the effect of acquiring expertise.
[DOI](https://doi.org/10.1109/TSE.2004.43).

**D5, Harrison et al. (1996), EFOOL:** 12 image-analysis algorithm sets were
implemented in SML and C++. The abstract reports no significant difference in
selected development-quality measures, including known errors and modification
requests, while some code metrics and testing time differed. Nonsignificance
does not establish equivalence. Old algorithm implementations do not establish
modern large-project or LLM-maintenance outcomes, but this is a useful
counterweight to assuming a universal functional advantage.
[DOI](https://doi.org/10.1049/sej.1996.0030).

**D7, Brborich et al. (2020):** an observational study compares effectiveness
and speed on maintenance tasks using equivalent procedural and OO web
applications. It establishes relevant prior art for the proposed comparison.
The accessible abstract does not give the sample, direction or magnitude needed
to declare a winner, and it explicitly motivates further study.
[DOI](https://doi.org/10.1109/CSEET49119.2020.9206213).

These three studies were read primarily through their complete abstracts, not
full methods audits. That restricts the strength of the claims above. The
earlier [architecture-burden assessment](architecture-maintenance-slopcode-assessment-2026-09-14.md)
retains the longitudinal and technical-debt evidence separately. Neither body
of evidence substitutes for observing this project's LLM maintenance outcomes.

## Proportionate next design, if separately adopted

Retain the supplied F#/modern-C# pair as a feasibility case. For a stronger
architectural claim, first review **one specific architecture contrast**, not
an inventory of programming paradigms. A possible later two-language/two-policy
design would contrast explicit-state/transition organization and encapsulated
component behavior within each language. Its within-language contrasts could
then be compared. This describes the logic of identification, not an adopted
four-cell implementation or an adequate sample-size calculation.

Require both alternatives to be credible designs in each language, with
qualified language/domain review and comparable information and support.
If a combination is artificial, do not force it to fill a table. A narrower
within-language experiment plus an honest package comparison is preferable to
calling an awkward translation an idiomatic control. Do not require equal
source size or classify mutation/inheritance as faults by definition.

A procedural, module-oriented alternative is worth adding only if it tests a
distinct realistic policy—for example, explicit data ownership with a direct
coordinator—rather than serving as a deliberately weak third baseline. It
could overlap substantially with a functional core and imperative shell.

Review a balanced change distribution before outcomes: new operations, new
representations/implementations, migration, asynchronous lifetime interactions
and hot-path constraints. Cook's extension discussion motivates why one
representation need not win on every kind of change. More independent project
families would extend scope more directly than simply adding model draws to
one seed. Later replication beyond .NET would still be needed for broad
cross-language/runtime claims.

The proposed primary observable remains cumulative behavioral correctness and
regression retention under a fixed policy. Architectural diagnostics should
explain witnessed failures/successes, not become an unvalidated elegance index.
Under the present one-submission policy this is success within budget, not
effort-to-success. Human maintenance savings and years-long production effects
remain outside what one supplied pair and eight dependent episodes establish.

Keep context capacity a separate question. The no-tools, fresh-conversation
condition removes tool-repair transcripts, not output-size effects, malformed
responses or language familiarity. The larger F# reference inputs at all eight
episodes are retained; do not tune them to reverse that finding. Maintaining
these supplied seeds does not measure the model's ability to invent their
initial architecture.

**Disposition:** broaden the research theory to architecture and language support,
while retaining F#/C# as the first bounded setting. No additional architecture,
language, library, workload, adapter, budget or execution policy is adopted.
Human review and a precise claim/outcome decision remain next; H flags stay
false, allocations zero, and no OAuth or benchmark model/count call is authorized.

## Reproducible Scite and DOI record

Search date: 2026-09-14 HKT. Connected Scite, user intent
`architecture_paradigm_scope`, limit 5, offset 0, default relevance, no date
filter. This is a bounded targeted investigation, not a systematic review,
exhaustive coverage claim or proof of novelty. Totals below are search hits,
not eligible studies. Title-list matching returned editions and near matches.

| Query | Exact input / extra filter | Total / returned |
| --- | --- | ---: |
| P1 | `"object-oriented" AND "procedural" AND ("maintenance" OR "maintainability")`; title `experiment` | 478 / 5 |
| P2 | `"functional programming" AND "object-oriented" AND ("maintenance" OR "modularity" OR "maintainability")` | 2627 / 5 |
| P3 | Titles: `On the Criteria To Be Used in Decomposing Systems into Modules`; `Why Functional Programming Matters`; `On Understanding Data Abstraction, Revisited` | 10 / 5 |
| P4 | `("immutability" OR "immutable") AND ("comprehension" OR "maintainability")`; title `experiment` | 758 / 5 |
| P5 | DOIs D1, D2, D3, D7 below | 4 / 4 |
| P6 | `"object-oriented" AND "maintenance"`; author `Henry` | 81 / 5 |
| P7 | `"procedural" AND "object-oriented" AND "maintenance"`; title `comparison` | 109 / 5 |
| P8 | `"software" AND ("immutability" OR "immutable") AND "comprehension"` | 16212 / 5 |
| P9 | Titles: `Comparing Programming Paradigms: an Evaluation of Functional and Object-Oriented Programs`; `A Controlled Experiment to Evaluate Maintainability of Object-Oriented Software`; `Evaluating the effect of a delegated versus centralized control style on the maintainability of object-oriented software` | 5 / 5 |
| P10 | DOIs `10.1109/icsm.1997.624239`, D7, D6; term `results` | 3 / 3 |
| P11 | Titles: `The effects of side-effects on program comprehension`; `An empirical comparison of the maintainability of object-oriented and procedure-oriented software` | 0 / 0 |

PM1 queried D4/D5 with term `design`, returning 2/2. PM2 queried the two
recent P2 paradigm-comparison DOIs without a term, returning 2/2. P11 strings
were search leads, not assertions that those exact publications exist.
There were **47 P1–P11 hits and 42 distinct Scite DOIs**; PM1/PM2 added no
new identities. Citation counts and supporting/contrasting labels were not
used to rank paradigm quality. Reprints are not independent experiments.

### Credited scholarly sources and reading extent

| ID / discovery | Canonical identity | Verified extent / limitation |
| --- | --- | --- |
| D1 / P5 | Parnas, *On the Criteria To Be Used in Decomposing Systems into Modules*, CACM 1972; [10.1145/361598.361623](https://doi.org/10.1145/361598.361623) | Original-paper [PDF](https://ckrybus.com/static/papers/decomposing_systems_into_modules_1972.pdf), selected discussion/conclusion pp.1056–1058 and abstract. Conceptual illustration, not an effort experiment. Scite abstract wording was not used to merge reprint details. |
| D2 / P5 | Hughes, *Why Functional Programming Matters*, Computer Journal 1989; [10.1093/comjnl/32.2.98](https://doi.org/10.1093/comjnl/32.2.98) | [Author-text teaching copy](https://courses.cs.umbc.edu/331/resources/papers/whyfp.pdf), introduction, modular-composition sections and conclusion; [author bibliography](https://www.cse.chalmers.se/~rjmh/pubs.htm) corroboration. This copy has a revision history; byte-equivalence to the journal edition is not asserted. |
| D3 / P3, P5 | Cook, *On Understanding Data Abstraction, Revisited*, OOPSLA/Onward 2009; [10.1145/1639949.1640133](https://doi.org/10.1145/1639949.1640133) | Author PDF §§1–3 and practical-duality discussion around p.10. Scite's notice on `10.1145/1640089.1640133` identifies another edition, not a retraction or another experiment. |
| D4 / P9 | Arisholm, Sjøberg, *Evaluating the Effect of a Delegated versus Centralized Control Style on the Maintainability of Object-Oriented Software*, TSE 2004; [10.1109/tse.2004.43](https://doi.org/10.1109/tse.2004.43) | Complete Scite **abstract** plus indexed primary-PDF design passage, not a full methods/results audit. PDF fetch failed; the old Simula landing now redirects readers to NVA and supplies no paper body. |
| D5 / P9 | Harrison, Samaraweera, Dobie, Lewis, *Comparing Programming Paradigms: an Evaluation of Functional and Object-Oriented Programs*, SEJ 1996; [10.1049/sej.1996.0030](https://doi.org/10.1049/sej.1996.0030) | Complete Scite **abstract**, [institutional metadata](https://eprints.soton.ac.uk/250597/) and indexed manuscript first page. Manuscript fetch failed; its displayed rebuild date is not the study's publication date. |
| D6 / P8, P10 | Coblenz et al., *Exploring Language Support for Immutability*, ICSE 2016; [10.1145/2884781.2884798](https://doi.org/10.1145/2884781.2884798) | Scite full-text introduction and definitions, plus method excerpts: eight expert interviews and three pilot users of IGJ-T. Qualitative design evidence, not a longitudinal maintenance-cost effect. |
| D7 / P2, P5, P10 | Brborich, Oscullo, Lascano, *An Observational Study on the Maintainability Characteristics of the Procedural and Object-Oriented Programming Paradigms*, CSEE&T 2020; [10.1109/cseet49119.2020.9206213](https://doi.org/10.1109/cseet49119.2020.9206213) | Complete Scite **abstract** and targeted excerpts only; no verified sample/effect-direction claim. |

Scite body calls were offset 0: D1 length 4500; D4/D5 length 6500;
D6/D7 length 6000; the two recent P2 comparisons length 8000. Only D6 returned
full text (6000 of 58455 characters); the other calls returned abstracts with
`contentDenied=true`, irrespective of search metadata suggesting open access.
Character offsets describe this session's access, not durable edition locators.

Primary-web follow-up checked the supplied blog and selected essay bodies,
official F# documentation, paper titles/author copies and DOI/publisher metadata.
No licensed bodies, private access links, tokens or private transcripts are
retained. Incidental uninspected search-result listings and bibliography targets
are not counted as reviewed studies.

### Remaining Scite DOI decisions

Exclusion below means **not used to substantiate this bounded assessment**,
not disproven, fabricated or necessarily low quality. Seven canonical DOIs
above plus these 35 rows account for all 42 distinct Scite DOI records.

| Query | DOI | Reason not used |
| --- | --- | --- |
| P1 | [10.1007/3-540-15199-0_29](https://doi.org/10.1007/3-540-15199-0_29) | Historical experience report; comparative maintenance identification not assessed. |
| P1 | [10.1109/isese.2005.1541837](https://doi.org/10.1109/isese.2005.1541837) | Subjective evolvability/reviewer agreement, not the selected maintenance intervention; useful future diagnostic-validation lead. |
| P1 | [10.5485/tmcs.2007.0159](https://doi.org/10.5485/tmcs.2007.0159) | Teaching multiparadigm programming, not selected maintenance outcome evidence. |
| P1 | [10.1147/sj.341.0096](https://doi.org/10.1147/sj.341.0096) | Group-support development experience; no controlled style comparison verified here. |
| P1 | [10.1016/s0010-4655(97)00158-6](https://doi.org/10.1016/s0010-4655(97)00158-6) | HEP control framework, not selected maintenance comparison. |
| P2 | [10.1145/2846680.2846689](https://doi.org/10.1145/2846680.2846689) | Already assessed, abstract-only, in the preceding architecture-first note; not a new independent finding here. |
| P2 | [10.21015/vtse.v13i3.2216](https://doi.org/10.21015/vtse.v13i3.2216) | Khan et al., 2025 microservices comparison. DOI/Crossref/publisher metadata and abstract verified; body retrieval failed. Abstract favors OO's balance, but actual maintenance measurements/controls were not verified. Retain for a later methods audit, not as established evidence of superiority. |
| P2 | [10.66472/paf.v1i1.23](https://doi.org/10.66472/paf.v1i1.23) | Simarmata and Karo Karo, 2026 distributed-data comparison. DOI/Crossref/publisher metadata and abstract verified; PDF returned 403. Abstract favors FP/declarative approaches, but maintainability operationalization and controls were not verified. Same exclusion standard as the contrary 2025 abstract. |
| P2 | [10.1109/wse.2012.6320536](https://doi.org/10.1109/wse.2012.6320536) | JavaScript class-style normalization, not selected longitudinal maintenance contrast. |
| P3 | [10.1145/1640089.1640133](https://doi.org/10.1145/1640089.1640133) | Another D3 edition; use canonical proceedings identity, not two studies. |
| P3 | [10.1007/978-3-642-40355-2_7](https://doi.org/10.1007/978-3-642-40355-2_7) | *Why Functional Programming Matters to Me* is a different work, not the requested Hughes paper. |
| P3 | [10.1007/978-3-642-59412-0_26](https://doi.org/10.1007/978-3-642-59412-0_26) | D1 reprint, not an independent result. |
| P3 | [10.1007/978-3-642-48354-7_20](https://doi.org/10.1007/978-3-642-48354-7_20) | D1 reprint identity, not an independent result. |
| P4 | [10.1037/cep0000230.supp](https://doi.org/10.1037/cep0000230.supp) | Bilingual irony-comprehension supplement; off topic. |
| P4 | [10.1145/3341642](https://doi.org/10.1145/3341642) | Racket/Chez runtime experience, not an isolated maintenance-style contrast. |
| P4 | [10.1111/josi.12642](https://doi.org/10.1111/josi.12642) | Social perceptions, not software maintenance. |
| P4 | [10.3390/socsci8070201](https://doi.org/10.3390/socsci8070201) | Border experiences, not software maintenance. |
| P4 | [10.3390/jsan13010006](https://doi.org/10.3390/jsan13010006) | Dairy blockchain experience, not selected architecture contrast. |
| P6 | [10.1109/metric.1993.263801](https://doi.org/10.1109/metric.1993.263801) | OO maintenance metrics, not selected style-intervention evidence. |
| P6 | [10.1002/smr.4360070206](https://doi.org/10.1002/smr.4360070206) | Maintenance in two OO systems; methods not assessed in this bounded follow-up. |
| P6 | [10.1108/01443570010318913](https://doi.org/10.1108/01443570010318913) | Manufacturing-cell specification, outside selected comparison. |
| P6 | [10.4271/2004-01-0110](https://doi.org/10.4271/2004-01-0110) | CFD toolkit, outside selected comparison. |
| P6 | [10.1108/17410380410523461](https://doi.org/10.1108/17410380410523461) | Manufacturing framework, outside selected comparison. |
| P7 | [10.1109/mysec.2011.6140642](https://doi.org/10.1109/mysec.2011.6140642) | Broad development-approach comparison; outcome/methods not verified. |
| P7 | [10.33899/csmj.2013.163431](https://doi.org/10.33899/csmj.2013.163431) | Design-metric comparison, not verified maintenance outcome. |
| P7 | [10.5220/0001336602130221](https://doi.org/10.5220/0001336602130221) | Structured/OO analysis documents, not the selected code-maintenance outcome. |
| P7, P10 | [10.1109/icsm.1997.624239](https://doi.org/10.1109/icsm.1997.624239) | Briand et al. compare OO/structured design documents. Relevant quality-versus-style lead; only excerpts inspected, no independently verified sample/effect estimate. |
| P7 | [10.1109/ms.2003.1207450](https://doi.org/10.1109/ms.2003.1207450) | Inspection-technique contrast, not the selected architectural treatment. |
| P8 | [10.1145/1287624.1287637](https://doi.org/10.1145/1287624.1287637) | IGJ technical mechanism; D6 supplies the selected usability/taxonomy discussion. |
| P8 | [10.7717/peerj-cs.1542](https://doi.org/10.7717/peerj-cs.1542) | Knowledge-graph augmentation, outside selected comparison. |
| P8 | [10.48550/arxiv.2606.31354](https://doi.org/10.48550/arxiv.2606.31354) | Git tag alteration, not program-state immutability. |
| P8 | [10.30564/ret.v4i4.3590](https://doi.org/10.30564/ret.v4i4.3590) | Art education, not software maintenance. |
| P9 | [10.1007/3-540-32179-9_20](https://doi.org/10.1007/3-540-32179-9_20) | D4 reprint identity, not another experiment. |
| P9 | [10.1007/978-3-540-32179-8_20](https://doi.org/10.1007/978-3-540-32179-8_20) | D4 reprint identity, not another experiment. |
| P9 | [10.1109/icsm.1990.131370](https://doi.org/10.1109/icsm.1990.131370) | Henry/Humphrey controlled OO-maintenance lead; institutional TR-90-39 abstract supports OO over procedural in its comparison. Full methods not assessed; do not substitute it for a modern general effect. |

Supplementary web lead [Hu, Hughes and Wang, 2015,
10.1093/nsr/nwv042](https://doi.org/10.1093/nsr/nwv042) was not selected:
its functional-programming influence review was not audited as comparative
maintenance evidence. B1–B3 and the homepage source-boundary check have no DOIs;
their exact URLs identify them. Official F# documentation is credited only for
language capabilities, not evidence of maintenance savings.

### Review and publication boundary

One Luna Max worker performed bounded read-only blog extraction under the
installed agent-deployment guidance. The main agent verified the three essay
bodies, checked the primary scholarly evidence to the extents declared above,
and owns the research synthesis and self-review. No human expert approval or
independent statistical replication is claimed.

Scite decision/audit ID: `alf-paradigm-architecture-scope-2026-09-14`.
The single decision submission accepted **12 cited / 36 excluded / 0 skipped**
records: seven scholarly DOI identities, five non-scholarly capability/context
sources, 35 other Scite DOIs and one supplementary web DOI. Thus 12 credited
records do not mean 12 empirical studies. The answer-scoped audit covered all
48 decisions, was not truncated, and reported no missing reasons or unlinked
retrievals. It does not independently validate the papers' results.

The main agent checked strict UTF-8 decoding of the three changed documents,
81 relative file-link targets, the seven/35 Scite DOI partition, and claim/access
boundaries. Path checks do not verify every Markdown anchor or external server.
Staged whitespace is checked with `git diff --cached --check`. No local code or
candidate tests are required for these documentation-only edits. The containing
commit's exact model-free CI must be verified after direct push, not inferred
from its parent's successful run; it is not yet available at this pre-publication
writing checkpoint. No code, construction fixture, scientific approval or live
allocation changed.
