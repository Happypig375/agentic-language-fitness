# S194 — The original external modularity replication

**Complete publication reading, 2026-10-02 HKT.** J. Daly, A. Brooks, J. Miller, M. Roper and M. Wood, *Verification of Results in Software Maintenance Through External Replication*, ICSM 1994, pp.50–57, DOI [10.1109/ICSM.1994.336790](https://doi.org/10.1109/ICSM.1994.336790). Reader: the main Codex AI session. All **eight pages**, **three figures**, **two tables**, **five numbered footnotes** and **fifteen references** were consumed; every page was visually checked because OCR damages words, column order and some numerical cells. The affiliation footnote was also read. No appendix is present. This is reconstruction and a descriptive check of printed numbers, not a new experiment or execution of the authors' induction system.

Existing native parent `SEQFXFNP`, note `E3UE9XJB` and user PDF `I2BDS3CM` preceded reading. Fresh read-back verifies parent4598/note4730/PDF4709 and memberships `PKLXQNEE`, `74BHFBRZ`, `MBYQJXUF`. File: **638,283 bytes**, SHA-256 **`78ed6d60aca59c5487fedf8d121cb8bdae300e7e3b9a3a192d2213e8c45c083f`**. Its eight printed pages match the registered50–57 range. No acquisition URL is recorded on the user attachment. Copyrighted pages and extraction files remain outside Git.

## Finding and lineage

The replication retains a **modular-faster mean**, approximately **48.0 versus59.1 minutes**, but does not reproduce the original study's large, statistically significant difference of **19.3 versus85.9 minutes**. This is a smaller, inconclusive comparison, not an equivalence result or proof that monolithic code is superior. The authors' subsequent ability/strategy explanations are exploratory.

[S90](S90-modularity-program-modifiability.md) is the original Korson/Vaishnavi study. [S193](S193-replication-modularity-account.md) is a later retrospective account of this same replication. S194 is its original conference report, **not another independent empirical case**. The fuller EFoCS-4-94 report, the Daly dissertation and Korson's dissertation/materials remain distinct unread/access-limited dependencies. Full conference-paper coverage does not establish correspondence with those more detailed sources.

## What was assigned and measured — pp.50–52

The point-of-sale inventory program has an approximately1,000-line modular version and1,400-line monolithic version constructed by replacing procedure/function calls with their bodies. Participants make functionally equivalent perfective changes intended to benefit from localized information hiding. This is a particular transformation and task, not a comparison of every architecture convention. The replicators retained an influential comment present only in the modular program to avoid changing the original treatment; details of that comment and their information-hiding concerns are deferred to the report. Explanatory footnotes for American terms are among the local adaptations.

Twenty-three unpaid volunteers from Strathclyde computer science took part: five second-year students, two third-year students, nine final-year students, four research students and three research assistants. The stated eligibility follows the original study's Pascal/IBM-PC/programming-experience criteria. Assignment is reported as random, without a detailed randomization procedure. Participants worked in one laboratory with alternating program versions, knew different versions existed, and were told some might finish sooner; the experiment's substantive hypothesis was withheld.

Only **seventeen completers** supply the published timing analysis: **eight modular and nine monolithic**. **Six participants, three per group, failed to finish within four hours** and were not asked to continue because they were unpaid, unlike Korson's participants. Those failures remain part of the observation record. Equal numbers of noncompleters do not make a completer-only timing comparison an unconditional effect for all assigned participants.

The procedure is a familiarization pretest, a10–15-minute break, the experiment, then personal details/debriefing. Before timed source work, participants read instructions and could ask questions. The four imposed phases are:

1. **Think:** write proposed code changes on paper after receiving the source listing.
2. **Edit:** enter those changes into the actual program.
3. **Syntax:** remove compilation/syntax errors.
4. **Logic:** debug until the program passes the supplied standard test.

Programs are saved after editing, syntax removal and a working result. Monitors time four or five participants each. The actual test suite/instructions and six incomplete trajectories are not printed here, so their coverage and individual stopping paths cannot be reconstructed from this paper alone.

**The reported “total” is not total wall time.** Figure1 sums think+syntax+logic, omitting edit. Table2 distinguishes `result` (time to complete the task) from `total_time` (`result−edit`). Thus neither preparation nor editing should silently be included in the48/59-minute comparison. Phase overlap also means the individual phase labels are not clean mechanism measurements.

## Preserve the observed timing result — pp.52–55

Own transcription of all seventeen rows in Figures1/3, checked against the rendered pages, reproduces the means and the Table1 sample standard deviations. These are checks of the **printed completer data**, not acquisition of original raw files or independent execution.

| Measure, minutes | Modular, n=8 | Monolithic, n=9 |
| --- | ---: | ---: |
| Think mean | 27.125 | 35.000 |
| Syntax mean | 10.750 | 7.333 |
| Logic mean | 10.125 | 16.778 |
| Sum excluding edit | **48.000** | **59.111** |
| Sample standard deviation of that sum | 25.445 | 26.970 |
| Pretest sum mean | 38.500 | 23.222 |

The modular mean is **18.80% lower** than the monolithic mean in this retained sample; the syntax phase goes in the other direction. Our pooled two-sample arithmetic yields **t≈−0.8705, df=15**. We do not recompute exact p-values or a corrected causal estimate. The paper reports the result as nonsignificant, printing `p<.4`, versus the original's `p<.0001`; these are the authors' reported bounds, not an exact p=.4 or a posterior probability of the hypothesis. Wide variation and this small selected sample limit what the difference can resolve.

The paper's published pretest rows confirm that all nine monolithic completers fall within the fastest twelve pretest ranks. The authors interpret this as a possible ability imbalance despite random assignment. The pretest was designed for familiarization, and instructions/reading strategy also influenced its times. This observed ranking is therefore not a validated ability scale, evidence that random assignment was absent, or proof that ability adjustment would recover Korson's large effect. S90's unstable preliminary-task rankings remain relevant contrary evidence.

## What the exploratory analysis actually does — pp.53–56

After the unexpected result, the researchers use IRIS rule induction over nineteen variables and corresponding pretest timings. They bin timing variables into three groups by choosing two histogram split points, group questionnaire answers by similar meaning, and add variables derived from saved programs. The system can take each database variable as an outcome. This is exploratory, data-dependent analysis rather than a prespecified confirmatory adjustment or independent validation set.

Two selected rules relate pretest/experiment times and relate missed changes during think to prolonged syntax/logic phases. Four participants with high syntax time made semantic corrections during that phase despite instructions; three were modular participants whose syntax times sum to73minutes. This is evidence that the imposed phase categories overlap in practice. It does not identify a pure effect of syntax checking or establish that these participants should be removed.

Saved-program comparisons show only five participants changed code between the syntax and final working versions. Among those without such changes, logic times nevertheless vary from1–20minutes for modular and1–5 for monolithic participants. The authors consider three alternative test procedures with demonstrated minimum durations **1min15s,55s and2min30s**, plus rereading time. They suggest having a monitor test code to reduce variation. Those investigator timings are not the original study's unpublished procedure timings.

They also consider a **hypothetical replacement** of such participants' logic times by one minute, reporting that the result still would not be significant (`p<.2594`). This is a sensitivity illustration conditioned on post-assignment code-change behavior, not an observed alternative protocol, a preregistered correction or an unbiased mechanism estimate. The paper does not print enough per-person difference flags to independently reconstruct this calculation without the fuller report/materials.

Strategy observations are equally concrete but limited. The two fastest monolithic finishers say they did not understand the program and did not need to understand it for these changes. The two slowest modular finishers attempted to follow control flow. Two monolithic participants introduced procedures. Other participants, including a noncompleter, objected to the forced phases and wanted to compile/run/explore before editing. These observations support studying how people solve the task; self-reported understanding is not a measured comprehension score. Efficient local editing and reorganization are valid behavior, not reasons to discard a successful result.

## Consequence for the survey

S194 closes the original-paper method gap behind S193: allocation is reported random; six failures are excluded from timing; the endpoint is standard-test completion; editing is subtracted; phase boundaries can shift work; and ability/strategy rules are post hoc. It preserves both the original positive study and the replication's smaller, inconclusive difference. It does not show that modularity has no benefit, that understanding code is generally unnecessary, or that a preferred adjusted result should replace the observations.

For B01/B10, source assignment, intermediate strategy, completion, missingness and measured time are separate. A task may allow fast local repair without broad understanding, while imposed work phases and test interaction alter measured burden. For the current Nu/ISE question, neither line-count transformation nor this human Pascal task establishes a language, model-context, runtime or D1 source-convention effect. The proposed agent study must preserve safe reorganization and correct catch-alls if later authorized; no construction follows from this reading.

The report/thesis/source/test dependencies remain specific access/reading gaps. They need follow-up when the influential comment, original test coverage or complete trajectories would change a live claim. The next accessible consequential method is **S200**, the positive concern-scattering/defect study, to balance the now-reconstructed S120/S195/S196 critique. S202's maintainer method and independent runtime/oracle/type frontiers remain open. No new worker or experiment is authorized.
