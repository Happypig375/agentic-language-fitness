# S92 — Information hiding, modification strategies and incomplete outcomes

**Complete publication reading, 2026-09-30.** Linda S. Rising and Frank W. Calliss, *An Experiment Investigating the Effect of Information Hiding on Maintainability*, Proceedings of the 1993 IEEE Phoenix Conference on Computers and Communications, 510–516, [DOI 10.1109/PCCC.1993.344523](https://doi.org/10.1109/PCCC.1993.344523). Zotero parent `69J7XZUJ`, user-library PDF `VLCZUJCH`, note `8CSIVZ5E`.

All seven pages, the task/structure descriptions, itemized outcome counts and 28 references were read. First-page identity and five subsequent page renders verify the protocol, outcome prose, summary arithmetic and references; there are no numbered figures/tables. The PDF has 730,135 bytes and SHA-256 `923b0fe01cf8932d825cc0be32654991ebaa74e1353ce833de1e3fe1781049e9`. Source versions, command scripts, questionnaires, quiz and individual observations were offered on request in the paper but were not acquired; no author contact or experimental reproduction occurred. The named IH(Module) metric is not numerically defined or reported in this paper.

## Live claim and comparison

B01/B02/B10/B11/B12 concern whether encapsulation helps people understand and change a program, whether it influences later structure, and whether structure can stand in for maintenance benefit. This paper is a direct same-language representation-hiding intervention, closer to S89's mechanism than S82's parameter/global comparison. It reports **no association with measured effort variables**, alongside qualitative structural/subjective observations. Its abstract's stronger preservation/improvement claims require the body-level qualifications below.

The original Flight application is about 800 lines of Ada, with a main procedure and five packages. FlightPlan and WaypointList hide aggregate state; FlightLeg, Location and Waypoint hide record representations behind private types. Two modified versions each contain one well-hidden and one deliberately exposed target:

| Version | Flight-plan change: array to linked list | Waypoint-list change: array to tree |
| --- | --- | --- |
| Flight1 | Poor hiding: FlightLeg is moved into FlightPlan, and the array representation is exposed so main/package code accesses it directly. Two design decisions share one package. | Good hiding: representation remains within the package body, with the element type separate. |
| Flight2 | Good hiding: aggregate and element representation remain in separate packages. | Poor hiding: WaypointList loses its body and exposes its array. Waypoint remains separate because merging it would make the task substantially more complicated. |

The treatment therefore changes package responsibility, visible representation, direct versus procedural access, file boundaries and recompilation consequences together. The two poor variants are deliberately **asymmetric**: only one merges element and aggregate decisions. Neither equivalence nor a pure information-content mechanism is independently demonstrated. The comparison does not test immutable versus mutable state, exhaustive matching, Nu or agents.

## Allocation, completion and measurement

Twenty-two graduate software-metrics students at Arizona State University participated in spring 1991, each with at least ten completed CS courses. Only **fourteen completed all stages**, eight using Flight1 and six Flight2. Eight initial participants' reasons, version/order assignments, partial times and modification outcomes are not reported. Of the fourteen completers, nine had worked in industry and seven were currently employed there; this is not an independently sampled professional comparison.

Program version is assigned by **on-campus versus remote attendance** to reduce cross-version information sharing. It is not randomized, and the mapping of campus status to Flight1/Flight2 is not supplied. Within each version, students are paired by Ada experience and assigned opposite task orders; each person thus encounters both good and poor hiding. Actual retained order counts are absent, so attrition may disturb the intended counterbalance. The two observations per participant remain dependent, and the good/poor condition corresponds to different tasks within a version. Site, asymmetric intervention and task/order effects require separation before a causal pooled estimate.

Students knew an experiment was taking place but were not told its target. They used DEC Ada on VAX VMS. Command procedures recorded logins, compile reasons/times, executions and logoffs; students supplied understanding and implementation time since their last login. Timing is thus partly retrospective self-report, not complete automatic active-work measurement. The next task was released after the first was judged correct. The paper does not specify a common deadline, task/oracle tests, independent old-behavior checks or grading/blinding reliability. Correct-completer observations cannot recover all-assignment success or cost.

The stated null concerns time to understand and implement. The result says no correlation was found between hiding and questionnaire information, understanding/implementation time, compile count, executions or total logged-in time. It provides no numerical estimates, coefficients, test names, p-values, intervals, analysis denominators or paired/order model. This is **an unquantified reported null**, not demonstrated equivalence or a measured zero effect. Students also reported spending much of the first task learning Ada. The text says none were familiar with Ada even though five listed it among their three most-used languages; prior exposure is not cleanly characterized.

Twelve of fourteen completers wrote that the poorly hidden part was harder to understand and implement; eight attributed this to poor design. These are retrospective self-reports among completers, distinct from measured time and all-assignment success. Quiz results were mixed: many answered that they did not know unrelated program portions, but answers about relevant portions were also weak. That does not establish preserved overall understanding or a successful comprehension intervention.

## Actual structural observations and incompatible summaries

The detailed result separates **where pointer fields live** from **whether accesses use package routines**. Those dimensions can move in opposing directions for the same submitted version.

| Target and retained modifications | Detailed observation |
| --- | --- |
| Poor FlightPlan, 8 | All eight add the next pointer to the element type, which the authors regard as deterioration. Five retain direct representation access; three add package-body routines and improve access hiding. |
| Good WaypointList, 8 | All eight replace internal routines, keep pointer fields in a new aggregate record and preserve hiding. |
| Good FlightPlan, 6 | Five preserve the separate element type; one puts a pointer in it and is explicitly classified as deterioration. |
| Poor WaypointList, 6 | Four add a package body/access routines; two create helper routines in main, improving that procedure's organization without improving information hiding. One also adds a pointer to the separate element type; it is the same person who did so in good FlightPlan. |

The observations support a bounded possibility that existing boundaries shape later edits, partly through the cost of editing/recompiling another file. They also show correct completers reorganizing poor code and one crossing a good boundary. Structure preservation is not guaranteed and no measured future benefit of the retained structures is supplied.

Three reporting problems materially limit the headline:

- The abstract says well-hidden sections do not suffer deterioration; the detailed good-FlightPlan result includes **one deterioration in six**, giving thirteen preserved good-condition modifications out of fourteen.
- The abstract says poor sections improve in roughly two-thirds of new versions. The body attributes improved hiding to **3/8 + 4/6 = 7/14** poor-condition modifications. Two further main-procedure reorganizations are explicitly said not to improve hiding, and pointer-location deterioration can overlap with access-hiding improvement. Counting all these as one outcome changes its definition.
- The conclusion calls the output **29 new versions** and lists ten deteriorated, thirteen unchanged and six improved, while fourteen completers performing two tasks yield **28 modification observations**. Printed percentages 36%, 46% and 21% align approximately with division by 28 and sum to 103%. The six improvements include the two main-procedure-only changes but omit the three poor-FlightPlan access improvements described earlier. The paper does not explain a twenty-ninth independent version or provide mutually exclusive participant-level classifications.

The page images confirm these are printed ambiguities, not OCR artifacts. Do not normalize the percentages, silently discard a category, assume mutually exclusive counts, or reinterpret 29 as independent people. The aggregate two-thirds-preserved-or-improved summary is not the same claim as two-thirds of poor sections improving in information hiding. Individual source versions/coding rules would be required to reconcile them.

## Implications and follow-up

**Unique:** typed modules and representation hiding were already studied as influences on maintenance strategies and structural preservation. This is prior evidence for a mechanism, not a new Nu innovation. **Valuable:** keeping a decision local can influence edits, but the paper supplies no quantified effort benefit or independent later-behavior benefit; learning, attrition and mixed reorganizations remain material. **Scientifically valid:** separate behavioral correctness, observed strategy, structural preference and cost; preserve all attempts and dependence; permit valid reorganization; and explicitly account for file/tool/feedback differences. These lessons do not establish an agent analogy, validate D1, or authorize new experiments.

The comparison with S91 is instructive: S91 measures integration-period modification counts; S92 measures an attempted maintenance intervention and later source structure; neither endpoint is interchangeable with all-obligation success at a fixed allowance. S92's praise of information hiding should be read together with its unquantified time result and adverse/ambiguous structural cases, without discarding the positive observations.

S90's earlier positive modularity experiment remains a live contrary lead. S92 additionally motivates checking Joyce's encapsulation-guideline study (1986 thesis/1987 journal), Gannon/Katz/Basili's Ada-package study, Woodfield/Dunsmore/Shen's modularization/comments experiment, Henry/Humphrey's C/Objective-C comparison and Rombach's LADY/Pascal experiment. SC23 verifies retrieved identities; its editions, actual coverage and remaining methods are retained in the [background ledger](../nu-background-searches-2026-09-30.md). The recommendation to teach design through maintenance examples is a proposal here, not a controlled teaching comparison against the other Ada team's training.
