# S135 — Testing the guarantees of pattern-match analyzers

**Complete publisher reading, 2026-10-01 HKT; passive artifact reconstruction, no compiler or author-script execution.** Cyril Flurin Moser, Thodoris Sotiropoulos, Chengyu Zhang and Zhendong Su, *Validating Soundness and Completeness in Pattern-Match Coverage Analyzers*, PACMPL 9/OOPSLA2, article 393 (2025), DOI [10.1145/3763171](https://doi.org/10.1145/3763171).

## Edition and coverage

Existing Zotero parent `7QEFTVJC` preceded reading. The publisher attachment `8ZSHTHAG` has 27 pages and 1,147,420 bytes, SHA-256 `f8945a033225a16eed55176fbebb89cb31608606b12b6808fd5c3183733e3ef3`. All 27 pages, nine figures, three numbered tables with their subparts, Algorithm 1, three theorem arguments and all 38 references were read. Every figure/table, the algorithm and additional formal-definition pages were visually checked. Full note `XNFVLJJZ` records this edition.

Author attachment `A578XB75` remains a separate 27-page, 995,673-byte copy, SHA-256 `54edb83b7df551127d30e08729a04c00ecadbb361bd81e287b6127f43f11ef0d`; its previous opening/partial-fourth-page reading does not certify full equivalence. Repository DOI `10.3929/ethz-c-000786323` is another locator for the same titled work, not an independent study. Available, Reusable and Results Reproduced badges on the publisher cover describe artifact-evaluation status; they are not this agent's reproduction.

The [Zenodo artifact](https://doi.org/10.5281/zenodo.16909625), dated 2025-08-20, was acquired through its public API after the web-page route failed. Native ZIP attachment `PQADFKSA` contains `ikaros-eval.zip`, 539,019 bytes, SHA-256 `30f97613b518a03d5e48ca205c1e4218f0f9be71496592d04b79c4a3ef2e55cb`; the repository MD5 `b3230063c20a1936f302a55e7d02861e` also matches. Its 90 file entries total 1,848,574 uncompressed bytes. The exact archive, selected source scope and independent descriptive reconstruction remain local; no publisher body or archive is committed.

## Method and assumptions

Ikaros generates algebraic data types, constructs a graph of constructor/type-parameter constraints, selects an instantiated type and produces pattern-matching expressions in a shared IR. Separate backends lower this IR into Scala, Java or Haskell. This is an analyzer-testing method, distinct from S119's coverage algorithm and S114/S136's program-level safety analyses.

Refinement-based generation (RefPG) starts with a wildcard and repeatedly partitions it into mutually disjoint patterns with the same coverage. Under the stated inhabitation model, retaining the partition yields an exhaustive match; deleting a nonempty member yields an inexhaustive match. Disjointness also supplies a check against falsely reported redundancy. The paper gives structural/refinement arguments, not a mechanized proof of the entire generator and its backends.

Random generation (RngPG) samples bounded-depth patterns from constructor-specific pools and allows combinations outside RefPG's disjoint cross-product structure. It asks an SMT solver whether a valid value exists outside all selected patterns. SAT supplies a missing-case witness; UNSAT supports exhaustiveness under the encoding. GADT constructor restrictions need additional validity predicates because ordinary SMT algebraic datatypes do not encode those restrictions automatically. The solver and translation are trusted components; the authors report encountering and obtaining a fix for one solver segmentation fault.

This is a restricted semantic model. The generator excludes guards, pattern synonyms, nonlinear patterns, strict fields, several forms of polymorphism/variance and other language-specific features. Its relaxed inhabitation permits constructor arguments supplied only by null or bottom-like values. The authors explicitly show that applying the same oracle to strict Haskell fields would produce false positives. Empty matches are excluded by design. Extending a backend's syntax does not automatically validate its semantics or oracle.

The oracle primarily concerns exhaustiveness. RefPG also detects false-positive redundancy reports; RngPG does not provide a general complete redundancy oracle. Compiler acceptance, successful matching, termination, intended output and future-domain obligations remain different properties. A compiler's intentionally approximate warning policy must also be distinguished from a violated documented guarantee.

## What the evaluation establishes

The opportunistic search developed Ikaros and tested changing stable compiler releases over nine months. Six scheduled configurations combined three compilers with two generation methods, but the tool did not run continuously; RngPG was introduced after three months. Manual triage and a tailored reducer supported reports, with a reported mean size reduction of 70%. No fixed total exposure denominator or representative sample of ordinary applications is supplied.

The paper and all sixteen released bug metadata records agree on the reported outcomes:

| Outcome at publication | Scala | Java | GHC |
| --- | --- | --- | --- |
| Missing exhaustiveness warning | 7 | 0 | 0 |
| Incorrect exhaustiveness rejection | 0 | 4 | 0 |
| Incorrect redundancy warning | 4 | 0 | 0 |
| Compilation performance regression | 1 | 0 | 0 |
| Fixed / confirmed-only / unconfirmed / won't fix | 10 / 2 / 0 / 0 | 2 / 0 / 1 / 1 | 0 / 0 / 0 / 0 |

These sixteen reported records are not sixteen independently established root causes. Metadata includes ten GADT cases, two other polymorphic cases, four ordinary ADT cases, six null-related cases and two constant-pattern cases; the last categories overlap. The publisher's row order differs from the artifact's JSON order, while these aggregate feature counts agree. GHC's zero discoveries are a useful observed result under this generator and exposure, not proof of complete reliability or a language ranking.

Three primary Scala issue bodies and all six associated comments were read through the ordinary GitHub API. [Issue 22590](https://github.com/scala/scala3/issues/22590) corroborates the constant-pattern missed warning and closure for the 3.7.0 milestone. [Issue 20132](https://github.com/scala/scala3/issues/20132) corroborates runtime MatchError and distinguishes it from a compiler crash; its comments identify potentially related reports. [PR 21000](https://github.com/scala/scala3/pull/21000), merged 2024-08-05, closes eight of the artifact's Scala reports together. Its complete description and 22-file list were inspected, not all patches. Shared repair does not establish eight independent causes or justify silently collapsing them to one.

[Issue 23407](https://github.com/scala/scala3/issues/23407) supplies the reachable-null example and conflicting warning after branch removal. It remained open in the retrieved API state, and its later discussion questions whether null-only inhabitants were intentionally ignored. This preserves a genuine diagnostic/behavior mismatch without claiming universal agreement on the desired warning policy. The Java won't-fix issue `JDK-8337522` returned 403; an exact-ID search returned no result. Its maintainer rationale remains unverified. Four released records have no report URL. The entire sixteen-case fix history was not independently audited.

## Released data: corroboration and limits

The archive supplies two Scala CSV-like `.stats` files with 10,000 rows each and three saved trigger-time series. Independent standard-library calculations read all rows and statically inspected the serialized numeric timestamps; no pickle objects or author programs were executed.

The trigger series recover **3,642 Scala plus 86 Java RngPG triggers, versus 36 Scala RefPG triggers**, matching Table 1c. First recorded triggers occur at 5.595 seconds, 388.844 seconds and 2,027.283 seconds respectively. This strongly favors RngPG on these recorded streams. Triggers can repeat the same defect; these are not thousands of distinct bugs, independent replications or a direct diversity-effect estimate. Missing streams are initialized to zero by the plotting script, so their absent raw files are not independently reconstructed zero-event histories.

The timestamp extraction script derives elapsed seconds from file creation/change time relative to a run-end marker. Its plotting script labels the axis hours without converting those values. The paper's twelve-hour figure and the saved event totals remain interpretable after explicit conversion; execution of the released plotting command was not verified. Repeated-run uncertainty, complete generated-input denominators and event-to-unique-defect mapping are absent from these series.

The two released statistics files confirm 7,042 SAT, 2,517 UNSAT and 441 Unknown results for RngPG, matching the paper's rounded 70.4%, 25.2% and 4.4%. Unknown cases are not proved correct or incorrect. Source inspection confirms that they are skipped before compiler comparison. Multiple sampled matches can reuse one generated type context, so rows are not automatically independent type-system challenges.

Most Table 2b summaries agree: mean 4.4033 declaration nodes, 2.8987 constructors and 7.71765 patterns round to 4, 3 and 8. The mean polymorphic-node count is **2.4088, rounding to 2**, as in the artifact README, whereas the publisher prints 3. The apparent conflict between a two-ADT cap and four mean declaration nodes is resolved by the source: the latter includes constructor representations, while base ADTs remain one or two. The statistics' “GADTs” field also counts constrained constructor nodes, not independent whole-program ADTs.

The released pattern-bin counts are:

| Patterns per match | RefPG | RngPG |
| --- | --- | --- |
| 1–5 | 8,197 | 8,303 |
| 6–10 | 838 | 997 |
| 11–20 | 464 | 464 |
| 21–50 | 266 | 204 |
| 51–100 | 115 | 27 |
| Over 100 | 120 | 5 |

RefPG has the larger mean and tail, but RngPG also generates matches above fifty patterns, contrary to the paper's categorical wording. The artifact README warns that its Figure 8 differs from the submitted paper. No replacement historical corpus is invented.

Table 3 reports generation in microseconds, compilation in milliseconds and SMT time in milliseconds. Its SMT column headings put the smaller values under “without timeout,” opposite the prose and artifact README. More materially, the analysis script's “with timeout” value is a **post hoc mean over solver durations below 50,000 microseconds**, while the implementation sets a 500-millisecond timeout. This is not a paired intervention measuring the complete resource cost of imposing versus removing a timeout. The saved Scala corpus gives 35.688 milliseconds over all solver results and 8.992 milliseconds over the 9,377 results below fifty milliseconds; these do not reproduce the publisher's separate 43.5/9.6 pair. Java/GHC timing CSVs for the reported 5,000-plus-5,000-per-language performance experiment are absent from this archive.

Source also shows that `processing_time` includes file/batch handling and compiler invocations when a batch fills; it is not intrinsically an isolated per-program compilation timer. The artifact's performance instructions request batch size one, while its supplied characterization corpus has different timing values. Generalization to ordinary build cost or maintenance effort is unwarranted. The positive trigger-finding result and real fixes do not depend on resolving every timing-table discrepancy.

## Artifact scope and transfer

Fifteen complete text files were read: both READMEs, Dockerfile, Cargo manifest, five result-processing scripts (`process_bugs`, `study-characteristics`, `study-performance`, `bug-evolution`, `pickle-bug-evolution`), `run-ikaros.sh`, Java/Scala installation scripts, both statistics structs and `typegen_args.rs`. Partial source coverage is `main.rs` lines 393–544; `programgen.rs` lines 119–199, 263–402 and 635–693; `z3checker.rs` lines 1–143. Remaining solver/translation/reducer implementations and all generated test bodies were not audited.

The code confirms the 500-millisecond solver bound, separate Unknown handling, batch timing, declaration-count definitions and Java preprocessing that removes compiler-reported dominated cases. The last step is another language-specific trust boundary; no new defect in it is established by this inspection. Formula construction and source lowering still need correspondence evidence before an unconditional oracle claim.

Sixty-seven embedded Ikaros files match Git blob hashes at repository revision `4a06d7d7c537acba9bedbda6beb523819e6d4a26` (2026-03-27); the two unmatched entries among the archive's 69 embedded files are the README and a submodule `.git` pointer. Hash equality binds those bytes, not their correctness or a complete source review. The Dockerfile uses Ubuntu22.04 rather than the paper's reported Ubuntu20.04 host and installs a moving latest GHC; it does not recreate a frozen nine-month compiler history. No container, compiler, solver, package installation or author test was run.

G08 has one incoming edge and a low-coverage flag. SC51 identifies `10.1145/3808320`, *Enumerating Ill-Typed Programs for Testing Type Analyzers*, as a conditional follow-up on construction-based negative oracles, without full-method credit. Noisy SC52/SC53 prefixes were screened and reformulated to the exact phrase in SC54, which returns two locators for S135. Neither those prefixes nor the narrow two-result query exhaust the field. Set-constraint safety, OCaml impossibility/precision, LF coverage and grammar/algebraic testing remain conditional routes alongside the already acquired S136.

**Unique:** unconfirmed; analyzer validation and generated positive/negative oracles are existing methods. **Valuable:** concrete missed warnings, misleading diagnostics, repairs and faster trigger discovery are supported within scope; their frequency or net maintenance cost in Nu/F# agent work remains unmeasured. **Scientifically valid:** full methods and selected released evidence are reconstructed, with explicit trust boundaries, dependent reports, incomplete exposure and timing limits. For D1, diagnostic opportunity must remain separate from independently scored old/new behavior. Continue S136's higher-order safety comparison and extension/practice, retaining the broader survey priorities and all experimental holds.
