# S25 — Adaptive model-selection predecessor

**Full publisher-PDF reading completed 2026-09-16 HKT by the main Codex AI session.** Cristina Tavares, Nathalia Nascimento, Paulo Alencar and Donald Cowan, *Adaptive Method for Machine Learning Model Selection in Data Science Projects*, IEEE Big Data 2022, 2682–2688. [DOI](https://doi.org/10.1109/BigData55660.2022.10020386).

## Asset and coverage

| Field | Evidence |
| --- | --- |
| Zotero | Parent `ISX3ANBU`, user-supplied publisher PDF `L5NEQQSU`, collection `PKLXQNEE` |
| PDF | Seven pages, 2,560,806 bytes; SHA-256 `d4ff26ddbc7b68f396e84271d4c2572d0bca5041186341851083803f01b8edb1` |
| Reading | All pp. 1–7 and all 28 references; no appendix |
| Visual checks | Identity p. 1 and all six figures pp. 4–7, including the flowchart, feature diagrams and adaptation examples; no results table or numbered equation |
| Limit | No linked executable artifact or measured prediction/decision-efficiency results in the paper. No experiment reproduced |

## Reconstruction and edition distinction

This is explicitly ongoing work. It translates Scikit-learn selection heuristics into feature models for algorithm families and application requirements, then illustrates how changing data or requirements can trigger a new choice. Features include sample size, labeled/text data, prediction type, number of categories, feature sparsity and desired performance. Nonfunctional requirements include transparency, performance, auditability and ethical requirements; listing a feature is not an operational validation of it.

The initial example is the 299-patient heart-failure dataset, with 12 input features plus a target. The heuristic selects LinearSVC. Two hypothetical adaptations illustrate the method: substantially larger data lead to SGD classification, while changing the goal from category to quantity leads to LASSO/ElasticNet regression. No train/test split, model-training results, confidence intervals, decision-time saving or assisted-user evaluation is reported. Although the introduction's outline promises an experiments/results section, the actual Section V is the conclusion. Do not infer an omitted result from that outline or from the phrase “configuration that was implemented.”

This resolves an important dependency of [S20](S20-gpt-model-selection.md) and [S27](S27-variability-aware-selection.md): **S25 supplies the earlier heuristic/feature-model method; S27 adds the subsequently reported executed example.** They are related works, not interchangeable editions or independent replications of the same empirical effect.

The figures retain specification problems seen in S27: the text's larger-than-100,000 scenario is illustrated with 1,200 samples in Figure 5, and the regression illustration retains an F1 label in Figure 6. The method does not provide a complete executable constraint system here. Neither diagram can be treated as a validated selection rule without reconciliation.

## Consequences and next readings

Conditional selection, explicit decision factors and adaptation are established. ISE's narrower contribution cannot be the use of diagrams or the observation that requirements affect the best choice. Its proposed adoption-time policy must also remain distinct from a policy that switches implementations after learning new outcomes. Any later adaptation/search policy would need its own information boundary, switching cost and allocation.

The empirical information-value question remains open in this source. A fixed architecture analysis needs comparison with ordinary use of the same information and effort, followed by common behavioral evaluation. It cannot infer productivity, explainability or user benefit from an illustrative feature model.

S01 and the direct architecture/code readings remain consequential. Clinical prediction, PHOTONAI, MLOps and general feature-modeling predecessors are conditional on adopting their numerical results or implementation mechanisms; ISE adopts neither. There is no reason to extend this branch merely to reproduce the clinical example. **Uniqueness remains unconfirmed; useful benefit is unmeasured; methodological rigor still depends on the proposed study's independent profiles and actual apparatus.**
