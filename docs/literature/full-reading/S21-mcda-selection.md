# S21 — MCDA selection before task data exist

**Full publisher-PDF reading completed 2026-09-16 HKT by the main Codex AI session.** Sebastian Sonntag, Erik Pohl, Janosch Luttmer, Jutta Geldermann and Arun Nagarajah, *A conceptual MCDA-based framework for machine learning algorithm selection in the early phase of product development*, Proceedings of the Design Society 4, 2257–2266 (2024). [DOI](https://doi.org/10.1017/pds.2024.228).

## Asset and coverage

| Field | Evidence |
| --- | --- |
| Zotero | Parent `49AP6LL6`, user-supplied PDF `CGPW7TGW`, collection `PKLXQNEE` |
| PDF | 10 pages, 537,733 bytes; SHA-256 `24cde4e0fd66fa416172bc99aee3d7013202534382664b85444513c1c27792cf` |
| Reading | All pp. 1–10, including all references pp. 9–10; no appendix |
| Visual checks | Identity p. 1; all four tables pp. 3, 5, 6, 8; all three figures pp. 4, 8, 9; equation p. 7 |
| Reproduction limit | The paper links PROMETHEE-Cloud, but releases no complete 164-source extraction ledger or case artifact in the PDF. No software, ML task or participant experiment rerun |

## Reconstruction

The intended beneficiary lacks ML expertise and needs a choice before an application dataset necessarily exists. The method has three stages: translate a product-development activity into an ML capability using a reference process; rank candidate algorithms using qualitative criteria and stated preferences; inspect the result, partial ordering, projected criteria and weight sensitivity before choosing.

The reference process draws on VDI 2221 and design literature. The evaluation matrix contains 16 algorithms—eight supervised and eight unsupervised—and nine criteria: data flexibility, quantity, preprocessing, parameter-definition complexity, scalability, memory, time, robustness and understandability (pp. 5–7). The paper reports examining 164 publications to construct the matrix. Accuracy/precision are deliberately excluded because they depend on application data. Qualitative scores therefore encode prior judgments about algorithm properties, not measured success on the example task.

The example is information extraction from engineering documents, mapped to classification. It uses assumed preferences, SIMOS-style weights and PROMETHEE; Table 4 gives weights, orientations and preference-function choices. Robustness has the largest weight, 0.162. Random forest ranks first, followed by decision tree and naïve Bayes. Figures 2–3 display flows, a partial ordering, a GAIA projection and weight-stability intervals. The demonstration shows how the specified criteria/preferences generate a recommendation. It does not execute an extraction benchmark or compare users' subsequent decisions.

## What the example does and does not establish

This is direct prior art for **pre-data, preference-sensitive algorithm advice**, including implementation burden and explanations. A recommendation matching a commonly used algorithm provides plausibility, not independent evidence of useful performance, lower cost, or reduced expert dependence. The conclusion explicitly leaves non-expert applicability to future case studies. A table asserting other approaches fail chosen requirements is also not proof that those approaches cannot be adapted (pp. 2–3).

Weight sensitivity describes robustness of a ranking **within the assumed decision model**. It does not validate the criterion values, reference mapping, completeness of candidate choices, or realized robustness of a recommended implementation. The study has no ordinary-review control, independently sampled task profiles, user outcomes or quantified analysis burden. Its subjective preferences can be explicit and reviewable without becoming objective measurements of downstream value.

Two visible specification limits matter if reusing the matrix. C4's prose assigns increasing scores to increasing parameter complexity, while Table 3 says larger values are better and Table 4 maximizes every criterion. The displayed values instead give simple decision-tree/naïve-Bayes models high scores. The intended orientation needs reconciliation. Also, the claims that criteria are distinguishable and draw on 164 sources are not accompanied by a complete source-to-cell derivation, uncertainty assessment or reproducible search/selection ledger. This review does not silently repair or adopt that matrix.

## Consequences and next readings

ALF cannot claim novelty merely for making a choice from qualitative information before execution, incorporating cost preferences, or visualizing a recommendation. Its value must be tested through a frozen decision policy and subsequent common behavioral outcomes. Keep hard feasibility constraints separate from tradeable preferences; freeze criteria directions and weights before evaluation, and report sensitivity as conditional on the stated model. A ranking's stability does not substitute for behavioral evidence.

S01 remains necessary for established selector evaluation, and S29 is promoted for the closer architectural tradeoff/explanation question. S19 provides the later recommendation experiment. The 2023 pattern-language precursor, reverse-logistics criteria, and detailed PROMETHEE/SIMOS sources retain conditional status: they become necessary if ALF adopts their mapping, numerical matrices or aggregation rules. It currently adopts none of those specific mechanisms, so reading them is not required just to reject novelty for pre-data qualitative advice. The requirement-extraction application likewise becomes necessary if its numerical task benefit is claimed; no such effect is imported.

**Uniqueness is unconfirmed, usefulness remains a conditional empirical question, and ALF's methodology is not validated by a coherent preference model.**
