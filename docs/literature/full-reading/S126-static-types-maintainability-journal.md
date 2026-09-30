# S126 — Typing and maintenance: expanded analysis of the S117 experiment

**Complete publisher-publication reading, 2026-10-01 HKT; printed-data reconstruction, no experimental reproduction.** Stefan Hanenberg, Sebastian Kleinschmager, Romain Robbes, Éric Tanter and Andreas Stefik, *An empirical study on the impact of static typing on software maintainability*, Empirical Software Engineering 19(5), 1335–1382 (October 2014), online 11 December 2013. DOI [10.1007/s10664-013-9289-1](https://doi.org/10.1007/s10664-013-9289-1).

## Identity, coverage and publication relationship

Zotero parent `SNE5FUTY`, publisher PDF `N3I67UQQ`, note `Y4CB9BQ9`. The record existed before body reading. The publisher/library file has **48 pages, 2,365,062 bytes**, SHA-256 `973fc5f3659f3a40de5b2300b56f61d6acb097964a04bc04d1602d02e6e9b1ae`. All 48 pages, nine figures, fifteen tables, code examples, forty references and author biographies were consumed. Figures were visually inspected at PDF pp. 11, 19–23 and 27–29; additional visual checks covered pp. 1/18/30/35–37/43. Tables 10–11 contain raster code: their complete examples were read from rendered pp. 35–36, not credited from their otherwise nearly empty text extraction. Tables 12–15 were reconstructed from every printed row.

The separate [author copy](https://pleiad.cl/papers/2014/hanenbergAl-emse2014.pdf), attachment `IR9WUVNS`, has 48 pages, 2,011,973 bytes, SHA-256 `b0214f2a6824d2d94f592183da9c6cfe020b8c44f3b40401dd7be8f5c2e4ea86`. Its opening identity and Table 15 were compared; the whole author edition was not reread or declared textually equivalent.

PDF p. 3 explicitly calls this an extension of [S117](S117-static-types-maintainability.md), adding related work, method/threat discussion, interaction-log analysis and comparison with a previous API study. **Every subject ID, order label, task time and total in journal Table 12 equals conference Table VII exactly**: 33 rows, 594 times and 66 totals. These are two publications of one experiment, not an independent replication. The journal's exploration of additional measurements is new analysis of the same attempts.

The live B02/B10/B12 question is whether favorable maintenance timings support a type-information/navigation mechanism, and how much the superseding analysis changes the conference interpretation. Neither publication assigns D1's explicit-current-case versus catch-all convention.

## Method and retained timing evidence

The reconstructed S117 design remains: 36 initial volunteers, 33 completers; 17 Groovy-first and 16 Java-first; nine fixed-order task forms repeated in both languages. A Java game-derived base was translated to Groovy without annotations and renamed into an email-domain Java variant. Names were weakened to remove direct type cues. Participants were Java-proficient; Groovy was restricted to Java-like usage. The custom editor omitted modern IDE navigation/completion, and tasks stopped when supplied runnable tests passed. The journal explicitly treats that endpoint as correctness (p. 8); it does not provide an independently held-out behavioral oracle.

The journal adds the Ubuntu 11.04 boot image/USB procedure and ThinkPad R60 machines with 1 GB RAM, but not an acquired image, test suite or interaction-log archive. Attrition reasons/retained occupational composition still are not resolved. Two selected type-error repairs favor Java in both orders, and CIT5 does too. Several other class-identification tasks have mixed order-specific evidence. Semantic repairs favor the second language in each order group.

The universal statement that nobody is slower overall in Java persists at p. 18. Its own Table 12 still contains the five counterexamples identified in S117: subjects 21/23/26/27/33. Preserve the lower Java aggregate mean and the task-specific positive findings; reject the universal participant statement.

The expanded analysis does not remove the inference limits of combining separate significance decisions. Section 3.6 calls one significant group plus one nonsignificant group a smaller language effect, opposing significant groups an effect smaller than learning, and two nonsignificant groups an effect too weak to matter. These interpretations require assumptions beyond the reported significance classifications. No equivalence margin, practical threshold or identified decomposition of learning and language effects follows from them. Fixed task order, domain coupling and task-dependent learning remain. The round-specific repeated-measures ANOVAs and taskwise Wilcoxon results are author reports, not independently rerun SPSS analyses.

## What the additional measurements mean

Section 6 adds three per-attempt outcomes:

| Measure | Author definition | Interpretation boundary |
| --- | --- | --- |
| Test runs | Each attempt to launch supplied tests, including compilation failures that prevent execution | Not a count of executed tests, test coverage, independent repair attempts or failures detected. |
| Files opened | Distinct viewed files per task, regardless of repeated visits | Not total context traffic, retained memory, source volume or useful information gained. |
| File switches | Transitions from one viewed file to another, including repeated visits | A navigation proxy; neither comprehension effort nor a causal mediator is directly measured. |

The exploratory analysis relaxes its reporting threshold: `.05 < p < .15` is presented as a trend, with additional combined significance/trend rules. Six ANOVAs plus taskwise/orderwise comparisons examine these outcomes; no general multiplicity control is stated. Partial eta-squared values of .350/.688 for test launches and .456/.454 for later-round switches/files are reported. They are model-dependent effect summaries, not proof that typing causally explains 35–69% of every participant's behavior.

Printed Tables 12–15 contain **132 rows and 2,640 measurement/total entries**. Every one of their 264 row totals equals the sum of its nine entries. This verifies arithmetic and extraction against printed headers; it does not establish that the labels or original recording are correct.

The following favorable descriptives use time, test-launch and viewed-file tables, whose respective task labels were retained. They are aggregate summaries of dependent participant/task observations, not new inferential estimates.

| Task | Mean time, Java / Groovy seconds | Mean test launches, Java / Groovy | Mean files viewed, Java / Groovy |
| --- | --- | --- | --- |
| TEFT1 | 235.85 / 928.06 | 2.64 / 8.03 | 3.52 / 6.97 |
| TEFT2 | 146.91 / 849.24 | 1.94 / 6.58 | 3.15 / 8.33 |
| CIT5 | 690.52 / 1,112.18 | 3.94 / 16.30 | 12.42 / 14.09 |

For both type-error tasks, the mean launch and viewed-file differences also favor Java in both order groups. CIT5's viewed-file medians are **13/13**, despite differing means and strongly differing test-launch counts. Different navigation proxies do not express the same effect. On semantic tasks, the authors find some Groovy-favorable navigation indications despite their inconclusive timing interpretation; the underlying launch/file means also reverse with language order. These results do not justify discarding adverse task families or replacing time/behavior with a convenient proxy.

## Unresolved presentation and file-switch discrepancies

The paper's explanation that file switching is the strongest indicator of time needs an explicit qualification beyond correlation-versus-causation.

**Figure legends:** in Figures 7 and 8, the legend labels horizontal hatching Java and diagonal hatching Groovy, but prominent distributions correspond to the opposite labels in Tables 13 and 14. For example, Figure 7's horizontally hatched CIT5 distribution centers near sixteen launches, whereas printed medians are Java four and Groovy sixteen. Figure 8's horizontally hatched TEFT2 distribution centers near eight viewed files, whereas printed medians are Java three and Groovy eight. Do not silently read these plotted directions as labeled or infer a corrected original dataset from an apparent legend inversion.

**Table 15 versus the claimed file-switch directions:** under its printed task/language headers, the reconstructed TEFT2 medians are **Java 32, Groovy 10**; only **6/33** participants have fewer Java switches. Its Groovy-first/Java-first mean pairs are **33.29/23.00** and **50.38/22.06**. Yet Table 7 and the discussion claim fewer Java switches on both type-error tasks in both order groups. Conversely, the printed SEFT1 column gives **32/33** participants fewer Java switches and means **8.18/40.41** for Groovy-first and **10.88/41.50** for Java-first; Table 7 reports a Java-first advantage for Groovy. These are substantial correspondence problems, not merely the choice between mean and median.

The publisher table was visually checked, and **all 33 Table 15 rows also match the author PDF**, with the same printed headings. Thus the discrepancy is not resolved by the local extraction or switching these two editions. Figure 9 and the inferential summaries also require source-label reconciliation. No task-column permutation, language-label swap or corrected result is adopted without provenance. The time table and the independently reconstructed test-launch/file-open tables remain usable within their stated limits; the file-switch mechanism claim is **unresolved at its source/measurement boundary**.

A focused publisher-page search for “Supplementary” and “Correction” returned no matching strings; Crossref supplied no update relation. Two focused web searches recovered the author-upload route and a secondary thesis, not a correction or raw-log packet. This is a bounded unsuccessful recovery attempt, not proof that no correction/data exists. No author contact, external message, payment, installation or experiment was performed.

## Synthesis and next sources

The authors themselves say in §6.7 that the relation between navigation indicators and time is not established as causal. A longer attempt permits more navigation, and comprehension difficulty, checking and source information change together. Even an internally consistent correlation would not isolate the effect of reducing navigation or equate human file switches with agent context cost. Here the additional publication discrepancy further limits that interpretation.

The expanded bibliography preserves genuinely contrary evidence: it describes a dynamic-typing benefit on a scanner task, costs of casts on short tasks, and API tasks favoring either language. Those summaries identify necessary primary comparisons; they are not new full readings or independent confirmation here. SC47/SC48 recovered the exact identities of Prechelt–Tichy argument checking `10.1109/32.677186`, Hanenberg's 2010 experiment `10.1145/1869459.1869462` (SIGPLAN edition `10.1145/1932682.1869462`), Mayer's undocumented-API experiment `10.1145/2384616.2384666` (SIGPLAN edition `10.1145/2398857.2384666`), and Ko's navigation study `10.1109/TSE.2006.116`. Same-title edition links do not add replications. The cited Steinberg–Hanenberg 2012 debugging work is explicitly unpublished work in progress; the Kleinschmager thesis remains unacquired.

S127–S129 already have records and PDFs. Their complete type-name, documentation and IDE methods now take priority over extending a large citation neighborhood: each can separate a specific unresolved mechanism in this experiment. The 2016 dynamically favorable task-design study and C02's coverage/extensibility methods remain active contrary/transfer routes. Keep the now-accessible Join Token methods and broader themes visible; this is not a D1-only stopping rule.

**Unique:** unresolved; static checking and type-information/navigation arguments have direct empirical predecessors. **Valuable:** selected type-error timing, launch and viewed-file benefits remain concrete; net effort, ordinary-task prevalence and Nu/agent transfer are unmeasured. **Scientifically valid:** publication/data lineage and printed arithmetic are resolved; the file-switch data/labels, causal mechanism and generalization are not. ISE's oracle, source equivalence and apparatus remain unvalidated. No theme or experimental hold is closed.
