# Discovery ledger: Nu form factors and research mechanisms

**Date:** 2026-09-14. **ALF starting head:** `ec2226e50b6a2de11e7cb2e2f2d7cd0d1d27dbd1`.
Companion: [claims, implications and reading additions](nu-form-factors-and-research-leads-2026-09-14.md).

## Scope and evidence level

The user requested Nu FAQ/blog/archive reading followed by paginated scite research before a later agent acquires the PDFs. This pass asks which concrete architectural/notation/tool trade-offs the practitioner sources suggest and which existing research could qualify those hypotheses or occupy the proposed gap. It is discovery and selected textual inspection, not a systematic review or completion of the full-PDF assignment. No PDF was retrieved, no paper was certified fully read, no Nu runtime was executed and no experiment was allocated.

The considered set contains 108 distinct literal DOI identifiers plus seven practitioner/discovery URLs. Related editions, title duplicates, graph nodes and retrieval positions are not independent studies. A credited reading-queue item may support only its identity/relevance, not a finding about agents. D below means deferred or related-edition evidence, not rejection on merit. N means outside this bounded question, not bad research.

## Practitioner material actually read

| Source | Reading and provenance | Limit |
| --- | --- | --- |
| [Nu FAQ](https://github.com/bryanedds/Nu/wiki/Frequently-Asked-Questions) | Returned page revision March 23, 2026; substantive design/type-safety and MMCC usage sections read. | Author guidance, not a controlled study. Later blog links refer to additions not present in this returned revision. |
| [Choosing ImSim/MMCC](https://github.com/bryanedds/Nu/wiki/Choosing-Between-ImSim-and-MMCC-For-Your-Game) | Returned page revision January 14, 2026; domain suitability, proximity and ordering trade-offs read. | Domain recommendations are author judgements; verify behavior against pinned code before designing a witness. |
| [Immediate mode all the things](https://vsynchronicity.wordpress.com/2024/11/18/immediate-mode-all-the-things-with-nu-game-engine/) | Main prose and illustrative code inspected. Published November 18, 2024; displayed update July 1, 2025. | Illustration of an API, not measured superiority or a current-runtime test. |
| [Pinned technical archive synthesis](https://github.com/Happypig375/nu-chat-analysis/blob/59f2bdee94575a087eda6b5278dcafdd68084a46/analysis/derived/bryanedds-nu-synthesis/report.md) | GitHub connector; technical portions of sections 1–6 examined at the stated commit. | Derived AI synthesis, useful for tracing sources, not independent corroboration. No claims from unrelated personal/social material. |
| [Blog homepage](https://vsynchronicity.wordpress.com/) | Discovery excerpts inspected. | Explicitly simulated expert dialogues are not real interviews/testimony and are excluded as empirical support. |
| [Simplicity-aware programming](https://vsynchronicity.wordpress.com/2026/09/07/simplicity-aware-programming/) | Search excerpt only; primary open failed. | Access-limited. No complete article reading or merger with the older returned FAQ claimed. |
| [Earlier Elm-style article](https://vsynchronicity.wordpress.com/2020/03/01/a-game-engine-in-the-elm-style/) | Discovery lead only. | Deferred, not counted as another source read in full. |

A failed open or guessed article path supplied no evidence. The matching connected GitHub app was used for the user's repositories. Public wiki/blog prose was read through web retrieval. No GitHub wiki-history commit was established for the returned pages; the displayed dates above are not invented immutable hashes.

## Search protocol and pagination

All scite literature requests used **limit 20**, including exact identity lookups. No date, publication-type or citation-count filters; relevance ordering. Exact lookups naturally returned fewer than twenty when fewer records matched. The two broad searches each continued past their first page.

| ID | Exact query / selection | Offset and requested/effective size | Returned / reported extent |
| --- | --- | --- | --- |
| N1a | `"cognitive dimensions" AND ("programming" OR "notation")` | 0; 20/20 | 20 of 14,925 |
| N1b | Same N1 query | 20; 20/20 | 20 of 14,925; positions 41–14,925 unexamined |
| N2a | `"change propagation" AND ("software architecture" OR "modularity")` | 0; 20/20 | 20 of 1,086 |
| N2b | Same N2 query | 20; 20/20 | 20 of 1,086; positions 41–1,086 unexamined |
| E1 | Twelve exact DOIs listed below, with a CodePlan title in the same request | 0; 20/20 | 12 records; the combined request did not recover CodePlan |
| E2 | Exact title `CodePlan: Repository-level Coding using LLMs and Planning` | 0; 20/20 | 2 records, publication and preprint |
| E3 | Exact DOIs `10.48550/arxiv.2110.15246`, `10.1109/ICSE48619.2023.00058`, `10.1145/3510003.3519016` | 0; 20/20 | 3 records, all previously discovered graph nodes |

E1's DOI input was:

```text
10.1006/jvlc.1996.0009
10.22152/programming-journal.org/2023/7/13
10.1002/spe.3435
10.1145/2577080.2577083
10.1109/TSE.2017.2655524
10.1016/j.jvlc.2016.07.005
10.48550/arXiv.2603.00601
10.1016/j.jss.2021.110947
10.1109/ASWEC.2009.31
10.1145/361598.361623
10.1145/3609025.3609478
10.1145/3759163.3760429
```

The seven search calls returned **97 positions**. Their union contains 90 literal DOI identifiers: 80 broad-query identities, five new identities from E1, two CodePlan identities, and three exact graph-follow-up identities. The graph adds eighteen further identities not in that final search union, yielding 108. Equivalently, before E3 the search union had 87; the graph contributes its twenty citers and one linked preprint, with E3 later revisiting three of those. These are identifier counts, not paper-reading counts.

N1 was intentionally exploratory and noisy, including other uses of cognitive dimensions. N2 likewise included mechanical-product change propagation. These tails are not evidence for or against software claims. ToCS appeared at N2 position 30; stopping at five or twenty would have missed this close lead. Conversely, reading forty positions is not saturation. Known source identity checks and primary-source follow-up supplied the focused synthesis.

## Selected scholarly reading and remaining limits

| DOI | Actual material inspected | Use and remaining work |
| --- | --- | --- |
| `10.22152/programming-journal.org/2023/7/13` | [Official journal metadata](https://programming-journal.org/2023/7/13/) and selected [author HTML](https://tomasp.net/techdims/) defining programming systems, qualitative dimensions, factoring/automation and feedback. | Conceptual distinction between notation and the whole programming system. Not a measured agent effect. Original PDF and complete paper remain pending. Primary site identifies Jakubovic, Edwards and Petricek; scite's abbreviated author list alone was incomplete. |
| `10.1006/jvlc.1996.0009` | Exact metadata; original body not read. An attempted author-introduction route failed. | Conditional full-reading identity for the Cognitive Dimensions vocabulary, not an empirical result. |
| `10.48550/arxiv.2603.00601` | [Primary v4 HTML](https://arxiv.org/html/2603.00601v4), selected sections 3, 6.5 and 7; v4 dated March 18, 2026. | Close predecessor on architectural-map construction. Evaluated scope versus roadmap, map probes as intervention, limited synthetic population and reported-graph proxy. Full reading added as P12. No whole-paper or released-code audit claimed. |
| `10.1145/3643757` | Exact publication metadata and [2024 author abstract](https://www.microsoft.com/en-us/research/publication/codeplan-repository-level-coding-using-llms-and-planning-2/); [2023 author page](https://www.microsoft.com/en-us/research/publication/codeplan-repository-level-coding-using-llms-and-planning/) checked for lineage. | Dependency/impact-aware planning already exists. Publication and preprint evaluation counts differ; full publication reading added as P13 rather than combining numbers. |
| `10.1109/tse.2017.2655524` | Exact metadata and [authors' publication abstract](https://www.rescala-lang.com/publications). | Human reactive/Observer comprehension evidence motivates a question; it does not establish an LLM or Nu benefit. Full protocol/denominators not reconstructed. |
| `10.1002/spe.3435` | [Publisher abstract](https://onlinelibrary.wiley.com/doi/10.1002/spe.3435) and actual scite body prefix: offset 0, 8,000 of 161,620 characters, `source: fulltext`, `hasMore: true`. | Metric versus user-task/usability distinctions, not full-paper reading. Remaining 153,620 extracted characters and PDF not read. Do not infer all methods from the introduction's summary. |
| `10.48550/arxiv.2110.15246` | [Primary abstract](https://arxiv.org/abs/2110.15246), after the graph returned a contrasting citation label. | A static readability-metric case is not a direct replication/refutation of the human comprehension experiment. Detailed methods remain pending. |
| `10.1109/icse48619.2023.00058` | Exact title/metadata and publisher listing. | Conditional reading on loops/streams and debugger support. No claimed direction or magnitude of its findings. |

The eight credited DOI identities above include reading-queue items and narrowly credited abstracts. Only three had selected scholarly body/HTML passages inspected. No article was fully reconstructed from its PDF. Purely primary sources support the technical findings; search mirrors are leads, not substitutes for source methods.

## Citation graph and interpretation

One incoming graph request used three seeds: ToCS, the TSE reactive-comprehension study and Technical Dimensions. Scite added linked preprint `10.48550/arxiv.2302.10003`, yielding four seed identities. Settings: direction `in`, depth 1, `max_edges: 20`, intent and snippets enabled.

Returned **20 edges / 24 nodes; truncated true**. Per-seed coverage was respectively **0 / 20 / 0 / 0**. All twenty returned citing edges concern the TSE study; the other seeds were flagged low coverage. This graph cannot establish that ToCS or Technical Dimensions has no follow-on work, and it is not an exhaustive reactive-programming screen.

`source s -> target t` means s cites t. Some passages cite the TSE work for statistical procedure, not for a replicated comprehension finding. The Holst/Dobslaw readability-metric paper carried a contrasting label, but the primary abstract showed a different measurement target. The label is not a vote against reactive programming. The debugger and metric papers were followed with exact lookups; other graph nodes remain leads.

## Complete DOI inventory

C = narrowly credited as specified above; D = deferred/unassessed or a related edition, not merit rejection; N = outside this bounded question. Short labels are navigation aids, not authoritative bibliography records. E positions identify additional exact/expanded identities not already in N1/N2; G positions enumerate graph citers. Related publications/preprints and deposits remain identifiable without being counted as independent replications.

| Position | DOI | Status and short label |
| --- | --- | --- |
| N1:1 | `10.1007/s10339-016-0788-z` | N — Talim weaving |
| N1:2 | `10.1016/j.jvlc.2006.04.003` | D — Beyond the notation |
| N1:3 | `10.1145/3148456.3148474` | D — MoLICC notation |
| N1:4 | `10.13140/rg.2.1.3449.0485` | D — Visualization dimensions deposit |
| N1:5 | `10.1145/3148456.3148507` | D — Visualization dimensions publication |
| N1:6 | `10.1145/1597849.1384321` | D — CD questionnaire and algorithms |
| N1:7 | `10.1017/cbo9780511600821.009` | D — Visual-programming case |
| N1:8 | `10.5753/ihc.2019.8375` | D — HCI evaluation using CD |
| N1:9 | `10.1007/978-3-540-69554-7_9` | D — Formalizing CD |
| N1:10 | `10.1016/b978-155860808-5/50005-8` | D — Notational systems chapter |
| N1:11 | `10.1006/jvlc.1996.0009` | C — Green and Petre CD |
| N1:12 | `10.1109/vlhcc.2018.8506483` | D — Blocks editor analysis |
| N1:13 | `10.1016/j.jvlc.2006.04.004` | D — CD achievements and questions |
| N1:14 | `10.1109/hcc.2001.995253` | D — AutoHAN |
| N1:15 | `10.17011/ht/urn.200804151351` | D — UML and CD |
| N1:16 | `10.7551/mitpress/13770.003.0008` | D — Live-coding notation chapter |
| N1:17 | `10.1109/vlhcc.2014.6883033` | D — Social robot API study |
| N1:18 | `10.1007/s11412-016-9236-4` | N — Collaborative learning |
| N1:19 | `10.22215/etd/2017-11747` | N — Place-name atlas |
| N1:20 | `10.1007/978-3-319-18425-8_3` | D — Domestic-IoT notation |
| N1:21 | `10.1007/978-94-017-3524-7_6` | D — Cognitive factors in diagrams |
| N1:22 | `10.1145/568760.568861` | D — CD and Z formalism |
| N1:23 | `10.1145/3544548.3580693` | N — Microgesture glyphs |
| N1:24 | `10.14236/ewic/eva2016.8` | D — Live-coding notation/performance |
| N1:25 | `10.1002/spe.3435` | C — Reactive API mixed evaluation |
| N1:26 | `10.1145/2851581.2886434` | D — Programming-language usability |
| N1:27 | `10.17771/pucrio.acad.27060` | D — Communicative dimensions thesis |
| N1:28 | `10.1145/1391469.1391474` | D — Parallel programming |
| N1:29 | `10.1007/s10270-014-0447-8` | D — WebML notation |
| N1:30 | `10.3390/su10093238` | N — Consumer sustainability |
| N1:31 | `10.22152/programming-journal.org/2023/7/13` | C — Technical dimensions |
| N1:32 | `10.1016/j.jvlc.2016.07.005` | D — Appropriate API abstraction |
| N1:33 | `10.1109/mc.2017.3001257` | D — PL research methodology |
| N1:34 | `10.48550/arxiv.2011.07565` | D — User-centered PL course |
| N1:35 | `10.1109/hcc.2002.1046334` | D — Attention-investment model |
| N1:36 | `10.1017/s1537592724002676` | N — International-relations judgements |
| N1:37 | `10.1016/j.ijhcs.2019.06.009` | D — Psychology of programming review |
| N1:38 | `10.1007/s13173-010-0017-z` | D — Nested context language |
| N1:39 | `10.1007/978-3-319-58460-7_11` | D — Security API CD |
| N1:40 | `10.17011/ht/urn.200804151349` | D — Psychology of programming introduction |
| N2:1 | `10.5220/0002998400780085` | D — Distributed-architecture propagation |
| N2:2 | `10.1017/dsd.2020.17` | D — Modularity and robustness simulations |
| N2:3 | `10.33915/etd.1721` | D — Architecture metric tool thesis |
| N2:4 | `10.1016/j.jss.2012.05.085` | D — Evolvability analysis |
| N2:5 | `10.1109/aswec.2009.31` | D — Domain-information propagation |
| N2:6 | `10.1016/j.jss.2021.110947` | D — Risk containers |
| N2:7 | `10.1109/ms.2022.3213880` | D — Infrastructure-as-code conformance |
| N2:8 | `10.1109/scc.2013.101` | D — Business process/SOA alignment |
| N2:9 | `10.1115/detc2018-86049` | N — Dynamic engineering-system propagation |
| N2:10 | `10.1504/ijmassc.2010.036800` | N — Product and organization propagation |
| N2:11 | `10.3990/1.9789036531757` | D — Requirements-architecture traceability |
| N2:12 | `10.1142/s021952591250083x` | D — Modularity dependence and change |
| N2:13 | `10.1145/243327.243624` | D — Unified event-based architecture |
| N2:14 | `10.12681/eadd/20666` | D — Architecture improvement thesis |
| N2:15 | `10.1155/2014/237243` | D — Network-based software propagation |
| N2:16 | `10.1155/2019/9414162` | D — Software stability simulation |
| N2:17 | `10.1007/s00163-022-00395-y` | D — Engineering propagation concepts |
| N2:18 | `10.1504/ijde.2011.045276` | N — Engineering parameter coupling |
| N2:19 | `10.1007/978-3-030-58617-1_6` | D — Architecture/model co-evolution |
| N2:20 | `10.1115/1.3149847` | N — Complex technical systems |
| N2:21 | `10.17771/pucrio.acad.26957` | D — Feature dependencies thesis |
| N2:22 | `10.1177/1063293x14553809` | N — Product-design scheduling |
| N2:23 | `10.1109/mise.2012.6226021` | D — Business/architecture co-evolution |
| N2:24 | `10.22215/etd/2019-13518` | D — Software/performance model propagation |
| N2:25 | `10.1115/detc2010-28773` | D — OO change-scope estimation |
| N2:26 | `10.3233/atde200093` | N — Product realization |
| N2:27 | `10.2139/ssrn.4693779` | D — Architecture smell evolution |
| N2:28 | `10.1109/access.2022.3149001` | N — Mechanical-product path optimization |
| N2:29 | `10.1002/sys.21686` | D — Modularity and software robustness |
| N2:30 | `10.48550/arxiv.2603.00601` | C — Theory of Code Space |
| N2:31 | `10.1002/sys.21400` | N — Product-design risk paths |
| N2:32 | `10.1007/978-3-030-45231-5_10` | N — Learning with delta lenses |
| N2:33 | `10.21236/ada407778` | D — Architecture quality tactics |
| N2:34 | `10.1155/2022/1994257` | N — Product module propagation |
| N2:35 | `10.4067/s0718-27242009000100006` | N — Product networks and sourcing |
| N2:36 | `10.1109/sbcars.2010.12` | D — Use-case modularity conference |
| N2:37 | `10.1504/ijwet.2016.081768` | D — Web architecture controlled experiment |
| N2:38 | `10.1108/ecam-08-2020-0615` | N — Digital twin engineering changes |
| N2:39 | `10.1016/j.jss.2011.11.1025` | D — Use-case modularity journal |
| N2:40 | `10.1109/csmr.2010.45` | D — Dependency-injection smells |
| E:1 | `10.1145/3609025.3609478` | D — Functional Shell GUI Easy |
| E:2 | `10.1145/2577080.2577083` | D — REScala language paper |
| E:3 | `10.1109/tse.2017.2655524` | C — Reactive comprehension study |
| E:4 | `10.1145/361598.361623` | D — Parnas decomposition |
| E:5 | `10.1145/3759163.3760429` | D — Functional UI evolution |
| E:6 | `10.1145/3643757` | C — CodePlan publication |
| E:7 | `10.48550/arxiv.2309.12499` | D — CodePlan preprint |
| E:8 | `10.48550/arxiv.2302.10003` | D — Technical dimensions preprint |
| G:1 | `10.48550/arxiv.2510.26579` | D — Bayesian inference debugging |
| G:2 | `10.1145/3191697.3214337` | D — REScala programming experience |
| G:3 | `10.1145/3328433.3328446` | N — Privacy-enhancing language support |
| G:4 | `10.1145/3360570` | D — Fault-tolerant interactive applications |
| G:5 | `10.1145/3387904.3389257` | D — Unified configuration access |
| G:6 | `10.1007/s10664-021-09938-8` | D — Large-scale structure and flows |
| G:7 | `10.24251/hicss.2019.864` | N — Security vulnerability detection |
| G:8 | `10.22152/programming-journal.org/2020/4/17` | D — Distributed language implementation |
| G:9 | `10.1109/tse.2018.2833109` | D — Distributed reactive consistency |
| G:10 | `10.1109/icse.2019.00102` | D — Production performance feedback |
| G:11 | `10.22152/programming-journal.org/2022/6/14` | D — Topology-level reactivity |
| G:12 | `10.1145/3328905.3332465` | D — Multitier distributed development |
| G:13 | `10.48550/arxiv.2110.15246` | C — Readability-metric counterpoint |
| G:14 | `10.1145/3524842.3527966` | D — Reactive API usage mining |
| G:15 | `10.1109/icse48619.2023.00058` | C — Loops/streams debugger experiment |
| G:16 | `10.22152/programming-journal.org/2021/5/4` | N — Reactive Wi-Fi firmware |
| G:17 | `10.1109/supercompcloud51944.2020.00010` | N — Reactive HPC cloud |
| G:18 | `10.1145/3510003.3519016` | D — Imperative/declarative collections |
| G:19 | `10.1109/ase.2019.00082` | D — Automated reactive refactoring |
| G:20 | `10.1109/icpc.2019.00047` | D — Hierarchical software comprehension |

The 108 DOI rows comprise 8 C, 78 D (including the two explicit related-edition records), and 22 N. Exact deferred reasons were retained in the service record. Among known metadata hazards: acknowledgements appeared in the abstracts for the communicative-dimensions thesis and use-case modularity entries; potential conference/journal/deposit relationships remain unverified. Do not build conclusions on those malformed abstracts. An open-access flag is not proof that a readable matching body was obtained.

## Recorded decision verification

One `report_citations` call recorded the complete set under:

```text
answer_id: alf-nu-form-factors-discovery-20260914
```

The service accepted **12 cited / 103 excluded / 0 skipped**. This combines the eight C DOI records with four credited practitioner sources. It does not mean twelve empirical studies support the hypothesis.

The subsequent `citation_report` returned:

```text
screened: 115
included: 12
excluded: 103
excluded_by_reason:
  out_of_scope: 22
  deferred: 77
  related_edition: 2
  not_empirical_evidence: 1
  access_limited: 1
by_stage: title_abstract 108; full_text 7
by_source: scite_mcp 108; web_search 6; other 1
truncated: false
excluded_without_reason: 0
included_without_reason: 0
retrieval_unlinked: false
answer-scoped retrieved: null
```

The seven `full_text` stage records are the three selected scholarly text inspections and four practitioner texts, including a derived archive. They are not seven papers read completely. The publisher-author routes for DOI verification remain documented above even when discovery provenance is scite. The report is a source-decision audit, not certification of systematic-review completeness, novelty or causal evidence.

## Bounded consequence

Preserve the eleven core full-PDF targets and add P12 ToCS and P13 CodePlan as close-predecessor reconstructions. Their questions and the conditional mechanism papers are in the companion note; do not promote the remaining inventory into a mandatory download list. The next full reader should reconstruct methods and implications, then revise the proposal from evidence. No new experiment, renderer, runtime wrapper, scorer or model allocation is created by this discovery pass.
