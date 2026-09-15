# S07 — ML recommendation in product development

**Full PDF read and bounded artifact reconstruction, 2026-09-16 HKT.** Reader: main Codex AI session. [Living queue](../selection-priority-reading-2026-09-15.md); [PLAN](../../../PLAN.md). No model calls, human adjudication or experimental reproduction.

## Identity and coverage

Sonntag, Luttmer and Nagarajah, **Can large language models support machine learning implementation in product development? A comparative analysis and perspectives**, Proceedings of the Design Society 5 (2025), pp. 861–870, DOI [10.1017/pds.2025.10100](https://doi.org/10.1017/pds.2025.10100).

| Asset | Verified identity |
| --- | --- |
| Zotero collection / parent / attachment | `PKLXQNEE` / `3B7596AC` / `J52964I6` |
| Publisher PDF | 347,543 bytes; 10 pages |
| SHA-256 | `cf6646531ab79f16da502c2d11d50b0ffb3dd40d63b0e1c5097061d53430ca3a` |
| Text coverage | All pp. 1–10, references included; no appendix |
| Visual checks | Identity p. 1; all five figures pp. 2–4, 7; both tables p. 6; both metric equations p. 5 |

Scite exact identity agrees. Its omitted editorial-notices field does not establish absence of notices. The supplied PDF closes the earlier acquisition gap; full reading does not close all methodological gaps.

## Reconstructed design

The selector receives a product-development problem formulated from a publication abstract and recommends a specific ML algorithm. It is not given the underlying operational dataset for implementation/testing. The authors rephrase solution-specific abstracts into solution-neutral problems (PDF pp. 3–5, Figure 4).

Scopus and Web of Science searches find 3,791 records, 2,914 after deduplication, 1,087 after title screening and 170 after abstract screening. Suitable publications are divided into problem definition, concept development, embodiment design and detailed design: 47/41/43/39. Random downsampling gives **39 per phase, 156 cases**. The search covers English peer-reviewed engineering applications from 2004–2024 and excludes optimization/non-ML work, general frameworks and inaccessible publications. These decisions shape the target population; the cases are not a random sample of ordinary maintainer decisions.

GPT-4o, Gemini 1.5 Pro and Claude 3.5 Sonnet receive a common task/format instruction through APIs with default parameters (PDF p. 5). There is one evaluated response sequence per model/case, without stochastic repeats. When output is multiple or too general, conditional follow-up prompts request the most appropriate algorithm, or one per identified subproblem. The authors call these “one-shot” prompts; they are clarifications, not one-example demonstrations. The selected follow-up subset is not a randomized prompt comparison.

## Suitability is not exact-label agreement

The task-fulfilment rate is **fulfilled cases / all cases**. A response can count as fulfilled when it gives the published algorithm **or an alternative judged equally applicable from its characteristics** (PDF p. 5). Therefore this study must not be grouped with strict single-label pattern matching.

The identical-algorithm rate is instead **identical cases / fulfilled cases**, not identical cases / 156. Table 1 gives aggregate fulfilment 61%/54%/59% and conditional identity 43%/68%/50% for GPT/Gemini/Claude. The second set of percentages does not measure unconditional success.

Table 2 reports zero-shot ratios of 66%/73%/99%, conditional zero-shot fulfilment of 61%/62%/58% and conditional follow-up fulfilment of 62%/36%/100%. These cannot establish the causal benefit of another prompt: cases enter the follow-up group because of their preceding output, and Claude's group is very small.

The six failure classes include unsuitable algorithms, missing or excessive subproblems, general terms, non-ML solutions and one claim of unsolvability. Figure 5 preserves differences between models. Proposed explanations include missing problem information and inadequate knowledge, but the study does not experimentally isolate those mechanisms. The later GraphRAG lead is therefore consequential, not optional corroboration of an already settled cause.

The published method's suitability is assumed from peer review rather than retested (PDF p. 9). Valid-alternative judgments are sensible in principle, but independent/blinded rater procedures, a complete operational rubric and agreement statistics are not specified sufficiently to reconstruct them. No generated implementation, downstream task performance, actual user adoption or measured net savings is evaluated here.

## Artifact scope

Inspected [IPE-PEP/ICED25](https://github.com/IPE-PEP/ICED25/tree/a2c24b3c730257a1dc3f58ab783158755720d125), commit `a2c24b3c730257a1dc3f58ab783158755720d125`: README, search protocol and dataset structure. The JSON has four groups of 39, **156 unique problem formulations**, with only problem-formulation and published-algorithm fields. This verifies the released input inventory, not the reported model outcomes.

| Inspected artifact | SHA-256 |
| --- | --- |
| `README.md` | `78916b60b07733bb4ec1613c03dbfc1c0e321dd25dc43dea0d1912adb9cd348a` |
| `Created dataset/dataset.json` | `62be2d511d7deb1d79c542de37cf9cb8f757d515035b31f2fa14b5ccc56a1fd3` |
| Search-protocol TXT | `94975259d7c2da19f0ec3c032d447533989eb23cc6db95b5d33c62d04988ac02` |

The repository also lists phase-specific bibliographies; these were not exhaustively reconstructed. No per-model responses, alternative-adjudication logs or outcome tables are present in the inspected tree. Full-input extraction does not certify that every source abstract was independently revalidated.

## Consequence for ALF and next reading

**Correct/narrow:** suitability evaluation already admits valid alternatives. ALF's distinction cannot be “we accept alternatives”; it must concern observed maintenance consequences of advice under the allowed information and workflow. Recommendation performance is prior work, and reported task fulfilment is not deployment ROI.

**Retain and sharpen:** define behavioral acceptance before evaluating advice; preserve failed/abstained profiles; specify who judges alternatives and what the judge can see; account for all clarification/analysis work. Extra prompts alter the procedure and need a declared policy, not post-result rescue.

Promote the direct **2026 GraphRAG follow-up (S19)** before treating the 2025 discussion as the current frontier. Promote **GPT in Data Science (S20)** for implemented selection heuristics, **the conceptual MCDA framework (S21)** for explicit qualitative criteria/weights, and **Intelligent User Assistance (S23)** for natural-language advice and novice/simple-method comparators. These are identity/abstract-screened leads, not newly completed full readings. [The next-reading record](../selection-reading-next-2026-09-16.md) gives their order, access and potential to change the proposal.
