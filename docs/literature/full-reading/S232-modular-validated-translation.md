# S232 — Modular translation: type compatibility and observed semantic preservation

## Identity and actual coverage

Hanliang Zhang, Cristina David, Meng Wang, Brandon Paulsen and Daniel Kroening, *Scalable, Validated Code Translation of Entire Projects using Large Language Models*, **PACMPL 9 (PLDI), article 212, pp. 1616–1641, June 2025**, DOI [10.1145/3729315](https://doi.org/10.1145/3729315). The selected [author-hosted final PDF](https://mengwangoxf.github.io/Papers/PLDI25.pdf) has 26 pages, 1,030,845 bytes, SHA-256 **`c1ac1adb781c61350a8f6383aede6c16323b6b55f1aa9d13cd808dca129b389c`**, MD5 `2e250904774effadf65a383ddf8078b5`. Native parent/note/PDF **`MG72SGFI` / `7DNXHR3V` / `P9C5EB8M`**, collection `PKLXQNEE`, precede intentional full reading; native attachment bytes match. Crossref gives June 10, while Bristol gives June 13 as the online publication date. Neither is the December 2024 preprint date.

**Complete selected-publication reading:** all 26 text pages, nine main sections, 17 figures, two tables, three algorithms, five definitions and 63 references; no appendix. Sixteen physical pages are visually inspected: **1, 4–6, 8–17, 19–20**. Figures, prompts, formulas and tabular columns are checked against those renders. Truncated displays receive no reading credit and are recovered in smaller ranges. Reading, arithmetic and passive artifact inspection are not reproduction; no author program, compiler, model, replay or container is run.

The earlier [arXiv v1](https://arxiv.org/abs/2412.08035), dated 11 December 2024, remains **metadata/abstract coverage only**, apart from automatically exposed search fragments. Its largest-project claim is 6,600 lines/369 functions; the final paper adds a 9,766-line/780-function case. C05's 2024 metadata refers to that lineage, not another independent study. Full preprint/final equivalence is not established. Bristol identifies a version of record, but its ordinary PDF route returned HTTP 403/HTML; the author copy supplies the complete selected edition. The paper displays ACM artifact-available/functional badges; these are not our independent replication.

## Method and the preserved contract

Oxidizer translates **Go to Rust** using four connected stages (Sections 3–6). The original project's existing tests provide instrumented execution snapshots. Top-level functions/methods, types/interfaces and globals are translated in dependency order, with mutual recursion grouped. Translated dependency signatures and definitions provide context without all function bodies. The type-driven stage checks compilation and compatibility; the later semantics-driven stage repairs bodies while retaining signatures. Despite the whole-project framing, **geo and ach are selected submodules** (Section 7.1).

Feature mappings combine a source-feature trigger, an instruction and a structural check on generated Rust. Examples make the integration obligations concrete:

- Arbitrary Go global initialization maps to Rust `Lazy::new`. Recognizing that wrapper does not constrain every initializer expression or prove the same initialization time/order/effects.
- Go error returns map to `Result` with error-trait requirements. This preserves an explicit failure channel, not necessarily the original error identity/message.
- Structural interfaces map through single-method traits, trait bounds and blanket implementations. This addresses overlapping interfaces and modular translation, with generated imports, visibility and external-library mappings as further obligations.

**Type compatibility is relative to observed feasible values** (Definitions 1–3), using JSON serialization/deserialization to connect source and target representations. A nil slice may need an optional Rust vector; the signature can compile while failing this cross-language value check. Compatibility is necessary for the chosen I/O comparison, but neither a universal equivalence proof nor a comparison of typed versus untyped source. Serialization assumptions, aliases, object identity, effects and unobserved values retain separate limits.

In the paper's type-driven phase, failed compilation is repaired locally. If a compatible signature can be obtained but the body cannot compile, the method substitutes a **mock that calls the original Go implementation**; an incompatible signature can abort translation. Mocks allow other fragments to progress and count as compilation/equivalence failures in the reported statistics. A runnable mixed-language result is therefore distinct from a fully translated Rust project.

Semantic repair uses original-function calls as mocks for callees, so an error in a dependency does not automatically contaminate the current fragment's comparison. It re-queries the body with the signature fixed. This is a useful localization mechanism; passing with source callees does not alone certify the integrated all-translated call graph. The same existing-test snapshots guide repair and supply validation. No independent held-out semantic test set is described. That is a legitimate translation-validation objective under its stated contract, but cannot be imported as final-test feedback into D1.

Definition 5 compares successful outputs, extended with argument/global pre/post state. Its source-failure branch requires a target failure without equality of error value, message or post-failure state. The studied globals change only during initialization. There is no measured guarantee for arbitrary mutable global schedules, pending callbacks, external effects or live interactive-state evolution. Functions lacking usable tests are treated as failing validation; nondeterminism can also prevent equivalence even for a valid translation. **Unvalidated, detected inequivalent and uncompilable are different reasons for missing a validated success.**

## Reported outcomes and comparisons

The implementation uses Claude 3 Sonnet through Bedrock, temperature 0.2, with reported feature re-query limit 10, type-driven limit 15 and semantics-driven limit 5, chosen at diminishing returns. Table 1 gives eight projects/submodules, 15–780 functions and 314–9,766 lines. Function coverage ranges 61.9–100%; statement coverage ranges 43.2–100%. The coverage is inherited from existing tests, not a common exhaustive oracle. No independent repeated model trials, confidence intervals or paired developer-cost study are reported here.

Table 2 reports percentages by functions and by source lines. The function columns below retain all eight cases; they are the paper's rounded rates, not reconstructed integer numerators or pooled estimates.

| Benchmark | Full: compile / equivalent | Without semantic repair: equivalent | Without type checks: equivalent | Without feature mapping: compile / equivalent |
| --- | ---: | ---: | ---: | ---: |
| geo | 94 / 68 | 66 | 62 | 1 / 0 |
| ach | 96 / 65 | 64 | 62 | 5 / 0 |
| textrank | 97 / 75 | 74 | 67 | 16 / 0 |
| go-edlib | 100 / 81 | 81 | 81 | 20 / 0 |
| stats | 100 / 73 | 73 | 54 | 3 / 0 |
| gohistogram | 100 / 63 | 63 | 63 | 96 / 0 |
| gonameparts | 100 / 71 | 71 | 29 | 29 / 0 |
| checkdigit | 100 / 86 | 86 | 76 | 21 / 0 |
| Reported average | **98 / 73** | **72** | **62** | **27 / 0** |

The full condition averages 97% compilable lines and 67% equivalent lines. Without semantic repair these are 96%/66%; without type checks, 95%/60%; without feature mapping, 20%/0%. Preserve the positive results: compatibility checking improves function equivalence in **six of eight** rows, and feature-guided translation supports substantial compilable/validated output across projects. The prose's “five out of seven” characterization does not match the final eight-row table; use the table's explicit cases.

The no-feature condition removes **both feature mappings and type-compatibility checks**. It is not a pure mapping ablation. All eight translations abort during the type-driven phase; zero validated equivalence records pipeline failure, not eight completed projects whose every output was demonstrated wrong. This adverse pipeline result is real reported evidence and must not be discarded through successful-project filtering.

Semantic repair adds 15 successful functions in geo, four in ach and one in textrank; the other five cases are unchanged. The reported 2.65 extra queries averages **successful semantic repairs only**, not all attempted repair or end-to-end cost. Mocks are reported for 43 geo functions/1,236 lines, 17 ach functions/516 lines and one textrank function/65 lines. The prose's textrank percentage and several rounded function-rate/roster denominators do not transparently reconstruct integer counts from Table 1 alone. Raw matched per-function outcomes would be needed for precise pooled or cost reanalysis.

The remaining failures include wrong functions/operators and borrow-related reasoning mistakes, alongside random behavior that the snapshot oracle cannot equate. Syntactic similarity is not a substitute for behavioral preservation. Conversely, those limits do not erase the reported 73% average validated-function yield. Comparisons to earlier studies' 25.8%/29% rates use different language/project sets, rather than a common head-to-head benchmark. The claimed reduction in developer effort is attributed to **reference 29**, not measured in S232.

## Released artifact: bounded correspondence check

The paper links [Zenodo release 15242640](https://zenodo.org/records/15242640), DOI **10.5281/zenodo.15242640**, published 18 April 2025. Its API identifies one 1,279,519,934-byte `artifact.zip`, with publisher MD5 `8a211d86438985bcf34a8d334ee34e20`. **The entire archive is not acquired and that whole-file checksum is not independently verified.** Bounded HTTP 206 reads verify returned ranges; ZIP reading validates selected member CRCs. The complete outer central-directory inventory contains 2,242 entries, but the 4,340,634,112-byte nested container tar and most bodies are uninspected. Range/member manifests remain local and ignored.

Thirteen members are acquired. Nine are read completely: README, driver, results reporter, snapshot collector, options, three shell entry points and Python oracle. Four receive selected-method coverage: `algorithm.py` lines 920–941, 1139–1220 and 1408–1823; `harness.rs` 221–530; `templates.rs` 85–168; and `go_features.py` 671–718 and 789–803. Search hits elsewhere are navigation, not complete body reading. Cached LLM transcripts, credential files, benchmark bodies and the container are not read. Truncated navigation/body output is not credited beyond recovered ranges.

| Selected member under `artifact/` | Bytes | SHA-256 |
| --- | ---: | --- |
| `README` | 7,159 | `b365142ddabe3a42a236b7655078178b1a51ee40635344f3bd374ccee2dacf92` |
| `transpile/driver_go_v5.py` | 7,038 | `d3910a27271e9731fb172dee44a0489c4ecb7b6fa015b352b8dee9d8d5a5e3ea` |
| `transpile/result_table.py` | 2,094 | `78c7fa23c1f326acf8c7aeb285fcc7c08ae46987b1a07567101b4de572eda0db` |
| `transpile/execsnapshots.py` | 2,502 | `02d66a1a21c0732203cd303a95e33f854df3eb3a54f4bbd5091e64d24a32d1da` |
| `transpile/translate_go/algorithm.py` | 65,029 | `0dc5493670a435f4271b4299e79294b38327047ae9bd905f2d5638aeff181a80` |
| `transpile/translate_go/oracle.py` | 9,231 | `37f418abfe7d0a32fb2a24a5ae213e4c9f708065289b29e8f7d619140e1017fd` |
| `transpile/Oracle/testgen/src/syntax/synthetic/harness.rs` | 35,808 | `7ef109a228053d783463cf7820c78edbee4416b70a6663cb09719d9bad1696f9` |
| `transpile/go_features.py` | 59,283 | `920a05d11a05dae741bd4337e95232e8cdc0a60be7885fc88a99146ea80f50cc` |

The release makes key checks concrete while leaving the final experiment unreconstructed:

- **Entrypoints and results:** the offline script replays six named benchmarks. The README says ach's logs failed and replay will be fixed later; geo is absent from that six-project entry point. Its expected equivalent/compiled percentages are TextRank 77/99, checkdigit 72/97, go-edlib 75/100, gohistogram 63/100, gonameparts 73/100 and stats 73/99. These differ in both directions from the final table. The uninspected tar cannot be ruled out as containing additional material.
- **Repair phases:** the default driver invokes `type_based_translation`. After compatibility processing, that function calls all weak/unit checks and exits (`algorithm.py` 1642–1645). The inspected default/offline route does not reach the paper's later semantic repair phase. A separate skeleton-refinement routine repairs compilation, and `skeleton_semantics` ends after oracle construction/validation. These source paths do not reproduce the final paper's four-condition experiment.
- **Acceptance boundaries:** compatibility checks have named type/function exceptions and treat absent function/static checks as acceptable. On the sixth failing compatibility query, the inspected loop can return the new state while logging a skipped check (1524–1530). This is an artifact-specific acceptance path, not evidence that a reported run actually took it or proof that the final paper used identical code.
- **Oracle behavior:** `signature_check` returns when its snapshot file cannot be opened, and otherwise deserializes observed inputs and successful outputs. The unit test instead unwraps its snapshot file, compares successful return JSON and borrowed-argument post-state, and ignores moved arguments in that post-state check. It catches panics; a source failure accepts any caught failure, including unwrapping an error return. Error identity and post-failure state are not compared. The inspected snapshot schema has inputs, return value, success and argument modifications, without per-call global pre/post fields. This does not establish the paper's general global-state extension.
- **Denominators and missingness:** `result_table.py` computes compilation from **all `GoModule.item_map` items**, minus mock-attempt log lines. `get_all_items` includes types, globals, functions and constants. Equivalence instead divides successful named unit-test processes by the available unit-test names. These are different denominators and are not a recovered function/line table. Snapshot collection does not enforce the original `go test` return status before parsing available JSON; partially failed original tests could therefore yield a partial snapshot set. No such failure was executed or observed here.

These are located correspondence and contract limits, not a replacement set of experimental outcomes. No missing rate is imputed, no paper result is silently corrected from README values, and no source-derived concern is reported as an executed failure.

## Consequence and next action

S232 supplies an established alternative for **dependency-local translation, explicit feature obligations, observed type interoperability and body-level semantic checks**. It narrows any novelty claim based on modularity or useful type feedback alone. Its positive type-check contrast and small/flat semantic-repair increments also show why compiler success, compatible representations, observed function behavior and integrated interaction must remain separate outcomes. It does not estimate Nu's architecture benefit, D1's explicit-case treatment, live-state preservation or net professional maintenance value.

The next consequential dependency is **reference 29, Repository-Level Compositional Code Translation and Validation**, arXiv `2410.24117`. S232 uses it to support a claim about reduced developer translation effort despite partial automated equivalence. Resolve its edition and native record before reading the primary user-study/comparator and validation method. This can change B09/B10/B12's benefit account more than another abstract ranking. C05's type-context retrieval and co-evolution methods, S229's inaccessible professional comparison, and existing live/temporal frontiers remain separate open routes. All experimental holds remain.
