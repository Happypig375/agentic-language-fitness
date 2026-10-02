# S155 — favorable design guidelines, measured through document tasks

**Complete selected-report reading, 2026-10-01 HKT.** Lionel C. Briand, Christian Bunse and John W. Daly, *A Controlled Experiment for Evaluating Quality Guidelines on the Maintainability of Object-Oriented Designs*, **IESE-Report 002.99/E, version 1.1, May 1999**. The [public institutional PDF](https://publica-rest.fraunhofer.de/server/api/core/bitstreams/45fa8ca4-dfd0-47dd-b114-73383c0e9beb/content) predates the 2001 TSE publication, [DOI 10.1109/32.926174](https://doi.org/10.1109/32.926174), 27(6), 513–530. Claims below concern the inspected report; its correspondence to the final journal text is unverified.

## Identity, coverage and missing materials

Native Zotero parent `ITEW7T4M`, report attachment `KEP3UXAJ`, note `4R8T7J8A`. The record preceded intentional body reading. Native attachment identity and hash were rechecked: **53 PDF pages, 262,061 bytes, SHA-256 `e5d958a7e9a8c4143074644ff16c1a45144025e45d7e65399e5a5283ec174e25`**. Coverage includes the cover/front matter, all 44 numbered body/reference/appendix pages, document-information page, five figures, seven tables, three numbered equations, four appendices A–D, eight footnotes and 29 references. Pages 2, 4 and 6 are blank, visually verified.

Text was read throughout; **25 distinct page images** were inspected: PDF pp. 1–2, 4, 6, 16–17, 20–21, 26–33 and 45–53. These cover every figure/table/equation, the translated questionnaire, degradation definitions, task examples and edition statement. Aggregate chart values and Table 7 labels were transcribed for limited local arithmetic; no original participant dataset, statistical test, experiment or author software was run. PDF, extraction, images and arithmetic remain outside Git.

The report lists a 1997 *Replication package for Design Experiment SE I WS 96-97* but gives no direct package URL. Its general ISERN bibliography route returns 404 through ordinary HTTP/HTTPS. Targeted searches recover the report citation, not the package. Both complete design-document sets, scoring keys and participant-level data therefore remain unavailable. Publisher/Unpaywall routes did not recover the 2001 journal file; the IEEE web page requests robot verification and the native request returns an empty 202 response. No challenge was bypassed. A listed 41-page ISERN 99-07 and the 1997 ESP account remain related, unverified editions. The institutional journal metadata's 513–529 differs from Crossref/DBLP's 513–530; the latter bibliographic identity is retained without claiming final-PDF inspection.

## What actually varies

The study investigates a bundle of Coad/Yourdon design principles: coupling, cohesion, naming/clarity, meaningful specialization and class simplicity. They are deliberately treated together because the authors consider them interdependent. The intervention is not one isolated structural metric.

Participants compare **two different application domains**: a conforming temperature/house controller and a degraded ATM design. The degraded version was produced from an initially conforming ATM design, but the original ATM is not an experimental arm. Both used OMT and roughly thirty pages of description, requirements and design. Layout, notation, requirements coverage and detail were harmonized after problems in the earlier study.

Degradations add interaction paths, responsibilities, inappropriate inheritance, unused but meaningful fields/methods, inconsistent names and merged classes. Appendix B makes naming and extra information-processing burden part of the treatment. For original ATM / degraded ATM / conforming controller, Table 1 reports respectively **14/18/13 classes**, **20/25/18 operations**, **12/16/9 associations**, **4/8/2 inheritance relationships** and **0/8/0 inconsistencies**. These are neither same-program alternatives nor a source-size-controlled contrast. Table 2 uses a special hierarchy-level aggregation for CBO to avoid dilution by added subclasses; its values are not ordinary per-class averages. Cohesion could not be measured from the available high-level documents.

The authors acknowledge domain confounding and explain their choice: different systems permit each person to act as their own control without immediately repeating the same design. Comparable metrics, textbook domains, curriculum familiarity, author pretesting and nonsignificant difficulty opinions are useful checks, but do not independently establish equal cognitive difficulty. Randomizing **presentation order** cannot separate guideline effects from the system permanently assigned to each guideline condition.

## People, tasks and observation

Thirty-three Kaiserslautern software-engineering students volunteered after course instruction; reported prior practice/design/impact-analysis experience was generally low. A university-scheduling example provided an interactive training session the preceding week. Two consecutive experimental days each allowed **90 minutes**, with participants working on one system per day. Drawing group letters determined which design came first; the order was counterbalanced. Hypotheses were not disclosed, and monitors withheld assistance judged to improve task performance.

For each system, participants answered seven conceptually matched understanding questions and marked locations needing change for two requests. They **did not implement those changes**. Marks on the documents were cross-checked against a summary form. Appendix D's controller examples remove rain detection and add on-demand state printing; it does not supply the full ATM task set or answer key. Tasks were intentionally focused on parts affected by the degradations, so they are not a sample of ordinary future requests.

The six outcomes are understanding time, correct understanding answers, impact-analysis time, completeness (correct locations / required locations), precision (correct locations / locations selected), and rate (correct locations / minute). The report calls precision `Mod_Corr`; this is **not executable correctness**, complete-change success or freedom from regressions. Understanding accuracy is inconsistently labeled `Und_Corr` in definitions and `Und_Comp` in tables.

The sample accounting needs care. Section 2.11 says 33 controller and 31 ATM observations after one person missed the second day, while Table 4 shows **33/32** for understanding and completeness. Phase timings are available for only **22/19** understanding observations and **21/19** impact observations: many participants recorded total time without the phase boundary. The paired tests use still different valid counts. Nonsignificant timing differences do not show that missingness is random; the authors leave that threat uncertain. Tight time limits also constrain interpretation of completion time.

## Positive results and their limits

Tables 4–6 report the following. Means use each outcome's observed sample; they are not a reconstructed complete-case paired dataset.

| Outcome | Conforming / degraded mean | Paired valid N | Reported result |
| --- | --- | --- | --- |
| Understanding time, minutes | 48.18 / 46.74 | 18 | No detected difference; the conforming mean is slightly longer |
| Correct understanding answers, maximum seven | 5.64 / 4.31 | 32 | Favors conforming; reported standardized difference 1.09, Z = 3.46, p printed .00 |
| Impact-analysis time, minutes | 29.71 / 30.21 | 17 | No detected difference |
| Impact completeness | .66 / .45 | 32 | Favors conforming; standardized difference .84, Z = 3.42, p printed .00 |
| Impact precision | .95 / .93 | 30 | p = .07, not significant at the declared .05 |
| Correct locations per minute | .65 / .37 | 17 | Favors conforming; standardized difference .61, Z = 2.11, p = .02 |

The study selected **one-sided alpha .05** after power planning from the preceding study. It uses Wilcoxon matched pairs after normality checks and says paired t-tests agree. No family-wise correction for these six outcome tests is described. Printed zero p-values are rounded. The text's description of p-values as probabilities of committing a Type I error should not be adopted as a valid interpretation of an observed p-value. Prior-effect power calculations, including an assumed effect for a newly measured outcome, do not validate actual missingness or equivalence under a null result.

Participant P26 found no correct locations for the conforming design in nine minutes. The main summaries retain this adverse observation. A later sensitivity analysis removes it and changes the precision p-value to .03. Poor performance is not established to be recording error; the significant sensitivity result should not replace the all-observation precision result. Figures 3 and 5 explicitly omit P26 from the degraded-design charts, while the conforming charts show 33 participants. Those charts are not a common complete-case comparison.

Figures 2–3 locate much of the accuracy difference in mapping requirements to classes, understanding a merged class, and describing relationships. This is plausible mechanism evidence under the chosen tasks. It does not independently identify each guideline's causal effect. Similarly, reports of difficulty with inheritance/coupling/cohesion support an interpretation but are post-task perceptions, with varying response denominators.

## Aggregate reconstruction leaves specific discrepancies

Visual checks establish several report-level limits rather than silently repairing them:

- Section 2.6 says **21 conforming / 22 degraded** change locations; Figures 4–5 show **22 conforming / 21 degraded**, with Table 7 listing 21 degraded locations.
- Figure 4's 22 printed counts sum to **500**. Dividing by 33 people and 22 locations gives approximately **.689**, rather than Table 4's .66. The prose's 21-location denominator gives .722, so that swap alone does not reconcile the conforming result. Participant data and the final journal are needed before assigning a cause.
- Figure 5's counts sum to **311**, but its 31-person sample omits P26. It must not be equated directly with Table 4's 32-person mean. Figure 2's understanding sum, 186/33, does agree with the printed 5.64 after rounding.
- Table 7 contains **eight** simplicity labels while the accompanying prose says six. Its other four guideline totals match the printed summary.
- The supplementary Kruskal–Wallis analysis treats per-location proportions as independent samples, despite repeated participants and shared designs/tasks. Its printed `p < 0.000` is also not a valid probability statement. Preserve the descriptive pattern without treating locations as independent experiments or inventing a corrected p-value.

These issues constrain exact reconstruction and component attribution. They do not remove the favorable main understanding/completeness/rate results as reported, prove the final journal contains the same discrepancies, or establish no benefit from guidelines.

## Lineage, transfer and next action

This is an **internal replication** of the OO portion of S156, using improved documents/tasks and a larger stated sample (33 versus the earlier 13). Same research group and materials lineage do not supply an independent application-family replication. [S156's supplied journal is now fully read](S156-oo-structured-design-maintainability.md), independently confirming its thirteen-participant controller/ATM comparison and document-task scope. The later report describes a new, larger internal replication with revised materials, not a duplicate publication of the same observations. S156's other journal/conference/report correspondence remains unresolved. The 1997 ESP and 1999/2001 versions also must not be counted as separate experiments without a correspondence check.

The comparison with [S94](S94-changeability-design-alternatives.md) is therefore narrower than “guidelines help” versus “guidelines hurt.” S94 changes organization within a coffee problem and asks for paper changes; S155 combines naming/structure changes with different domains and asks for answers and change locations. [S96](S96-industrial-credit-maintenance.md) additionally includes professional implementation/testing with unequal tools and documents. Each supplies useful evidence for its actual activity; none measures a Nu-specific or all-lifecycle effect.

G24's expanded incoming-citation screen and primary follow-up are recorded in the [background ledger](../nu-background-searches-2026-09-30.md). **S157 SyDRA** is selected for game-engine architecture recovery and measured human understanding/impact analysis; **S158** for practitioners' design-quality judgments, experience and testing practices. Both have since received full selected-publication reconstructions in their linked index entries. The acquired S95 inheritance-depth method and the conditional god-class, UML/OCL, statechart and service-coupling comparisons retain distinct roles. Broad metric-prediction descendants are not automatically full-reading priorities.

**Unique:** unconfirmed; guideline/document assessment and experimental source comparisons are established prior work. **Valuable:** positive understanding and location-identification outcomes under a time allowance are concrete, while implementation, QA/training cost, lifetime gain and Nu transfer remain unmeasured. **Scientifically valid:** useful paired observation and documented degradation/task procedures, with system confounding, missing times, outlier sensitivity and aggregate/edition gaps. The later survey continuation now follows the C05/S125 game-agent evaluation frontier; preserve unresolved S155 final-journal/package and S156 alternate-edition correspondence. No experimental hold changes.
