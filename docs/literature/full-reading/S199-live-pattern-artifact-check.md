# S199 — What the released study package permits checking

**Bounded read-only inspection, 2026-10-02 HKT**, supporting [the S199 reconstruction](S199-live-pattern-documentation.md). This is our examination of released material and our descriptive arithmetic, not a new empirical case, author-code execution or an independent rerun of the experiment.

## Identity and coverage

The [Zenodo v1.0 release](https://zenodo.org/records/10849702) has version DOI `10.5281/zenodo.10849702` and concept DOI `10.5281/zenodo.10849701`. The [GitHub v1.0 tag](https://github.com/SoftwareForHumans/DesignPatternDoc-UserStudy/tree/v1.0), verified through GitHub's API after a web-cache miss, resolves to `a81f66b6324dcf3c65b467bc9be9b07e9d08023d`. ZIP SHA-256 `6e724fe2185e9cd4a917afe3ef1810cb3a6bfcad2503c1e13ddfc3b2642fca71`, **2,713,128 bytes**, matches the downloaded bytes; its MD5 matches Zenodo's `b7d64042ddbb4912a567e9b8cc63dc94`. Native attachment `9F3DW85F` belongs to the existing S199 parent `VCVMUNHF`.

There are **42 archive entries, including 28 files**. Inventory is complete; content coverage is deliberately bounded:

| File(s) | Actual inspection |
| --- | --- |
| `README.md` | Complete text; coding of groups/variables, task preparation and XML installation instructions |
| `syntax.sps` | Complete text; tests requested and variables used; **not executed** |
| `data.csv` | All **21 rows ×28 numeric columns** parsed/checked; groups 10/11, no empty values, all per-person totals equal the six task-time sums |
| Task 1 Java, five files | All bodies: CNN, NewsChannel, Main, Channel and NewsAgency; Observer news example |
| Task 2 Java, four files | All bodies: Client, Light, RemoteControl and Command; concrete command/wiring absent |
| Task 3 Java, eight files | All bodies: six concrete classes and two abstract classes; animal factory and extension task |
| `questionnaire/controlGroup.pdf` | All **five pages text and visual** |
| `questionnaire/experimentalGroup.pdf` | All **ten pages text**; pages **2–5 visual**, including its illustrative graphics; page 10 is blank |
| `Task2/src/pattern/doc.png` | Entire prepared Command diagram visually inspected |
| `pattern_instances.xml` | Complete structural parse; selected opening/end sections and task-instance fields read, **not every schema body** |
| `answers/controlGroup.csv`, `answers/experimentalGroup.csv` | Headers and record counts only: **10×24** and **11×40**; participant response bodies/identifying fields not read |
| `DesignPatternsReferenceCard.pdf` | Two pages acquired, extracted and rendered, **body not consumed** |
| `data.sav` | Not read |

Protocol text coverage is therefore **15 pages**, visual coverage **nine pages**, separate from the main publication. Embedded PDFs were not imported as additional native attachments. Acquisition/extraction does not count as reading. The public plugin repository's README was separately read; its implementation and relation to the study build are unverified.

Hashes for independently handled components:

| Component | Bytes | SHA-256 |
| --- | ---: | --- |
| Numerical `data.csv` | 1,659 | `7ee71360312785b8d950c5ad9c5c533ecb0286aa8213c7a8d1a125a16704a504` |
| Control protocol | 2,046,982 | `906062564ed27cd6b0a007e387e41e8828a89a5d6ba1514c54f8f6c7b0781974` |
| Experimental protocol | 3,553,894 | `80ec5deb3ebb01fd130ae36cf505664e280936aecae7ca39ab26a0df1e7ed7b2` |
| Reference card, unread | 84,665 | `567fc3b2f51c752aa08242d2b97881ab6445436bcca880b11dffd2ed2fa64645` |
| XML | 12,420 | `ed473f73d9ae053d84666ae6fd8e027a46bf795573972e99c15870f8c0a3e6de` |

## What the starter artifacts add

The control and experimental protocols define three scenarios and six subtasks, with Giraffe as the factory extension. Control participants draw diagrams manually; experimental participants use the plugin. Both receive a State diagram example; the experimental instructions also illustrate the plugin with Bridge. Per-scenario form start/stop requests are distinct from the researcher's subtask timing. The control protocol includes draw.io familiarity, while the analysis CSV has five background variables. The experimental protocol adds fifteen feature-specific judgments, beyond the three final questions in the analysis table.

Task 2's prepared diagram and XML identify Command, Light/Receiver and RemoteControl/Invoker, leaving ConcreteCommand unfilled. The starter Client constructs a light and remote but never assigns a command. RemoteControl guards against a null command. A successful implementation therefore needs an appropriate command and its wiring; a structural role warning alone does not implement the behavior.

Task 3's factory tests Elephant and Lion, then returns Pig as a fallback; a separate provider recognizes the Animal factory and otherwise throws. Adding Giraffe can preserve the Pig catch-all after inserting an appropriate branch. The task does not compare alternative baseline source conventions. Eight Java files include only six concrete classes, so counting every type as a concrete class would overstate a discrepancy with the paper's size description.

The XML contains one project state, one accepted instance, three participants, six design-pattern schemas and twenty-four role-link elements. Its prepared participant names are simple names, while the paper describes fully qualified names. This is a version/implementation question, not evidence that the prototype fails at runtime. The README's per-IDE-profile installation path also makes study preparation explicit; a repository XML file is not automatically project-local state in every installation.

## Arithmetic and statistical-reporting check

Our local standard-library script reads the released numeric CSV and calculates group counts, sums, means, sample standard deviations and standard errors. It verifies each person's total against the six task times. The README calls `TotalTime` the entire experiment, but these values are task sums; they do not include every tutorial, setup or questionnaire activity.

For the three t-tested timing outcomes, own pooled-variance arithmetic reproduces the printed results to rounding: T21 **t=3.8162, d=1.6674**; T31 **t=3.9998, d=1.7476**; T22 **t=−0.0808, d=−0.0353**. These calculations validate transcription/interpretation of this table, not causal isolation of liveness or the randomization procedure.

For rank outcomes, we calculate the smaller Mann–Whitney U from pairwise wins/ties and use tie-adjusted rank variance with **no continuity correction**. With N=21, the printed “r” values closely track **z²/N**. For timing, own |z|/√N values are about **.753, .845 and .846**, whose squares are about **.567, .714 and .715**, corresponding to printed .57, .71 and .72. The same squared-statistic relationship holds closely for six external-access and three final-question rows; intermediate rounding accounts for small last-digit differences. Those reported values should not silently be read as the usual unsquared rank effect size.

The printed dispersion values likewise match **standard errors** rather than sample standard deviations. For example, T11 standard errors are approximately **104.66 and 26.80 seconds**, with standard deviations approximately **330.97 and 88.88**. A minor background-variable rounding discrepancy does not change that distinction.

The released SPSS syntax requests t-tests and Mann–Whitney tests, with an exact-test time limit; it contains no effect-size formula or complete normality-analysis reconstruction. It agrees with the tables on rank-testing T11/T12/T32, contrary to a prose task-list typo. We did **not** run SPSS, reconstruct exact p-values or replace the authors' inferential analysis. Printed p=.000 is rounded reporting, not a zero probability; the paper's description of p as the probability that the null is true is not adopted. For T22, half the two-sided p for a negative control-minus-experimental statistic is not the upper-tail p for a prespecified control-greater alternative. The outcome remains nonsignificant either way.

Across tasks, external accesses total **241 in ten controls** and **50 in eleven experimental participants**; experimental internal accesses total **198**. Comparing per-person external rates yields 81.14% fewer, while the paper's 89% uses T11's unnormalized 46/5 comparison. The corresponding combined event rates would be 24.10 and 22.55, but summing differently defined internal/external events does not make them equal-cost cognitive actions. Favorable external-access relocation is preserved without claiming an 89% reduction in all attention switching.

No released submitted participant code/diagrams exist to re-score: the paper explicitly says they were lost after analysis. The researcher did check them during the sessions. Both facts are necessary to describe what correctness evidence existed and what can now be verified. All copyrighted bodies, extraction dumps and uninspected response tables remain outside public Git.
