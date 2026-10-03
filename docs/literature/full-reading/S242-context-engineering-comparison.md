# S242 — Context engineering: information, navigation and cost

Yichen Li, Qiye Lin, Yun Peng, Zhihan Jiang, Jinyang Liu, Chaozheng Wang, Yintong Huo and Cuiyun Gao, *One Size Does Not Fit All: Revisiting Code Context Engineering for Repository-Level Code Generation*, [DOI10.1145/3808138](https://doi.org/10.1145/3808138), PACMSE3(FSE), Article FSE131, July2026. Main-agent reading,2026-10-04.

The study reports useful gains from dependency context and model-dependent gains from repository navigation. It also measures substantially different information and inference costs across methods. These are comparisons of context-acquisition packages for missing functions/classes, not an equal-budget language or source-convention experiment. The published results do not establish D1's new-and-retained behavior or Nu's interactive-state benefits.

## Identity, acquisition and actual coverage

Read **all24 text and rendered pages**, seven main sections, **six figures, eight tables and67 references**, including acknowledgments and data availability; no appendix is present. The author-hosted ACM-formatted PDF names the correct DOI/authors and a CC BY4.0 license. Crossref instead formats the issue as pages2952–2975 with a30June2026 date. The paper records receipt12September2025 and acceptance24March2026. These metadata differences do not create separate works. The conference event abstract describes seven methods; the selected PDF describes ten and governs the reconstruction. Publisher landing/PDF access fails; byte identity with the publisher's delivery remains unverified.

Native collection `PKLXQNEE` was checked by DOI/title/edition before creating parent **`7L4XWB78`** and note **`MR8D3IEZ`**. They precede selected body reading. The [author PDF](https://www.zhihan-jiang.com/files/FSE26/CCE.pdf), attachment **`8STYJEUP`**, has **2,695,215bytes**, SHA-256 **`79e0af8cd291ad1d488612dd0497fd989178e71c08737c493fc6dad14b5459b7`**, MD5 **`85788716aa38f3cadfa33bf42ce0d072`**. The [slide deck](https://www.zhihan-jiang.com/files/FSE26/CCE-slides.pdf), attachment **`H8CUIET9`**, has **23pages /3,644,605bytes**, SHA-256 **`fa182b3a4dd21358d9b966e646a39546cba63242a1ffc28d773e60828580635a`**, MD5 **`ce7435e84657d670c6ef3ca0eafd09fb`**. All23 slides' extracted text and rendered slides10,11,14,15,18,19,20 are read. The latter reuse the result tables, dependency/composition plots and case illustration; other slides have no claimed visual coverage. The deck is a companion presentation, not independent evidence.

The linked [repository](https://github.com/YichenLi00/CCE/tree/1eaa7cdc4ad802f4a65e9a0c4017560b0757b7ba) is pinned to **`1eaa7cdc4ad802f4a65e9a0c4017560b0757b7ba`**,7July2026. Its complete untruncated tree contains **one file, `FSE26_CCE.pdf`**. The inspected branch list has only `main`, with no tags or releases. The repository PDF has the same size but SHA-256 **`da0da97d70371fbe20178e5f33f184195bb833b641d08ef73ef78356617eef28`**. Own passive comparison finds188 differing bytes, different creation/modification dates (7July versus23July), but **identical extracted text and identical rendered pixels at1× on every one of24 pages**. This supports display/body correspondence, not binary identity or publisher equivalence. The repository's advertised corrected dataset, ten implementations and framework are absent from this inspected public revision. No author code, model, test, compiler or experiment is run; hashing, PDF comparison and arithmetic are not reproduction.

## Task, methods and information contract

Sections2–3 use “repository-level” for code whose missing implementation depends on other files, rather than synthesizing an entire repository. A common base prompt contains the requirement, signature and available local file context. The study adds context using **ten methods** from three families:

| Family | Implemented information path |
| --- | --- |
| Similarity retrieval | BM25, UniXcoder and CoCoSoDa each retrieve top-five examples. An adapted RepoCoder first generates a draft, then retrieves with that draft before final generation. |
| Static dependency extraction | `SA_Method` resolves imports/symbols to dependent method bodies; `SA_File` includes whole dependent files. Adapted A3-CodGen also supplies third-party function signatures obtained through runtime introspection during preparation. |
| Navigation | `NavRaw` supplies five filesystem/search tools. `NavPlus` supplies ten tools, including definition/reference lookup, class structure, function/class reads and semantic search over prebuilt structural/semantic indexes. Adapted SWE-Agent retains windowed bash-style navigation but removes editing commands. |

The same backbone model collects context and generates the solution in navigation conditions; independent tool calls may be batched within one request. `NavPlus` deliberately combines static/semantic infrastructure with active navigation. These implementations therefore compare practical packages, not orthogonal presence/absence of three pure mechanisms. The paper does not specify a common total token/call allowance, task-level truncation/overflow rule, exact navigation stopping cap or length-matched context control. Equal task and generator do not make input information, reasoning calls and cost equal.

The authors report removing test-related directories and files containing tests before context acquisition (§3.1). Function/class bodies are missing under the infilling formulation; the class discussion explicitly describes removal of the class body. Without the preparation artifact, exact target removal, duplicate filtering, residual hints and separation of reference instrumentation from accessible context cannot be independently checked. Removal of test files alone would not prove absence of all solution hints or pretraining exposure.

## Samples, models and scoring

The **439 tasks** comprise230 CoderEval functions,115 DevEval functions sampled one per repository, and94 restored RepoClassBench Python classes under its detailed-description setting. Three of97 Python class environments were not restored. Table2 describes the full benchmark inventories, including CoderEval's460 Python/Java tasks; those inventories are not the evaluated439-task sample. The presented analysis is Python-focused, with Java discussed as a possible future transfer. The unavailable selection manifest prevents independently binding every CoderEval task and language split. RepoClassBench covers ten repositories; the study does not supply a selection-probability argument making these tasks representative of maintenance work.

The eight named backbones are Llama3.3-70B, Qwen3-235B-A22B, Qwen3-Coder480B-A35B, GPT-OSS120B, DeepSeekR1-671B-A37B, GPT-4o, Claude4Sonnet and Gemini2.5Pro. All are accessed through external APIs, with temperature0 and default thinking budgets. These labels, sometimes accompanied by references to older model generations, do not recover immutable service versions or inference configurations. Preserve the tested labels without extending results to current deployments or treating the paper's commercial/closed-source grouping as a verified licensing classification.

**Pass@1** is the proportion of first generated solutions that pass the supplied tests. The main evaluation uses one generation per task. A reported50-task, three-repeat stability check found identical code; the paper does not bind all configurations of that subset, and it cannot establish universal deterministic API behavior. No task-level confidence intervals, paired success tables or complete execution logs are supplied. The reported three class-environment exclusions are distinct from generated-program failures; other timeout/error/missingness handling remains unrecovered.

Only seven methods are evaluated for classes: RepoCoder, `SA_Method` and A3-CodGen are omitted. The authors explain that fine-grained static variants rely on sibling code lost when the whole class is removed and that their RepoCoder draft adaptation is function-specific. Comparing class and function outcomes therefore changes dataset, task granularity, available local structure and eligible methods together. It is not an isolated randomized task-size interaction.

## Positive and adverse outcomes

Table6's last column averages **relative improvement over the base** across models; it is not a percentage-point gain. Preserve the selected aggregate pattern:

| Method | DevEval relative gain | CoderEval relative gain | RepoClassBench relative gain |
| --- | --- | --- | --- |
| BM25 | 3.73% | 5.77% | 7.22% |
| RepoCoder adaptation | 4.87% | 7.85% | Not evaluated |
| `SA_Method` | 7.28% | 17.51% | Not evaluated |
| `SA_File` | 10.29% | 19.19% | 12.54% |
| A3-CodGen adaptation | 8.19% | 18.95% | Not evaluated |
| `NavRaw` | 6.98% | 14.47% | 14.72% |
| `NavPlus` | 9.77% | 17.17% | 26.16% |
| SWE-Agent adaptation | 7.82% | 15.61% | 17.17% |

Static dependency context improves the function results across the tested models. For example, Qwen3 DevEval improves **61.74→69.57%** with `SA_File`, a7.83-point /12.68%-relative increase. Navigation reaches some higher individual scores: `NavPlus` reaches73.91% on DevEval with Claude4Sonnet and Gemini2.5Pro, tied by SWE-Agent with Claude. On RepoClassBench, Claude improves **30.85→45.74%** with `NavPlus`, compared with37.23% using `SA_File`.

The contrary cases matter. Llama3.3 CoderEval falls **41.74→35.22%** under `NavRaw` and to38.26% under SWE-Agent, while `NavPlus` reaches47.39%. For Llama class tasks, **all three navigation variants are below the24.47% base**:19.15/21.28/20.21%; `SA_File` reaches26.60%. BM25 also lowers Llama CoderEval to40.43%. These observations support model/task/tool-dependent benefits; they do not show that all navigation is beneficial or that static analysis guarantees success. Attribution to reasoning strength, alignment or target-to-file ratio remains an explanatory interpretation rather than a separately manipulated mechanism.

## Cost, latency and denominator corrections

The timing setup is one Ubuntu20.04.4 workstation with32-core3GHz Xeon,64GB RAM and an80GB A100, while model inference is remote. Timing repeats12 times, discards the maximum/minimum and averages the remainingten. Table7 reports DevEval **preparation time, deliberately excluding model inference**:

| Method | Offline ms/repository | Online preparation ms/task | Mean model calls/task |
| --- | --- | --- | --- |
| BM25 | 133 | 11 | 1 |
| `SA_Method` | 3,011 | 383 | 1 |
| `SA_File` | 2,756 | 269 | 1 |
| RepoCoder | 487 | 127 | 2 |
| `NavRaw` | None | 1,426 | 9.85 |
| `NavPlus` | 9,380 | 2,075 | 4.62 |
| SWE-Agent | None | 1,386 | 11.47 |

These figures support lower preparation/call burdens for the selected passive methods. They are neither measured end-to-end response times nor tail latency. Figure3 shows size-associated indexing/retrieval trends; its trend plots do not establish a universal complexity bound or the claimed negligible cost of incremental maintenance. The prose calls7,811ms “multi-minute”; the table's explicit millisecond unit governs, approximately7.8seconds.

Table8 counts input **plus output over all invocations**, rather than just the final prompt. Its mean totals are4,977 base,8,195 `SA_Method`,9,695 A3-CodGen,28,412–29,790 for the three ICL variants,33,247 RepoCoder,43,497 `SA_File`,56,785 `NavPlus`,82,463 SWE-Agent and92,147 `NavRaw`. Thus `NavPlus`/`NavRaw` are about **11.41×/18.51× base**, but only **1.31×/2.12× `SA_File`**. The displayed token means span18.51×, not more than two orders of magnitude. The headline10–20× cannot be applied to every passive comparator.

The study's estimated historical API costs also depend on model-specific pricing/tokenizers and input/output mix. For Claude4Sonnet the table gives$0.0395 base,$0.2506 `SA_File`,$0.5295 `NavPlus` and$0.7136 `NavRaw` per function task: navigation is about2.11×/2.85× the full-file comparator. These are the paper's estimates, not current price quotes or invoices. The class narrative reports navigation cost up to$1.47/task without a corresponding full class-cost table or raw packet. Cumulative tokens across calls are distinct from maximum resident context; summing them does not by itself demonstrate context-window overflow. The positive effectiveness results remain, but they do not establish equal-budget cost-effectiveness or human productivity.

## What dependency coverage establishes

Sections3.4/4.3 define ground-truth dependencies as cross-file functions invoked while running the reference solution's tests. **DCR** is the fraction whose definitions are collected. It is coverage of that observed dependency set, not all feasible dependencies, semantic obligations or future behavior. Class-level DCR is explicitly left for future work. Exact function identity matching, treatment of partial definitions, zero-dependency tasks and aggregation require the absent metric implementation.

The paper reports DCR33.9–38.6% for similarity retrieval,76.2% for `SA_Method`,80.9% for `SA_File`,33.5–73.2% for `NavRaw` across models and42.0–76.8% for `NavPlus`. Reported Spearman correlation with Pass@1 across method/model configurations is0.78, p<0.001. This is useful association evidence, not proof that supplying a definition causes a fixed increment in success or that DCR independently validates the oracle.

The composition analysis classifies a code fragment as definition if it contains at least one observed dependency definition, otherwise reference if it contains a call site, otherwise other. Definition takes precedence when both occur. `SA_Method` has88% definition /5% reference fragments; `NavPlus`55% /28%; `NavRaw`35% /7%, with58% other; BM2522% definition /68% other. The units are classified fragments, not necessarily fractions of prompt tokens or separately verified semantic evidence. The simplified `format_error` case illustrates how reference lookup can expose formatting conventions missed by import-following.

This supports tracking definitions and usage examples separately. It does **not isolate `find_references`**: the richer toolkit also changes semantic search, structural queries, read granularity and the resulting trajectory. Nor does the case prove that every passive strategy is inherently unable to retrieve call sites. The study's successful package and mixed outcomes should be retained while its stronger universal/causal wording is narrowed. The slide deck's “same task, different context” explanation does not add an equal-budget or tool-component control.

## Consequence and next action

For B09/B12, S241 and S242 jointly support a bounded account: current program structure and examples can help generation; navigation changes which information arrives and how much work is spent obtaining it; tested success, dependency coverage, calls, cumulative traffic and resident context are different endpoints. Larger or more structured input is not evidence that Nu's authored source is compact, that F# itself helps a fixed agent, or that explicit enumeration satisfies future semantic/temporal obligations. Preserve the existing E/H compactness counterevidence and all experiment holds.

The selected paper's primary method is now reconstructed. The advertised implementation/data remain an **artifact-access gap**, not an unread paper or proof that the reported effects are false. Recheck the pinned repository's successor or an author-linked release if those implementation details become decisive; no purchase, author contact or worker is authorized by this reading. The next strongest accessible frontier is **C05:8, CodeChat-Eval**, for instruction selection, refinement trajectories and retention of earlier correctness. Resolve its primary edition and native record before body reading. Other multi-turn/API-evolution leads, context inlining, modern .NET retained-history/tails and game-change evidence remain conditional independent routes.
