# S30 — Early architectural decisions at Volvo Cars

**Full main-paper reading completed 2026-09-16 HKT by the main Codex AI session.** Karl Öqvist, Jacob Messinger and Rebekka Wohlrab, *Supporting Early Architectural Decision-Making through Tradeoff Analysis: A Study with Volvo Cars*, FSE Companion 2024, pp. 411–416. [DOI](https://doi.org/10.1145/3663529.3663860).

## Asset and coverage

| Field | Evidence |
| --- | --- |
| Zotero | Parent `KW5W6GZM`, PDF `XPVV88YQ`, collection `PKLXQNEE` |
| PDF | [Chalmers publisher copy](https://research.chalmers.se/publication/542772/file/542772_Fulltext.pdf); seven PDF pages including cover; 647,649 bytes; SHA-256 `a8004f530bb97fd81214458167c53689d4c97b66a37b066391613f60577a4c06` |
| Reading | All seven PDF pages, six article pages and 22 references; all four figures checked visually on PDF pp. 4–6; no main-paper tables or appendix |
| Supplement | [Figshare v2](https://doi.org/10.6084/m9.figshare.24258439.v2) metadata enumerates 16 assets, including interview guide, themes/codes, study overview and component/parameter descriptions. File and archive downloads through the public API/ndownloader routes returned 403; these bodies remain unread |
| Artifact | [Pinned repository](https://github.com/karloq/architectural-tradeoff-analysis/tree/e80a524d6f641a9a3fdbe9f3469bcdf242dc5568), commit `e80a524d6f641a9a3fdbe9f3469bcdf242dc5568`; complete untruncated inventory, README, all source cells of PCA/CSV-merger/feature-model notebooks, complete `pcatools.py`, and both scaling run scripts inspected |
| Limit | Static source and data-dimension checks only. No author notebook, Simulink model, PCA, clustering, AWS workload or interview analysis was executed/reproduced. Binary Simulink models and the separate decision-tree notebook were not inspected |

## What was evaluated

This design-science study involved five Volvo Cars practitioners: three architects, a cloud architect and an engineering lead, spanning approximately 3 to 25 years of experience. Five initial interviews lasted 20–30 minutes; three development/evaluation iterations each lasted five weeks and included focus-group feedback (article pp. 412–413). Participants helped shape the method and judged its usefulness; they were not an independent randomized test population.

The case concerns vehicle battery telemetry. Seven AWS architecture candidates across Simple, Stream and Sophisticated families are modeled in Simulink. The nominal simulated workload sends 8 kB each second from 1,000 vehicles for 15 minutes, with a tenfold load comparison. Quantities include latency, modeled cost, a complexity count of blocks/parameters, and load sensitivity. These are neither measured maintenance quality nor an actual cloud deployment. The authors explicitly caution that the specific values are not factual claims about deployed systems (pp. 413, 415).

After simulation, the method filters the configuration table, performs Pareto-based selection, and uses radar plots, component/quality correlations and PCA displays to support architecture-, component- and parameter-level discussion (Figures 1–4). Thus quality outcomes have already been obtained before the explanation step. It is not source-only prediction of unobserved future coding-agent behavior.

Participants reported that the plots exposed tradeoffs consistent with prior experience and stimulated useful discussion. PCA was difficult without experience; radar plots helped quick comparisons. The first model/scripts cost one full-time person-week, subsequent models a few hours, and plots minutes (p. 415). Those reported setup times do not establish net decision savings, and there is no comparison of later decision correctness or maintenance outcomes against ordinary review.

The paper itself asks whether constructing the simulation input already supplies much of the benefit, or whether visualization and discussion add it. This is direct support for a rival explanation, not evidence that the analysis has no value.

## Bounded reconstruction findings

- **Counts remain edition/artifact-specific.** Article p. 413 says 12,136 unique simulated setups; p. 414 says 1,200 configurations. The notebook reads `April21/combined.csv`, which has 14,000 finite rows, 2,000 per topology. Exact row deduplication leaves 12,152; the displayed cost threshold of 50 leaves 11,140. Its stored output reports 1,012 filtered rows, consistent with the latter two counts. No inspected number justifies silently replacing either paper denominator. The unrelated `official_runs/complete_1.csv` has 80,920 rows and only nine columns; its filename does not establish that it is this paper's analyzed table.
- **Figure 3's correlation direction needs care.** Caching is displayed with negative correlations with all four numerical quality measures, although the prose calls its correlation with quality positive. Here high cost/latency/complexity/load sensitivity means poor quality. Interpret favorable quality separately from a positive numeric correlation; do not repeat the prose as a sign claim.
- **The PCA implementation differs from a direct PCA of configuration observations.** Notebook cells construct the variables' correlation matrix; `createPCA` fits/transforms its rows. Display helpers then min–max scale the component scores to [−1, 1], and `specialPCA` groups plotted points with DBSCAN and offsets displayed quality markers. The main paper calls the graph a loading plot; these coordinates should not be imported as ordinary variable loadings or causal effects without reconciliation.
- **Figure/data selection is not frozen by a caption.** Figure 4 is described as the top 15% per architecture. The inspected final parameter-analysis cell instead uses all `df_filtered` rows. The artifact computes 15% subsets elsewhere, so this establishes a current source-path difference, not which version generated the published figure.
- **“Top 15%” need not mean exactly 15%.** The helper repeatedly removes complete nondominated fronts until its requested count is reached or exceeded. Radar plots use filtered means and different hand-specified log/linear/standardization transformations per measure, rather than a common direct numerical scale. Neither visualization area nor explained variance is a decision-utility estimate.
- **The simulator scripts are not a publication-ready reproduction recipe.** The multi-topology script is currently restricted to `for topo = 5:5`, with 2,000 configurations and paired fleet loads. The separate scaling script uses 15 configurations and ten-second parameter values, with a different scalability aggregation. No claim is made that these current settings generated the publication; the underlying block models and missing supplemental definitions would be needed to reconcile them.

## Consequences for research discovery

**Uniqueness:** practitioner-facing architectural tradeoff explanation and qualitative evaluation already exist. Do not claim their absence. This paper does not test the incremental value of responsibility/coordination information for LLM coding-agent maintenance.

**Value:** the interviews support an industrial need for understanding tradeoffs and report perceived usefulness in this case. They do not validate ALF's adoption benefit, savings or F#/Codex-specific beneficiary fit. A method-specific claim must compare equally informed alternatives and account for modeling/analysis effort.

**Rigor:** distinguish model construction, information acquisition, visualization and human discussion. A fixed-executor behavioral comparison can test coding-agent outcomes; it cannot by itself establish an assisted-human decision benefit. Preserve all-profile outcomes rather than selecting only favorable Pareto cases after observing performance.

S31's nine-participant study remains a consequential access-limited follow-up if the architecture-choice candidate is retained. The Figshare guide/themes remain a method gap for detailed qualitative-method reuse. With the user's new question-discovery objective, this source informs candidate comparison; it does not oblige retaining the preceding architecture-selection proposal.
