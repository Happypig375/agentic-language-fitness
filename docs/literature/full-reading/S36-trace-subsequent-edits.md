# S36 — TRACE: subsequent edits and tool-assisted propagation

**Full read, 2026-09-16:** Chenyan Liu, Yun Lin, Yuhuan Huang, Jiaxin Chang, Binhang Qi, Bo Jiang, Zhiyong Huang and Jin Song Dong, *Learning Project-wise Subsequent Code Edits via Interleaving Neural-based Induction and Tool-based Deduction*. ASE 2025, pp. 1377–1389, DOI [10.1109/ASE63991.2025.00117](https://doi.org/10.1109/ASE63991.2025.00117). Read [arXiv 2604.12220v1](https://arxiv.org/abs/2604.12220v1), posted 14 April 2026; do not confuse posting and conference dates or assume publisher-file identity.

Zotero `PKLXQNEE`: parent `XZTV9KAM`, PDF `LLQU9UBJ`; 13 pages, 1,054,830 bytes, SHA-256 `6644e9e4d710cb7d42a38c4fcb113fa98359511fa556140468556ba54665aa2e`. All pages and references read, six figures, twelve tables and Algorithm 1 visually checked on PDF pp. 3–10. Main-paper reading complete; bounded supplement/source inspection below, no experimental reproduction.

## Purpose and mechanism

TRACE recommends the next edit from a repository, prior edits and an optional description. It combines a learned tool invoker, locator and generator. LSP rename, definition/use, clone and diagnostic facilities provide locations or edits; neural models handle remaining ambiguity. Six token/line edit labels distinguish changes that ordinary replace/insert/keep labels merge. The locator and generator use CodeT5; the supplement specifies **CodeBERT-base for the invoker**, not three CodeT5 models.

The motivating parameter-change example explicitly distinguishes finding dependent sites from choosing correct parameter values and updating behavior. Incorrect rename invocation can damage unrelated uses. Thus useful static propagation and incomplete semantic coverage are already recognized; neither idea is a new ALF contribution.

## Evaluation and strongest limits

The filtered corpus contains 38,647 commits from a stated 678 repositories in Python, Go, Java, JavaScript and TypeScript. Llama 3 filters vague/multiple-intent commit messages and rewrites retained descriptions. Static localization/generation use other hunks from the same commit as context; their targets are edit labels, exact patch match and BLEU, not independently executed feature correctness. Exact matching also penalizes valid alternative implementations.

The 500-commit simulation, 3,211 hunks, starts from the first reference edit. At each step it selects a predicted matching location or a remaining reference location, evaluates generated alternatives, then **applies the reference edit** (p. 9). It never measures an autonomous trajectory accumulating its own incorrect edits. Table XI's 25.71% TRACE versus 24.22% Cursor acceptance at location rank one is a descriptive edit metric, not a percentage of completed projects. The released acceptance script combines a location match with **best generation BLEU at ten**, which must accompany any reuse of the rank label.

The separate user study has 24 students, three groups of eight, three selected Python tasks, a first-edit hint, executable tests and a 30-minute task budget. TRACE is faster in the first two tasks; Cursor is faster in the third (Tables XII and pp. 10–11). This is important contrary evidence against uniform superiority. The paper reports signed-rank tests between stratified groups without documenting a defensible participant pairing; the retrieved supplement prose does not resolve that requirement. Task-one TRACE/CoEdPilot p = 0.0781 is not significant at the stated 0.05 threshold. Do not import these p-values, effect sizes or durations as ALF power inputs. The over-trust account is authors' qualitative interpretation of selected and sampled recordings, not a causal estimate of a warning policy.

## Supplement and artifact checks

The [author site](https://sites.google.com/view/code-trace/homepage) was accessible through direct HTTP after a web-tool access failure. Fully read its homepage and seven pages' prose: benchmark, hyperparameters, demographics, editing tasks, overall performance, user-behavior analysis and observations. Embedded tables/images and participant videos were not fully audited; the observations page says complete unredacted recordings would be released after acceptance. No claim of full multimedia-supplement coverage or independent behavior coding.

The benchmark page clarifies that train/validation and validation/test may share projects, while train/test do not. Thus Table V's 390 + 92 + 207 project memberships exceeding 678 is not by itself a counting error. This still leaves validation-dependent model selection and the exact split membership to reconstruct before reproduction. Hyperparameters specify model identities, lengths, losses and training settings; no training was run.

[TRACE source](https://github.com/code-philia/TRACE/tree/5f2dde43dbc22b5ac38a6b4e658ab0d3377c5a31) is pinned at `5f2dde43dbc22b5ac38a6b4e658ab0d3377c5a31`, untruncated tree inspected. Fully read root and RQ1/RQ2/RQ4/RQ5 READMEs and `count_acceptance.py`; read `simulation.py` lines 1–192 and located matching/scoring branches. The simulation registers predictions against `simulating_edit["after"]`, then retains the reference edit. Its ordering branches are not uniformly random, despite the paper's random-fallback wording. No results rerun, weights downloaded, extension installed or author code executed. Remaining source and raw participant/test oracles are not reconstructed.

## Consequence

D1 must study the **total behavioral effect of an assigned source convention under actual autonomous maintenance**, with unchanged source/tool access across arms, useful ordinary compiler feedback, and independent obligations. Do not claim first tool-assisted propagation or use reference patch insertion to rescue candidates. D3's generic retrieval mechanism already overlaps S35/TRACE. D5 must retain null/adverse tasks: a locally coordinated edit can favor a simpler interaction. TRACE's participant productivity is not Codex performance evidence.
