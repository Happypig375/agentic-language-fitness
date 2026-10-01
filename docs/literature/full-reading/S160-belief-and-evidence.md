# S160 — practitioner belief and project evidence have different scopes

## Identity, coverage and live question

Prem Devanbu, Thomas Zimmermann and Christian Bird, *Belief & Evidence in Empirical Software Engineering*, ICSE 2016, pp. 108–119, [DOI 10.1145/2884781.2884812](https://doi.org/10.1145/2884781.2884812). The [Microsoft author PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/06/devanbu-icse-2016-2.pdf) contains twelve pages, 351,293 bytes, SHA-256 `e15ee24b70ac80fbfa3777a0d82ae885bc48760e3aa6e4ace8548fa102f9b3bf`. Native Zotero parent `KP5JXSAK`, attachment `RRQM584F`, note `BLRXQMG2`; stored identity/hash reverified on 2026-10-01.

All twelve pages, one figure, two numbered tables, three model displays, both mathematical expressions, six numbered footnotes, the author note and 59 references read. Every page extracted/rendered; visual pages 4/7/8/9 cover the figure, tables and models. Column interleaving was resolved visually. This is the author edition; exact publisher-file correspondence remains unverified. No underlying survey/repository data, original analysis or experiment was reproduced.

B10/B12 question: what can developers' reported conviction, project-specific experience and a repository comparison establish about a practice's value? This constrains how Nu practitioner claims, source conventions and measured benefits are connected. It does not make expert reports worthless or make this study's chosen measure a universal definition of benefit.

## Survey population and observations

About 2,500 Microsoft developers, testers, program managers and supervisors were invited; **564 responded**, approximately 22% by the paper's rounding. The sample spans projects and locations but remains a self-selected sample within one organization. The 386 US, 48 India, 39 China, 66 Europe and 25 other-location counts sum to 564. Respondents include 497 men, 53 women, seven other-gender and seven unspecified responses; mean age is 32.5 years, SD eight. Degrees are 267 bachelors, 211 masters and 29 doctorates, with 57 unspecified. These are sample descriptions, not profession-wide prevalence estimates.

Researchers selected sixteen five-point agreement statements for practical consequence, informed developer opinion and potential comparison with evidence. An opportunistic merge-related claim was included. This is neither an exhaustive belief inventory nor a random sample of all software practices. Participation did not require identifying answers; later interview/raffle contact information was separate. This paper does not report those interviews.

Table 1 orders statements by disagreement/dispersion. Reviews receive mean agreement 4.48, coding standards 4.18, complexity 4.00, unit tests 3.85 and static typing 3.75. Language choice is 3.17 and geographical distribution 2.86. Those ordinal summaries establish reported agreement on the questions as phrased, not the effects of those practices. The table calls its dispersion column **Variance**, while the surrounding method first refers to standard deviation; coding-standard dispersion is .79 in the table and .78 in prose. This reconstruction preserves the discrepancy rather than choosing an unreported correction.

Open-ended rationales illustrate why people value practices: readable conventions, review effort, communication across locations, documentary assertions and defect detection can be different outcomes. The paper provides illustrative quotations rather than an auditable exhaustive coding/reliability analysis. Its summaries of prior research on reviews, typing, assertions and static analysis are contextual secondary accounts. They are not new comparative results, and a claim about scarce evidence in 2016 is not a verified description of today's literature.

For each respondent's **two strongest opinions**, participants identified and ranked influences; ties among more than two equally strong opinions were randomly resolved. Thus Figure 1 is conditional on selected strong opinions and selected influences. Personal experience is selected 1,033 times, peer opinion 674, mentors/managers 499, research papers 257 and other influences 148. These are influence selections across up to 1,128 opinion prompts, **not counts of different people**. The text does not print an exact selection count for trade journals or all per-item missingness. Selected ranks are inverted for display; it is not an unconditional ranking in which every person ranks all six sources.

Personal experience ranks highest and research papers near the bottom under this elicitation. This supports the descriptive importance of experience in reported belief formation. It does not identify the causal origins of opinions, actual research-reading behavior, expertise calibration, or what a dissemination intervention would change.

## Purposively selected two-project comparison

After inspecting disagreement on controversial survey statements, the authors select geographical distribution and two large projects with contrasting answers. **Pr-A** is an operating-system project with approximately 400,000 files and 150 million source lines; **Pr-B** is a web service with approximately 430,000 files and 85 million lines. Both involve roughly 8,000 developers, over 100 buildings, dozens of cities and around twelve countries. Selection is purposive and informed by the observed contrast, not a random sample of projects.

Pr-A respondents tend to reject the claim that distributed development preserves quality; Pr-B respondents tend to accept it. A Pearson chi-squared comparison reports p < .001. The paper does not supply project-specific respondent counts, a full contingency table or a belief-difference effect size. The two projects' very large file populations do not enlarge the number of independently sampled organizations or project cases.

Repository data cover millions of changes beginning in 2012. An exact end window, full retained file count and extraction release are absent. The response **nfix** counts repair commits associated with each file using project-specific log conventions: a BUG prefix in one project and several conventions in the other, identified through authors' prior work and informants. It is not a complete census of independently verified customer defects, their severity, repair cost, coordination burden or delivery time. No released precision/recall audit is reconstructed here.

Four controls are average file size, total commits, number of distinct committers and the largest committer's share. These are measurements within the observed history, rather than experimentally assigned, pre-treatment covariates. In particular, total commits include repair activity, while developer count and ownership can reflect several causal roles. Prior usage of these controls does not establish that all confounding is removed or that the resulting coefficient represents the total effect of geographical distribution.

Localization indicators mark a file whose commits are mostly concentrated in one building, city, region or nation. The method says **more than 75%**; nearby prose/caption also uses “75% or more,” leaving the equality boundary unclear. Sensitivity checks from 65% to 85% are reported as similar, without full results.

| Project | One building | One city | One region | One nation |
| --- | ---: | ---: | ---: | ---: |
| Pr-A | 56% | 90% | 91% | 92% |
| Pr-B | 76% | 80% | 83% | 85% |

These are Table 2's proportions of concentrated files. The page-eight prose swaps Pr-B's building/city labels; the table governs this reconstruction, with the conflict retained.

## Conditional results and their limits

The baseline regressions contain the four controls. Eight augmented models add **one** geographical indicator at a time—four models per project. They do not estimate four geographical coefficients jointly. Baseline R² is .65 for Pr-A and .34 for Pr-B; F statistics are 2.5 × 10⁵ and 6.4 × 10⁴. Printed t-values indicate increasing repairs with file size, commits and number of developers, and decreasing repairs with concentrated ownership. Coefficients, standard errors, exact retained denominators and practical-unit predictions are not printed.

The authors report acceptable residual, variance-inflation and heteroskedasticity diagnostics and similar quasi-Poisson results. High-leverage outliers were removed, but the exclusion rule/count is unavailable. The alternative count model and threshold checks are sensitivity reports, not independent replications. Files share developers, commits and project context; a very large row count does not establish independent observations.

For each geographical addition the reported proportionate R² change is below .005. The displayed Cohen f² is the increment in explained variance divided by the full model's residual variance:

| Project | Building f² (t) | City f² (t) | Region f² (t) | Nation f² (t) |
| --- | --- | --- | --- | --- |
| Pr-A | .0015 (−20.9) | < .001 (11.3) | .0030 (15.2) | < .001 (7.9) |
| Pr-B | .0035 (−30.0) | < .001 (−2.17, p = .03) | .0017 (21.9) | .001 (16.9) |

All other displayed tests report p < .001. Every f² is below the cited .02 convention for a small effect. Concentration in one building has a negative repair association in both projects; the city coefficient is negative in Pr-B, while the other coefficients are positive. This is useful evidence of small **additional modeled variance** and mixed conditional directions in these histories. It is not a formal equivalence result, proof of zero effect, a bound on absolute economic consequences, or evidence that remote development cannot affect other outcomes.

The authors characterize Pr-B's beliefs as consistent with their evidence and Pr-A's as inconsistent. That interpretation depends on the specific repair-count outcome, localization quantization and covariate adjustment. Their own validity discussion excludes maintainability, readability and subtle personal relationships. Developers' coordination concerns can therefore be materially relevant without being captured by these models.

Confirmation bias is offered as a possible explanation, not measured as an individual mechanism. The study does not match each person's exposure to a causal outcome, track belief updates or manipulate dissemination. Its statistical-background discussion supplies a prior/error-rate illustration; the empirical study does not perform Bayesian updating. A test's nominal false-positive rate must not be replaced with an observed p-value when interpreting that background formula.

## Consequence for Nu and D1

Practitioner testimony can identify mechanisms, local constraints and important outcomes. Comparative repository evidence can challenge a specific factual prediction under its measured scope. Neither should silently replace the other. Nu's public claims remain claims with distinct source authority; this study neither validates them nor establishes that their authors are biased.

For D1, strong agreement with coding standards does not prove the benefit of explicit enumeration. Conversely, weak published evidence or small conditional repair associations elsewhere do not prove a convention has no value. New and retained behavior, task conditions, diagnostic opportunities, effort and failure outcomes must remain explicit. An eventual study can retain useful practitioner-motivated hypotheses while measuring outcomes independently; no experiment is authorized here.

| Criterion | Disposition |
| --- | --- |
| Unique | Belief/evidence comparison and project-specific corroboration are established research questions. No priority claim for ISE follows. |
| Valuable | The study documents experienced practitioners' reported influences and a consequential mismatch under one outcome model. Nu-specific prevalence, net benefit and transfer remain unmeasured. |
| Scientifically valid | Self-selection, selected strong opinions, post-survey case choice, repair proxies, dependent files and conditional controls constrain stronger claims. Small incremental variance is not universal practical equivalence. |

## Follow-up and remaining coverage

SC111/SC112, G31 and W243–W248 are recorded in the [practice follow-up screen](../nu-background-belief-practice-screen-2026-10-01.md) and [search ledger](../nu-background-searches-2026-09-30.md). Two explicit original-title/artifact searches and the primary Microsoft entry did not locate an original data/code release. The entry links the paper and BibTeX; this bounded failure does not prove no release exists.

The 2018 IEEE Software account, DOI `10.1109/MS.2018.4321246`, describes the same 564-response Microsoft survey in the returned author passage and directs readers to the full paper. It is a related account, not independent corroboration; its complete body is unread. The earlier Rainer/Hall/Baddoo 2003 content-analysis route distinguishes local opinion and empirical evidence, with only selected returned passages/primary abstract screened here.

Three distinct method dependencies now have native records and verified PDFs: **S180**, five productivity/quality/experience beliefs in 1995–2006 developer data; **S181**, displayed comprehension metrics and separate subjective/performance outcomes; **S182**, defect-prediction beliefs across repository histories. Their abstract/opening coverage does not validate their methods or reported effects. The similarly named 2019 reply and 2020 “disconnect” report retain unresolved lineage rather than being counted as independent replications.

Read the already acquired S161 metric/judgment comparison next, then prioritize these direct methods and S162's hot-fixing practice against the remaining type/runtime/oracle frontier. Title screening of incoming citations is not a full abstract or field screen. No B theme closes and no experimental hold changes.
