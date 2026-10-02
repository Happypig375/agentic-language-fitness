# S233 — AlphaTrans: compositional validation and developer completion

## Identity and actual coverage

Ali Reza Ibrahimzada, Kaiyao Ke, Mrigank Pawagi, Muhammad Salman Abid, Rangeet Pan, Saurabh Sinha and Reyhaneh Jabbarvand, *AlphaTrans: A Neuro-Symbolic Compositional Approach for Repository-Level Code Translation and Validation*, **PACMSE 2 (FSE), article FSE109, pp. 2454–2476, July 2025**, DOI [10.1145/3729379](https://doi.org/10.1145/3729379). Crossref records online publication on 19 June 2025. The selected [author-hosted final PDF](https://alirezai.cs.illinois.edu/assets/pdf/alphatrans.pdf) has **23 pages, 1,112,913 bytes**, SHA-256 **`3c476fd2c2cbec1ca9c16ab150be3419072b4a1449f1fc2f09daa3ac3cf31c7c`**, MD5 `babd390d55c5943a05bb357aaf956205`. Native parent/note/PDF **`WTYEF4TL` / `IL22FIRN` / `PGDSHS4X`**, collection `PKLXQNEE`, precede intentional full reading; attached bytes match. This resolves [S232](S232-modular-validated-translation.md)'s reference 29 at its final edition.

**Complete selected-publication reading:** all 23 text pages, eleven sections, seven figures, six tables, two algorithms and 66 references; no appendix. Fifteen physical pages are visually inspected: **1, 4–10, 12–13, 15–19**. All diagrams, algorithms and tables are included. Truncated displays are recovered in bounded ranges before credit. PDF extraction, passive artifact inspection and independent arithmetic are not reproduction; no author program, model, compiler, test, replay or container is executed.

The earlier title is *Repository-Level Compositional Code Translation and Validation*, [arXiv2410.24117](https://arxiv.org/abs/2410.24117). Version metadata identifies v1 on 31 October 2024, v2 on 4 November, v3 on 24 February 2025, v4 on 24 April and v5 on 19 June. Earlier bodies remain unread except automatically exposed discontinuous ResearchGate fragments. The v1 abstract reports 6,899 fragments, 99.1% syntax, 25.8% functional validation and 36 hours average translation; the final reports 17,874 fragments, 96.40%, 25.14% and 34 hours. These are editions of one work, not independent cases. S232's borrowed older rate is not silently replaced by the final. Artifact-available/functional badges on the paper are external certifications, not our replication.

## Method and observation boundary

AlphaTrans translates **Java to Python**, combining static decomposition, type mapping, a validated target skeleton, fragment generation and two execution-based validation routes (Sections 3–6). The ten projects are reduced versions of public projects: selection requires a working Java 21 build/test suite and bounded call-graph size; unsupported library dependencies and their uses are removed, retaining at least half the original methods. Results do not concern untouched upstream repositories or arbitrary language pairs.

The source is transformed to remove overloading and handle constructors through renamed methods, identifiers/factories and rewritten calls. Existing source tests check these transformations. Methods and fields become fragments; a call graph with backedges removed supplies reverse dependency order. Tests are decomposed into cumulative prefixes ending at application-method calls, with whole blocks retained for loops, branches and exception constructs. A failed prefix prevents later prefixes from running. A successful prefix without an assertion supplies execution evidence, not an intended-value check.

Type mapping uses documentation, usage context and one in-context example, followed by execution of a target annotation/prototype. Of **1,797 types**, 915 custom types receive generated skeletons and 738 of 882 other types map successfully; the resulting **91.99%** includes the custom types. The authors then manually map 144 unresolved types, improve 182 accepted mappings and augment 38 with unions. The subsequent 100% skeleton validation therefore follows manual work. Reuse of that mapping is plausible, but its construction cost and generalization to unseen libraries are not measured. Fields initially hold `None` and bodies `pass`; skeleton validity is distinct from implemented behavior.

Main translation uses DeepSeek-Coder-33B-Instruct at temperature zero, an adaptive three-to-five attempt budget and feedback repair. Prompts include source, dependencies, a partial target and an example. Tests guide repair and then supply the reported checks; no independent held-out evolution oracle is described.

- **Graal validation** substitutes one Python fragment into the original Java project, with translated dependencies delegating back to Java. The paper describes proxies, representation conversion and shared-state handling. Source tests then observe the substituted fragment with source-language neighbors. Graal success is useful local evidence, not proof of the fully translated program or all inputs. Library types, cycles/maps, impure hashes and ambiguous object lists constrain interoperability.
- **Translated-test validation** runs Python tests against the translated target. Test translation receives syntax checking; a separate proof or independent adjudication that every translated assertion preserves the Java oracle is absent. Prefixes can establish runtime reachability before an assertion is reached. All executed tests passing is relative to their content, reachability and correct translation.

The selected `graal_validation.py` delegates deeper interoperability to project methods; that engine is not fully inspected. `test_validation.py` implements prefix stopping and coverage-based outcomes. Its source does not independently validate translated assertions. Do not promote the paper's interface description to a fully audited alias/exception/state implementation.

## Reported results, including positive and adverse contrasts

The source roster has **836 classes, 8,575 methods and 2,719 JUnit tests**, including application and test code. After decomposition, Table 1 reports **17,874 fragments: 2,245 application fields, 641 test fields, 4,654 application methods and 10,334 test methods**. Existing tests cover 56.57% of application methods. Table 2's percentages use all **4,654 application methods**, not only covered methods or all 17,874 fragments.

| Outcome | DeepSeek main condition | GPT-4o ablation |
| --- | ---: | ---: |
| Application syntax valid | 98.80% | 98.80% |
| Graal success / all application methods | 24.50% | 27.83% |
| Graal success count in stored results | 1,140 | 1,295 |
| Additional Graal-error methods with all translated tests passing, M1 All | 30 | 6 |
| Reported functional validation: Graal success plus M1 All | **25.14%** | **27.95%** |
| Translated-test pass rate, TPR | 9.76% | 6.45% |
| Application methods with all translated tests passing, ATP | 2.88% | 2.26% |
| M1 Some, as printed in Tables 2/5 | 118 | 34 |

These preserve substantial local translation successes while showing that a model's higher Graal result need not improve integrated target-test outcomes. DeepSeek's Graal-success rate among covered methods is approximately 43.30%; the overall 24.50% must not be described as a conditional covered-method rate. Uncovered methods, Graal infrastructure errors, detected failures and target nonexecution remain distinct. Pylint scores of 10/10 after formatting do not measure maintainability or idiomatic design.

Removing transformation lowers Graal success to 4.58%, ATP to 0.81% and TPR to 3.05%. It also changes the application-method denominator to 4,431. This is a useful adverse pipeline comparison, not a fixed-unit isolated effect of one refactoring. File-level translation over 782 files per model has context/syntax failures, only eight DeepSeek/twelve GPT partially validated files, and zero TPR. That comparison removes the skeleton/incremental strategy together; it does not isolate context size or the language itself. Repeated-model uncertainty and independent timing replications are not reported.

EvoSuite-generated tests have 66.87% standalone application-method coverage versus 56.57% for the original suite, but coverage falls in three projects. The paper reports aggregate TPR/ATP gains of 5.85/2.11 percentage points; CSV gains neither. These tests are shorter and may lack strong assertions. They cannot use the Java 21 Graal route in this setup. The selected helper uses Java 11 and copies GPT-generated test translations to both model conditions, so this is a specific additional-test protocol rather than evidence that arbitrary extra coverage guarantees semantic preservation.

The test-decomposition result reports 62.41% passing prefixes within selected failing-test groups. Eligibility conditions on multiple prefixes and observed execution; tests/prefixes are dependent. The released analyzer groups by class/method/test and appends this rate only when exactly one observed prefix fails at the end. It is not a population-wide successful-obligation rate or a measured reduction in diagnosis time.

## What the developer exercise establishes

Two participants complete four translations chosen with reference to their project familiarity (Section 7.3). The paper reports:

| Project | Completion hours | Lines added / deleted |
| --- | ---: | ---: |
| commons-fileupload | 5.5 | 120 / 114 |
| commons-cli | 11 | 614 / 1,253 |
| commons-csv | 30 | 2,676 / 999 |
| commons-validator | 34 | 3,585 / 2,416 |

The average is **20.125 hours, reported as 20.1**. Finishing these partial translations with all tests passing is a positive feasibility result. The study supplies neither a matched unaided-translation condition nor an independently adjudicated fixed-oracle timing comparison. Its weeks/months counterfactual, general effort saving and asserted upper bound are not measured by these four completions. S232's claim of reduced developer effort consequently remains a borrowed inference, not an established comparative effect.

The release contains both partial and manually completed projects. Their test-file blob identities differ in **22/35 cli, 18/29 csv, 8/23 fileupload and 42/64 validator** test files. This is metadata evidence that the tests also change, not proof of test weakening. Selected CSV test inspection shows constructive repair: an empty translated test becomes many assertions, and mistaken method names/arguments are corrected. Test translation work belongs in completion cost, while all-passing completion is not independent validation against an unchanged original oracle.

The paper's unnumbered null-conversion example on physical page 15 and selected manual `CSVFormat.py` illustrate a narrower semantic caveat. Converting a null value using ordinary Python `str` removes a concatenation type error but produces `"None"`; Java string conversion produces `"null"`. This follows [Java 21 JLS §5.1.11](https://docs.oracle.com/javase/specs/jls/se21/html/jls-5.html#jls-5.1.11) and the selected `none_repr`/`NoneType` definitions in [CPython 3.10.14](https://github.com/python/cpython/blob/v3.10.14/Objects/object.c#L1477). The shown conversion alone is not a universal preservation fix. Selected null-string tests use literal `"null"`/`"---"`, not this null-value case. This is a source-level observation about the displayed mapping, not an executed failing test or a claim that every manual result is incorrect; wildcard imports and the complete runtime are not audited.

## Artifact identities and bounded reconstruction

The official [v0.1.0 release](https://github.com/Intelligent-CAT-Lab/AlphaTrans/releases/tag/v0.1.0), published 2 March 2025, resolves to **`1e7f027e018592872d53ade5db85e4edf9ca57f5`** (23 February). The complete Git tree has 6,856 entries and is not truncated. Current main is not substituted for this pin. The release README and five method/reporting scripts are read completely; two CSV implementation files and two CSV test files receive selected coverage. Model configuration/credentials, generated prompt/feedback bodies and most source files are not read.

The paper's [Zenodo artifact](https://zenodo.org/records/15204625), DOI **10.5281/zenodo.15204625**, is dated 1 April 2025:

- **`alphatrans-artifacts.zip`**, fully acquired: **56,536,010 bytes**, verified publisher MD5 `3f1f6a50b64e0e30a0dce8d36551b3c3`, SHA-256 **`fa6a257d3ccdd066b98e9b6d4e90afbd919008af6551f7219f2feed4c5c22984`**. Complete inventory: 4,959 entries. Independent parsing reads status/count fields in **1,570 result JSON members, 785 per model**, excluding EvoSuite members and the reporter's anonymous/overload cases. Parsing is mechanical; it is not full reading of their generated source, prompts or feedback.
- **`code-repository.zip`**, **181,882,203 bytes**, publisher MD5 `50c7d9eb231f30f76f2ef64ea3b2511b`: complete 12,864-entry central-directory inventory through verified HTTP 206 ranges; seven selected members acquired with ZIP CRC checks and byte-identical to the release files. The whole archive is not downloaded or hash-verified. A basename-only README selection was ambiguous and received no body-reading credit; the separately acquired pinned release README is fully read.

| Selected release member | Bytes | SHA-256 / coverage |
| --- | ---: | --- |
| `README.md` | 14,564 | `56fc571c49f36eb9874d5b15d9d9a8d6b3488f9cd1e409278af92b0a28092d29`; full |
| `src/postprocessing/print_results.py` | 13,701 | `5160def7321c1a7172054afb60699afa5de661a1401cfe3e5aa5ce1029c5e518`; all 261 lines |
| `src/postprocessing/analyze_test_decomposition.py` | 6,263 | `a8a52e37aea9c6bf8021cb8e340299975e5beeba0cc096a2a4e6e691a8c2de3b`; all 136 lines |
| `src/postprocessing/atp_tpr_plus.py` | 10,259 | `0e7be6f318372c6a91d4ea51f2d00934c5f76fe100a1ef3bf735abeb9ad744f1`; all 247 lines |
| `src/translation/graal_validation.py` | 2,726 | `513972fff04abe55807d75f05a79123a04f45809ca7daa825a1ce289d4b64822`; all 78 lines |
| `src/translation/test_validation.py` | 4,767 | `6aee3b5ab587029535b6dcbabf276784165c36bea7d59570bfdbe6f8bf5a1cc8`; all 88 lines |
| Manual `CSVFormat.py` | 48,649 | `9c6a1c26d024f5cb58ad60a97dd574a0f323df4ffb5d70a447fce4217cd0b871`; 107–112, 236–242, 703–709, 913–919, 936–942 and import/binding navigation |
| Partial `CSVFormat.py` | 43,060 | `abbe38ea2d3b7ecf2e356ad4ebf0fd09ae5db1a70d12bd9b56a3ed455912c4a2`; 106–112, 236–242, 646–652, 853–859, 876–882 and import/binding navigation |
| Manual `CSVFormatTest.py` | 50,988 | `e97fc34abc20e582dd29f3e368b8acacbf289cb9d72650c77102ef295fb8b6ea`; selected quote/null-method passages, 78–80, 330–355, 1108–1143 and initial diff excerpt |
| Partial `CSVFormatTest.py` | 44,148 | `49383d01a9553482e522eac11578ad50c12f49a3c9817b2ac9a6b45c2e47a36d`; selected quote/null-method passages, 78–80, 330–335, 950–985 and initial diff excerpt |

The four CSV members are under `data/manually_verified_translations/commons-csv/{manual_translation|partial_translation}/src/{main|test}/org/apache/commons/csv/`. The seven byte-matched code-ZIP members are the five scripts and two implementation files; the two tests were fetched only from the release. Exact inventories/ranges/member hashes remain local and ignored. Complete acquisition or inventory is not complete source reading.

### Located M1 reporting error and preserved successes

Independent arithmetic reproduces **all twenty project rows' Graal-success and M1 All/Some counts** in Tables 2 and 5. The preserved positive numerators are 1,140/1,295 Graal successes plus 30/6 additional M1 All cases. It also locates a specific error in the interpretation of **M1 Some**:

1. `print_results.py` lines 202–226 append the label `some-all` when a fragment has multiple executed tests and all fail.
2. `calc_m1` lines 6–23 counts every non-`all` label intersecting Graal errors as M1 Some.
3. Stored results consequently put **38 fragments with zero passing tests inside DeepSeek's 118 M1 Some**, and **9 inside GPT's 34**. These are observed stored statuses, not a hypothetical code path.

| Project | DeepSeek M1 All / Some / zero-pass subset | GPT M1 All / Some / zero-pass subset |
| --- | ---: | ---: |
| cli | 0 / 16 / 2 | 0 / 1 / 0 |
| codec | 11 / 27 / 3 | 2 / 18 / 2 |
| csv | 0 / 3 / 3 | 0 / 8 / 4 |
| exec | 6 / 9 / 3 | 1 / 1 / 0 |
| JavaFastPFOR | 6 / 25 / 11 | 2 / 0 / 0 |
| fileupload | 2 / 3 / 0 | 1 / 3 / 0 |
| graph | 0 / 1 / 0 | 0 / 0 / 0 |
| jansi | 0 / 1 / 0 | 0 / 0 / 0 |
| pool | 4 / 2 / 0 | 0 / 0 / 0 |
| validator | 1 / 31 / 16 | 0 / 3 / 3 |
| Total | **30 / 118 / 38** | **6 / 34 / 9** |

For example, the DeepSeek codec record for `MurmurHash3`, method `944-950:mix32`, stores four failures and no success; `IncrementalHash32x86`, `1026-1083:add`, stores five failures. The script nevertheless includes these in Some. Moreover, its All/Some categories are disjoint, whereas the paper's description of Some as at least one passing test would include All. Graal outcomes stored as dictionaries trigger an early `continue` at lines 100–114, skipping the associated translated-test observations. These representation and definition choices prevent a single unqualified corrected percentage. **The reported 27.03% runtime-valid claim, formed from 1,140 + 118, is not supported by the Some label as interpreted in the paper.** This does not erase the matching Graal successes or the separately matching All counts.

Two further correspondence limits remain. Direct stored syntax statuses give 17,334/17,874 = 96.979% for DeepSeek and 17,808/17,874 = 99.631% for GPT, differing from the paper's all-fragment 96.40%/99.2%; application syntax 4,598/4,654 agrees. Pending/Graal error/nonexecution statuses also do not transparently recover every printed partition, so no alternative final result packet is asserted. Figure 7's 74 + 1,096 and 1,096 + 205 totals equal **1,170 and 1,301**, matching Graal success **plus M1 All**, despite a Graal-success caption. These are located count/label discrepancies, not new experimental outcomes.

## Consequence and next action

AlphaTrans establishes useful predecessors for source transformation, type/context mapping, dependency-local translation, source-backed execution and incremental test feedback. Its local validated successes and four human-completed projects are positive evidence. They do not establish net developer time savings, universal semantic preservation, live-state safety, a Nu architecture advantage or D1's explicit-case benefit. The exact M1 error demonstrates why generation, test translation, execution, classification and published synthesis must be audited as separate steps.

The next consequential source is **MatchFixAgent**, identified on the primary author's publication page and linked as OpenReview **`MuyXpH3GL1`**. It addresses validation and repair verdicts for translation, directly bearing on the distinction now exposed in S232/S233. Resolve its edition and native record before reading its comparison and human-ground-truth method; its surfaced abstract claims are not accepted results here. ReCodeAgent, TRAM and skeleton-guided translation remain conditional methods, not an automatically expanded queue. S229's complete professional comparison and the independent live/temporal/type frontiers remain open. All experimental holds persist.
