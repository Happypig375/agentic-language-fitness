# S04 — MicroRec

**Full PDF read and bounded artifact reconstruction, 2026-09-16 HKT.** Reader: main Codex AI session. No model execution or experiment reproduction. [Living queue](../selection-priority-reading-2026-09-15.md); [PLAN](../../../PLAN.md).

## Identity and coverage

Alsayed, Dam and Nguyen, **MicroRec: Leveraging Large Language Models for Microservice Recommendation**, MSR 2024, printed pp. 419–430, DOI [10.1145/3643991.3644916](https://doi.org/10.1145/3643991.3644916). This is the recommendation paper, not the unrelated FPGA work sharing the short name.

| Asset | Verified identity |
| --- | --- |
| Zotero collection / parent / attachment | `PKLXQNEE` / `6EX7AWI8` / `7YUWVT9N` |
| Publisher PDF | 921,317 bytes; 12 pages |
| SHA-256 | `53ecebed5460aad806b33a505a7877d4a70be5d4aafaff5efb76f862475ebb75` |
| Text coverage | All pp. 1–12, including 37 references; no appendix |
| Visual checks | Identity p. 1; all five figures on pp. 3–6 and 10; all three tables on pp. 9–10; loss/metric equations pp. 4, 5, 7 |

Two-column extraction was checked against the rendered pages and reread in natural column order. Stored bytes, extraction and renders remain outside Git. Scite exact identity was checked; an omitted notices field is not a negative notices audit.

## Decision, information and evaluation

The system retrieves Stack Overflow questions and reranks results using repository README and Dockerfile content. A query describes required functionality. Its output helps discover candidate microservices; it does not choose between tested source packages and then observe later coding-agent maintenance.

PDF pp. 3–6 describe contrastive representations and cross-encoder reranking: DistilRoBERTa or OpenAI `text-embedding-ada-002` representations, with a TinyBERT cross-encoder. README text is condensed where needed. QQ, QD, QR512 and QRD vary the supplied information; comparing question-only CLEAR with documentation-enriched variants therefore bundles information and representation changes. The implementation's own four-service decomposition is a design description, not a controlled maintainability result.

The June 2023 Stack Overflow dump is filtered for questions with accepted answers linking repositories that have README and Dockerfile files; repositories need at least five associated posts. Dockerfile similarity/clustering further consolidates candidates. The paper reports **2,868 posts and 178 repositories**. Its listed split sizes, **1,613 + 554 + 688 = 2,855**, leave **13 posts unaccounted for** (PDF pp. 6–7). The paper describes avoiding overlapping services between splits; inspected source supports grouping by repository labels, but does not independently verify the final published data.

The primary outcomes are MRR, MAP and precision/recall at several ranks, using accepted-answer repository associations as relevance. They are neither implementation correctness nor adoption utility. The paper reports Wilcoxon significance at p < .05; exact test units, complete values and uncertainty intervals remain insufficiently specified in the inspected record.

## Read the results with their denominators

Table 1 reports BERT QRD MRR/MAP of .5309/.5309 versus CLEAR .2926/.1041. QRD improves top-rank measures but does not dominate: CLEAR has higher precision and recall at ranks 5 and 10. Table 2 reports GPT QRD MRR/MAP .5473/.5473; QR512 is slightly higher at precision/recall@10. These are conditional retrieval comparisons, not uniform improvements at every operating point.

For the Docker Hub comparison (PDF pp. 8–10), the authors create 688 synthetic repositories whose descriptions match dataset questions, then use 100 randomly selected queries and the top five results. They report 63 versus 4 queries with a correct result, and 185 versus 5 correct returned answers. Those are distinct units: **15.75-fold query-hit counts** and **37-fold answer counts**, respectively; they do not establish a maintenance effect. Repeated relevant questions can map to the same underlying repository (Table 3).

Figure 5 visualizes embeddings with UMAP/HDBSCAN. Cluster appearance does not isolate why the system succeeds. Evaluation with developers and domain experts remains proposed future work (PDF p. 11); the paper does not present a later executable maintenance study.

## Released scorer: a material comparability concern

Inspected [MicroRec-Replication](https://github.com/MicroRec/MicroRec-Replication/tree/08aac8a2e9afed519b3f0a7702accc65ae43e344), commit `08aac8a2e9afed519b3f0a7702accc65ae43e344`. Read the README routes, dataset-generation notebook and the relevant construction/scoring cells of `CLEAR03-rerank.ipynb` and `all-q-r-rerank.ipynb`. Other downloaded notebook variants were not fully reconstructed. No notebook cells were executed.

| Source location | Static finding |
| --- | --- |
| `CLEAR00-dataset`, cells 5–9 | Groups by repository label, splits unique labels using seed 42, and assigns all corresponding questions. This supports a repository-level split **in that script**; output path `generated3` differs from the evaluator's `generated5`. |
| `CLEAR03-rerank`, cells 5, 9, 12 | Both scorers treat associated **question strings** as relevant targets and divide AP/recall by their count. |
| `all-q-r-rerank`, cells 5, 9 | Builds documentation from the first 350 README words plus 200 Dockerfile words. It stores relevant question strings for one scorer and a **singleton list containing one processed document** for the other. The singleton is a list, not a string-length denominator. |
| Same notebook, scoring functions and aggregate loop | The documentation scorer removes its sole relevant document after the first match, so its AP equals reciprocal rank by construction. The question scorer averages over multiple relevant questions. Recall still uses the number of relevant questions for both. |

Thus the released QRD comparison changes the relevance unit between question and documentation scoring. The repeated equality of MRR and MAP is consistent with this construction. **The headline MAP gain cannot be taken as a commensurate improvement until the target units and denominators are reconciled.** This is a source-level concern in the pinned artifact, not a rerun of all paper tables or proof that every reported metric is wrong. Exact publication-run linkage and other variants remain to check if numerical reuse is proposed.

The authors' public Drive folder was reachable and lists `data.zip`, `models.zip`, `Evaluate Cross-Encoder.zip` and a labeled-output archive. A bounded `data.zip` acquisition returned HTML rather than ZIP; no data archive or model weights were inspected or executed. Do not describe the entire artifact as private or unavailable. Current data membership, the 13-post discrepancy and exact saved-table provenance remain unresolved.

## Consequence for ALF and next reading

**Retain:** recommendation and code/document retrieval are established adjacent work. This full paper's experimental target differs from prospective source-maintenance choice.

**Strengthen:** use the same decision and outcome units across every selector; preserve multiple valid alternatives and common denominators; freeze data/profile membership; distinguish ranking, analyst agreement and measured behavioral utility. Report adverse operating points, synthetic-corpus assumptions and analysis costs. Do not borrow MicroRec's percentage gains for ALF effects, power or ROI.

Promote **S22, Evaluating Recommendation Systems**, for evaluation design and metric/utility alignment, and **S24, A Machine Learning Approach to Service Discovery for Microservice Architectures**, for prior selection work explicitly targeting runtime QoS. S24 could challenge any broad statement that service recommendation lacks behavioral outcomes; its different decision object must be reconstructed before use. Existing **S01/S06/S16** remain the foundations for defaults, conditional value and information cost. The [next-reading record](../selection-reading-next-2026-09-16.md) states the unresolved conditions.
