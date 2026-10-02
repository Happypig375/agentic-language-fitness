# S132 — static types during scanner/parser development

## Identity and actual reading

Stefan Hanenberg, *An Experiment About Static and Dynamic Type Systems: Doubts About the Positive Impact of Static Type Systems on Development Time*, OOPSLA 2010, pp.22–35, [DOI10.1145/1869459.1869462](https://doi.org/10.1145/1869459.1869462). The SIGPLAN DOI10.1145/1932682.1869462 is a linked identical edition in the existing Crossref record, not another experiment. [University-hosted PDF](https://ics.uci.edu/~jajones/INF102-S18/readings/23_hanenberg.pdf):14pages,1,464,974bytes,SHA-256 `7a2eae04589b46859c2595ac318dda0963cd4b536af446d95888d6ca24b70936`. Native parent/note/PDF **`L6ZLJ59R`/`CCUPSE94`/`U9K3QT3I`** were reverified before body reading.

**All14pages visually read**, including13numbered figures, their eight embedded tables, both footnotes and27references. PyMuPDF/Poppler and the web parser return corrupt character mappings; extracted text is not credited as readable coverage. Rendered pages are readable, with pages7/10/11 enlarged to verify numerical rows. Own passive arithmetic transcribes42scanner times,42scanner debugging intervals and49parser percentages. Original activity logs, source programs, acceptance tests and author analysis code are not acquired or executed. Full publication reading is distinct from experiment reproduction.

This answers a B02/B10/B12 question about development beyond small API-use tasks. It concerns new single-developer programs, not maintenance or successor-domain changes.

## Treatment, assignment and endpoints

Sections3–4 construct two versions of **Purity**, a small object-oriented language, and a common class-browser/test-browser IDE. They share classes, late binding, single inheritance, block closures and a small library. The static version requires nominal annotations on parameters, returns, locals and blocks, and has an additional cast operator. It has no generics; collections contain Object. Static checking of the whole program occurs before execution, and an error in an unrelated method can prevent the requested run. This compares an annotation/checking/feedback bundle in a new language, not removal of checking with all source information retained as in [S130](S130-procedure-argument-checking.md).

Forty-nine undergraduates with Java and formal-language coursework are convenience sampled. Interviews allocate them to two groups intended to balance experience; random allocation is not reported. They have not previously implemented a scanner/parser. Participants are told they are exploring programming, not the specific typing hypothesis. The study runs in six sessions over one year. Dynamic participants receive16hours of instruction and static participants18hours, including extra block-typing instruction. This preparation is outside the27development hours; the reported task comparison is not total training/adoption cost.

Each participant writes a scanner and a simplified MiniJava recognizer from a context-free grammar, using only one language version. Work takes27hours over four days in supervised rooms, with breaks excluded, no work taken away and no sharing. The IDE logs accepted program edits and test attempts. Although the paper describes language×task as2×2, scanner and parser are nested parts of one project; they are not separately randomized task-size conditions or a language crossover.

Two different outcomes are used:

- **Scanner:** replay logged edits after the study and find the first version passing23hidden minimal acceptance tests. Participants do not receive those tests. They are not required to finish the scanner before starting parser work, so its elapsed completion measure can include interleaved work.
- **Parser:** run200valid and200invalid strings against the final delivered program. Passing50% is compatible with a constant true/false recognizer. This is a bounded functional endpoint at fixed time, not time to full completion or maintainability/readability/extensibility.

The common environment reduces language-library/documentation differences, but new-language learning, block semantics, annotation effort, casts and execution gating remain treatment components. The paper itself recognizes limits from design freedom, group balancing and learning.

## Results, with passive checks of printed values

Section5 starts with25dynamic and24static participants. Four dynamic and three static participants never satisfy all scanner tests and are excluded from its timing analysis, leaving21per group. Some excluded people still complete parser work. The scanner result therefore describes observed completers; noncompletion is not zero time or random missingness.

| Scanner quantity | Dynamic | Static |
| --- | ---: | ---: |
| Completers / assigned |21/25|21/24|
| Sum of printed seconds |391,107|582,602|
| Mean seconds, recalculated |18,624.14|27,742.95|
| Median seconds |16,994|28,463|
| Rank sum |370|533|

All42Figure3values reproduce these sums/means/medians and Figure6rank sums. Dynamic mean time is9,118.81seconds lower, about152minutes or32.9% of the static mean **among completers**. The reported Mann–Whitney p=.04 agrees with own continuity-corrected normal approximation p=.04159. Pooled standard error4,127.60seconds gives t≈−2.209 on40degrees of freedom and, using the standard t critical value, the printed95% interval of about−17,461 to−777seconds. The paper reports two-sided t p=.03; its direction and interval are supported by the printed rows.

**Correspondence limits:** Figure9instead prints mean difference−13,140.3, inconsistent with both Figure3means and its own interval midpoint. The text converts the interval to19–291minutes, whereas777seconds is about13minutes. Figure4standard deviations reproduce using population denominators, not sample denominators. These localized discrepancies do not reverse the observed scanner advantage. Original logs and analysis remain needed to establish exact input provenance.

The paper splits each language group by its observed completion median and reports p=.03/.04 within the resulting halves. Such outcome-defined groups cannot establish that pretreatment skill was balanced or eliminate group-composition confounding. Nor does failing to reject normality establish a normal population; the conditional t analysis and rank result retain their actual scopes.

Section6retains **all49participants** for parser functional success. Fourteen dynamic and eleven static entries are exactly50%; the complete printed percentage table confirms those counts. The reported all-participant Mann–Whitney p=.40 detects no distributional difference. It does not establish equivalence, no meaningful effect, or equal total development time. The later analysis excluding50% rows claims12dynamic/11static observations, but Figure12leaves **11dynamic/13static**. Consequently its p=.60 subgroup result is retained as reported, without claiming the printed table reproduces that analysis. Other outcome-based subgroup tests are exploratory and do not establish a task-size interaction.

## Debugging proxy and mechanism limits

Sections5.5/6.2approximate type-related debugging from logged test attempts. For dynamic programs, an interval begins at an execution stopped by an undeclared-variable or missing-method exception and ends at the next successful test run; null-pointer exceptions are excluded. For static programs, the interval begins when attempted execution is prevented by the type checker and ends at the next accepted attempt. The intervals assume participants immediately fix the triggering problem. They may include other work, and the two endpoints expose different information about behavior.

For scanner completers,42Figure10rows reproduce totals50,286/61,935seconds and mean2,394.57/2,949.29seconds, with reported p=.49. Printed Figure11standard deviations1,997/2,113 do not match either sample or population deviations from those rows: sample1,926.80/2,239.14; population1,880.36/2,185.18. The original analysis binding is unresolved. For the full project, Figure13and section6.2report shorter dynamic debugging intervals, p=.01. That is a favorable dynamic result for this proxy, not a demonstrated mediation of development time.

The paper speculates that executing dynamic code reveals partial functional information earlier, whereas blocked static execution does not. It also speculates that static information may compensate elsewhere during the larger task. Neither mechanism is isolated or measured directly. A nonsignificant scanner debugging comparison does not demonstrate equal effort or falsify every possible static-checking benefit.

## Lineage, use and next consequence

The [author bibliography](https://sites.google.com/site/stefanhanenberg/home) and [DBLP record](https://dblp.org/rec/conf/oopsla/Hanenberg10) verify the publication route. The author's58-line software page lists other tools but no resolved Purity/log package. Exact-title/report searches do not recover original material; this is bounded access work, not proof of absence.

[S206](S206-ecoop-type-study-partial.md), the earlier four-page ECOOP2010report cited as reference12, is separately recorded. Its lawful two-page preview describes the same author,49undergraduates, scanner/parser grammar task, custom two-version language, one-language assignment and16/18hour training. Treat it as a related likely shared-study report, **not independent corroboration**; later pages and participant-level correspondence remain unavailable. The distinct SIGPLAN edition of S132 is explicitly an identical work.

S132 supplies consequential adverse evidence against a universal static-typing speed benefit, alongside the positive checking/maintenance/API findings in S130/S117/S126and the mixed tasks in S131. It does not establish a general dynamic-language advantage, that benefits disappear with scale, or a maintenance/agent result. The candidate D1 comparison uses two initially equivalent F# sources, both potentially exhaustive; its future-case guidance and retained behavior are different treatments/endpoints. No Nu, F#/C#, context-window or explicit-case effect can be inferred here.

The selected reading is complete despite the extraction failure. S206's missing remainder and the original logs are specific residual access gaps. Continue acquired **S184** to resolve S183's professional-maintenance allocation, timing and conditional smell/size model, preserving favorable observations as well as limits. The broader type, runtime, persistence and oracle frontiers remain open; no experiment is authorized.
