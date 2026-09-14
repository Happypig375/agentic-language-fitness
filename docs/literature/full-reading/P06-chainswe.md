# P06 - ChainSWE: Benchmarking Coding Agents on Multi-Bug Software Maintenance

## Identity, editions and coverage

Qirui Jin and colleagues, DOI `10.48550/arXiv.2607.02606`. Main Codex AI reader consumed **v2 (September 1, 2026), all 19 PDF pages**, references and appendices A-D. Zotero `FMTJ9SHC`, exact hash in [assets](assets.json). Rendered pp. 2, 4-5, 7-9 and 12-19 inspected: all figures/tables, code-patch examples and prompts. V1 (July 1, 18 pages, `8F2EA7B6`) was compared through a whole-text difference inventory plus direct reading of pp. 4-9 and visual inspection of pp. 7-9. V1 is retained as a historical edition, not claimed as a separate continuous full read.

[arXiv history](https://arxiv.org/abs/2607.02606) verifies both dates. V2 changes author/affiliation information, adds contamination subgroup analyses and revises consequential captions. The cited [C-lister/ChainSWE repository](https://github.com/C-lister/ChainSWE) returned HTTP 404 through both the GitHub API and web reader on 2026-09-15. Exact runtime, source/test exposure, worker-model identity and scoring code consequently remain unavailable. Full v2 reading is complete; method reconstruction is limited, not experimentally reproduced.

## Construction and selected population

The authors mine chronological overlapping issues from six Python SWE datasets, joining adjacent base commits or later patches that apply cleanly to earlier resolved states (pp. 3-5). AST-derived overlap of modified files/functions/classes filters candidate windows. Sequential application of gold test/fix patches must make F2P tests pass without P2P regressions. Length-2 chains are dropped. A Qwen3.7-Max/BASELINE ORACLE pre-run then retains only chains with more than half of their bugs solved. This conditions the benchmark on model-assisted tractability; it is not a random maintenance population or a model-free construction procedure.

Final data are 100 chains, 304 bug positions and 54 listed repositories: 97 length-3, two length-4, one length-5 (pp. 5, 8, 12-13). Six source families are considered, but SWE-bench Pro contributes zero surviving chains; 52% are SWE-rebench-v2. Repositories can contribute multiple overlapping chains, and a chain can induce subchains. The number of statistically independent unique bug histories is not established by 304 positions. Gold replay validates specified tests, not every possible obligation or arbitrary future change.

## Reconstructing the actual controls

| Mode | Predecessor and process | Retained information | Interpretation |
| --- | --- | --- | --- |
| ORACLE | Reset container to chain base, apply all earlier gold fixes and test patches before the current task | Correct reference source/test state; current task prompt | Reference-state baseline, not the agent's own prior solution |
| SEQ | Same container, commit each agent patch and continue; fresh agent conversation per bug | Agent-modified repository and persistent environment | Inherited-state policy outcome |
| SEQ+MEM | Same repository continuation, conversation also retained | Earlier observations, edits and dead ends | Total persistent-history policy effect, including any changes in earlier patches |

Sections 4.3-4.4 state continuation after failed bugs, 100 turns and 30 minutes per instance. A fresh conversation does not imply a fresh environment. ORACLE changes reference/test state and container reset jointly; equal prior-test availability across modes is not fully specified without code. Section 5.1 also describes exposure to earlier issues/gold patches more broadly than the current-issue prompt. Therefore the modes are useful templates, not a fully controlled direct causal decomposition of memory and source structure.

Three SWE-EDIT configurations cross seven models with API defaults/medium reasoning (pp. 5-7). BASELINE retains full history and edits via exact replacement. SUMMARIZE triggers above 50k input tokens, summarizes the prefix and keeps 50 recent messages. SUB-AGENT delegates file selection and editing: a viewer chooses line ranges and an editor receives code plus an instruction and can rewrite a whole file (appendix D). This changes information selection and execution authority, not only context length. The text's claim of the same tools/prompts/model across configurations is too broad; auxiliary model identities, budgets, costs and effective prompts require unavailable configuration evidence.

## Outcomes, estimates and limits

Per-bug success means all target tests pass; full-chain success means every bug passes. Table 2 cost is average USD **per chain**, despite the general metrics discussion also mentioning per-task cost. Published table-2 cell means recompute to 58.94% ORACLE, 36.52% SEQ and 36.92% SEQ+MEM: about a 22.4-point/38% relative ORACLE-to-SEQ loss. All 21 cells lose per-bug accuracy under SEQ, but some full-chain cells improve (GPT-5.5/Gemini under summarization). There is no reported repeated-run interval or equivalence test establishing a zero memory effect.

GPT-5.5 benefits from memory under summarization (+7.3 points) and subagents (+8.2), but loses 1.6 points under baseline (p. 7). Configuration-average gains are not universal. At position 3, reported reductions approach 70% relative, not 70 percentage points; position analyses omit the three longer chains (p. 8). Chronology, selection, repository state and stochastic solver behavior remain alternatives to intrinsic depth alone.

The chain-error definition is ORACLE success paired with SEQ failure: 318/663 downstream BASELINE failures, or 47.96% (p. 9). A single contrasting stochastic run does not prove every discordance was caused by earlier code, although the detailed patch/test witnesses in appendix C strengthen particular examples. Under-/over-edits are defined relative to gold edits; a different correct implementation is not automatically wrong. Reported fingerprints are 40% regression, 25% unfixed target and 34% unusable patch/uncollectable suite (rounding leaves 1%). Test underspecification can make hidden future obligations impossible to infer, as the authors acknowledge (pp. 9-10).

Appendix A4 reports **average maximum** input context per chain, e.g. baseline 48.1k SEQ versus 63.6k SEQ+MEM. This is different from cumulative input and does not show that any declared provider limit was reached. Summarization reduces the average maximum to 48.4k under SEQ+MEM, without establishing why individual outcomes changed.

## Edition and arithmetic corrections that must survive handoff

V1 table 2 (p. 7) says scoring stops at the first unresolved bug and later bugs count unresolved, contradicting v1's continuation description. V2 deletes that scoring clause while retaining the numeric table. V1 table 3 labels Claude-Opus rows estimated; v2 removes that qualification without changing displayed values. V1 figure 4(b) gives 174 attempted chain errors; v2 changes it to 318. Use v2's wording, retain the differences, and do not certify raw evaluation provenance from editorial changes alone.

Some table-2 cells cannot be one-decimal rounded integer successes out of the stated 304, e.g. 64.0% (194/304=63.8%, 195/304=64.1%). Eight displayed cells fail that simple denominator compatibility check. Averaging or additional denominators could explain them, but are not specified. V2's source/date subgroup losses (tables 10-11) are much smaller than the overall 22.4-point gap; common matched weighting would not reconcile them, so underlying membership/weighting remains needed. These are reporting limits, not fabricated alternative results.

## Consequences for ALF

Reuse and credit reference-predecessor, inherited-fresh and inherited-persistent controls. For any future ALF protocol, explicitly define repository, installed state, transcript and prior-test exposure separately; continue/stop rules and treatment of unscored successors must be frozen in advance. A cloned identical predecessor/transcript intervention would answer a different direct memory question from evolving each policy independently.

Do not infer that history is universally harmful, that subagent repair merely insulates a planner, or that all ORACLE/SEQ discordance identifies latent maintainability. ALF's proposed contribution must exceed these existing controls through prospective architecture-specific predictions, correct predecessors and valid public obligations, with source size/task difficulty as rivals. No ChainSWE model-filtering pass, worker deployment or experiment is authorized by this reading.
