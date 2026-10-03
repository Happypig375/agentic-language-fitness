# S107 — Bounded path suggestions and trace replay on a remote runtime

## Identity and actual coverage

Maarten Steevens, Tom Lauwaerts and Christophe Scholliers, *Remote Concolic Multiverse Debugging*, **ECOOP 2026, LIPIcs 372, 27:1–27:29**, DOI [10.4230/LIPIcs.ECOOP.2026.27](https://doi.org/10.4230/LIPIcs.ECOOP.2026.27), published **25 June 2026**. Existing native parent/note/PDF **`DLDX93XY` / `P4ZZCFMN` / `ZSZS9JFL`** were checked before continuing the full reading. The four collections `PKLXQNEE`, `NDU9BTP7`, `MBYQJXUF`, `IPZX66LF` are preserved. Scite's January 1 date is generic metadata; the primary publisher supplies the actual publication date.

| Edition / native attachment | Identity and reading scope |
| --- | --- |
| Official publisher / `ZSZS9JFL` | **29 pages, 3,402,313 bytes**, SHA-256 `22360b90ea5dfbaa7cbf3555ed3653137d13d42cb2e863180c97e2c739a326ea`, MD5 `9668d65dfa07e5123a8e1f63c280455e`. **All text pages, eight sections, 18 figures, Table 1, Algorithm 1 and 46 references read.** Thirteen visual pages: **1, 3, 7–9, 11–13, 15, 17–18, 20–21**. No appendices in this edition. |
| [Extended arXiv v2, 28 April 2026](https://arxiv.org/abs/2604.23035v2) / `TRQCP2DK`, same parent | **47 pages, 4,420,527 bytes**, SHA-256 `f64ffa4b622df8ea62463c214d23af40df6d1fed9ce92c429c9a66a3951c199e`, MD5 `f3f658ff1aeb88cd0fa4e640c6b97957`. **Complete Appendices A–F, physical pages 30–47**, including proofs, source listings, Figures 19–30 and Table 2; cover and page 20 table compared. Fourteen visual pages: **1, 20, 30–38, 40, 46–47**. The other main-body pages were not independently reread; this is not a second full-publication or replication credit. |
| [DARTS artifact description](https://doi.org/10.4230/DARTS.12.1.11) / parent `A83MVGHH`, PDF `TD7HF6NF` | Parent registered before body reading. **8 pages, 1,312,908 bytes**, SHA-256 `cfcba3ccf456bd1392373900c103c4e8207fbde56d3d90d052f6c3b1d2ae3367`, MD5 `d7db887b9d782ee9e45f3664d1b0066b`. **All eight text/visual pages, seven sections, Appendix A, eight figures, Table 1 and three references read.** Same-work companion, not independent benefit evidence. |

All attachment bytes match native storage. The publisher advertises a large VM archive with MD5 `ff735b349b8895d5bba56e61f70f65ee`; that archive was **not downloaded, hashed locally or executed**. Its reported 10.36 GB web size and 11.13 GB description are left as source labels, not claimed corrupt bytes. No author program, VM image, compiler, solver, benchmark, model, debugger session or hardware experiment ran. The source reading below is passive.

## Architecture and restoration contract

The debugger separates a WARDuino WebAssembly runtime on the device from a desktop client that maintains the execution tree and performs concolic analysis. In the formal model, ordinary VM instructions are deterministic. Input primitives are the only nondeterministic source; output primitives perform external actions without returning a value. The represented program state contains locals, globals, data stack, memory and remaining instructions. External-world state is not a component of that tuple (Sections 4.1–4.3).

During free execution, the server sends each input result with the number of instructions since the preceding synchronization. During paused stepping it reports each instruction. Tree edges encode either a deterministic step or a mocked input value. The client can build a useful execution history without retaining a full memory snapshot at each edge. An **on-demand snapshot is still transferred to start analysis from the current device state**; “trace-based” does not mean snapshots never occur.

Sliding to a descendant replays the edge operations. Sliding elsewhere resets the VM to its loaded-program start state and replays from the root, automatically injecting the chosen inputs. The tree remains available across a reset. Mocking substitutes a primitive's return value instead of taking a fresh physical sensor reading. Output calls remain external actions in the rules. Thus this mechanism restores the represented VM execution by re-execution; it does not undo a motor action, rewind another device, or restore a jointly consistent physical environment. The paper explicitly **trades MIO's reversible I/O for lower forward-execution cost** (Sections 3, 4.4, 7; extended Appendix A.4).

The semantics serialize communication, giving server-to-client processing priority and blocking the server while the client handles messages. This is a simplifying semantic choice, not a measured asynchronous-network guarantee. Incompatible frontend messages can make the formal system stuck. The Kotlin UI offers program upload, but this work primarily explores executions of one program version. It supplies no general state-migration contract across source edits.

## What concolic suggestions and the proof cover

Analysis starts from the concrete snapshot: existing values become symbolic constants, the symbolic environment starts empty and the path condition is true. Future input calls introduce fresh symbols. Concrete and symbolic operations proceed together, branch tests extend the path condition, and an SMT solver selects a new assignment outside previously covered path conditions. The tree-building algorithm merges common prefixes by checking whether exchanged input prefixes still satisfy the two path conditions (Sections 5.1–5.4; extended Appendix A.7).

Three limits are independently configurable: executed instructions, symbolic input operations and concolic iterations. Selecting an already calibrated state can make the remaining analysis much smaller because earlier calibration values stay fixed. This is useful conditional exploration; it does not establish coverage of all calibrations or earlier histories.

The soundness/completeness arguments in extended Appendix D concern **reachable represented program states under the stipulated language/debugger semantics**. Soundness relies on executing the underlying instructions and restricting mock values to feasible primitive returns. Completeness relies on the developer's ability to supply a suitable manual mock for any input step. The appendix explicitly describes automatic concolic exploration as an under-approximation. A bounded suggestion tree therefore does not inherit the whole debugger's reachability completeness.

Control-flow representation also differs from testing every value or intended behavior. In the zoetrope example, an analog input directly sets motor speed without branching, so the analysis supplies one representative value. Other speeds still require manual exploration. The worked temperature/gesture examples use unexpectedly repeated sensor reads to expose extra choices, a useful diagnostic affordance. They do not constitute a controlled user study or an independent behavior oracle. The proof neither verifies physical-effect reversal nor proves application correctness, and no proof checker was run here.

## Evaluation and its meaningful positive results

The authors select Arduino examples with an input sensor and a conditional, excluding output-only examples and unsupported sensors. They add a gesture controller and their own breakout game. The twelve rows include calibrated/un-calibrated variants of one program. Arduino examples are translated into AssemblyScript; the supplementary source makes loop limiting and other modifications explicit. The column called **States** is an estimate from the product of input options along a maximal-choice path, not an enumerated count of all reachable VM states. Paths and maximum choices are distinct quantities.

| Program | Suggested paths / maximum choices | Loop horizon | Analysis time, seconds |
| --- | ---: | ---: | ---: |
| Crystal ball | 11 / 8 | 2 | 0.283 |
| Knock | 2 / 2 | 1 | 0.038 |
| Touch sensor lamp | 2 / 2 | 1 | 0.003 |
| Switch | 4 / 4 | 1 | 0.131 |
| Keyboard | 5 / 5 | 1 | 0.116 |
| Love-o-meter | 4 / 4 | 1 | 1.172 |
| While, fixed calibration | 3 / 3 | 1 | 0.063 |
| While, calibration included and analysis capped | 76 / 65 | 1 | 219.613 |
| Knock lock | 13 / 3 | 2 | 0.074 |
| Zoetrope | 16 / 2 | 2 | 0.080 |
| Gesture robot | 31 / 2 | 1 | 0.106 |
| Breakout | 3 / 3 | 259 | 5.032 |

These are useful reductions in the options a developer must initially inspect. **Nine of twelve rows finish below one second**; the calibration case remains a substantial adverse case, rather than disappearing behind “reasonable time.” Its fixed-calibration comparison conditions the problem and changes the source/state; it is not an equal-coverage speedup. The knock-lock's two iterations do not cover every three-knock unlocking scenario, which the paper itself flags as a reason to extend the horizon.

The breakout result is directly relevant game evidence: three suggested paths represent paddle-left, hit and paddle-right at the selected horizon. Input values can vary without changing the preceding control path. The enormous printed `3.992 × 10^935` input-combination estimate is therefore **not a measured search-time speedup or evidence that every gameplay state was tested**. The complete 398-line appendix game includes display setup, drawing and ball/paddle updates; it is a small authored demonstration rather than a production engine evaluation.

For **50,000 breakout instructions**, the main paper reports approximately **1.9 seconds untraced, 2 seconds traced and 5 minutes with MIO checkpointing**. Extended Appendix F locates this comparison on a **Raspberry Pi Pico W, dual-core Cortex-M0+ at 133 MHz**; the abstract's STM32 prototype wording should not relabel this specific experiment. Frequent display-output primitives trigger snapshots every roughly two or three instructions in the expensive condition. The result supports a strong forward-execution advantage in this workload, with slower backward navigation because replay restarts from the beginning. It does not measure total debugging time, memory/communication volume, repair success or the benefit of maintaining equivalent reversible-I/O guarantees.

## Supplement and source correspondence

The artifact description deliberately supplies **emulator example output** rather than the hardware observations above. At 50,000 instructions it prints **2,946 ms untraced, 3,941 ms traced and 224,561 ms checkpointed**. Own arithmetic gives **33.77% tracing overhead over that emulator baseline**, while checkpointing is about **56.98 times the tracing time**. These are calculations from printed examples, not new measurements or replacements for the hardware comparison. The five listed instruction counts are cumulative checkpoints, not five independent repetitions.

Artifact Appendix A.2 explains two table differences. Crystal ball uses a manual `2 × 2 × 8 = 32` estimate in the paper, whereas the implemented random source is an analog-input surrogate followed by modulo, giving `2 × 2 × 4096 = 16,384` before reduction. The calibration example prints **190 paths / 162 maximum choices** rather than **76 / 65**, explicitly attributed to bounded analysis. Times also vary with platform. The final paper's switch prose says five paths while its table says four; both the artifact table and later source below support four under a 0–4095 sensor domain. Historical cause remains unresolved. Knock's two-path table versus four-path narrative uses different one/two-loop horizons and is not a contradiction.

The [paper-linked `rcmd` source](https://github.com/TOPLLab/MIO/tree/08571ec4a888b7fa0f39bbf113681fef58bf1a5b) is pinned to **`08571ec4a888b7fa0f39bbf113681fef58bf1a5b`**, **12 August 2026**, later than publication. The complete returned top-repository tree has **227 entries, not truncated**. Its two WARDuino submodule commits are recorded, but their recursive contents were not read: ordinary `82a8afd87338e53b08eebb7c5d0a3db2ef1e0f9c`, symbolic `5a0582161bf1e91d654450e50a46a63ba63b2b24`. Thirteen selected files were fully read and hashed:

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `README.md` | 2768 | `79b2d4ca62adfb834e4457f5596569c138cd8b846626ed65a97c355c41286d7f` |
| `src/test/kotlin/benchmarks/TracePerformance.kt` | 1915 | `f744c221abb75de775f7942e841a2aee66a4ebce9d8bf4589cfadbbcc0cdc52f` |
| `.gitmodules` | 184 | `afbe4efddae7d84d120955281c1b6b72335e0838b763ffac632774edbddd0b0a` |
| `src/test/kotlin/benchmarks/Benchmarks.kt` | 4587 | `cf1aa4c5edf7b6835161496d15b8ac7a697a3f9e79fdab4257fbd22c62b540f4` |
| `src/main/kotlin/be/ugent/topl/mio/concolic/Analyse.kt` | 4666 | `3a6310bbe83fa44876830f047149e81ee4a4874d4b45e9e661500c99652d26e1` |
| `benchmarks/evaluation.py` | 2274 | `cacb17d706bd174386bc1ecf368b6cbfdae5625b1ed32a3fe2b3d799a2510956` |
| `run-benchmarks.sh` | 329 | `7ec739df4566a9b511e487082cf4dbc7a392a913343b114fb5d611540e0d4a60` |
| `src/test/kotlin/benchmarks/graphs.tex` | 12795 | `336f400ee47ef043739db3180a6ff3b82b2f18e9b14554e9e722c24304169d97` |
| `src/test/kotlin/DebuggerTestBase.kt` | 995 | `01935a9c51ace4f3acc0db2415859f832d833ab3ec4dfd3eacc4fc43a9771cce` |
| `benchmarks/arduino-switch-example/switch.ts` | 1776 | `13cc7fecb264a6e7be9ee5d39d3e088d38abb10fab1ea3bb8c828603d4d6a1b5` |
| `benchmarks/arduino-crystal-ball/crystal-ball.ts` | 3323 | `4c1f15cfecad63629f2ed38f5d69228ad90706d8b2af5b547a40c8128f0f2b14` |
| `benchmarks/arduino-while-no-calibrate/while.ts` | 2334 | `b4e41db57d9cc2f8135cbd33ac4d88d5c604d53b3eeaa823242b0c1a328fa0bb` |
| `benchmarks/arduino-while-example/while.ts` | 2324 | `9843de513d6ad3727d7ce8b48223bf3bcf39259b57c21d59f10b87a0fb150029` |

The bounded inspection establishes concrete integration and measurement choices:

- `Analyse.kt` serializes the current snapshot with `io = false, overrides = false`, passes instruction/symbol/iteration/stop-PC limits to a separate concolic executable, and turns returned input paths into tree nodes. The solver/runtime implementation is in the unread submodule; this wrapper is not implementation-wide validation of the proof or prefix-merging algorithm.
- `evaluation.py` supplies twelve explicit configurations. Both calibration variants use **100 instructions, ten symbols and 200 concolic iterations** in this later revision; breakout uses **259 symbols**, not a universal 259-iteration guarantee for arbitrary programs. The script generates `table.tex`, which is not stored in the inspected tree. There is no recovered raw packet tying all final table rows to this revision.
- `TracePerformance.kt` chooses emulator mode, performs **100,500 initial unmeasured instructions**, then takes five cumulative 10,000-instruction intervals per policy. It clears stored checkpoints within each timed interval. This supports the artifact's emulator route; it does not reconstruct the exact Pico W run or measure retained-memory consumption. The other benchmark class and plotting file concern prime-program/checkpoint studies and are not secretly additional S107 breakout replications.
- The source modifies examples materially: crystal ball uses an analog-input/modulo surrogate, a two-iteration loop and omitted LCD output; the switch maps 0–4095 to 0–3; the calibration versions have a single outer iteration and a single conditional calibration. The appendix fixed-calibration listing retains an infinite loop, so one-loop functional intent can agree while source versions differ. No compiler or behavior-equivalence check was performed.

The public archive and current source are available. Their unexamined contents and unresolved final-run binding should be called bounded coverage, not access denial or a reproduced failure. The README's Linux/macOS support and Java/C++/Z3/custom-runtime requirements are integration obligations, not measured adoption effort.

## Consequence for Nu and next action

For **B03–B08/B10/B12**, this closes the selected remote-debugger method gap. It adds a useful concrete game example, strong scoped forward-execution results and an explicit high-cost analysis case. It also separates three contracts: a replayable VM trace, a bounded set of representative control paths, and consistency of external effects. Nu's retained state could support a different trade-off, but cannot by itself establish the last two contracts or a developer benefit.

Consolidate S99/S100/S105/S106/S107 with the already reconstructed migration and game alternatives, using editable scope, state/history, queued work, external effects, observations and full costs. **MIO's own I/O-compensation method remains a consequential primary-reading dependency**, currently represented here through S107's account and bibliographic identity, not a newly completed reading. Follow it if the comparison depends on its exact reversible-I/O contract. S229's professional-workflow access and .NET/game transfer remain distinct gaps. No new experiment, model or extra worker is authorized by this reading.
