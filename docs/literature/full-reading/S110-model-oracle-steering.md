# S110 — tolerating divergence without treating agreement as correctness

**Complete reading, 2026-10-01 HKT.** Gregory Gay, Sanjai Rayadurgam and Mats P. E. Heimdahl, *Improving the Accuracy of Oracle Verdicts Through Automated Model Steering*, ASE 2014, DOI [10.1145/2642937.2642989](https://doi.org/10.1145/2642937.2642989). Reader: main Codex session; no independent reviewer or reproduction.

## Identity and actual coverage

Native Zotero parent **`YQBJWRPD`**, existing user PDF **`JDVULA6X`**, note **`8ZVXE5WA`**, were verified before continuing the intended reading. Parent/PDF versions were **2992/2899**; existing memberships `PKLXQNEE`, `MBYQJXUF`, `NDU9BTP7` and attachments are preserved. PDF: **11 pages, 559,896 bytes**, SHA-256 **`33e26865a0d69349c6621ff75dca9dfcbf8c8ac8930f87bea591f80e7febfe0d`**.

Coverage is all eleven pages, printed **527–537**, all four figures, nine tables, five equations, footnotes, algorithm and 32 references. Every page was inspected visually as well as through extraction. A tool output that initially truncated pages 7–9 was reread; no credit rests on that missing output. The complete bibliography ends on page 537. Crossref and the native metadata instead specify **527–538**. A standard publisher PDF request returned **403 HTML**, so exact final-publisher correspondence and the extra metadata page remain unverified.

The [author's eleven-page copy](https://greg4cr.github.io/pdf/14ase.pdf) is **312,134 bytes**, SHA-256 **`c1b603cd521aa577d5f3c5ad97ff8444991ac3c9038096b1d5184dc5ae51e0bf`**. A complete extracted-token comparison finds only the eleven missing printed page numbers. This is strong text correspondence, not a byte-identical attachment or a separate independent study; its full visual equivalence was not checked. No duplicate PDF was added to Zotero. All bodies/extractions remain outside Git.

## Mechanism and integration obligations

The useful problem is model/SUT divergence caused by acceptable timing differences. An idealized model can produce a false failure even when a real implementation satisfies the requirements, and its subsequent state can continue diverging. The proposed solution **steers the model-based oracle**, leaving the SUT execution unchanged. It records the SUT trace, replays inputs against the model, backtracks the model before a mismatching transition, searches for a permitted reachable successor, and continues from the adjusted model state. This differs from correcting a running SUT or merely overriding a verdict.

Three choices determine the accepted behavior: constraints on adjustable variables, a distance over observations shared by model and SUT, and a steering policy. The bounded-model-checking search uses Kind and Z3. The prose first seeks zero distance, then permits successively closer states when policy allows partial improvement. Reachability limits the candidates; constraints limit the allowable adjustments. A mature model and justified tolerances are prerequisites, not consequences of finding a close state.

Figure 3's abbreviated pseudocode does not expose threshold updates, no-solution handling or the final best-target convention with sufficient detail to certify the search implementation. The paper describes limited-transition reachability but does not supply the executed bound, solver configuration, random seeds or exact run manifest. This is an implementation-reconstruction limit, not evidence that the reported method fails. We did not execute the authors' code.

The authors recommend offline use because steering adds computation. Page 531 mentions additional seconds to minutes, without a measured timing distribution, hardware baseline, solver-call counts or end-to-end effort study. The experiment does not establish online suitability or quantify net developer time saved. The suggestion that independently editable constraints are easier to revise than explicit nondeterministic models is a design rationale, not a measured adoption result.

## Case, test units and reference labels

One generic patient-controlled analgesia management subsystem is modeled in Simulink/Stateflow and translated to Lustre: **23 states, 50 transitions, 6,299 Lustre lines**. The SUTs are model-derived variants, not independent physical pump implementations. Two variants delay departure from patient-requested or intermittent bolus modes; fifty single-fault mutants are made from the original and each timing variant. The stated total is **152 SUT versions**: two timing-only, fifty fault-only and one hundred combining both. This is one system with related variants, not 152 independent applications.

The shared suite has **100 random tests of 30 steps**, representing thirty seconds. Timing fluctuations are controlled by an extra input, with the same fluctuation value reused across variants having that timing modification. Pre-steering failures are attributed to acceptable timing, unacceptable timing, or a seeded fault. Mutation operators alter arithmetic/relations/Boolean operations, previous-cycle values, constants and same-type variable uses. Cited mutation-validity studies are separate evidence; this case does not itself validate transfer to real defects.

Fault-origin labels are not identical to requirement-violation labels. Page 535 explicitly says that a fault-caused timing deviation can remain within the allowed tolerance and is nevertheless classified as fault-induced. Such a deviation can pass steering, and the authors expect a human using the same requirements might agree. Consequently, the reported false negatives measure loss against this experimental labeling convention; they cannot all be relabeled demonstrated hazardous behavior. Conversely, a lack of hazardous evidence is not assurance of safety.

The initial model's passing runs are treated as true negatives. Thus the unsteered recall of one is conditional on faults exposed and labeled by this setup, not proof that the original oracle detects every real fault. Mutant-level complete masking, equivalent-mutant treatment, interactions in attribution and general detection probability are not recoverable from the pooled tables.

## Executed tolerance and comparator

Five of twenty model inputs may change: patient-bolus duration, intermittent-bolus duration, lockout interval, intermittent-bolus interval and total infusion duration. Each adjustment lies between **current value minus one and current value plus two seconds**. The other fifteen inputs, including prescription and sensor inputs, remain fixed. The paper regards this as a realistic timing allowance; it does not test sensor inaccuracy or derive clinical validity from these chosen numbers.

The main observations are five outputs: commanded flow rate, current mode, active-infusion duration, log indicator and new-infusion flag. Numeric values are normalized to zero–one using predetermined minima/maxima; unequal Boolean or enumeration values contribute one. The two distances are Manhattan and **squared** Euclidean. Their numeric normalizers and selected observations affect the preferred target; a small distance does not imply equivalence of unobserved state or external effects.

The stepwise-filter baseline permits a mismatch when the SUT is in a patient/intermittent dosage mode no longer than the prescribed duration plus two seconds, its flow rate matches that mode, and all other observed variables agree. It neither searches reachable states nor changes the model state. This is a concrete comparison against this filter, not every possible tolerant or history-aware oracle. The paper acknowledges alternatives and that adding reachability to a filter narrows the conceptual difference.

## Positive and adverse results, with denominators

Tables 3–6 provide the following raw run counts. “Fault-induced” retains the authors' origin-based label.

| Initial category | Initial count | Squared-Euclidean steering: pass / fail | Manhattan steering: pass / fail | Filter: pass / fail |
| --- | ---: | ---: | ---: | ---: |
| Pass | 11,364 | 11,364 / 0 | 11,364 / 0 | 11,364 / 0 |
| Acceptable timing failure | 1,438 | 1,286 / 152 | 1,198 / 240 | 1,286 / 152 |
| Unacceptable timing failure | 268 | 0 / 268 | 0 / 268 | 0 / 268 |
| Fault-induced failure | 2,230 | 43 / 2,187 | 43 / 2,187 | 1,253 / 977 |

**Own arithmetic:** every column totals **15,300**, although the methods and results repeatedly say **15,200** runs. The failing rows sum to the stated 3,936; the mismatch concerns the total/pass accounting. Including an unmodified model's hundred runs would explain the difference arithmetically, but no acquired manifest establishes that explanation. Preserve the discrepancy rather than silently changing a cell or the experimental design.

Within the reported categories, squared-Euclidean steering correctly reclassifies **89.43% of 1,438** acceptable-timing failures; Manhattan reclassifies **83.31%**. Both retain all 268 unacceptable-timing failures and mask **43/2,230 = 1.93%** of initially exposed fault-induced failures, or **43/2,498 = 1.72%** of all reference-positive failures. These are more informative denominators than the paper's approximately .3% of all runs. The particular filter removes the same 1,286 timing false alarms as squared-Euclidean steering but masks 1,253 fault-induced failures. This is a substantive favorable comparison for steering under the stated setup.

From raw cells, precision/recall/F1 are approximately **.635/1/.776** unsteered, **.942/.983/.962** for squared-Euclidean steering, **.911/.983/.946** for Manhattan, and **.891/.498/.639** for filtering. Table 7 instead prints F1 **.77/.96/.94/.64**, respectively; not all printed values are conventional two-decimal rounding of the raw cells. The qualitative comparison survives, but exact reproductions should use a reconciled dataset. No confidence intervals, independent system replications or developer time measurements accompany these pooled estimates.

Steering reduces the number of reported failures to 2,607 or 2,695. That reduction includes both corrected false alarms and the 43 masked fault-induced outcomes; it is not all beneficial time saved. The authors explicitly recommend steering as a way to focus investigation and recommend an **unsteered run for the final verdict**. Their hypothesis that a fault is unlikely to be masked on every exposing test is not demonstrated by these run-level tables.

## Cumulative state and finite observation

The additional experiment observes total infused volume as well as the five outputs. Table 8 has initial-pass 11,311, acceptable-timing 1,435, unacceptable-timing 268 and fault-induced 2,286: again 15,300 total, but **different reference-category membership** from the five-output comparison. The filter now passes 312 acceptable-timing failures and 598 fault-induced failures, retaining 1,123 and 1,688 respectively. Own raw-cell precision/recall/F1 are **.635/.766/.694**; Table 9 prints **.64/.76/.70**. These are reported separately from the original observation definition.

The authors state that adding volume makes no change to the steering results in Tables 4–5, but do not provide a complete new steering table reconciling the changed initial categories. Therefore do not treat the statement as a verified paired, identical-label comparison. Its mechanism is nevertheless useful: changing the model's state can carry tolerated timing history forward, while the selected filter only changes judgments and leaves accumulated model state untouched.

This is not an unbounded temporal guarantee. Thirty-second tests of one modeled subsystem do not establish all later reservoir behavior, arbitrary asynchronous triggers, pending work, external effects or reset correctness. Local tolerance, observed state, finite history, origin-based fault labels and final adjudication must remain separate. For Nu/D1, the transferable lesson is to state which divergences are acceptable and which state/history is observed; it does not authorize adapting final scoring to a candidate's behavior.

## Lineage, residual understanding and disposition

No study-package URL is supplied in the read article. The author's publication page identifies an earlier ICSE 2014 NIER proposal, a same-title 2015 dissertation and an expanded TSE article. **SC129**, exact-title search with `limit:20`, offset zero, returns two records: the journal DOI **10.1109/TSE.2016.2615311** (2017 issue; author's page groups it under 2016) and dissertation DOI **10.13140/RG.2.1.4602.8647**. Neither return supplies an abstract, body excerpts or citation contexts. They are lineage leads, not independent confirming studies. The journal continuation is selected as S197 to check broader cases, masking units, costs and any artifact route before expanding claims.

**Established mechanism:** bounded reachable-state adjustment can tolerate modeled divergence while carrying state forward. **Measured effect:** in this one model-derived setup it corrects many timing false alarms and retains considerably more fault-induced failures than the implemented filter. **Residual limits:** observation-dependent labels, seeded-fault origin versus requirements, total-count and edition discrepancies, unacquired run/configuration data, and unmeasured developer cost. These qualify the useful result without discarding it. S104's steering primary dependency is now reconstructed; the broader oracle survey remains open. All construction and experimental holds remain.
