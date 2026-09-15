# S20 — GPT model selection against conventional heuristics

**Full arXiv v1 reading, 2026-09-16 HKT; main Codex AI session.** This continuation follows the [next-reading decision](../selection-reading-next-2026-09-16.md). No author models were executed; [PLAN](../../../PLAN.md) retains all experimental holds.

## Identity, edition and coverage

Nascimento, Tavares, Alencar and Cowan, **GPT in Data Science: A Practical Exploration of Model Selection**, IEEE BigData 2023, DOI [10.1109/BigData59044.2023.10386503](https://doi.org/10.1109/BigData59044.2023.10386503). Read [arXiv 2311.11516v1](https://arxiv.org/abs/2311.11516v1), submitted 20 November 2023. Its 11 pages are not asserted equivalent to the ten-page publisher edition (pp. 4325–4334).

| Asset / coverage | Verified record |
| --- | --- |
| Zotero parent / attachment | `CGLRKL88` / `ZXNE49CA`, collection `PKLXQNEE` |
| Bytes / SHA-256 | 685,770 / `885106570bded555dc2ab0efef479729b20e05f91b08d6d947ecdcf8007c5384` |
| Text | All PDF pp. 1–11, including 16 references; no appendix |
| Visual | Identity p. 1; all nine figures pp. 2, 5–7, 9–10; result blocks pp. 8–9; logical constraints and embedded code inspected |

Scite/Crossref and primary first-page identities agree. The scoped indexed-notice filters returned no hits; this is not a guarantee that no notices exist.

## Reconstructed procedure

The authors ask GPT-4 for model-selection factors generally and for ranked models given three supplied datasets: heart-failure survival (299 records), diabetes classification and car-price regression. They manually express the responses as feature diagrams and constraints (PDF pp. 3–7). The paper itself cautions that the general verbal explanation may not describe GPT's actual internal decision process. Those explanations are a reported rationale, not a validated causal mechanism.

For comparison, a system from Tavares et al. (2022) encodes Scikit-learn selection heuristics. The authors implement recommended algorithms using Scikit-learn and tune parameter grids with `GridSearchCV` (PDF pp. 8–10, Figures 7–9). Heart-failure data are split into 239 training and 60 test cases using stratification. This is **actual execution of recommended models and measurement of predictive performance**, stronger than pattern-label agreement alone.

The paper combines ranked recommendations, several evaluated candidates and outcome-based transitions. It does not establish a separately frozen selector transferred across an independent set of new decision problems. Three datasets are the decision cases; their many data rows or hyperparameter combinations are not independent selector cases. Exact GPT snapshot/settings, repeated advice, complete preprocessing, CV folds/scoring/refit policy, and run seeds are not fully specified in the read edition. Prompt-supplied data and later training/test information also need a precise timing boundary before deployment claims.

## Results and reconstruction limits

| Case | Reported result and proper limit |
| --- | --- |
| Heart failure | Logistic regression, LinearSVC and random forest each have accuracy .8167. Reported AUCs are .8588, .7529 and .8896, respectively. Logistic regression improves on LinearSVC's AUC but is not the largest AUC in that block. A classification-wide superiority statement conceals accuracy ties and metric-dependent rankings. |
| Diabetes | Logistic regression accuracy .9604 versus SGD .9599, both AUC .9625. Random forest/gradient boosting reach .9721/.9723 accuracy, but evaluating additional suggested models is not identical to validating a predeclared first-choice rule. No confidence interval or independent selector replication establishes a general advantage. |
| Car prices | Scikit-first Ridge has RMSE 339,373.6684 and R² .6226; GPT-first random forest has RMSE 360,838.8792 and R² .5733. Random forest has lower MAE (119,192.8818 versus 122,614.1828). Keep the adverse case and metric trade-off rather than retrospectively choosing the winning metric/model. |

Figure 9's Python dictionary repeats the same `SVR` key for linear and RBF grids. If executed literally, the latter replaces the former; a full evaluator is needed to reconcile intended and executed comparisons. The PDF supplies parameter grids and printed scores, but no linked complete evaluator or run archive. Targeted title/author/artifact searches did not identify a verified companion repository in this pass. This is an acquisition/reconstruction limit, not evidence that no artifact exists.

Costs, human use and broader deployment remain unmeasured; the paper explicitly proposes real-world integration and wider evaluation as future work. Its future idea of simulating human subjects with LLMs is neither performed evidence nor authorization for ALF workers. No clinical or deployment conclusion is adopted from these illustrative datasets.

## Consequence for ALF

**Narrow the uniqueness claim further:** executable evaluation of LLM recommendations against conventional selection rules already exists. ALF cannot claim that transition as new. Its candidate contribution remains whether **decision-time architectural responsibility information** improves prospective coding-agent maintenance choices beyond a credible default/ordinary review.

**Retain with source:** compare declared actions on common outcomes, record ties/adverse cases, and distinguish verbal rationale from mechanism. **Strengthen:** freeze the first choice, fallback or any adaptive search policy, its primary utility and full cost before outcomes; do not compare a selected portfolio winner with a single baseline choice or switch metrics afterward. Preserve independent decision profiles separately from executor repetitions.

The exact conventional-selector predecessor, **Adaptive Method for Machine Learning Model Selection in Data Science Projects**, `10.1109/BigData55660.2022.10020386`, is now a consequential full-reading lead for baseline derivation. S22/S01 remain necessary for evaluation and information-cost conventions; S23 for ordinary-judgment comparisons. Completing this PDF neither confirms the proposal nor settles those dependencies.
