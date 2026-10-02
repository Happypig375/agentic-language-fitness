# S234 — MatchFixAgent: validation, repair and the equivalence contract

## Identity and actual coverage

Ali Reza Ibrahimzada, Brandon Paulsen, Reyhaneh Jabbarvand, Joey Dodds and Daniel Kroening, *MatchFixAgent: Language-Agnostic Autonomous Repository-Level Code Translation Validation and Repair*, **ICML 2026, PMLR 306:49428–49451, 6–11 July 2026**. The [publisher record](https://proceedings.mlr.press/v306/ibrahimzada26a.html) supplies the selected [final PDF](https://raw.githubusercontent.com/mlresearch/v306/main/assets/ibrahimzada26a/ibrahimzada26a.pdf). No publisher DOI is listed. [arXiv 2509.16187](https://arxiv.org/abs/2509.16187), DOI `10.48550/arXiv.2509.16187`, is the preprint lineage: v1 19 September 2025, v2 18 December 2025, v3 28 May 2026. Its metadata/abstract were read; its bodies were not independently compared with the final. The OpenReview `MuyXpH3GL1` route presents a browser challenge, while the publisher route works. The final is therefore not access-blocked.

Native parent/note/PDF **`KZ7LG5GF` / `8RIBV5KZ` / `WCIYTQJF`**, collection `PKLXQNEE`, precede intentional full reading after a title/DOI check of 1,250 top-level holdings. The final PDF has **24 pages, 3,228,158 bytes**, SHA-256 **`edce02db05a918d85c22cd1a4bb73a29eae2eb6fa50deec61faa53ab50446f24`**, MD5 `2338c63a8085642ddafa2054e8ebdee5`; native bytes match. **All 24 text pages, five main sections, seven figures, seven tables, three algorithms, references and Appendices A–J are read.** Eighteen physical pages are visually inspected: **1–4, 6–9, 15–24**. This covers all figures, tables, algorithms, displayed code and prompts. Column/table extraction errors are resolved visually. Pages 5 and 10–14 have text coverage only.

The released workbook is native attachment **`943RVC59`**, acquired and attached before data reading: **870,484 bytes**, SHA-256 **`009c1cf8c7607a7628b510d692e21a8e145d543f2c1497d7b2607b0bfc4e93f8`**, MD5 `08bc43d77112ecdc85e64cabc6afaa33`, native-byte-matched. Its exact reading scope and the later source pin are below. Our work is passive reading and arithmetic over stored values, not independent human adjudication or reproduction. No author code, model, compiler, test, replay or container is executed.

## Method: useful complementary checks, with a specified observation target

MatchFixAgent takes a **source/target function pair with access to both projects**, then combines six semantic analyses, generated execution tests, optional repair and a verdict agent (Sections 2–3; Appendices A–B/J). It does not prove a complete translated repository correct.

The semantic analyses concern control flow, data flow, inputs/outputs, library calls, exceptions and specifications. Tree-sitter supplies lightweight language-specific representations. The control-flow comparison abstracts node/edge categories and averages Jaccard similarities; a score at least **0.7** accepts that dimension without an LLM. The paper reports avoiding roughly a quarter of control-flow and a third of data-flow LLM calls this way. Although the data-flow prose mentions edit distance, Algorithm 3 averages best path similarities in both directions. These approximate structural checks are useful filters, not a semantic-equivalence proof; aliasing, concurrency and context-sensitive reasoning are not implemented by the described lightweight analysis.

LLM checks add context and domain reasoning. The I/O prompt asks about effects, edge cases and complexity; specifications can come from documentation, signatures or inference from the source. Exception analysis considers propagation, recovery, type and message, but defaults to an equivalent result for that dimension when neither side explicitly handles errors. An inferred source specification is not an independent statement of intended behavior.

The test/repair agent can inspect files, invoke tools, write tests and modify the target. Its prompt requires execution in both languages and retaining a negative verdict for an originally inequivalent pair even when a patch is produced. The verdict agent consolidates reports. The selected prompts define equivalence using matching outputs and identical intermediate states at corresponding reachable points, without supplying a formal cross-language state correspondence or common admissible-input domain. The human annotations sometimes instead accept idiomatic differences or judge maintainability. Those are consequential choices about the contract, not interchangeable measurements of one universal property.

The reported main configuration uses Claude Code 1.0.51 with Claude 3.7 Sonnet and a 1,000-second timeout, selected through a 300-case timing exercise. Six language pairs use specified environments, including Rust 1.87, Python 3.12.9, Java 21.0.7, Node 22.16, GCC 7.3.1 and Go 1.24.4. Appendix I acknowledges one main trial; a claim of stable results from a large sample is not a measured rerun distribution.

## Benchmark, denominators and positive/adverse outcomes

The benchmark contains **2,219 function pairs in 24 project/language cases**, with 910,398 source lines: 192 Oxidizer pairs in six projects, 1,346 AlphaTrans pairs in four, 337 SKEL pairs in eight and 344 RustRepoTrans pairs in six. Projects are reused across translation and validation studies; these are not 24 independent replications by different research teams. The six Oxidizer projects are the released subset examined in [S232](S232-modular-validated-translation.md); `noach` and `geo` are absent. RustRepoTrans's `libp2p` cases are excluded for flaky tests. Rule-based translators and Syzygy are excluded by the paper's chosen function-level comparison, not evidence that those alternatives lack value.

Appendix C describes a random sample of 1,346 from 4,643 AlphaTrans pairs. The workbook and current reporter instead contain the **complete application-method counts of four projects**: CLI 273, CSV 235, fileupload 192 and validator 646. Six other whole projects are marked ignored and hidden. The 4,643 frame corresponds to S233's 4,654 methods minus eleven dead `commons-graph` methods. This locates the sample composition; it does not reconstruct an undocumented historical randomization procedure. The released extractor uses **GPT-4o Graal-validation outcomes**, not S233's DeepSeek headline or translated-test M1 statuses.

| Outcome | Reported/reconstructed value | What it establishes |
| --- | --- | --- |
| Existing tools' verdicts | 1,140 equivalent, 449 inequivalent, 630 unavailable | Verdict availability 71.6%; unavailable is a separate outcome. |
| MatchFixAgent's verdicts | 1,519 equivalent, 682 inequivalent, 18 unavailable | **99.2% availability**, not 99.2% accuracy. |
| Joint binary verdicts | 1,571; 1,143 agreements = 878 equivalent + 265 inequivalent | **72.8% agreement** on jointly decided pairs; 428 disagreements remain. |
| Retained manually reviewed disagreements | **88/145 favor MatchFixAgent; 57/145 favor the existing tool** | A favorable 60.7% in the reviewed strata, not an overall population-accuracy estimate. |
| Sampled agreements | 106/110 judged correct, four judged wrong | Agreement is useful evidence but can share a mistake. |
| Repair in the 265 jointly inequivalent pairs | **134/265 = 50.6%**, versus **49/265 = 18.5%** | A reported improvement of **32.1 percentage points** under these checks/cohorts. |

These headline counts are independently recomputed from the workbook's 24 included project rows and human-rating cells, rather than merely copied from its cached totals. All selected total columns match. Stored observations remain stored observations, not reexecuted results.

For disagreements, two **authors** independently examine up to five cases in each of two strata per project: tool-equivalent/agent-inequivalent and the reverse. The paper calls these D1/D2; they are unrelated to this repository's proposed experiments. Of 159 initial cases, 14 are excluded, leaving **92 and 53** respectively. The paper attributes three exclusions to unavailable Oxidizer mocks and eleven to non-one-to-one Rust translations. The actual annotations label eight of the eleven as non-one-to-one and describe three incomplete implementations; one explicitly suggests an artifact-side bug. Exclusion is therefore preserved with its actual reason rather than silently treated as a correct verdict.

The retained results strongly vary by predecessor:

| Source of pairs | MatchFixAgent favored | Existing tool favored |
| --- | --- | --- |
| Oxidizer | **37/44 (84.1%)** | 7/44 |
| AlphaTrans | **25/34 (73.5%)** | 9/34 |
| SKEL | **23/43 (53.5%)** | 20/43 |
| RustRepoTrans | **3/24 (12.5%)** | **21/24** |

Preserve both the substantial Oxidizer/AlphaTrans gains and the RustRepoTrans counterexample. Fixed per-project/per-direction sampling is not prevalence weighting over all 428 disagreements. Reviewers investigate the argument for inequivalence, then favor equivalence if that argument is unsupported; this is not exhaustive proof of equivalence. The paper itself acknowledges the absence of known true accuracy. Blinded external review or our own new human review is not claimed.

The workbook reconstructs **118/145 = 81.38% initial reviewer agreement** and 27/145 = 18.62% conflict on retained disagreements. One retained case has an initial `Ignore` rating. The paper's stated **83.7%** agreement does not reconstruct from these retained ratings; including all 159 also does not recover it. The additional agreement check has **105/110 = 95.45%** initial agreement, matching its reported 95.5%, and contains 88 jointly equivalent and 22 jointly inequivalent cases. The paper's shorthand about sampling equivalent cases does not describe all these rows.

The qualitative data explain why the contract matters. Consensus rows accept nil-slice/empty-vector differences, some error-representation changes and behavior outside valid calling contexts. Conversely, rows 96 and 103 favor MatchFixAgent for an unnecessary leaked allocation and unused variables; that is a broader quality judgment. Row 60 describes an agent repairing a function and then incorrectly declaring the **original** equivalent. The heap-order annotation at row 90 notes that tests with unique values fail to distinguish the disputed tie behavior. These are author judgments read from the data, not faults independently reproduced here. They motivate explicit admissibility, observation and original-versus-repaired-version records.

Repair results also have conditional scopes. Among the 265 jointly inequivalent pairs, MatchFixAgent repairs 17/21 Oxidizer, 46/63 AlphaTrans, 5/11 SKEL and 66/170 RustRepoTrans cases; the predecessor's 49 successful repairs are in RustRepoTrans. For AlphaTrans, the authors manually assess repairs because the original Graal route is unreliable; the workbook contains **46 yes/17 no** over 63 cases (CLI 7/9, CSV 16/20, validator 23/34). For the other groups, patches are judged using previously failing original tests, rather than their own generated tests alone. These are useful checks, but development access to the original tests is not an independently withheld final oracle, and passing previously failing cases does not certify every retained behavior. A further **47/49** accepted patches concern the selected tool-equivalent/agent-inequivalent cases adjudicated in the agent's favor.

S234's broad statement that prior systems do not report repair effectiveness should not overwrite S232's **20 reported semantic repairs** (15 `geo`, four `noach`, one `textrank`) across its final eight-project evaluation. Those projects/stages differ from S234's six-project released subset and current driver. Preserve the final-paper and inspected-release scopes separately.

## Coverage, cost and ablation interpretation

The workbook reproduces the reported **89.6% to 98.1% coverage**, an 8.5-point macro-average change across included projects. Its underlying means are 89.5510 and an 8.4881-point increment. It adds **479 newly covered fragments**; the selected reporter counts a fragment as newly covered when the prior status is unexercised/pending and the test/repair agent returns a binary verdict. That is the release's accounting rule, not our independent audit of execution traces or obligation coverage. Coverage and assertion sensitivity remain different.

The main table records **$2,710.45 and 686,885 cumulative seconds**, averaging $1.2215 and 309.55 seconds per pair. These are the authors' reported costs, not charges incurred by this reading. Development comparisons count 1,650 framework lines against 3,843/10,859/19,052 in earlier tools and report author effort estimates. The advertised 2.3/6.6/11.6 ratios are line-count ratios; external agent/model/parser work and different engineering scope prevent treating them as controlled net development savings.

The Qwen3-Next-80B-A3B extension reports 1,452 equivalent, 708 inequivalent and 59 unavailable verdicts. The workbook reconstructs **1,109/1,548 = 71.64%** agreement with existing tools on jointly decided pairs. It has no analogous completed human-rating columns; blank/zero cost cells in that results sheet are not evidence of free execution. Appendix G's claimed **23.8-fold lower cost** is not a whole-pipeline ratio recovered from its printed Table 7 component means: summing those displayed means gives $0.24418 versus $0.18892, approximately **1.29**. The six semantic components alone have a different ratio. This arithmetic is not corrected provider billing; the paper acknowledges cached-input reporting problems and says bills were checked, while those billing logs were not acquired. Main-table and component-table cost scopes also differ.

The 96-case Codex/o4-mini exercise changes the agent framework and model together, and uses 58 equivalent/38 inequivalent instances despite prose about equal contribution. Agreement with earlier tools is not independent human accuracy. The later `sample_openai_study.py` instead requires 100 samples, with unseeded selection and per-project branches. This is an edition/reconstruction limit, not evidence that the published run used that exact script.

The non-dispute ablation defines its reference using cases on which the full system and comparator agree. Its full-system 100% is therefore conditioned on the selection, not external accuracy. It uses 1,091 cases rather than Table 1's 1,143 agreements; the dispute ablation uses 416 rather than 428. The gap is not resolved by the inspected current sampling code. Threshold TPR/TNR uses the system's final decisions as reference, not the reviewed human labels. These experiments describe conditional component behavior and availability; they do not establish that a particular multi-agent architecture is necessary or that filtering alone guarantees semantic validity.

## Released artifact: identities, inspected scope and unresolved packet

The [official repository](https://github.com/Intelligent-CAT-Lab/MatchFixAgent) is inspected at **`a14a82215c1e89858de2bf6eaf10682a4c6ecb11`**, committed **11 September 2026**. No tags or GitHub releases were returned. The complete nontruncated tree has **23,114 entries**; inventory is not body reading. This pin postdates the conference paper and is not silently treated as its execution version.

The README and four source files are fully read. Two more files have bounded source reading, one has navigation only, and two data JSONs have schema/status-field inspection only. Git blob identity, byte size and SHA-256 were checked on acquisition:

| Member | Bytes / SHA-256 | Actual body coverage |
| --- | --- | --- |
| `README.md` | 10,923 / `992c36055af6abf0ee2a76b75d5489eaca1fbfd1aed5ecec0c9fcd702eb1814f` | Complete. |
| `src/analysis/sample_ablation_study.py` | 3,274 / `b130988c55cf0a7498e76941b5b94976f2752a078a54c54ac44ba523a555e3bd` | Complete; binary combinations use test/repair verdicts. |
| `src/analysis/sample_openai_study.py` | 4,426 / `0128d7cab713ab1615bb0cd8595994e47f7de5e5cacb8ac03a1b7058e36454d3` | Complete; current 100-sample requirement differs from paper. |
| `src/parse_results/extract_alphatrans.py` | 3,556 / `e9836dc454f968c0a86b3739ab333df04c77cc3e07498ea355227280170a67cc` | Complete; GPT-4o Graal outcomes, not M1. |
| `src/agents/match_agent/verdict_agent/agent.py` | 6,963 / `4931e2837b95df1422dea82555ef65ccf873c483cb0c61873aa91b5052cd4e39` | Complete; report consolidation and parsing/error handling. |
| `src/analysis/analyze_validator_agent.py` | 40,266 / `5ceb79572904cad0b5aa85935d3b53a7161cff0b0811ddeb44a076328c9f0bf3` | Lines 55–100, 310–404, 430–472, 598–628, 716–739; other matches are navigation only. |
| `configs/prompt_templates.yaml` | 21,905 / `5391853a6c442fadfeaebb9476c31aa611f4a31872694108355595a40735a8d9` | Lines 1–41 and 244–326, plus navigation; not all prompts fully read. |
| `src/agents/match_agent/prompt_generator.py` | 14,431 / `cb30c35ad2e012a932ce70c1057caaf2c1a301d93cc853d60a84ea404edec162` | Acquired; regex navigation only. |
| `data/agent_results/match_agent/alphatrans/commons-fileupload.json` | 229,185 / `da1434afcbd5a14e246e42c8515fec13badc04f17e1504d1838b18918d2a1759` | 192-record schema inspected; source/target bodies unread. |
| `data/agent_results/match_agent/oxidizer/checkdigit.json` | 44,269 / `b118879bd716dd22574aacb15e2163a94e96d730a3820e9c5af2c44980b0eb7f` | 29-record schema inspected; source/target bodies unread. |

The reporter at lines 440–455 **prefers a binary test/repair verdict**, using the final verdict only when that earlier verdict is nonbinary. Its sample exclusions are at 374–384; coverage counting at 600–603; selected cost accounting sums test/repair and verdict fields. These located rules qualify a simple architectural reading in which the final consolidation always determines the reported label. The two acquired data JSONs lack completed `match_agent` outputs, so their names do not establish that the final execution packet has been recovered. Optional reset/retry code exists; no claim is made that it was used to select published outcomes.

README's concept DOI `10.5281/zenodo.17051106` resolves to [versioned record 20165225](https://doi.org/10.5281/zenodo.20165225), published **15 May 2026**. The four-file inventory comprises the acquired workbook and three **unacquired** ZIPs:

| Unacquired file | Advertised bytes / MD5; not locally verified |
| --- | --- |
| `main-experiments.zip` | 49,153,916,189 / `bf4c82b13d1439c501d44accc556083c` |
| `rebuttal-experiments.zip` | 148,063,913,354 / `d0637fc7df14f5da3727a04ac4b3b4d4` |
| `original_tool_projects.zip` | 152,771,204 / `6a2e599d4187d3e5be1b1514f8623b88` |

No ZIP member inventory, full archive hash, image import or run is claimed. README also identifies some omitted ablation/threshold images. No author contact or new access purchase was attempted. These are bounded artifact gaps, not a claim that the complete publication is unread or that the accessible survey must stop.

**Workbook coverage:** all ten sheet structures and stored cell/formula XML were parsed, without recalculation or visual rendering. All six human sheets' identity/rating columns were paired; the 159 disagreement-consensus rows, including their comments, were read. Agreement-consensus comments were read for its first four rows and all four negative judgments; other agreement and individual-reviewer comments remain unreviewed. All 63 manual-repair ratings and the first four repair comments were read. The 24 included main project rows, ignored-row identities, selected total/formula cells and both models' headline totals were inspected. Cost-sheet coverage is headers and opening rows only; Table 7's printed component arithmetic is separate. Main-sheet rows 20–25 and 32 are explicitly hidden, matching the excluded-project labels and subtotal scope. Complete XML parsing is not complete annotation reading. Local ignored manifests and our `s234-workbook-audit.json` preserve the arithmetic; copyrighted bodies and extraction dumps are not committed.

## Consequence for Nu and the wider survey

This is positive primary evidence that complementary semantic reasoning and targeted execution can identify translation defects missed by existing validation and can produce useful repairs. It is also direct adverse evidence against using an agent verdict, cross-tool agreement, test reachability or a broad quality judgment as an automatic semantic oracle. Strong differences across predecessor datasets matter more than one pooled headline.

For **B02/B07/B09/B10/B12**, define the permitted input/state correspondence, observed effects and original versus repaired version before interpreting a verdict. Separate diagnostic availability, generated tests, executed assertions, independent judgment and missing observations. That distinction applies to Nu's types, edit feedback and retained state without claiming a Nu-specific effect or transferring these repair percentages to the fixed-F# D1 proposal. Comparative human maintenance benefit and total adoption cost remain unresolved empirical questions.

The immediate translation-validation dependency is now reconstructed at its final-publication and bounded-artifact scopes. The next consequential reading returns to the acquired **S105 temporal-breakpoint method**, to resolve how triggers, alternate histories and pending observations are represented during interactive debugging. S106's monitor semantics and S99/S107's live/remote methods remain distinct gaps. SKEL/TRAM and other translation neighbors remain conditional; a new neighbor is not automatically the next priority. All experimental and additional-worker holds remain.
