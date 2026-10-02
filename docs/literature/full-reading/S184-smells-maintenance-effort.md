# S184 — code smells, observed effort and conditional models

## Identity and actual coverage

Dag I.K. Sjøberg, Aiko Yamashita, Bente C.D. Anda, Audris Mockus and Tore Dybå, *Quantifying the Effect of Code Smells on Maintenance Effort*, IEEE TSE 39(8),2013,pp. 1144–1156,[DOI10.1109/TSE.2012.89](https://doi.org/10.1109/TSE.2012.89). Native parent/note/PDF **`B6DMTQRT`/`QMKG6JVD`/`C2BVX58N`** were checked before body continuation. Existing publisher PDF:13 pages,2,775,261 bytes,SHA-256 `ab4d7865f7e0626aab00f27324e077bb2f48c1a56d1102839c2b96876b3e1445`. A separate historical attachment-refresh note `N54SEK8S` remains preserved.

All 13 pages, nine tables including the smell-definition appendix, and 46 references read. Visual pages 1–4,6–9,11; pages 5,10,12,13 text-only. No numbered scientific figures or separate supplement occurs in this copy. Own arithmetic covers all 48 initial smell counts, eleven file/effort allocation rows and eleven change-summary rows. Original file/event/revision data, model code and acceptance-test implementations are not acquired. No author tool, regression fit, maintenance task or experiment is executed.

This closes the selected B01/B10/B11/B12 method dependency of [S183](S183-maintenance-metrics.md), not an independent empirical case. Section 1 explicitly identifies that earlier paper as an analysis of the same maintenance tasks.

## Case, assignment and observed work

Four companies originally implement the same web-system requirements, primarily in Java. The systems run in parallel for two years, routing each user consistently to one implementation by IP address. Two platform adaptations are then needed to restore operation, and users request a tailored-report feature. The three maintenance tasks are performed on the existing systems; code smells, LOC and revision behavior are not separately randomized interventions.

Three Czech and three Polish professionals are hired for approximately€50,000, selected from 65 earlier skill-study participants for reliable medium-to-high performance, motivation and availability. The work lasts three to four weeks, with one or two authors present. Each developer receives one system and then another, repeating the requirements. The paper reports constrained random assignment, but its prose repeats S183's impossible statement about each person maintaining all four systems twice. **Table 4 resolves the actual analyzed allocation:**

| System | Round 1 developers | Round 2 developers |
| --- | --- | --- |
| A |1,6|2|
| B |2|5; developer 6 assigned but unfinished and excluded|
| C |3,5|4|
| D |4|1,3|

There are 12 planned and 11 analyzed developer×system assignments. Completion-based exclusion leaves A/C/Dthree observations each and Btwo. It is not evidence of six people independently completing all four systems. Round 2 also changes the implementation, so its improvement combines requirements/domain learning with a new codebase; it is not longitudinal familiarity with the same implementation.

MimEc logs IDE events including editing, reading, navigation, search and execution. The paper describes file-attributed effort but does not provide a reproducible idle/overlap/outside-IDE attribution algorithm. Developers must commit at least daily and submit compiling revisions; SVNKit counts those revisions. An author performs acceptance testing after all tasks on a system, using functionality, performance, browser/security, validation, database and role-access scenarios. Few observed defects motivate using revision count as a **quality proxy**. Neither the complete test suite nor a file-level defect measurement is supplied. Daily 20–30 minute interviews and 60 minute completion interviews feed a separately published qualitative analysis, not a new independent case.

## Exposure, units and model

Before maintenance, InCode 2.0.7 and Borland Together identify twelve smell types. The latter finds additional types beyond InCode's Data Class/Feature Envy/God Class; four other supported smells are absent. The tools have fixed thresholds. Large Class and Long Method are not directly tested. Smell definitions in Table 9 include structural relationships as well as local size/control concerns; file-level outcomes can miss effects borne by another file or by a specific method.

The four initial Java inventories contain 63/168/29/119 files and 8,205/26,679/4,983/9,960 LOC, matching S183. The reported 298 distinct modified files are not 375 independent systems or developers. Table 4 counts 375 modified **file-assignment occurrences**,234 read-only occurrences and 213 created files,822 in total. The same original file can be worked on by more than one developer. Section 6.3 also says the analysis includes worked-on files that were only read. The exact regression row set, zero-log handling, intercept coding and treatment of repeated-file residual dependence are not specified sufficiently to reconstruct the fit; categorical developer/system/round controls do not by themselves establish independent errors.

The models use natural-log effort, smell counts, file size and revisions, with developer/system/round covariates. The paper reports approximately normal residuals, no obvious residual-pattern problem and maximum VIF2.98. These diagnostics address selected model assumptions, not causal identification or held-out prediction.

| Model | Added predictors beyond developer/system/round | Adjusted R² | Selected nominal findings |
| --- | --- | ---: | --- |
|0|None|.15|Covariates jointly matter but leave substantial variation|
|1|Twelve smell counts|.36|Feature Envy+.72,p=.00007; God Class+1.4,p=.002; several weaker adverse associations; Refused Bequest−.76,p=.015|
|2|Also file size|.42|Feature Envy+.37,p=.041; Refused Bequest−.81,p=.0057; other prior adverse smell associations weaken|
|3|Also revisions during maintenance|.58|File size+.58,p=4×10⁻⁸; revisions+2.2,p=2×10⁻²⁷; Refused Bequest−.65,p=.0089; no nominally significant positive smell coefficient|

Dropping smells from Model 3 leaves adjusted R²=.58 to reported precision. The paper reports.38 after dropping both smells and revisions. This is useful **conditional explanatory evidence**: the selected smell measures add little to the stated predictors in this dataset. It does not mean size/revisions explain all effort variation; the full model explains about 58%, and equal rounded adjusted R²is not exact identity of fitted predictions. The paper notes multiple-comparison concerns; the displayed p-values are nominal, and no corrected confirmatory Refused Bequest result is established here.

Revision count is produced during the maintenance being explained. It may reflect task difficulty, design-mediated rework, commit practice or effort itself; it is not a pretreatment measured-quality variable. Conditioning on it can remove part of a possible design mechanism or introduce other bias. Likewise, if a design change affects size, a size-adjusted coefficient answers a different question from its total effect. **The conditional null is preserved; the claim that removing smells cannot reduce effort is not identified by this model.** No randomized refactoring, causal LOC reduction or future-task prediction is performed.

## Positive observations and numerical reconstruction

Own Table 4 arithmetic reproduces all eleven assignment totals and counts,189.4 logged Java-file hours, and 15,510 new LOC. Modified/read-only time sums 114.1/10.6 hours; displayed new-file row times sum 64.7 versus the printed 64.6 total, compatible with independent one-decimal rounding. Round means 20.9 and 12.8 hours reproduce an approximately 38.8%decline, consistent with the stated approximately 40%. These are unpaired means over six/five completed assignments, not an estimated pure learning effect. Work allocation varies greatly: the two first-round A developers devote 73%and 21%of their effort to modifying existing files.

Table 6 reports positive effort–churn Spearman associations: **.59 for 375 modified-file occurrences and.66 for 213 new files**. Effort–revision correlations are.47/.53; churn–revision correlations.65/.56. These are useful validations of association in these adaptive/perfective tasks. They do not make churn interchangeable with time, independently validate revisions as quality, or establish calibrated transfer to corrective maintenance, agents or Nu.

Table 7's all-language adjusted system efforts are A 24/B 39/C 17/D 28 hours. The smaller system C again has the lowest reported effort; B the highest. This preserves the favorable system-size association in S183. The all-language totals 10,440 for C/11,303 for Dcoexist with average file sizes 180/89, so the paper warns that splitting large files can move rather than eliminate work. It does not test that refactoring intervention. Table 7 has different inventory and effort scopes from Java-only Table 3/4 and S183; the exact aggregation/version and round-adjustment formula remain unresolved. Do not silently replace S183's 18/33/13/23 hours with these 24/39/17/28 hours.

All 48 Table 3 smell counts reproduce row totals and system sums **111/161/44/97**,413 in total. The text reverses C/D's Refused Bequest incidence: the table has 0/1, while section 3.3 says 1/0. Section 5.2's stated whole-system initial 111/172 smells for C/Ddoes not reconcile with Table 3's 44/97 under the same counting interpretation; another aggregation is possible but unestablished. No invented corrected dataset or model follows.

All eleven Table 8 rows reproduce its unweighted average changes to rounding: LOC+2%, total smells−6%, Feature Envy−26%, ISP Violation+33%, Data Clump+44%, God Class−18%. Developers initiated any refactoring themselves and did not know the smell hypothesis. These observations describe concurrent maintenance, not randomized smell removal or its effort benefit.

## Remaining scope and survey consequence

The paper's analysis of copying finds no smell-density relation after considering size, and it reports that worked-on smelly files were often modified. This challenges a simple claim that developers merely avoided every smell. It does not fully settle cross-file costs or changes concentrated in nonsmelly methods. These were the first substantial post-deployment changes; cumulative decay and later maintenance are unobserved. Small web systems, six selected professionals, eleven completed assignments and detector-specific smells bound transfer. Equal requirements reduce functional variation but do not isolate one architectural mechanism.

W356–358 follow the publisher, repository and author routes plus exact/data queries. The author bibliography links the DOI, with no data link at the relevant entry. The existing native record contains one PDF and two notes, no activity/model package. The earlier NVA route and failed access history remain recorded; they are not blindly repeated. Searches also expose related qualitative/inter-smell/problem-endpoint studies and a thesis, retained as consequential method leads rather than counted as independent confirmation or substituted for the raw regression data. Original data remain unlocated within these bounded checks, not proven absent.

S184 supports skepticism about interpreting an automatic smell count as a general effort oracle, while retaining positive size/churn associations and concrete professional work. It does not prove design principles irrelevant, validate minimal source as a universal goal, or reverse the project's negative F# compactness observations. Next read acquired **S75**, the 36-page game-specific smell study, to compare its mechanisms and practitioner evidence with this general maintenance model. S185, related qualitative methods and runtime/persistence/oracle frontiers stay open. No experiment or new worker is authorized.
