# S91 — Design metrics, integration changes and prediction limits

**Complete publication reading, 2026-09-30.** Douglas A. Troy and Stuart H. Zweben, *Measuring the Quality of Structured Designs*, Journal of Systems and Software 2, 113–120, [DOI 10.1016/0164-1212(81)90031-5](https://doi.org/10.1016/0164-1212(81)90031-5). The issue identifies 1981; the first-page copyright and price footer say 1982. The closing page records receipt on 5 July and acceptance on 6 August 1981. Zotero parent `PVZRIGSE`, user-library PDF `ZQLTGG8W`, note `MAQS93U4`.

All eight pages, the structure-chart figure, four tables, all 21 metric definitions and ten references were read. The first page and six further renders cover every table/figure and consequential OCR ambiguities. The PDF has 992,483 bytes, SHA-256 `f83c40f3c97f7e1c67aeb3d0fc3a46563567da17289fdcdf5e43f0251215f515`. No original charts, change logs, source, regression outputs or underlying dataset were acquired. The associated March 1981 Ohio State master's thesis remains a separate, unread source; the journal reading does not confer its detailed-analysis coverage. No fitted model or author experiment was reproduced.

## Live claim and observation unit

B01/B10/B11/B12 concern whether design information available before implementation can signal later problems, and whether such associations validate a design recommendation. S82 cites this study as favorable industrial evidence for coupling. It analyzes **73 design units and their coded programs from one industrial project**, produced by seven designers. Two people account for 56 units: 31 database-subsystem designs and 25 report-generator designs. The unit is a whole program/subroutine with a structure chart, not each box in that chart, each change event, or an independent project.

Design documents were created before coding and then left unchanged. That timing makes them a potentially prospective information source. It also means implementation-time design changes are absent from the predictor documents. The authors explicitly acknowledge this mismatch; the study does not identify the causal effect of faithfully implementing the original design or intervening on coupling.

The outcome is the **number of source-code modifications after a programmer entered code into the history bank as ready for integration/system testing**. Earlier coding/unit-test changes are unrecorded. Changes cannot reliably be mapped to individual chart components and are aggregated to the design unit. The analysis calls these modifications errors, but their causes are not classified: requirements changes, design faults, coding mistakes and clerical corrections may all contribute. No modification effort, severity, complete behavioral success, production failure rate or operational maintenance cost is measured. The conclusion explicitly proposes maintainability and reliability as additional future outcomes.

This phase-specific recording can make interface-related problems particularly visible while omitting defects already found locally. It does not establish representative all-lifecycle defect prevalence. The paper reports no common observation duration, exposure normalization, developer workload adjustment, source size baseline or independent outcome adjudication.

## Metrics and analysis

Twenty-one candidate measures are grouped into overlapping constructs. Coupling includes counts of interface/control/common-data connections and top-level data-structure/simple parameters. Cohesion includes listed side effects, maximum/average fan-in and possible return values. Complexity uses chart depth, maximum/average fan-out, box count, decisions and loops. Modularity and size reuse several of those same measures. X3 is printed as the total number of interconnections per box; the paper supplies no raw chart-calculation examples to resolve its relationship with the maximum and average measures.

The authors recognize that chart depth and box count can simultaneously be read as high complexity/size and high modularity, implying opposing quality predictions. The mapping of a metric to a construct is therefore an assumption, not an independent measurement of each design principle. Varying chart detail and missing accompanying descriptions further change what can be measured.

Each of three overlapping datasets is analyzed with forward stepwise linear regression using three candidate sets: all available metrics; metrics with a simple outcome correlation significant at .05; and a set with intercorrelations below .50. Predictor screening and model fitting use the same data. The journal supplies selected-variable lists and fitted r², but no held-out predictions, cross-validation, external project validation, complete coefficients/standard errors, residual diagnostics or adjusted r². It does not specify enough of the selection procedure to reproduce the models from the article alone.

| Analysis and unit count | All available candidates: fitted r² | Outcome-correlation screen: fitted r² | Lower-intercorrelation set: fitted r² |
| --- | --- | --- | --- |
| All 73 units | .53 | .24 | .33 |
| Database designer/subsystem, 31 units | .62 | .36 | .23 |
| Report-generator designer/subsystem, 25 units | .62 | .40 | .26 |

These are nine fits to one project and overlapping subsets, not nine replications. Multiple candidates relative to the small within-subsystem samples and data-dependent selection leave optimistic fit and unstable choice plausible. The r² values are proportions of observed outcome variation fitted by those models, not proportions of defects prevented, future prediction accuracy, or maintenance savings. The summary's comparison with an earlier claim that about half of integration errors could have been detected during design compares different quantities; it does not independently validate this r² range or establish a 50–60% ceiling on prediction.

## Results, conflicting directions and printed inconsistencies

Coupling-related variables appear repeatedly; complexity/size appear more in the database subset. Some selected measures correlate in the opposite direction to the hypothesized quality ordering. The authors acknowledge mixed coupling directions in analysis 2 and unfavorable signs for the modularity hypothesis, rather than supporting a universal lower-coupling rule. Cohesion is poorly represented when documentation is missing. A selected variable's presence does not by itself establish the intended causal direction or construct.

Visual inspection confirms two reporting ambiguities that OCR alone cannot resolve:

- Analysis 1 says X8, X9 and X16 were excluded for missing values, yet Table 2's second available-variable list includes **X9**. No differing usable-row count or explanation is given.
- Analysis 2 says no cohesion measures were selected, yet Table 3's first selected set includes **X16**, explicitly classified as a cohesion measure for possible return values. The narrative and table cannot both be taken literally under the given mapping.

These do not erase the reported fitted associations, but they prevent an exact reconstruction of which construct each model supposedly validates. Coefficient signs described in prose are simple correlations, not a supplied multivariable coefficient table; do not silently substitute one for the other.

Further analyses remove coupling variables from the all-unit/report fits or complexity variables from the database fit. Their changes in r² are described qualitatively without complete values. A fourth design set, assisted by the database designer but resembling the report-generator task, is said to favor coupling over complexity. Its size, membership/overlap, full results and controls are absent. This is a useful application-versus-designer hypothesis, not an independent crossed experiment separating their effects.

The authors explicitly ask future studies to standardize design detail, complete accompanying documents, collect intended metrics prospectively, distinguish modification causes and measure other quality outcomes. These limits belong to the result, not merely generic objections added later.

## Consequences and next sources

**Unique:** using design-time architecture measures to anticipate later code problems is established prior work. Neither the timing of the information nor a regression constitutes a new ISE mechanism. **Valuable:** the industrial associations motivate inspecting interfaces, but no net recommendation benefit, Nu effect or comparison against simpler reviews is established. **Scientifically valid:** keep the design-time information boundary, separate recording-phase changes from defects and effort, retain designer/project dependence and validate predictions outside the development sample. Do not condition a causal architecture claim on realized modifications. This reading does not revive D2 execution or validate D1's proposed oracle/equivalence.

S82's parameter/global manipulation and this observational chart analysis address different interventions, outcomes and development phases. A classroom null and these industrial correlations can coexist; neither establishes that all coupling or information-hiding prescriptions help or fail. S93's now-acquired original structured-design paper and S92's Ada intervention are consequential mechanism/endpoint comparisons, not automatically validated by citation here.

The earlier institutional [Troy thesis record](http://rave.ohiolink.edu/etdc/view?acc_num=osu1750087720304527) is an acquisition lead for detailed models and missingness; it has not been read. SC22 follows Yin/Winchester's design-measure study, Lattanzi's development-methodology account and Daly/Mnichowicz's switching-system report. Their metadata and actual follow-up state are recorded in the [background ledger](../nu-background-searches-2026-09-30.md), without importing effect estimates or independent-replication credit from S91's bibliography.
