# S83 — Program structure, task complexity and maintenance performance

## Identity and actual coverage

Deborah A. Boehm-Davis, Robert W. Holt and Alan C. Schultz, *The role of program structure in software maintenance*, **International Journal of Man-Machine Studies 36(1), 21–63, January 1992**, [DOI 10.1016/0020-7373(92)90051-l](https://doi.org/10.1016/0020-7373(92)90051-l). The received/revised dates are 21 March 1989 and 8 August 1990; these are not publication dates. The article says it is based on 1987 and 1988 presentations, whose bodies and observation correspondence were not inspected. Those presentations are not independent replications here. The same-title Lindroos work previously screened remains a different work.

The existing native Zotero parent **`KGGBUN45`**, note **`7WA2IKLR`** and user-library PDF **`XEEYDY5K`** were verified before continuing beyond the prior opening-page reading. Memberships `PKLXQNEE`, `74BHFBRZ` and `MBYQJXUF` are preserved. The actual stored file matches the local copy: **43 pages, 2,347,726 bytes**, SHA-256 **`894155108e1edaede702b1e61a66dbbf81f13eaa421a02c424a1ce64bccc6b80`**, MD5 **`842de7d727f75e50adfc53026f80d1fa`**.

**Complete publication reading, 2026-10-03:** all 43 text pages, four sections, five figures, three numbered tables, 29 references, and complete Appendices A–B. Appendix A prints all three student-transaction program forms (physical pages 20–39); Appendix B supplies a sample task, dictionary and current/expected output (40–43). **Twenty-one visual pages: 1, 5, 7–12, 14–15, 21, 25, 27, 30, 34–36, 38, 41–43**, including every figure/table and selected listing details. OCR merges identifiers and punctuation; the scan is authoritative for checked details. This is a structural reading of printed code, not a byte-exact transcription, compiled baseline-equivalence check or reproduction. No author code, compiler, experimental system or participant task was executed.

SC151 requests `limit:20`, offset 0, for the exact DOI and returns one metadata record with an institutional redirect and `contentDenied:true`; no abstract, excerpts, citation contexts or editorial notice are returned. Its tally has five mentioning statements and 38 citing publications, not a graph inspected here. Full-body access comes from the user-library attachment, not Scite. No new keyword screen or unchanged historical exclusion is counted.

## What was varied

Thirty-six paid volunteers—**18 professional programmers and 18 advanced undergraduate computer-science students**, all with Pascal experience—worked on three small programs: a military address database, a host-at-sea buoy/navigation/weather problem and a student linked-list transaction system. Each problem had three prepared Pascal versions. “Functional decomposition” denotes procedural decomposition into coherent functions, not functional programming or immutable state.

The in-line form expands calls into the top-level program; this also reduces the number of variables and removes parameter interpretation. The functional form groups operations by function. The object-oriented form simulates abstraction/encapsulation using grouped modules, names prefixed by the owning object, nested routines and controlled data access. It has **no inheritance hierarchy or class system**. The authors explicitly limit their claim to these implementations rather than all definitions of object-oriented design. The Jackson method is not a fourth treatment: earlier work had produced the same final modules as functional decomposition, so only the latter form was tested here.

Table 1 gives source lines excluding comments/documentation:

| Program form | Host-at-sea | Military address | Student transactions |
| --- | ---: | ---: | ---: |
| In-line | 123 | 280 | 309 |
| Functional decomposition | 162 | 312 | 223 |
| Object-oriented abstraction | 233 | 373 | 244 |

These are compound organization treatments, with different names, declarations, interfaces, duplication and lengths. The shortest form depends on the problem. Neither source length nor the label “modular” alone identifies the cause of a maintenance difference.

The split-plot Latin-square design has problem and form as within-person factors; modification complexity and programmer category are between-person factors. **Each person works on three of nine problem/form combinations**, sees every problem and form once, and receives either three simple or three complex changes. Frequencies are balanced within each programmer category, and order is independently randomized. This is 36 people and 108 task exposures, not 108 independent programmers or nine independent application domains. Assignment to every between-person condition is not described as an independently randomized recruitment process.

Simple changes are described as affecting one location and complex changes as affecting several. Appendix B makes one concrete simple task reviewable: add the number of students to the end of each list output, with successive expected totals of **9 and 8**. It supplies the functional-decomposition overview, a variable dictionary and output examples. It does not supply the other five modification specifications or a site-by-site complexity/equivalence audit across all nine programs. The appendix shows organization and the permitted information, without recovering the complete original experimental package.

## Task, feedback and measured effort

A half-hour practice session teaches the IBM PC editor, compilation and checking cycle. Participants receive program requirements/design/change instructions, a variable dictionary, a paper source listing matching the screen, and current/expected output. Expected output is development feedback in this study; it is not a hidden final oracle. Work continues until successful completion or **1.5 hours**, with breaks between problems.

Logged editor commands supply editing sessions, transactions and elapsed study/edit time. The time endpoint includes studying the program, deciding what to change and editing; it **excludes compiling, linking, executing and checking**. It therefore measures a meaningful part of a change task, but not total elapsed work, authoring/training cost or lifetime maintenance effort. The text mentions error recording but supplies no separate error-rate/result table. Counts and treatment of capped or unsuccessful tasks are not reported, so the summaries do not establish universal completion, regression freedom or a recovered all-attempt success rate.

After all three tasks, participants report background and rate difficulty. They then reconstruct program components and relationships on cards. Scorers are blinded to condition and record chunks, links, depth, width and connectedness. These are **post-task representation measures**, not pretreatment skill, an objective location-finding task or a direct accuracy score for every represented proposition. Blinding is useful; it does not identify a mediation pathway from source organization through representation to performance.

## Positive, null and conditional results

The following are the article's rounded marginal means in minutes. They exclude the time components above and pool different task/complexity conditions.

| Group | Functional | In-line | Object-oriented | Reported form comparison |
| --- | ---: | ---: | ---: | --- |
| Professionals | 29 | 33 | 38 | `F(2,24)=2.60`, reported `p<.10`; inconclusive at .05, not equivalence |
| Students | 34 | 38 | 49 | `F(2,24)=5.79`, reported `p<.05`; form-by-problem and form-by-complexity interactions also reported |

**The favorable student result is consequential.** The paper's discussion attributes the form difference to complex modifications: Figure 4 places their means at roughly 44 minutes for functional decomposition, 49 for in-line and 73 for the object form; simple-change means cluster around 26–28 minutes. These figure readings are approximate, not recovered raw means or confidence intervals. Figure 3 shows a particularly costly object-form host-at-sea task. A single pooled “modularity speedup” would erase the task dependence.

Simple versus complex changes average **20 versus 47 minutes for professionals** and **26 versus 54 for students**. The professional form means have the same ordering as the student means, but the .05 comparison is unresolved. Separate significance in one group and not the other does not itself demonstrate a group-by-form interaction or prove professionals immune to structure. The combined unadjusted group analysis is nonsignificant; a subsequent analysis covarying the assigned simple/complex task reports **33.3 versus 40.2 minutes**, `F(1,33)=5.59`, `p<.05`. This is the reported adjusted category comparison, not a randomized effect of becoming experienced.

Professional editing cycles average **1.5 versus 2.8** for simple/complex changes, without another significant effect. Student cycle results are nonsignificant. Editor-transaction counts differ by problem and complexity; the student form-by-complexity interaction parallels Figure 4. A literal reporting inconsistency is visible on printed page 31: student complexity is given as **`F(1,17)=1.58, p<.01`**. Own standard-library arithmetic gives an upper-tail probability about **.226** for that literal F/df pair, so the claimed threshold and statistic cannot both be accepted unchanged. The intended statistic is unknown; this does not overturn the separately reported timing interaction or erase the observed transaction means. No participant-level reanalysis was possible.

Student recall contains about **4.06/4.11 chunks** for functional/object forms versus **3.22** for in-line, and **2.94/2.89 relationships** versus **2.11**. In-line recall is more densely connected. Professional recall responds chiefly to modification complexity: **4.1 versus 3.2 chunks** and **3.1 versus 2.0 relationships** for complex/simple tasks. More recalled structure is not automatically more correct understanding; the object form can produce more chunks while taking longer to modify.

Subjective ratings also retain a clear unfavorable result for this object implementation. Professionals find its units harder to recognize (**3.33**, versus **2.28** functional and **2.11** in-line). Students rate it harder to locate information and recognize units; perceived working difficulty is a .10-level trend. Table 3 relates difficulty ratings to time/cycles/transactions after partialling change difficulty. Its row correlations are small positive associations (for example, information-finding difficulty with time **r=.235**, and unit-recognition difficulty with time **r=.291**). It treats **108 program exposures** as its stated sample; a clustered/repeated-person correlation analysis is not reported. These retrospective ratings can reflect the difficulty already experienced. They do not establish a causal information-locality mechanism.

Background is also heterogeneous. Professionals average **3.61 commercial-programming years** versus **.22** for students, but the groups are not significantly different on several language/design-method exposure measures. Language breadth, programs written and operating-system breadth correlate with time; years of programming and education do not significantly correlate with performance here. This neither establishes a universal skill proxy nor makes coding agents equivalent to the student group.

## Materials and inference boundaries

The complete printed transaction programs corroborate the treatment description: the in-line version repeats list-search/insertion logic, the functional version reuses routines, and the object form separates linked-list, transaction-file and permanent-file operations with prefixed interfaces. All operate on mutable pointer/file state. Appendix B's dictionary and supplied output make this a documented, feedback-supported change exercise, not unaided comprehension of arbitrary source.

The article supplies selected materials but no participant records, timing logs, full six-change set, confidence intervals for the plotted cells or machine-readable original programs. Printed listings also contain apparent transcription inconsistencies—for example, object-list insertion prints `Insert_after(D)` on page 55 where that routine has no corresponding declared `D`. This is a publication/package correspondence limit, not a reproduced failure of the historical program. OCR is not used to manufacture additional source defects, and no broad baseline-equivalence or replication claim follows.

The authors themselves reject a general recommendation for or against the methodologies from these particular Pascal versions. Preserve their **actual positive conditional performance evidence**, professional uncertainty and adverse object-form findings. The small prepared programs, limited task set, bundled source changes, unspecified cap disposition and omitted checking time bound transfer; they do not make the experiment irrelevant.

## Consequence for Nu and continuation

S83 supplies direct prior art for evaluating source organization through actual modification tasks. Alongside [S155/S156's document-task evidence](S156-oo-structured-design-maintainability.md) and [S81's later control-style experiment](S81-control-style-experience.md), it shows why location finding, implemented changes, correctness and total effort must remain distinct outcomes. Its functional-decomposition result supports the plausibility that factoring suited to a task can help; it does not establish that maximum decomposition, minimum lines, object orientation, functional programming or Nu's source convention is uniformly best.

For B01/B10/B11/B12, Nu's locality/appropriate-factoring claim is therefore a conditional empirical proposition with substantial prior art. A source-grounded explanation must name the information/edit boundaries and actual change family; post-task preference or recall cannot stand in for a verified mechanism. Nu/F#/agent benefit, explicit enumeration versus equivalent catch-all, interactive temporal obligations and lifecycle cost remain unmeasured by S83.

[S229's completed professional expert–AI reading](S229-picoscenes-expert-ai.md) now adds favorable feature-effort, defect and hardware measurements with explicit allocation, cost and semantic-preservation boundaries. Its architecture/context/feedback bundle does not isolate a source-convention effect. The current survey advances to S103's coexisting-schema/update method; no experiment, worker or construction hold changes.
