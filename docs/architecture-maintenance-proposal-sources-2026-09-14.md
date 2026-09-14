# Research proposal: source and search ledger

Date: **2026-09-14 HKT**. ALF base:
`4757a6c5cbbd0f764f9c39b596c5517cc024f48b`.
Companion: [standalone research proposal](architecture-maintenance-research-proposal-2026-09-14.md).
This is bounded scoping research, not a systematic review, saturation claim,
peer-review certificate or adopted experiment. Counts below describe retrieval
positions and identifiers, not independent studies or full papers read.

The sections through the initial publication checks below describe the original
proposal published at `0df55a45b5087a9420807617ea165c01c873f779`. The appended
follow-up records the revised proposal's background, architecture-lineage,
metadata and pagination work. Initial citation decisions stay historical.

## Evidence used and reading extent

| Source / DOI | Primary edition and actual reading | Contribution and limitation |
| --- | --- | --- |
| CodeThread, `10.48550/arXiv.2606.21804` | [v1](https://arxiv.org/html/2606.21804v1); Scite metadata refreshed. Prior primary introduction and §§3.1–3.3 retained. | Downstream human/agent predecessor comparison is already prior art. Existing-test success is not complete behavioral equivalence. |
| Needle in the Repo, `10.48550/arXiv.2603.27745` | [v1](https://arxiv.org/html/2603.27745v1); Scite metadata refreshed. Prior starter-shaping, dual-oracle and motivating-example reading retained. | Supplied architectural probes are not new; structural compliance differs from demonstrating downstream benefits of either credible alternative. |
| SlopCodeBench, `10.48550/arXiv.2603.24755` | [v2](https://arxiv.org/html/2603.24755v2); Scite metadata refreshed. Prior inherited-state/fresh-conversation and cost analysis retained. | Evolution and next-checkpoint costs are not novel contributions of this proposal. Do not mix versions. |
| Xu, Yang and Chen, SWE-Refactor, `10.48550/arXiv.2602.03712` | [v1](https://arxiv.org/html/2602.03712v1), 3 February 2026. Primary abstract and §3.2 task/verification methods read this turn. | Developer refactorings in Java repositories, compilation/tests and transformation metrics. Not an experiment on later changes to assigned architectural packages. Preprint. |
| Lin et al., SmellBench, `10.48550/arXiv.2606.05574` | [v1](https://arxiv.org/html/2606.05574v1), 4 June 2026. Introduction, §3.3 evaluation, selected cross-file passages and limitations read. | Injected Python smells and fine-grained repair assessment, including LLM quality judging. Refactoring-quality targets do not establish future maintenance savings. Preprint. |
| Dinu, Mihăescu and Rebedea, SmellBench, `10.48550/arXiv.2605.07001` | [v2](https://arxiv.org/html/2605.07001v2), 12 May 2026; primary abstract, §§3.2, 5.1 and construct-validity passages read. Discovered through Lin's bibliography, then exact Scite lookup. | Architectural-smell repair and false-positive judgments. Authors explicitly warn that tool disappearance need not mean genuine improvement; native CLI differences confound isolated-model interpretation. **Different work from Lin et al.**, not another edition. Preprint. |
| Sambu et al., `10.1109/ICSA66085.2026.00033` | [ICSA conference abstract](https://conf.researchr.org/details/icsa-2026/icsa-2026-papers/27/LLMs-for-Architectural-Refactoring-An-Exploratory-study-on-Monoliths-to-Microservice), proceedings pp. 268–279. Scite body unavailable; attachment click returned the same page. | Abstract describes seven summarization strategies, four LLMs and six architectural metrics on four systems. This qualifies the gap; no full-methods exclusion of downstream outcomes is claimed. Lab-news performance figures are not combined with the abstract. |
| Knoble and Popa, *Functional Shell and Reusable Components for Easy GUIs*, `10.1145/3609025.3609478` | FUNARCH 2023, pp. 20–28; [author PDF](https://defn.io/papers/fungui-funarch23.pdf), [proceedings](https://sigplan.org/OpenTOC/funarch23.html). Scite served actual body: offsets 0–7,000, 7,000–14,000 and 14,000–22,000 of 33,976 characters in this session. | Introduction, design/use and experience through §5.2 and part of §5.3 read, **not the whole paper**. Racket functional views, ownership/callback organization and imperative GUI integration are architectural experience evidence, not controlled maintenance effects. Related arXiv 2308.16024 is the same work. |
| Bengtsson et al., ALMA, `10.1016/S0164-1212(03)00080-3` | [Author PDF](https://www.cs.vu.nl/~hans/publications/y2004/alma.pdf), 2004. Scite metadata refreshed; prior §§4.1–4.6 and §8 reading retained. | Scenario elicitation, analysis goals and impact assessment motivate the proposed chain design. Predicted impact and measured agent behavior remain different evidence. |
| Fowler, MVU, `10.4230/LIPIcs.ECOOP.2020.14` | [Proceedings paper](https://doi.org/10.4230/LIPIcs.ECOOP.2020.14), 2020. Scite metadata refreshed; prior selected formal-model reading retained. | Formal architectural lineage, not proof of Nu implementation properties or maintenance benefits. |

Earlier selected primary readings are reproducibly located in the
[Nu-methodology ledger](nu-grounded-maintenance-sources-2026-09-14.md) and
[frontier ledger](research-frontier-gap-sources-2026-09-14.md). They are reused
evidence, not counted as newly read full papers. The further reused sources are:

| DOI identity | Source / prior reading | Use |
| --- | --- | --- |
| `10.1007/s10664-008-9102-8` | [Runeson and Höst](https://doi.org/10.1007/s10664-008-9102-8), online 2008 / issue 2009; selected publisher §§2.1–2.5 and §§3.1–3.3 | Purposeful case design, units and triangulation, not a requirement for randomly sampled architects. |
| `10.1007/s10664-021-10072-8`; `10.48550/arXiv.2002.07764` | [Baltes and Ralph v6](https://arxiv.org/html/2002.07764v6), 20 October 2021, related journal 2022; introduction, §§2.1.1–2.1.3 and §6.2 | Sampling limits. The journal/preprint are one work. Prior Scite misassociated abstract remains rejected; primary text is the evidence. |
| `10.1109/TSE.2014.2372785` | [Barr et al.](https://doi.org/10.1109/TSE.2014.2372785), IEEE TSE 2015; author/institutional abstract and indexed front matter only | Oracle distinction; application to outside-LLM scoring is our inference, not a result from that survey. |
| `10.1117/12.3020480`; `10.48550/arXiv.2407.07207` | Thompson et al., *Real-time adaptive optics control with a high level programming language*, [v1](https://arxiv.org/html/2407.07207v1), selected §§2.4–2.5 previously read | User-corrected identity. State machines, messages and Dear ImGui coexist; evidence against a false binary, not a maintenance comparison. Proceedings and preprint identifiers are not independent replications. |

No whole-engine superiority, human-to-model expertise equivalence, model ranking
or causal effect of F# syntax is inferred from these sources. The primary papers
are credited only for the selected claims. Scite supporting/contrasting labels
are not votes establishing the proposed hypothesis.

## New Scite search record

No date, citation-count, language or publication-type filters. Relevance order.
P1/P2 requested 25 but the service returned an effective limit of 20; continuation
used **offset 20**, not 25. P2/P2b cover the first 40 positions; P4/P4b cover all
35 positions returned for that exact query. This does not establish coverage of
the field. P1 and P3 were noisy and were reformulated, not treated as absence.

| ID | Exact query or DOI selection | Offset; requested/effective limit; returned / reported total |
| --- | --- | --- |
| P0 | DOIs: `10.48550/arXiv.2606.21804`, `10.48550/arXiv.2603.27745`, `10.48550/arXiv.2603.24755`, `10.1016/S0164-1212(03)00080-3`, `10.4230/LIPIcs.ECOOP.2020.14`, `10.1145/361598.361623` | 0; 10/10; 6/6 |
| P1 | `("coding agent" OR "large language model") AND (architecture OR "design pattern" OR "state ownership") AND (maintenance OR evolution OR downstream)` | 0; 25/20; 20/37647 |
| P2 | `("code maintainability" OR "software maintenance") AND (experiment OR intervention OR refactoring) AND ("large language model" OR "coding agents")` | 0; 25/20; 20/440 |
| P2b | Same exact term as P2 | 20; 20/20; 20/440 |
| P3 | `("model-view-update" OR "immediate mode" OR "functional core") AND (maintainability OR experiment OR evaluation)` | 0; 20/20; 20/10157 |
| P4 | `"architectural refactoring" AND (LLM OR "large language models")` | 0; 20/20; 20/35 |
| P4b | Same exact term as P4 | 20; 20/20; 15/35 |
| P5 | `"functional core" AND "imperative shell"` | 0; 20/20; 4/4 |
| P6 | DOIs: `10.48550/arXiv.2605.07001`, `10.1002/iis2.70208`, `10.5281/zenodo.18622108` | default 0; 5/5; 3/3 |

Citation-graph check PG1: seeds `10.48550/arXiv.2606.21804` and
`10.48550/arXiv.2603.27745`, direction `in`, depth 1, maximum 40 edges,
intent included. Returned **0 edges / 2 seed nodes**, not truncated; both seeds
flagged low coverage. Keyword and primary-bibliography follow-up were used;
zero coverage is not evidence that no follow-on work exists.

Other access outcomes: Parnas `10.1145/361598.361623` returned only an 843-character
fallback abstract, not body text, and is not an additional cited anchor.
`10.1002/iis2.70208` still lacked a title/abstract on exact retry; its relevance
is unresolved. Zenodo `10.5281/zenodo.18622107` / `18622108` share ICSA title and
author metadata; no independent study is counted and their exact deposit
relationship is not assumed. Opening the latter deposit failed. No access
failure is classified as proof of irrelevance or absence.

Web search strings were `"Functional Shell and Reusable Components for Easy GUIs"`,
`"LLMs for Architectural Refactoring" "Monoliths"`, and
`"SWE-Refactor" "SmellBench"`; the last combined query was not useful.
Exact primary arXiv pages and conference links then supplied the methods above.
One search result was an ICSA showcase page, not this paper's research-paper
entry; the correct entry was opened separately. No secondary site is used for
technical findings. All new web endpoints are listed below, including discovery
duplicates; repeated opens/finds are not additional studies.

## DOI retrieval inventory

P0–P6 returned **128 positions / 123 distinct DOI identifiers**. Ten are credited
in the initial proposal, 113 are not credited. Six further DOI identifiers above reuse
prior verified sources. C means credited; E means not used in this bounded
proposal, **not necessarily rejected after full-methods review**. Particularly
relevant unread leads are identified explicitly. No five-result cutoff or
full-paper coverage is claimed. Normalized DOI case does not change identity.

| Query/rank | DOI | Retrieved title | Decision / reason |
| --- | --- | --- | --- |
| P0:1 | [10.48550/arxiv.2603.27745](https://doi.org/10.48550/arxiv.2603.27745) | Needle in the Repo: A Benchmark for Maintainability in AI-Generated Repository Edits | C — Needle v1: supplied starters and functional/structural oracles; selected methods reused, not a new full-paper reading. |
| P0:2 | [10.48550/arxiv.2603.24755](https://doi.org/10.48550/arxiv.2603.24755) | SlopCodeBench: Benchmarking How Coding Agents Degrade Over Long-Horizon Iterative Tasks | C — SlopCodeBench v2: inherited multi-episode implementation and checkpoint costs; prior primary review retained. |
| P0:3, P2:17 | [10.48550/arxiv.2606.21804](https://doi.org/10.48550/arxiv.2606.21804) | Is Agent Code Less Maintainable Than Human Code? | C — CodeThread v1: predecessor authorship and downstream maintenance; selected methods reused from the prior primary-source review. |
| P0:4 | [10.1016/s0164-1212(03)00080-3](https://doi.org/10.1016/s0164-1212(03)00080-3) | Architecture-level modifiability analysis (ALMA) | C — ALMA scenario/impact methods from previously read author-PDF sections; no measured agent effect implied. |
| P0:5 | [10.1145/361598.361623](https://doi.org/10.1145/361598.361623) | On the criteria to be used in decomposing systems into modules | E — Parnas modularization foundation; only fallback abstract read, not needed as an additional evidentiary anchor here. |
| P0:6 | [10.4230/lipics.ecoop.2020.14](https://doi.org/10.4230/lipics.ecoop.2020.14) | Model-View-Update-Communicate: Session Types Meet the Elm Architecture | C — MVU formalization: prior selected primary methods; not proof of MMCC maintenance superiority. |
| P1:1 | [10.36001/phmconf.2025.v17i1.4454](https://doi.org/10.36001/phmconf.2025.v17i1.4454) | Large Language Model Accelerated Maintenance Insights | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P1:2 | [10.33774/coe-2024-cdlwg](https://doi.org/10.33774/coe-2024-cdlwg) | Large Language Model for automobile | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P1:3 | [10.48550/arxiv.2602.06176](https://doi.org/10.48550/arxiv.2602.06176) | Large Language Model Reasoning Failures | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P1:4 | [10.48550/arxiv.2601.10194](https://doi.org/10.48550/arxiv.2601.10194) | Autonomous Quantum Simulation through Large Language Model Agents | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P1:5 | [10.1117/12.3092066](https://doi.org/10.1117/12.3092066) | Large language model-based code assistance | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P1:6 | [10.21203/rs.3.rs-5351103/v1](https://doi.org/10.21203/rs.3.rs-5351103/v1) | DNAHLM - DNA sequence and Human Language mixed large language Model | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P1:7 | [10.55041/ijsrem34001](https://doi.org/10.55041/ijsrem34001) | CHATBOT USING LARGE LANGUAGE MODEL | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P1:8 | [10.48550/arxiv.2604.16475](https://doi.org/10.48550/arxiv.2604.16475) | Spike-driven Large Language Model | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P1:9 | [10.34133/research.0655](https://doi.org/10.34133/research.0655) | Road of Large Language Model: Source, Challenge, and Future Perspectives | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P1:10 | [10.56801/rebicte.v9i.177](https://doi.org/10.56801/rebicte.v9i.177) | Large Language Model in SD-WAN Intelligent Operations and Maintenance | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P1:11 | [10.1117/12.3121410](https://doi.org/10.1117/12.3121410) | An intelligent maintenance decision-making method for power equipment based on multimodal large language model | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P1:12 | [10.48550/arxiv.2510.10161](https://doi.org/10.48550/arxiv.2510.10161) | Large Language Model Sourcing: A Survey | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P1:13 | [10.48550/arxiv.2602.16836](https://doi.org/10.48550/arxiv.2602.16836) | Claim Automation using Large Language Model | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P1:14, P2:11 | [10.48550/arxiv.2604.16359](https://doi.org/10.48550/arxiv.2604.16359) | LLM4Log: A Systematic Review of Large Language Model-based Log Analysis | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P1:15 | [10.1101/gr.278870.123](https://doi.org/10.1101/gr.278870.123) | CodonBERT large language model for mRNA vaccines | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P1:16 | [10.20944/preprints202402.1409.v1](https://doi.org/10.20944/preprints202402.1409.v1) | ArabianGPT: Native Arabic GPT-based Large Language Model | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P1:17 | [10.48550/arxiv.2607.05055](https://doi.org/10.48550/arxiv.2607.05055) | Toward Trustworthy Large Language Model Agents in Healthcare | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P1:18 | [10.48550/arxiv.2603.08801](https://doi.org/10.48550/arxiv.2603.08801) | Large Language Model-Assisted Superconducting Qubit Experiments | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P1:19 | [10.48550/arxiv.2211.09085](https://doi.org/10.48550/arxiv.2211.09085) | Galactica: A Large Language Model for Science | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P1:20 | [10.1016/j.omtn.2024.102255](https://doi.org/10.1016/j.omtn.2024.102255) | Large language model to multimodal large language model: A journey to shape the biological macromolecules to biological sciences and medicine | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P2:1 | [10.48550/arxiv.2607.02606](https://doi.org/10.48550/arxiv.2607.02606) | ChainSWE: Benchmarking Coding Agents on Multi-Bug Software Maintenance | E — Close inherited-maintenance lead retained in earlier reviews; not newly methods-audited or used as an extra gap anchor here. |
| P2:2, P4b:21 | [10.48550/arxiv.2511.04824](https://doi.org/10.48550/arxiv.2511.04824) | Agentic Refactoring: An Empirical Study of AI Coding Agents | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2:3 | [10.48550/arxiv.2605.08366](https://doi.org/10.48550/arxiv.2605.08366) | SWE Atlas: Benchmarking Coding Agents Beyond Issue Resolution | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2:4 | [10.48550/arxiv.2605.07769](https://doi.org/10.48550/arxiv.2605.07769) | Coding Agents Don't Know When to Act | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2:5 | [10.48550/arxiv.2605.14415](https://doi.org/10.48550/arxiv.2605.14415) | SWE-Chain: Benchmarking Coding Agents on Chained Release-Level Package Upgrades | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2:6 | [10.48550/arxiv.2602.16819](https://doi.org/10.48550/arxiv.2602.16819) | Hybrid-Gym: Training Coding Agents to Generalize Across Tasks | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2:7 | [10.48550/arxiv.2601.02200](https://doi.org/10.48550/arxiv.2601.02200) | Code for Machines, Not Just Humans: Quantifying AI-Friendliness with Code Health Metrics | E — Close Code Health lead retained in earlier frontier review; not an additional independent architecture intervention here. |
| P2:8 | [10.21203/rs.3.rs-4437272/v1](https://doi.org/10.21203/rs.3.rs-4437272/v1) | Large Language Model Based Mutations in Genetic Improvement | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2:9 | [10.48550/arxiv.2605.06464](https://doi.org/10.48550/arxiv.2605.06464) | To What Extent Does Agent-generated Code Require Maintenance? An Empirical Study | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2:10 | [10.48550/arxiv.2602.14046](https://doi.org/10.48550/arxiv.2602.14046) | Every Maintenance Has Its Exemplar: The Future of Software Maintenance through Migration | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2:12 | [10.48550/arxiv.2510.19864](https://doi.org/10.48550/arxiv.2510.19864) | SODBench: A Large Language Model Approach to Documenting Spreadsheet Operations | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2:13 | [10.48550/arxiv.2606.11447](https://doi.org/10.48550/arxiv.2606.11447) | AI Coding Agents Can Reproduce Social Science Findings | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2:14 | [10.1002/smr.2698](https://doi.org/10.1002/smr.2698) | Software maintenance practices using agile methods towards cloud environment: A systematic mapping | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2:15 | [10.48550/arxiv.2604.02544](https://doi.org/10.48550/arxiv.2604.02544) | Developer Experience with AI Coding Agents: HTTP Behavioral Signatures in Documentation Portals | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2:16 | [10.48550/arxiv.2602.17955](https://doi.org/10.48550/arxiv.2602.17955) | Mining Type Constructs Using Patterns in AI-Generated Code | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2:18 | [10.21203/rs.3.rs-3182322/v1](https://doi.org/10.21203/rs.3.rs-3182322/v1) | Learning Risk Factors from App Reviews: A Large Language Model Approach for Risk Matrix Construction | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2:19 | [10.48550/arxiv.2601.20160](https://doi.org/10.48550/arxiv.2601.20160) | How do Agents Refactor: An Empirical Study | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2:20 | [10.1007/s10515-024-00473-6](https://doi.org/10.1007/s10515-024-00473-6) | Large language model based mutations in genetic improvement | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2b:21 | [10.48550/arxiv.2604.16404](https://doi.org/10.48550/arxiv.2604.16404) | On the Use of Commit Messages for Corrective Software Maintenance: A Systematic Mapping Study | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2b:22 | [10.48550/arxiv.2602.01655](https://doi.org/10.48550/arxiv.2602.01655) | ProjDevBench: Benchmarking AI Coding Agents on End-to-End Project Development | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2b:23 | [10.21203/rs.3.rs-5589929/v1](https://doi.org/10.21203/rs.3.rs-5589929/v1) | Large Language Model for Requirements Engineering: A Systematic Literature Review | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2b:24 | [10.48550/arxiv.2607.18057](https://doi.org/10.48550/arxiv.2607.18057) | Test Coverage Analysis of Agentic Pull Requests | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2b:25 | [10.48550/arxiv.2607.22569](https://doi.org/10.48550/arxiv.2607.22569) | Execution-Grounded Security Testing for Coding Agents in Software Engineering Pipelines | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2b:26 | [10.48550/arxiv.2606.05574](https://doi.org/10.48550/arxiv.2606.05574) | SmellBench: Towards Fine-Grained Evaluation of Code Agents on Refactoring Tasks | C — Lin et al. SmellBench v1 selected methods and limitations; injected smells and refactoring quality, not Dinu et al.'s study. |
| P2b:27 | [10.48550/arxiv.2604.03135](https://doi.org/10.48550/arxiv.2604.03135) | AI-Assisted Unit Test Writing and Test-Driven Code Refactoring: A Case Study | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2b:28 | [10.48550/arxiv.2604.13934](https://doi.org/10.48550/arxiv.2604.13934) | Towards Enabling An Artificial Self-Construction Software Life-cycle via Autopoietic Architectures | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2b:29 | [10.1109/icsm.2001.972768](https://doi.org/10.1109/icsm.2001.972768) | Hypothesis-based concept assignment to support software maintenance | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2b:30 | [10.48550/arxiv.2602.19441](https://doi.org/10.48550/arxiv.2602.19441) | When AI Teammates Meet Code Review: Collaboration Signals Shaping the Integration of Agent-Authored Pull Requests | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2b:31 | [10.48550/arxiv.2606.14061](https://doi.org/10.48550/arxiv.2606.14061) | LLM Agents Can See Code Repositories | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2b:32 | [10.21203/rs.3.rs-10348169/v1](https://doi.org/10.21203/rs.3.rs-10348169/v1) | Agentic AI for Code Quality: A Four-Agent Machine Learning System for Repository Refactoring, Public RAG, Groq Reasoning, and Reinforcement Learning | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2b:33 | [10.48550/arxiv.2603.15004](https://doi.org/10.48550/arxiv.2603.15004) | TriFusion-LLM: Prior-Guided Multimodal Fusion with LLM Arbitration for Fine-grained Code Clone Detection | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2b:34 | [10.48550/arxiv.2512.24570](https://doi.org/10.48550/arxiv.2512.24570) | On the Effectiveness of Training Data Optimization for LLM-based Code Generation: An Empirical Study | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2b:35 | [10.1109/icsme55016.2022.00020](https://doi.org/10.1109/icsme55016.2022.00020) | Evaluation of Context-Aware Language Models and Experts for Effort Estimation of Software Maintenance Issues | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2b:36 | [10.48550/arxiv.2602.03712](https://doi.org/10.48550/arxiv.2602.03712) | SWE-Refactor: A Repository-Level Benchmark for Real-World LLM-Based Code Refactoring | C — SWE-Refactor v1 selected task/verification methods distinguish refactoring checks from later maintenance. |
| P2b:37 | [10.48550/arxiv.2601.13139](https://doi.org/10.48550/arxiv.2601.13139) | From Human to Machine Refactoring: Assessing GPT-4's Impact on Python Class Quality and Readability | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2b:38 | [10.48550/arxiv.2603.15538](https://doi.org/10.48550/arxiv.2603.15538) | QiboAgent: a practitioner's guideline to open source assistants for Quantum Computing code development | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2b:39 | [10.3390/software4010003](https://doi.org/10.3390/software4010003) | The Scalable Detection and Resolution of Data Clumps Using a Modular Pipeline with ChatGPT | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P2b:40 | [10.1145/3793302.3793344](https://doi.org/10.1145/3793302.3793344) | ML in a Box: Analyzing Containerization Practices in Open Source ML Projects | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P3:1 | [10.1109/aina.2007.78](https://doi.org/10.1109/aina.2007.78) | Immediate Mode Scheduling of Independent Jobs in Computational Grids | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P3:2 | [10.1080/00437956.1999.11432485](https://doi.org/10.1080/00437956.1999.11432485) | Wallace Chafe's light subject constraint in conversational discourse in the immediate mode of consciousness | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P3:3 | [10.4204/eptcs.265.8](https://doi.org/10.4204/eptcs.265.8) | Space Improvements and  Equivalences in a Functional Core Language | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P3:4 | [10.1080/02670836.2019.1705027](https://doi.org/10.1080/02670836.2019.1705027) | Investigation of functional core-rim composite part production by inserted powder injection moulding | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P3:5 | [10.1016/s1097-2765(01)00316-1](https://doi.org/10.1016/s1097-2765(01)00316-1) | Reconstitution of a Functional Core Polycomb Repressive Complex | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P3:6 | [10.1101/2020.06.10.145201](https://doi.org/10.1101/2020.06.10.145201) | Brain networks subserving functional core processes of emotions identified with componential modelling | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P3:7 | [10.3390/nano11061546](https://doi.org/10.3390/nano11061546) | Multi-Functional Core-Shell Nanofibers for Wound Healing | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P3:8 | [10.1038/sj.emboj.7601765](https://doi.org/10.1038/sj.emboj.7601765) | Reconstitution reveals the functional core of mammalian eIF3 | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P3:9 | [10.1093/cercor/bhad093](https://doi.org/10.1093/cercor/bhad093) | Brain networks subserving functional core processes of emotions identified with componential modeling | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P3:10 | [10.1038/s41598-017-03420-6](https://doi.org/10.1038/s41598-017-03420-6) | The dynamic functional core network of the human brain at rest | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P3:11 | [10.3389/fmicb.2020.01361](https://doi.org/10.3389/fmicb.2020.01361) | Scoring Species for Synthetic Community Design: Network Analyses of Functional Core Microbiomes | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P3:12 | [10.1145/2790449.2790512](https://doi.org/10.1145/2790449.2790512) | Improvements in a functional core language with call-by-need operational semantics | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P3:13 | [10.1128/jb.00933-15](https://doi.org/10.1128/jb.00933-15) | A Functional Core of IncA Is Required for Chlamydia trachomatis Inclusion Fusion | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P3:14 | [10.1261/rna.076117.120](https://doi.org/10.1261/rna.076117.120) | An evolutionarily conserved RNA structure in the functional core of the lincRNA Cyrano | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P3:15 | [10.1002/adhm.201300577](https://doi.org/10.1002/adhm.201300577) | Functional Core/Shell Drug Nanoparticles for Highly Effective Synergistic Cancer Therapy | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P3:16 | [10.21608/eijssa.2020.51218.1058](https://doi.org/10.21608/eijssa.2020.51218.1058) | Effect of Functional Core Conditioning Training on Hiking at Sailing Radial | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P3:17 | [10.1021/nl0490826](https://doi.org/10.1021/nl0490826) | From Functional Core/Shell Nanoparticles Prepared via Layer-by-Layer Deposition to Empty Nanospheres | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P3:18 | [10.26508/lsa.202101271](https://doi.org/10.26508/lsa.202101271) | Phylogenetic profiling resolves early emergence of PRC2 and illuminates its functional core | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P3:19 | [10.1101/2024.01.23.576934](https://doi.org/10.1101/2024.01.23.576934) | Propofol Disrupts the Functional Core-Matrix Architecture of the Thalamus in Humans | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P3:20 | [10.1091/mbc.e13-07-0381](https://doi.org/10.1091/mbc.e13-07-0381) | ER exit sites are physical and functional core autophagosome biogenesis components | E — Broad-query namesake, other-domain or general-method lead; not used for this architecture-maintenance comparison. |
| P4:1 | [10.48550/arxiv.2607.21632](https://doi.org/10.48550/arxiv.2607.21632) | A Consensus-Based Framework for Relative Preference Evaluation of Large Language Models | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P4:2 | [10.5281/zenodo.18622107](https://doi.org/10.5281/zenodo.18622107) | LLMs for Architectural Refactoring: An Exploratory study on Monoliths to Microservices | E — Same-title/author architectural-refactoring deposit lineage; canonical ICSA DOI used, deposit relation not independently established. |
| P4:3, P6:2 | [10.5281/zenodo.18622108](https://doi.org/10.5281/zenodo.18622108) | LLMs for Architectural Refactoring: An Exploratory study on Monoliths to Microservices | E — Same-title/author ICSA deposit; metadata retrieved but body access failed. Not an independent study. |
| P4:4 | [10.1109/icsa66085.2026.00033](https://doi.org/10.1109/icsa66085.2026.00033) | LLMs for Architectural Refactoring: An Exploratory Study on Monoliths to Microservices | C — ICSA conference abstract reports architectural metrics; full methods inaccessible, qualified overlap assessment only. |
| P4:5 | [10.48550/arxiv.2510.06104](https://doi.org/10.48550/arxiv.2510.06104) | Explaining Code Risk in OSS: Towards LLM-Generated Fault Prediction Interpretations | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P4:6 | [10.48550/arxiv.2603.29632](https://doi.org/10.48550/arxiv.2603.29632) | An Empirical Study of Multi-Agent Collaboration for Automated Research | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P4:7 | [10.48550/arxiv.2603.01051](https://doi.org/10.48550/arxiv.2603.01051) | CelloAI Benchmarks: Toward Repeatable Evaluation of AI Assistants | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P4:8 | [10.48550/arxiv.2607.20452](https://doi.org/10.48550/arxiv.2607.20452) | AINTMA: Agentic AI Architecture for Autonomous Test Management with Generative Intelligence, Secure Cloud Communication and Adaptive Quality Analytics | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P4:9 | [10.48550/arxiv.2512.08492](https://doi.org/10.48550/arxiv.2512.08492) | Autonomous Issue Resolver: Towards Zero-Touch Code Maintenance | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P4:10 | [10.48550/arxiv.2603.07091](https://doi.org/10.48550/arxiv.2603.07091) | Exploring the Reasoning Depth of Small Language Models in Software Architecture: A Multidimensional Evaluation Framework Towards Software Engineering 2.0 | E — Relevant small-model architecture reasoning lead; methods unassessed, model-capability arm deferred. |
| P4:11 | [10.48550/arxiv.2510.19366](https://doi.org/10.48550/arxiv.2510.19366) | MoE-Prism: Disentangling Monolithic Experts for Elastic MoE Services via Model-System Co-Designs | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P4:12 | [10.48550/arxiv.2604.17464](https://doi.org/10.48550/arxiv.2604.17464) | Project Prometheus: Bridging the Intent Gap in Agentic Program Repair via Reverse-Engineered Executable Specifications | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P4:13 | [10.48550/arxiv.2605.01392](https://doi.org/10.48550/arxiv.2605.01392) | Using LLMs in Software Design: An Empirical Study of GitHub and A Practitioner Survey | E — Relevant design-practice/survey lead; methods unassessed, not evidence of downstream package effects. |
| P4:14 | [10.48550/arxiv.2608.12246](https://doi.org/10.48550/arxiv.2608.12246) | VICBench: A Multi-Language Benchmark for Code Vulnerability Detection | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P4:15 | [10.48550/arxiv.2606.07420](https://doi.org/10.48550/arxiv.2606.07420) | Lost in Migration: Exposing Android Framework Vulnerabilities in Parallel Java-Kotlin Implementations | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P4:16 | [10.48550/arxiv.2606.31368](https://doi.org/10.48550/arxiv.2606.31368) | MOA: A Profiling-Guided LLM Framework for Memory-Optimization Automation at Codebase Scale | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P4:17 | [10.1002/spe.70035](https://doi.org/10.1002/spe.70035) | Detecting Microservice's Architectural Anti‐Pattern Indicators Using Graph Neural Networks | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P4:18 | [10.48550/arxiv.2604.11477](https://doi.org/10.48550/arxiv.2604.11477) | OOM-RL: Out-of-Money Reinforcement Learning Market-Driven Alignment for LLM-Based Multi-Agent Systems | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P4:19 | [10.48550/arxiv.2511.13998](https://doi.org/10.48550/arxiv.2511.13998) | LoCoBench-Agent: An Interactive Benchmark for LLM Agents in Long-Context Software Engineering | E — Relevant long-context engineering lead; method overlap remains unassessed in this bounded proposal search. |
| P4:20 | [10.1002/smr.70068](https://doi.org/10.1002/smr.70068) | Enhancing Task Prioritization in Software Development Issues Tracking System | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P4b:22 | [10.48550/arxiv.2606.06843](https://doi.org/10.48550/arxiv.2606.06843) | Empirical Study on the Characteristics and Evolution of AI-usage in GitHub Repositories: Evidence from Code Comments | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P4b:23 | [10.48550/arxiv.2602.09540](https://doi.org/10.48550/arxiv.2602.09540) | SWE-Bench Mobile: Can Large Language Model Agents Develop Industry-Level Mobile Applications? | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P4b:24, P6:1 | [10.1002/iis2.70208](https://doi.org/10.1002/iis2.70208) | (metadata title absent) | E — Title/abstract still absent after exact-DOI retry. Relevance unresolved, not evidence of low quality or absence. |
| P4b:25 | [10.48550/arxiv.2511.01348](https://doi.org/10.48550/arxiv.2511.01348) | The Future of Generative AI in Software Engineering: A Vision from Industry and Academia in the European GENIUS Project | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P4b:26 | [10.48550/arxiv.2510.11039](https://doi.org/10.48550/arxiv.2510.11039) | RepoSummary: Feature-Oriented Summarization and Documentation Generation for Code Repositories | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P4b:27 | [10.1002/spe.70062](https://doi.org/10.1002/spe.70062) | Developing a Framework for the Quality‐Driven Migration to Microservices: A Multi‐Method Design Science Study | E — Relevant quality-driven microservice migration lead beyond rank 20; full methods unassessed, novelty boundary remains qualified. |
| P4b:28 | [10.21203/rs.3.rs-6688473/v1](https://doi.org/10.21203/rs.3.rs-6688473/v1) | Self-Programming AI: Code-Learning Agents for Autonomous Refactoring and Architectural Evolution | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P4b:29 | [10.48550/arxiv.2601.14523](https://doi.org/10.48550/arxiv.2601.14523) | Large Language Model-Powered Evolutionary Code Optimization on a Phylogenetic Tree | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P4b:30 | [10.48550/arxiv.2606.27122](https://doi.org/10.48550/arxiv.2606.27122) | Mostly Automatic Translation of Language Interpreters from C to Safe Rust | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P4b:31 | [10.48550/arxiv.2604.03789](https://doi.org/10.48550/arxiv.2604.03789) | Automated Conjecture Resolution with Formal Verification | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P4b:32 | [10.48550/arxiv.2510.07941](https://doi.org/10.48550/arxiv.2510.07941) | An AUTOSAR-Aligned Architectural Study of Vulnerabilities in Automotive SoC Software | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P4b:33 | [10.48550/arxiv.2604.25222](https://doi.org/10.48550/arxiv.2604.25222) | Adaptive Management of Microservices in Dynamic Computing Environments: A Taxonomy and Future Directions | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P4b:34 | [10.3390/app16136729](https://doi.org/10.3390/app16136729) | MRQF-MAS: A Multiscale Relativistic Quantum Finance Framework for Cooperative Multi-Agent Trading Systems with Shared Knowledge Base | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P4b:35 | [10.33612/diss.833424077](https://doi.org/10.33612/diss.833424077) | Understanding, Analysis, and Handling of Software Architecture Erosion | E — Software/agent/architecture-adjacent lead; title/partial-abstract screening only, full-methods overlap unassessed. |
| P5:1 | [10.1145/3414080.3414092](https://doi.org/10.1145/3414080.3414092) | Hailstorm: A Statically-Typed, Purely Functional Language for IoT Applications | E — Functional IoT language lead; no full-methods assessment for this application comparison. |
| P5:2 | [10.1145/3609025.3609478](https://doi.org/10.1145/3609025.3609478) | Functional Shell and Reusable Components for Easy GUIs | C — GUI Easy selected body sections through part of section 5: functional composition and imperative integration; experience report, not controlled maintenance effects. |
| P5:3 | [10.18523/2617-3808.2018.33-39](https://doi.org/10.18523/2617-3808.2018.33-39) | Implementing HTTP-Service in a Functional Domain-Specific Language Based on Free Monads | E — Functional HTTP-service design lead; no full-methods assessment for this application comparison. |
| P5:4 | [10.22541/au.164510374.48530005/v1](https://doi.org/10.22541/au.164510374.48530005/v1) | Features of a dream programming language: 2nd draft | E — Programming-language design lead; not assessed as controlled maintenance evidence. |
| P6:3 | [10.48550/arxiv.2605.07001](https://doi.org/10.48550/arxiv.2605.07001) | SmellBench: Evaluating LLM Agents on Architectural Code Smell Repair | C — Dinu et al. SmellBench v2 selected expert-validation, scoring and construct-validity methods; not Lin et al.'s study. |

## New web endpoint inventory

These **21 endpoints** include one failed open. DOI/URL aliases are retained
for access provenance, not counted as different studies. C/E has the same
meaning as above; primary text reading is limited to the sections stated.

| Calls | Endpoint | Decision / use |
| --- | --- | --- |
| PW1 | [Functional Shell and Reusable Components for Easy GUIs](https://arxiv.org/abs/2308.16024) | E — Discovery or duplicate publication/event page; canonical primary source used. |
| PW1 | [Functional Shell and Reusable Components for Easy GUIs](https://www.researchgate.net/publication/373574753_Functional_Shell_and_Reusable_Components_for_Easy_GUIs) | E — Secondary discovery/duplicate; primary source used, no technical finding credited here. |
| PW1 | [Free Video: Functional Shell and Reusable Components for Easy GUIs from ACM SIGPLAN \| Class Central](https://www.classcentral.com/course/youtube-funarch-23-functional-shell-and-reusable-components-for-easy-guis-347631) | E — Secondary discovery/duplicate; primary source used, no technical finding credited here. |
| PW1 | [LLMs for Architectural Refactoring: An Exploratory Study on Monoliths to Microservices \| Request PDF](https://www.researchgate.net/publication/410808834_LLMs_for_Architectural_Refactoring_An_Exploratory_Study_on_Monoliths_to_Microservices) | E — Secondary discovery/duplicate; primary source used, no technical finding credited here. |
| PW1 | [Publications · Karthik Vaidhyanathan](https://karthikvaidhyanathan.com/publications/) | E — Discovery or duplicate publication/event page; canonical primary source used. |
| PW1, PW3, PW4 | [LLMs for Architectural Refactoring: An Exploratory study on Monoliths to Microservices (ICSA 2026 - Research Papers) - ICSA 2026](https://conf.researchr.org/details/icsa-2026/icsa-2026-papers/27/LLMs-for-Architectural-Refactoring-An-Exploratory-study-on-Monoliths-to-Microservice) | C — Canonical conference abstract; methods inaccessible; maps to ICSA DOI. |
| PW1 | [Functional Shell and Reusable Components for Easy GUIs](https://defn.io/papers/fungui-funarch23.pdf) | C — Author-PDF search result confirms identity; actual selected body read via Scite, not a complete PDF review. |
| PW1 | [FUNARCH 2023: Proceedings of the 1st ACM SIGPLAN International Workshop on Functional Software Architecture](https://sigplan.org/OpenTOC/funarch23.html) | C — Primary proceedings metadata for GUI Easy publication identity. |
| PW1 | [FUNARCH 2023 - ICFP 2023](https://icfp23.sigplan.org/home/funarch-2023) | E — Discovery or duplicate publication/event page; canonical primary source used. |
| PW1 | [Two papers accepted at the International Conference on Software Architecture (ICSA) 2026 – Frame Lab](https://www.framelab.team/2026/02/07/international-conference-on-software-architecture-icsa-2026/) | E — Discovery or duplicate publication/event page; canonical primary source used. |
| PW1 | [LLMs for Architectural Refactoring: An Exploratory Study on Monoliths to Microservices. – Frame Lab](https://www.framelab.team/publication/llms-for-architectural-refactoring-an-exploratory-study-on-monoliths-to-microservices/) | E — Discovery or duplicate publication/event page; canonical primary source used. |
| PW1 | [Functional Software Architecture](https://functional-architecture.org/events/funarch-2023/) | E — Discovery or duplicate publication/event page; canonical primary source used. |
| PW1 | [dblp: FUNARCH](https://dblp.org/db/conf/funarch/funarch2023.html) | E — Secondary discovery/duplicate; primary source used, no technical finding credited here. |
| PW1, PW2 | [ICSA 2026 - Software Architecture Showcase - ICSA 2026](https://conf.researchr.org/track/icsa-2026/icsa-2026-software-architecture-showcase) | E — Wrong conference track for the target paper; correct research entry used. |
| PW2 | [[2602.03712] SWE-Refactor: A Repository-Level Benchmark for Real-World LLM-Based Code Refactoring](https://arxiv.org/abs/2602.03712) | C — Primary SWE-Refactor edition metadata; same work as DOI. |
| PW2 | [[2606.05574] SmellBench: Towards Fine-Grained Evaluation of Code Agents on Refactoring Tasks](https://arxiv.org/abs/2606.05574) | C — Primary Lin et al. SmellBench edition metadata; same work as DOI. |
| PW3, PW4 | [SWE-Refactor: A Repository-Level Benchmark for Real-World LLM-Based Code Refactoring](https://arxiv.org/html/2602.03712v1) | C — Selected SWE-Refactor task/verification methods; maps to cited DOI. |
| PW3, PW4 | [SmellBench: Towards Fine-Grained Evaluation of Code Agents on Refactoring Tasks](https://arxiv.org/html/2606.05574v1) | C — Selected Lin et al. methods/limitations and Dinu bibliography lead; maps to cited DOI. |
| PW5 | [[2605.07001] SmellBench: Evaluating LLM Agents on Architectural Code Smell Repair](https://arxiv.org/abs/2605.07001) | C — Primary Dinu et al. edition metadata; v2 dated 12 May, not Scite fallback January date. |
| PW6, PW7 | [SmellBench: Evaluating LLM Agents on Architectural Code Smell Repair](https://arxiv.org/html/2605.07001v2) | C — Selected Dinu et al. expert-validation, scoring and limitations; maps to cited DOI. |
| PW5 | [ICSA deposit (open failed)](https://zenodo.org/records/18622108) | E — Deposit open failed; same-title/author metadata not an independent study. |

## Public Nu history: bounded AI extraction

One read-only Luna Max worker inspected public source/history while the main
agent handled Scite, methodology and acceptance. No edits, builds, execution or
private transcript publication occurred. Search date: 2026-09-14 HKT.
GitHub Search API, one page per query, `per_page=100`, no state restriction:

| Exact query | Returned |
| --- | ---: |
| `repo:bryanedds/Nu is:issue Breakout` | 0 |
| `repo:bryanedds/Nu is:pr Breakout` | 0 |
| `repo:bryanedds/Nu is:issue MMCC` | 19 |
| `repo:bryanedds/Nu is:pr MMCC` | 2 |
| `repo:bryanedds/Nu is:issue ImSim` | 10 |
| `repo:bryanedds/Nu is:pr ImSim` | 2 |

The six queries returned **33 positions / 29 unique issue/PR records**. No query
needed pagination. Ten public bodies/timelines were inspected; the other 19
received metadata/title-only screening. These counts do not describe all Nu
history or establish task-mining saturation. Commit/path inspection supplied
three additional historical maintenance leads and one rejected cleanup lead.

Pin `064f7ae92a8506689cd91aff5e6804a375d6ef3d` has author timestamp
`2026-07-23T01:55:40-04:00`. Exact read-only
`git merge-base --is-ancestor <commit> <pin>` returned 0 for `a22fe112`,
`edec18e2` and `39d5dc97`. For `6890bcf4` it returned **128: object unavailable**
in the local pinned clone, not a verified non-ancestor exit code. Public metadata
dates that resolution to 12 August and source inspection shows the pinned MMCC
still uses `DesiredScreen`. The worker's initially ambiguous ancestry summary
was clarified before publication; no four-commit ancestry claim is retained.

| Retained public change | Date / inspected scope | Interpretation |
| --- | --- | --- |
| [Issue #1374](https://github.com/bryanedds/Nu/issues/1374), [resolution 6890bcf4](https://github.com/bryanedds/Nu/commit/6890bcf4f101501a1e1552cbcddf55f6a5de6548) | Issue opened 31 May, closed 13 August 2026; commit 12 August. Public body/timeline and engine/application diff inspected. | Screen-selection API convergence; source-version sensitivity, not an application-only matched task. |
| [a22fe112](https://github.com/bryanedds/Nu/commit/a22fe112e209dae806482c821fe32bf63d0dc5bf) | 5 February 2026; ImSim template and Breakout selected-screen guard | Inherited application fix motivates lifecycle contracts, not an unpatched baseline defect. |
| [edec18e2](https://github.com/bryanedds/Nu/commit/edec18e27bb9b43adb93404a8a50d54392ce6946) | 24 February 2026; ImSim ball initialization/life-reset velocity diff | Real application fix, but MMCC's physics model differs. No exact shared repair claim. |
| [39d5dc97](https://github.com/bryanedds/Nu/commit/39d5dc97321c7b7af75f05b5fb11c2fe7b40a0b7) | 12 January 2025; MMCC content conditional on Playing state | Lifecycle motivation with style-specific implementation. |

The rejected [129567b7 cleanup](https://github.com/bryanedds/Nu/commit/129567b795cc62db165bbf972472e97265375e75)
makes ImSim superficially more similar to MMCC but supplies no clear behavioral
maintenance task. Other strong exclusions were Content debugging (#1046),
ImSim deferred-context snapshots (#1089), an ImSim API defect (#1281) and
physics-dependency PRs (#1218/#1437). They are real engineering concerns, but
not symmetric application changes in the proposed fixed-engine comparison.

Inventory: B = body/timeline inspected; T = metadata/title only. Labels are
short paraphrases, not quoted issue titles. C is a scenario lead, not empirical
support for architectural superiority.

| Item | Short label | Extent | Decision / reason |
| --- | --- | --- | --- |
| [#607](https://github.com/bryanedds/Nu/issues/607) | descendant event specification | B | E — Style/API-specific engine or tooling concern; not selected as a shared application scenario. |
| [#761](https://github.com/bryanedds/Nu/issues/761) | shrink MMCC call stacks | B | E — Style/API-specific engine or tooling concern; not selected as a shared application scenario. |
| [#789](https://github.com/bryanedds/Nu/issues/789) | visual editing of model entries | B | E — Style/API-specific engine or tooling concern; not selected as a shared application scenario. |
| [#887](https://github.com/bryanedds/Nu/issues/887) | property lens fallback | B | E — Style/API-specific engine or tooling concern; not selected as a shared application scenario. |
| [#955](https://github.com/bryanedds/Nu/issues/955) | generated World.doSubscription keys | B | E — Style/API-specific engine or tooling concern; not selected as a shared application scenario. |
| [#1044](https://github.com/bryanedds/Nu/issues/1044) | ImSim presumptive-lens documentation | B | E — Style/API-specific engine or tooling concern; not selected as a shared application scenario. |
| [#1046](https://github.com/bryanedds/Nu/issues/1046) | MMCC Content debugging | B | E — Style/API-specific engine or tooling concern; not selected as a shared application scenario. |
| [#1089](https://github.com/bryanedds/Nu/issues/1089) | snapshotting ImSim context in World.defer | B | E — Style/API-specific engine or tooling concern; not selected as a shared application scenario. |
| [#1281](https://github.com/bryanedds/Nu/issues/1281) | generic ImSim doGroup | B | E — Style/API-specific engine or tooling concern; not selected as a shared application scenario. |
| [#1374](https://github.com/bryanedds/Nu/issues/1374) | MMCC screen selection like ImSim | B | C — Public lifecycle/API motivation and source-pin sensitivity; no equivalent task assumed. |
| [#177](https://github.com/bryanedds/Nu/issues/177) | Potential Performance Issue Tracking | T | E — Title/metadata only; application/task comparability unassessed, not a substantive rejection. |
| [#449](https://github.com/bryanedds/Nu/issues/449) | Automatic Content Memoization | T | E — Title/metadata only; application/task comparability unassessed, not a substantive rejection. |
| [#528](https://github.com/bryanedds/Nu/issues/528) | ModelDriven rigid-body facet documentation | T | E — Title/metadata only; application/task comparability unassessed, not a substantive rejection. |
| [#532](https://github.com/bryanedds/Nu/issues/532) | FSharp.Core collection equality short-circuit | T | E — Title/metadata only; application/task comparability unassessed, not a substantive rejection. |
| [#598](https://github.com/bryanedds/Nu/issues/598) | port BlazeVector completely to MMCC | T | E — Title/metadata only; application/task comparability unassessed, not a substantive rejection. |
| [#764](https://github.com/bryanedds/Nu/issues/764) | serializable MMCC children / ESP | T | E — Title/metadata only; application/task comparability unassessed, not a substantive rejection. |
| [#769](https://github.com/bryanedds/Nu/issues/769) | OpenGL.NET RuntimeType allocations | T | E — Title/metadata only; application/task comparability unassessed, not a substantive rejection. |
| [#779](https://github.com/bryanedds/Nu/issues/779) | compiled MMCC change propagation | T | E — Title/metadata only; application/task comparability unassessed, not a substantive rejection. |
| [#853](https://github.com/bryanedds/Nu/issues/853) | Omni Blade NPC model-change interaction | T | E — Title/metadata only; application/task comparability unassessed, not a substantive rejection. |
| [#917](https://github.com/bryanedds/Nu/issues/917) | automatic model-conversion notification | T | E — Title/metadata only; application/task comparability unassessed, not a substantive rejection. |
| [#930](https://github.com/bryanedds/Nu/issues/930) | Nu as a platform for non-technical creators | T | E — Title/metadata only; application/task comparability unassessed, not a substantive rejection. |
| [#981](https://github.com/bryanedds/Nu/issues/981) | broader name for ImNui | T | E — Title/metadata only; application/task comparability unassessed, not a substantive rejection. |
| [#1103](https://github.com/bryanedds/Nu/issues/1103) | Gaia property-table alignment | T | E — Title/metadata only; application/task comparability unassessed, not a substantive rejection. |
| [#1145](https://github.com/bryanedds/Nu/issues/1145) | Terra Firma pause soft-lock | T | E — Title/metadata only; application/task comparability unassessed, not a substantive rejection. |
| [#1229](https://github.com/bryanedds/Nu/issues/1229) | ImSim-like API for Prime.Ecs | T | E — Title/metadata only; application/task comparability unassessed, not a substantive rejection. |
| [#1257](https://github.com/bryanedds/Nu/issues/1257) | Unreal-style networking | T | E — Title/metadata only; application/task comparability unassessed, not a substantive rejection. |
| [#1189](https://github.com/bryanedds/Nu/pull/1189) | GcDebug/LOH-thrashing documentation | T | E — Title/metadata only; application/task comparability unassessed, not a substantive rejection. |
| [#1218](https://github.com/bryanedds/Nu/pull/1218) | Box2dNet character physics | T | E — Title/metadata only; application/task comparability unassessed, not a substantive rejection. |
| [#1437](https://github.com/bryanedds/Nu/pull/1437) | Box2D.NET update | T | E — Title/metadata only; application/task comparability unassessed, not a substantive rejection. |

Pinned public source links and the manual-physics/dynamic-body distinction are
retained in the [previous extraction ledger](nu-grounded-maintenance-sources-2026-09-14.md#nu-source-extraction-and-limits)
and the proposal. Source inspection establishes none of runtime/build success,
player-visible equivalence, headless feasibility, sandbox safety or maintenance
advantage. Those are explicit future feasibility questions.

## Citation audit and publication checks

Scite answer ID: `alf-architecture-maintenance-proposal-2026-09-14`.
One final `report_citations` call recorded **34 credited / 154 not credited**,
**0 skipped**, across **188 identifiers/endpoints**. The subsequent
`citation_report` confirmed 188 recorded decisions, no missing reasons,
`retrieval_unlinked = false` and `truncated = false`. Its answer-scoped
`retrieved` field is null, not a verified literature-search denominator.
Provenance: 123 Scite DOI records, 21 web endpoints and 44 reused/public-source
records. DOI/URL/deposit aliases are not independent works. The 33 `full_text`
stages include selected paper sections and public issue/source diffs; this is
**not 33 complete papers read**. Earlier answer IDs were not modified.

Another read-only AI session (Sol, high effort) audited only the proposal's
dispatch arithmetic, analysis units, missing-versus-zero rules, Phase A/B
authority and package-level inference boundaries. It reported no blocking or
important findings in that scope. The main agent owns design, source acceptance
and final self-review; neither session constitutes human expert validation.

Local checks actually run:

- `python -m unittest discover -s tests -p test_ci_scope.py -v`: **11 passed**.
  Printed detection-fallback messages are expected test cases, not a CI failure.
- PowerShell strict UTF-8 decoding, trailing-whitespace/replacement-character
  checks on all four changed Markdown files: passed.
- **101 relative file links** resolved; **3 pinned public-source file paths**
  matched the inspected Nu checkout. This does not validate every external DOI
  endpoint or establish runtime behavior.
- `git diff --check`: passed. The final containing commit and exact-commit CI
  are reported in the publication handoff; no status-only follow-up is needed.

No experimental call, OAuth staging, candidate run or new allocation occurred.
Only the proposal, this ledger and the PLAN/AGENTS entry points are in scope.
The unrelated untracked `uv.lock` is not staged. Validation is documentation
scope: CI-routing regressions, UTF-8/whitespace and local source-link checks;
no runtime or experimental behavior is inferred from those checks.

## Follow-up: proposal background, architecture lineage and pagination

Revision base: `0df55a45b5087a9420807617ea165c01c873f779`.
This section records the subsequent user requests, not a rewrite of the initial
search or its closed audit. The user requested a paper-like proposal with
definitions/background before the questions, explicit dataset/analytics,
metadata fallback beyond Scite, deeper pagination, and justification of
MMCC/ImSim as alternatives—including the mathematical/operational and
turn-based/real-time descriptions.

### Disposition and changes

The proposal now separates introduction, architecture lineage, close agent
studies, conditional gap, questions, dataset construction and analytical methods.
It adds explicit credibility criteria, distinguishes existing examples from an
unbuilt research dataset, and specifies paired trajectory contrasts, whole-block
uncertainty, null bounds and failure coding. Success requires a valid submission,
build and cumulative behavior; retained source after a malformed response is
not counted as that response succeeding. These are **unadopted proposal
clarifications**, not edits to a frozen protocol or permission to construct/run.
The 192+5 ceiling remains proposed, allocated zero. All previous holds and
completed construction evidence remain intact.

The more defensible provisional contrast is explicit model/transition
organization versus locally expressed interaction/world synchronization.
Neither MMCC/ImSim nor MVU/ImGui is an exhaustive taxonomy of major game
architectures. The exact mathematical/operational phrases were not found in the
bounded public Nu inspection and are retained as the user's characterization.
No verified direct MMCC/ImSim scholarly comparison was located. This is
non-discovery under the search/access limits below, not an absence/novelty proof.

### Search extent and selection

Scite returned an effective maximum of 20 in earlier discovery calls; this
follow-up requests at most 20 and uses the **returned page length** for offsets.
R1's requested 12 was an exact lookup of nine known DOI records, not a literature
cutoff. R2/R2b continue the earlier P2 query at offsets 40/60; its reported total
changed from 440 to 441. Relevance rankings can change, so the old/new pages are
not described as one immutable 80-item snapshot.

R0–R3b returned 93 positions; the architecture follow-up adds 125, for
**218 positions / 211 distinct normalized Scite DOI identifiers** in this
revision. The full identifier/position inventory below distinguishes credited,
unassessed, off-topic and related-edition records. These are not counts of
independent studies, complete papers read or all eligible literature.
A2/A2b cover all 37 results for that exact query; that is not field saturation.
A5 mistakenly started at offset 20 on a reformulated query with only 19 results;
A5a immediately recovered offset 0. The empty page is not absence evidence.
A0/A6 returned zero; A8 returned two botanical/entomological false positives.
A1's MMCC/ImSim acronyms and A3's Elm terminology produced extensive unrelated
matches. Reformulation and primary-source follow-up are more meaningful than
blindly exhausting these noisy rankings.

| ID | Exact term/selection | Offset; requested/effective limit; returned/total |
| --- | --- | --- |
| R0 | `Exact selections: 10.1145/361598.361623; 10.1145/2884781.2884822; 10.1145/3194164.3194178; 10.1109/SEAA53835.2021.00032` | 0; 6/6; 4/4 |
| R1 | `Exact selections: 10.4230/LIPIcs.ECOOP.2020.14; 10.1145/3609025.3609478; 10.1016/S0164-1212(03)00080-3; 10.48550/arXiv.2603.24755; 10.48550/arXiv.2606.21804; 10.48550/arXiv.2603.27745; 10.48550/arXiv.2602.03712; 10.48550/arXiv.2605.07001; 10.48550/arXiv.2606.05574` | 0; 12/12; 9/9 |
| R2 | `("code maintainability" OR "software maintenance") AND (experiment OR intervention OR refactoring) AND ("large language model" OR "coding agents")` | 40; 20/20; 20/441 |
| R2b | `("code maintainability" OR "software maintenance") AND (experiment OR intervention OR refactoring) AND ("large language model" OR "coding agents")` | 60; 20/20; 20/441 |
| R3 | `("coding agent" OR "coding agents") AND ("starting code" OR "initial implementation" OR "code structure" OR "code organization")` | 0; 20/20; 20/239 |
| R3b | `("coding agent" OR "coding agents") AND ("starting code" OR "initial implementation" OR "code structure" OR "code organization")` | 20; 20/20; 20/239 |
| A0 | `"model-view-update" AND ("immediate mode" OR ImGui OR "immediate-mode")` | 0; 20/20; 0/0 |
| A1 | `("MMCC" OR "ImSim") AND ("Nu" OR "game engine" OR architecture)` | 0; 20/20; 20/296 |
| A2 | `("immediate mode" OR "immediate-mode") AND ("retained mode" OR "retained-mode") AND (GUI OR interface OR architecture)` | 0; 20/20; 20/37 |
| A2b | `("immediate mode" OR "immediate-mode") AND ("retained mode" OR "retained-mode") AND (GUI OR interface OR architecture)` | 20; 20/20; 17/37 |
| A3 | `("Elm architecture" OR "model-view-update") AND (comparison OR evaluation OR architecture)` | 0; 20/20; 20/492 |
| A4 | `"immediate mode" AND (GUI OR interfaces) AND (functional OR declarative OR "model view" OR comparison)` | 0; 20/20; 20/268 |
| A5 | `"model-view-update" AND (GUI OR games OR "user interface")` | 20; 20/20; 0/19 |
| A5a | `"model-view-update" AND (GUI OR games OR "user interface")` | 0; 20/20; 19/19 |
| A6 | `"model-message-command-content" OR ("ImSim" AND "Bryan")` | 0; 20/20; 0/0 |
| A7 | `Exact selections: Evolution of Functional UI Paradigms; Functional Reactive Animation; Exploring the immediate mode GUI concept for graphical user interfaces in mixed reality applications` | 0; 20/20; 7/7 |
| A8 | `("Elm" OR "model-view-update" OR "model view update") AND (ImGui OR "immediate-mode GUI" OR "immediate mode GUI")` | 0; 20/20; 2/2 |

Deeper positions changed the synthesis: SWE-CI appeared at R2:60, RepoProbe at
R2b:79 and RepoMod-Bench at R3b:40. StaminaBench appeared at R3:6. The search did
not stop at five or twelve results. These specific leads were selected for
methods reading because they might already perform architecture assignment or
behavioral maintenance. Later UI searches found a directly relevant conceptual
comparison, Sperber/Schlegel, through web discovery followed by exact Scite
identification. Recent temporal-reactivity work `10.48550/arXiv.2607.27074`,
complex-interaction artifact `10.21504/rur.32900561`, and several agent-policy
leads remain unassessed; they cannot support blanket novelty exclusions.

### Added or refreshed primary reading

| Identity | Edition, access and actual extent | Use and boundary |
| --- | --- | --- |
| Parnas, `10.1145/361598.361623` | Crossref metadata; DOI landing 403; [university-hosted article](https://john.cs.olemiss.edu/~hcc/csci555/notes/localcopy/Parnas_Criteria_Decomposing.pdf), abstract, responsibility/KWIC discussion and criteria passage | Conceptual decomposition rationale, not an agent-maintenance effect estimate. |
| Xiao et al., `10.1145/2884781.2884822` | Crossref; [author PDF](https://personal.stevens.edu/~lxiao6/papers/ICSE-16-Debt.pdf), front matter, introduction and selected methods refreshed | Seven-project history/churn evidence. Prior footer DOI discrepancy stays resolved by registry metadata, not a new paper identity. |
| Besker et al., `10.1145/3194164.3194178`; Lenarduzzi et al., `10.1109/SEAA53835.2021.00032` | Scite/Crossref metadata refreshed; prior selected body reading reused, not newly complete reading. [Lenarduzzi institutional abstract](https://researchportal.tuni.fi/en/publications/technical-debt-impacting-lead-times-an-exploratory-study) also checked | Self-reported debt burden and contrary/qualified warning–lead-time evidence; not interchangeable outcomes. |
| SWE-CI, `10.48550/arXiv.2603.03823` | [v4](https://arxiv.org/html/2603.03823v4), 1 April 2026; abstract, §§2.1–2.3 and 3.1–3.2 | Historical base/target pairs with architect/programmer iterations and dynamic requirements. Already measures behavioral evolution; historical elapsed days are not days of agent execution. |
| StaminaBench, `10.48550/arXiv.2606.19613` | [v1](https://arxiv.org/html/2606.19613v1), 17 June 2026; abstract, Algorithm 1, §§3.1–3.2 and selected retry/harness discussion | Starts with agent-authored service, then generated changes. Feedback, test retries and process retries are distinct; none is silently adopted here. |
| RepoProbe, `10.48550/arXiv.2608.04783` | [v2](https://arxiv.org/html/2608.04783v2), 6 August 2026; bounded worker read §§3.1–3.2, 4.1–4.2, 5.1, 5.3–5.4 | Fixed repository/Q&A, 500 items/50 repositories; textual checklist, no edits. Inference from task definition: no assigned architecture followed by behavioral maintenance. |
| RepoMod-Bench, `10.48550/arXiv.2602.22518` | [v1](https://arxiv.org/html/2602.22518v1), 26 February 2026; worker read §§2.1–2.4, 3.1, Appendices A.2–A.4 | Source-to-target modernization with hidden black-box tests, architecture freedom, fresh main-run workspaces. Preliminary repeated-workspace iterations are explicitly separate; neither condition assigns credible starting architectures for later changes. |
| Yang, `10.48550/arXiv.2607.21674` | [v1 abstract](https://arxiv.org/abs/2607.21674v1), 23 July 2026; no body-methods reading | Output-format/model interaction motivation only; no effect sizes, best format or model ranking imported. |
| Sperber/Schlegel, `10.1145/3759163.3760429` | [author PDF](https://www.deinprogramm.de/sperber/papers/funarch-ui.pdf); selected §§1–9, 13–14 and bibliography. Crossref date 9 October 2025; workshop 12–18 October | MVC/MVU design tradeoffs, not ImGui or controlled downstream effects. Text search for “immediate” returned none; not a global absence claim. |
| Fowler, `10.4230/LIPIcs.ECOOP.2020.14` | Scite body unavailable; [proceedings PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol166-ecoop2020/LIPIcs.ECOOP.2020.14/LIPIcs.ECOOP.2020.14.pdf), introduction and §§2.1–2.2 selected passages | MVU is formalized with operational semantics. Related arXiv `1910.11108` and artifact `10.4230/DARTS.6.2.13` are not independent replications. |
| Elliott/Hudak, `10.1145/258948.258973` | Scite served 2,184-character fallback abstract, OCR artifacts and extraneous trailing matter; **not body text**. Author site failed | Only the clear abstract claim about time-varying behaviors/denotational treatment is used. Related `10.1145/258949.258973` is not another experiment. |
| Zuev et al., `10.20998/2413-4295.2025.02.08` | Scite 2,738-character abstract; Crossref and [publisher abstract](https://vestnik2079-5459.khpi.edu.ua/article/view/325758), published 20 July 2025. Primary PDF routes failed | Published immediate/retained comparison and implementation lead; claimed benefits are not accepted as a measured longitudinal effect. PDF/publisher author ordering differs; proposal uses et al. |
| Brendel/Liedtke, `10.18420/vrar2022_1678` | Scite metadata, no readable text; Crossref 404. [DataCite](https://api.datacite.org/dois/10.18420/vrar2022_1678) identifies 2022/GI and correct [repository item](https://dl.gi.de/items/c5202678-a861-47d5-8894-cfb7e57ee0bb). PowerShell HTTP 200, empty abstract element and restricted PDF indicator | Metadata-verified relevant lead only. Secondary search abstract is not substituted for primary methods. A guessed earlier GI handle was wrong/unverified and supplies no evidence; no copy request or access-control bypass. |

For Scite fulltext calls AT0–AT3, offsets were zero, length requested 8,000;
returned respectively 0, 2,738, 0 and 2,184 characters, none full text. The
service's fallback label matters. New Sperber reading was selected sections,
not a complete-paper critical appraisal. Prior GUI Easy/ALMA, methodology,
oracle, adaptive-optics and other benchmark readings retain the limits in the
initial section and linked earlier ledgers.

### Metadata failures resolved, not erased

- `10.1002/iis2.70208`: [Crossref](https://api.crossref.org/works/10.1002%2Fiis2.70208)
  returns Langmead, Padget, Waldman and Keeble, *Deployment of a Multi-Domain Model
  DSM based Approach for Automotive System Development: Improving Traceability
  and Security Impact Analysis*, INCOSE International Symposium 36(1),
  1564–1584. Registered print/issued date July 2026; online 11 September 2026.
  Crossref's type is journal-article despite the symposium venue. The
  2,266-character registered abstract was read; Wiley landing/full XML/PDF
  returned 403. It motivates adjacent AI-assisted impact analysis, not a
  verified architecture-maintenance comparison. Earlier unresolved status
  remains historical, not the current verdict.
- `10.1109/ICSA66085.2026.00033`: [Crossref](https://api.crossref.org/works/10.1109%2FICSA66085.2026.00033)
  identifies Sambu, Capuano, O'Dea, Vaidhyanathan and Muccini; ICSA 2026,
  pp. 268–279, issued June 2026, proceedings-article. Record creation on
  24 July is not publication date. No registered abstract; IEEE route returned
  202 and a PDF route returned anti-bot HTML, not paper text. Prior conference
  abstract remains the evidence.
- Zenodo `10.5281/zenodo.18622107` and `10.5281/zenodo.18622108`:
  DOI content negotiation verifies the same title/authors and issue date
  12 February 2026. DataCite relations explicitly say **18622107 HasVersion
  18622108 / 18622108 IsVersionOf 18622107**. Their 18,070-character description
  is a replication-package README, not an article abstract. Record API requests
  timed out after 20 seconds; no package PDF or full methods were read.
  Registry relationships establish version provenance, not independent studies.

Background metadata was also checked through Crossref's
`https://api.crossref.org/works/<URL-encoded DOI>` endpoint for
`10.1145/361598.361623`, `10.1145/2884781.2884822`,
`10.1145/3194164.3194178`, `10.1109/SEAA53835.2021.00032`,
`10.1145/3759163.3760429` and `10.20998/2413-4295.2025.02.08`.
These succeeded; the GI DOI is registered at DataCite, so its Crossref 404
does not mean the paper is missing. An arXiv export API call returned 429 once;
official abstract/HTML pages supplied RepoProbe/RepoMod evidence instead.

### Public Nu interpretation and exact sources

A reused Luna/Max worker owned only metadata/source extraction; the main agent
retained research design and claim acceptance. The Nu task used public source,
not private transcripts in the neighboring analysis. No files were edited by
the worker. The main agent separately checked the consequential MMCC gameplay
update/event passages after handoff.

| Public source identity | Reading/use |
| --- | --- |
| Nu `064f7ae92a8506689cd91aff5e6804a375d6ef3d`, 23 July 2026 | README, both Breakout trees and selected core dispatcher/content/ImSim/frame-loop ranges. Both examples real-time; manual versus engine physics remains a package confound. |
| [MMCC wiki revision](https://github.com/bryanedds/Nu/wiki/Model-View-Update-for-Games-via-MMCC/9cb6d2fe3865c68fd4ac3a945efb81946ef59174), 23 June 2025 | Author-stated MVU generalization, commands and recursive per-simulant organization. Not proof of enforced purity or representative prevalence. |
| [ImSim wiki revision](https://github.com/bryanedds/Nu/wiki/Immediate-Mode-for-Games-via-ImSim/e657be2c650864c4917fdf81f23e7775e76e9b95), 18 July 2025 | Author-stated declarative API and stack-based identity lineage. Not purely imperative or absence of domain state. |
| [Jump Box revision](https://github.com/bryanedds/Nu/wiki/Minimal-ImSim-Example-%28Jump-Box%29/e3771cec313e8181db2395adae368563ee646f3a), 4 November 2025 | Initialization/reload/dynamic synchronization operator explanations; core pinned source also inspected. |
| [Both top-level samples changed together](https://github.com/bryanedds/Nu/commit/e897941884bebeb6bba76a302b1cf0927a85ae66), 23 June 2026 | Same author/source lineage, not independently sampled architects. |
| [MMCC Gameplay](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Projects/Breakout%20Mmcc/Gameplay.fs#L85) | Model update each frame, world audio calls at lines 115/120/132/147, update/time events at 203–207. Effect separation is an intended organization, not enforced purity. |
| [Dear ImGui author wiki](https://github.com/ocornut/imgui/wiki/About-the-IMGUI-paradigm), displayed revision 3 October 2025; retrieved 14 September 2026 | Selected API-definition/limitations passages. No-state, no-events or continuous-loop requirements are rejected. Practitioner primary documentation, not a scholarly comparison. |

A malformed worker link was explicitly corrected to the pinned MMCC Gameplay
file before integration. Failed web opens of wiki revisions were not read as
absence; worker source-revision inspection and direct raw source reading supplied
evidence. No execution, equivalence, ideal purity or expert approval follows
from these source checks.

### Follow-up DOI inventory

C = credited for a qualified claim or explicitly marked access-limited lead.
E: unassessed = not selected for further body review, not a full-methods
rejection. E: off-topic = clear unrelated acronym/topic match.
E: related = related edition/artifact, not independent evidence.
**22 credited / 189 not credited Scite identifiers**; six additional canonical
bibliography DOIs reuse prior primary evidence or registry recovery above.
Positions are query-local returned ranks, not citation counts.

| DOI | Retrieval positions | Returned title | Disposition |
| --- | --- | --- | --- |
| `10.1109/seaa53835.2021.00032` | R0:1 | Technical Debt Impacting Lead-Times: An Exploratory Study | C |
| `10.1145/3194164.3194178` | R0:2 | Technical debt cripples software developer productivity | C |
| `10.1145/2884781.2884822` | R0:3 | Identifying and quantifying architectural debt | C |
| `10.1145/361598.361623` | R0:4 | On the criteria to be used in decomposing systems into modules | C |
| `10.48550/arxiv.2603.27745` | R1:1 | Needle in the Repo: A Benchmark for Maintainability in AI-Generated Repository Edits | C |
| `10.1145/3609025.3609478` | R1:2 | Functional Shell and Reusable Components for Easy GUIs | C |
| `10.48550/arxiv.2606.05574` | R1:3 | SmellBench: Towards Fine-Grained Evaluation of Code Agents on Refactoring Tasks | C |
| `10.48550/arxiv.2603.24755` | R1:4 | SlopCodeBench: Benchmarking How Coding Agents Degrade Over Long-Horizon Iterative Tasks | C |
| `10.48550/arxiv.2606.21804` | R1:5, R3b:26 | Is Agent Code Less Maintainable Than Human Code? | C |
| `10.48550/arxiv.2602.03712` | R1:6 | SWE-Refactor: A Repository-Level Benchmark for Real-World LLM-Based Code Refactoring | C |
| `10.1016/s0164-1212(03)00080-3` | R1:7 | Architecture-level modifiability analysis (ALMA) | C |
| `10.4230/lipics.ecoop.2020.14` | R1:8, A3:2 | Model-View-Update-Communicate: Session Types Meet the Elm Architecture | C |
| `10.48550/arxiv.2605.07001` | R1:9 | SmellBench: Evaluating LLM Agents on Architectural Code Smell Repair | C |
| `10.48550/arxiv.2511.06186` | R2:41 | Diagnosing and Resolving Android Applications Building Issues: An Empirical Study | E: unassessed |
| `10.48550/arxiv.2607.09510` | R2:42 | Failure as a Process: An Anatomy of CLI Coding Agent Trajectories | E: unassessed |
| `10.48550/arxiv.2604.24398` | R2:43 | MAS-SZZ: Multi-Agentic SZZ Algorithm for Vulnerability-Inducing Commit Identification | E: unassessed |
| `10.21203/rs.3.rs-10926809/v1` | R2:44 | A Concern-Centric Empirical Evaluation of Multi-Language Code Smells: An LLM-Assisted Study of JNI Software Evolution | E: unassessed |
| `10.48550/arxiv.2605.03956` | R2:45 | Generating Proof-of-Vulnerability Tests to Help Enhance the Security of Complex Software | E: unassessed |
| `10.1007/978-0-387-77743-6_21` | R2:46 | Software Evolution for Evolving ChinaSoftware Evolution for Evolving China | E: unassessed |
| `10.48550/arxiv.2601.14936` | R2:47 | LLM-Based Repair of C++ Implicit Data Loss Compiler Warnings: An Industrial Case Study | E: unassessed |
| `10.48550/arxiv.2606.31368` | R2:48 | MOA: A Profiling-Guided LLM Framework for Memory-Optimization Automation at Codebase Scale | E: unassessed |
| `10.3390/software5020019` | R2:49 | Investigating the Refactoring Capabilities of Small Open-Weight Language Models | E: unassessed |
| `10.48550/arxiv.2511.04012` | R2:50 | PSD2Code: Automated Front-End Code Generation from Design Files via Multimodal Large Language Models | E: unassessed |
| `10.1002/spe.70005` | R2:51 | Generative Artificial Intelligence for Software Engineering—A Research Agenda | E: unassessed |
| `10.48550/arxiv.2607.10411` | R2:52 | Mitigating LLM Sycophancy in Code Smell Detection Using Evidence-Guided Reasoning Prompts | E: unassessed |
| `10.48550/arxiv.2602.22020` | R2:53 | Detecting UX smells in Visual Studio Code using LLMs | E: unassessed |
| `10.21203/rs.3.rs-10418588/v1` | R2:54 | AST-Level Semantic Watermarking Framework for AI-Generated Code: Robust Provenance Attribution via Structural Invariants | E: unassessed |
| `10.48550/arxiv.2603.03194` | R2:55 | BeyondSWE: Can Current Code Agent Survive Beyond Single-Repo Bug Fixing? | E: unassessed |
| `10.48550/arxiv.2511.08177` | R2:56 | GazeCopilot: Evaluating Novel Gaze-Informed Prompting for AI-Supported Code Comprehension and Readability | E: unassessed |
| `10.48550/arxiv.2607.04092` | R2:57 | SEDCoT: Enhancing LLM-Based COBOL Code Translation via Symbolic Execution and Delta Debugging | E: unassessed |
| `10.3390/electronics13091644` | R2:58 | AI-Driven Refactoring: A Pipeline for Identifying and Correcting Data Clumps in Git Repositories | E: unassessed |
| `10.21203/rs.3.rs-3150943/v1` | R2:59 | A Machine Learning Based Three-Step Framework for Malicious URL Detection | E: unassessed |
| `10.48550/arxiv.2603.03823` | R2:60 | SWE-CI: Evaluating Agent Capabilities in Maintaining Codebases via Continuous Integration | C |
| `10.48550/arxiv.2511.01166` | R2b:61 | MicroRemed: Benchmarking LLMs in Microservices Remediation | E: unassessed |
| `10.48550/arxiv.2601.11655` | R2b:62 | Advances and Frontiers of LLM-based Issue Resolution in Software Engineering: A Comprehensive Survey | E: unassessed |
| `10.48550/arxiv.2606.06843` | R2b:63 | Empirical Study on the Characteristics and Evolution of AI-usage in GitHub Repositories: Evidence from Code Comments | E: unassessed |
| `10.48550/arxiv.2606.07341` | R2b:64 | Empirical Evaluation of Large Language Models for Migration of Code Fragments to Post-Quantum Cryptography | E: unassessed |
| `10.48550/arxiv.2511.08301` | R2b:65 | Smarter Together: Creating Agentic Communities of Practice through Shared Experiential Learning | E: unassessed |
| `10.48550/arxiv.2604.23667` | R2b:66 | Automated Classification of Human Code Review Comments with Large Language Models | E: unassessed |
| `10.48550/arxiv.2604.18413` | R2b:67 | TypeScript Repository Indexing for Code Agent Retrieval | E: unassessed |
| `10.21203/rs.3.rs-10508210/v1` | R2b:68 | QiboAgent: a practitioner's guideline to open source assistants for Quantum Computing code development | E: unassessed |
| `10.48550/arxiv.2512.17419` | R2b:69 | SWE-Bench++: A Framework for the Scalable Generation of Software Engineering Benchmarks from Open-Source Repositories | E: unassessed |
| `10.48550/arxiv.2511.13998` | R2b:70 | LoCoBench-Agent: An Interactive Benchmark for LLM Agents in Long-Context Software Engineering | E: unassessed |
| `10.48550/arxiv.2607.18462` | R2b:71 | Beyond Resolved Rate: A Non-Functional Quality Study | E: unassessed |
| `10.48550/arxiv.2510.06844` | R2b:72 | Oops!... I did it again. Analysing and Handling Conclusion (In-)Stability in Socio-Technical Software Engineering | E: unassessed |
| `10.48550/arxiv.2510.14778` | R2b:73 | Leveraging Code Cohesion Analysis to Identify Source Code Supply Chain Attacks | E: unassessed |
| `10.48550/arxiv.2511.00450` | R2b:74 | SmartDoc: A Context-Aware Agentic Method Comment Generation Plugin | E: unassessed |
| `10.48550/arxiv.2607.21674` | R2b:75 | Output Format x Model Identity: Interaction Effects in Single-Round Coding Agent Performance | C |
| `10.48550/arxiv.2602.02934` | R2b:76 | AgenticSZZ: Temporal Knowledge Graph-Guided Agentic Bug-Inducing Commit Identification | E: unassessed |
| `10.48550/arxiv.2606.19814` | R2b:77 | CoRaCommit: A VS Code Extension for Commit Message Generation with Exemplar Retrieval | E: unassessed |
| `10.48550/arxiv.2510.09721` | R2b:78 | A Comprehensive Survey on Benchmarks and Solutions in Software Engineering of LLM-Empowered Agentic System | E: unassessed |
| `10.48550/arxiv.2608.04783` | R2b:79 | RepoProbe: Benchmarking Architecture-Aware Repository Comprehension with Checklists | C |
| `10.48550/arxiv.2604.13648` | R2b:80 | Figma2Code: Automating Multimodal Design to Code in the Wild | E: unassessed |
| `10.48550/arxiv.2601.17406` | R3:1 | Fingerprinting AI Coding Agents on GitHub | E: unassessed |
| `10.48550/arxiv.2606.16545` | R3:2 | Can LLM Coding Agents Reason About Time Series? | E: unassessed |
| `10.48550/arxiv.2607.02134` | R3:3 | Coding-agents can replicate scientific machine learning papers | E: unassessed |
| `10.48550/arxiv.2604.20779` | R3:4 | SWE-chat: Coding Agent Interactions From Real Users in the Wild | E: unassessed |
| `10.48550/arxiv.2512.12216` | R3:5 | Training Versatile Coding Agents in Synthetic Environments | E: unassessed |
| `10.48550/arxiv.2606.19613` | R3:6 | StaminaBench: Stress-Testing Coding Agents over 100 Interaction Turns | C |
| `10.48550/arxiv.2607.14573` | R3:7 | Alipay-PIBench: A Realistic Payment Integration Benchmark for Coding Agents | E: unassessed |
| `10.48550/arxiv.2607.02911` | R3:8 | CoACT: Action-Preserving Observation Compression for Coding Agents | E: unassessed |
| `10.48550/arxiv.2605.08366` | R3:9 | SWE Atlas: Benchmarking Coding Agents Beyond Issue Resolution | E: unassessed |
| `10.48550/arxiv.2601.16746` | R3:10 | SWE-Pruner: Self-Adaptive Context Pruning for Coding Agents | E: unassessed |
| `10.48550/arxiv.2605.05138` | R3:11 | Executable World Models for ARC-AGI-3 in the Era of Coding Agents | E: unassessed |
| `10.48550/arxiv.2604.03515` | R3:12 | Inside the Scaffold: A Source-Code Taxonomy of Coding Agent Architectures | E: unassessed |
| `10.48550/arxiv.2603.17104` | R3:13 | When the Specification Emerges: Benchmarking Faithfulness Loss in Long-Horizon Coding Agents | E: unassessed |
| `10.48550/arxiv.2601.21372` | R3:14 | NEMO: Execution-Aware Optimization Modeling via Autonomous Coding Agents | E: unassessed |
| `10.48550/arxiv.2607.22711` | R3:15 | CORVUS: Context Optimization and Reduction Via Underlying Synchronization for LLM Coding Agents | E: unassessed |
| `10.48550/arxiv.2602.09892` | R3:16 | Immersion in the GitHub Universe: Scaling Coding Agents to Mastery | E: unassessed |
| `10.48550/arxiv.2512.03549` | R3:17 | PARC: An Autonomous Self-Reflective Coding Agent for Robust Execution of Long-Horizon Tasks | E: unassessed |
| `10.48550/arxiv.2606.10933` | R3:18 | Frontier Coding Agents Use Metaprogramming to Adapt to Unfamiliar Programming Languages | E: unassessed |
| `10.48550/arxiv.2605.06125` | R3:19 | Breaking, Stale, or Missing? Benchmarking Coding Agents on Project-Level Test Evolution | E: unassessed |
| `10.48550/arxiv.2606.26289` | R3:20 | Augmentation with Dilution: A Large-Scale Empirical Study of Human Contributor Ecosystems After AI Coding Agent Adoption | E: unassessed |
| `10.48550/arxiv.2607.01810` | R3b:21 | Decoupling Code Complexity from Newcomer Participation: A Causal Study of AI Coding Agent Adoption in OSS | E: unassessed |
| `10.48550/arxiv.2603.17973` | R3b:22 | TDAD: Test-Driven Agentic Development - Reducing Code Regressions in AI Coding Agents via Graph-Based Impact Analysis | E: unassessed |
| `10.48550/arxiv.2607.13080` | R3b:23 | Inference Economics of Enterprise Coding Agents: A Case Study of Cloud vs. On-Premise LLMs | E: unassessed |
| `10.48550/arxiv.2604.14609` | R3b:24 | El Agente Forjador: Task-Driven Agent Generation for Quantum Simulation | E: unassessed |
| `10.48550/arxiv.2510.19868` | R3b:25 | Knowledge-Guided Multi-Agent Framework for Application-Level Software Code Generation | E: unassessed |
| `10.48550/arxiv.2510.12399` | R3b:27 | A Survey of Vibe Coding with Large Language Models | E: unassessed |
| `10.48550/arxiv.2604.19022` | R3b:28 | On Accelerating Grounded Code Development for Research | E: unassessed |
| `10.48550/arxiv.2511.11012` | R3b:29 | Beyond Accuracy: Behavioral Dynamics of Agentic Multi-Hunk Repair | E: unassessed |
| `10.48550/arxiv.2607.15970` | R3b:30 | Code-Poisoning Property Inference Attacks | E: unassessed |
| `10.48550/arxiv.2606.19235` | R3b:31 | CodeSentinel: A Three-Layer Defense Against Indirect Prompt Injection in Code Contexts | E: unassessed |
| `10.64898/2026.07.29.741496` | R3b:32 | Scientific computing in the age of agentic AI: an exploratory field report | E: unassessed |
| `10.48550/arxiv.2606.30573` | R3b:33 | SWE-INTERACT: Reimagining SWE Benchmarks as User-Driven Long-Horizon Coding Sessions | E: unassessed |
| `10.64898/2026.01.09.26343542` | R3b:34 | ClinAgent: A Five-Layer Architecture for Autonomous Clinical Trial Statistical Programming | E: unassessed |
| `10.48550/arxiv.2607.10621` | R3b:35 | WebDesignIter: Co-Evolving Design Knowledge for Repository-Level Front-End Code Generation | E: unassessed |
| `10.48550/arxiv.2603.27277` | R3b:36 | Codebase-Memory: Tree-Sitter-Based Knowledge Graphs for LLM Code Exploration via MCP | E: unassessed |
| `10.48550/arxiv.2603.13640` | R3b:37 | SemRep: Generative Code Representation Learning with Code Transformations | E: unassessed |
| `10.48550/arxiv.2601.13943` | R3b:38 | RepoGenesis: Benchmarking End-to-End Microservice Generation from Readme to Repository | E: unassessed |
| `10.48550/arxiv.2601.02200` | R3b:39 | Code for Machines, Not Just Humans: Quantifying AI-Friendliness with Code Health Metrics | E: unassessed |
| `10.48550/arxiv.2602.22518` | R3b:40 | RepoMod-Bench: A Benchmark for Code Repository Modernization via Implementation-Agnostic Testing | C |
| `10.1002/ijch.202200077` | A1:1 | Ligand‐Directed Chemistry for Protein Labeling for Affinity‐Based Protein Analysis | E: off-topic |
| `10.31374/sjms.90` | A1:2 | Sovereignty and Transnational Cooperation in the Gulf of Guinea: How a Network Approach can Strengthen the Yaoundé Architecture | E: off-topic |
| `10.1002/qua.20753` | A1:3 | Automated derivation and parallel computer implementation of renormalized and active‐space coupled‐cluster methods | E: off-topic |
| `10.48550/arxiv.2010.15710` | A1:4 | MIRISim: A Simulator for the Mid-Infrared Instrument on JWST | E: off-topic |
| `10.1371/journal.pone.0245264` | A1:5 | Enhancing web search result clustering model based on multiview multirepresentation consensus cluster ensemble (mmcc) approach | E: off-topic |
| `10.32604/cmc.2024.051916` | A1:6 | A GAN-EfficientNet-Based Traceability Method for Malicious Code Variant Families | E: off-topic |
| `10.1109/tia.2019.2934024` | A1:7 | A DC-Link Capacitor Voltage Ripple Reduction Method for a Modular Multilevel Cascade Converter With Single Delta Bridge Cells | E: off-topic |
| `10.21236/ada246330` | A1:8 | A Distributed Architecture for Multimedia Conference Control | E: off-topic |
| `10.1038/s41598-022-17351-4` | A1:9 | Multidirectional motion coupling based extreme motion control of distributed drive autonomous vehicle | E: off-topic |
| `10.1177/30504554241311177` | A1:10 | Learned Lossless Image Compression Based on Optimal Kernel Transformer Approach | E: off-topic |
| `10.1049/pel2.70071` | A1:11 | Simplified Control for an SSBC‐Based STATCOM | E: off-topic |
| `10.18618/rep.2020.2.0011` | A1:12 | A Flexible DSP-FPGA Based Platform for Experiments with Modular Multilevel Cascade Converters | E: off-topic |
| `10.35483/acsa.aia.inter.21.27` | A1:13 | Community Health Design: A Collaborative Framework for Improving Public Health Outcomes | E: off-topic |
| `10.3390/pr9060929` | A1:14 | MalCaps: A Capsule Network Based Model for the Malware Classification | E: off-topic |
| `10.3390/electronics11203377` | A1:15 | More than Meets One Core: An Energy-Aware Cost Optimization in Dynamic Multi-Core Processor Server Consolidation for Cloud Data Center | E: off-topic |
| `10.3389/fnins.2022.850932` | A1:16 | Heterogeneous Ensemble-Based Spike-Driven Few-Shot Online Learning | E: off-topic |
| `10.1049/iet-pel.2012.0494` | A1:17 | Generalised analytical methods and current‐energy control design for modular multilevel cascade converter | E: off-topic |
| `10.1107/s1600576720013412` | A1:18 | ATSAS 3.0: expanded functionality and new tools for small-angle scattering data analysis | E: off-topic |
| `10.1016/j.dark.2018.11.002` | A1:19 | lenstronomy: Multi-purpose gravitational lens modelling software package | E: off-topic |
| `10.48550/arxiv.1207.6381` | A1:20 | Efficient implementations of minimum-cost flow algorithms | E: off-topic |
| `10.20998/2413-4295.2025.02.08` | A2:1, A4:1 | ALGORITHM AND SOFTWARE IMPLEMENTATION OF IMMEDIATE MODE INTERFACE FOR VISUALIZATION SYSTEMS | C |
| `10.1145/1044588.1044593` | A2:2 | Network aware parallel rendering with PCs | E: unassessed |
| `10.1145/280814.280837` | A2:3, A4:5 | The design of a parallel graphics interface | E: unassessed |
| `10.71097/ijsat.v17.i1.10200` | A2:4 | Parallel Editing in p5.js and Paper.js with ShareDB: An OT‑based Architecture and a CRDT Metadata Lane | E: unassessed |
| `10.5772/9502` | A2:5, A4:3 | Embedded User Interface for Mobile Applications to Satisfy Design for All Principles | E: unassessed |
| `10.1145/1315184.1315209` | A2:6 | Building high performance DVR via HLA, scene graph and parallel rendering | E: unassessed |
| `10.5220/0001350903420348` | A2:7 | A NEW METHOD FOR BUILDING LARGE-FORMAT TILED DISPLAYS SYSTEMS | E: unassessed |
| `10.1109/visual.2005.1532787` | A2:8 | A Shader-Based Parallel Rendering Framework | E: unassessed |
| `10.1109/vis.2005.6` | A2:9 | A Shader-Based Parallel Rendering Framework | E: unassessed |
| `10.1109/vrais.1998.658503` | A2:10, A4:12 | Bamboo-a portable system for dynamically extensible, real-time, networked, virtual environments | E: unassessed |
| `10.11610/isij.0305` | A2:11 | Fuzzy Controller for Antitank Wire Guided Missile Simulator with Direct X SDK | E: unassessed |
| `10.25046/aj070605` | A2:12 | Advantages of 3D Technology in Stereometry Training | E: unassessed |
| `10.1007/3-540-49201-1_5` | A2:13 | From Functional Animation to Sprite-Based Display | E: unassessed |
| `10.4028/www.scientific.net/amm.421.672` | A2:14 | Research of Efficiency of Computer 3D Animation | E: unassessed |
| `10.1109/pvgs.2003.1249041` | A2:15 | Sort-first, distributed memory parallel visualization and rendering | E: unassessed |
| `10.2118/27545-pa` | A2:16 | An Object-Oriented Solution to an Interdisciplinary 3D Visualization Tool | E: unassessed |
| `10.1093/bioinformatics/btg104` | A2:17 | FPV: fast protein visualization using Java 3DTM | E: unassessed |
| `10.1007/978-3-540-77129-6_10` | A2:18 | Out-of-Order Execution for Avoiding Head-of-Line Blocking in Remote 3D Graphics | E: unassessed |
| `10.1002/cpe.4377` | A2:19 | CoderLabs: A cloud‐based platform for real‐time online labs with user collaboration | E: unassessed |
| `10.1145/1508044.1508085` | A2:20 | A survey and performance analysis of software platforms for interactive cluster-based multi-screen rendering | E: unassessed |
| `10.1109/vr.2006.20` | A2b:21 | A Survey of Large High-Resolution Display Technologies, Techniques, and Applications | E: unassessed |
| `10.11610/isij.0317` | A2b:22 | Monitor Research Centers | E: unassessed |
| `10.1007/978-1-4842-4427-2_19` | A2b:23 | Cinematic Rendering in UE4 with Real-Time Ray Tracing and Denoising | E: unassessed |
| `10.1145/142920.134067` | A2b:24 | PixelFlow: high-speed rendering using image composition | E: unassessed |
| `10.1109/sibgra.2004.1352973` | A2b:25 | A load-balancing strategy for sort-first distributed rendering | E: unassessed |
| `10.1145/133994.134067` | A2b:26 | PixelFlow: high-speed rendering using image composition | E: unassessed |
| `10.1142/s0219467801000098` | A2b:27 | TOM: TOTALLY ORDERED MESH A MULTIRESOLUTION STRUCTURE FOR TIME CRITICAL GRAPHICS APPLICATIONS | E: unassessed |
| `10.1016/s0306-4379(98)00002-7` | A2b:28 | Concurrent rule execution in active databases | E: unassessed |
| `10.1109/sc.2000.10003` | A2b:29 | Distributed Rendering for Scalable Displays | E: unassessed |
| `10.22215/etd/2015-11133` | A2b:30 | ACH Walkthrough: Designing and Building a Web Application for Collaborative Sensemaking | E: unassessed |
| `10.1007/978-3-031-03789-4_18` | A2b:31 | Modern Evolution Strategies for Creativity: Fitting Concrete Images and Abstract Concepts | E: unassessed |
| `10.32657/10356/2592` | A2b:32 | Framework for a realtime distributed rendering environment | E: unassessed |
| `10.1142/9781860949524_0194` | A2b:33 | A FRAMEWORK FOR A REAL-TIME DISTRIBUTED RENDERING ENVIRONMENT | E: unassessed |
| `10.1109/2945.556501` | A2b:34 | Interactive display of large NURBS models | E: unassessed |
| `10.11606/d.3.2008.tde-18022009-165517` | A2b:35 | Uma metodologia para o desenvolvimento de aplicações de realidade aumentada em telefones celulares utilizando dispositivos sensores. | E: unassessed |
| `10.47749/t/unicamp.2007.411113` | A2b:36 | Uma arquitetura de suporte a interações 3D integrada a GPU | E: unassessed |
| `10.1145/2661229.2661274` | A2b:37 | Massively-parallel vector graphics | E: unassessed |
| `10.48550/arxiv.1910.11108` | A3:1 | Model-View-Update-Communicate: Session Types meet the Elm Architecture | E: related |
| `10.4230/darts.6.2.13` | A3:3 | Model-View-Update-Communicate: Session Types Meet the Elm Architecture (Artifact) | E: related |
| `10.1007/978-1-4842-2610-0_5` | A3:4 | Elm Architecture and Building Blocks | E: unassessed |
| `10.1007/978-3-030-37051-0_98` | A3:5 | A Novel Hybrid RNN-ELM Architecture for Crime Classification | E: unassessed |
| `10.1109/ijcnn.2015.7280603` | A3:6 | OXRAM based ELM architecture for multi-class classification applications | E: unassessed |
| `10.21504/rur.32900561.v1` | A3:7 | Demo Elm code for complex interactions and a design pattern to handle them | E: unassessed |
| `10.21504/rur.32900561` | A3:8 | Demo Elm code for complex interactions and a design pattern to handle them | E: unassessed |
| `10.1109/tnano.2015.2441112` | A3:9 | Exploiting Intrinsic Variability of Filamentary Resistive Memory for Extreme Learning Machine Architectures | E: off-topic |
| `10.1108/compel-07-2020-0246` | A3:10 | Using optimal choice of parameters for meta-extreme learning machine method in wind energy application | E: off-topic |
| `10.4204/eptcs.363.8` | A3:11, A5a:7 | Teaching Interaction using State Diagrams | E: unassessed |
| `10.1002/cpe.7231` | A3:12 | A systematic review on machine learning algorithms used for forecasting lake‐water level fluctuations | E: off-topic |
| `10.1111/exsy.13432` | A3:13 | An optimized extreme learning machine‐based novel model for bearing fault classification | E: off-topic |
| `10.1364/boe.549363` | A3:14 | Fast blood flow index reconstruction of diffuse correlation spectroscopy using a back-propagation-free data-driven algorithm | E: off-topic |
| `10.1038/s41598-025-16798-5` | A3:15 | M-estimation activation functions for high-performance extreme learning machine ensemble classification | E: off-topic |
| `10.14428/esann/2023.es2023-31` | A3:16 | Performance Evaluation of Activation Functions in Extreme Learning Machine | E: off-topic |
| `10.18517/ijaseit.8.5.5006` | A3:17 | Early Detection of Dengue Disease Using Extreme Learning Machine | E: off-topic |
| `10.1007/978-3-319-67792-7_1` | A3:18 | Deep Learning with Dense Random Neural Networks | E: unassessed |
| `10.3233/idt-210152` | A3:19 | A novel MCDM ensemble approach of designing an ELM based predictor for stock index price forecasting | E: unassessed |
| `10.1007/s11334-022-00486-y` | A3:20 | Forecasting adversities of COVID-19 waves in India using intelligent computing | E: unassessed |
| `10.21236/ada308276` | A4:2 | Implementation of a Rule-Based Framework for Managing Updates in an Object-Oriented VPF Database, | E: unassessed |
| `10.1109/ismar.2008.4637354` | A4:4 | ComposAR: An intuitive tool for authoring AR applications | E: unassessed |
| `10.1007/978-3-662-10874-1_12` | A4:6 | Active XML: A Data-Centric Perspective on Web Services | E: unassessed |
| `10.1101/2023.10.24.563727` | A4:7 | PhysiCell Studio: a graphical tool to make agent-based modeling more accessible | E: unassessed |
| `10.1109/sibgrapi-t.2012.10` | A4:8 | Interactive Graphics Applications with OpenGL Shading Language and Qt | E: unassessed |
| `10.3758/s13428-019-01245-x` | A4:9 | Ratcave: A 3D graphics python package for cognitive psychology experiments | E: unassessed |
| `10.1109/oceanse.2019.8867434` | A4:10 | Stonefish: An Advanced Open-Source Simulation Tool Designed for Marine Robotics, With a ROS Interface | E: unassessed |
| `10.46471/gigabyte.128` | A4:11 | PhysiCell Studio: a graphical tool to make agent-based modeling more accessible | E: unassessed |
| `10.21105/joss.02791` | A4:13 | s4rdm3x: A Tool Suite to Explore Code to Architecture Mapping Techniques | E: unassessed |
| `10.1109/2.19829` | A4:14 | Composing user interfaces with InterViews | E: unassessed |
| `10.1109/cvprw.2014.100` | A4:15 | Addressing System-Level Optimization with OpenVX Graphs | E: unassessed |
| `10.1016/j.softx.2021.100945` | A4:16 | PlatformCommander — An open source software for an easy integration of motion platforms in research laboratories | E: unassessed |
| `10.22214/ijraset.2022.45595` | A4:17 | Algorithmic Trading Stock Price Model | E: unassessed |
| `10.1145/71031.71034` | A4:18 | Rule management and evaluation: an active DBMS perspective | E: unassessed |
| `10.3390/computation3030444` | A4:19 | Towards Online Visualization and Interactive Monitoring of Real-Time CFD Simulations on Commodity Hardware | E: unassessed |
| `10.5753/jis.2011.605` | A4:20 | A Case Study of Augmented Reality for Mobile Platforms | E: unassessed |
| `10.1145/3689728` | A5a:1 | Statically Contextualizing Large Language Models with Typed Holes | E: unassessed |
| `10.48550/arxiv.2607.27074` | A5a:2 | A Type-and-Effect System for Temporal Dependency Analysis of Render-based Reactive Programs | E: unassessed |
| `10.3389/fninf.2013.00028` | A5a:3 | Reaction-diffusion in the NEURON simulator | E: unassessed |
| `10.36227/techrxiv.14212571.v1` | A5a:4 | Choosing a Global Architecture for Mobile Applications | E: unassessed |
| `10.1145/3519939.3523728` | A5a:5 | Quickstrom: property-based acceptance testing with LTL specifications | E: unassessed |
| `10.48550/arxiv.2203.11532` | A5a:6 | Quickstrom: Property Based Acceptance Testing with LTL Specifications | E: unassessed |
| `10.1111/1467-8659.1430003` | A5a:8 | Distributed Augmented Reality for Collaborative Design Applications | E: unassessed |
| `10.48550/arxiv.2005.11841` | A5a:9 | scadnano: A browser-based, scriptable tool for designing DNA nanostructures | E: unassessed |
| `10.1145/3397495` | A5a:10 | A Survey of Multitier Programming | E: unassessed |
| `10.1145/3412932.3412945` | A5a:11 | Language-integrated updatable views | E: unassessed |
| `10.48550/arxiv.2003.02191` | A5a:12 | Language-Integrated Updatable Views (Extended version) | E: unassessed |
| `10.1101/2024.07.15.603553` | A5a:13 | NanoLAS 2.0: A Comprehensive Update on a Nanobody-Focused Platform with Advanced Visualization and Docking Simulation Features | E: unassessed |
| `10.4204/eptcs.314.2` | A5a:14 | Generating Interactive WebSocket Applications in TypeScript | E: unassessed |
| `10.1007/978-3-642-38911-5_13` | A5a:15 | Refactorings in Language Development with Asymmetric Bidirectional Model Transformations | E: unassessed |
| `10.1145/3356590.3356633` | A5a:16 | Mental Models of Loudspeaker Directivity | E: unassessed |
| `10.48550/arxiv.2107.10793` | A5a:17 | A Typed Slicing Compilation of the Polymorphic RPC Calculus | E: unassessed |
| `10.1007/s10270-017-0622-9` | A5a:18 | A feature-based survey of model view approaches | E: unassessed |
| `10.1145/3479394.3479406` | A5a:19 | A Typed Slicing Compilation of the Polymorphic RPC calculus | E: unassessed |
| `10.1017/s0956796800003671` | A7:1 | A functional reactive animation of a lift using Fran | E: unassessed |
| `10.1145/258949.258973` | A7:2 | Functional reactive animation | E: related |
| `10.1145/3609023.3609806` | A7:3 | The Beauty and Elegance of Functional Reactive Animation | E: unassessed |
| `10.18420/vrar2022_1678` | A7:4 | Exploring the immediate mode GUI concept for graphical user interfaces in mixed reality applications | C |
| `10.1145/258948.258973` | A7:5 | Functional reactive animation | C |
| `10.2197/ipsjjip.33.368` | A7:6 | Functional Reactive Animation with Functions of Time | E: unassessed |
| `10.1145/3759163.3760429` | A7:7 | Evolution of Functional UI Paradigms | C |
| `10.1093/aesa/30.3.549` | A8:1 | Nearctic Collembola Or Springtails of the Family Isotomidae | E: off-topic |
| `10.5962/bhl.title.16542` | A8:2 | The elements of botany ... Being a translation of the Philosophia botanica, and other treatises of the celebrated Linnæus, to which is added an appendix, wherein are described some plants lately found in Norfolk and Suffolk | E: off-topic |

### Web discovery and endpoint disposition

New web discovery strings are retained below. Exact primary opens, registry
requests and selected sections are documented above. RWeb2 used
`"On the criteria to be used in decomposing systems into modules" filetype:pdf`
and `"Technical Debt Impacting Lead-Times" 2021`.

- AWeb0: `"model view update" "immediate mode" comparison`
- AWeb0: `"immediate mode" "retained mode" GUI empirical study`
- AWeb0: `"MMCC" "operational" Nu`
- AWeb0: `"ImSim" "mathematical"`
- AWeb1: `"immediate mode" "retained mode" "study" GUI -site:reddit.com -site:stackoverflow.com -site:gamedev.stackexchange.com`
- AWeb1: `"Model-View-Update" "comparison" GUI paper`
- AWeb1: `"immediate mode" "Elm" thesis`
- AWeb1: `"Exploring the immediate mode GUI concept"`
- AWeb4: `"10.18420/vrar2022_1678"`
- AWeb4: `"10.20998/2413-4295.2025.02.08"`
- AWeb4: `site:conal.net "Functional Reactive Animation" semantics`
- AWeb8: `"immediate mode" "retained mode" thesis comparison GUI`
- AWeb8: `"Elm" "ImGui" comparison study paper`
- AWeb8: `"Functional reactive animation" filetype:pdf Elliott Hudak`
- AWeb8: `"model view update" "immediate" comparison architecture -site:reddit.com -site:researchgate.net`

The following 119 distinct web discovery/attempt endpoints include aliases,
secondary pages and unavailable routes; they are **not 119 studies**. C credits
only the specific primary metadata/text use above; E does not claim a complete
assessment. A practitioner page is not promoted to peer-reviewed evidence.
The Lambda Days PDF was Terrell's 2016 slide deck, **not** the Elliott/Hudak
article despite the search snippet; it was not used as that primary paper.
Registry and worker-specific routes are separately recorded above and in the
final audit. No authentication-bearing Scite access links are published.

| Retrieval | Endpoint | Use |
| --- | --- | --- |
| RWeb1 | [Endpoint](https://personal.stevens.edu/~lxiao6/papers/ICSE-16-Debt.pdf) | C: scoped primary |
| RWeb1 | [Endpoint](https://arxiv.org/html/2603.24755v2) | C: scoped primary |
| RWeb2 | [Endpoint](https://citeseerx.ist.psu.edu/document?doi=5d752e29e29b42cc509417699a98d9dca8212c83&repid=rep1&type=pdf) | E: discovery only |
| RWeb2 | [Endpoint](https://ckrybus.com/static/papers/decomposing_systems_into_modules_1972.pdf) | E: discovery only |
| RWeb2, RWeb3, RWeb4 | [Endpoint](https://john.cs.olemiss.edu/~hcc/csci555/notes/localcopy/Parnas_Criteria_Decomposing.pdf) | C: scoped primary |
| RWeb2 | [Endpoint](https://doi.org/10.1184/r1/6607958) | E: discovery only |
| RWeb2 | [Endpoint](https://www.citedrive.com/en/discovery/on-the-criteria-to-be-used-in-decomposing-systems-into-modules/) | E: discovery only |
| RWeb2 | [Endpoint](https://www.scribd.com/document/259536877/lect-3-1) | E: discovery only |
| RWeb2 | [Endpoint](https://id.scribd.com/document/386209993/3-Rom-PDF-Parnas-New) | E: discovery only |
| RWeb2 | [Endpoint](https://researchportal.tuni.fi/en/publications/technical-debt-impacting-lead-times-an-exploratory-study) | C: scoped primary |
| RWeb2 | [Endpoint](https://www.rankless.org/hit-papers/10.1145/361598.361623) | E: discovery only |
| RWeb2 | [Endpoint](https://inigomedina.co/library/work/parnas-criteria-decomposing-modules) | E: discovery only |
| RWeb2 | [Endpoint](https://www.scribd.com/document/827024425/On-the-Criteria-to-Be-Used-in-Decomposing-Systems-Into-Modules) | E: discovery only |
| RWeb2 | [Endpoint](https://www.sciencedirect.com/science/article/pii/0010465585900840) | E: discovery only |
| RWeb2 | [Endpoint](https://www.researchgate.net/publication/3076981_Toward_a_Product_System_Modularity_Construct_Literature_Review_and_Reconceptualization) | E: discovery only |
| RWeb2 | [Endpoint](https://www.researchgate.net/publication/283566310_Improving_Design_Decomposition) | E: discovery only |
| RWeb2 | [Endpoint](https://principles-wiki.net/resources%3Aon_the_criteria_to_be_used_in_decomposing_systems_into_modules) | E: discovery only |
| RWeb2 | [Endpoint](https://de.wikipedia.org/wiki/Cross-Cutting_Concern) | E: discovery only |
| RWeb2 | [Endpoint](https://en.wikipedia.org/wiki/David_Parnas) | E: discovery only |
| RWeb2 | [Endpoint](https://en.wikipedia.org/wiki/Cross-cutting_concern) | E: discovery only |
| RWeb2 | [Endpoint](https://en.wikipedia.org/wiki/Flow-based_programming) | E: discovery only |
| RWeb2 | [Endpoint](https://en.wikipedia.org/wiki/Decomposition_%28computer_science%29) | E: discovery only |
| RWeb2 | [Endpoint](http://sunnyday.mit.edu/16.355/parnas-criteria.html) | E: discovery only |
| RWeb2 | [Endpoint](https://fr.wikipedia.org/wiki/Liste_de_publications_importantes_en_informatique) | E: discovery only |
| RWeb5 | [Endpoint](https://arxiv.org/abs/2603.03823) | C: scoped primary |
| RWeb5 | [Endpoint](https://arxiv.org/abs/2606.19613) | C: scoped primary |
| RWeb5, RWeb8 | [Endpoint](https://arxiv.org/abs/2607.21674) | C: scoped primary |
| RWeb6, RWeb7, RWeb8, RWeb9 | [Endpoint](https://arxiv.org/html/2603.03823v4) | C: scoped primary |
| RWeb6, RWeb7, RWeb8, RWeb9 | [Endpoint](https://arxiv.org/html/2606.19613v1) | C: scoped primary |
| AWeb0 | [Endpoint](https://github.com/idircarlos/zraygui) | E: discovery only |
| AWeb0 | [Endpoint](https://imsm.mimuw.edu.pl/study.php) | E: discovery only |
| AWeb0 | [Endpoint](https://stackoverflow.com/questions/47444189/what-are-the-performance-implications-of-using-an-immediate-mode-gui-compared-to?noredirect=1) | E: discovery only |
| AWeb0 | [Endpoint](https://forum.snap.berkeley.edu/t/immediate-mode-gui/22165) | E: discovery only |
| AWeb0 | [Endpoint](https://lobste.rs/s/coy6gt/why_is_building_ui_rust_so_hard) | E: discovery only |
| AWeb0 | [Endpoint](https://lobste.rs/s/kqtie6/c_ui_libraries) | E: discovery only |
| AWeb0 | [Endpoint](https://xc-jp.github.io/blog-posts/2022/11/22/python-model-view-update-frameworks.html) | E: discovery only |
| AWeb0 | [Endpoint](https://conf.researchr.org/details/plnl-2024/plnl-2024/1/Salix-Elm-style-Web-programming-in-Rascal-an-exercise-in-library-design) | E: discovery only |
| AWeb0, AWeb1, AWeb4 | [Endpoint](https://www.researchgate.net/publication/386416751_Exploring_the_immediate_mode_GUI_concept_for_graphical_user_interfaces_in_mixed_reality_applications) | E: discovery only |
| AWeb0 | [Endpoint](https://real-eod.mtak.hu/2003/1/SZTAKITanulmanyok_100.pdf) | E: discovery only |
| AWeb0, AWeb8 | [Endpoint](https://gamedev.stackexchange.com/questions/24103/immediate-gui-yae-or-nay) | E: discovery only |
| AWeb0, AWeb8 | [Endpoint](https://learn.microsoft.com/en-us/windows/win32/learnwin32/retained-mode-versus-immediate-mode) | E: discovery only |
| AWeb0 | [Endpoint](https://blog.goingforbrooke.com/rust-guis/) | E: discovery only |
| AWeb0 | [Endpoint](https://api.pageplace.de/preview/DT0400.9780133373707_A23602794/preview-9780133373707_A23602794.pdf) | E: discovery only |
| AWeb0 | [Endpoint](https://www.pesco.europa.eu/wp-content/uploads/2024/11/2024-DE-European-Medical-Command-EMC-Website-leaflet.pdf) | E: discovery only |
| AWeb0 | [Endpoint](https://en.wikipedia.org/wiki/Multinational_Medical_Coordination_Centre/European_Medical_Command) | E: discovery only |
| AWeb0 | [Endpoint](https://ntrs.nasa.gov/api/citations/20000120039/downloads/20000120039.pdf) | E: discovery only |
| AWeb0 | [Endpoint](https://www.reddit.com/r/gameenginedevs/comments/1ew5djv) | E: discovery only |
| AWeb0 | [Endpoint](https://www.marines.mil/Portals/1/Publications/MCTP%203-40F.pdf) | E: discovery only |
| AWeb0 | [Endpoint](https://www.cse.chalmers.se/edu/year/2011/course/TDA361/Advanced%20Computer%20Graphics/IMGUI.pdf) | E: discovery only |
| AWeb0 | [Endpoint](https://www.reddit.com/r/gameenginedevs/comments/1drusgv) | E: discovery only |
| AWeb0 | [Endpoint](https://de.wikipedia.org/wiki/Multinational_Medical_Coordination_Centre-Europe) | E: discovery only |
| AWeb0, AWeb8 | [Endpoint](https://www.reddit.com/r/GraphicsProgramming/comments/1jsuby6) | E: discovery only |
| AWeb0 | [Endpoint](https://it.wikipedia.org/wiki/Centro_multinazionale_di_coordinamento_medico/Comando_medico_europeo) | E: discovery only |
| AWeb0, AWeb8 | [Endpoint](https://en.wikipedia.org/wiki/Immediate_mode_%28computer_graphics%29) | E: discovery only |
| AWeb0 | [Endpoint](https://www.reddit.com/r/C_Programming/comments/1fyblps) | E: discovery only |
| AWeb0, AWeb8 | [Endpoint](https://en.wikipedia.org/wiki/Retained_mode) | E: discovery only |
| AWeb0 | [Endpoint](https://www.reddit.com/r/programming/comments/1vrtje0/how_an_immediate_mode_ui_shirei_retains_component/) | E: discovery only |
| AWeb0 | [Endpoint](https://www.reddit.com/r/gameenginedevs/comments/1ozp9z4/why_are_retained_mode_guis_so_rarely_used_in_game/) | E: discovery only |
| AWeb0, AWeb8 | [Endpoint](https://www.reddit.com/r/explainlikeimfive/comments/eugfbr) | E: discovery only |
| AWeb0, AWeb8 | [Endpoint](https://ru.wikipedia.org/wiki/%D0%93%D1%80%D0%B0%D1%84%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9_%D0%B8%D0%BD%D1%82%D0%B5%D1%80%D1%84%D0%B5%D0%B9%D1%81_%D0%BD%D0%B5%D0%BC%D0%B5%D0%B4%D0%BB%D0%B5%D0%BD%D0%BD%D0%BE%D0%B3%D0%BE_%D1%80%D0%B5%D0%B6%D0%B8%D0%BC%D0%B0) | E: discovery only |
| AWeb0 | [Endpoint](https://www.reddit.com/r/GraphicsProgramming/comments/1mzsux1) | E: discovery only |
| AWeb0 | [Endpoint](https://www.reddit.com/r/programming/comments/ggg7io) | E: discovery only |
| AWeb0, AWeb8 | [Endpoint](https://www.reddit.com/r/opengl/comments/190wrxv) | E: discovery only |
| AWeb1, AWeb2, AWeb3, AWeb6 | [Endpoint](https://www.deinprogramm.de/sperber/papers/funarch-ui.pdf) | C: scoped primary |
| AWeb1 | [Endpoint](https://fhoehl.com/future-browser) | E: discovery only |
| AWeb1 | [Endpoint](https://drops.dagstuhl.de/entities/volume/LIPIcs-volume-166) | E: discovery only |
| AWeb1 | [Endpoint](https://github.com/cben/model-view-self-modify) | E: discovery only |
| AWeb1 | [Endpoint](https://zbornik.ftn.uns.ac.rs/index.php/zbornik/article/download/64/84/425) | E: discovery only |
| AWeb1 | [Endpoint](https://ethz.ch/content/dam/ethz/special-interest/infk/inst-pls/arv-dam/documents/bachelors-theses/lugic-bsc-thesis.pdf) | E: discovery only |
| AWeb1 | [Endpoint](https://oboe.com/learn/interfaces-grficas-modernas-com-rust-1rgovta/study-guide) | E: discovery only |
| AWeb1 | [Endpoint](https://drops.dagstuhl.de/storage/01oasics/oasics-vol109-evcs2023/OASIcs.EVCS.2023/OASIcs.EVCS.2023.pdf) | E: discovery only |
| AWeb1, AWeb4 | [Endpoint](https://vestnik2079-5459.khpi.edu.ua/article/view/325758/325661) | E: access/unverified |
| AWeb1 | [Endpoint](https://github.com/BuLEEto/Skald/) | E: discovery only |
| AWeb1 | [Endpoint](https://deepwiki.com/lustre-labs/lustre/2.1-model-view-update-pattern) | E: discovery only |
| AWeb1 | [Endpoint](https://ipfire.infania.net/pdf/interdata/32bit/os32/1986_8.1.2/48-047F00R01_OS32_Asynchronous_Communications_Reference_Manual_1986.pdf) | E: discovery only |
| AWeb1 | [Endpoint](https://cse135.site/dataviz-overview.html) | E: discovery only |
| AWeb1 | [Endpoint](https://www.mauricepeters.dev/2023/10/model-view-update-mvu-pattern-using-asp.html) | E: discovery only |
| AWeb1 | [Endpoint](https://www.researchgate.net/publication/294238106_User_Interface_for_the_SMAC_Traffic_Accident_Reconstruction_Program) | E: discovery only |
| AWeb1 | [Endpoint](https://analysis.4sceners.de/blog/model-view-catharsis/) | E: discovery only |
| AWeb1 | [Endpoint](https://www.researchgate.net/topic/GUI/publications/57) | E: discovery only |
| AWeb2, AWeb3 | [Endpoint](https://github.com/ocornut/imgui/wiki/About-the-IMGUI-paradigm) | C: scoped primary |
| AWeb2 | [Endpoint](https://doi.org/10.18420/vrar2022_1678) | E: discovery only |
| AWeb4 | [Endpoint](https://www.researchgate.net/publication/394461243_ALGORITHM_AND_SOFTWARE_IMPLEMENTATION_OF_IMMEDIATE_MODE_INTERFACE_FOR_VISUALIZATION_SYSTEMS) | E: discovery only |
| AWeb4 | [Endpoint](https://repository.kpi.kharkov.ua/entities/publication/4f32ba44-b1c8-4424-be5b-b28d94811183/full) | E: access/unverified |
| AWeb4, AWeb6 | [Endpoint](https://vestnik2079-5459.khpi.edu.ua/article/view/325758) | C: scoped primary |
| AWeb4 | [Endpoint](https://web.kpi.kharkov.ua/auts/en/research/) | E: discovery only |
| AWeb4, AWeb6 | [Endpoint](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2020.14) | C: scoped primary |
| AWeb4 | [Endpoint](https://dl.gi.de/handle/20.500.12116/39954) | E: access/unverified |
| AWeb5 | [Endpoint](https://vestnik2079-5459.khpi.edu.ua/article/download/325758/325661) | E: access/unverified |
| AWeb5 | [Endpoint](https://arxiv.org/html/1910.11108v4) | E: access/unverified |
| AWeb5 | [Endpoint](https://conal.net/papers/icfp97/) | E: access/unverified |
| AWeb6 | [Endpoint](https://dl.gi.de/handle/20.500.12116/40168) | C: scoped primary |
| AWeb6 | [Endpoint](https://conal.net/papers/icfp97/icfp97.pdf) | E: access/unverified |
| AWeb7 | [Endpoint](https://drops.dagstuhl.de/storage/00lipics/lipics-vol166-ecoop2020/LIPIcs.ECOOP.2020.14/LIPIcs.ECOOP.2020.14.pdf) | C: scoped primary |
| AWeb8 | [Endpoint](https://exchangetuts.com/what-are-the-performance-implications-of-using-an-immediate-mode-gui-compared-to-a-retained-mode-gui-1639487825149630) | E: discovery only |
| AWeb8 | [Endpoint](https://gabdube.github.io/articles/retained_gui/release/retained_gui.html) | E: discovery only |
| AWeb8, AWeb9 | [Endpoint](https://www.lambdadays.org/static/upload/media/1456745842918599frpnui_lambdadays1.pdf) | E: discovery only |
| AWeb8 | [Endpoint](https://oandre.gal/concepts/immediate-mode-vs-retained-mode/) | E: discovery only |
| AWeb8 | [Endpoint](https://vuink.com/post/ryvnfanhe-d-dpbz/blog/immediate-mode-gui-programming) | E: discovery only |
| AWeb8 | [Endpoint](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/C828ACD945F6DF45CE9B5DFDF0B67C76/S0956796800003671a.pdf/functional_reactive_animation_of_a_lift_using_fran.pdf) | E: discovery only |
| AWeb8 | [Endpoint](https://www.scribd.com/document/1023185604/Functional-Reactive-Animation) | E: discovery only |
| AWeb8 | [Endpoint](https://en.wikipedia.org/wiki/Casey_Muratori) | E: discovery only |
| AWeb8 | [Endpoint](https://citeseerx.ist.psu.edu/document?doi=f617c6f8fe05d3a371facb02210ad99b57a3e8a9&repid=rep1&type=pdf) | E: discovery only |
| AWeb8 | [Endpoint](https://www2.imm.dtu.dk/pubdb/edoc/imm888.pdf) | E: discovery only |
| AWeb8 | [Endpoint](https://news.ycombinator.com/item?id=25624044) | E: discovery only |
| AWeb8 | [Endpoint](https://ratatui.rs/concepts/rendering/) | E: discovery only |
| AWeb8 | [Endpoint](https://unresearch.ing/ggui_retro) | E: discovery only |
| AWeb8 | [Endpoint](https://gamedev.net/tutorials/programming/graphics/direct3d-immediate-mode-r911) | E: discovery only |
| AWeb8 | [Endpoint](https://upcommons.upc.edu/bitstream/handle/2117/175735/143606.pdf) | E: discovery only |
| AWeb8 | [Endpoint](https://knowledge.uchicago.edu/record/585/files/Samuels_uchicago_0330D_13489.pdf) | E: discovery only |
| AWeb8 | [Endpoint](https://de.wikipedia.org/wiki/Retained_Mode) | E: discovery only |
| AWeb8 | [Endpoint](https://de.wikipedia.org/wiki/Immediate_Mode_%28Computergrafik%29) | E: discovery only |
| AWeb8 | [Endpoint](https://www.reddit.com/r/rust/comments/j0840q) | E: discovery only |
| AWeb8 | [Endpoint](https://www.reddit.com/r/cpp/comments/c7rrnv) | E: discovery only |
| AWeb8 | [Endpoint](https://www.reddit.com/r/rust/comments/omnvaq) | E: discovery only |
| AWeb8 | [Endpoint](https://www.reddit.com/r/cpp/comments/14h7mvu/declarative_gui_libraries/) | E: discovery only |
| AWeb10 | [Endpoint](https://github.com/bryanedds/Nu/wiki/Model-View-Update-for-Games-via-MMCC/9cb6d2fe3865c68fd4ac3a945efb81946ef59174) | C: scoped primary |
| AWeb10 | [Endpoint](https://github.com/bryanedds/Nu/wiki/Immediate-Mode-for-Games-via-ImSim/e657be2c650864c4917fdf81f23e7775e76e9b95) | C: scoped primary |
| AWeb11 | [Endpoint](https://arxiv.org/abs/2407.07207) | C: scoped primary |

### Follow-up audit and validation

Scite answer ID:
`alf-architecture-maintenance-proposal-background-2026-09-14`.
One final recording call retained **79 credited / 290 not credited**,
**0 skipped**, across **369 DOI identifiers/endpoints**. The read-only audit
confirmed no missing reasons, `retrieval_unlinked = false` and
`truncated = false`. Provenance is 211 Scite DOI records, 117 web endpoints
and 41 other primary/reused source records. The 58 `full_text` stage labels
include selected passages, reused readings and public source inspection;
they are **not 58 whole papers read**. The 311 title/abstract labels include
unassessed discovery leads. Its `retrieved: null` and mechanical
`screened: 369` fields do not establish a systematic-review denominator.
Aliases and documentary metadata account for part of the credited set; the
proposal's bibliography has 28 canonical works/leads, not 79 independent studies.
The original closed audit ID was not modified.

Main-agent self-review covered terminology before RQs, source claim/edition
limits, direct-comparison versus lineage distinctions, credibility criteria,
dataset availability, dispatch arithmetic, dependent units, policy zeros versus
infrastructure nulls, and the construction/live authority boundary. The
bootstrap interval is specified only when all 12 matched blocks are fully
scored; otherwise the proposed missing-data bounds preserve null records.
The extraction worker supplied evidence, **not a new independent design review**.
Neither is human expert approval.

Checks actually run for this documentation revision:

- `python -m unittest discover -s tests -p test_ci_scope.py -v`: **11 passed**.
  Expected fallback diagnostics are part of those regression tests.
- Strict UTF-8 decoding, replacement-character and trailing-whitespace checks
  on the four in-scope Markdown files: passed.
- **101 relative file links** resolved. This does not test all external sites,
  execute Nu or establish baseline equivalence.
- `git diff --check`: passed. Source-specific assertions were checked against
  the cited excerpts/worker reading; no runtime checks are newly claimed.
- Fetch confirmed no upstream divergence at base `0df55a4`; a PowerShell
  quoting error in the first revision-range check was corrected using the
  literal `'HEAD...@{u}'`. It did not change repository history.
- Publication uses only these four Markdown files, directly to the configured
  upstream with no PR. Exact containing commit/CI are reported at handoff;
  skipped runtime jobs are not passed experimental evidence.

No experimental call, OAuth staging, candidate execution, recruitment, new
construction or allocation occurred. The unrelated `uv.lock` remains unstaged.
