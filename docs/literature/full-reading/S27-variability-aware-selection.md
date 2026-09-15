# S27 — Variability-aware model selection

**Full arXiv-v1 reading completed 2026-09-16 HKT by the main Codex AI session.** Cristina Tavares, Nathalia Nascimento, Paulo Alencar and Donald Cowan, *Variability-Aware Machine Learning Model Selection: Feature Modeling, Instantiation, and Experimental Case Study*. [ArXiv v1](https://arxiv.org/abs/2501.00532v1), 31 December 2024; [journal DOI](https://doi.org/10.1109/ACCESS.2025.3558218), IEEE Access 13, 62527–62542 (2025). Scite's journal hit misnames an author; the primary PDF/Crossref authors above control.

## Asset and coverage

| Field | Evidence |
| --- | --- |
| PDF | ArXiv v1, 14 pages, 2,750,656 bytes |
| Zotero | Parent `R2JC2WTL`, PDF `HGRJ8BFH`, existing collection `PKLXQNEE`; stored hash verified |
| SHA-256 | `758331feed33ca28a3d8a700130a152f6f24ec569138bf1ff935ee4ba648a35e` |
| Reading | All pp. 1–14, including all 32 references; no appendix |
| Visual checks | Identity p. 1; all eight figures on pp. 5–8 and 13; constraints pp. 8–10; result block p. 10 and the only table, Table I, p. 11 |
| Edition/access limit | Publisher PDF request returned HTTP 418; the 16-page journal edition was not compared. The arXiv record's overlap notice concerns another preprint, not a retraction finding |
| Artifact limit | No companion executable repository linked in this PDF or verified by the targeted title/artifact search. This does not prove none exists. No model training or benchmark reproduced |

## Reconstruction

The paper explicitly extends the preliminary 2021 work and **S25 (2022)** (p. 2). It formalizes existing selection heuristics through feature diagrams and constraints, rather than learning a new selector from labeled evaluation cases. Five phases identify factors, instantiate a heuristic, design a case, select candidate techniques and evaluate results. It uses Scikit-learn's version-1.0.1 flowchart, with information about problem type, labeled/text data, sample size, feature properties and desired performance. Formalization and design-time adaptability are central; dynamic examples are illustrative future extensions.

The empirical case uses the same 299-patient heart-failure dataset discussed in S20. Its path first recommends LinearSVC, followed by alternatives if the model does not meet a performance threshold. The authors choose an F1 target of 0.77 based on a prior paper's reported result, make a stratified 239/60 training/test split, and use GridSearchCV (pp. 9–10). They report F1 0.780, MCC 0.672 and balanced accuracy 0.848 for LinearSVC, compared with results quoted from earlier studies (Table I). This is **executed model evaluation**, not only expert agreement with a suggested label.

It is nevertheless a **single selected application**, not independent validation of a general policy's expected benefit. Matching a split ratio does not ensure identical patients, preprocessing, tuning, features or random states across the published comparisons. The full grid, seeds, fold policy and run-level outputs are not specified sufficiently here to reconstruct that comparison. No measured time saving, ordinary-review comparison, user adoption effect, or out-of-sample evaluation over independently selected applications establishes the proposed broader benefits.

## Material limits

- **A heuristic representation is not an improved heuristic.** The authors explicitly say in the threats section (p. 11) that they do not evaluate the heuristics' correctness. A comparator using the same heuristic without the feature diagrams would be needed to isolate added value from the representation. ALF similarly needs an information/budget-matched ordinary review if it claims value for a responsibility-analysis method.
- **The boundary between advice and search matters.** The recommendation queue uses a performance-dependent stopping rule. A future benchmark must say whether those evaluations are part of selection and charge their cost. It cannot compare a pre-execution choice with a search procedure that receives uncharged outcome feedback.
- **Printed constraints need reconciliation.** The switch prose says move on when an algorithm is not working, but several rules contain `¬notWorking` (pp. 8–10). `Category ⇔ ¬(Quantity ∧ Structure)` also does not itself express mutually exclusive prediction types. These visible inconsistencies prevent treating the displayed logic as a verified executable selector.
- **The illustrations are not validated changes.** Figure 7 shows a new sample size of 1,200 where the prose describes exceeding 100,000 before switching to SGD. Figures 7–8 show 12 features, while the case prose describes 13 plus an additional target. The regression illustration retains an F1 label. These are edition-specific diagram/text discrepancies, not additional executed cases.
- **Do not import the performance advantage.** Table I's specificity is lower than one cited comparator, and test-set/class-polarity comparability is not resolved. The ALF inference needs no numerical superiority claim from this clinical illustration, so the clinical baselines are deferred unless that claim becomes necessary.

## Decision consequences

S27 strengthens the rejection of novelty for formalized conditional advice, diagrams/constraints or comparing a recommendation with executed outcomes. It does not settle whether architectural responsibility information improves **prospective coding-agent maintenance choices**. The useful residual question is the incremental behavioral benefit of that information beyond simpler, matched alternatives, with decision-time inputs and analysis/search cost made explicit.

S25 remains the exact earlier comparator dependency and is queued for a lawful full copy; S27 is not silently substituted for that edition. The next consequential readings are S23's novice/ordinary-method evidence and S01's established selector evaluation. PHOTONAI and the clinical comparison papers become necessary only if their numerical comparisons or adaptive-search mechanisms are adopted; no such claims are adopted here. **Uniqueness remains unconfirmed, value remains a testable conditional benefit, and the methodology remains a proposal requiring case and apparatus validation.**
