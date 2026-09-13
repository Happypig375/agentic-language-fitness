# Architecture, maintenance burden and SlopCodeBench

**Date:** 2026-09-14 HKT. Targeted research/design assessment, not a protocol adoption.

**Inspected repository:** `b8850c6fd7b069c1f55171fe85c7776815ae64bc`.
The [current review packet](maintenance-sim-human-review-2026-09-12.md)
remains authoritative for construction settings and open approvals. This note
extends the [verifiability assessment](maintenance-research-verifiability-2026-09-13.md);
it does not replace its evidence or the frozen historical experiments.

## Assessment

Architecture-first is a worthwhile direction, provided the claim is narrower
than “F# has an architectural advantage.” Separate two questions:

1. Under ample, fully supplied context, do independently idiomatic F# and modern
   C# implementations support different maintenance outcomes under matched changes?
2. Does reducing available context change that difference?

The first need not depend on F# being shorter. The second needs a genuinely
different context treatment, not two labels on identical inputs. Architectural
organization could affect comprehension even when everything fits; separating
experimental questions does not prove their mechanisms are unrelated.

The literature below supports the importance of the question, not a universal
architecture-to-cost conversion, nor an established F# effect. Counts of papers
or Scite supporting statements are not an effect estimate. This was a bounded
search, not a systematic review or proof of novelty.

## What measured maintenance evidence supports

| Source | Observation and unit | Limit on interpretation |
| --- | --- | --- |
| S1, Xiao et al., ICSE 2016 | In seven Apache projects, the top five detected debts involved 8–25% of error-prone files and 20–61% of **bug-fixing churn**, used as an effort proxy. | Retrospective identification using history, not measured labor savings from a randomized architectural intervention. |
| S2, Besker et al., TechDebt 2018 | 43 developers in six companies supplied 473 reports over seven weeks; average reported time wasted because of technical debt was 23%. | Repeated self-report, all technical-debt types; neither architecture-only attribution nor a population constant. |
| S3, Nayebi et al., industrial longitudinal case | The preprint's Table II reports average bug-fixing duration 10.74 → 7.31 days and churn 102 → 33.9 LOC per bug after refactoring. | One evolving company/product; features and business rules also changed. Elapsed resolution time and churn are not interchangeable with active developer hours. |
| S4, de Toledo et al., SEAA 2021 | The conference abstract reports 84% fewer incidents after selected architectural-debt repayment in a roughly 1,000-microservice financial system. | Before/after case; incident count is not maintenance effort. Paper-level controls and observation windows were not verified from full text. |
| S5, Lenarduzzi et al., SEAA 2021 | SonarQube debt-item counts did not establish a robust increased-delay relationship across the studied Java projects. | Small/weak associations existed; this is not proof that architecture has no effect. Their lead-time measure used inducing/fixing commit timestamps, not directly observed labor. |

Primary access and exact editions: [S1 author paper](https://personal.stevens.edu/~lxiao6/papers/ICSE-16-Debt.pdf),
[S2 DOI](https://doi.org/10.1145/3194164.3194178),
[S3 preprint v1](https://arxiv.org/pdf/1811.12904v1),
[S4 conference abstract](https://dsd-seaa2021.unipv.it/seaa/AcceptedPapers.html?sec=accepted),
[S5 DOI](https://doi.org/10.1109/SEAA53835.2021.00032).
S1 §§1,7 acknowledge the churn proxy. S2 methods and validity passages were
read through Scite. S3 §§IV–VI and Table II were checked: the separate 72%
figure concerns a selected issue/file comparison and must not replace the
table's bug-duration measure. S5 §§IV–VII report weak negative raw correlations,
a small presence/absence difference and a Granger finding in only one of 22
eligible projects; an abstract's “no effect” wording alone hides that detail.

These results motivate measuring *consequences of change*, not awarding a
maintainability score for attractive syntax. They also caution against treating
fewer smells, files or changed lines as automatically less work.

S6, [Figueroa and Robbes, PLATEAU 2015](https://doi.org/10.1145/2846680.2846689),
is especially relevant to framing: its abstract questions the empirical reach
of general functional-programming/modularity claims and describes a small GHC
investigation. Only its abstract was verified here. It is neither an F#–C#
comparison nor evidence that no relevant research exists in 2026.

## What SlopCodeBench already covers

[S7, primary v2, 7 May 2026](https://arxiv.org/html/2603.24755v2) contains 36
problems and 196 checkpoints: agents start from scratch, choose internal
architecture and repeatedly extend persistent code. Fresh sessions prevent chat
history from being the only accumulated state. Native tool-using agents are
evaluated on correctness, structural erosion, verbosity and resource cost;
the reported experiments are Python-only.

Appendix B.3 already relates earlier metrics to next-checkpoint outcomes:
reported erosion correlates 0.167 with cost and −0.018 with pass rate; LOC's
cost correlation is 0.502. Those raw associations do not isolate architectural
causation. The human-repository comparison is not a matched architecture
intervention. Neither controlled F#/C# architecture contrasts nor context-boundary
manipulation are established by these results.

Thus “iterative agents accumulate bad code” and “earlier code metrics relate
to later cost” are not sufficient novelty claims for this project.

## A defensible extension, not another benchmark framework

My recommended first research question is:

> Under the same maintenance obligations, model and fixed response policy,
> do separately idiomatic F# and modern-C# architecture packages differ in
> cumulative correctness and regression retention when all eligible context is supplied?

This is a package comparison. Language syntax, representation, authored
architecture, guidance, libraries and model familiarity can all contribute.
Calling a package result an intrinsic language effect would overstate it.

A mechanistic hypothesis can accompany it: explicit invariant ownership,
consistent state/effect boundaries and useful extension boundaries might reduce
missed obligations or inappropriate cross-boundary changes. Evidence must connect
those features to later witnessed successes/failures, not merely to the presence
of unions, records, classes, mutation or eloquent impact explanations.

The strongest incremental contribution would be a controlled test of that
mechanism. Behaviorally equivalent architecture alternatives *within a language*
would help separate architecture from language. That would be a new reviewed
treatment, not an automatic addition to the current pair. Avoid a deliberately
bad C# baseline or a straw-man “unstructured” variant. Assess plausible trade-offs
and their consequences under different kinds of change.

A proportionate sequence is:

1. Human-review the existing pair as a feasibility case. Modern C# receives
   serious idiomatic design and comparable architectural/domain guidance.
   Record expertise and support costs; do not imply that knowing an idiom or
   selecting an architecture comes for free.
2. Specify a behavioral primary outcome before candidate results. A reasonable
   choice for review is cumulative-contract success under a fixed budget,
   with regressions and inherited-defect survival reported separately.
   Define missing/unsafe/apparatus-failure treatment explicitly; retain every
   scheduled attempt rather than analyzing only surviving compilable snapshots.
3. Use architectural diagnostics as explanatory evidence. Validate their
   reliability and relevance against observable obligations; do not combine
   them into an unvalidated “F# elegance” score. A Python-oriented complexity
   or smell threshold should not become a cross-language architecture score
   without validating its meaning in both languages.
4. For broader claims, add independently authored project/architecture families
   selected before outcomes. Repeated model draws do not create new projects;
   successive episodes are dependent. Do not build a large factorial study
   merely to make the pilot look definitive.
5. Only later consider an architectural intervention or context-capacity arm,
   with its own reviewed question and allocation.

The change distribution matters: adding a new operation can favor a different
representation from adding a new variant or external implementation. Include
countervailing changes, such as hot-path mutation, migration and asynchronous
lifecycle interactions. Review changes against realistic maintenance needs, not
which language wins. More abstractions can themselves create indirection and
learning costs.

Do not automatically “control away” source size as if it were an unrelated
nuisance: size may be part of the proposed mechanism. Instead distinguish the
total package outcome from a separately justified mechanism analysis. Full-file
response size can impose an output burden even with ample input context.

The existing prototype should answer whether the desired measurements are
feasible. Prior benchmarks can inform contracts and analysis without importing
their hidden solutions, duplicating an entire benchmark suite or adding new
runner/proxy infrastructure. The present search does not establish a “first”
claim for this exact combination; a paper would still need a wider novelty review.

## What the current construction can and cannot establish

The [standalone packet](maintenance-sim-human-review-2026-09-12.md) already has
one supplied idiomatic pair, eight inherited episodes, fresh conversations,
no tools, one submission per episode and no diagnostic repair feedback.
Safe wrong/noncompiling state persists. That removes wrong-tool-call repair
transcripts from the condition, but not malformed responses, language familiarity,
candidate code growth or output-size effects.

This is maintenance of a **supplied architecture**, not a test of whether F#
makes the model invent a better initial architecture. Changing the seed source
would change the question.

With a single fixed submission per episode, the defensible outcome is success
within that budget, not effort required to reach a correct solution. More tokens
or wall time could reflect response size or a more complete attempt. Estimating
effort-to-success would need a separately reviewed repair/completion policy and
explicit handling of unsolved/censored attempts; it is not silently adopted here.

The proposed 86,016 input / 61,440 output authored-byte caps remain unactivated.
All trusted reference inputs fit; F# inputs are larger at every episode. This
does not demonstrate a context boundary, but neither does it disprove a possible
maintenance benefit. Preserve that finding. Do not tune source or tasks to
reverse it.

The present one-pair, eight-episode construction supports feasibility, not
large-project or years-long generalization. Human maintenance evidence motivates
an LLM experiment; it does not substitute for one, and an LLM result would not
by itself establish human-team savings.

**Disposition:** recommend architecture-first research with context capacity
kept separate. This is an assistant recommendation responding to the user's
question, not approval of a revised protocol. No workload, evaluator, adapter,
model, backend, allocation or execution flag changed. Next remains human review
of the construction and the precise claim/outcome to adopt.

## Reproducible search and source record

Search began 2026-09-13 HKT and continued across midnight to 2026-09-14.
Connected Scite searches used limit 5, offset 0, default relevance, no date
filter, and user intent `architecture_maintenance_burden`. Counts are returned
records, not eligible-study counts. Titles can match editions of one work.

| Query | Exact search; extra filters | Returned total / inspected hits |
| --- | --- | ---: |
| A1 | `"architectural technical debt" AND ("maintenance" OR "cost" OR "productivity")` | 121 / 5 |
| A2 | `"architecture" AND "maintenance effort"`; title `empirical` | 64 / 5 |
| A3 | `"modularity" AND ("change cost" OR "maintenance effort" OR "change effort")` | 2524 / 5 |
| A4 | `"architecture" AND ("technical debt interest" OR "maintenance burden")` | 1196 / 5 |
| A5 | titles: `Identifying and Quantifying Architectural Debt`; `The Impact of Software Architecture on Developer Productivity`; `Is functional programming better for modularity?` | 2 / 2 |
| A6 | `"architecture" AND "maintenance costs"`; title `empirical` | 180 / 5 |
| A7 | `"architectural debt" AND ("cost" OR "defects" OR "change")` | 202 / 5 |
| A8 | `"technical debt" AND "wasted" AND "time"` | 599 / 5 |
| A9 | title list: `A Longitudinal Study of Identifying and Paying Down Architectural Debt` | 2 / 2 |
| A10 | title list: `Technical Debt Impacting Lead-Times: An Exploratory Study` | 1 / 1 |

AM1/AM2 targeted S2's DOI with terms `methodology` and
`"23" OR "validity"`, respectively: one hit each, same limit/offset.
The unmatched productivity title in A5 was a search lead, not a publication
assertion. Primary-web follow-up searched exact paper titles for author copies,
checked SlopCodeBench's current version, and checked conference/DOI metadata.

There were 40 main-query hits, 38 distinct Scite DOIs. Seven DOI records were
used for six study lineages; S3's conference and preprint are one study.
S7 adds one primary-web preprint lineage. The table below records all 38 DOI
decisions; exclusion means not used in this bounded assessment, not disproven
or necessarily low quality. Citation snippets' bibliography targets and
incidental uninspected web-result listings are not additional reviewed studies.

### Used sources: identity and access

| ID | Identity | Verified reading extent |
| --- | --- | --- |
| S1 | Xiao, Cai, Kazman, Mo, Feng; ICSE 2016, pp.488–498; [10.1145/2884781.2884822](https://doi.org/10.1145/2884781.2884822) | Author PDF §§1,7 and abstract; Scite body unavailable. Crossref confirms title/DOI/pages. Author-copy footer instead prints `...2884825`; retain the discrepancy, use the verified metadata identity, not the footer as a second study. |
| S2 | Besker, Martini, Bosch; TechDebt 2018, pp.105–114; [10.1145/3194164.3194178](https://doi.org/10.1145/3194164.3194178) | Scite primary introduction and methods plus targeted results/validity passages; not an independent reading of every page. Seven-week repeated surveys, not ten months of diary observations. Public author PDF did not open through the web tool. |
| S3 | Nayebi et al.; ICSE-SEIP 2019; [10.1109/ICSE-SEIP.2019.00026](https://doi.org/10.1109/ICSE-SEIP.2019.00026); preprint [10.48550/arXiv.1811.12904](https://doi.org/10.48550/arXiv.1811.12904) | Methods/results/limits from **v1, 30 November 2018**, especially §§IV–VI, VIII and Table II; conference metadata verified separately. VOR body equivalence not asserted. |
| S4 | de Toledo, Martini, Sjøberg, Przybyszewska, Frandsen; SEAA 2021, pp.196–205; [10.1109/SEAA53835.2021.00033](https://doi.org/10.1109/SEAA53835.2021.00033) | **Conference abstract only.** Scite's purported full text began a 317,357-character thesis, not an identified paper body; rejected for full-paper evidence. |
| S5 | Lenarduzzi, Martini, Saarimäki, Tamburri; SEAA 2021, pp.188–195; [10.1109/SEAA53835.2021.00032](https://doi.org/10.1109/SEAA53835.2021.00032) | Scite primary introduction and selected §§IV–VII; conference abstract corroboration. Java/SonarQube scope, not a general architectural null. |
| S6 | Figueroa, Robbes; PLATEAU 2015, pp.49–52; [10.1145/2846680.2846689](https://doi.org/10.1145/2846680.2846689) | **Abstract only**, Scite and institutional record; workshop paper, not contemporary F#/C# evidence. |
| S7 | Orlanski et al.; [10.48550/arXiv.2603.24755](https://doi.org/10.48550/arXiv.2603.24755) | Primary **v2, 7 May 2026**; §§2–3, B.3, C.1, D.1; preprint status, not inferred peer review from DOI. |

Scite body calls: S1/S2/S4/S6 at offset 0, length 6000;
S2 additionally offset 6000, length 8000; S5 offsets 0/12500/20500,
lengths 8000/8000/5500. Offsets document access, not durable section locators.
No licensed full bodies, private transcripts, access tokens or institutional
access URLs were saved to the repository.

A Luna Max worker performed bounded read-only S7 scope extraction under the
installed agent-deployment guidance. The main agent checked primary claims,
including B.3, and owns the synthesis and self-review; no human expert review
is claimed. The injected old Orca routing-file path was absent; the available
global routing instruction and installed skill governed delegation.

### Complete Scite DOI screening

| Query provenance | DOI | Decision |
| --- | --- | --- |
| A1 | [10.1145/3194164.3194176](https://doi.org/10.1145/3194164.3194176) | Identification process, not selected burden measurement. |
| A1 | [10.1142/s021819402150008x](https://doi.org/10.1142/s021819402150008x) | Refactoring cost estimation is not observed downstream maintenance burden; retained lead only. |
| A1 | [10.1007/978-3-030-58923-3_14](https://doi.org/10.1007/978-3-030-58923-3_14) | Returned abstract was a repository/rights notice; substantive evidence not verified. |
| A1 | [10.1109/seaa53835.2021.00033](https://doi.org/10.1109/seaa53835.2021.00033) | Use S4. |
| A1 | [10.5220/0009577805310539](https://doi.org/10.5220/0009577805310539) | Debt-index construction, not validated downstream burden in this follow-up. |
| A2 | [10.1109/csmr.2011.26](https://doi.org/10.1109/csmr.2011.26) | Operational knowledge intervention, outside selected architecture contrast. |
| A2 | [10.38124/ijsrmt.v3i4.1540](https://doi.org/10.38124/ijsrmt.v3i4.1540) | Testing-framework focus; venue and burden evidence not verified. |
| A2 | [10.48550/arxiv.2205.01842](https://doi.org/10.48550/arxiv.2205.01842) | Method-size study, not selected architectural maintenance intervention. |
| A2 | [10.2139/ssrn.4693779](https://doi.org/10.2139/ssrn.4693779) | Architecture-smell evolution lead; downstream burden not verified here. |
| A2, A6 | [10.1016/j.infsof.2016.01.012](https://doi.org/10.1016/j.infsof.2016.01.012) | GUI-test-suite maintenance, outside selected architecture contrast. |
| A3 | [10.2307/3250939](https://doi.org/10.2307/3250939) | System lifetime/effort relationship, not selected architecture contrast. |
| A3 | [10.1155/2010/685950](https://doi.org/10.1155/2010/685950) | Community project economics, not selected architecture contrast. |
| A3 | [10.1016/s0164-1212(00)00033-9](https://doi.org/10.1016/s0164-1212(00)00033-9) | Relevant broader maintenance-effort lead; full methods not assessed in this bounded follow-up. |
| A3, A5 | [10.1145/2846680.2846689](https://doi.org/10.1145/2846680.2846689) | Use S6. |
| A3 | [10.1016/b978-0-12-410464-8.00006-4](https://doi.org/10.1016/b978-0-12-410464-8.00006-4) | Decision-support model, not selected observed burden study. |
| A4 | [10.48550/arxiv.1810.10855](https://doi.org/10.48550/arxiv.1810.10855) | Microservices debt-interest lead; body/outcome not verified here. |
| A4 | [10.1007/s42979-020-00406-6](https://doi.org/10.1007/s42979-020-00406-6) | Relevant debt-interest case lead; body not assessed here. |
| A4 | [10.5220/0001729802950300](https://doi.org/10.5220/0001729802950300) | Ontology maintenance rather than the software-architecture comparison. |
| A4 | [10.3389/frobt.2024.1437496](https://doi.org/10.3389/frobt.2024.1437496) | Synthetic consciousness, outside software-maintenance burden. |
| A4 | [10.1057/palgrave.ejis.3000688](https://doi.org/10.1057/palgrave.ejis.3000688) | Agent-oriented modeling framework, outside selected burden comparison. |
| A5 | [10.1145/2884781.2884822](https://doi.org/10.1145/2884781.2884822) | Use S1. |
| A6 | [10.1007/s10257-005-0029-y](https://doi.org/10.1007/s10257-005-0029-y) | Application-architecture survey lead; burden estimand not verified. |
| A6 | [10.64220/amla.v2i2.005](https://doi.org/10.64220/amla.v2i2.005) | Connectivity-framework focus; venue and burden evidence not verified. |
| A6 | [10.4028/www.scientific.net/amr.368-373.854](https://doi.org/10.4028/www.scientific.net/amr.368-373.854) | Building economics, not software architecture. |
| A6 | [10.1504/ijitm.2010.029432](https://doi.org/10.1504/ijitm.2010.029432) | SOA adoption/enabler survey, not selected longitudinal maintenance-burden study. |
| A7 | [10.1109/seaa.2018.00073](https://doi.org/10.1109/seaa.2018.00073) | Debt-index design, not selected observed maintenance outcome. |
| A7 | [10.1109/access.2022.3158648](https://doi.org/10.1109/access.2022.3158648) | Debt accumulation/prioritization during migration; body not assessed here. |
| A7 | [10.24251/hicss.2021.807](https://doi.org/10.24251/hicss.2021.807) | Organizational innovation/debt tensions, outside selected burden contrast. |
| A7 | [10.1007/978-3-030-00761-4_21](https://doi.org/10.1007/978-3-030-00761-4_21) | Smell-based identification/prioritization, not selected downstream burden measurement. |
| A7 | [10.1109/sam.2015.11](https://doi.org/10.1109/sam.2015.11) | Management-method overview, not primary burden measurement. |
| A8 | [10.1145/3194164.3194178](https://doi.org/10.1145/3194164.3194178) | Use S2. |
| A8 | [10.5753/jserd.2023.2417](https://doi.org/10.5753/jserd.2023.2417) | Debt-management organizational practice, outside selected burden contrast. |
| A8 | [10.7551/mitpress/12440.001.0001](https://doi.org/10.7551/mitpress/12440.001.0001) | Broad practice book, not an independent primary burden study. |
| A8 | [10.1109/ms.2021.3086578](https://doi.org/10.1109/ms.2021.3086578) | Practice guidance, not selected primary burden measurement. |
| A8 | [10.1016/j.infsof.2022.106926](https://doi.org/10.1016/j.infsof.2022.106926) | Prevention framework; body/outcome not assessed here. |
| A9 | [10.1109/icse-seip.2019.00026](https://doi.org/10.1109/icse-seip.2019.00026) | Use S3. |
| A9 | [10.48550/arxiv.1811.12904](https://doi.org/10.48550/arxiv.1811.12904) | Use S3. |
| A10 | [10.1109/seaa53835.2021.00032](https://doi.org/10.1109/seaa53835.2021.00032) | Use S5. |

Three considered supplementary web records were excluded: Adrian Colyer's
2016 *The Morning Paper* explanation of S1 and the
[SciSpace S1 aggregator](https://scispace.com/papers/identifying-and-quantifying-architectural-debt-47zlhf2enm)
were secondary duplicates, replaced by the author paper; the
[later developer-productivity replication/extension lead](https://www.sciencedirect.com/science/article/pii/S0164121219301335)
was title/snippet-only here and was not counted as independently verified
sample/effect evidence.

Scite answer ID: `alf-architecture-maintenance-burden-2026-09-14`.
The one final decision submission accepted **8 cited DOI records / 34 excluded
records / 0 skipped**: 38 Scite DOIs plus four supplemental web records.
The eight credited DOIs represent seven study lineages, not eight independent
studies. The read-only audit checked source decisions and reasons.

### Documentation verification and publication boundary

The main agent self-checked source units, editions and claim limits, strict UTF-8
decoding of the three changed documents, and existence of 79 relative file-link
targets in those documents. This checks paths, not every Markdown anchor or
external server. Staged whitespace is checked with `git diff --cached --check`.
No code or experimental fixture changed; no local candidate/test execution was
needed for these documentation edits. The containing commit's existing
Linux/Windows model-free CI must be checked after direct publication, not
inferred from the earlier source commit's green CI. That external CI result is
not available at this pre-publication writing checkpoint.
