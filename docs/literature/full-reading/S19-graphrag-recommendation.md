# S19 — GraphRAG for ML algorithm recommendation

**Full publisher-PDF reading completed 2026-09-16 HKT by the main Codex AI session.** Sebastian Sonntag, Adrian Dörnbach and Arun Nagarajah, *Graph retrieval-augmented generation for enhancing LLM-based ML algorithm recommendation in product development*, Proceedings of the Design Society 6, 2551–2560 (2026). [DOI](https://doi.org/10.1017/pds.2026.10613).

## Asset and coverage

| Field | Evidence |
| --- | --- |
| Zotero | Parent `H27ZR2MJ`, user-supplied PDF `S3GRDLYI`, collection `PKLXQNEE` |
| PDF | 10 pages, 423,950 bytes; SHA-256 `8a96e56d1e1f6ae70e91e70795b28cc57bb3dabbb360142ee9be8e8b269a123f` |
| Reading | All pp. 1–10, including references on pp. 9–10; no appendix |
| Visual checks | Identity/Figure 1 p. 1; Figures 2–6 pp. 3–5 and 8; both tables p. 7; three equations p. 6 and complete illustrated prompt p. 5 |
| Artifact | [IPE-PEP/DESIGN2026](https://github.com/IPE-PEP/DESIGN2026/tree/b6a5a424d5f38214e7b0e55d29a1d7b60dd6497d), pinned commit `b6a5a424d5f38214e7b0e55d29a1d7b60dd6497d`; complete untruncated file inventory, metadata/configuration, all result-file schemas/membership, and bounded prompt/output examples inspected |
| Limit | No model or retrieval experiment rerun; no independent re-adjudication of every output |

## Reconstruction

The selector receives an early product-development problem and recommends ML problem types and algorithms. A knowledge graph links task clarification, activities, design tasks, methods, subtasks and atomic ML tasks. A fixed BAAI/bge-m3 embedder, FAISS search, graph expansion and text linearization supply contextual examples. These examples explicitly state task count and ML problem type; they are additional decision information, not passive telemetry or evidence about a model's internal representation.

Three models—GPT-4o-mini, Gemini 2.5 Flash and Claude Haiku 4.5—receive baseline or graph-context prompts at temperature 0.2, five repetitions per condition. The baseline omits the context. The paper's task-fulfilment rate (TFR) accepts an applicable alternative algorithm, with applicability assessed through literature review, rather than executing the recommendation. Graph retrieval quality (GRQ) measures judged relevance of retrieved subgraphs. Output consistency rate (OCR) concerns repeatability, not correctness. Human comparison is future work (p. 9).

Table 1 reports overall TFR changes of 58→88%, 64→87% and 60→86%. Benefits are not uniform: GPT/Gemini regression recommendations decline from 93% to 79%; Claude classification declines from 76% to 73%. Table 2 reports OCR 59→96%, 29→73% and 29→91%, while Gemini classification OCR declines from 43% to 36%. GRQ averages 88%. These are the paper's reported scores, not independently reproduced effects or estimates transferable to ALF.

## Artifact and inference limits

- **Decision units differ from the prose.** Page 5 describes 56 problem formulations, including ten compound formulations. The pinned dataset has **46 unique formulations: 36 single and ten double**, yielding **56 atomic task labels, exactly 14 per class**. Every one of the 30 output files has the same 46 titles, totaling 1,380 response entries. The likely distinction is formulations versus component tasks; without the evaluator/adjudications, the precise TFR/OCR aggregation is unresolved. Do not treat 56 labels or five repeats as independent adoption decisions.
- **The graph is not fully released here.** Its documentation records six node classes and counts totaling 169 nodes; it does not contain the actual labeled nodes/edges. The repository releases prompts, outputs, dataset and configuration, but no retriever/evaluation code or per-output correctness/relevance adjudications. It therefore supports bounded inspection, not full reconstruction of the retrieval experiment.
- **Consistency needs an equivalence rule.** All 46 prompts are constant across the five repeats within each model/condition. Literal equality of all five entire response strings is 16/46 in both GPT conditions, 3/46→4/46 for Gemini and 0/46 in both Claude conditions. This is a deliberately narrower string check, **not a correction of semantic OCR**. It shows why the missing equivalence/scoring rule matters; semantic or per-task consistency may differ substantially.
- **Graph-specific causality is not identified.** Context versus no context bundles additional domain information, decomposition and presentation. No information-matched text-retrieval/ordinary-analysis control separates graph structure from the information supplied. Correlation between GRQ and TFR does not establish an internal cognitive mechanism. Model size and temperature do not remove those confounds.
- **Generation is not application value.** Literature-assessed suitability, reproducibility of a recommendation, useful executed outcomes and user benefit remain distinct. The reported aggregate gains do not establish net value after graph construction, retrieval and advice costs. Five repeats estimate generation variability within these cases, not broad case coverage.
- **Cross-study percentages are not matched comparisons.** The comparisons with S07 and the fine-tuned predecessor use different models/corpora or subsets. S07 reports 61% for its best overall model, not the average of its three models. S19's introduction describes an average of 61%; retain S07's actual 61/54/59% denominators. The 74% fine-tuning comparison remains unverified until S28 is read.

## Consequences and next readings

The full paper supplies close prior art for structured domain information improving judged recommendations and for allowing valid alternative algorithms. It does not settle ALF's narrower behavioral information-value question. Preserve matched-information controls, explicit recommendation equivalence, common denominators, per-profile outcomes, adverse subgroups and full analysis cost. Do not claim novelty for contextual decomposition or graph-based advice.

Promote **S28**, *Did You Understand the Problem?* ([DOI](https://doi.org/10.1115/DETC2025-169694)), because it created the 400-publication corpus and informs the cross-study generalization claim. Its primary metadata has three authors, including Janosch Luttmer; S19's abbreviated two-author reference is not authoritative. The publisher currently returns HTTP 403 despite an OA indication; access and full reading remain pending. S21 is the directly relevant preference/constraint predecessor and is now fully read. The GraphRAG survey cited here is DOI `10.1145/3777378`, **not** the already read A03 position paper. A full survey reading is conditional on adopting GraphRAG; ALF currently does not. Generic ontology construction and RAG mechanism sources are deferred for the same reason.

**Uniqueness remains unconfirmed; practical value is conditional; methodological validity requires independent case and apparatus validation.** This reading narrows claims and controls, not experimental authority.
