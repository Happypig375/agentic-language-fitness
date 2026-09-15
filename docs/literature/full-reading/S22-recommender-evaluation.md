# S22 — Evaluating Recommendation Systems

**Full author-manuscript reading completed 2026-09-16 HKT by the main Codex AI session.** This is a methodological chapter, not an ALF experiment or a reproduction of the studies it cites. [DOI](https://doi.org/10.1007/978-0-387-85820-3_8); [lawful author-hosted PDF](https://www.ise.bgu.ac.il/faculty/liorr/recsyshb/chEvaluation.pdf).

## Identity and coverage

Guy Shani and Asela Gunawardana, *Evaluating Recommendation Systems*, in *Recommender Systems Handbook*, printed 2011, pp. 257–297; the publisher metadata also records online publication in 2010. The acquired manuscript numbers its pages 1–41. Its equations and typography have not been reconciled with the publisher edition.

| Asset | Recorded evidence |
| --- | --- |
| Zotero parent / PDF | `YGCJ62UT` / `INXXCCBT`, existing collection `PKLXQNEE` |
| PDF | 41 pages; 218,925 bytes |
| SHA-256 | `df0dbc90d31eac88e9e9a165635c67258cca49f103f9798b605e85e61e503ac7` |
| Text coverage | All PDF pp. 1–41, including all sections, four worked examples and references on pp. 36–41 |
| Visual checks | Identity p. 1; statistical passage/equation pp. 11–13; metric equations pp. 16–17, 20–22, 24; confidence example p. 26; the only numbered table, Table 1 on p. 17. No numbered figures or separate appendix |
| Supplements | No companion experimental artifact identified in the chapter; cited studies were not thereby reproduced or fully read |

## Reconstruction and relevance

The chapter evaluates **recommendation systems for a specified application**, distinguishing offline experiments, task-based user studies and online behavior. Its review covers accuracy, coverage, confidence, trust, novelty, serendipity, diversity, utility, risk, robustness, privacy, adaptivity and scalability. These are different properties with different observation requirements, not interchangeable definitions of quality.

- **Information and sampling (§2, pp. 2–10):** choose a hypothesis and domain-relevant data; record filtering and the information hidden at prediction time. Random versus temporal withholding answers different questions. Filtering users/items and using unrealistic user simulations can change the target population. Development/pilot data used to tune a method cannot also provide its independent confirmation.
- **Experimental unit (§2.4, pp. 11–13):** repeated recommendations to one user need not be independent. The analogous ALF unit is a genuinely distinct adoption/change profile; repeated candidate runs do not manufacture more selector decisions. The chapter also warns against testing many variants or metrics until one appears significant.
- **Relevance units (§3.2, pp. 15–23):** predicting ratings, retrieving used items and ranking alternatives require different targets and denominators. Unused items may simply have been unknown to the user. Reference ties can mean either missing preference information or actual indifference; these require different penalties. A single exact historical choice is therefore not automatically the only valid recommendation.
- **Coverage and confidence (§§3.3–3.5, pp. 24–27):** high performance on a selected subset is insufficient without coverage; confidence in an outcome differs from a user's trust. Reporting confidence may itself change the user's subsequent inspection. ALF abstentions and ties belong in the all-profile accounting, and explanation requests remain interventions.
- **Useful outcomes (§§3.8–3.10, pp. 30–32):** an application's utility and costs need explicit definitions. Accuracy does not establish business benefit, and average monetary cost is not automatically comparable user utility. Online/user evidence is needed for claims about acceptance, interaction or realized user benefit. A fixed-executor ALF comparison can estimate behavioral choice quality under its policy, not adoption or end-to-end return on analysis effort.

## Verified manuscript problems; do not copy the formulas

The rendered pages confirm that the following are present in this acquired manuscript, rather than extraction artifacts. They are bounded edition-specific observations, not a claim that every edition contains these errors or that the chapter's conceptual distinctions are unusable.

1. **P. 11 reverses the rejection direction** in one sentence, saying to reject above the threshold, immediately followed by text saying that such a result is not significant. Its informal probability-of-luck interpretation also should not be used as a definition of a p-value.
2. **P. 12, equation (1), holds the binomial coefficient denominator constant across the tail sum.** With eight wins and two losses, its printed expression gives 135/1024, whereas summing the actual binomial terms for 8, 9 and 10 gives 56/1024. This is our arithmetic check, not an experimental result. Tail direction, ties and one/two-sided hypotheses still require specification.
3. **P. 13 labels an independence-product threshold as Bonferroni.** The displayed `1 − (1 − α)^(1/N)` is not the Bonferroni `α/N` bound. Do not transfer the chapter's threshold or independence language into ALF. Its cited Demšar primary methods paper is promoted as S26 to resolve the statistical guidance.
4. **P. 16, equation (3), adds a square root to MAE.** The adjacent numerical illustration also does not produce the stated disagreement: errors `(2,2,2,0)` versus `(3,0,0,0)` give ordinary MAEs 1.5 versus 0.75 and RMSEs √3 versus 1.5, so both prefer the second. This is another direct arithmetic check.
5. **Other displayed definitions need independent checking before use.** On p. 20 the signed products labeled as counts can become negative; a perfectly ordered single pair yields an impossible negative NDPM under the printed equations. P. 22's purported per-user R-score also sums over users, and p. 26 uses A's denominator in B's expression. None of these formulas is adopted as an ALF endpoint.

## Evidence-to-design consequences and next sources

**Retain** the separation of prediction/ranking quality, coverage, interaction and utility, and the need for an application-defined outcome. **Reject** treating an offline proxy, a convincing explanation, or a significant accuracy difference as sufficient evidence of useful adoption. Keep the relevant population and observational unit explicit, and freeze the primary endpoint/comparison before outcomes.

S26, **Demšar (2006), Statistical Comparisons of Classifiers over Multiple Data Sets**, is now necessary to inspect the chapter's statistical foundation; the JMLR PDF is openly available. The existing S01 ASlib reading remains necessary for selector/default/oracle conventions and information costs. S23's actual user-assistance evidence can test the boundary between selector quality and user benefit. These are directed dependencies, not a requirement to read every reference in this chapter. This reading allocates no user study, candidate run or new statistical experiment.

**Three criteria:** generic recommendation evaluation is established prior art, so uniqueness remains about the proposed architectural information and maintenance decision. Value requires a meaningful utility or behavioral endpoint and comparison cost, not an assumed accuracy-to-benefit bridge. Methodological rigor improves by respecting those boundaries and correcting formulas, but the ALF case, independent profiles and apparatus remain unvalidated.
