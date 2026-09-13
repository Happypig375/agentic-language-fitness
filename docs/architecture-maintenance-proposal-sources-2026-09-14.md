# Research proposal: source and search ledger

Date: **2026-09-14 HKT**. ALF base:
`4757a6c5cbbd0f764f9c39b596c5517cc024f48b`.
Companion: [standalone research proposal](architecture-maintenance-research-proposal-2026-09-14.md).
This is bounded scoping research, not a systematic review, saturation claim,
peer-review certificate or adopted experiment. Counts below describe retrieval
positions and identifiers, not independent studies or full papers read.

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
in this proposal, 113 are not credited. Six further DOI identifiers above reuse
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
