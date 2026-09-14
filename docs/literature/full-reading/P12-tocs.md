# P12 - Theory of Code Space

## Identity and coverage

Grigory Sapunov, *Theory of Code Space: Do Code Agents Understand Software Architecture?*, DOI `10.48550/arXiv.2603.00601`, v4, March 18, 2026. Main Codex AI reader consumed all 14 PDF pages, references and appendices A-D. Rendered pp. 5-11 and 14 include both figures, tables 1-8, formulas and the codebase layout. Zotero `RXVC7BGE`; bytes in [assets](assets.json). The title page explicitly labels results preliminary and the paper work in progress/under review.

## What is actually evaluated

TOCS evaluates **Construct**, the production of architectural maps during read-only exploration. Revise and Exploit are future evaluation, despite framework support and counterfactual-probe facilities. It does not report a downstream maintenance experiment or validate that graph F1 predicts successful changes.

The generator produces one Python pipeline pattern across three seeds (42, 123, 999), 27/30/27 modules and 70/84/70 typed edges, with 15/16/15 planted constraints. Neutral filenames, registry wiring, adapters, middleware and legacy distractors make traversal less trivial; the domains are ETL/log/text processing. The architecture is authored, not sampled from real projects, and no architecture alternatives are randomized. Edge totals are 150 IMPORTS, 39 CALLS_API, 16 DATA_FLOWS_TO and 19 REGISTRY_WIRES (224 total). Purpose and naming constraints are authored specifications, not necessarily empirically established maintenance principles.

The agent has twenty actions, with LIST, full-file OPEN, location-only SEARCH, signature/docstring INSPECT and DONE. SEARCH provides no snippets. Every three actions it is asked for JSON components, edges, exports, confidence, invariants and unexplored areas. Probe calls do not consume the action budget, but consume inference and can change subsequent exploration. No successor tasks or code edits occur. Main evaluation uses four rule baselines and six model aliases, once per model/codebase, temperature zero except GPT-5.3-Codex at one; no repeated-seed or prompt-population uncertainty. The reported ± values are half-ranges across three generated cases, not confidence intervals. Complete auxiliary-token/time/retry accounting is not reported.

Active chooses observations. Passive-full receives all files once; passive-oracle receives twenty files ranked by ground-truth connectivity; passive-replay receives a prior observation log. These conditions change information quantity, order, prompts and number of calls. The paper's Gemini replay uses **GPT's trace** (§6.4), so its active/replay comparison also changes file selection. It cannot isolate decision overhead from selection. The stated decomposition is a set of different contrasts, not an additive partition of a single causal total.

## Scoring and findings

Dependency F1 uses exact `(source file, target file, edge type)` sets. Directory/symbol-qualified alternatives receive no credit. Invariant scoring uses authored structured forms; main tables use relaxed rather than near-zero strict matching. Externalized maps are a proxy: failure to serialize is not proof of missing latent knowledge, and an accepted map is not proof of executable behavior. Confidence ECE and action/OPEN AUC are additional diagnostics.

Table 2: GPT dependency F1 .676 and Claude .664 exceed Config-Aware .577; Claude's AUC .350 exceeds GPT .306. The other four LLMs have lower dependency F1 than Config-Aware. LLMs **collectively**, not each model, discover all four edge types; Claude data-flow recall is zero. Model/graph rankings are preliminary, not architecture or language effects. Config-Aware's advantage over Random is 3.125x at B=10, but Random slightly exceeds it at B=25 (.632/.626); an action threshold changes the comparison.

Table 4: GPT passive-full minus active is -.219; Gemini about +.227 from rounded cells (reported +.226). Oracle minus active is +.061/+ .172 (reported +.060/+ .172). Decision contrast is labeled **active minus replay** in table 4 (+.011/-.092), reversing §3's passive-minus-active definition. GPT invariant F1 is highest for full (.757), followed closely by replay (.752); these are not evidence that larger visible context always hurts.

Table 5: retained maps versus no intermediate probes change GPT dependency F1 by +.138 and invariant F1 +.169. Gemini dependency F1 changes -.011, invariant F1 +.243. Probe-only (generate then remove JSON) scores lower than no-probe for dependency F1 in both models (-.074/-.079). Thus a supposedly free measurement is an intervention, consistent with the paper's later qualification. Small single-run cases cannot establish universal harm/benefit or a latent-memory mechanism.

Reported instability includes loss of correct edges between maps; it concerns observable serialization. Prompt revisions turn invariant scores from zero into substantial relaxed scores. Table 8's Claude change is .664-.639=.025, conflicting with §7.3's .012; GPT .676-.564=.112 from rounded cells versus reported .113. Figure 1b's heatmap labels include denominators such as 46 imports/6 registry edges and a cell 18/6, unlike table 3's three-case totals; do not reuse it as a consistent aggregate count table. There is no basis here to claim intrinsic model-scale effects, architecture mediation or benchmark novelty beyond the bounded retrieval record.

## Read-only artifact reconstruction

[che-shr-cat/tocs](https://github.com/che-shr-cat/tocs/tree/e617928f612c839c4b40debb875249472ab4d765) was pinned to `e617928f612c839c4b40debb875249472ab4d765`. Read README (MIT), full system/probe prompts, full `metrics/map_accuracy.py` and `gap_analysis.py`, passive-condition functions in `evaluation/run_eval.py` (387-605), and portions of constraint-discovery code. No author code or model invocation ran. Exact result-generation provenance, active-adapter retry/token defaults, generator validation and all raw runs remain unverified.

The current relaxed invariant scorer discards `pattern` and generally `via`, matching `(type, normalized src, normalized dst)` with empty gold endpoints as wildcards. INTERFACE_ONLY may promote `via` to dst. Sets collapse different constraints sharing this reduced representation; greedy matching over sets can depend on iteration order when wildcard matches compete. This is weaker than the paper's four-field description and can accept a type without demonstrating its actual rule. The strict scorer includes **five** fields, including pattern. Neither should be treated as a semantic oracle without explicit examples of acceptable/incorrect alternatives.

The code's APG decision sign is replay-minus-active, confirming disagreement with table 4. Its generic gap analysis uses the strict invariant field, while the paper reports relaxed scores; reproduction must identify the publication aggregation path. ECE defaults to ten bins versus five in the paper. Action AUC integrates coordinates from zero to `(n-1)/n`, not a complete normalized unit interval; budget comparisons need that convention fixed. These are static specification differences, not demonstrated changes to published numerical results.

Passive-oracle ranks files by edge participation, not a proven maximum-information subset. Nonprobe observations still trigger model responses, so equal file counts do not imply equal inference. Passive-full is one call; replay preserves every logged observation and generates fresh responses. Probe-only removes JSON exchanges and substitutes acknowledgments. These details make the control implementable in principle but do not remove its bundled differences.

## ALF implication

Architectural map evaluation and persistent maps already have direct prior art. Use a source-grounded architecture description and observable change obligations; do not equate the ability to print a graph with maintainability. Keep research probes outside candidate context by default. Any later probe/scaffold intervention needs a separate adopted treatment, matched observation provenance, a no-probe control, robust semantic acceptance rules and full auxiliary accounting. This pilot does not validate Nu's form factors or the existing F#/C# pair.
