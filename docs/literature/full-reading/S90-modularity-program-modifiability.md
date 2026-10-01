# S90 — modularity and the kind of maintenance change

Read 2026-10-01 by the main Codex session. Timothy D. Korson and Vijay K. Vaishnavi, *An Empirical Study of the Effects of Modularity on Program Modifiability*, chapter 12 in *Empirical Studies of Programmers: First Workshop*, Ablex, 1986, printed **168–186**. [ACM catalogue locator](https://dl.acm.org/doi/10.5555/21842.28893); the current web open failed and exact Scite title/identifier lookups returned no record. The held chapter and [author bibliography](https://www.andrews.edu/~bidwell/sda-cs/sda-cs.html) establish the work. The same-title dissertation is a separate, unread edition, not an additional independent experiment. No DOI registration is newly asserted.

Existing native parent **`8D4ULNQW`**, PDF **`A2UC9VJX`**, canonical note **`HH36U2WA`**; title, parent/attachment relation and stored hash reverified before continued reading. File **20 pages, 2,456,929 bytes**, SHA-256 **`d03931d9361b88704416ab23b40dff4214e3e5a379984a0fa78c8559c3485c95`**. Complete chapter text coverage: physical **2–20**, nineteen pages. The administrative delivery cover is outside the publication reading. Visual coverage: physical **2, 6, 9, 12–17**, covering opening, all seven figures, all four participant tables and the later-session adjustment. All 23 references and the opening footnote included; no appendix in the chapter. Delivery identifiers and copyrighted bodies remain outside Git.

Own arithmetic below checks the printed totals and group assignments. It does not run the authors' programs or repeat their experiment. [S193](S193-replication-modularity-account.md) is the later primary-author account of an external replication of the first task; its separate limitations matter to the synthesis.

## Decision, treatment and scope — printed pp. 168–174

The decision is how an existing program's decomposition affects the effort of a particular change. The proposed routes are **localizing a change behind a boundary**, **reusing existing domain operations**, and **understanding/changing distributed existing behavior**. The fourth task deliberately lacks those expected advantages. These are predecessors for task-dependent modularity benefits, not a test of Nu, functional programming, case enumeration or model context.

The scope is nonrecursive Pascal business applications: inventory, scheduling, calendar and purchasing. All programs have at least 450 source lines; the conclusion gives an average of 995 lines. The authors classify their work as adaptive maintenance—enhancing, adding or changing features—not original design cost, defect repair alone or runtime optimization. S193 later calls the first task perfective maintenance; the concrete inventory-access change is the reliable comparison unit across those labels.

The modular version is a loosely coupled hierarchy with high cohesion, using S93's structured-design categories: no pair worse than stamp coupling except common coupling within an information cluster; at least 90% of modules in the top three cohesion categories. The monolithic version inlines every procedure/function body at its call sites. This removes reusable boundaries and can duplicate or relocate code. Functional equivalence is an author premise, not independently executed here.

Page 171 says control structures, names, comments, indentation and **program length** are held constant. The later replication authors describe approximately **1,000 versus 1,400 lines** for the first task (S193 p. 372). Exact source files/line-count definitions are not recovered here, so that discrepancy remains unresolved. Do not treat inlining as an isolated scalar coupling or length treatment. The psychological chunking argument is a proposed explanation; neither mental chunks nor retained agent context are measured.

## Participants, assignment and endpoint — pp. 174–178

Sixteen selected Pascal/IBM-PC users participate: **seven professionals and nine advanced students** at Southern College of Seventh-Day Adventists. Professional means at least one year's equivalent full-time experience. Two professionals are systems programmers, four application programmers and one a data-processing head. Selection establishes familiarity in this setting, not a representative developer population.

All receive one identical short pretest for orientation, followed by the four tasks in a fixed order. Each task assigns eight participants to each source version. Task 1 is randomized; each later task splits the preceding assignment-history groups equally at random. The printed memberships reproduce **all sixteen possible four-task condition histories once**. This balances prior treatment histories; it neither counterbalances program/task order nor has each person modify both versions of the same program. Four tasks reuse the same sixteen people and are not four independent sampled populations.

An observer records four phases: plan/code edits on paper; type them into the computer; remove syntax errors; debug logic until a supplied standard test passes. The reported outcome sums **paper coding + syntax correction + logic debugging**, excluding typing. It is therefore not total elapsed maintenance labor. Supplied-test success is the feedback/stopping endpoint; no independent hidden final oracle or complete behavioral guarantee is established. Phase durations describe where time was spent and are not independent randomized mechanism effects.

The chapter offers instructions, specifications, documentation and both source versions on request. Those materials and the dissertation have not been acquired in this segment; no author contact occurred.

## Four tasks and observed results — pp. 177–183

| Task | Concrete change / proposed benefit | Mean minutes, modular / monolithic | Own reduction from printed participant totals | Reported comparison |
| --- | --- | ---: | ---: | --- |
| 1, inventory register | Access the inventory file directly instead of through an intermediate array; three boundary modules versus scattered access code | 19.3 / 85.9 | 77.6% | p < .001 |
| 2, workstation schedule | Add removal from a waiting list; reuse existing primitive operations | 44.1 / 259.8 | 83.0% | p < .001 |
| 3, calendar | Widen display and allow more messages; similar numbers of changed/added lines spread through each version | 127.8 / 215.8 | 40.8% | p < .025 |
| 4, purchasing | Add an interactive input-file editor; little interaction with old behavior and no reusable existing module | 82.5 / 82.3 | −0.3% | No significant difference reported |

The exact reconstructed means are **19.25/85.875, 44.125/259.75, 127.75/215.75 and 82.5/82.25**. Their first three monolithic/modular ratios are **4.46, 5.89 and 1.69**. These are substantial positive observed benefits under the study's endpoint. Task 4 preserves a near-zero aggregate difference; it does not prove equivalence or the universal absence of benefit outside the proposed categories. Its phase means also differ in offsetting directions.

Figure 3 places the selected tasks in distinct regions of a conceptual, overlapping three-set taxonomy. It is not a factorial experiment separately manipulating localization, reuse and comprehension on the same task. The calendar result supports faster completion of that assigned source/task bundle; it does not directly establish chunking as the mediator.

Four monolithic attempts do not finish in the initial sitting: two in task 2 and two in task 3. They return, receive unclocked refamiliarization, and finish. The authors count only **half** of the later sitting's timed logic-debugging duration, to compensate for possible forgetting. These are adjusted completed times, not unaltered wall times or missing observations. All modular attempts finish within the first sitting. Every task table contains all sixteen participants.

Taking the displayed timing decompositions literally and restoring the omitted half changes the monolithic means to **274.5** for task 2 and **243.375** for task 3. This descriptive sensitivity check strengthens the modular advantage; it does not recover unrecorded refamiliarization/typing time or validate the adjustment. One stated first-sitting logic duration, 310 minutes, conflicts with the declared 6–10 pm session window. Raw timestamps are unavailable.

The original page images confirm several reporting discrepancies:

- Figure 4 prints monolithic syntax mean **13.9**, whereas its eight entries give **18.875**, consistent with the plotted bar and reported total mean.
- Page 183 labels two task-3 logic totals as **220**; its own formulas give **149** and **239**, agreeing with Figure 6. The sensitivity calculation uses those formulas/table values.
- The later **4.02-times** overall claim has no explicit aggregation rule. The arithmetic mean of the four task ratios is about **3.26**. Use task-specific results rather than adopt an unspecified pooled effect.

The authors choose Wilcoxon rank-sum after Bartlett tests find unequal variances in tasks 2/3 and report similar t-test conclusions. Their wording describes a test of equal means; rank-sum alone does not identify a mean-only effect under arbitrary distribution differences. The chapter provides thresholds rather than full inferential specifications or intervals. The positive timing gaps remain evidence; incomplete inferential detail is not grounds to erase them.

## Preliminary cases and what carries forward — pp. 183–186

Earlier student trials are described as directionally similar. One graduate pilot retains eight of roughly twenty students who finish its pretest; reported p-values range .03–.07. Its selection, unpublished rows and shared investigators prevent treating this summary as independent confirmation of the main case. The authors also report an initial slightly monolithic-favorable pilot that motivated their task taxonomy. That contrary observation helped refine the claim and should remain visible.

Attempts to use preliminary task times as a stable ability covariate failed because participant rankings varied between tasks. This is pertinent to S193's later explanation based on a pretest imbalance: neither report establishes a universally valid programming-ability score. Similarly, the authors' claim that task 4 rules out programmer bias is stronger than that one null comparison can establish; task-dependent behavior remains possible.

**Disposition:** retain strong task-specific positive timings and the fourth-task null; distinguish source assignment, strategy, phase time, supplied-test stopping and residual correctness. Localization and reuse are established plausible mechanisms, but this experiment does not identify a pure cognitive pathway, optimal module size, lifecycle payoff or Nu/agent transfer. Correct targeted editing and safe reorganization remain legitimate strategies.

**Next consequence, updated2026-10-02:** integrate S193’s smaller, inconclusive first-task replication without pooling its later chapter as a new2008 experiment. The original1994 conference paper **S194** now has a verified eight-page user PDF under its existing record; first-page-only coverage is recorded in the [index](INDEX.md). Its full allocation/timing/data method is unread, with access now closed. The fuller report, Daly thesis and S90 dissertation/materials remain separate gaps. Continue accessible type/runtime/oracle alternatives; no experiment, worker or construction is authorized.
