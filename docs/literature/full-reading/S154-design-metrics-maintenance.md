# S154 — design metrics, observed association and prospective prediction

**Complete chapter and accompanying presentation reading, 2026-10-01 HKT.** H. Dieter Rombach, *Design metrics for maintenance*, Ninth Annual Software Engineering Workshop, NASA Goddard Space Flight Center, November 1984, SEL-84-004, accession 86N19972. [Primary chapter record](https://ntrs.nasa.gov/citations/19860010501); [public proceedings](https://ntrs.nasa.gov/api/citations/19860010496/downloads/19860010496.pdf). Selected as S98 reference 23 to resolve the design/implementation metric method and its validation limits, not to add an independent favorable language comparison.

## Identity, coverage and lineage

Native Zotero parent `SLFNRQJL`, note `82SCRYH5` precede intended body reading. Attachment `7FJMZZDN` is the **364-page proceedings**, 8,450,333 bytes, SHA-256 `c6d1d83e1f48ade65871070f3c8fec3fdc243409f82b99df37b463bf45d1bb51`; parent/file/hash were verified. Full reading covers **PDF pp. 113–149**: the 22-page paper at printed pp. 100–121, a separator marked 121a, and fourteen presentation pages numbered 122–135. Both figures, all three paper tables, all presentation content and nine references were read. PDF pp. 121 and 130–149 were visually inspected, including every figure/table and slide; the other body pages were read as text. A higher-resolution Table 1 crop verifies an inconsistent phase-count total. OCR loses an equation and corrupts some digits; images establish those entries. The whole volume is not read, and there was no source-program execution or experimental reproduction.

The paper explicitly studies six **C-TIP** systems in the DISTOS/LADY project: three time-sharing and three process-control systems. It is a related predecessor of S98, which adds a language comparison and summarizes LADY metrics. The six-system data must not be treated as an independent replication of that project, or silently substituted for S98’s LADY-specific correlations. Exact case/version and participant overlap remains unresolved.

## Measurement model and data collection

The authors distinguish a **change cause** from the several module edits it induces. Stability concerns affected units and work elsewhere in the system; modifiability concerns effort within an affected module. For a given module, “internal” effort is its own work and “external” effort is work in other modules caused by the same change. This is an outcome decomposition, not a guarantee that fewer modules means less total effort.

The model separates explicit shared data, implicit shared assumptions, direct calls/uses and indirect data transfer. An implicit dependency can be a buffer-size or terminal-count assumption absent from a formal interface. Control-flow metrics use direct relationships; data-flow metrics add explicit/indirect transfer; information-flow metrics additionally include implicit assumptions. The latter require analysis or judgment, so their higher descriptive correlation comes with a measurement burden.

An **isolated** exterior metric describes potential use of a library module; an **integrated** metric describes its actual connections within a particular system. Fourteen collected characteristics cover imports/exports, parameters, output parameters, implicit information and connected units. Interior candidates are control structure `v(G)`, design length `L`, and interface-access intensity `IA`. Here `L` counts edges between control/interface-access nodes in a design graph, not simply source lines. `IA` counts imported-function calls plus exported functions. Candidate combined metrics have the form `K ∼ K_exterior × K_interior`, with exterior-only and interior-only comparisons.

Formal design documentation includes import/export signatures, descriptions of purpose and function semantics, and Pascal-like algorithm/control-flow descriptions. Figure 1 supplies a hierarchy of system/subsystem/module views; Figure 2 distinguishes formal interface/control portions from informal explanations. These substantial documentation requirements constrain the proposed automated measurement and its transfer to ordinary code repositories.

Three graduate developers, assisted by students, constructed the systems over approximately eighteen months. Student assistants performed subsequent maintenance work over about six months; a system’s maintainer had not developed it. Each system has 25 seeded-fault corrections, ten environmental changes and fifteen requirement changes: **300 task specifications across six systems**, not 300 independent architectures. Fault-class proportions follow development observations. The paper warns that the selected number/types of maintenance changes were chosen by judgment.

Structural characteristics are explicitly collected **after development, from the final system design**. Change/effort forms cover development and maintenance; weekly author/developer meetings check the data. Comparing final-design structure with development changes is therefore retrospective. Measuring that final version before subsequent maintenance supplies temporal ordering for those tasks, but does not establish that the same measured structure was available at an early design decision. No held-out-system prediction or prospective design-choice intervention is reported.

## Positive results and what their scales mean

Spearman correlations are computed across modules **within individual systems**. The displayed examples represent selected systems, rather than a new independent sample for every metric. Table 2 has 27 metric rows and four outcome columns (104 numerical cells; four dashes); Table 3 has 27 rows and four columns (104 numerical cells; four dashes). The suffixes classify significance: `-` means at least .05, `*` below .05, `+` below .01, and an unmarked numerical value below .001. A suffix dash is not a negative correlation; the standalone blank/dash cells are not measured zeroes.

Representative TSS-1 comparisons preserve the useful signal:

| Outcome | Selected metric | Reported rank correlation |
| --- | --- | --- |
| Affected modules | Integrated information flow × interface-access intensity | .8200 |
| Affected modules | Integrated data flow × interface-access intensity | .7855 |
| Affected modules | Integrated data flow alone | .6458 |
| Affected modules | Interface-access intensity alone | .6828 |
| External change effort | Integrated information flow alone | .8065 |
| External change effort | Integrated data flow alone | .7780 |
| Internal change effort | Integrated information flow × design length | .8230 |
| Internal change effort | Integrated data flow × design length | .7962 |
| Internal change effort | Design length alone | .7049 |

The corresponding best affected-module correlations for PCS-1 are .8168 and .7810 for information/data flow combined with `IA`. For internal effort, TSS-3 reaches .8196 with information flow/length, while PCS-1/PCS-3 reach .7344/.7289. Stronger associations for different outcomes require different interior measures. In particular, ordinary length/control complexity is weak for affected-module counts but useful for internal modification effort. Conversely, `IA` alone is not a useful internal-effort predictor in this account. No universal scalar “maintainability” effect follows.

The author argues that explicit-data metrics are a practical compromise because collecting implicit information is harder. That is a reasonable measurement tradeoff supported by the displayed associations; the paper does not measure the net cost/benefit of adopting those metrics. It supplies neither module-level raw observations, an independent ranking evaluation nor calibrated error for predicted staff-hours. Choosing the best of many correlated metrics within these systems also needs separate validation.

The presentation’s final page explicitly says that **no sufficiently good linear regression relating complexity to maintenance data was found**, and calls for validation in larger projects and realistic maintenance. This clarifies the ordinal scope: high rank correlation does not support multiplying a metric reduction by an estimated number of hours saved. Proposed lower/upper thresholds, optimal complexity balance and early design-choice uses remain open questions.

## Edition, denominator and unsupported-detail limits

- The body studies C-TIP only. Table 1’s mean time-sharing size is about 10.67 KLOC and module-object/type counts are 41.33/20.33; S98’s C-TIP size rounds similarly, but its module counts are 61/20. Process-control counts average 16.33/9.67 here versus 30/9 in S98. Differences in versions or counting definitions are not resolved by their common project lineage. Do not merge the tables or claim six extra independent systems.
- The body identifies three developers and maintenance assistants without a full allocation table. Presentation p. 127 says nine one-person teams, each handling one time-sharing and one process-control system, but does not partition those roles. S98 describes six maintainers. This does not establish a contradiction—the populations/roles may differ—but prevents reconstructing participant independence from the slides alone.
- The slide says faults are identical within a system type, while the body qualifies maintenance experiments as as-identical-as-possible and S98 explains why identical faults were unattainable. Preserve the more detailed limitation rather than inferring identical task exposure.
- Table 1’s PCS-2 development change total is **37**, while its displayed phase counts **2 + 16 + 0 + 10 + 8 + 4 = 40**. Its earliest-document counts sum to 37. Other five phase-count columns sum to their stated totals. This is an unreconciled table discrepancy, not evidence of a reproduced experimental failure.
- Claims that code metrics correlate about .1 more strongly, maintenance needs about twice the effort of the same development changes, and isolation/correction effort shifts from approximately 1:1 to 3:1 are explicitly **not backed by data in this paper**; the author refers to the dissertation. They remain reported observations with an unavailable methods/data dependency, not independently verified ratios.

S153’s acquired contents identify the dissertation’s experiment/data sections, separate implementation/design metric sections, meta-metrics and transfer discussion. Its body remains unavailable. Existing foundation references explain vocabulary and modeling; none replaces these missing primary observations. No additional foundation was promoted merely to inflate reading coverage.

## Effect on the wider survey

This reading resolves how the earlier method constructs its measures and why useful structural association need not be prospective prediction. S98’s positive language-package isolation result remains intact; S154 does not supply its missing test tails or raw LADY data. For Nu/ISE, distinguish representation, availability at decision time, measurement cost, observed edits and independently evaluated later behavior. Exposing implicit dependencies can make a metric easier to obtain without proving lower maintenance cost.

**Unique:** unconfirmed; design-time structural measurement and maintenance association have clear predecessors. **Valuable:** useful scoped rank associations and a concrete explicit/implicit measurement tradeoff, without validated net savings. **Scientifically valid:** full paper/presentation reconstruction with selected-system dependence, timing, raw-data and lineage limits; no new causal estimate or experimental reproduction. Continue S96’s accessible industrial maintenance study to address professional practice, while S153’s specific data/validation gap remains access-limited. All experimental holds remain.
