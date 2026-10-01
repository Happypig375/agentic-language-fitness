# S197 — steering constraints, delayed effects and learned tolerances

**Complete author-manuscript reading, 2026-10-01 HKT.** Gregory Gay, Sanjai Rayadurgam and Mats P. E. Heimdahl, *Automated Steering of Model-Based Test Oracles to Admit Real Program Behaviors*, registered as IEEE TSE 43(6),531–555, June 2017, DOI [10.1109/TSE. 2016.2615311](https://doi.org/10.1109/TSE.2016.2615311). The author lists it under 2016. This is an expanded continuation of [S110](S110-model-oracle-steering.md), not an independent replication of the pump study. Reader: main Codex session; no experimental reproduction or independent reviewer.

## Identity, coverage and lineage

Native parent **`E4PANRXS`**, PDF **`Z6LU4T8U`**, note **`YMZMF9C4`** were created and verified before body reading. Existing memberships `PKLXQNEE`, `MBYQJXUF`, `NDU9BTP7` are preserved. The [author PDF](https://greg4cr.github.io/pdf/16steering.pdf) has **24 pages, 682,518 bytes**, SHA-256 **`a57f1633aae2858bb87b7f34c6847dfea37b97bd7e1f340b588996fe19e0ce0a`**. Every page is headed with the journal name and **TBD**, numbered 1–24. It is a prepublication manuscript, not a verified 25-page final edition.

All 24 pages were read in extracted text and visually, including nine figures, seventeen tables, both plots embedded with Tables 13–14, five equations, three footnotes, 54 references and the author biographies. The standard DOI web open was inaccessible. Direct Crossref-listed accepted-manuscript and ordinary IEEE stamp routes each returned **418 HTML**, not PDFs; no challenge bypass was attempted. Final-edition correspondence remains unverified. The same-title May 2015 dissertation is a separate lineage source, not credited as read merely because it occurs in the dataset ZIPs.

The paper now identifies source and data, enabling the bounded artifact inspection below. Original bodies, archives and source copies remain outside Git.

## What the extension adds

The mechanism still adjusts the **oracle model**, leaving the SUT trace unchanged. It instruments the previous model state as an initial state, represents selectable input changes and tolerances as an SMT problem, and searches **one transition** for a closer observable successor. Internal/output variables may be made steerable by temporarily treating them as inputs; constraints govern that freedom. The distance uses selected common observations, not complete state equality.

The expanded prose makes the search more explicit: first seek exact agreement; otherwise halve a distance threshold, then refine from the last viable result. The reproduced pseudocode is an outline, not a complete implementation specification. The released generic code supplies the second refinement loop and numerical details, but does not establish an exact global-minimum certificate in every solver outcome. A current-state tie can select actions with different later consequences.

New evidence includes a second modeled subsystem, a constraint-relaxation comparison, a treatment-learning method, measured computation times and source/data links. Constructive versus declarative model adoption and low constraint-maintenance burden remain reasoned proposals; these studies do not measure either practice claim.

## Systems, reference labels and observation

| System | Stateflow / Lustre size | SUT variants and main suite | Main observations |
| --- | --- | --- | --- |
| Infusion manager | 23 states, 50 transitions, 6,299 lines; Table 4 reports 19 inputs, 825 internal variables, 5 outputs | Two timing variants;50 original-model mutants plus 50 per timing variant:152 SUTs. 100 random tests, 30 steps/seconds each | Flow rate, mode, duration, log indicator, new-infusion flag |
| Pacing subsystem | 48 states, 120 transitions, 24,017 lines;18 inputs, 545 internal variables, 5 outputs | One timing variant, 50 original mutants and 50 timing-variant mutants:101 SUTs. 100 random tests, 30–100 event steps over 3,000 ms | Atrial/ventricular event classifications, event time, next scheduled atrial/ventricular pace |

These are model-derived SUTs, with simulated timing perturbations and seeded faults, not physical devices or independent production implementations. The pump retains S110's case lineage. The random-input probabilities favor normal operation; extreme events such as power-off are unlikely by design. That choice helps isolate steering behavior but constrains rare-event coverage. Timing perturbations are shared across corresponding variants to distinguish timing from mutation effects.

The authors label initial outcomes as pass, acceptable timing, unacceptable timing or fault-induced. They again acknowledge that fault-origin timing deviations can satisfy the allowed requirements. Therefore origin-based masking and demonstrated requirement violations are distinct. Unsteered recall of one is conditional on the original oracle's exposed/labeled failures. The claim that a mutant is unlikely to be masked on every exposing test remains a belief; the paper does not supply mutant-level complete-masking results.

Both metrics are normalized Manhattan or squared Euclidean over selected outputs. The pump's strict tolerances permit five timers to change by −1…+2 seconds. Pacing permits event-time delay 0…4 ms and toggling atrial/ventricular sensed-event indicators. The extension says these constraints were developed from specifications and domain-expert consultation; no independent clinical or hardware validation follows from that statement. Filters compare the specified outputs and tolerate the designated timing ranges while leaving model state unchanged.

## Useful performance with a real tradeoff

The main strict-steering results for both metrics are reported as identical, unlike S110's metric-specific pump counts. Keep those editions separate rather than pooling them as independent replications.

| Main outcome | Infusion manager, Table 6 | Pacing, Table 7 |
| --- | ---: | ---: |
| Acceptable-timing failures initially | 1,406 | 2,208 |
| Correctly reclassified by steering | 1,245 | 2,065 |
| Correctly reclassified by filter | 1,245 | 1,010 |
| Initially exposed fault-origin failures | 2,229 | 4,329 |
| Masked by steering | 43 | 297 |
| Masked by filter | 1,252 | 258 |
| Unacceptable-timing failures retained by both | 268 | 571 |

For pacing, the internally summing Table 7 has 10,100 runs. Own raw-cell calculations give steering precision/recall/F1 **.970/.939/.954**, versus filtering **.795/.947/.864**, and no adjustment **.689/1/.816**. Steering corrects **93.52%** of the 2,208 acceptable-timing failures versus **45.74%** for the filter, but masks **6.86%** of 4,329 fault-induced failures versus **5.96%**. The filter's slightly higher recall is genuine counterevidence to dominance on every endpoint. Page 16's prose gives 258 for steering, although the table gives 297 and its 2.9% and Table 8 recall agree with 297. Preserve the conflict, using the explicit table for the labeled arithmetic.

The pump remains favorable to steering against this filter, but exact aggregate accounting is unresolved: Table 6's initial cells total **15,267**, its post-adjustment cells **15,258**, and its acceptable-timing row has **1,245+152=1,397**, not 1,406. The methods declare 15,200, while the results prose retains 11,364+3,936=15,300 from the earlier account. These are observed manuscript discrepancies, not corrected data. The cumulative-volume comparison repeats the 15,300-cell table, changes initial categories and claims unchanged steering without a reconciled new count table. No acquired run manifest yet resolves those units.

The extension does quantify overhead: mean processing is **.008 s** for tests without steering, **13.54 s** for steered pump tests and **162.91 s** for steered pacing tests, on an i7-4790,3.60 GHz, 16 GB workstation. These are conditional test-processing means, not paired speed ratios, online latency guarantees or net developer effort. Labeling, model/constraint construction and human investigation cost remain unmeasured. The authors retain offline investigation support and recommend an **unsteered final verdict**.

## More freedom can worsen later agreement

The constraint experiment uses each timing variant plus five randomly selected mutants of each original/variant. Pump constraints progress from strict timers −1…+2, through −2…+5, unrestricted timer inputs, to unrestricted inputs. Pacing progressively enlarges event/refractory/rate windows, then frees all inputs. Table 11's pump cells sum to 1,695, whereas the stated 17 variants×100 tests would suggest 1,700; the 1,100 pacing cells sum consistently. These are smaller related subsets, not another large independent sample.

Printed pump precision/recall/F1 are approximately **.93/1/.96** strict and **1/.48/.65** with unrestricted inputs. Eliminating false alarms is achieved partly by admitting unacceptable behavior. Pacing is more revealing: strict is about **.95/.93/.94**, medium/minimal **.94/.77/.85**, unrestricted **.62/.89/.73**. Own raw-cell unrestricted precision is. 615. Despite extra freedom, acceptable-timing corrections fall from 284/306 to 34/306.

The authors explain the latter through delayed effects. Sensed-event/time variables affect the current step; rate, refractory and mode parameters may matter only later. A solver can match today's observed outputs while changing a currently irrelevant parameter that causes an unrecoverable later divergence. This is a plausible, source-grounded account and a scoped adverse result; it is not an independently isolated causal estimate of each variable. Look-ahead and change penalties are proposed future work.

For interactive evolution, carrying state forward is useful, but local distance minimization does not establish preserved future obligations. A final evaluator should not change accepted behavior in response to a candidate's failures. That remains separate from permitted development feedback.

## Learned constraints: useful elicitation, limited validation

TAR3 receives per-step variable changes, before/after observation differences and labels for correct/incorrect/no verdict change. Ten treatments targeting correct changes and ten targeting incorrect changes are generated; overlapping variable/range suggestions are removed and unspecified variables locked. Four starting-constraint levels, two distances and ten stochastic repetitions produce **80 sets per system**. Here “treatment” is a learned restriction, not proof of a causal intervention effect. Learning from locked variables can only tighten their existing freedom.

This experiment uses one pump timing variant, PBOLUS, and the pacing timing variant, **excluding seeded-mutant implementations**. Its perfect or near-perfect recall therefore concerns unacceptable timing in those cases, not learned-constraint retention of code faults. Results are medians over ten learning repetitions, not eighty independent systems.

For PBOLUS, printed median precision/F1 range from **.65/.77 to. 82/.89**, with recall 1; filtering gives. 70/1/.82. Learning from unrestricted inputs can beat that filter on this timing case. Pacing's automatically learned windows initially give precision **.24–.26**, recall 1 and F1 **.39–.42**, versus the filter's. 32/1/.48. A representative strict-derived table corrects 9 of 76 acceptable deviations and retains 24 unacceptable ones.

The authors then widen learned bounds by one at each end and rerun the classified tests. Reported pacing medians improve to **.75/.88/.81**: a useful positive tuning result with loss of timing-failure recall. The text calls its 2–3 to 1–4 event-time example “seconds,” whereas the pacing setup specifies milliseconds; retain that unit discrepancy. The paper describes learning and tuning on classified executions and does **not specify an independent test split, held-out systems or fresh post-tuning validation**. It therefore demonstrates elicitation/tuning potential rather than an established out-of-sample reliability estimate. Human-label correctness and effort are not independently measured; S109 remains relevant to that assumption.

## Released implementation: bounded inspection

The [public prototype](https://github.com/Greg4cr/Steering-Framework) is pinned to **`4c846c0047279b49cb6e49772dadcb6187d9ff71`**,23 June2015. A complete, untruncated 46-entry tree was inspected by path. Eleven selected files, **2,420 lines total**, were read completely: README 117; `SteerModel.java`692; `SteerPacemaker.java`448; `GetScores.java`194; pump/pacing result checkers 496/440; demo configuration 10, tolerances 20 and three one-line lists. An initially incomplete display of the pacemaker loop was covered through targeted rereading. All fetched files match their Git blob IDs and SHA-256 manifests; no binaries or author code were executed.

Material findings are concrete:

- Both steering classes set jKind's bound to **one** and select Z3. The generic code includes range reduction followed by refinement. It treats an `UnknownProperty` as a stopping condition alongside a valid no-counterexample result, and subtracts. 001 when converting fractional scores. This implementation does not justify an unconditional exact-minimum claim.
- The pacemaker driver synthesizes state-update events, limits the working step count to 100 and removes surplus steered-trace records. The README explicitly describes this case-specific event handling. A generic stateful-oracle label alone does not capture that integration work.
- The result checkers classify fault-origin failures using deviations from an **unmutated SUT trace** at initially mismatching steps, then apply timing rules. They accumulate per-test confusion cells and optional prior results. These are concrete reference procedures, not independent requirement proofs or a mutant-level survival analysis.
- Trace comparison assigns 10,000 to an unmatched row. Both result checkers omit a mismatch at `step == steered.size()-1`; with the header convention this is a particular unmatched-suffix boundary, not simply every normal final row. Exact trace alignment, completion and missingness need the executed run manifest before drawing a detection claim from this source.
- The pump checker uses duration-count boundaries and defaults an otherwise unclassified initial mismatch to its within-tolerance category. The pacing checker requires equal trace lengths for filtering and uses one-sided 0…4 timing bounds. These details qualify the high-level comparator description; no static observation here quantifies its effect on the published tables.
- Normalization is optional in code, and the demo leaves it blank. Its suite lists 0…10 and its twenty-input/five-output lists plus strict timer constraints are a demonstrator configuration, not the complete experiment manifest. The README says generic policy options are not implemented in this release. The tree provides no identified TAR3 training/tuning package.

The retained SHA-256 values for the two steering classes are **`0d86292b5a4fc814f1adef2a8f41133b1efa815b32a3003c7db73901bce0c1dc`** and **`e20a72b7cbe5c27e7f9845f1b6d70a552dff5d2a3b70e9e075ff6f5b974d3f9d`**. Result checkers: **`bd0386cf1f5de639c8ba50cd8da93a07bf551f3ce289d810f75c0d7b283d999b`**, **`b414b6403b430bdd5195dc2e52d4d89e99fb330d8bad8803aecc0a4d3cff1466`**. Injection/parser/worker helpers, bundled dependencies, models and demo traces are not fully inspected. This 2015 snapshot narrows implementation questions without certifying the executed journal revision or reproducing its outcomes.

## Dataset access and remaining correspondence

The complete [PROMISE pump](https://openscience.us/repo/test-generation/manager.html) and [pacing](https://openscience.us/repo/test-generation/pacing.html) landing pages lead to Zenodo datasets. Web DOI clicks fail, but direct record APIs and file downloads succeed with verified registered MD 5 and SHA-256. Both archives are attached under S197's existing parent:

| Dataset / native attachment | Exact archive identity | Actual inspection |
| --- | --- | --- |
| [10.5281/zenodo. 268502](https://doi.org/10.5281/zenodo.268502), `K7ICXJFZ` | 13,787,561 bytes; SHA-256 `37f8ad56c83cfde688b89f405caf704150e196f7de92591c4ed5f1046368fd11` | Complete 711-member inventory; full 58-line README; header and complete structural parsing of `random_steering.csv` |
| [10.5281/zenodo. 268508](https://doi.org/10.5281/zenodo.268508), `WHXVXREF` | 15,718,531 bytes; SHA-256 `19a5921a028a89d9ec1afb019e67f48acb54cbab3c3db72284f3145272e30831` | Complete 454-member inventory; full 51-line README; header and complete structural parsing of `random.csv` |

Archive member counts include directories and version-control metadata, not that many independent scientific artifacts. The pump file contains **100 tests×30 rows×20 values**, SHA-256 **`ac10eaa0dac2928b6c1d0ede79387334bbd4c91df70dc615113bf7bcad4a0620`**. The pacing file contains **110 tests**,110 repeated headers, 4,479 rows, 18 values per row and 27–57 rows per test, SHA-256 **`bc0ee152dc9b048ae065f7d097768801b3ac41e874230a06b8b6888e30551621`**. Data values were not individually adjudicated. The latter is a larger raw-input archive than the declared 100-test experiment; event-expanded execution traces are another unit. Selection and final trace correspondence remain unverified.

The pacing README limits the model to VVI/DDD modes and calls the journal work an under-submission TOSEM draft; the registered publication is later TSE. PROMISE dates both donations 21 September2015, whereas pacing's Zenodo metadata dates its deposit 3 February2017. These are dataset/edition lineage differences, not another replication. The inventories expose no named journal result table, classification log, selected-mutant manifest or learning-split package; the binaries, embedded papers, `.svn` contents, fault documents and model bodies remain unread. Acquisition is not full artifact reconstruction or reproduction.

**Disposition:** S197 adds useful evidence for tolerating timing divergence, quantified offline overhead, an adverse delayed-effect case and promising constraint elicitation. It does not establish universal superiority, complete fault sensitivity, independently validated learned tolerances or net development savings. Source/data access is now materially improved; exact run lineage and labels remain explicit residuals. Continue the broader runtime/cost frontier through acquired S111 and the remaining C02/fault-sensitivity methods rather than making this single lineage the whole survey. No theme closes and all experimental holds remain.
