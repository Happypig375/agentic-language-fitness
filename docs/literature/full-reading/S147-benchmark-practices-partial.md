# S147 — What the CHAMP warning record actually contains

**Historical scope, superseded for current reading status:** the [complete final-journal reconstruction](S147-benchmark-practices.md) now covers the acquired sixteen-page PDF and additional RQ2 material. Native parent `IZE2C6FX` replaces the deleted historical `GP4BQG7X`; canonical note `2H26NKVR` was preserved by that existing merge. The following dated access record and bounded CHAMP analysis are retained, not asserted as current access limitations.

**Partial reading, 2026-10-01 HKT; no full-work credit.** Diego Costa, Cor-Paul Bezemer, Philipp Leitner and Artur Andrzejak, *What's Wrong with My Benchmark Results? Studying Bad Practices in JMH Benchmarks*, IEEE TSE 47(7), 1452–1467 (2021; online 2019), [DOI 10.1109/TSE.2019.2925345](https://doi.org/10.1109/TSE.2019.2925345). Native record `GP4BQG7X`, note `2H26NKVR` preceded intended reading. The live question is whether this later study establishes a failure in [S143's](S143-champ-immutable-collections.md) published measurements.

## Access and bounded paper evidence

The [author manuscript](https://asgaard.ece.ualberta.ca/papers/Journal/TSE_2019_Costa_Whats_Wrong_With_My_Benchmark_Results_Studying_Bad_Practices_in_JMH_Benchmarks.pdf) is indexed as seventeen pages. Direct HTTPS requests fail with a connection reset using both Python and Windows curl; HTTP also resets after waiting. Cached web text is available, but page screenshots fail. No local PDF, byte hash, native PDF attachment or equivalence to the sixteen-page final issue is claimed. The coauthor publication page confirms the DOI but supplies no alternate PDF; an older first-author site returns 404.

Selected text covers acquisition/selection methods on manuscript page 5, Table 2 on page 6, static rules on page 7 and the artifact row in Table 6 on page 8, plus opening, execution, false-positive and bibliography fragments. The study screens 123 buildable projects selected from a larger GitHub set. The artifact row lists 213 benchmark methods and 25 affected methods, with practice-instance counts 4/1/2/12/3 for RETU/LOOP/FINAL/INVO/FORK. These are different counting units. Crucially, section 3.2.2 explicitly excludes `oopsla15-artifact` from the subsequent performance-impact experiment. The paper's impact findings on other projects do not constitute a CHAMP rerun. No broader prevalence or repair-effect conclusion is reconstructed from this partial reading.

## Released evidence behind that row

The linked [author study repository](https://github.com/DiegoEliasCosta/badJMHpractices-study/tree/9500e3ae0b65b31a8baf6385989005bb9dc4e469) resolves to commit `9500e3ae0b65b31a8baf6385989005bb9dc4e469`, 1 April 2019. The untruncated tree has 2,165 entries. The root and RQ1 READMEs were read completely; the occurrence CSV's schema and target row were inspected; the target XML's warning records were parsed; seven of 36 notebook cells were read for extraction, category mapping and export. No notebook, static analyzer, build or benchmark was executed. The README still calls the paper under revision, so publication/artifact correspondence remains bounded.

The occurrence CSV contains 123 rows and reproduces the target row's 213 methods and five practice counts. The raw XML contains 271 entries, including method detections and several warning types that the notebook does not export. Counting every XML entry as a bad practice would therefore be incorrect.

The 213 detected methods comprise **101 JMH sample methods, 90 JMH internal-benchmark methods, eleven project map methods, ten project set methods and one project dominator method**. The exported practice types give 22 instances:

- Four RETU entries concern intentionally problematic JMH sample methods, not the CHAMP map/set operations.
- The one LOOP entry is a JMH unsafe-loop example. All three FORK entries belong to the JMH forking example.
- All twelve INVO entries occur in JMH sample/internal-benchmark classes.
- Of two FINAL entries, one is the JMH constant-folding example; the other flags the dominator harness's constant dataset-file-name string.

Thus **21 of these 22 exported practice instances are in bundled JMH classes**. This does not reconstruct the paper's separate 25 affected-method count, but it prevents interpreting the 22 instances as 22 defects in the paper's collection workloads. The selected notebook filters generated classes but does not exclude these bundled JMH classes. Its RETU mapping combines dead stores and ignored static returns; it does not include the XML's additional unsunk-variable warnings.

Three such additional XML warnings point to the project's map/set iterator methods. S143's independently inspected source consumes yielded values through a blackhole. A flagged iterator variable is not itself proof that the measured iteration was eliminated. Likewise, the dataset-file-name field is used during setup, not as the numeric benchmarked value. These are static scope observations, not executed proof that the analyzer is wrong or that the original timings are correct. The launch scripts request one fork; the debug `main` methods' settings are another distinct context.

The XML is 2,021,883 bytes, SHA-256 `a739c3efa46f27791e26930fd64845c05487384ea9942209b6f25738c9d7dfb3`. The CSV is 3,344 bytes, SHA-256 `ebeab32e2543ec0a8abbf8c0a388e5cf68c6f9adeaddcb605c3483cd7ae302eb`. The inspected notebook is 16,982 bytes, SHA-256 `ed47ab748b1fc15749419671efce53ca1120f6b5b7bf50b87bbc7a020f5f86cb`. All paths are under the pinned repository's `RQ1. Occurrences of bad JMH practices/` directory. Local manifests retain the README hashes and exact acquisition URLs.

## Disposition

This resolves the immediate citation implication: the study identifies an artifact-level static screen, with substantial bundled-library scope, and explicitly does not measure CHAMP's alleged impact. It cannot be cited as a demonstrated invalidation of S143's results. [S146](S146-jvm-benchmark-context.md) supplies a separate, fully reconstructed context-sensitivity concern. Neither qualification certifies S143's runtime claims beyond its stated setting.

Full S147 methods, rule validation, the six-project impact data and final-edition correspondence remain unread/unresolved. Promote those when the background synthesis needs their broader prevalence or repair-effect estimates; the targeted CHAMP dependency does not require pretending that the whole study has been read. B06/B12 and all experimental holds remain open.
