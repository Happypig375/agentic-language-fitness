# S241 — CatCoder: type context before generation

Zhiyuan Pan, Xing Hu, Xin Xia and Xiaohu Yang, *CATCODER: Repository-Level Code Generation with Relevant Code and Type Context*, [arXiv2406.03283v2](https://arxiv.org/abs/2406.03283v2), 21 November 2025. The original June 2024 title was *Enhancing Repository-Level Code Generation with Integrated Contextual Information* (retained C05:64). Main-agent reading, 2026-10-04.

CatCoder combines retrieved implementation examples with statically extracted type/member declarations before generating a missing function. Its measured gains are useful evidence for providing repository information. They do not estimate a language effect, diagnostic-repair effect, equal-input-budget effect or benefit from D1's explicit-case convention.

## Identity and actual coverage

Read **all 26 text and rendered pages**, eight main sections, **eight figures, eight tables, Algorithm 1 and all 53 references**. The manuscript contains no appendix. Its ACM DOI field is an unfilled template, not the publication DOI. Crossref independently identifies the same-author journal lineage as [DOI10.1145/3779217](https://doi.org/10.1145/3779217), **ACM TOSEM35(8), 1–25, 16 July 2026**. Publisher landing/PDF requests return403. The accessible v2 governs this reading; equivalence to the final journal body is unverified, and the original v1 body is not separately read.

Native collection `PKLXQNEE` was checked by DOI/title/edition before selection. Parent **`43B3QJYB`** and note **`TJJZMDRN`** precede the primary read; subsequent metadata corrections preserve their identities. Attachment **`FBUXXJE6`** contains the [v2 PDF](https://arxiv.org/pdf/2406.03283v2): **1,989,470 bytes**, SHA-256 **`8e136f96c83b382b48914f02ce173da5c89800d7502dd5edeb1ab6c0194374b7`**, MD5 **`bda3dff9969d63a095a716e676f748ee`**. Native stored bytes match.

The [released artifact](https://github.com/pan2013e/catcoder/tree/6c3874ec83165534bb4154d584740b542f7bba40) is pinned to **`6c3874ec83165534bb4154d584740b542f7bba40`**, 5 December 2025, an untruncated135-entry tree. This is later than the read manuscript, not a certified execution snapshot. Read **27 complete files /2,918 lines** listed below, including both evaluation paths, prompts, retrieval, type extraction, scoring, test adapters and selected analyzer implementation. Parse both Arrow datasets at schema/row/selected-field scope and the headers, aggregate metrics and sample-group structure of twelve CodeLlama13B result JSONs. Inspect the first two task descriptions/test fields per language. Generated result bodies, all individual task implementations, other-model JSON bodies and the crate archive are **not** comprehensively read. No author code is imported or run, and no compiler, analyzer, model, benchmark, package installation or experiment is invoked. Our parsing, hashing and arithmetic are passive inspection, not reproduction.

## Mechanism and information contract

Sections3–4 define an empty function, its description/signature and the surrounding repository as input. Recursive source splitting prefers type/function boundaries, then control-flow boundaries and newlines. The sparse retriever uses BM25; the dense retriever uses MPNet embeddings and distance ranking. Weighted reciprocal-rank fusion combines dense/sparse results at **70/30**, followed by deduplication. Java uses a2,000-character chunk setting and top4 per retriever; Rust uses1,000 and top8. These are per-retriever counts, not a guaranteed total of4/8 prompt chunks or token budgets. The character unit is located in the released `RecursiveCharacterTextSplitter` calls; the manuscript states the sizes without that unit.

Type context serializes fields, constructors/method signatures and related types. The paper's graph explanation bounds expansion to nearby dependencies and prunes standard-library types. The inspected Java implementation starts from the containing class, target parameters/return type and class fields, uses JDT.LS definition lookup, and serializes declarations without method bodies or field initializers. Its helper has first-definition and generic-argument handling limits. Rust uses signature/self types, related field types and rust-analyzer definitions/implementation structures, usually excludes trait implementations and standard-library dependencies, and uses the first returned definition. The selected Rust workspace loader supports one package and one library target. These concrete rules qualify a broad claim of universally complete type context.

The prompt contains the type context and retrieved code before the docstring/signature. A frozen model supplies the body; common postprocessing trims tags/Markdown, removes an incomplete final line, appends closing braces heuristically and restores a signature when needed. There is no compiler-feedback repair loop in this generation path. The compiler/tests score completed samples afterward. Figures1/3/4 illustrate how a matrix API plus an existing construction example can guide a new method; this demonstrates the proposed information relationship, not that both components are necessary for every task.

The retrieval loaders remove the target's declared line range and filter returned chunks containing its signature/name. Type extraction reads the checked-out repository but the selected declaration serialization does not emit the target body. A whitespace-normalized exact-full-function scan across the four stored context fields finds no match longer than80 normalized characters in either dataset. This narrow negative check does **not** exclude partial copies, near duplicates, pretraining exposure or other leakage; the authors explicitly leave benchmark leakage investigation open (§8).

The public retrieval cache is keyed by Java project/package or Rust path, rather than a complete task/revision identity, and the return helpers convert ranked results to sets. Cache lifetime, target filtering, ordering and task/version binding therefore require care in regeneration. These are static implementation observations, not proof that the published runs leaked answers or used the wrong order. The released Rust preprocessing helpers also expect some older field names that differ from the stored Arrow schema; the main evaluator uses the stored schema. Full regeneration requires a verified preparation path rather than assuming that the stored evaluator and every helper are interchangeable.

## Comparison, samples and oracle

The Java benchmark adapts **238 CoderUJB tasks from Defects4J**, sequentially removing17 over the512-output-token limit, five lacking convenient modifiers/annotations, and17 standalone functions: **199 tasks**. The stored data spans14 project labels. This deliberately emphasizes repository-dependent functions; it is not a sample of all development work. The Rust authors select **90 documented functions from13 crates**, requiring detailed descriptions and documentation tests. Mean function size/complexity is16.59 lines/4.59CCN for Java and10.68/2.64 for Rust (Table3). Language, task distribution, analyzer implementation and oracle differ together; their effect sizes are not a controlled Java-versus-Rust comparison.

Three baselines use the common prompt format: empty context, preceding in-file context, and an adapted RepoCoder retrieval approach. The manuscript describes RepoCoder's successive generation/retrieval queries. The released final evaluator instead reads a **precomputed `repocoder_data` field** for every sample; a helper accepts prior generated code, but the inspected release does not bind its original model, iteration count or total construction/inference budget. The ablations remove retrieval (`-CR`) or type context (`-TC`), preserving the remaining stored component. They are useful component-removal contrasts, without a sham or length-matched replacement.

There are **ten stochastic outputs per task**, temperature0.6/top-p0.7, at most512 new tokens each. Both compile@k and pass@k use the standard without-replacement estimator for at least one success amongk samples, then average over tasks; k is1/3/5. A pass@5 value is not the accuracy of an unselected single delivered answer. Repeated outputs and six models do not turn shared tasks into independent project or human samples. The manuscript supplies no task-level uncertainty interval or paired significance analysis for these contrasts.

Java patches the fixed Defects4J checkout and tests the task's listed test methods, rather than automatically running its full suite. The adapter uses30-second compilation and60-second per-test-method limits. Rust patches the function while retaining its original documentation and invokes `cargo build`, then a documentation-test filter derived from the starting line, with30-second limits. The adapter accepts a zero exit status without verifying an expected nonzero test count. The inspected artifacts do not include per-sample compiler/test logs or realized test-count validation. Consequently these are author-reported compilation and benchmark-test outcomes; passing is not proof of all intended behavior or temporal obligations.

Rust's examples/assertions are part of the supplied docstring: the first two stored tasks visibly contain the same examples in `test_body`. These are **visible specification examples**, not an independently hidden oracle. That is a legitimate function-completion setting; it cannot substitute for D1's separately held-out new-and-retained obligations. Timeouts count through the adapters' failure booleans rather than a separately analyzed missingness category. No reported frequency of such failures is recovered.

## Positive, null and adverse observations

Table5 gives the following percentages for CodeLlama13B; each triple is k=1/3/5:

| Method | Java compile | Java pass | Rust compile | Rust pass |
| --- | --- | --- | --- | --- |
| Empty context | 33.6 /49.4 /56.2 | 14.9 /22.1 /25.2 | 18.0 /28.3 /33.1 | 10.8 /15.8 /18.2 |
| In-file | 59.7 /72.7 /76.8 | 35.3 /43.8 /47.6 | 52.1 /66.5 /70.9 | 41.6 /55.7 /61.6 |
| RepoCoder adaptation | 63.0 /74.1 /78.2 | 41.0 /46.9 /49.0 | 63.7 /73.4 /76.4 | 49.4 /59.5 /63.0 |
| CatCoder | 71.9 /84.8 /88.4 | 44.7 /54.0 /57.5 | 65.1 /75.5 /78.9 | 52.7 /62.0 /65.9 |

Thus the reported improvements over RepoCoder are **3.7 percentage points Java pass@1** and **3.3 points Rust pass@1** using the printed rounded values. The headline maximum17.35% is a **relative** Java pass@5 improvement, not17.35 percentage points. Stored aggregate values give approximately3.719/3.222 points at pass@1 and17.360% relative Java pass@5. Small differences from prose percentages arise when rounded table entries are used. These arithmetic checks read saved summaries; they do not recompute test success from generated programs.

Table7 retains useful ablation evidence: removing type context lowers Java pass@1 **44.7→39.5** and Rust **52.7→49.9**; removing retrieval lowers them to **27.5/23.3**. Retrieval contributes the larger observed drop in this setting, while type information supplies an additional gain. Figures5/8 include both helpful selection of the correct API/field and failure despite plausible API use. In particular, the published failure lacks a required null case, and the displayed code also differs in state assignment; the null check alone is not an experimentally isolated cause of all failed tests.

Figure6 compares six models ranging from6.7–13B and reports favorable CatCoder pass@1 differences for every tested model, with average relative gains of13.73% on Java and8.4% on Rust. Preserve this model-spanning positive observation without extending it to present-day models, arbitrary languages or interactive editing. The inspected tree contains Java results for those six models but Rust result files only for CodeLlama13B, and other-model ablation result bodies are absent from that tree. The Figure6 raw-result coverage is therefore incomplete.

The **CodeBLEU result goes the other way**: RepoCoder scores0.57 versus CatCoder0.56 for Java and0.46 versus0.44 for Rust (Table6); Rust syntax scores tie at0.60 and dataflow is omitted because the chosen tool does not support it. Keep this metric disagreement alongside the favorable compile/test results. Similarity to an existing implementation and satisfying an oracle are different endpoints. Most individual samples still fail at pass@1 in the Java comparison; context does not guarantee correct reasoning, handling of dynamic/reflection features or complete requirements.

## Context and cost boundaries

Passive inspection of all stored context lengths gives the following **character** counts, not tokens or inference costs:

| Stored field | Java median (range) | Rust median (range) |
| --- | --- | --- |
| Type context | 5,051 (353–15,000) | 1,824 (37–5,371) |
| Retrieved code | 7,094 (3,431–10,000) | 6,432.5 (3,489–8,929) |
| RepoCoder context | 7,167 (2,569–10,000) | 6,440 (3,206–13,334) |
| In-file context | 3,505 (1,736–5,156) | 2,833.5 (631–3,953) |

All four fields are nonempty for every stored task. CatCoder adds type context to its retrieval field; adding these separate medians is not the median total prompt length. Neither the paper nor the selected evaluator establishes equality of input-token allowances, task-level prompt truncation, monetary cost or cumulative baseline iterations. Accordingly the evidence supports the supplied-information package and its ablations, not an input-budget-neutral improvement or a source-compactness mechanism.

The latency study (§5.4, Figure7/Table8) sequences29 functions in the approximately400k-line Closure Compiler repository. It measures **prompt construction only**, excluding model inference, compilation/testing and human work. Retrieval/type extraction can overlap: cold-start component times38.8/4.62seconds yield38.8seconds total; subsequent means1.08/1.32seconds yield1.56seconds total. The approximately25-fold cold/warm ratio compares different tasks in one sequence, not repeated paired uncached/cached runs of each task or a whole-workflow speedup. Figure7's axis is broken. Warm caching is a useful reported result; end-to-end latency, edit-triggered cache invalidation, peak storage and comparative developer productivity remain unmeasured here.

## Artifact correspondence and limits

All twelve CodeLlama13B files contain the expected199 or90 task groups with exactlyten generated-code strings each and stored aggregate compilation/test metrics. Their72 metric entries correspond to the printed Table5/7 pattern. The common full Java compile@5 is stored as **88.3724%**: Table5 prints88.4 while Table7 prints88.3. Preserve that small printed inconsistency rather than inventing a second run. Result JSONs provide aggregate rates and code strings, not the underlying per-sample test verdicts needed to independently rebuild the rates without execution.

The public source makes the intended current-type information, retrieval, shared postprocessing and selected tests concrete. It does not fully recover how every stored context was prepared, all six-model/Rust/ablation results, the latency logs, training contamination or the final journal edition. Those are bounded correspondence gaps. They do not erase the published positive comparison, and they do not establish that the method fails.

## Consequence and next action

For B09/B12, this resolves a consequential alternative to diagnostic repair: **type information can guide generation before a diagnostic exists**. Source organization, tool-selected information, prompt size, postprocessing, compiler acceptance and tested behavior are separate parts of the causal account. Nu's domain conventions may affect any of them; this work measures none of Nu's future-case or temporal guarantees. Reuse the completed S230–S234 repair/translation methods rather than relabeling this as their same intervention.

The next primary lead is **DOI10.1145/3808138**, *One Size Does Not Fit All: Revisiting Code Context Engineering for Repository-Level Code Generation*, found during the exact-title metadata check. Its context-form comparison can change the unresolved information/budget explanation; only metadata is currently considered, so no positive or adverse result is imported. *In Line with Context* (DOI10.1145/3797094) is a conditional alternative. C05 multi-turn retention/API evolution and the independent managed-runtime/game-change frontiers remain open. No experiment or additional worker is authorized.

## Pinned companion identities

All following identities refer to the December2025 pin above. Source/schema files were read completely; result files and Arrow bodies have only the explicitly described inspection coverage. Raw bodies remain outside public Git.

| File | Bytes / lines | SHA-256 |
| --- | --- | --- |
| `README.md` | 2,334 / 32 | `118e4764401c8a77b81bb0b6c6d6da398f6bc35f0d403179520210532ebfaf6e` |
| `catcoder/java/evaluation.py` | 6,453 / 194 | `6a774da37b6cadadaad943c358a759adbf5cc938b84acac380d703f6ff88661c` |
| `catcoder/java/inference.py` | 4,965 / 135 | `b896aa8f8cad3e30b0c2a82e30b2eb5894fbc7153ec945fa4bbc440a6417c3e2` |
| `catcoder/java/retrieve_relevant_code.py` | 8,679 / 220 | `94a07556d6a6417ef2032c1c53ac35ebbf5d1393b02305413c4c5bd297dc750e` |
| `catcoder/java/extract_type_context.py` | 1,189 / 35 | `e17bb53b119c9aad4621d2a454ead2b7394e36f050e1838ca31d72ea363b1d15` |
| `catcoder/java/test_adapter.py` | 3,660 / 109 | `529f16a0396ca1091da641daad074ededd338323547d9f61618c7e795e706de2` |
| `catcoder/java/metrics.py` | 3,077 / 96 | `786276b2af1d5ab4943b34fd1200865b275982cb2ea8dcda726154a259e62c14` |
| `catcoder/java/util.py` | 3,001 / 91 | `43a98b139cc0f628bc5329893c4b2dfe62c84fbb19cec674babb83c0cb35ddff` |
| `catcoder/java/prompts/codegen` | 417 / 9 | `c0599392c9970018254aaf33dd508404445c47c61797af92753bfc3bc159653c` |
| `catcoder/java/dataset/javaeval/dataset_info.json` | 1,786 / 98 | `7e29456a6281a5ec8cf577ee5d36b638d280c41947ad20f369c9c9f197f53a93` |
| `catcoder/rust/evaluation.py` | 6,845 / 209 | `e812c4e3d0a80be02c9288d758ced42ee52add94aa43bf1d379bb98f4f0fbc47` |
| `catcoder/rust/inference.py` | 4,937 / 135 | `38425c13c405a62a0dc91f3e31a1818e149bff05816194b802e2285ae429612e` |
| `catcoder/rust/retrieve_relevant_code.py` | 7,169 / 178 | `91a4c3ca3eb2963df2bb7031ca8447180f3f38be6fb0d652cdfae2f7d82365ae` |
| `catcoder/rust/extract_type_context.py` | 379 / 14 | `cc55fb1dd212e540d4eee60bf2d532fd24601db5847557b74eb8d52068116bb7` |
| `catcoder/rust/test_adapter.py` | 3,121 / 86 | `781efc45bbd4f107ce81af2ab3067dc2de4ca741b1e038048d66ffd87f4d623a` |
| `catcoder/rust/metrics.py` | 3,155 / 97 | `633776108a89050f9a7afcb5a447be0c718bfa8ffdf3ad1b5675f24d5320e119` |
| `catcoder/rust/util.py` | 3,827 / 131 | `43f3df478aa4a83cbea62ded8be3b84a0c0dbcc4df7717f123914c2d41d704f2` |
| `catcoder/rust/prompts/codegen` | 416 / 9 | `2d56077a4d984e0e70342da0509bd26d8768d0a1d1fb0e2f34a2cefee97a0f76` |
| `catcoder/rust/dataset/rusteval/dataset_info.json` | 1,256 / 71 | `29f6fa7414233c4c63f44aeef53279d7ff99924a2be515c737560b4db4c558ea` |
| `catcoder/tools/java/java_analyzer/analyzer.py` | 2,026 / 50 | `8dfb2cb2ca247a1ea5021bf5f6018de53e60e90015f35a5cf489e5ac78abb361` |
| `catcoder/tools/java/java_analyzer/lsp_utils.py` | 4,383 / 94 | `79c59fa687c519895b4dc4c2f93f1d1faf652751f97057805cb3ad4bce540d2c` |
| `catcoder/tools/java/java_analyzer/string_utils.py` | 5,037 / 104 | `7920fde08db4b53e92caf91e93f202c779fb9d69019c2ca68380a7d5183d77b4` |
| `catcoder/tools/intellirust/intellirust/context.py` | 5,275 / 137 | `99e51711d36264ebc92cd24aa75c96431e889f5c561ba5c3596c47d09dd284e9` |
| `catcoder/tools/intellirust/src/visitor/fn_visitor.rs` | 4,502 / 149 | `2ac6ce276466035117be8196b432db2e4cb18b9d46d7632c1e5ab8598e146f58` |
| `catcoder/tools/intellirust/src/visitor/type_visitor.rs` | 3,592 / 120 | `fe0d85949eabd25c4dd102062a34d9ae503121d190c22806bc5fa0eb3a5d7af8` |
| `catcoder/tools/intellirust/src/analyzer/workspace.rs` | 7,792 / 237 | `1016dc103c592fee7d858cbf40bf9cc42197530514880941a2471eb5f1f4e819` |
| `catcoder/tools/intellirust/intellirust/file_structure.py` | 2,755 / 78 | `1b3f3ee55012481435253b2234177383bb186438b1701118ca8ab1cce69595c1` |
| `catcoder/java/dataset/javaeval/data-00000-of-00001.arrow` | 14,979,960 / structured | `5b8e19c09d9dffc2887c0f7b09d3cf22b1472e5572d2eb5c936e999a4e8a9956` |
| `catcoder/rust/dataset/rusteval/data-00000-of-00001.arrow` | 1,883,104 / structured | `6c169b66a4c2689199672755ca7166445ceb6222979e87978ce98dc9cf6c2c81` |
| `results/java/vanilla/codellama-13b_temp0.6_topp0.7_n10.json` | 922,042 / structured | `861fec84a0619a28bb7f2c4549d5b454751436bfad627c74647fe97c208c3aa0` |
| `results/java/infile/codellama-13b_temp0.6_topp0.7_n10.json` | 1,106,206 / structured | `ee5a96b6d599312bfc4713d0888c2f1166927f5d063e863372dcaa5ea7ed5a12` |
| `results/java/repocoder/codellama-13b_temp0.6_topp0.7_n10.json` | 1,130,871 / structured | `ab34121a55eeb808c3422e2b773e4d702c90ddd0de3c083a728a8b6f36cb46e1` |
| `results/java/catcoder/codellama-13b_temp0.6_topp0.7_n10.json` | 1,108,569 / structured | `ea15076e2f43d950be92cd302ed94983159423b3af0b220ab739e9cd1e0c47ad` |
| `results/java/-cr/codellama-13b_temp0.6_topp0.7_n10.json` | 941,021 / structured | `f8b5b4ce1ddf9248a3743402cb2ae8dc0dc72ef9ccc76bc24723e18304ce3854` |
| `results/java/-tc/codellama-13b_temp0.6_topp0.7_n10.json` | 1,065,489 / structured | `a7362b5d2972d3bc59874273a5822ad00058f7a4b5e72f41a884f37b27d7aa15` |
| `results/rust/vanilla/codellama-13b_temp0.6_topp0.7_n10.json` | 225,780 / structured | `eed3ace04345e420eb5789b5748e66307e8a01f48fc6e89da6243a505bf71fb7` |
| `results/rust/infile/codellama-13b_temp0.6_topp0.7_n10.json` | 258,297 / structured | `ca142705b76d66ce16c71006d913d5fff202efe7a1394f2490fee42056d277a2` |
| `results/rust/repocoder/codellama-13b_temp0.6_topp0.7_n10.json` | 274,728 / structured | `6155a65ea3e636e50d54d907887a1cca4ec74e41f131108649bd229c15c0e654` |
| `results/rust/catcoder/codellama-13b_temp0.6_topp0.7_n10.json` | 274,545 / structured | `5c5eee54716fe70a52729012ed324d7ffa83c9cb928ad317994c8347c54c323d` |
| `results/rust/-cr/codellama-13b_temp0.6_topp0.7_n10.json` | 278,229 / structured | `979f1f526e436cdd2cb05b247f7c4c482215113235d63887b826932456945fbd` |
| `results/rust/-tc/codellama-13b_temp0.6_topp0.7_n10.json` | 265,497 / structured | `386d88d8103aad1a543a48b94054d0a695d65a06588cac58258c1b266cf078d9` |
