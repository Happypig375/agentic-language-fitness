# Source audit: selection evidence closure

**Date:** 2026-09-15. **Base:** `f1bea15451d14b1027c356e0b2830acd85a86aa6`.

Companions: [review](selection-evidence-closure-2026-09-15.md), [proposal](architecture-maintenance-research-proposal-2026-09-15.md), [priority DOI queue](literature/selection-priority-reading-2026-09-15.md).

This is a bounded continued source/method review, not systematic coverage, a new complete-PDF reading batch, independent human review or reproduction. Prior P01–P13/A01–A03 reconstructions are reused at their recorded extent; their coverage and Zotero records are unchanged. Sixty-five literal DOI identifiers below are not sixty-five studies read or independent experiments.

## Decision and retrieval

The question is whether direct recommendation and general selection literature already supply the proposed contribution, and which controls are needed for useful, scientifically valid architectural advice. Retrieval distinguishes target-program choice from agent-system, model, healthcare and runtime-service architecture.

Every Scite literature request used **limit 20**. Exact lookups naturally returned fewer. No date, publication-type or citation-tally filters were imposed. Relevance ordering was used.

| Call | Selection | Offset | Returned / reported total |
| --- | --- | --- | --- |
| Q0 | Narrow recommendation query below | 0 | 1 / 1 |
| K1 | Five exact DOIs: MicroRec, pattern suggestions, JSS review, Rice and an incorrectly guessed ASlib identity | 0 | 5 / 5 |
| Q1 | Broader architecture/microservice query below | 0 | 20 / 1,580 |
| Q1p2 | Same query | 20 | 20 / 1,580 |
| K2 | Correct ASlib journal/preprint identities, meta-level selection and Kotthoff survey | 0 | 4 / 4 |

```text
Q0:
("microservice recommendation" OR "architecture pattern recommendation" OR
 "software architecture selection") AND
("large language model" OR LLM OR "generative AI")

Q1:
("software architecture" OR microservice) AND
(recommendation OR selection) AND
("large language model" OR LLM)
```

Q0's narrow wording missed known direct papers, which were recovered by exact identity and primary routes. Q1 remained noisy; positions 41–1,580 are unexamined. Forty returned titles/excerpts do not establish absence of a duplicate, and exhausting the one-record Q0 does not mean field saturation. These searches plus K1/K2 yield 50 literal identifiers. The correctly excluded wrong identifier remains in the audit rather than disappearing from provenance.

Web discovery used exact-title/DOI queries for MicroRec, architecture-pattern suggestions, Rice/ASlib, algorithm-selection evaluation and the failure-aware paper. Primary publisher, conference, arXiv, institutional and author-repository routes were followed. Search-only mirrors, podcasts, scraped reviews and unrelated similarly named papers were not used as method evidence. Deep Research plugin discovery returned no matching plugin in this turn; no separate Deep Research job or outside model worker ran.

## What was actually inspected

| Work / source | Actual evidence | Limits / consequence |
| --- | --- | --- |
| MicroRec `10.1145/3643991.3644916` | [Official MSR 2024 abstract](https://2024.msrconf.org/details/msr-2024-technical-papers/21/MicroRec-Leveraging-Large-Language-Models-for-Microservice-Recommendation), authors/title and discovery/ranking target | ACM full-text route returned 403/error. Ranking metrics in the abstract do not become maintenance effects; detailed candidate-set, relevance and downstream methods remain unread. Unrelated FPGA MicroRec is not this work. |
| Pattern suggestions `10.1007/978-3-031-66336-9_19` | [Publisher abstract and notes](https://link.springer.com/chapter/10.1007/978-3-031-66336-9_19), author institutional abstract, linked author result artifact | Scite `read_fulltext` offset 0/length 8,000 returned 0 characters and `contentDenied=true`. No full chapter or training-split verification. |
| Pattern author artifact | `JoelLV/Software_Architecture_Gen`, complete tree inventory and `Results.md` through GitHub connector; tree SHA `97a0ee66b8e6e9acccd72304ec9bc0ec0d2a21e7`, result blob `6e4b0b1dd2135453f81c84523371a61617106402` (19,634 bytes) | Ten textual expected/actual pattern examples inspected. Test 2 is multi-label; Test 3 input includes an SOA explanation while expected label is Microservices. These are observable artifact ambiguities, not a reproduced scoring rule, proof of experimental invalidity or proof about the complete paper. Readback confirmed the same blob. No author scripts/models executed. |
| ASlib journal `10.1016/j.artint.2016.04.003`; preprint `10.48550/arXiv.1506.02465` | Publisher identity, [arXiv history](https://arxiv.org/abs/1506.02465), and [v3 parsed PDF](https://arxiv.org/pdf/1506.02465v3), especially definition 1 (PDF page 4), sections 6.2–6.3 (pages 20–21), and selected text about scenario selection | v3 is 6 April 2016, 36 PDF pages, accepted preprint. Selected text only, not complete or visually verified. Screenshot attempts on unversioned pages 20/21 returned internal errors; pinned-v3 pages 4/20 returned cache-miss errors. No successful render, local PDF or hash acquired. Publisher/preprint are related editions, not two experiments. |
| Meta-level selection `10.1007/s10994-022-06161-4` | [Primary open HTML](https://link.springer.com/article/10.1007/s10994-022-06161-4), sections 2 and 6.1 plus neighboring definition/validation passages | Expected stochastic performance, single-best/virtual-best, feature costs and evaluation conventions inspected. Not a complete article/PDF read; no figure/result reanalysis or ensemble implementation. |
| Failure-aware enhancements `10.48550/arXiv.2602.02896` | [Primary v1 HTML](https://arxiv.org/html/2602.02896v1), sections III, V and VI, with surrounding results read to locate the claims; [version history](https://arxiv.org/abs/2602.02896) | Primary history shows v1 dated 2 February 2026; no later edition was verified. Selected methods explicitly use manual inspection without execution. Full PDF and linked Zenodo artifact `10.5281/zenodo.17637008` not reconstructed. No numerical result, diagnosis reliability or policy effect is independently reproduced. |
| GenAI architecture review `10.1016/j.jss.2025.112607` | [Publisher-visible related-work excerpt](https://www.sciencedirect.com/science/article/abs/pii/S0164121225002766) and exact identity | Supports the primary-study trail, not current comprehensive novelty. Earlier selected preprint reading remains separate; publisher body not newly read in full. |
| Product-development recommendation `10.1017/pds.2025.10100` | [Primary Cambridge HTML](https://doi.org/10.1017/pds.2025.10100), selected sections 2.2–2.4 and 4.3 | Distinguishes judged applicability from exact algorithm matches and records untested source validity/output variability. No new complete PDF, numerical table/figure verification or executable recommendation trial by this reviewer. |
| Rice `10.1016/S0065-2458(08)60520-3`; Kotthoff `10.1609/aimag.v35i3.2460` | Exact metadata; Rice's [Purdue earlier report record](https://docs.lib.purdue.edu/cstech/99/) and later primary selection citations | Original chapter/survey not read. The 1975 report is not automatically the same as the 1976 chapter; history leads only. |

The PDF skill was consulted before ASlib inspection. Render failures are not counted as visual coverage. The theoretical/noise examples in the new proposal were checked by local enumeration and arithmetic; they are original reasoning under explicit assumptions, not empirical results from ASlib or ALF.

A raw public-repository byte download into the working container failed DNS resolution. GitHub connector reads/writes remained available. No full checkout test, author experiment, provider request or runtime baseline is claimed.

## Citation graph

G1: seeds MicroRec and the pattern-suggestion DOI, incoming direction, depth 1, maximum 20 edges, intents and snippets enabled. It returned **16 edges / 18 nodes**, `truncated=false`, seed coverage **9 / 7**, with no low-coverage flag. Of the 16 citing identifiers, the JSS review was already in K1; the remaining 15 bring the union to **65**.

`s` is the citing source and `t` the cited work. The only substantive returned snippet is the product-development paper's motivation paragraph; most edges are title/metadata only. Untruncated retrieval in this index does not establish all citations or full field coverage. No supporting/contrasting label is treated as a quality vote. CIAO's preprint/publisher relationship and PodGPT's versions are possible lineages, not counted as independent replications.

## Identity and chronology safeguards

The initial guessed `10.1016/j.artint.2015.08.003` resolves to **Modelling structured societies: A multi-relational approach to context permeability**, not ASlib. The correct ASlib journal identity was independently resolved as `10.1016/j.artint.2016.04.003`. No claim or library addition uses the incorrect ID as ASlib.

Q1:40 has apparently incompatible title/excerpt content and remains quarantined. Q1:8 reports December 2026 metadata, after this September 15 review. Without verified earlier online availability it is a deferred lead, not evidence of a present competing publication. Placeholder dates, title collisions and incomplete author lists are not silently normalized into facts.

## Complete decision inventory

C = credited for the bounded claim above; D = deferred/not newly assessed; N = outside this question; I = incorrect or unresolved identity/excerpt pairing. D is not rejection on merit. The inventory has **8 C / 25 D / 30 N / 2 I**. It contains versions and reused metadata, not 65 independent studies.

| DOI | Retrieval | Decision | Scope / reason |
| --- | --- | --- | --- |
| `10.3390/software4010006` | Q0:1 | D | Microservice-design survey, excerpts only; primary route rate-limited. |
| `10.1016/S0065-2458(08)60520-3` | K1 | D | Foundational identity, original body unread. |
| `10.1016/j.artint.2015.08.003` | K1 | I | Wrong ASlib guess; resolved to a different article. |
| `10.1145/3643991.3644916` | K1/G1 seed | C | Official discovery/ranking abstract; body unavailable. |
| `10.1007/978-3-031-66336-9_19` | K1/G1 seed | C | Publisher abstract and author result artifact, not full paper. |
| `10.1016/j.jss.2025.112607` | K1/G1 | C | Limited publisher related-work trail. |
| `10.48550/arXiv.2607.05055` | Q1:1 | N | Healthcare agent framework. |
| `10.48550/arXiv.2604.08567` | Q1:2 | N | Multi-user agent policy. |
| `10.3390/app16147197` | Q1:3 | N | E-government transparency application. |
| `10.1101/2024.07.11.24310304` | Q1:4 | N | PodGPT preprint, different target. |
| `10.48550/arXiv.2510.22787` | Q1:5 | D | C4 design automation, methods unread. |
| `10.48550/arXiv.2603.17833` | Q1:6 | D | ArchBench earlier evidence retained, not newly read. |
| `10.1038/s44385-025-00022-0` | Q1:7 | N | PodGPT publication, not independent maintenance evidence. |
| `10.1016/j.mex.2026.104113` | Q1:8 | D | Relevant mapping title, future-dated metadata unresolved. |
| `10.48550/arXiv.2604.16359` | Q1:9 | N | Log-analysis review. |
| `10.48550/arXiv.2606.18976` | Q1:10 | D | CAPRA architecture-output evaluation. |
| `10.3390/s25092696` | Q1:11 | N | Logistics application. |
| `10.48550/arXiv.2511.07458` | Q1:12 | N | Log evaluation. |
| `10.48550/arXiv.2602.10479` | Q1:13 | N | Agent-system architecture. |
| `10.48550/arXiv.2602.02896` | Q1:14 | C | Selected primary enhancement/decision methods. |
| `10.48550/arXiv.2601.13007` | Q1:15 | D | Architecture recovery. |
| `10.3390/s25164911` | Q1:16 | N | Energy application. |
| `10.48550/arXiv.2604.08293` | Q1:17 | D | CIAO documentation, possible related published edition below. |
| `10.3390/software3040029` | Q1:18 | N | Dental application. |
| `10.1055/a-2851-0739` | Q1:19 | N | Clinical notes. |
| `10.48550/arXiv.2603.07091` | Q1:20 | D | Architectural task/model reasoning, unread. |
| `10.48550/arXiv.2603.23698` | Q1:21 | D | Architecture-derived penetration tests. |
| `10.5121/csit.2023.132403` | Q1:22 | N | Smart-service dialogue. |
| `10.48550/arXiv.2603.09004` | Q1:23 | D | Microservice generation/context. |
| `10.1002/mgea.70075` | Q1:24 | N | Materials application. |
| `10.48550/arXiv.2511.01166` | Q1:25 | D | Runtime microservice remediation. |
| `10.1016/j.mcpdig.2025.100196` | Q1:26 | N | Healthcare. |
| `10.20944/preprints202407.0049.v1` | Q1:27 | N | Interview training. |
| `10.48550/arXiv.2603.22603` | Q1:28 | N | Cloud threat models. |
| `10.48550/arXiv.2602.13266` | Q1:29 | N | Prompt storage. |
| `10.1002/eng2.70437` | Q1:30 | N | Manufacturing requirements. |
| `10.3390/math14060950` | Q1:31 | N | Customer-query service matching. |
| `10.3390/software5010010` | Q1:32 | N | Privacy application. |
| `10.1088/2631-8695/ae94e7` | Q1:33 | N | Model consensus/orchestration. |
| `10.3390/cmsf2026013016` | Q1:34 | N | Neurosymbolic agent architecture. |
| `10.48550/arXiv.2512.20586` | Q1:35 | N | Radiosurgery. |
| `10.1016/j.esmorw.2026.100726` | Q1:36 | N | Oncology RAG. |
| `10.33612/diss.833424077` | Q1:37 | D | Architecture-erosion dissertation. |
| `10.48550/arXiv.2510.27190` | Q1:38 | N | Agent trust/security. |
| `10.17770/etr2024vol2.8060` | Q1:39 | N | Tourism chatbot. |
| `10.15276/ict.01.2024.17` | Q1:40 | I | Apparent title/excerpt mismatch. |
| `10.1016/j.artint.2016.04.003` | K2 | C | Correct ASlib publisher identity. |
| `10.48550/arXiv.1506.02465` | K2 | C | Same work's v3, selected parsed sections only. |
| `10.1007/s10994-022-06161-4` | K2 | C | Selected primary definitions/evaluation methods. |
| `10.1609/aimag.v35i3.2460` | K2 | D | Algorithm-selection survey metadata. |
| `10.1007/978-3-032-24216-7_4` | G1 | D | Architecture-document evaluation. |
| `10.1109/icsa66085.2026.00026` | G1 | D | CIAO publication identity, lineage not counted independently. |
| `10.1109/icsa66085.2026.00031` | G1 | D | Architecture-view generation. |
| `10.1109/icaiqsa64000.2024.10882424` | G1 | N | GenAI deployment architecture. |
| `10.1109/icsa-c65153.2025.00049` | G1 | D | Design from informal specifications. |
| `10.1007/978-981-96-7238-7_17` | G1 | D | Software-development survey. |
| `10.1007/978-3-032-02138-0_5` | G1 | D | Source-based architecture recovery. |
| `10.1002/spe.70022` | G1 | N | Developer-task recommendations. |
| `10.1145/3686803` | G1 | D | Self-adaptive systems roadmap. |
| `10.1109/eei70303.2026.11640661` | G1 | N | Compute/network routing. |
| `10.1017/pds.2025.10100` | G1 | C | Selected primary recommendation criteria and limits. |
| `10.5753/sbcars.2025.14592` | G1 | D | Microservice clustering. |
| `10.1007/s11432-025-4670-0` | G1 | D | Software-engineering LLM survey. |
| `10.1109/tsc.2026.3679374` | G1 | D | Runtime orchestration monitoring. |
| `10.3390/fi17120543` | G1 | D | QoS service-selection review. |

## Decision-service verification

The complete 65-identifier set was sent once to `report_citations` under:

```text
alf-selection-evidence-closure-20260915-f1bea
```

It accepted **8 cited / 57 excluded / 0 skipped**. The inspected `citation_report` returned:

```text
screened: 65
included: 8
excluded: 57
excluded_by_reason: deferred 25; out_of_scope 30; identity_mismatch 2
by_stage: title_abstract 61; full_text 4
truncated: false
included_without_reason: 0
excluded_without_reason: 0
retrieval_unlinked: false
answer-scoped retrieved: null
```

All DOI discovery provenance is `scite_mcp`; primary follow-through is listed above. `full_text` denotes selected body sections, not a completed PDF. A publisher/preprint pair is not two independent studies. Service acceptance is not evidence of novelty, systematic review, author-method validity or full access. The local inventory counted 65 unique literal IDs and reconciled the decision/stage totals.

## Remaining uncertainty and useful endpoint

The current source pass resolves the reported objects of the direct recommendation leads and adds missing selection-method prior art. It does not demonstrate absence of an equivalent study or validate a new Nu experiment. The next complete readings are finite and decision-linked. Inaccessible methods stay inaccessible; history-only or unrelated discoveries do not force another full bibliography sweep.

The actual improvement is in the claim and test: distinguish empirical architectural-information value from generic selection, label agreement, lucky-run maxima and uncharged advice. Preserve the earlier evidence, compare meaningful alternatives and return for human A0 disposition before any construction or candidate spending.
