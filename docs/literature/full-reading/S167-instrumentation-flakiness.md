# S167 — instrumentation and test flakiness

Shawn Rasheed, Jens Dietrich and Amjed Tahir, *On the Effect of Instrumentation on Test Flakiness*, AST 2023, [DOI 10.1109/AST58925.2023.00016](https://doi.org/10.1109/AST58925.2023.00016). Reading completed 2026-10-01. Live question: B07/B10/B12, whether observation changes the behavior being judged and whether a variability score measures failures or their causes.

## Identity and actual coverage

Native Zotero parent `6QMM4TTK`, note `W3U22LFB`, PDF `FZY7XPU6`, established before reading. Chosen [arXiv 2303.09755v1](https://arxiv.org/pdf/2303.09755), 17 March 2023: **five pages, 241,846 bytes**, SHA-256 `ee61b44359a09faac1ebbf1fc54d1d02f9c1fb9923baedc5432d6a5f55648133`, reverified against the native stored file. All five pages, Figure 1, Tables I–IV, the code example, Jaccard equation, three footnotes and eighteen references read. Pages 2–4 visually inspected. Exact correspondence to the publisher's conference file remains unchecked.

The public Bitbucket release was inspected at commit `9fb5651d0cd8ede72c58861cf0282058ca1eee96`. Its [separate artifact reconstruction](S167-instrumentation-artifact-check.md) records complete filename inventory, three textual files and **47 of 1,080 result ZIPs**. Read-only parsing of selected report fields and descriptive arithmetic are not execution of the study, its Java projects or the instrumentation tools.

## What was compared

The authors select eleven Java/Maven projects from the earlier Shaker dataset, then omit hbase and ozone because their tests took over thirty minutes. Nine remain: Chronicle Queue, CorfuDB, azure-iot-sdk-java, Exhibitor, Flow, Karate, MockServer, RipMe and Kill Bill. Table I fixes commits/tags. The printed CorfuDB baseline duration is **2,784.2 seconds**, already over thirty minutes; therefore this is not a consistently demonstrated thirty-minute eligibility boundary for all retained projects.

Each project is run twenty times in each of six configurations: baseline; Elastic APM 1.34.1; OpenTelemetry 1.12.0; JaCoCo 0.8.8; IntelliJ coverage agent 1.0.684; and Java Flight Recorder, without a separately printed version. That gives **9 × 6 × 20 = 1,080 runs**, not 1,080 independent applications. The described machine has a 3.2 GHz six-core i7 and Oracle JDK 8u301. Fixed hardware/OS/JVM is asserted, but the OS name and enough randomized-order, reset and environment details to reconstruct all runs are absent.

The mechanism is broader than timing overhead. Instrumentation can consume processor/memory resources, load classes, change scheduling and occupy resources such as ports. The worked MockServer example uses port 8888, also occupied by the APM configuration. Such a deterministic configuration conflict is distinguishable from within-configuration nondeterminism. Source-to-bytecode coverage mapping is a different measurement issue, followed through S171; industrial root-cause instrumentation is followed through S172.

## Outcomes and units

The paper distinguishes success, failure, error and skip. It describes flaky tests as those whose outcome changes across runs **or configurations**, then develops a score intended to exclude variation seen only between configurations. Preserve those two definitions. A persistently failing test, an absent report and a skipped test are not interchangeable with a healthy stable pass.

For run outcome sets containing `(test, state)` pairs, distance is one minus Jaccard similarity. A configuration's twenty runs yield **190 unordered run pairs**, summarized by a mean and median. Those pairs reuse runs; they are not 190 independent observations. A score of zero can describe an always-failing test. Variability is not a monotone measure of failure probability across its entire range and does not establish fault severity or instrumentation causation.

The text defines the selected test set, FT, as tests flaky “in all configurations,” while later results include positive scores for a configuration when baseline has no flaky tests. A literal intersection would exclude those tests. This could be wording or implementation, but the released files do not include the analysis code needed to resolve it. Do not silently replace the definition with a union.

## Positive, null and adverse results

The descriptive directions are mixed, rather than uniformly adverse to instrumentation. Table III's CorfuDB baseline has fifteen flaky tests and Table IV gives score .475; JaCoCo has ten and .556; JFR has 74 and .119; Elastic APM has 75 and .352. A count and pairwise variability can move in opposite directions. Azure's seventeen baseline flaky tests become zero under JaCoCo and IntelliJ, while reported test totals also vary between configurations. These are fixed selected projects and tools, not a prevalence estimate for all instrumentation.

Exhibitor is reported as having zero baseline flaky tests and one under JFR, with a .200 score. The raw release supports the average outcome totals but **does not reconcile that score** under the printed formula: see the bounded check below. MockServer/OpenTelemetry has one flaky test in Table III but no score in Table IV, whose stated omission rule is zero flakiness. Karate/JaCoCo likewise has one flaky test but no Table IV project row. These omissions remain unresolved.

The discussion reports that observed changes were generally small and only rare examples were attributed to instrumentation. No formal test, interval, equivalence margin or power calculation supports treating its “no significant changes” wording as an equivalence finding. Twenty runs can miss infrequent failures. Nevertheless the actual mixed directions and examples remain evidence against asserting that every instrument necessarily worsens every suite.

The prose also conflicts about an external-tool failure. A `FrontendToolsLocatorTest::toolLocated` example is first associated with RipMe, then Flow/RipMe external failures are called incidental, and later the Flow example is listed as OpenTelemetry-induced. The selected Flow reports contain a **different** failing test in both baseline and OpenTelemetry, concerning an old pnpm version. Four runs cannot resolve the whole attribution. Preserve the inconsistency instead of repairing the project/test identity by inference.

## Bounded release check

The release lists the expected nine projects, six configurations and twenty indices per cell. Complete baseline/JFR report sets for Exhibitor were available before the public API returned **429** during the remaining selected downloads. Further requests stopped; other literature work continued. The artifact note records the exact 47-file manifest and 37 selected files not fetched.

Exhibitor ZIPs contain both individual-class and aggregate suite XML. Fifty-three regular test identities are normally reported twice, producing the paper's 106 success entries. JFR run 6 contains setup/teardown entries and a conflicting duplicate: the same regular method is recorded as skipped in the aggregate suite and failed in the class report. A simple last-entry-wins dictionary would hide that disagreement, so it is **not** an authoritative reconstruction of individual outcomes. Raw entry averages, **105.9 successes, .1 failures and .1 skips**, match Table III.

For JFR, nineteen runs have identical relevant outcome sets and one differs. With the stated mean over all 190 unordered pairs and any fixed test set, only nineteen pairs can have nonzero Jaccard distance. Each distance is at most one; hence the mean is at most **19/190 = .100**, inconsistent with the printed **.200**. This bound does not require resolving the duplicate's skipped-versus-failed state. Restricting to the one common varying regular test also gives .100. No author analysis implementation was located in the listed package, so the cause of the mismatch and other rows' correctness remain unresolved. This is a specific paper/data/formula discrepancy, not a reproduced experiment or grounds to discard every result.

The exceptional Exhibitor report contains an `IllegalArgumentException` about duplicate Curator instance keys. It establishes an observed report, not that JFR caused the fault. The three cached MockServer baseline runs all pass; instrumented MockServer reports were not fetched, so the port-conflict attribution was not independently verified from this release.

## Consequence and remaining work

S159's game timing/physics failures, S164's coverage infrastructure and S167's Java outcomes have different workloads, denominators and observation scopes. Preserve the positive operational/stability findings as well as adverse examples without pooling them into a universal instrumentation effect. Instrumentation state, absence/skipping, reproducibility and failure attribution belong in an observation contract; useful diagnostics do not themselves establish retained or changed application behavior.

Bibliography follow-up promotes S171's source/bytecode mapping and S172's industrial diagnosis method, both acquired with native records before body reading. G30's seven incoming entries include a table of contents, two environmental-flakiness edition identifiers and four other study/position-paper routes. SC100–102 and W229–W230 retain Shaker, safLate, actionable score design, environmental controls, concurrency amplification and practice/review leads at their actual metadata/abstract/selected-passage scope. Sanitizing or skipping a failing test to permit a build is not evidence that its behavioral obligation passed. The forty-five-page journal extension of S171 is a distinct incomplete edition, not an independent replication.

**Unique:** observation interference and diagnostic instrumentation have prior mechanisms; no ISE firstness established. **Valuable:** measuring interference is a concrete need, while its size and net benefit are workload-specific and unmeasured for Nu. **Scientifically valid:** the primary text supports bounded mixed observations; ambiguous outcome sets, duplicate report units, score mismatch and causal attribution limit stronger inference. No experiment or new worker is authorized. S166/S170's original fault-validity methods, S169's framework and the wider practice/type/runtime frontiers remain open.
