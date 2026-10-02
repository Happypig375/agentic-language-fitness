# S222 — Statistical testing, state control and initialization interactions

**Identity:** Hélène Waeselynck, *Vérification de logiciels critiques par le test statistique*, doctoral thesis, Institut National Polytechnique de Toulouse, defended **19 January 1993**, LAAS report **93.006**, order 681. The [author bibliography](https://homepages.laas.fr/waeselyn/index.php?choix=3) links the [selected primary PDF](https://homepages.laas.fr/waeselyn/papers/these_Helene_WAESELYNCK.pdf). Chapter III contains a primary account of [S221's formal/statistical experiment](S221-formal-statistical-testing-access.md); Chapter V extends the same component to integration and initialization testing. These are related experiments on one case, not independent industrial replications.

**Library and acquisition, 2026-10-02:** native preflight covered 240 collection parents and 1,234 global top-level items with no matching title. Parent **`I5ASL6PY`**, PDF **`XU49C43Y`** and note **`A62LWB6X`** retain collection `PKLXQNEE`; the parent preceded intentional body reading. The PDF has **187 physical pages**, **599,295 bytes**, SHA-256 **`f85ca1170d7dca9f15986310754e092091fc901116313803c983c962accf1759`**, MD5 **`8672627d629ae2658ffab1bf99b41882`**. Stored attachment bytes were read back and verified. Bodies, extraction, images and own arithmetic remain ignored local artifacts.

## Exact reading boundary

This is a **bounded primary-method reconstruction**, not a full-thesis reading. Text coverage is PDF **1–11, 38–39, 45–49, 57–90, 117–170 and 176**: **107 physical pages**, including blank pages 2, 6 and 90. This includes front matter/introduction, selected Chapter II definitions and probability arguments (printed pp.30–31, 37–41), **all Chapter III (pp.49–81)**, **all Chapter V (pp.109–156)**, the **complete general conclusion (pp.157–162)** and the bibliography page containing the Marre1992 entry (p.168). Other search locators/partial contents passages are not complete-page credit. Chapters I and IV, most of II and the remaining bibliography are not systematically read.

Visual inspection covers PDF **1, 46–49, 59–60, 62, 64, 67, 69, 71, 73, 77–79, 81, 84–87, 125–126, 128–129, 132, 134–136, 139–141, 146, 148–152, 156–158 and 160–161**: **43 pages**. This includes all **16 Chapter III figures**, all **21 Chapter V figures**, selected II figures b–d, tables, the central probability formula and harness/initialization passages. The landscape histogram is rotated for inspection. PyMuPDF emits a color-profile warning on some pages; text extraction and the inspected renders remain usable. The awkward text wrapping around Figure V.r is visible in the source. No claim is made to uninspected graphics or independent numerical replication of the transition matrices.

## Unit experiment: useful selection evidence with explicit budgets

Chapter III studies four C functions from one **1,091-line** nuclear emergency-rod monitoring component. Its 24ms cycle handles 19 positions from five interface cards. The selected functions contain **30, 43, 135 and 77 lines**; FCT3 performs filtering and FCT4 conversion. Ten structural criteria induce several equivalent criterion classes for each program.

Mutation creates **2,914** variants; **98** are judged equivalent, leaving **2,816**: 265/548/1,416/587 by function. The footnote on p.52 identifies only **one known real unit defect** in the supplied testing documents, corresponding to an FCT2 mutation. Equivalence includes 40 functionally equivalent, ten systematically masked and 48 environment-dependent cases. These classifications are relative to execution/observation conditions, not all mathematical equivalence of arbitrary implementations.

| Selection | Suites and input lengths | Observed scope |
| --- | --- | --- |
| Deterministic structural | 73 suites across the four functions; lengths 2–19 inputs | Criteria are exercised through small selected representatives; weaker suites for the first three functions are often subsets of stronger ones. |
| Criterion-guided statistical | 22 suites: one each for FCT1/FCT2, five under each of two distributions for FCT3/FCT4; lengths 170/80/405/850 | Distribution targets criterion-element activation, with a nominal probability target and different criterion classes. |
| Uniform statistical | Twelve suites: one each for FCT1/FCT2 and five each for FCT3/FCT4 | Lengths match the corresponding guided suites, not the deterministic ones. |

The structural-statistical suites kill all eligible mutants in FCT1/FCT2 and, under the all-path distribution, FCT3. Uniform suites also kill all in the first two functions; uniform is not uniformly ineffective. In FCT3, all-path deterministic scores are .792/.840, whereas each all-path statistical suite kills all 1,416 mutants. A weaker statistical distribution leaves 17 survivors because two paths receive zero probability; the five uniform suites leave 229–626. In FCT4, the guided suites achieve .9898–.9915: five boundary-index mutants always survive, while a sixth is killed by one suite under each of the two guided distributions. Boundary-directed tests are therefore complementary to broad stochastic stimulation (pp.64–73, Figures III.j–n).

The positive guided-selection result is substantial within this case. It does not isolate selection strategy at equal deterministic/statistical test budgets, and suite replication is only one for the two small programs. It measures detection of this mutation population, not developer benefit or a multi-system industrial defect rate.

Own bookkeeping reproduces 73/34 deterministic/statistical suites and **31,671** statistical suite–mutant pairs. The printed deterministic total is **50,533**; multiplying Figure III.g's suite counts by the stated mutant populations gives **50,553**, a 20-pair discrepancy left unresolved. No mutation score is recalculated from an unavailable original result file.

## The harness is part of the behavioral claim

The generator adapts `drand48`, checks several elementary randomness properties and writes seeded input files. A supervisor and per-program executor compare outputs against the original program, whose reference behavior is checked with specification-derived invariants/partial inverses. Target/host integer-width differences require a conversion constant correction. The harness detects execution errors/timeouts, resumes subsequent inputs with retained shared state and stops after ten execution errors. A mutant is killed by a detected execution fault or output difference. These are meaningful oracle safeguards, not a proof that the reference implementation is correct.

Pages 75–78 expose a consequential hidden-state case. Deleting a zero assignment in FCT3 makes an intended combinational operation depend on the output cell retained from the previous call. Starting a new process or resetting that cell to zero for every input can hide the mutant; initializing to one can hide a converse assignment defect. Test ordering can make a shorter subset sequence reveal a fault that the longer sequence misses. Another pointer mutation has environment-dependent, intermittent consequences. Input-set inclusion therefore does not automatically imply sensitivity inclusion for the executed stateful sequence.

The lesson is conditional: reset according to the specified semantics and record retained state. Other operations intentionally need their previous value. Neither always resetting nor always preserving memory is a universal oracle policy.

## S221 linkage: control, observation and the denominator

Pages 78–80 and Figure III.p compare five **282-input** algebraic suites with five **405-input** structural-statistical suites on FCT3's **1,467 generated mutants**.

| Control and observation | Equivalent / eligible mutants | Survivors in the five suites |
| --- | --- | --- |
| Algebraic input sequences, closed-loop internal state; filtered output only | 122 / 1,345 | 40, 47, 42, 29, 40 |
| Same closed-loop suites; filtered output and calculated state | 122 / 1,345 | 0, 0, 1, 2, 0 |
| Statistical inputs with direct internal-state control; output and state | 51 / 1,416 | 0, 0, 0, 0, 0 |

Without direct state control, some paths/trajectories cannot occur and additional mutants are masked. Adding state observation makes corrupted state visible before it propagates to the final filtered output. Those choices explain both the strong formal-testing result and why the statistical comparison cannot be read as an isolated selection-strategy effect. More internal observations require a correct oracle for them; arbitrary implementation-state identity is not automatically the application requirement.

The **1,345 and 0/0/1/2/0** values match the S221 revised-chapter preview. This primary author account resolves the mutation population and harness dependency behind S220's compressed known-bug narrative. It does not supply every missing LOFT unfolding/regularity detail or prove equivalence of the unavailable original and revised publications.

## Integration: statement coverage misses temporal interactions

Chapter V compares two implementations of the same approximately 1,000-line component: **INDUS**, supplied by industry, and **ETUD**, written by a student. The initial functional model has operating-mode automaton **M0 (12 states, 88 transitions)**, filtering automaton **M1 (12 states, 54 transitions)** and conversion decision table **M2 (eight rules)**. Reset/restart input connects otherwise absorbing behavior. Separate input profiles target high-level M0 and low-level M1/M2 to avoid starving subordinate behavior.

The method adjusts input probabilities to increase the least frequent modeled state/rule, using a .05 probability grid and a stationary convergence threshold of 10^-6. The reported low/high suite portions contain **85 + 356 = 441** inputs. Five such functional suites are compared with five **500-input** structural suites empirically tuned for ETUD statement coverage, and one **5,300-input** uniform suite. The least executed ETUD statement block appears at least fourteen times in each structural suite.

The programs are run back-to-back. On a difference, the first fault is diagnosed/corrected and the same suite rerun until agreement. Results are consequently conditional on successive repairs; for example, H is exposed only after G is corrected. They are not thirteen independent single-fault variants or an untouched final evaluation.

Initially twelve distinct faults are diagnosed: **A–K in ETUD**, and **Z in INDUS**. Z is missing explicit zero initialization: operational hardware clears RAM, whereas the ported test harness preserves a value across simulated resets. It demonstrates an environment-dependent portability/initialization obligation, not an observed operational reactor failure.

| Initial suites, Figure V.k (p.133) | Faults detected |
| --- | --- |
| Uniform, one suite of 5,300 | A, D, F, G, H: five of twelve |
| Structural, five suites of 500 | A–F, I, J, K in all five; G in 2/5, H in 1/5, Z in 3/5 |
| Functional, five suites of 441 | A–K in all five; Z in 4/5 |

Functional selection produces a favorable detection result with fewer inputs in this comparison. High statement coverage alone misses some operating-mode/initialization interactions. Test design, specification and diagnosis costs are not measured comparatively, so input savings are not a net engineering-cost estimate.

## Refinement: deliberately exercise behavior after initialization

The remaining Z miss motivates a more detailed **Statemate** specification. Hierarchical Statecharts represent lifecycle, orthogonal activities, broadcast events and shallow/deep history. C leaf functions supply some calculations. The high-level chart has 33 terminal states; ordinary-card, special-card and conversion charts have 55, 44 and 35. Model and corrected implementation agreement is checked on existing suites; this is useful consistency checking, not independent proof of the model's truth.

The selected coverage criterion is explicitly weak: terminal-state coverage, merging analogous states across 19 measurements. It does not cover all simultaneous configurations or event sequences. Four kinds of cross-level interaction are distinguished: activity lifecycle, synchronization/information flow, higher-level access to lower-level I/O, and changes to another communicating activity. The implemented refinement targets **initialization and its transient aftermath**: select the first subsequent input to raise conditional activation probabilities, then resume the ordinary profile until the next initialization (pp.148–153).

Empirical instrumentation uses 22 low-level and seventeen high-level counters. The five new suites retain **441 inputs**; low/high terminal minima are eleven/seventeen activations, and initialization occurs at least 104 times per suite. The author explicitly does not derive a precise theoretical Statechart suite bound here.

All five refined suites expose a new **L defect in ETUD**, depending on the **first five measurements after initialization**, between execution 15 and 267. None of the earlier structural or functional suites found it. After correcting L, the three versions agree; testing the original implementations then detects all twelve earlier faults in every refined suite, including Z (pp.153–154). The case therefore reports **thirteen distinct real defects in total: twelve student defects and one industrial implementation's ported-environment defect**. This is productive method refinement on the same case following a known miss, not a held-out generalization estimate.

## Probability and finite-observation boundary

Chapter II's expression `q_N = 1 - (1 - P_min)^N` describes the least element's marginal activation probability under independent repeated draws. It is neither the joint probability that every criterion element is covered nor a probability that the program is correct.

Chapter V Equation 5.1 instead inserts a stationary state probability and adds a convergence prefix. **Own mathematical qualification:** stationarity does not make successive state visits independent. A symmetric two-state chain with .99 self-transition probabilities is already stationary at (.5,.5), yet the probability of never visiting one chosen state in N consecutive observations is `.5 × .99^(N−1)`, rather than `.5^N`. At N=20, the corresponding hit probabilities are approximately **.587** and **.999999**. A burn-in prefix does not remove that dependence. Thus stationary marginal probabilities alone do not establish the stated general finite-run hit guarantee; a no-hit/first-passage argument or additional dependence assumptions are needed. This symbolic counterexample does not recompute the author's particular matrices, negate the observed detection results or claim a reproduced failure of the case implementation.

## Survey consequence and remaining work

B07 gains a concrete positive case for specifying and exercising transitions after a lifecycle event, together with an observed miss under ordinary coverage. B04/B08 gain an explicit distinction between resetting, retaining, controlling and observing state. B12 must keep generated mutants, natural defects, equivalent-mutant policies, dependent repairs, input counts and engineering effort separate. The same histories and observers can change what a fault count means.

For Nu and interactive-software evolution, these are prior method obligations: identify the trigger, state ownership, observation horizon, pending work and valid external outcomes before treating replay/checkpoints as an oracle. The evidence does not establish a Nu implementation, a compiler-diagnostic mechanism effect, or complete coverage of new behavior. It also does not justify erasing the favorable detection comparisons.

The original S221 bodies remain an edition/access task. Remaining thesis chapters are not automatically the next reading: the selected unit and integration chapters answer this consequential case question. Return to the survey's independent game/runtime and temporal-evolution frontiers, using their claim-specific gaps. No author C program, mutant, generator, Statemate model, Markov simulation, proof assistant or candidate experiment is executed; own work is reading, source bookkeeping and elementary arithmetic/symbolic reasoning.
