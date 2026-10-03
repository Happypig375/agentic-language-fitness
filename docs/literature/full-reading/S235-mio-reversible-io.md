# S235 — Multiverse debugging with explicit I/O compensation

**Complete publication reading, 2026-10-03.** Tom Lauwaerts, Maarten Steevens and Christophe Scholliers, *MIO: Multiverse Debugging in the Face of Input/Output*, PACMPL 9(OOPSLA2), article358, 30pages, published9October2025, [DOI10.1145/3763136](https://doi.org/10.1145/3763136). The repository's continuous pagination is2396–2425. Native Zotero parent **`B768XDR7`**, note **`QFF2IAPX`**, were created before selected body reading after checking254 collection parents and1,260 library top-level items by DOI/title. Four memberships, including `PKLXQNEE`, are retained.

| Source and native attachment | Identity | Actual coverage |
| --- | --- | --- |
| [UGent published copy](https://biblio.ugent.be/publication/01KFB69MCM28BFM42ZD7BDESKQ/file/01KFB6AYK6MYRY9D138VZ8718W.pdf), `5QH6GIFM` | **2,085,405bytes**, SHA-256 `4acd9fcbff1e217a696a9eb60896473254803a56827e962d7f1c61ba2f14765d`, MD5 `e7c3a460751c9f3151f1510f8e5aebb0` | All31 physical text pages: ACM cover plus30 article pages, seven sections, fifteen figures, Algorithm1, footnotes and100 references. Seventeen visual pages:1–2,4,7,9–18,20–22, covering every figure, algorithm and substantive displayed rule/theorem. |
| [Extended arXiv2509.06845v1](https://arxiv.org/abs/2509.06845v1),8September2025, `JNGY5AEP` | **34pages,2,017,084bytes**, SHA-256 `f8678bf284ab6501c32a819849bb384265da3af6042f8daf99a05c70dc71af32`, MD5 `d0b55701946c4a86cc3bf9f0d4222c24` | Complete Appendices A–B, physical31–34, including Figures16–17 and all proofs; also opening page and final bibliography page30. Five visual pages:1,31–34. Remaining main body is not independently reread or certified identical to the final article; its bibliography has99 entries. |
| [Paper-cited Zenodo v0.1.4](https://doi.org/10.5281/zenodo.15838624),8July2025, `Q5WK98YR` | **4,370,699bytes**, SHA-256 `8b4028aa224a096e864fe87e9ffabccbf21da979269067731a2d62d28d3fc54f`, advertised and locally verified MD5 `c2002373cdd6d3a187347d4a08b18659` | Complete147-entry ZIP inventory; selected source reading below. Acquisition includes binaries but none is executed. The archive omits the WARDuino submodule's contents; its pinned source is inspected separately. |

All three native stored files are hash-verified. Web-reader PDF/Zenodo routes fail, while ordinary system-trust HTTPS retrieves the repository PDF, arXiv PDF and Zenodo API/archive. No certificate verification is disabled. Extraction and visual reading, source reconstruction, artifact badges and experimental reproduction remain separate. No compiler, debugger, solver, board, author script/test, application or demo video is run.

## Why this dependency changes the comparison

[S107](S107-remote-concolic-debugging.md) reduces forward-debugging cost by replacing repeated checkpoints with input/instruction traces and giving up output compensation. S235 supplies the missing primary account of the stronger effect contract. It combines a WARDuino device backend with a Kotlin desktop history/UI, mocking and sparse snapshots, and demonstrates a Lego color dial. This is the same research lineage, not an independent replication or an S107-equivalent experiment.

The program has one code base and a tree of executions. Nodes remain distinct even when their represented values repeat; loops are unrolled. Source-version exploration is explicitly distinguished in §6 and its combination with execution exploration is future work. An update-code button and a module-upload API therefore do not establish a general live code/state-migration contract.

## Reversible I/O is a supplied contract

Ordinary instructions are deterministic; non-determinism enters through input primitives. A primitive's argument-dependent possible values must be known, and mocks must belong to that set. Output primitives must complete **synchronously and atomically** and have a **deterministic compensating action** returning the relevant external state to its preceding condition. Each invocation supplies its own compensation, potentially using captured state. Input operations use a no-op compensation.

The formal semantics assumes independent sensors. The prototype additionally permits simple programmer-declared output/input dependencies, such as a digital pin forcing a sensor result. An independent range check is not a model of every physically possible joint input sequence. The paper explicitly elides environmental interactions from its proof model and calls a richer dependency language future work. Parallel execution is also outside this formalization.

The state includes the VM store, local values/instructions, execution mode, incoming command, mock map and snapshot list. A snapshot follows each I/O primitive. Ordinary instructions between these boundaries can be replayed deterministically. To step backward across an output, invoke its compensation, restore the earlier VM snapshot and replay only the intervening ordinary instructions. Arbitrary branch travel first reverses to the lowest common ancestor, then advances with the recorded input choices. This is more than retaining an immutable value, and differs from S107's reset/root replay without compensating outputs.

The supported boundary is consequential. §5.4 excludes asynchronous outputs and physically irreversible effects; arbitrary public-service interactions cannot simply be rewound. Unknown/unbounded input spaces need further sampling machinery. Controllable test environments can broaden practical use, but they change the environment and require their own correspondence argument. Time, peers, irreversible consequences and temporal obligations do not become restored merely because selected pins or motor targets are restored.

## What the proofs warrant

The first two theorems concern **reachability of represented VM configurations**: debugger-reached states have an ordinary forward path, and an ordinary path can be followed through suitable commands/mocks. Completeness is an existence property, not evidence that the UI enumerates every path, finishes an infinite tree or supplies the right input without human effort. AppendixB makes the admissible-mock and reachable-snapshot premises explicit.

Compensation soundness is separate. Its argument reduces a walk in the rooted execution tree to a forward path by removing closed walks, pairing output steps with their reversing steps. This relies on the output/compensator contract; it does not synthesize or independently prove the physical compensator. AppendixB defines effect equivalence through the named output/compensation operations, rather than introducing a complete physical-world state model.

The written rules also retain specification limits. Figure10 and AppendixA write primed store/local fields in the mock result without an explicit equality/frame premise, whereas the proof uses the ordinary input result with those components unchanged. Definition3 lists stepped output and compensation rules but does not explicitly list the free-running output variant. These are literal presentation gaps requiring clarification for mechanization, not executed counterexamples or a claim that the intended implementation permits arbitrary state changes. No proof assistant or independent formal checker is supplied or run in this inspection. The useful contract and conditional proof argument survive without upgrading them to verified end-to-end device correctness.

## Positive timing evidence and its units

The paper reports an **STM32L496ZG at80MHz** connected to a laptop. The timing workload has no I/O primitives, so fixed checkpoint intervals isolate snapshot/communication cost; it does not measure a realistic effect-heavy game's whole debugging session. Figure13 averages ten repetitions of each selected configuration, with250–1,250 instructions.

| Snapshot policy at1,250 instructions | Printed time/ratio relative to no snapshots | Meaning |
| --- | --- | --- |
| No snapshots | Baseline averages about222.7ms across these short executions | Communication/control overhead remains in the measurement; this is not pure VM instruction throughput. |
| Every instruction | About19seconds /85× | Strong adverse full-snapshot overhead on this device/workload. |
| Every5 instructions | About4seconds /17.9× | Large improvement over every instruction, with substantial remaining overhead. |
| Every10 instructions | About2.1seconds /9.5× | A further scoped improvement. |
| Every50 instructions | About2.7× | A latency/storage tradeoff, not a free reversible execution. |
| Every100 instructions | About1.9× | The favorable sparse-snapshot endpoint in this comparison. |

The filled areas in Figure13 are display fills, not uncertainty intervals. Figure14 reports about468ms for the smallest backward step; from roughly1,000 to30,000 reexecuted instructions, cost rises about11ms per additional thousand, reaching about one second. Its first plotted jump is substantial, so a single slope should not be extrapolated through the468ms origin. The authors' “negligible” interpretation is relative to slower forward snapshotting and physical actions; no human response-time or task-success study tests it. Ten runs are repeated timings of one program, not ten independent applications.

The color dial is a concrete favorable demonstration: the sensor selects a color, a motor moves the needle, backward travel compensates the selected motor state, and mocks permit different color paths. The paper reports a snapshot approximately every37 instructions in that example. It supplies no comparative repair-time, error-rate, learning or total-integration study, nor a measured memory/energy/frame-tail distribution. Its suggestion that graphical applications may be easier to reverse is a transfer hypothesis. S107's later game timings use their own hardware/configuration and effect contract; they are not a repeated S235 benchmark at equivalent guarantees.

## Archived implementation and experiment correspondence

The cited tag resolves to **`df95bb592726dcd918ba768e6dc1c1ad9eb16cf7`**,8July2025. Its complete146-entry Git tree is untruncated and matches the ZIP's named root; `.gitmodules` pins **WARDuino `9154b533201e8bc92401edb3264b9289e639ee88`**. That submodule's653-entry recursive tree is also untruncated. These identities are prior to acceptance/publication; neither is independently bound to the particular reported hardware binary.

Twenty selected source/configuration files are acquired and hashed: **fourteen completely read, six read only at the ranges below**. Whole repository, submodule, GUI, transport, interpreter and test-suite coverage is not claimed.

| Source under the MIO tag unless labeled WARDuino | Coverage and SHA-256 |
| --- | --- |
| `README.md` | Complete41lines; `5dd2420382bb65449903228e050e37103c205d47ec4a846ddc2fd84c1f308b03` |
| `.gitmodules` | Complete3lines; `7d75906a9535f8fc4a8f1d392338fe6ec847cbfa2caa582511804d4413557512` |
| `run-benchmarks.sh` | Complete3lines; `7ec739df4566a9b511e487082cf4dbc7a392a913343b114fb5d611540e0d4a60` |
| `src/test/kotlin/DebuggerTestBase.kt` | Complete27lines; `8f7d793bf29c7918d7f5c7eefe6cb89c63c3f24b51cac3c32ff74d6b0f75e507` |
| `src/test/kotlin/benchmarks/Benchmarks.kt` | Complete115lines; `5a67edbb71df34685a050f2d09789cb97bec0319803b1ba1bee60343f0e30536` |
| `src/test/kotlin/benchmarks/graphs.tex` | Complete406lines; `336f400ee47ef043739db3180a6ff3b82b2f18e9b14554e9e722c24304169d97` |
| `src/test/resources/prime/impl.c` | Complete53lines; `b2675bd0b8ac145d6114050b1d7cff8c925e45a9a0e90cbcdd278040560f694c` |
| `src/test/resources/prime/compile.sh` | Complete1line; `5a3bb5a2f555c31edf9612f25e6890525fe22c06941f567185a024a8c9cff3b4` |
| `examples/dial/README.md` | Complete9lines; `1c08d43f398e4d66478c43c51c3471ab47db2cdf046cd923f81a1a18b6731439` |
| `examples/dial/dial.ts` | Complete95lines; `60f6aefcb9f58e900a36ef8eadd8f45f7a99e455ca4064246a5255c80ae70504` |
| `src/main/kotlin/be/ugent/topl/mio/debugger/Relations.kt` | Complete162lines; `b1ecd26637ff79ebb11ac9a7a44ff4a72561b07f093968ad347039a3fdcefb61` |
| `…/debugger/MultiverseDebugger.kt` | Lines73–97,161–394; `804e9d0537e1e3725568c81dd92291dc3aae66fd7f0af34675667f2eb0cf27a6` |
| `…/debugger/Debugger.kt` | Lines248–313,335–362,378–464; `13698f2576940617c4cba8bb3dcc7d8cb1e70908e5dad90f4741f833f19e6cfd` |
| `…/woodstate/WOODState.kt` | Lines60–202,590–627; `2441bc4aaaf39f4589e7ecdedc4cc9ca4d55e1dbc625c5cc8dea9015ecd420bb` |
| WARDuino `src/Primitives/primitives.h` | Complete84lines; `fd9590847d97a81066e5d363c883eb567788cf96be46dc2313d493b0f1a00b94` |
| WARDuino `src/Primitives/Mindstorms/Motor.h` | Complete95lines; `50f81019b7a100ab6ab5397dc2e5f999037d16d8336329e5dd097e6d71469cb2` |
| WARDuino `src/Primitives/Mindstorms/Motor.cpp` | Complete123lines; `c0b2acf0a2a99c156d69dabfd7f7a5030ae54bd65c73e3fce411a8012ac14201` |
| WARDuino `src/Primitives/arduino.cpp` | Lines500–544; `4885d1ea9bc4b20cb2614eea9acc1c0229b0aa36a074a57b7db81413583edd8e` |
| WARDuino `src/Primitives/zephyr.cpp` | Lines53–118,241–439,463–566; `2eadd58013519c69caf188a4cd2ca0af2749b0df8c58fb0da0f58bb148998a38` |
| WARDuino `src/Debug/debugger.cpp` | Lines958–1027,1354–1404,1581–1663; `516869708a8b9c1afe884dcf84bed6650030de03c7c9065ad026f6051219677b` |

The source corroborates useful machinery: checkpoint restore transmits selected I/O and overrides by default; the backend dispatches registered serializers/compensators, with concrete digital-pin and motor-target implementations. The motor driver reads encoder drift and blocks while driving toward its target. The dependency parser handles one output condition and one single-argument input override. This inspection does not establish every sensor dependency or that every mock satisfies the formal admissibility premise; the inspected backend override handler validates a function lookup without a sensor-range test.

The archived snapshot also bounds reproduction:

- `Benchmarks.kt` measures the six snapshot policies, five instruction counts and ten repetitions. A configuration chooses serial hardware or an emulator; a missing port permits emulator fallback. Backward timing uses ten trajectories, manually clears checkpoints and adds999 to its x-coordinate after each1,000-instruction continuation/backstep. `graphs.tex` consumes named CSVs and the shell script normalizes by the same-instruction baseline. **No CSV exists in the complete tag/archive inventory**, so raw variability and final plot values are not independently reconstructed.
- The source prime loop stops when the **sum of primes** reaches13,374,242, whereas the paper describes checking integers up to that bound. The supplied compile command produces `prime.wasm`; the test uses `prime-no-mem.wasm`. No source/binary equivalence is established. These differences qualify exact workload recovery without erasing the reported sparse/full-snapshot contrast.
- The released dial includes setup, raw-color mapping, a100ms delay and a call using motor index3. The inspected STM32-guarded serializer records only motor targets0 and1; its primitive argument order also differs from the dial's declaration/call order. These are concrete archive/example correspondence gaps, not a reproduced hardware failure or evidence that the reported demonstration never worked. The paper's schematic motor listing is not an exact transcription of this source.
- The README requires Linux/macOS, Java22 and a custom WARDuino build. It already mentions a separate experimental concolic branch, while the paper's evaluated contribution is reversible I/O/checkpointing. Those source features do not retroactively supply S107's later evaluated concolic method. Porting the proposed recipe to C/GDB is discussed, not implemented or measured in this article.

## Disposition and continuation

**Mechanism:** selected external outputs can be integrated into multiverse navigation through explicit inverse/restore behavior and snapshots at effect boundaries. This closes the particular S107 compensation dependency and sharpens Nu's history comparison. It does not establish an unrestricted environmental rewind, automatic cross-version migration or preserved temporal obligations.

**Outcome:** retain the large measured improvement over full snapshotting and the concrete color-dial demonstration, with residual forward/backward costs and absent comparative developer outcomes. Neither conditional proof nor artifact availability measures net Nu maintenance benefit. No firstness claim for Nu, general reversibility claim or experiment follows.

The next substantive gap returns to **program structure and maintenance outcomes**: acquired S83, *The role of program structure in software maintenance*, can change B01's account of how representation affects actual maintenance rather than only source scores. S229's professional-workflow body remains a separate access frontier. Causal-consistent concurrent reversal, robot-assembly compensation and environment-modeling references remain conditional semantic follow-ups if a Nu claim requires them; this paper's bibliography alone does not establish their methods or mandate reading every neighbor.
