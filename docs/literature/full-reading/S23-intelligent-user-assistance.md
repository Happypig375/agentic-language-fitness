# S23 — Intelligent assistance for data-mining method selection

**Full publisher paper and supplement read, 2026-09-16 HKT; main Codex AI session.** This is source reconstruction and bounded artifact inspection, not model execution, experimental reproduction or human approval. [PLAN](../../../PLAN.md) retains the experimental holds.

## Identity and coverage

Patrick Zschech, Richard Horn, Daniel Höschele, Christian Janiesch and Kai Heinrich, **Intelligent User Assistance for Automated Data Mining Method Selection**, *Business & Information Systems Engineering* 62(3), 227–247 (2020), DOI [10.1007/s12599-020-00642-3](https://doi.org/10.1007/s12599-020-00642-3). The publisher and primary PDF identify Richard Horn; Scite's Richard L. Van Horn attribution is not used.

| Asset | Exact coverage and identity |
| --- | --- |
| Publisher paper | Zotero parent `Z628RY2C`, PDF `8STU578C`, collection `PKLXQNEE`; 21 pages, 2,142,139 bytes; SHA-256 `a56e93e0699460b736f761fa0abe4c76eedca6bae71c995c2b990b1a88993d20` |
| Paper reading | All PDF pp. 1–21, including references pp. 20–21; all eight figures and nine tables visually inspected on pp. 5–6, 9–17; identity p. 1 |
| Publisher supplement | [Appendices A–I](https://media.springernature.com/original/springer-static/esm/art%3A10.1007%2Fs12599-020-00642-3/MediaObjects/12599_2020_642_MOESM1_ESM.pdf), 26 PDF pages (cover plus printed 1–25), 1,022,556 bytes; SHA-256 `ad95be7f501aa6815bc3f154940fca1694ebd68cfaadca20381c8ab0457229d0`; attached as `I4PZA5D7` to the same parent; stored hash verified |
| Supplement reading | All pp. 1–26: requirements, rationale, corpus examples, embedding/model selection, prototype, all 60 evaluation cases/scores, complete questionnaire and robustness checks. Tables A1/B1/C1/D1/G1/I1–I3, figures E1/E2/F1 and the image-only instructional sheet inspected; G1's complete text with rendered layout checks; no appendix omitted |

Scite/Crossref identity checks and scoped notice queries are in the [source ledger](../selection-reading-sources-2026-09-16.md). No indexed notice was returned in that scope; this does not establish universal absence.

## What the system and evaluation do

The text-based assistant maps a natural-language problem description to **three broad method classes**: clustering, prediction (classification/regression), and frequent-pattern mining (association/sequence mining). It provides scores and an illustrative method explanation/application. It does not select an existing source package or test its subsequent maintenance behavior. The design-science motivation draws on practitioner exchanges, prior requirements research and the authors' experience; these are not an intervention study of users' realized benefits (paper pp. 5–9, supplement A–B).

The learning base begins with approximately 50,000 documents from Elsevier, arXiv and Medium. Syntactic cleaning produces roughly 45,000 RICH documents for embeddings. Semantic filtering uses sentence representations, DBSCAN noise removal and proximity to selected definitions; class balancing yields about 7,300 DEF records. Synonym replacement and Markov generation expand this to about 22,000 AUG records (pp. 9–11). Calling all underlying material academic would overlook Medium.

The authors search 36 FastText and 480 DAN configurations and train 14,876 classifier variants. They compare alternative embeddings/classifiers, then combine promising SVM, LSTM and GRU predictions using performance-derived weights. Supplement D explicitly evaluates embedding alternatives on the validation dataset; pp. 11–13 and 16 describe using that external dataset to select the final components and ensemble. The same **60 balanced problem descriptions, 20 per class**, support the reported final comparison. These differ from the training corpus, but their role in selecting the method prevents treating them as a separately untouched confirmatory test.

The human reference comprises 20 German master's students with limited data-mining experience. After an introductory sheet, they assign one class or select “not sure” for each of 60 randomly ordered descriptions, taking 25–38 minutes. The questionnaire permits requesting the introductory sheet again and forbids multiple answers (supplement H). Three more experienced graduate students supplied a 91% pretest average; this does not establish universally unambiguous labels. Participants **were not randomized to receive the assistant**. Their unassisted judgment is a comparator, not evidence of improvement from using the system.

The simpler text baselines use TF–IDF with SVM or MLP, deliberately without hyperparameter optimization. The full configuration changes representations, model families, ensemble composition and tuning effort. It is consequently a comparison of bundles; its difference cannot isolate context extraction alone or establish superiority over an equally resourced ordinary analysis.

## Results, uncertainty and practical limits

Table 7 reports accuracies of .33 for random guessing, .55 for novices, .58 for the strongest baseline and .90 for the full configuration. Appendix G's class maxima account for **54/60** full-system successes: three clustering errors (CL7/CL9/CL11), no prediction errors, and three frequent-pattern errors (AR1/AR5/AR18). The baseline accounts for 35/60. This is a check of printed scores, not rerunning a classifier. Retain the domain-specific errors and the selection-on-validation limit with the reported gain.

The statistical tests use **scores for the designated correct class**, not binary recommendation correctness. Novice scores are the fraction of students choosing that class, whereas system scores come from classifiers. Paper pp. 16–17 apply a variance-robust ANOVA followed by independent t tests with Bonferroni adjustment. The table uses 240 group observations (error df 236), although the same 60 cases appear under each method. The reported procedure does not account for this pairing; vote fractions and classifier confidence also have different meanings. Greater confidence alone is not calibration, reliability or behavioral utility. The reported significance cannot validate ALF's architecture effect or supply a sample-size/effect assumption.

Appendix I documents keyword, domain-entity and length sensitivity. Some substitutions deliberately change the task, so those flips are not invariance failures. Others reveal lexical/domain dependencies; the authors acknowledge a tendency toward frequent-pattern mining for sales-related descriptions. The checks are selected examples, not a new independent population estimate. Paper p. 19 explicitly leaves practical usefulness, usability, comprehensibility and target-group suitability to further socio-technical evaluation. Economic feasibility is a design rationale; no measured net savings or adoption effect is established.

## Bounded artifact reconstruction

Inspected the primary [rsmttud/Recommender-System repository](https://github.com/rsmttud/Recommender-System/tree/57598ae92b0f9e97d4488712ee8da4e31d3d5a44), pinned at `57598ae92b0f9e97d4488712ee8da4e31d3d5a44`: complete tree listing, README, app/helper routing, `RecommendationFacade`, `Prediction`, `Ensemble`, `SystemEvaluation`, and a bounded inspection of the small evaluation ZIP. No author module was imported or executed.

The facade combines SVM/DAN, GRU/DAN and LSTM/FastText with stored weights `.725/.75/.775`. The ensemble code forms a weighted sum without dividing by the weight total; the UI helper then applies `log2(1.01+x)` and rounds. These operations preserve an argmax but do not themselves make a calibrated probability distribution. Do not substitute these displayed values for Appendix G's near-normalized score triples or assume this repository revision generated the publication tables. The evaluation helper calculates classification accuracy from argmax outputs; it is not a complete reproduction of the paper's confidence-based inference.

`datasets/eval_data.zip` is available (18,482 bytes, SHA-256 `baa87fe9cbdeea3f8a6a730bcc88544c8d70a61d2c357faf1949c9cd762f504f`), with class-labeled text cases. Inspected examples differ in wording/content from Appendix G, including its machine-energy clustering and player-price descriptions; no exact publication-run manifest was established. Other training data/models are listed, and the README points to an approximately 11 GB container and an external FastText model. These were not fetched or run. Availability of this prototype does not close publication-edition, complete tuning-log or evaluation-reproduction gaps.

## Consequences and follow-up decision

**Uniqueness:** Natural-language advice, design requirements, explicit ordinary-judgment references, contextual representations and downstream method illustrations are established. ALF's remaining question concerns the incremental prospective behavioral value of architectural information under a declared coding-agent policy, not invention of assistance or structured advice.

**Value:** Retain a credible ordinary-review comparison and report analysis effort. Keep technical choice quality distinct from human benefit, adoption and return on investment. If human assistance later becomes an intended causal claim, it needs its own allocation and evaluation; this reading authorizes none.

**Rigor:** Freeze all selection-development decisions before evaluation profiles. Match comparator information and effort where claiming a method-specific benefit, keep cases paired, distinguish confidence from correctness, preserve abstentions/valid alternatives, and define which meaning-preserving or task-changing perturbations are being examined.

ASlib (S01) and the existing selection-method sources remain consequential for decision units and cost conventions. The direct architecture/code sources S05/S08/S03 are now more discriminating for the residual architectural-information claim than further general NLP classifier comparisons. S21 remains blocked but relevant to a transparent ordinary criteria/weighting comparator. The earlier 2019 text-recommender precursor is historically relevant; a full read is conditional on a specific development-history claim, because this complete 2020 paper and supplement already reconstruct the advice/evaluation mechanism used here. No new broad novelty assertion follows from that deferral.
