# Source decisions for the next-reading assessment

**2026-09-16 HKT.** Supports the [reading-order decision](selection-reading-next-2026-09-16.md), not a systematic review or final novelty verdict. Exact full-reading coverage remains in the eight S notes and the index; S23 includes its full supplement. Prior P/A readings are reused at their recorded extent.

## Retrieval and actual scope

| Call | Requested page / returned coverage | Consequence |
| --- | --- | --- |
| Exact S02/S04/S07 DOIs | limit 20, offset 0; total/count 3/3 | Identities matched the supplied PDFs. |
| Citation graph, three seeds | both directions, depth 1, max_edges 200, intent included; 87 edges / 89 nodes; truncated false | Followed 16 non-seed incoming work identities. Graph s is citing and t cited. Seed coverage 16/43/29; no low-coverage flags. These are indexed edges, not complete bibliographies or field coverage. |
| Exact follow-up identities | 16 incoming works + 4 MicroRec references; limit 20, offset 0; total/count 20/20 | Screened all returned titles/metadata; many abstracts were absent or truncated. Exact lookup exhausted its supplied set, not the field. |
| Three additional S07 method references | limit 20, offset 0; total/count 3/3 | S20/S21/S23 identities; primary checks precede import. |
| Indexed-notice filters | Each of has_retraction, has_concern, has_correction, has_erratum separately true, scoped to the 26 exact DOIs; each limit 20, offset 0; total/count 0/0 | No notices returned by those indexed filters. The ordinary response omitted notices fields; zero filtered hits does not certify absence of all notices. |

These exact retrievals yield **26 distinct Scite identities**. No further page was required for an exhausted exact set or zero notice result. This pass used citation-follow-up and primary identity/acquisition searches, not a new broad systematic keyword review. Incidental search hits and uninspected graph nodes are not represented as screened primary studies. Reading a paper's bibliography does not mean reading every cited paper.

Primary follow-up used author repositories, Crossref, Cambridge/Design Society, arXiv, Springer, the Ben-Gurion chapter host and the author-institution DiVA record. DOI/title/author/edition checks found S23's Richard Horn misattributed in Scite, corrected from publisher/Crossref. S22 has a 2010 online/2011 printed date distinction; S20's 11-page preprint is not asserted identical to the 10-page publication. Existing S05 edition/date reconciliation remains pending. Access failures and truncated abstracts are explicit, not negative results.

For the document-evaluation citer, the [primary arXiv abstract](https://arxiv.org/abs/2601.19693) was inspected. For informal-specification architecture generation, the [author-institution abstract](https://re.public.polimi.it/handle/11311/1292266) was inspected. Other deferred incoming studies below generally received only title/metadata screening; their uninspected methods cannot establish absence of downstream evaluation.

## Considered decision set

“Credited” includes papers credited **as necessary next readings**, not only fully read evidence. “Deferred” means excluded from this segment's evidential conclusion at the stated depth; it is not rejection, a quality judgment or permanent exclusion. Existing-queue entries have no newly claimed full coverage. Stable new full-reading IDs S19–S27 are all added to Zotero. The additional bibliography-only dependencies remain conditional until their method is needed.

| Decision in this segment | Work / DOI | Reason and actual scope |
| --- | --- | --- |
| Credited | Can large language models support machine learning implementation in product development? A comparative analysis and perspectives — `10.1017/pds.2025.10100` | S07 publisher PDF fully read; valid alternatives, conditional identity and prompt-selection limits. |
| Credited | MicroRec: Leveraging Large Language Models for Microservice Recommendation — `10.1145/3643991.3644916` | S04 publisher PDF fully read; bounded scorer comparison identifies relevance-unit concern. |
| Credited | Using Generative Artificial Intelligence for Suggesting Software Architecture Patterns from Requirements — `10.1007/978-3-031-66336-9_19` | S02 chapter fully read (volume PDF 285-294); current artifact ambiguity and implications, not reproduction. |
| Deferred | RGPRec: A RAG‐Enhanced GNN for Personalized Task Recommendations in Open‐Source Communities — `10.1002/spe.70022` | Deferred after metadata/title screening: developer-task recommendation, not the declared package decision. Reopen if allocation/beneficiary matching enters the claim. |
| Credited | Graph retrieval-augmented generation for enhancing LLM-based ML algorithm recommendation in product development — `10.1017/pds.2026.10613` | Promoted S19: direct 2026 follow-up. Primary identity/abstract and selected HTML only; OA PDF blocked; full read pending. |
| Deferred | Automated Clustering of Microservices Using Natural Language Processing and Clustering Algorithms — `10.5753/sbcars.2025.14592` | Deferred after metadata/title screening: NLP microservice clustering. Reopen if candidate decomposition or structural partition scoring enters the method. |
| Deferred | Using LLMs to Evaluate Architecture Documents – Results from a Digital Marketplace Environment — `10.1007/978-3-032-24216-7_4` | Deferred after primary arXiv abstract screening: architecture-document judgments versus architects. Reopen for analyst-map/rater validation; no full read. |
| Deferred | CIAO - Code In Architecture Out - Automated Software Architecture Documentation with Large Language Models — `10.1109/icsa66085.2026.00026` | Deferred after metadata/title screening: automated architecture documentation. Reopen if the selector generates source maps automatically; method uninspected. |
| Deferred | Automated Software Architecture Design Recovery from Source Code Using LLMs — `10.1007/978-3-032-02138-0_5` | Deferred after metadata/title screening: source-to-architecture recovery. Reopen for automated information extraction; method uninspected. |
| Deferred | Generative AI for Self-Adaptive Systems: State of the Art and Research Roadmap — `10.1145/3686803` | Deferred after metadata/title screening: self-adaptive-systems roadmap. Reopen if dynamic controller policy is adopted; not negative evidence about execution. |
| Deferred | Decentralized Generative AI Model Deployment Using Microservices — `10.1109/icaiqsa64000.2024.10882424` | Deferred after metadata/title screening: deployment of generative models using microservices, not yet a demonstrated competing maintenance-selector method. |
| Credited | A Machine Learning Approach to Service Discovery for Microservice Architectures — `10.1007/978-3-030-86044-8_5` | Promoted S24: primary institutional abstract identifies runtime QoS selection. Full text unavailable; no method/result confirmation. |
| Deferred | LEMON: LLM-Enabled Monitoring for Microservices Orchestration — `10.1109/tsc.2026.3679374` | Deferred after metadata/title screening: monitoring/orchestration. S24 is the more direct first runtime-selection read; do not assume LEMON has no relevant outcomes. |
| Credited | Generative AI for software architecture. Applications, challenges, and future directions — `10.1016/j.jss.2025.112607` | Existing S05 retained as architecture/code overlap priority; newly retrieved metadata, no new full reading or edition equivalence. |
| Deferred | Rethinking the Evaluation for Conversational Recommendation in the Era of Large Language Models — `10.48550/arxiv.2305.13112` | Deferred after metadata/title screening: conversational recommendation evaluation. Reopen for conversation-specific relevance rules after the general S22 methods read. |
| Deferred | BERT-Based Approaches for Web Service Selection and Recommendation: A Systematic Review with a Focus on QoS Prediction — `10.3390/fi17120543` | Deferred after metadata/title screening: web-service/QoS review. Reopen if S24 exposes missing primary outcome methods; not fully screened. |
| Deferred | DockerFinder: Multi-attribute Search of Docker Images — `10.1109/ic2e.2017.41` | Deferred after MicroRec bibliography and exact metadata screening: Docker image search. Reopen if matching/search corpus construction becomes an ALF mechanism. |
| Credited | Evaluating Recommendation Systems — `10.1007/978-0-387-85820-3_8` | Promoted S22: metric/utility and comparative evaluation methods; full 41-page author-manuscript reading; metric/utility distinctions and verified formula errors. |
| Deferred | Generative AI for Software Development: A Survey — `10.1007/978-981-96-7238-7_17` | Deferred after metadata/title screening: broad development survey. First follow architecture-specific S05 and direct competitors. |
| Deferred | LLM-based Automated Architecture View Generation: Where Are We Now? — `10.1109/icsa66085.2026.00031` | Deferred after metadata/title screening: architecture-view generation. Reopen for automated map construction or if S05/S08 identifies consequential behavior tests. |
| Deferred | A survey on large language models for software engineering — `10.1007/s11432-025-4670-0` | Deferred after metadata/title screening: broad LLM/SE survey. Architecture-specific S05 first; not excluded as low quality or exhausted evidence. |
| Deferred | Leveraging LLMs to Automate Software Architecture Design from Informal Specifications — `10.1109/icsa-c65153.2025.00049` | Deferred after primary institutional abstract screening: generation of architecture diagrams from specifications. Reopen for architecture authoring or relevant execution methods found through S05/S08. |
| Deferred | Research on Multi-Layer Computing Power Routing Based on Microservice Dynamic Orchestration in Computing and Network Integration — `10.1109/eei70303.2026.11640661` | Deferred after metadata/title screening: dynamic orchestration/routing. No active dynamic-deployment claim; method uninspected. |
| Credited | A conceptual MCDA-based framework for machine learning algorithm selection in the early phase of product development — `10.1017/pds.2024.228` | Promoted S21: explicit criteria/weighting and practical example; primary abstract screened, OA PDF blocked, full read pending. |
| Credited | Intelligent User Assistance for Automated Data Mining Method Selection — `10.1007/s12599-020-00642-3` | Promoted S23: full 21-page publisher and 26-page supplement reading; bounded pinned artifact; development/confirmation and unaided-user limits; correct author Richard Horn. |
| Credited | GPT in Data Science: A Practical Exploration of Model Selection — `10.1109/bigdata59044.2023.10386503` | Promoted S20: implemented selection heuristics and conventional comparator; full 11-page arXiv-v1 reading, all figures/results; edition/search/metric limits. |
| Credited | ASlib: A benchmark library for algorithm selection — `10.1016/j.artint.2016.04.003` | Existing S01 priority for defaults, profile splits, information cost and failed runs; prior partial reading unchanged. |
| Credited | Failure-Aware Enhancements for Large Language Model (LLM) Code Generation: An Empirical Study on Decision Framework — `10.48550/arXiv.2602.02896` | Existing S03 priority for advice derivation and code outcome scope; prior partial reading unchanged. |
| Credited | Algorithm selection on a meta level — `10.1007/s10994-022-06161-4` | Existing S06 priority for conditional value, uncertainty and cost; prior partial reading unchanged. |
| Credited | ArchBench: Benchmarking Generative-AI for Software Architecture Tasks — `10.48550/arXiv.2603.17833` | Existing S08 priority to reconstruct executable architecture/code overlap; no new full reading. |
| Credited | Impact of Experience and Team Size on the Quality of Scenarios for Architecture Evaluation — `10.14236/ewic/ease2008.1` | Existing S15 priority for independent profile construction and author/rater effects; no new full reading. |
| Credited | Algorithm Selection for Combinatorial Search Problems: A Survey — `10.1609/aimag.v35i3.2460` | Existing S16 priority for selection foundations and missing methods; no new full reading. |
| Credited | Building Software by Rolling the Dice: A Qualitative Study of Vibe Coding — `10.48550/arXiv.2512.22418` | Existing S17 priority conditional on practitioner/beneficiary claims; no new full reading. |
| Deferred | A Pattern Language Approach to Identify Appropriate Machine Learning Algorithms in the Context of Product Development — `10.1017/pds.2023.37` | S07 bibliography-only lead; defer until S21/S19 reconstruction establishes need for earlier pattern-language method; not rejected. |
| Deferred | Selection of Suitable Machine Learning Algorithms for Classification Tasks in Reverse Logistics — `10.1016/j.procir.2021.01.086` | S07 bibliography-only lead; defer to explicit criteria reading S21 first, reopen for selection-criteria derivation. |
| Deferred | Identification of evaluation criteria for algorithms used within the context of product development — `10.1016/j.procir.2020.02.207` | S07 bibliography-only lead; defer until S21 shows which criteria need primary reconstruction. |
| Deferred | CLEAR baseline paper (identity not independently reconstructed here) — `10.1145/3510003.3510159` | MicroRec bibliography lead; inspected released baseline scorer suffices for the bounded code comparison; full CLEAR body needed if numerical reproduction is proposed. |
| Deferred | Did You Understand the Problem? – Evaluating Fine-Tuned Language Models for Identifying AI-Related Tasks in Product Development — `10.1115/DETC2025-169694` | S19 primary bibliography/selected-method lead; defer to S19 dataset and evaluation reconstruction. Not independently identity-verified or fully screened here. |

The earlier set had 38 decisions. With S25/S26/S27 and the two technical documentation sources below, the prepared record has **43 considered decisions: 22 credited and 21 deferred**. Eight S works are newly fully read; S19/S21/S24/S25 have now been supplied and identity-checked, but their full readings are pending. Full-reading count, citation count, source-method reconstruction and experimental reproduction are different quantities.

## Continuation retrieval and source additions

An exact-title Scite query for S25, S26 and S27 requested limit 20/offset 0 and returned total/count 3/3: S25 plus the journal/arXiv identities of S27. S26 was absent and was verified from JMLR instead. There are now 29 distinct retrieved Scite DOI identities in this pass, with S27's two identities representing one work. Each of the four notice filters on the three added DOI identities returned 0/0; their generic “not indexed” wording conflicts with successful unfiltered retrieval and is not a notice-absence certificate.

| Decision | Added source | Actual reason and depth |
| --- | --- | --- |
| Credited | S25, `10.1109/BigData55660.2022.10020386` | Exact conventional comparator/predecessor for S20/S27; user-supplied publisher PDF identity verified, full reading pending |
| Credited | S26, [JMLR primary record](https://jmlr.org/papers/v7/demsar06a.html) | Fully read publisher PDF pp. 1–30 to resolve the S22 statistical dependency; no DOI invented |
| Credited | S27, `10.1109/ACCESS.2025.3558218`, arXiv alias `10.48550/arXiv.2501.00532` | One work, fully read arXiv v1 pp. 1–14; journal edition unexamined, representation/one-case limits |
| Credited | [NIST Bonferroni documentation](https://www.itl.nist.gov/div898/handbook/prc/section4/prc473.htm) | Primary technical-page inspection verifies the general inequality for arbitrary events; not another full paper |
| Credited | [SciPy Wilcoxon documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wilcoxon.html) | Primary technical-page inspection of symmetry, ties/zeros and exact-method conditions; no test/model executed |

The user subsequently supplied S19/S21/S24/S25, superseding the access-blocked wording in the original decision rows above. Their attachment identities/hashes and exact pending scope are recorded in the current reading decision. No new work was duplicated. The source list remains prepared, not yet submitted as a completed handoff.

## Scite report and limits

The actual decision set will be submitted once near handoff and its scoped citation report inspected. The service's binary cited/excluded fields represent the credited/deferred decisions above; reasons preserve pending-full-read and access-blocked states. Report counts are provenance checks, not systematic coverage, novelty confirmation or independent human approval.
