# Targeted full-reading queue: architectural choice and selection validity

**Added 2026-09-15; input `f1bea15451d14b1027c356e0b2830acd85a86aa6`.** This is a DOI acquisition/reconstruction handoff, not a record of completed full reading or an experimental allocation. [PLAN](../../PLAN.md), the [review](../selection-evidence-closure-2026-09-15.md) and [source audit](../selection-evidence-closure-sources-2026-09-15.md) govern scope.

The earlier P01–P13 and A01–A03 identifiers and coverage are unchanged. The S-identifiers below are local to this queue until a later reading index reconciles them. Check the existing Zotero collection by DOI/title/version before additions; no new Zotero record or stored PDF was created in this pass. Related preprints/publisher editions are not independent studies.

## Priority full reads

Read S01–S03 first. S04–S05 carry forward already identified acquisition gaps. Do not restart the original sixteen readings. A full read is worthwhile because each item can change a specific contribution or method decision, not because its title adds another citation.

| ID | Work and DOI | Current evidence and lawful route | Required reconstruction and consequence |
| --- | --- | --- | --- |
| **S01** | **ASlib: A benchmark library for algorithm selection** — `10.1016/j.artint.2016.04.003` | New method priority. Publisher identity verified; related accepted preprint `10.48550/arXiv.1506.02465`, **v3**, is [accessible](https://arxiv.org/pdf/1506.02465v3). Selected parsed PDF sections inspected only; screenshots failed. The 36-page preprint is not certified identical to the publisher edition. | Reconstruct fixed/virtual-best comparators, instance splits and nesting, feature-time accounting, failed/missing runs, metric normalization and selection of scenarios. Identify conventions ALF should reuse and ones it must not copy, especially outcome exclusions/imputation and stochastic hindsight. |
| **S02** | **Using Generative Artificial Intelligence for Suggesting Software Architecture Patterns from Requirements** — `10.1007/978-3-031-66336-9_19` | Existing priority retained. [Publisher](https://doi.org/10.1007/978-3-031-66336-9_19) abstract/notes and linked author result artifact inspected; full chapter body denied by Scite. Author/institution or legitimate library copy needed. | Reconstruct dataset authorship, labels and valid alternatives, train/test separation, input prompts, multiple-label scoring and whether any downstream execution occurs. Resolve the observed Test 2/3 ambiguities without assuming artifact-only evidence describes the full study. Revise novelty at the level of actual outcomes, not the word recommendation. |
| **S03** | **Failure-Aware Enhancements for Large Language Model (LLM) Code Generation: An Empirical Study on Decision Framework** — `10.48550/arXiv.2602.02896` | Newly promoted. Primary [v1](https://arxiv.org/abs/2602.02896v1) methods/discussion inspected. DOI and v1 identity verified; no new full-PDF claim. The primary paper links artifact DOI `10.5281/zenodo.17637008`, not yet inspected here. | Reconstruct selected-failure sampling, model/information differences, manual completion scoring, times and excluded costs, the derivation of the recommendation table, and any independent prospective validation. Separate a demonstrated method outcome from a post-hoc rule. Do not import numeric magnitudes or causal claims without this reconstruction. |
| **S04** | **MicroRec: Leveraging Large Language Models for Microservice Recommendation** — `10.1145/3643991.3644916` | Existing priority narrowed, not discarded. [Official MSR abstract](https://2024.msrconf.org/details/msr-2024-technical-papers/21/MicroRec-Leveraging-Large-Language-Models-for-Microservice-Recommendation) establishes query/retrieval/ranking; ACM full text unavailable here. Do not confuse with the unrelated FPGA paper using MicroRec as its title. | Establish candidate service corpus, actual role of Stack Overflow and registry documents, relevance ground truth, leakage/splits, Docker Hub baseline and any implemented/downstream outcome. The known ranking target is not enough to assert the whole paper lacks maintenance evidence. |
| **S05** | **Generative AI for software architecture. Applications, challenges, and future directions** — `10.1016/j.jss.2025.112607` | Carry forward publisher-version review. Related preprint `10.48550/arXiv.2503.13310`; prior selected reading remains selected. [Publisher route](https://doi.org/10.1016/j.jss.2025.112607). | Reconcile editions, dates/search cutoff, inclusion rules and source-to-outcome table. Follow only primary studies that could close the exact decision-value gap. Do not convert a historic survey's open problem into present nonexistence evidence. |

Copyable priority DOI list (publisher identity preferred; deduplicate against the library):

```text
10.1016/j.artint.2016.04.003
10.1007/978-3-031-66336-9_19
10.48550/arXiv.2602.02896
10.1145/3643991.3644916
10.1016/j.jss.2025.112607
```

ASlib's related open preprint identifier, as an alternative edition of S01:

```text
10.48550/arXiv.1506.02465
```

## Conditional full readings, not automatic scope expansion

| ID | DOI / work | Trigger and exact decision |
| --- | --- | --- |
| **S06** | `10.1007/s10994-022-06161-4` — **Algorithm selection on a meta level** | Promote before using estimated oracle/headroom normalization, learned/ensemble selectors or its uncertainty conventions. Selected primary HTML sections 2 and 6.1 already establish expected-performance and information-cost distinctions. A complete reading should reconstruct data subsets, baseline selection, exclusions and validation; do not build a meta-selector merely because the paper exists. |
| **S07** | `10.1017/pds.2025.10100` — **Can large language models support machine learning implementation in product development? A comparative analysis and perspectives** | Promote before claiming recommendation usefulness beyond label/applicability judgments or adapting its problem-formulation protocol. Selected primary HTML sections 2.2–2.4 and 4.3 distinguish accepted alternative algorithms from exact matches and disclose untested underlying validity/output variability. Reconstruct judgments, solution-neutralization, prompt retries and execution evidence. |

```text
10.1007/s10994-022-06161-4
10.1017/pds.2025.10100
```

Other verified discovery identities are **Rice (1976)** `10.1016/S0065-2458(08)60520-3` and **Kotthoff's survey (2014)** `10.1609/aimag.v35i3.2460`. They support historical orientation through exact metadata and later primary methods; full reading is optional if history or missing method coverage makes it decision-critical. The Purdue 1975 Rice report is an earlier edition, not automatically the 1976 chapter. Do not add both as independent studies or make both full reads compulsory before cheap A0 feasibility.

## What to do after each PDF is read

1. Verify DOI/title/authors, edition/date/notices and attachment identity. Preserve lawful source, PDF hash and actual text/visual/appendix/supplement coverage. A parser, abstract or artifact read cannot complete the PDF checklist. Note missing figures, clipped pages and unavailable artifacts honestly.
2. Reconstruct **decision object and available information -> procedure/training -> comparator -> outcome generation -> scoring/uncertainty -> claim**, with page/section/table locators. Separate reported facts from assumptions and from ALF's proposed adaptation.
3. Record true independent cases, repeated runs, missingness, selected populations, costs, useful alternatives and counterevidence. Recalculate only published arithmetic when possible; mark experimental reproduction separately.
4. Update the evidence matrix: whether the study already evaluates the proposed contribution, which narrower distinction remains, which baselines/controls are reusable, and which asserted benefit is unsupported. Withdraw overlaps; preserve useful replication/adaptation options.
5. Revise PLAN and the active proposal if a material result changes the contribution or control. Do not simply append a new paper summary while leaving a contradicted claim live. Preserve the earlier record as history.

After S01–S05 or a documented access block, return an explicit **unique/value/validity** disposition and the smallest next decision. S06/S07 are promoted only by their triggers. Global novelty need not be proven to propose bounded exploratory A0, but no missing source can be treated as absence. Do not hold all useful work indefinitely for unrelated literature.

## Acquisition and execution boundaries

Use Scite for exact identities, lawful access and citation contexts; literature searches request 20 items and relevant pagination beyond the first page. Full-reading status requires actual PDFs and necessary supplements, not mosaics of snippets. Inspect primary versions when source dates or titles conflict. The incorrectly queried `10.1016/j.artint.2015.08.003` is **not ASlib**; its identity is quarantined in the audit and must not be imported as S01.

These are research-reading tasks only. No acquisition failure permits bypassing access controls. No new PDF is committed into the public repository by default. No model/candidate probes, repairs, A0 construction, recruitment or extra workers are authorized by this queue. A missing full text produces a DOI-specific access request and affected-claim list, not invented method details or a restarted broad search.
