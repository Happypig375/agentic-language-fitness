# S26 — Statistical comparisons across data sets

**Full reading completed 2026-09-16 HKT, main Codex AI session.** Janez Demšar, *Statistical Comparisons of Classifiers over Multiple Data Sets*, JMLR 7(1), 1–30 (2006). [Publisher record](https://jmlr.org/papers/v7/demsar06a.html); [publisher PDF](https://jmlr.org/papers/volume7/demsar06a/demsar06a.pdf). No DOI is asserted from the title search, which did not return this paper; identity comes from JMLR and the PDF.

## Asset and coverage

| Field | Evidence |
| --- | --- |
| PDF | 30 pages, 273,373 bytes, JMLR publisher copy |
| Zotero | Parent `53J4YFRJ`, PDF `4P28RRAQ`, existing collection `PKLXQNEE`; stored hash verified |
| SHA-256 | `aa5fa1c71338d0d380e7a97e3503ce486d4e5798069647a8d39f57a1f99a7c8c` |
| Reading | All pp. 1–30 including references pp. 28–30; no appendix |
| Visual inspection | Identity p. 1; all seven numbered tables on pp. 4, 7, 9, 11, 12, 14, 23; unnumbered comparison p. 15; all seven figures on pp. 16, 21, 22, 24–26; consequential formula/assumption pages 7, 9–12 |
| Supplement/reproduction | C4.5, Orange and UCI sources are described, but no paper-specific executable bundle was reconstructed or run. This is full method reading, not replication |

## What the paper actually establishes

The problem is comparison of **two or more classifiers across multiple data sets**, assuming each data-set score is estimated reliably. The independent sample size is the number of data sets, not their rows or cross-validation folds (pp. 2, 5, 15). Repeated within-data-set runs improve score estimation; they do not supply independent draws of different problems. Data-set independence is assumed, not guaranteed by naming several benchmarks.

The review of ICML 1999–2003 finds varied and often inadequately adjusted comparison practices (Table 1). The methodological argument distinguishes mean differences, signed ranks, win counts and within-data-set algorithm ranks. These answer different questions and make different commensurability assumptions. The paper recommends Wilcoxon for two classifiers and Friedman plus appropriate post-hoc comparisons for several, favoring comparisons to a prespecified control when that is the real question (pp. 6–16). Failure to find a difference is not an equivalence result; average ranks and critical-difference diagrams do not express practical utility differences.

Its empirical study uses seven real classifiers and 40 UCI data sets, repeatedly drawing sets of ten with 1,000 repetitions. Selection probabilities are deliberately biased using already measured accuracy differences, to study statistical-test behavior (pp. 17–20). The author explicitly distinguishes that simulation from an acceptable algorithm-evaluation sampling procedure. It **does not estimate Type I/II errors against known ground truth**. Lower p-values and more rejections here are not direct evidence of superior error calibration. The two proposed repeatability measures also rank tests differently because agreement at a threshold depends on proximity to that threshold (Figures 3–7; conclusion pp. 26–28).

## Necessary caveats and checks

- **P-value interpretation:** p. 9 correctly distinguishes the probability of the observations under the null from the probability of the null, resolving S22's misleading informal wording.
- **Multiplicity:** p. 12 gives Bonferroni-Dunn's division by the comparison count; pp. 12–13 distinguish Holm's sequential procedure. However, p. 10 also incorrectly describes Bonferroni as supposing independence. The [NIST handbook's general inequality](https://www.itl.nist.gov/div898/handbook/prc/section4/prc473.htm) applies to arbitrary events: with valid individual tests, Bonferroni's family-wise bound does not require independence. S22's product-based threshold must not be substituted for it.
- **Small samples and ties:** Table 3 lists five wins out of five as sufficient for a two-sided 5% sign test. Direct binomial arithmetic gives `2 × (1/2)^5 = 0.0625`, so that cell cannot justify an exact two-sided 5% rejection. The text also splits ties, rather than providing a universal rule suitable for every implementation. Do not copy critical values or tie handling blindly.
- **Wilcoxon is not assumption-free:** its target, symmetry, independent paired observations and treatment of ties/zeros matter. The [SciPy reference](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wilcoxon.html), inspected as implementation documentation, makes the symmetry target and differing zero conventions explicit and warns that the ordinary exact calculation changes with ties/zeros. No SciPy test was run or chosen as an ALF protocol here.

## Consequences for ALF

Retain **independent profiles as the unit of generalization**, preserve within-profile executor uncertainty, and specify the primary contrast rather than searching all pairwise/metric comparisons. The case's common behavioral utility can justify a mean-effect estimand that generic cross-domain ranks do not answer. Thus this reading does **not** mandate replacing the proposal's meaningful-effect analysis with a Wilcoxon/Friedman significance gate.

Use ties, failed runs and uniformly good/bad profiles in the declared population. Do not select final profiles from favorable measured package differences, count only significant wins, or interpret a nonsignificant result as interchangeability. Exact uncertainty methods and assumptions remain to be specified for the eventual outcome hierarchy; importing a famous test does not validate the apparatus or its sample size.

This resolves the immediate S22 statistical-reference dependency sufficiently to reject its faulty formulas. S01 remains the more direct selection-evaluation foundation. No further generic statistics-paper expansion is required unless the final outcome/sampling design demands it. **Uniqueness:** statistical comparison is established; **value:** rank significance is not useful improvement; **rigor:** conditional on valid units, assumptions, outcomes and adequate information, all still to be specified for ALF. No new experiment is authorized.
