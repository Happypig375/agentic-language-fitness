# S230 — ArkTS generation: compiler feedback, behavioral scoring and reporting limits

## Identity and coverage

Ekin Can Erkuş, Cansen Çağlayan Yılmaz and Mustafa Umut Demirezen, *ArkTS code generation: A comprehensive evaluation with large language models*, **Empirical Software Engineering31(4), article109**, online2 April2026; DOI [10.1007/s10664-026-10844-0](https://doi.org/10.1007/s10664-026-10844-0). Native parent/note/PDF `APFWN9Q4`/`DDHVTB3H`/`LQERL9DU`, collection `PKLXQNEE`. The record precedes intentional complete reading; an earlier exact-title search automatically exposed bounded methods passages.

The34-page publisher PDF is2,029,101 bytes, SHA-256 **`d2538ffa763715865fa5c00185bd6fa19403597a4db8b4e360b8a72ad7af5577`**, verified byte-for-byte through the native Zotero attachment route. All34 pages of text, five main sections, AppendixA.1–A.3,15 tables, five figures, three numbered listings, diagnostic patterns, three equations and42 bibliography entries are read. Rendered pages **1,6,9,14,15,17–24,30–32** are visually inspected (16 pages); page21's landscape table is rotated for legibility. Remaining text/tables are read through extraction. No separate supplementary file is linked on the inspected publisher page. No model, compiler, candidate or author code was run; checks below are our elementary arithmetic on published values.

**Distinct work/edition:** Research Square DOI `10.21203/rs.3.rs-7362986/v1` is **not** an earlier edition of this paper. Crossref explicitly links it to `10.1007/s10515-026-00599-9`, with different first two authors and a different benchmark; it is retained as S231. One shared coauthor and ArkTS subject matter do not establish shared data or independent replication.

## Method and intended evidence

EMH contains300 tasks,100 per difficulty. Table4 gives14 algorithms,32 data structures,29 API tasks and225 UI patterns; it is intentionally dominated by UI tasks, not balanced across categories. Easy/medium/hard algorithm counts are3/1/10, while UI counts are69/80/76. Difficulty reflects reference control flow, state and abstraction rather than an independently calibrated maintenance workload.

Sections2.2–2.4 describe sampling HumanEvalX/APPS/MBPP and ArkTS repositories, rewriting instructions, LLM reference/test drafts, expert refinement, deduplication, compilation/tests and frozen metadata. Candidates needing substantial correction or showing unstable/ambiguous behavior are removed or repaired. References must pass. Exact source proportions, the drafting model, annotator counts, deduplication threshold, seeds, toolchain version/container digest and complete test contracts are not supplied in the paper. Some passages describe repository-native UI/lifecycle items as already included; others reserve them for a second wave (pp.8–11,15,25–29). Their actual contribution to the300 tasks needs the item-level lineage.

The21-model pipeline sends all300 prompts, removes simple noncode wrappers, rejects missing code blocks, compiles in a restricted container, then tests successful builds. Generation latency excludes compilation and testing. The defined denominator, **TotalGenerated**, contains only returned responses without transport failure within the timeout; missing responses are not imputed. This is an explicit conditional estimand, not equal coverage of a common task set. Model selection uses earlier performance/preliminary ArkTS results; generation settings are said to be fixed but exact values and API snapshots are not enumerated.

The useful method distinction is **Tier1** parse/type/link success versus **Tier2** behavior after compilation. Table3 explicitly includes wrong outputs, contract mismatch, runtime exceptions, state/lifecycle faults and timeouts. AppendixA.2 gives ordered first-match diagnostic regexes, a fallback category and5% manual failure checks. The pilot uses only the first compiler diagnostic for a minimal repair. This makes compiler feedback an observed intermediate signal, not a specification of intended state or temporal behavior. Negative paths and timing tests are partly future work (p.29).

## Reported outcomes, including favorable pilot evidence

Table8 has **3,270 returned responses from6,300 requested model–prompt pairs**, with107 reported solved instances; these are model/task occurrences, not independent projects. DeepSeek-R1 solves10/44 returned responses(22.7%), Claude3.7Sonnet41/300(13.7%), GeminiPro6/48(12.5%) and GeminiFlash23/300(7.7%). Thirteen models have zero observed solves. Lower observed success with difficulty is reported for the eight nonzero models. Wilson intervals in Table9 express binomial uncertainty conditional on returned responses; they do not correct model-dependent missingness or establish a controlled language effect.

For perspective, our calculation of **confirmed solves per300 requested prompts** is3.33% for R1 and13.67% for Sonnet. This does not impute unseen correctness or replace the paper's estimand; it shows why its conditional ranking and the absolute delivered-success comparison differ. Time spent on missing requests is also needed for deployment throughput. Equation1 combines returned-response Pass@1 with model-call latency; it excludes compile/test work, and Table8 suppresses latency for zero-solve models.

The separate30-task pilot(10 per difficulty, outside EMH) reports:

| R1 setting | Solved /30 | Compiled /30 | Reported mean model-generation ms |
| --- | --- | --- | --- |
| Baseline, no exemplar/repair | 7 | 15 | 470 |
| One compact exemplar | 8 | 18 | 560 |
| Two exemplars | 9 | 19 | 615 |
| Two exemplars plus one compiler-guided repair | 11 | 23 | 680 |

These are favorable reported results: four additional solves and eight additional compiling outputs versus baseline; the incremental repair contrast after two examples is two solves/four compiling outputs. Preserve that direction. The final setting changes both context and number of model calls; it is not an isolated type-system or repair-mechanism effect. The abstract/conclusion say one example plus repair, whereas Section3.5/Table14 specify two. The model is selected for its highest main-study conditional Pass@1. Item-level transitions, repeated draws, paired uncertainty, compiler/test costs and whether680ms sums both calls remain unavailable. The described repair sees a compiler diagnostic; no final-test-driven stopping is described. That does not independently certify the released information boundary.

## Judge and numerical correspondence

Section2.5.3 initially describes an independent LLM judge with three ratings, a human agreement check and a one-week stability sample. It then states that the uploaded file contains **9 for every judge score**, and replaces those values using code-structure tokens, prompt/code alignment, imports, bracket balance, explanation cues and difficulty. A continuous index is mapped through skewed percentile bins to spread scores and fit the low functional-success pattern (pp.13–14). Figure2 visibly labels its values **estimated**; Table7 summarizes300 scores(mean5.21).

Therefore this distribution is a reconstructed structural proxy, not observed independent judge agreement with execution. Its intentional scaling cannot independently corroborate the low Pass@1. The judge model, original300-item mapping to the21-model outputs, exact scoring weights/bin boundaries and promised numerical human/stability agreement are not reported. Listing3's prompt names prompt/code/difficulty as inputs and asks about compilation/tests, but supplies no actual test outcomes. Do not silently combine this protocol with the feature-based replacement.

Other material correspondences remain unresolved after visual checking:

- **Category denominators change.** Table12's rates use Table4's fixed category sizes, including one medium algorithm and one hard API item. For R1, weighting the easy rates by3/8/20/69 gives approximately4.97% after rounding, consistent with five solves per100 requested easy tasks; Table11 instead gives31.3%=5/16 returned tasks. Category-specific returned counts are absent. The category table cannot be read as the same conditional success measure without qualification.
- **Compilation and timing figures disagree with tables.** Table10 includes compilation success53.67%,58.45%,87.05% and78.84%; Figure4's visible vertical range ends at50%, with no model labels despite the prose promising labels. Its axes say execution time, while the method/caption refer to generation time. It cannot support the stated model-specific timing explanation as printed.
- **Some rates need a different aggregation or correction.** For example, Table13's GeminiFlash compilation-failure41.55% over the stated300 returned outputs implies124.65 failures, impossible for a single binary count rounded to two decimals. This is a reporting/denominator discrepancy, not a reproduced runtime failure or evidence of misconduct.
- **Error interpretation exceeds reported detail.** Table13 reports only total compilation failure and syntax percentages. Per-model undefined-reference/type-error shares and the asserted near-flat or rising subtype trends are not tabulated. Figure5 contains nonmonotone individual series; no underlying values are supplied for reconstructing the broader trend claim.

The appendix's code sample is not an executable validation packet: Listing1(p.30) is a plain class that fetches data and returns an HTML table string, with no shown ArkUI decorators or component lifecycle; it is labeled a successful hard task. There are no accompanying assertions, runtime context, asynchronous scheduling rules or network stubs. This does not prove the sample fails; it limits what it demonstrates about reactive UI correctness under the described no-network harness.

## Artifact/access scope and survey consequence

The inspected publisher HTML is409,591 bytes, SHA-256 `59b0358d11db93ab978a450ca791c4b1d41162396d7d11e190c8d85f5ad3483a`; its relevant links lead to the15 tables/five figures, not a dataset/code archive. **Data Availability(p.32) says data, prompts and scripts are available from the corresponding author on reasonable request.** The paper's repeated release/pinning language does not provide a public runnable packet or exact environment here. Two focused searches returned16 locators, including S231's different public implementation and other ArkTS studies; none is substituted for EMH. No author contact is authorized or performed.

S230 establishes a concrete reported typed-UI benchmark design and a small favorable examples/repair comparison, with severe limits on reconstructing its actual behavioral oracle, quantitative ranking and independent judge evidence. Preserve both. It supports the separation of compilation, behavior, missingness and latency; it does not establish a benefit from stronger typing, reactive architecture, Nu, live evolution or D1 enumeration. Claims that low-resource training exposure explains the results and that gains transfer to Compose/SwiftUI/Flutter remain hypotheses rather than controlled comparisons.

Next read **S231's distinct compiler-feedback method and bounded public implementation** to compare native UI representation, feedback/stopping and compilation versus behavioral scoring. C05's typed retrieval/modular translation and multi-turn evolution routes remain conditional next methods. S229's professional benefit claims remain a primary-access gap; finishing EMH does not resolve them or complete the survey. All holds persist.


**Follow-up, 2026-10-03:** [S231’s selected preprint and bounded public release are now reconstructed](S231-harmonyos-compiler-feedback.md). Its positive compilation and conditional manual behavior outcomes are a different benchmark, with an unresolved final-edition body and public three-attempt/ten-attempt experiment correspondence. The next method is C05’s modular type-compatible Go-to-Rust translation, not another reading of S230’s unchanged tables.
