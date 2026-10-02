# S231 — HarmonyOS compiler feedback: compilation gains and manual behavior checks

## Identity, edition and actual coverage

Mehmet Cem Aytekin, Fatma Gizem Calli/Çallı and Mustafa Umut Demirezen, *Automating Code Generation for a New Ecosystem: Establishing Baselines with Large Language Model Based Code Generation for ArkTS and HarmonyOS*, Research Square v1, posted 4 September 2025, DOI [10.21203/rs.3.rs-7362986/v1](https://doi.org/10.21203/rs.3.rs-7362986/v1). This is the **fully read edition**. The linked final article is *Automated Software Engineering* 33(2), article 59, 27 February 2026, DOI [10.1007/s10515-026-00599-9](https://doi.org/10.1007/s10515-026-00599-9), with the second author's surname given as Yılmaz. The final body remains access-limited. This work is distinct from [S230](S230-arkts-code-generation.md); a shared coauthor does not establish independent replication or shared benchmark data.

Native parent/note/PDF: **`BWMPQFHC` / `DPY6K2LK` / `9RVEAHWT`**, collection `PKLXQNEE`. The record precedes intentional full reading; discovery had already exposed the abstract, bounded opening text and repository README. The selected PDF has **33 physical pages** (Research Square cover plus 32 manuscript pages), 1,826,675 bytes, SHA-256 **`929a204a961cda7cc9d66fbfc6e2382d3a9aa6d2884f29109a9006ded9f5509e`**, MD5 `94f904a2f4868db104190f0fcb8bc8cb`, verified against the native attachment.

All 33 pages, six main sections, Appendix A.1, seven tables, eleven figures, Equation 1, the repair prompt, code fragments and 32 references are read. Thirteen physical pages are visually inspected: **8–10, 13, 15–16, 18, 20–22, 26–28**. Figure 5 is also inspected at higher resolution; its first label overlaps the axis tick but the point, caption and table give 37%. An initial oversized display of pages 7–13 was truncated and received no reading credit; bounded subsequent displays recovered those pages. A PDF color-profile warning during acquisition did not prevent extraction or the selected renders. Reading/reconstruction is not reproduction: no model, compiler, emulator, author program or candidate was run.

The final publisher preview exposes the abstract, references, Appendix A.1, data link and nine figure links. The ordinary final-PDF and Scite-provided institutional routes returned HTML, not a PDF. Of three public figure routes tried, only **final Figure 4** returned an image (37,609 bytes, SHA-256 `c239b1f086d2530caf9b5efd9ea969c43eaa330765e6371a8def192027432598`), visually inspected at its small 312-pixel width. It contains the large-model ICF curves numbered Figure 3 in the preprint. Final/preprint numbering and references differ; full textual or numerical equivalence is **not established**. The final abstract's phrase “syntactic Pass@1” must not silently replace the preprint's sequential Success@10 definition. All detailed results below are attributed to v1.

## Method and estimands

ArkTS-Test has 100 natural-language tasks, claimed to cover more than 20 UI components, with 30% basic, 50% intermediate and 20% advanced tasks. Section 3.1 describes expert reference implementations typically spanning 200–500 lines and task metadata. References are not given to the model. The tasks concern fresh component/application generation, not modification of a maintained predecessor with retained obligations. The training set has 1,000 instruction/code pairs adapted from OpenHarmony examples, with instructions manually constructed from explanatory material and visual demonstrations. The paper states that train and test content do not overlap.

Ten base models are compared on one initial completion per task. The automated gate writes code into an existing project, invokes the HarmonyOS build and calls a zero exit status syntactic success. That label covers the configured build result, not syntax alone or demonstrated runtime correctness. The paper's Equation 1 is the usual probability estimator for at least one success among k draws, while adjacent prose incorrectly defines k as a minimum number of correct solutions. This does not change the explicitly described one-attempt baseline.

**Iterative Compilation Feedback (ICF)** uses a fresh model interaction after each failed build. Each repair receives the original instruction, the entire current failing source and compiler error text. It stops at the first successful compilation or ten total attempts. **Success@k** is cumulative compile success along this dependent repair trajectory, rather than success among k independent samples. This is a concrete prior feedback method. There is no matched ten-call, no-diagnostic control here to isolate feedback from additional generation opportunities.

The uncertainty procedure resamples the 100 recorded first-success attempt numbers, including failure at all attempts, 2,000 times. It does not rerun models, sample new prompt formulations or estimate deployment reliability across future ecosystems. The prose's interpretation of bands as variation across prompts/model reliability exceeds that procedure. Exact per-task trajectories and the plotted interval calculations are not available in the inspected release.

The behavior check is separate and manual. One designated ArkTS-expert tester deploys **only compilable outputs of the three best Success@10 models** to a virtual device, checking prompt requirements, appearance, event handling and state changes. No agreement study, blinding, per-item checklist, event schedule, trace or adjudication packet is reported. This is useful reported human assessment, not independently reproduced validation. The repair loop is described as receiving compiler feedback only; the later manual semantic assessment is not described as repair feedback.

## Reported positive, null and adverse outcomes

| Model/condition | First-attempt compilation | Compilation within ten attempts | Manual successes among compilable outputs | Confirmed manual successes per 100 tasks, calculated from Table 7 |
| --- | --- | --- | --- | --- |
| Claude Sonnet 4 | 35% | 91% | 88/91 = 96.7% | 88% |
| DeepSeek-V3-0324 | 15% | 83% | 76/83 = 91.6% | 76% |
| Claude 3.7 Sonnet | 27% | 80% | Not assessed in the reported semantic comparison | — |
| Gemini 2.5 Pro | 11% | 71% | Not assessed | — |
| Qwen3 Coder | 9% | 66% | Not assessed | — |
| Gemma3-12b | 1% | 26% | Not assessed | — |
| Qwen2.5-Coder-14B-Instruct | 1% | 2% | Not assessed | — |
| DeepSeek-R1-Distill-Llama-8B | 0% | 3% | Not assessed | — |
| Mistral-7b Instruct | 0% | 0% | Not assessed | — |
| Fine-tuned GPT-4o-mini, selected batch 32/one epoch | 37% | 82% | 74/82 = 90.2% | 74% |

Base GPT-4o-mini scores 4% on the first attempt. The fine-tuning sweep reports 31–37% across nine batch/epoch configurations; two tie at 37%, and the one-epoch configuration is selected. ICF then raises that selected model by another 45 percentage points. The main positive evidence is substantial **reported compilation improvement**, plus high conditional manual success for the selected outputs. The three all-task manual yields above retain the favorable direction without presenting 96.7% as success on all tasks. They are arithmetic from published counts, not a new run or a causal semantic improvement estimate: comparable manual outcomes for the baseline are absent.

Preserve the flat or small gains for the other smaller models. The between-model comparison does not isolate parameter count, training exposure, general reasoning or coding specialization. Several parameter counts are explicitly estimates; it does not establish a minimum model size. Nine fine-tuning configurations are compared on the reported evaluation set, with no separate development set identified for configuration choice. Holding tasks out of weight training does not by itself make the selected configuration's estimate independent of model selection.

Section 4.4 reports correction rates of 85% for property/type errors, 78% for imports/scoping and 62% for API/component hallucination. Table 6's percentages instead describe the distribution of all error messages across repair attempts. Counts, error-instance matching across edits and classification reliability are absent, so these are distinct reported summaries, not task-level causal effects. Code examples use native components, decorators and state; one repair replaces a missing external module with inline definitions. Architecture can change during repair.

Six described semantic failures concern incomplete drag/drop, a triangle indicator, removing rather than replacing text, pull-to-refresh, sliding animation and radio styling. The text-removal case is a direct example of compilable code violating a state obligation. The triangle example also invokes a preferred native implementation beyond the short displayed prompt; without a complete rubric, a behaviorally acceptable alternative cannot be ruled out merely for using another implementation. Still images do not validate temporal behavior. Figures 6 and 9 display the same drag/drop-looking screen under different failure captions; that visual does not independently establish the claimed pull-to-refresh observation.

The paper reports approximate service prices and fine-tuning expenditure, but no paired end-to-end developer effort, task-level tokens/latency or deployment-cost comparison. “Practical utility” remains a transfer claim. The positive counts should not be erased because those broader benefits are unmeasured.

## Released implementation and data correspondence

The official [repository at commit `2ee9645`](https://github.com/cemaytekin/llm-finetuning-arkts/tree/2ee96450843fa43c4b492e2febb6ad8dabfe8433), dated 8 December 2025, is inspected passively. The complete recursive path inventory has 309 blobs and is not truncated; most are vendored libraries/build material. The six-entry commit history ends with README updates after August uploads. This is the linked public release, not a verified archive of the measured experiment.

Complete reading covers nine files: README, `compiler_tool.py`, `FileCache.py`, root/entry build profiles, the hvigor configuration, `Index.ets`, and the local/ability test files. Both CSV files are parsed for schema/counts; all 100 test prompts and training rows 1, 500 and 1000 are read. The remaining 997 training bodies, native C++ implementation, vendored libraries and build logs are not read. Local per-file SHA-256/blob manifests are retained outside Git.

| Material | Bytes | SHA-256 |
| --- | ---: | --- |
| `compiler_tool.py` | 11,902 | `66c0a9297677ba5dc8563d190e35d41c184da7d15825b68c044b8a0e50c97d97` |
| `FileCache.py` | 3,712 | `11f52c73dc599b46021c04f42b221f69f7a340f1314e96eb00ce980dda19337d` |
| `arkTS_test_data.csv` | 15,933 | `82533da4e5d5d4fb646e27ffd87fd4eabe76ff9ea46d08d5688a138a54faf4d6` |
| `arkTS_train_data.csv` | 1,967,827 | `2034299cce5a743a0ab67794b2b2769bb4caf81209b5cd97fff2ff4cd5dc3680` |

The code establishes a real, concrete compiler-feedback pattern, with material correspondence limits:

- **Feedback and stopping:** `evaluate_llm_performance` (lines 192–236) has three explicit attempts, each conditioned on the previous nonzero exit status. It carries full current source and adds source-line context to the error. It has no ten-attempt driver, bootstrap calculation or semantic assessor. The main block sends one fixed yellow-circle task to one model; it does not parse the README's advertised `--input` argument. The evaluation helper expects a `Test Instructions` column, whereas the public test CSV has `instruction`.
- **Build contract:** `compile_file` invokes `assembleHap`, with `arkts.compiler.ets.type-check=false` and a nullable-related option. The flag's effective semantics in the measured toolchain are unverified; an exact primary-domain search returned no results. It is not sound to infer that every type check was disabled merely from that string. Paths and model identifiers are fixed, while the root build profile specifies HarmonyOS 5.0.1/API 13. The README's broad version advice does not pin the original run environment.
- **Outcome retention:** the helper records counts of the substring `ERROR`, not complete exit statuses/diagnostic histories. A failed build without that substring could yield a zero count in the CSV while the loop itself still treats it as failure. Early successes fill later columns with zero, and only the latest source is retained. Those fields alone cannot reconstruct all reported trajectories. The cache has a revert method, but the inspected compiler routine never invokes it; restoration after every attempt is not established by these callers.
- **Data:** the test CSV has exactly 100 nonempty, unique normalized instructions and **no reference-code or metadata columns**, despite the paper/README's instruction-code-pair description. Test reference lengths, difficulty membership and semantic rubrics cannot be checked from it. The training CSV has 1,000 populated instruction/code pairs, 967 unique normalized instructions and 969 exact code cells. Code-cell line counts range 15–218, median 61; these are training examples, not the missing test references. Comparing instructions with Unicode NFKC, case and whitespace normalization finds no train/test exact-normalized match. That limited check does not establish semantic independence or absence of code clones.
- **Behavioral tests:** the two inspected test files contain basic string-containment/self-equality assertions; they are not task-specific UI/state/temporal oracles. `Index.ets` is a short native yellow-circle/text component. No generated-output/100-task decision packet is identified in the complete path inventory. Logs and cache files exist but were not inspected or treated as substitute result records.

Source inspection establishes these differences; no executable failure, performance replication or security test is claimed. Credentials and full source/data bodies are not copied into the repository or Zotero note.

## Survey consequence and next action

S231 gives **positive prior evidence for compiler-guided repair of native declarative UI code**, with observed residual state/interaction/appearance failures and an explicit separate manual behavior gate. This is stronger than a syntax-only catalogue, but it does not estimate a Nu architecture effect, preservation under software evolution, net professional benefit or D1's explicit-case versus catch-all treatment. Compiler diagnostics, source changes, final behavior and missing observations remain separate.

Use this result alongside S230's favorable small pilot, rather than averaging their incompatible benchmarks or describing the common-author papers as independent replications. The public release resolves a method gap and exposes specific reproducibility obligations; the final-edition body and original per-task packet remain access/coverage gaps. No additional model, adapter or experiment is authorized.

Next follow C05 position 1, **Scalable, Validated Code Translation of Entire Projects using Large Language Models**, DOI `10.1145/3729315`. Its modular type-compatibility checks and I/O validation can test the next consequential distinction: local diagnostic compatibility versus whole-project semantic preservation when language features and representation change. Resolve edition and native holdings before reading. C05's CatCoder/type retrieval and multi-turn methods remain conditional, while S229's professional-workflow body and the existing live/temporal frontiers remain open.
