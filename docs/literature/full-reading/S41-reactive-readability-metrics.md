# S41 - Readability metrics under reactive refactoring

**Full reading completed 2026-09-29.** Gustaf Holst and Felix Dobslaw, *On the Importance and Shortcomings of Code Readability Metrics: A Case Study on Reactive Programming*, [arXiv:2110.15246v1](https://arxiv.org/abs/2110.15246v1), posted 2021-10-28, DOI [10.48550/arXiv.2110.15246](https://doi.org/10.48550/arXiv.2110.15246). All 11 pages, sections I-IX, 29 references, figures 1-6, tables I-IV and equation 1 were read. Figures/tables/equation were checked in MuPDF renders of pages 3, 5-8 and 10. Zotero parent `9V2ERRQH`, PDF `C7XEQGMD`; SHA-256 `0de7bf9c441cbb393cd6029b95c59c51bd63fbdcbb9c309205e3682b3c8053e6`. No publisher edition was assumed equivalent. Reader: the main Codex session, not independent human review.

## Actual intervention and outcome

Sections III and VI describe a manually authored, method-level RxJava 3.0.2 refactor of Kryonet, a headless Java network library. The reported original system has 54 classes, 283 methods and 3,664 lines. The comparison selects **42 methods in five classes**, preserving public interfaces and method boundaries. Exclusions include methods over 50 lines, lack of iteration or error handling, and single-statement methods. This is neither a random project sample nor a redesign into a fully reactive architecture.

Statements are placed in reactive operator chains, with `doOnSubscribe`, `doFinally` and `doOnNext` accommodating effects. Lambda parameters use single-character names. The authors deliberately avoid functional decomposition to keep methods comparable. They report that the existing test suite passes; this does not establish independently verified equivalence, and the tests were not rerun here.

The outcomes are **preexisting static metrics**: PMD cyclomatic complexity, Buse/Weimer predicted readability and Scalabrino's combined predicted readability. No new human comprehension, maintenance, debugging or coding-agent experiment is performed. The paper's comparison with S39 therefore changes the language/library, code, population and outcome; it is not an adverse human replication of S39.

## Results and bounded artifact reconstruction

The paper links [Zenodo record 4277872](https://zenodo.org/records/4277872), labeled a replication package for the submission. Its public API identifies two archives. Both were downloaded, their published MD5 checksums verified, and their SHA-256 recorded:

| Archive | Bytes | Published MD5 | SHA-256 |
| --- | ---: | --- | --- |
| `measurements.zip` | 24,774 | `13b07518eaa1497aff850c2a73437575` | `304442c9797b7cb0e1c24bad520228a2a71e661dcd75b88c0642327ac9ad2b97` |
| `source_code.zip` | 44,043 | `a96727baf924d44bfbc9a07bcc896ac8` | `c6e453d2e469331a809aec9550f20c443083d9c14b05dd2854191c6602c8ee94` |

Both semicolon-delimited CSVs contain 42 data rows with 42 unique `(class_name, signature)` keys, and the two key sets match. The class distribution is Client 7, Connection 11, Server 15, TcpConnection 4 and UdpConnection 5. Recalculating means and sample standard deviations from the released scores reproduces Table IV to its displayed precision. This checks aggregation of supplied measurements; it does **not** rerun the metric tools or reproduce the refactor/testing experiment.

| Mean across the 42 selected methods | Original | Reactive |
| --- | ---: | ---: |
| PMD cyclomatic complexity | 5.7381 | 1.4524 |
| Buse/Weimer predicted readability | 0.07761 | 0.04140 |
| Scalabrino predicted readability | 0.63437 | 0.38305 |

The source archive contains five original and five reactive Java files. The two `Server.sendToTCP` bodies were inspected and match Figure 6's loop-to-operator-chain example; the corresponding CSV scores match its caption. The rest of the Java bodies were not fully audited. The archive contains no complete build/test harness or metric-tool environment, so the reported behavioral equivalence and extraction configuration remain unverified. No downloaded code was executed.

## What the contrast establishes and leaves open

Sections VII-VIII show that the refactor lowers counted control-flow complexity while adding punctuation, parentheses and operator identifiers that affect predicted readability. This is a useful warning about representation-sensitive proxies. Moving explicit branches into library operators can reduce a local metric without demonstrating fewer end-to-end behavioral obligations. That latter statement is an inference from the measured boundary and inspected example, not a measured maintenance effect.

The authors argue that the readability models are unsuitable for reactive code, partly using their own judgment and S39's different human study. Their dataset alone cannot determine whether the refactored methods are easier for humans: it supplies no human criterion for these exact snippets. Conversely, a lower model score does not refute S39's human result. Do not adopt the preferred metric as ground truth merely because its direction agrees with the hypothesis.

Figures 1-5 display standard deviations across selected methods, not confidence intervals across independent projects. The paper uses the word significant, but reports descriptive aggregates without an inferential comparison establishing a population effect. Its local illustration, selection policy and single-project dependence prevent using 42 methods as 42 independent game-engine trials. The printed CYC definition is not adopted as an ISE measurement specification; any later metric implementation needs its own precise definition and version.

## Design consequence and follow-up

**Unique:** readable/reactive source claims and measurement criticism are established; neither is a new Nu contribution. **Valuable:** the study justifies testing useful behavior rather than promising value from a favorable static score. Nu/agent benefit remains unmeasured. **Scientifically valid:** retain complete new/old obligations, source/tool opportunity and adverse cases in D1; source compactness and static metrics may describe assigned implementations but cannot replace behavioral endpoints or prove their mechanism.

S40's API tasks and S43/S49's debugger comparisons remain closer human follow-ups. The bibliography also identifies primary studies on metric/perception disagreement, automatically assessed understandability, and Java lambda introduction (references 21-26). Reopen the particular study if a later claim depends on human metric calibration; their results are not newly credited from S41's secondary summaries. No experimental allocation changes.
