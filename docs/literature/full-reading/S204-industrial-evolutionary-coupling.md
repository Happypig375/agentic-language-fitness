# S204 — Evolutionary coupling and industrial defects

**Full publication reading, 2026-10-02 HKT.** Serkan Kirbas, Bora Caglayan, Tracy Hall, Steve Counsell, David Bowes, Alper Sen and Ayse Bener, *The relationship between evolutionary coupling and defects in large industrial software*, Journal of Software: Evolution and Process 29(4), e1842, 2017; online 7 February 2017. DOI [10.1002/smr.1842](https://doi.org/10.1002/smr.1842). Two industrial histories provide positive, heterogeneous associations between files that change together and reported defects. This supports investigating co-change information alongside other context. It does not measure the benefit of reducing coupling, nor validate a universal defect predictor.

Existing native Zotero parent **`TGXYAWQD`**, note **`GNASZJD7`** and PDF **`R64439QR`** preceded reading. The final publisher-layout PDF is **19 pages, 1,201,418 bytes**, SHA-256 `7cee3dceebe030531f095856736fd9b707b9796bdcdf90fd0470989e7833e852`, acquired from the [Brunel archive](https://bura.brunel.ac.uk/bitstream/2438/14865/1/FullText.pdf). Prereading versions were 4814/4840/4812. All nineteen pages were read as text, including Appendix A, limitations, acknowledgments and all 49 numbered references. Fourteen pages were visually inspected: **1, 4–12, 16–19**, covering all ten figures, fifteen tables, six mathematical expressions and marked footnotes. Pages 2–3 and 13–15 have text-only coverage. References 6 and 11 repeat one work; reference count is not independent-study count.

## Population, history and observation units

| Context | Financial system | Telecommunications system |
| --- | --- | --- |
| Language/process bundle | COBOL, PL/I and JCL; modified waterfall; legacy over 25 years | Java web applications; agile/TDD; MVC described |
| History window | 2009–2013 | 2006–2013 |
| Subsystems / modules | 20 / 274 | 4 / 11 |
| Developers | 460 | 25 |
| Source size | 87 million LOC; 150,000 files | 310,000 LOC; 26,000 files |
| File versions / commits | 192,000 / 50,000 | 180,000 / 24,000 |
| Reported fraction of files changed | 11% | 15% |

The five extracted data sources are two version-control repositories, two defect repositories and the financial company's configuration-management database. They are not five independent projects. A module is a team-owned functional grouping of files within one subsystem. File-level metrics are correlated separately within modules; later box plots compare module characteristics. These units should not be interchanged.

The financial system extends the authors' earlier banking studies, cited as the 2014 ESEM and Turkish-conference accounts. The present paper adds telecommunications data and analyses, rather than an entirely independent replication of the banking observations. The previously discovered journal-first presentation is also not another dataset. The languages, processes, architectures, scale and history differ together across the two companies; their comparison does not isolate agile development, TDD or MVC.

## What co-change and defect measures actually count

The financial repository usually records one file per commit, making same-commit grouping inadequate. The authors group changes by modification request (MR), including fixes and enhancements; one request can span several transactions. For a file, **NoECF** counts distinct other files changed for at least one common request. **NoECFMR** sums the number of partners over requests, so repeated pairing contributes repeatedly. A pair that changes together in five requests contributes one to NoECF and five to NoECFMR.

Coupling is counted only inside the file's module. Cross-module relations are excluded, even though some manual examples later involve them. Transactions changing more than thirty files are excluded from coupling calculation, and files above 10,000 LOC are removed as size outliers, reportedly 0.4% of files. The transaction filter and request-level aggregation are distinct choices. No temporal decay removes obsolete relations after refactoring, and no independently validated semantic-dependency oracle is supplied.

Defect attribution assumes that files changed by a fix contain the defect. Financial links come through the configuration-management database; completeness depends on its recorded change categories. Telecommunications links combine issue IDs in SVN comments and revision references in JIRA. Between 73% and 79% of fixed bugs are linked each year; some omitted fixes require database changes rather than a source commit. A missing link is not a verified defect-free file, and changes needed to repair a bug need not all be its origin.

The outcomes are defect count **NoD**, defect density **NoD/LOC**, and a binary indicator of at least one defect for the logistic models. The history windows supply both coupling and defects; no separate exposure cutoff, lagged target window or held-out prediction protocol is reconstructed. Fix requests can contribute to both the coupling history and the defect outcome. This shared construction and developer activity provide reasons not to interpret the associations as the effect of a preceding design treatment. The authors explicitly describe explanatory association models rather than validated prediction models.

## Positive associations and the selected distributions

Spearman correlations are significant at .05 in **161/274 financial modules** and **6/11 telecommunications modules** for coupling against defect count. The financial distribution is generally low to moderate, with 21 modules described as highly correlated. Defect-density analysis yields **147/274** significant financial modules and a similar distribution. These are useful scoped positive results, including heterogeneity within one industrial system.

The histograms show the significant subsets, not all modules. For example, Figure 2 uses 161 financial modules and Figure 4 uses 147. Thirty-two of the 113 financial modules without significant count correlations have at most ten commits. Thus a nonsignificant result can coexist with little opportunity to observe coupling; it is not proof of no relationship. Equally, selecting modules by significance does not provide an unbiased distribution of effect strengths.

Modules with detected correlations generally have more files, revisions, coupling links and developer activity. The authors compare these groups using box plots and report significance for their differences. Statistical power, measurement opportunity and actual heterogeneity can all contribute to that grouping. It does not identify a causal mechanism by which small modules prevent co-change defects. Indeed, Appendix A5 reports a **negative** size–correlation-strength association, rho **−.218**, p **.005**. Presence of statistical significance and magnitude of the association are different questions.

Manual examples illustrate missed coordinated edits and changes with unintended consequences in related files, including relations not evident from structural or dynamic coupling. This gives the metric a concrete engineering interpretation: inspect related change obligations that a local view can miss. Selection criteria, case counts and a controlled repair comparison are not supplied, so those examples are explanatory illustrations rather than measured recommendation accuracy or maintenance savings.

## Regression controls and the meaning of the reported eight percent

The initial logistic model includes NoECFMR, NoECF, commit count and developer count. NoECFMR and NoECF have variance-inflation factors around 21; the former is removed. Subsequent models add interactions, remove correlated terms and apply stepwise significance reduction. VIF thresholds differ: 2.5 for the simple model and 10 for the interaction model. This is an in-sample model-selection procedure, without reported out-of-sample calibration or discrimination.

LOC is used for outlier filtering, density and separate size analysis, but is not a term in the printed logistic models. The methods mention prior defect count; Tables 3–11 do not show that predictor or establish its time cutoff. Therefore a fully reconstructed prior-defect/size-adjusted prospective effect cannot be claimed. The exact company composition and observation count for the displayed fitted models are not clearly specified in the inspected reporting.

Table 10's final fitted log-odds are:

`−2.9878 + .0747 × NoECF + .0324 × NoCommits + .9823 × NoDevs − .0184 × NoECF × NoDevs`.

Table 11 reports odds ratios of 1.08, 1.03, 2.67 and .98 for those terms. The introduction describes an additional coupling as making a **module** eight percent more likely to be defective. Three qualifications are necessary: the modeled outcome is at **file** level; an odds ratio is not a fixed change in probability; and the interaction changes the coupling slope.

**Our algebraic reconstruction:** at fixed developer count `d` and commit count, one more coupling has conditional odds ratio `exp(.0747 − .0184d)`. This is approximately 1.058 at one developer, 1.001 at four, and .983 at five. The coefficient changes sign near 4.06 developers. These illustrative values follow from the printed fit, not recovered observations or an intervention; support across the actual file-level developer distribution remains unspecified. They prevent treating 1.08 as a universal marginal benefit from removing a coupling. This check executes no author model or experimental system.

Appendix A3 reports near-identical ranks for the two coupling measures (.99), positive coupling–defect correlations (.28), and strong dependence among activity metrics. Rank correlation and linear-model VIF measure different relationships; their differing magnitudes are not by themselves contradictory. The unavailable rows/model specification prevent independent refitting or robustness assessment.

## Defect types qualify the aggregate result

Only the telecommunications company supplies the 22 root-cause labels described in Appendix A1. A defect can have more than one label, so types are not mutually exclusive. Table 12 selects types with significant results; all listed p-values are printed as .000, which should be understood as rounding, not literal zero.

| Defect category | NoECFMR versus NoD | NoECF versus NoD |
| --- | --- | --- |
| Code implementation | .176 | .182 |
| Acceptance criteria | .111 | .113 |
| Functionality not implemented | .088 | .091 |
| Analysis | .083 | .085 |
| Not an issue | .052 | .045 |
| Test implementation | .060 | .061 |
| Third-party system | .047 | .045 |
| Bad data | .091 | .093 |

Code implementation is the largest of these associations. The prose calls it moderate, although the paper's own thresholds classify .1–.3 as low and values below .1 as trivial. Preserve the numerical result rather than upgrading its strength. The authors omit ten other types for trivial correlations and report four nonsignificant types: incorrect environment, CRM bug, user error and database disconnect/reconnect error. These null/trivial outcomes constrain a blanket defect-risk claim.

Code implementation and “not an issue” constitute approximately 28% and 20% of labels, respectively. Practitioners reportedly use the latter for deployment problems, whereas Appendix A1 gives it a broader nondefect interpretation. Label prevalence, attribution and overlapping categories affect interpretation. They do not identify a causal path from coupling to each defect type.

## Supplement, lineage and access boundaries

The final PDF contains Appendix A, including all root-cause descriptions, selected defect/no-defect box plots, the main-metric correlation table and size analysis. Appendix A2 intentionally removes numeric y-axis values to protect company data; visual inspection cannot recover those distributions. No raw repository/issue data, mapping table, model frame or executable analysis has been acquired or run.

**W340** inspects the [Brunel item record](https://bura.brunel.ac.uk/handle/2438/14865), its linked full-record view and the publisher landing page. Brunel lists only `FullText.pdf`; native HTTP retrieves the full record after a web cache miss and confirms that file link. The publisher page is unavailable through the web tool and returns HTTP403 through ordinary native HTTP. The paper mentions supporting information online, but no additional payload is identified through these routes. That remains an external-supplement access uncertainty, not proof that the embedded appendix exhausts every released item. There is no bypass or access purchase.

Earlier discovery screens and the final PDF are one work lineage. The positive S200 concern/defect study is cited as a predecessor but uses different concern definitions and data; it is not a replication of these industrial histories. The earlier banking reports overlap the financial data. Opposing prediction findings cited in this paper remain separate conditional primary-method dependencies; their reporting here does not substitute for reading them.

## Survey consequence and next action

For **B01/B10/B11/B12**, co-change histories can expose relationships absent from a local structural view and supply additional context for defect investigation. The paper contributes industrial evidence with within-system variation and root-cause distinctions. It supports neither a universal source-compactness/coupling target nor a Nu-specific maintenance benefit. Reducing coupling, improving task guidance, predicting future faults and reducing repair effort are separate proposed outcomes.

This closes the selected publication's temporal/control/unit reading gap while retaining raw-data and external-supplement uncertainty. The fit's interaction, selected histograms and defect-label results belong in the synthesis alongside the positive associations. None establishes that coupling reduction is ineffective; the causal intervention remains unmeasured.

**Next consequential action:** return to the less developed **B03 coordination frontier** and read already acquired **S142 JEScala**. Its object-level event/join rules and explicit comparators can distinguish subscription identity, event selection, handler order and runtime burden from Nu's coordination claims. Preserve the independent type, persistence/runtime and temporal-oracle paths. This is a change of consequential mechanism, not a numerical stopping point or experimental authorization.
