# S97 — design guidelines, module enforcement and later structural choices

**Complete journal reading, 2026-10-01 HKT.** Daniel Joyce, *An identification and investigation of software design guidelines for using encapsulation units*, Journal of Systems and Software 7(4), 287–295, 1987, [DOI 10.1016/0164-1212(87)90028-8](https://doi.org/10.1016/0164-1212(87)90028-8). This B01/B02/B10/B12 predecessor to S92 separates design organization from language support and immediate maintenance effort from subsequent source structure.

## Identity and coverage

Zotero parent `C8Y9RQJS`, existing user-library PDF `UCCBGMCG`, note `9HJVZZHD`. Parent identity and attachment relationship/hash were reverified through the native API before continuing the read. The nine-page journal file has 1,097,757 bytes and SHA-256 `c6e06e3553f6809192f6e0fc54cbcb61d78e52bc8c1ad56824a608ddc74770a4`. All nine pages, five figures, three tables and twenty references were read. All pages were visually inspected because both natural and sorted extraction interleave some columns and corrupt numbers/ligatures. The images, rather than that extraction alone, establish the table entries below.

The paper refers its fuller experimental methods/statistics to the author's same-title Temple dissertation, reference 9, printed as `1986(7)`. That related edition is now **S152**, native parent `KSRQDGTE`, note `N7GD5LRA`, selected for the missing allocation/outcome/data dependency. It is distinct from the journal record and does not imply a second empirical case. No thesis body/PDF was acquired or read. MPACT lists 1987, while an institutional catalog lists a 1986 doctorate; the thesis's exact edition/date remains unresolved. No author contact, purchase, source-program execution or experimental reproduction occurred.

## Mechanism and assigned comparison

The six design guidelines combine information hiding, abstract data types, domain-object modeling, isolation of likely changes/resources/design choices, data-transformation boundaries and reusable generalization. Encapsulation units provide explicit exports, hidden implementation and state that persists between procedure calls. That last use of “persistence” means ordinary module-local state, not immutable historical versions. Similarly, the paper's **functional decomposition** means procedural top-down refinement, not functional programming.

The running example simulates bank arrivals/departures and teller queues. The guideline-based Modula-2 version groups teller queues, bank behavior and the incoming-customer stream into modules. The textbook-style version distributes queue operations among event-handling procedures. Table 1 describes concrete structural differences: 0 versus 3 modules, 11 versus 15 procedures, 139 versus 115 statements, 35 versus 0 global-variable references from procedures, and 48 versus 78 declaration lines. These are representation properties, not measured comprehension or future maintenance benefits. The printed Figure 4b counts sum to 113 statements including module initialization and main, while Table 1 says 115; the 15 procedure counts average 5.2 as printed. This small example-level discrepancy is not resolved by silently changing either source.

Twenty-seven participants were matched on a preliminary task and randomly divided into three groups. Each phase supplied one of three versions:

| Label | Program supplied |
| --- | --- |
| XX | Top-down procedural design without the guidelines |
| GX | Guideline-based design, with modules mimicked using globals, procedures and comments |
| GL | The same guideline-based design supported by Modula-2 modules |

The experiment used three separate programs and switched group membership each time, enabling within-person comparisons. GX versus GL is the nearer language-support contrast; XX versus either changes the original organization as well. The journal does not provide the full assignment sequence, all programs/tasks, participant background, individual observations, all eight dependent-variable definitions or detailed ANOVA results. It reports average program size of 870 lines including comments, little prior encapsulation experience beyond two short projects, and no instruction in the philosophy behind the supplied designs. Those limits constrain transfer; they do not warrant assuming no benefit or assuming that training would have produced one.

## What was observed

**Immediate process measures:** the authors describe ANOVAs on eight performance variables in each of three phases as inconclusive, with scattered significant results and no clear guideline/support conclusion. No treatment means, intervals or complete test results are supplied in this journal account. This is not demonstrated equivalence. Figure 5 reports correlations between the same participants' times under different conditions:

| Time measure | XX–GX | XX–GL | GX–GL |
| --- | --- | --- | --- |
| Understand original program | .84 | .82 | .90 |
| Design maintenance update | .56 | .55 | .49 |
| Debug revised program | .66 | .73 | .68 |

The design-time entries have printed probability values .01, .02 and .04; the other entries print .00 at the displayed precision. Correlation describes stable relative performance across conditions; it does **not** demonstrate equal condition means or eliminate a treatment effect. Printed .00 is not an exact zero probability.

**Chosen solution structure:** the first phase changed the bank program so customers could move to an advantageous queue, including an empty queue. The authors classify two shortcuts as corrupting data meaning or event order, while two alternatives add a specialized enqueue operation or generalize the existing one. They explicitly say the shortcuts produce correct output and require less immediate coding. They therefore measure structural judgments and possible future liabilities, not observed behavioral failure on a later obligation.

Table 2 records shortcut/other counts of **7/2 for XX, 1/8 for GX and 1/8 for GL**. The descriptive difference is large: 7/9 versus 2/18 when the guideline groups are combined. The paper reports a chi-square result at the .01 level. The table has small expected cells, and coding criteria/reliability or an independent blinded classification are not supplied. This is positive evidence of a relation between supplied design and editing strategy for this task, without a measured estimate of eventual harm or a separate GL advantage over GX in this endpoint.

**Boundary transgressions:** across all phases the authors select five opportunities to access a design unit's internal variables from outside it. GX and GL preserve visible intended boundaries; GL can still cross them by changing exports. The reported improper/proper counts are:

| Opportunity | GX improper / proper | GL improper / proper |
| --- | --- | --- |
| 1 | 2 / 7 | 3 / 6 |
| 2 | 4 / 5 | 1 / 8 |
| 3 | 6 / 3 | 5 / 4 |
| 4 | 3 / 6 | 0 / 9 |
| 5 | 9 / 0 | 2 / 7 |
| Total | 24 / 21 | 11 / 34 |

The aggregate rates are 53.3% versus 24.4%, a descriptive difference of 28.9 percentage points. Opportunity 1 goes in the opposite direction; much of the total difference comes from opportunity 5. These are **45 opportunity observations per condition, not 45 independent people**. The study rotates 27 participants across programs/conditions, and the journal does not provide person-by-opportunity assignments. Its pooled chi-square claim at .01 does not itself account for this dependence. Individual data would be needed for an appropriate repeated/clustered analysis; no new inferential claim is made from the marginals.

Together, the findings support the possibility that organization and enforced boundaries influence which correct edits people choose. They do not show that preserving the original boundary is always preferable, that all changed exports are mistakes, or that source organization can replace an independent behavioral endpoint.

## What remains unmeasured and how it affects the survey

Each program underwent only **one maintenance stage**. The authors explicitly propose a future sequence of changes to test whether their structural classifications predict later cost. Claims about slower structural deterioration, longer service life or lower lifetime cost therefore remain hypotheses. Their tasks deliberately excluded changes confined to one design unit, limiting exposure to the very locality benefit the guidelines predict. This is a defined task-selection limit, not a reason to discard the reported inconclusive process results. Larger systems, trained programmers and teams are suggested follow-ups, not observations.

S92 is a later separate study with different Ada tasks, allocation and incomplete outcomes; it should not be pooled with this experiment as if treatment and structural classifications were identical. S152 is instead a fuller account of the present research, pending acquisition. S90's favorable modularity result and S98's distributed-language experiment remain consequential alternatives. Existing foundation readings can supply mechanism vocabulary without being reread merely because they appear in this bibliography.

For Nu/ISE, retain a three-part distinction: **the source convention assigned, the editing strategy chosen, and later behavior/cost**. Compiler-supported boundaries can be changed by the maintainer; valid reorganization must remain an allowed outcome. A one-step structural preference cannot validate a claim of improved future maintenance. These observations motivate controls, not an inference that humans and coding agents respond identically or that D1 is experimentally ready.

**Unique:** unconfirmed; organization and language-supported boundaries have prior maintenance interventions. **Valuable:** concrete structural differences and a plausible longer-term decision, with inconclusive immediate-process evidence and unobserved future benefit. **Scientifically valid:** full journal reconstruction with exact denominators and contrary cells; fuller methods, classification reliability, individual dependence and later outcomes remain separate limits. W172–W175 record the attempted dissertation and citation routes. Scite reporting/citation follow-up remains pending its quota reset. Continue S98 independently while S152 remains access-limited; no experiment is authorized.

**Audit/access update after the 2026-10-01 UTC reset:** S97’s prepared decisions are now submitted and its `citation_report` inspected, with zero skipped entries, missing reasons, unlinked warnings or truncation. The pending state above is historical. G22’s retried S150 incoming graph returns seven edges/eight nodes, including one same-title preprint/publication lineage; SC86 and W181 supply a bounded method/edition screen. Exact counts and open routes are in the [background ledger](../nu-background-searches-2026-09-30.md) and [runtime screen](../nu-background-runtime-screen-2026-10-01.md).
