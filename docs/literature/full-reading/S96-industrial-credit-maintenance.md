# S96 — industrial maintenance effort and the cost of an OO rewrite

**Complete journal reading, 2026-10-01 HKT.** Joa Sang Lim, Seung Ryul Jeong and Stephen R. Schach, *An empirical investigation of the impact of the object-oriented paradigm on the maintainability of real-world mission-critical software*, Journal of Systems and Software 77 (2005), 131–138, [DOI 10.1016/j.jss.2004.11.004](https://doi.org/10.1016/j.jss.2004.11.004), online 18 December 2004. This B01/B06/B10/B11/B12 case supplies professional operational maintenance evidence, with positive effort results, unequal development support and adverse runtime costs.

## Identity and coverage

Existing Zotero parent `67NPS9NV`, user-library attachment `69M7WB4Q`, note `N678B4S5`. Identity, parent relationship and stored hash were reverified through the native API before continuing. The eight-page journal PDF has 171,848 bytes and SHA-256 `9c3f9196d26895ad870151c0848b812edcc5c23c6b413ad6ae24f2f3558c12db`. All eight pages, four tables and 24 references were read; all eight page images were inspected. There are no numbered figures or attached study-data supplements in this file. No author program, operational data, benchmark or test suite was executed. The arithmetic below checks the printed aggregates, not the original observations.

## What was compared

One Korean credit-card company operated a legacy non-object-oriented (NOO) C/TAL system and an OO C++ rewrite that the authors describe as functionally equivalent. The company processed about 2.5 million transactions daily in the reported 2003 setting. Both systems received **one credit-limit-integration change**: replacing separate purchase and cash-advance limits with one overall limit.

There were two teams of six professionals. The NOO team comprised experienced legacy maintainers; the OO team had participated throughout the rewrite. Their comparable domain expertise is an author judgment, not an independently measured balance. No random team-to-version assignment, participant-level outcomes, variance estimates or inferential comparison is reported. Twelve professionals are therefore not twelve independent language assignments. The natural maintenance processes were deliberately retained, bundling source organization, language, documentation, development method, tools, team history and role division.

The abstract describes random selection from 488 change requests. Section 4.3 narrows this to random selection **within level 4**, of which Table 2 contains 19 in 2003. The eight numeric level entries sum to 488 for 2003 and 1,376 for 2002; level 9 is printed as a dash. The experiment is not a uniform sample of the whole request pool. A relatively substantial integration change may expose cross-component work differently from the many small requests. Generalization across tasks is explicitly left to further research.

Participants recorded time and artifact changes at their manager's request. Interviews, stakeholder meetings, walkthroughs and inspections checked apparent anomalies. They were not told the work was an experiment. This reduces one possible expectancy cue but does not by itself establish the authors' stronger claim of no Hawthorne effect: participants knew they were recording their activities. The paper supplies no independent blinded outcome scoring or released behavioral oracle.

## Effort and change volume

Tables 3–4 report technical effort in person-minutes:

| Phase | NOO | OO |
| --- | --- | --- |
| Requirements | 240 | 260 |
| Analysis and design | 1,020 | 310 |
| Implementation | 660 | 215 |
| Test | 1,103 | 182 |
| Deployment | 30 | 17 |
| Sum, calculated from the tables | **3,053** | **984** |

The OO total is approximately **67.8% lower**, a descriptive difference of 2,069 person-minutes, or 34.5 person-hours, for this one change. That substantial observed advantage should be retained. Requirements effort nevertheless increases from 240 to 260, qualifying the abstract/conclusion's all-phase wording. Managerial effort was not measured; the earlier rewrite and production of its documentation/frameworks are outside this change's cost. It is also unclear whether all later performance-test defect repairs and tuning are included. These aggregates do not establish a future maintenance payback or a net lifecycle cost advantage.

Source and artifact counts move differently from effort:

| Change measure | NOO | OO |
| --- | --- | --- |
| Executable lines changed | 182 = 51 purchase + 131 cash | 277 = 268 purchase + 9 cash |
| Source files changed | 5 | 11 |
| Test cases | 15 | 39 |
| Files tested | 1 | 4 |
| Files compiled / deployed | 2 / 2 | 6 / 6 |

The OO purchase logic was reused for cash advances, reducing that second component's edits while increasing the total lines changed. Fewer changed lines or files therefore cannot substitute for the effort endpoint. The OO team also updated four requirements pages and seven analysis/design pages, versus no requirements pages and two design pages in NOO. Document-page counts are not commensurate units of knowledge or work across representations.

## Plausible mechanisms and what they do not isolate

The OO team could consult class/use-case/activity diagrams and **operation specifications containing business logic**, pre/postconditions, signatures and pseudocode. The NOO team relied more on source inspection and verbal communication with analysts. The paper explicitly reports that repetitive sequence diagrams were of little value and that UML alone could not express all business details. It does not isolate a UML effect, an encapsulation effect or a programming-language effect.

The authors attribute easier impact analysis to the available specifications and more local variables/interfaces, and attribute some NOO rework to ambiguous communication and shared globals. These are plausible process explanations grounded in their observations; reduced mental load was not measured directly. Black-box reuse and ready testing support coexist with the OO team's reported burden of additional files and dissatisfaction with restricted roles. Those qualitative costs have no separate quantitative estimate.

The OO team produced 283 lines of CppUnit scripts. Although Table 4 labels NOO test scripts “not done,” section 6 describes a NOO simulator that fed database-stored cases and logged results. This is a comparison of testing arrangements, not simply automated versus manual testing. Likewise, the 15 and 39 CLI cases are not comparable measures of correctness or fault sensitivity merely because one count is larger.

## Behavioral assurance, runtime and adoption

Section 7 describes matching approved/rejected transaction counts, starting with 100 tests based on historical operational data and scaling stepwise to one million. Many defects were found and fixed, but the paper gives no per-arm counts, defect taxonomy, timings or released cases. Matching aggregate acceptance counts does not establish complete state/trace equivalence. The million executions are not a million independent maintenance assignments and are distinct from Table 4's CLI test-case counts.

Performance of the **whole architecture including CLI** remained worse for OO. No quantitative latency/throughput ratio or distribution is reported. The company purchased about a million dollars of additional resources, including two CPUs, disk storage and a middleware license. Preserve this reported resource cost and the fact of continued adoption. The authors interpret the purchase as a decision to save on future maintenance; the paper does not measure the future savings or calculate a return on that investment. A favorable maintenance observation and adverse runtime cost can both be true.

## Consequences and follow-up

Compared with S97/S98's laboratory settings, this case strengthens professional-practice relevance while weakening isolation of individual mechanisms. It supports a **bundled process/source/tool benefit for one operational change**, with a concrete runtime tradeoff. It does not establish OO superiority across tasks or an F#/C#, Nu, immutable-state, live-reload or coding-agent effect. Common tool/document opportunity and separate behavioral, editing-effort and runtime endpoints remain necessary when a later authorized ISE experiment claims a narrower treatment.

S84's task-dependent inheritance evidence is already read. S95's acquired inheritance-depth method and S94's acquired changeability study remain consequential contrary/lineage follow-ups. The previously screened Briand/Bunse design-document and quality-guideline studies remain relevant to the documentation-versus-organization explanation; appearing again in this bibliography does not add an independent finding. Hadar/Hazzan and Purchase address diagram comprehension, while Kim et al.'s copy/paste field study could qualify a universal reuse claim; these are conditional leads, not new full readings. No need arises to reread every foundation reference.

The [background ledger](../nu-background-searches-2026-09-30.md) records G23/SC87/W182–W184's incoming-citation and primary-abstract screen. Later metric/prediction citations are not replications of this two-team case. MIDST supplies a potentially relevant interactive-tool comparison; database surveys, class-diagram associations and recent prediction frameworks require their own outcome/validation reconstruction before use as benefit evidence. The 2016 review's unchanged earlier screening is reused rather than recounted as new work.

**Unique:** unconfirmed; professional organization/tool comparisons predate ISE. **Valuable:** a large observed effort advantage and an adverse runtime/resource tradeoff, without demonstrated net lifecycle benefit or Nu transfer. **Scientifically valid:** complete reconstruction of a natural two-team, one-change comparison; treatment bundling, task selection, behavioral verification and missing individual/cost data limit causal and external claims. Continue the acquired S94 method/replication dependency; no experimental hold changes.
