# S147 — Benchmark warnings, changed measurements and intended work

**Complete journal reading, 2026-10-01 HKT.** Diego Costa, Cor-Paul Bezemer, Philipp Leitner and Artur Andrzejak, *What's Wrong with My Benchmark Results? Studying Bad Practices in JMH Benchmarks*, IEEE TSE 47(7), 1452–1467, July 2021; online 27 June 2019, [DOI 10.1109/TSE.2019.2925345](https://doi.org/10.1109/TSE.2019.2925345). This extends the [earlier CHAMP-specific reconstruction](S147-benchmark-practices-partial.md), whose artifact analysis remains valid within its stated bounds.

## Identity and coverage

The existing live Zotero parent is **`IZE2C6FX`**, PDF **`D26VZPFG`**, canonical note **`2H26NKVR`**. Native inspection found the historical parent `GP4BQG7X` deleted and explicitly replaced by the live record; its original note is already under that replacement. No duplicate was created or deleted record restored. The dated acquisition note `8CFNJE5Z` remains history. Record, attachment and edition were verified before body reading.

The final publisher PDF has **16 pages, 1,487,081 bytes**, SHA-256 **`00c3ba4c4a911122507d4c98549dce1f0ea08417d5bca8e331c6198e6968f1df`**. All sixteen pages were read and visually inspected, including ten figures, ten tables, eight listings, seven URL footnotes, 44 references and the closing material. The previously cached seventeen-page author manuscript was only partially read; whole-edition equivalence is not asserted. The journal now governs the paper-level reconstruction.

## Mechanisms and sampling units

The study asks whether five JMH coding/configuration practices occur in open-source projects and alter benchmark measurements. It does not measure application improvements or software-maintenance gains. An invocation, an iteration, a fork/trial, a parameterized benchmark instance, a benchmark method and a flagged practice are distinct units.

| Rule | Possible measurement failure | Qualification established by the method |
| --- | --- | --- |
| RETU | An unused result permits dead-code elimination | Consuming the result can preserve intended work; an assertion/exception path or intentionally irrelevant value can make a static warning inappropriate |
| LOOP | Accumulating results in a benchmark loop permits unrolling/merged work | A blackhole can separate intended operations; a real accumulation workload should not automatically be rewritten |
| FINAL | Final primitive state permits constant folding | The constant's use and the intended workload matter; setup-only constants can be irrelevant |
| INVO | Per-invocation setup/teardown adds harness/timestamp overhead | Expensive or semantically necessary per-invocation setup cannot simply be moved to the iteration boundary |
| FORK | Zero forks reuse profiling state and can omit fork-specific options | Debugging configuration and command-line overrides are legitimate contexts; the annotation alone does not establish the production measurement configuration |

SpotJMHBugs operates on bytecode through SpotBugs and restricts analysis to classes containing benchmark methods. The unused-value analysis tracks dependencies on values stored in fields, returned or consumed by a blackhole. Calls outside those classes and runtime compiler transformations limit what it can recognize. The manual impact sample exposes false positives, but does not establish general detector recall.

The 2017 GitHub selection starts with **839 projects**, removes forks to leave **506**, and retains **123** that build with the stated limited Maven/Gradle intervention. Thirty-five have at least one detected practice; among 49 projects with at least ten benchmarks, 25 do. The **331 detected instances** comprise RETU 89, LOOP 128, FINAL 25, INVO 82 and FORK seven. This is a prevalence screen of selected buildable repositories, not a population estimate of confirmed faults.

The performance study selects the most-starred eligible projects within each practice. It explicitly excludes `oopsla15-artifact` and `benchmark-arraycopy` from FORK impact testing. Across six selected projects, **112 initial flags minus 19 rejected flags = 93 accepted practice instances**, mapped to **105 benchmark methods**, with thirteen separately fixed versions. These different units explain the 112/93/105 totals; they are not interchangeable denominators. Table 7 gives four rejected LOOP instances, while its discussion says five; the printed total of nineteen uses four.

## Performance comparison and actual findings

The original configurations are retained, runs alternate original/fixed versions, and each version is repeated five times. The reported median is 780 counters per parameterized instance, with a range of 100–14,400. The platform is a six-core E5-1660, 64 GB RAM, Linux 3.16.0-53 and 64-bit HotSpot JDK 1.8.0_65. These iteration counters do not constitute hundreds of independent projects or workloads.

For non-intrusive fixes, the paper uses a Wilcoxon comparison at **alpha .01**, plus non-negligible Cliff's delta. A benchmark counts as impacted if **any** parameterized instance meets both criteria; its reported effect size is the largest absolute instance effect. No multiplicity correction is described. A large distributional effect need not be a large absolute time difference.

For four intrusive INVO fixes, setup code is moved **inside the timed method**, retaining fields to avoid another escape-analysis change. This changes the measurement boundary. The study separately calls a benchmark impacted when all its instances are comparable or faster despite timing that additional work. That supports a harness-overhead concern; it does not identify an uncontaminated application-kernel time or make the two methods' estimands identical.

| Final-paper category | Benchmarks | Impacted | What the evidence supports |
| --- | ---: | ---: | --- |
| RETU | 43 | 15 | Consuming previously ignored results can materially change measurements; one reported logging example becomes about 32% slower |
| LOOP | 25 | 23 | Separating loop operations changes many selected measurements; reported median slowdown is about 22%, with much larger individual cases |
| FINAL | 7 | 5 | Some constant-folding-related changes are measurable; four logging effects are small |
| INVO, non-intrusive | 21 | 20 | Moving suitable setup out of the invocation path can sharply reduce measured cost |
| FORK | 5 | 5 | Selected configurations are sensitive to process/profile context |
| INVO, intrusive | 4 | 3 | Three cases meet the distinct overhead comparison criterion |
| **Arithmetic total** | **105** | **71** | **Tables 8–9 sum to 71; the introduction says 73. The discrepancy is unresolved.** |

Table 8 also prints **57.1%** beside FINAL's five of seven; the actual fraction is **71.4%**, consistent with the discussion's rounded 71%. These inconsistencies qualify aggregate reporting without erasing the concrete positive and null comparisons. In particular, a slower corrected benchmark can be a more faithful measurement rather than a slower application.

## Released artifact: a revision boundary, not a reproduction

The [author repository](https://github.com/DiegoEliasCosta/badJMHpractices-study/tree/9500e3ae0b65b31a8baf6385989005bb9dc4e469) is pinned to **`9500e3ae0b65b31a8baf6385989005bb9dc4e469`**, 1 April 2019. Its README describes a paper under revision. The older RQ1/CHAMP inspection is preserved in the partial note rather than repeated as new evidence.

For RQ2, this continuation read all three READMEs, all eleven source cells of `summarize-results.ipynb`, and six complete Python files: `analyze_bench.py`, `batch-analysis.py`, `jmh_parser.py`, `utils.py`, `analysis/wilcoxon.py` and `analysis/cliffsdelta.py`. Stored notebook output was only partly inspected. Git blob identities and SHA-256 were verified on all fourteen newly fetched files. No author script, notebook, build or benchmark was executed.

Our own parsing groups the **343 summary rows** by project, practice, package, class and method. There are **111 method/practice groups**, including six Netty `SETUP` groups with blank significance/effect fields. The remaining **105 groups** yield **72** with at least one stored significant/non-negligible instance. The category counts are RETU 15/43, LOOP 23/25, FINA 5/7, INVO 24/25 and FORK 5/5. Netty's INVO group contains sixteen methods, whereas the final article distinguishes twelve non-intrusive and four intrusive methods. Its six separate SETUP rows also do not match the final article's four-case intrusive account. Thus this CSV cannot silently settle the final article's 71-versus-73 discrepancy. Stored flags are used as recorded; their statistical tests were not recomputed.

The inspected analysis source explicitly removes warm-up rows, then independently filters each version to absolute within-instance z-scores below three. It inner-joins retained rows by benchmark identity, parameters, fork, iteration and trial, and passes the resulting paired vectors to `scipy.stats.wilcoxon`. Its **alpha is .001**, unlike the paper's .01. Pooling iteration counters and joining ordinal counters need an appropriate dependence/pairing justification; source inspection alone does not establish it. Independent filtering also determines which paired observations survive. This is a concrete discrepancy in the pinned release, not proof that the final paper used precisely that release.

The 414-row `statistical_tests.csv` was inspected only for schema and an initial record; it was not reconstructed as another complete analysis. A warm-up label in that exported record is not evidence that the inspected analysis includes warm-ups. Both `raw-results.csv` files fetched from the repository are **Git LFS pointers**, not their 61,679,167- and 109,866,855-byte payloads. Those payloads remain unacquired/unread. No raw-data reproduction or revised significance result is claimed.

| Newly inspected artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `results/summarized-results.csv` | 72,580 | `671eb0ca22f0959845cf7c63b0725389f1f548546d623bf62f58a928601e1357` |
| `results/statistical_tests.csv`, schema/initial-record only | 157,967 | `7cc62e07cee11e68c6866f22191bf4d2d0a896895c041c82117852a3a2b96ecd` |
| `scripts/notebooks/summarize-results.ipynb` | 13,348 | `d4a94cb352aeda0c98094c1f85ab58e91692b4acd5994cba9ccbc7f49149488f` |
| `scripts/analyze_bench.py` | 8,819 | `448714e9c1cf4f9dda7ff8300ba8baca5bad3339919b90e2bf14b22cc40b4cfc` |
| `scripts/analysis/wilcoxon.py` | 379 | `b43cc0f8bc55a52e7680a40faf489b989ed61443f4bb3fc48cc12bde1eb3832f` |

These paths are relative to `RQ2. Impact of bad JMH practices/`; local manifests retain every URL, remaining hash and LFS object identity. Copyrighted bodies/data and extraction dumps remain outside Git.

## Developer validation and disposition

The paper reports seven PRs containing 57 benchmark changes, selected for large observed effects: six accepted and one pgjdbc proposal rejected. The latter used zero forks deliberately for IDE debugging and described different operational configuration. A Druid response removed unused benchmarks instead of adopting the proposed change unchanged. Acceptance is useful external feedback on selected cases, not an unbiased precision estimate, a measured productivity benefit or proof that every timing alteration corrects a production defect. The original pgjdbc/Druid threads were not independently read: web opens failed and the direct GitHub API attempt hit an anonymous rate limit.

For **B06/B12**, distinguish a static warning, intended workload, measured counter, accepted repair and application outcome. S147 supplies real examples of changed measurements and concrete method safeguards, while preserving legitimate configurations and unaffected cases. For [S143 CHAMP](S143-champ-immutable-collections.md), the earlier result still holds: most exported flags concern bundled JMH classes, and CHAMP was explicitly excluded from impact testing. [S146](S146-jvm-benchmark-context.md) supplies a separate context-sensitivity result. Neither paper proves a general Nu speedup, slowdown or maintenance effect.

**Remaining actions:** final-version raw-data/analysis correspondence is necessary before adopting an exact aggregate impact rate or recomputing inference; the article and pinned release alone do not resolve it. This bounded method gap does not prevent continuing the wider survey. Resume C02's uncompleted type/extensibility coverage, retaining S194's original replication access route, S184/S185 and the temporal-oracle priorities. All construction, worker and experiment holds remain.
