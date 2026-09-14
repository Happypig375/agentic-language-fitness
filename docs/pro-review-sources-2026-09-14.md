# Source audit for the architecture-maintenance plan review

**Date:** 2026-09-14. **Repository basis:** `73d0a2364640f6284a5ee3403d0e6562a4bbb520`.
Companion: [review findings](pro-review-2026-09-14.md), [revised proposal](architecture-maintenance-research-proposal-2026-09-14.md).

## Scope and question

This is a bounded critical review of the current claim and design, not a replacement for the extensive existing [proposal ledger](architecture-maintenance-proposal-sources-2026-09-14.md), not a full systematic review, and not a count of all papers relevant to architecture. The decision is whether the current proposal supports a small case-feasibility step and what must change before an interpretable maintenance comparison exists.

The screen prioritizes controlled source/predecessor interventions, inherited behavioral evaluation, software-architecture scenario analysis and measurement validity. Agent-harness, neural-model and other-domain architecture are different variables. Unassessed close leads are deferred, not declared absent or low quality. Already reviewed earlier work remains in its original ledger and is not counted as newly read here.

## Retrieval and pagination actually performed

Scite searches used relevance order, no date/publication/citation filters. Returned dates such as January 1 were not treated as preprint release dates.

| ID | Exact request | Returned extent |
| --- | --- | --- |
| S0 | Exact DOIs: CodeThread, SlopCodeBench, NITR, ALMA, Evolution of Functional UI Paradigms, hybrid-search journal paper | Offset 0, limit 10; 6 records / reported total 6. |
| S1 | `"coding agents" AND ("architectural" OR "minimal-pair" OR "code cleanliness") AND ("maintenance" OR "maintainability" OR "controlled")` | Offsets 0 and 20; requested/effective limit 20; 20 + 20 returned / reported total 1,713. Positions 41–1,713 unexamined. |
| S2 | `"architectural alternatives" AND ("coding agents" OR "large language models")` | Offset 0, requested/effective limit 20; 20 returned / reported total 86. Noisy cross-domain matches; remaining 66 unexamined, not evidence of absence. |

These are **66 retrieval positions / 64 distinct literal DOI identifiers**, not 64 independently read studies. S1 repeats two S0 identifiers. The graph records below are additional metadata/link discovery and are not added to a full-text reading count. This review did not stop at five results, but neither does 20 or 40 establish saturation.

The noisy S2 query is recorded as a specificity limitation, not a successful exhaustive exclusion of architectural alternatives. Its borderline software-design leads remain in the table. The bounded review proceeds on verified closest methods and explicitly limited claims; a publication-level novelty statement needs a completed separately defined search scope.

## Scite body access and primary-source fallback

| Source | Scite outcome | Actual primary reading in this pass |
| --- | --- | --- |
| Code Cleanliness, arXiv v1 `2605.20049` | `read_fulltext` offset 0/length 8,000 returned 0 characters, content denied. An earlier search OA flag did not provide a body. | [Primary HTML v1](https://arxiv.org/html/2605.20049v1): §§2–3, selected result definitions and §6 limitations. Minimal-pair construction, controls, reference tests and the independent-task rather than evolving-state limitation. Not a claimed entire-paper review. |
| SlopCodeBench, v2 `2603.24755` | Exact metadata and search excerpts; indexed snippets can describe a different edition. | [Primary HTML v2](https://arxiv.org/html/2603.24755v2): inherited-state protocol and evaluation/regression distinctions, especially §2.4. No transfer of older snippet counts into v2. |
| CodeThread, v1 `2606.21804` | Exact metadata and citation passages. | [Primary HTML v1](https://arxiv.org/html/2606.21804v1): introduction and §§3.1–3.3 predecessor construction/filtering and downstream task comparison. Working-predecessor filtering is a key distinction from our no-reset arm. |
| NITR, v1 `2603.27745` | Exact metadata, selected probe/oracle excerpts. | [Primary PDF v1](https://arxiv.org/pdf/2603.27745v1): introduction and §3 probe/oracle construction. The HTML route failed; PDF text supplied the method. No inference from diagram geometry is used. |
| Specification Emerges, v1 `2603.17104` | Search metadata and project-state snippets. | [Primary HTML v1](https://arxiv.org/html/2603.17104v1): §§2–3 task disclosure, evaluation and external project-state intervention. This is not an assigned application-package study. |
| GameEngineBench, v1 `2607.03525` | Search metadata and evaluation excerpts. | [Primary HTML v1](https://arxiv.org/html/2607.03525v1): runtime/evaluation §5 and limitations, including post-solve LLM judging and wrappers. No model-ranking result imported. |
| ALMA, `10.1016/S0164-1212(03)00080-3` | Metadata available; body not supplied through the exact lookup. | [Author paper](https://www.cs.vu.nl/~hans/publications/y2004/alma.pdf): scenario elicitation §4.3 and alternatives §§7.1–7.3. Original page 14 was also rendered; this does not mean all figures were reviewed. |
| Sperber/Schlegel, `10.1145/3759163.3760429` | `read_fulltext` offset 0/length 8,000 returned 0 characters, denied. | Official proceedings/author metadata followed by [author PDF](https://www.deinprogramm.de/sperber/papers/funarch-ui.pdf): selected architecture/MVC, Universe/Elm/MVU and conclusion passages. Conceptual trade-offs, not controlled maintenance outcomes. |
| Wohlin et al., `10.1016/j.infsof.2022.106908` | Actual `source: fulltext`, offset 0, returned 8,000 of 55,842 characters, `hasMore: true`. | Introduction/search-strategy definitions and beginning of related work only. Supports planned-search versus ad-hoc distinction; not a claim to have replicated the full method. |

Primary versions, not mirrored AI summaries, support the revised methods. Discovery pages such as generated paper overviews, vendor validation blogs and search snippets are not evidence for experimental results. Readable text and source identity were checked separately; no access restriction was bypassed.

## Citation graph checks

**G1:** incoming from Code Cleanliness, CodeThread and NITR; depth 1, maximum 50 edges, intent/snippets enabled. Returned **0 edges / 3 nodes**, not truncated; all three seeds were flagged low-coverage. This supports no conclusion about actual follow-on work. Keyword and primary-method follow-up supplied the review.

**G2:** outgoing from ALMA and the 2022 hybrid-search journal work; depth 1, maximum 30 edges, intent/snippets enabled. Scite automatically added linked arXiv `2307.02612`. Returned **30 edges / 33 nodes, truncated true**. ALMA and the linked preprint had zero seed coverage; the journal had 30. The graph is not an exhaustive literature screen. The linked preprint is not a new replication.

The G2 snippets mostly locate methods/background references; supporting labels about hybrid search are not evidence for ALF's architectural hypothesis. The journal's actual introduction was read before using its method distinction. The other targets below remain metadata/context leads, not 30 read studies. The Wohlin 2014 author PDF was opened as a method lead but was not used for an additional detailed methods claim.

## Source decisions

C = credited for the bounded claim in the reading table; D = relevant/possibly relevant but deferred or access-limited, **not scientifically rejected**; N = not used for this decision because the retrieved material concerns a different variable/domain/study type. Titles below are compact labels for readability, not authoritative bibliography entries. Citing one work twice is not a second independent source.

The final Scite decision record uses answer key `alf-pro-review-2026-09-14`. Its binary cited/excluded vocabulary maps D to not-credited with an explicit deferral reason. Service acceptance is checked at handoff; that record is provenance, not PRISMA certification or completeness of field coverage.

| Query position | DOI | Short label | Status and reason |
| --- | --- | --- | --- |
| S0:1 | `10.48550/arxiv.2606.21804` | CodeThread | C — Primary v1 predecessor and downstream-task methods assessed. |
| S0:2 | `10.48550/arxiv.2603.24755` | SlopCodeBench | C — Primary v2 inherited-state, evaluation and regression distinctions assessed. |
| S0:3 | `10.48550/arxiv.2603.27745` | Needle in the Repo | C — Primary v1 probe and functional/structural oracle construction assessed. |
| S0:4 | `10.1016/s0164-1212(03)00080-3` | ALMA | C — Primary author paper scenario and alternative-comparison sections assessed. |
| S0:5 | `10.1145/3759163.3760429` | Evolution of Functional UI Paradigms | C — Primary author paper selected architectural trade-offs; not an agent experiment. |
| S0:6 | `10.1016/j.infsof.2022.106908` | Hybrid database search and snowballing | C — Scite body introduction/search definitions read; not the whole study. |
| S1:1 | `10.48550/arxiv.2605.20049` | Code Cleanliness | C — Primary v1 minimal-pair methods and limitations assessed; close predecessor. |
| S1:2 | `10.48550/arxiv.2511.04824` | Agentic Refactoring | D — Observational refactoring lead; no new full-methods assessment in this pass. |
| S1:3 | `10.48550/arxiv.2608.03392` | Self-Evolving Coding Agents | N — Agent-system evolution rather than assigned software-architecture contrast. |
| S1:4 | `10.48550/arxiv.2605.08366` | SWE Atlas | D — Related engineering-workflow benchmark; selected snippets, no full-methods exclusion claim. |
| S1:5 | `10.48550/arxiv.2603.27745` | Needle in the Repo | C — Duplicate S0 identifier; credited once at work/version level. |
| S1:6 | `10.48550/arxiv.2602.09185` | AIDev | N — Observational contribution dataset; not the current assigned-package mechanism. |
| S1:7 | `10.48550/arxiv.2606.26924` | Deterministic Control Plane | N — Harness/configuration control rather than maintained-program architecture. |
| S1:8 | `10.48550/arxiv.2510.08511` | AutoMLGen | N — Machine-learning optimization agent, outside the current maintenance contrast. |
| S1:9 | `10.48550/arxiv.2512.21373` | AInsteinBench | D — Scientific-repository benchmark lead; no full-methods assessment here. |
| S1:10 | `10.48550/arxiv.2512.12216` | Training Versatile Coding Agents | N — Agent training/environment construction, not the proposed architectural intervention. |
| S1:11 | `10.48550/arxiv.2604.13107` | Can Coding Agents Be General Agents? | N — General business automation capability, outside current scope. |
| S1:12 | `10.48550/arxiv.2603.24755` | SlopCodeBench | C — Duplicate S0; primary v2 controls interpretation, not older indexed excerpts. |
| S1:13 | `10.48550/arxiv.2604.11045` | Sema Code | N — Agent infrastructure architecture rather than target-program organization. |
| S1:14 | `10.48550/arxiv.2607.12220` | Contract-Grounded Behavior Trees | N — Robot behavior synthesis, not longitudinal software-package maintenance. |
| S1:15 | `10.1145/3786335.3813223` | Hedwig | N — Autonomy/oversight intervention, not the selected program-architecture contrast. |
| S1:16 | `10.48550/arxiv.2607.02807` | SwarmResearch | N — Open-ended search-agent orchestration, not assigned application packages. |
| S1:17 | `10.48550/arxiv.2601.16746` | SWE-Pruner | D — Relevant context-policy lead for a later H intervention; not newly assessed. |
| S1:18 | `10.48550/arxiv.2606.13175` | The End of Code Review | N — Position/synthesis claim, not primary empirical evidence for this package effect. |
| S1:19 | `10.48550/arxiv.2602.05892` | ContextBench | D — Relevant retrieval metrics; prior project evidence retained, no new full review. |
| S1:20 | `10.48550/arxiv.2602.17037` | Wink | D — Runtime agent-intervention lead, not current program-architecture evidence. |
| S1:21 | `10.48550/arxiv.2607.25431` | CodeNib | D — Repository-context serving; possible future retrieval mechanism, not assessed here. |
| S1:22 | `10.48550/arxiv.2512.12730` | NL2Repo-Bench | N — From-scratch generation rather than the selected inherited contrast. |
| S1:23 | `10.48550/arxiv.2606.01522` | Type-Error Ablation and AI Coding Agents | D — Important compiler-feedback mechanism lead; metadata/excerpts only in this pass. |
| S1:24 | `10.48550/arxiv.2607.21217` | ICAE-Bench | D — Interactive project-building lead; full methods not assessed. |
| S1:25 | `10.48550/arxiv.2607.20759` | IssueTrojanBench | N — Malicious-request security evaluation, not current question. |
| S1:26 | `10.48550/arxiv.2601.21372` | NEMO | N — Optimization modelling workflow, not program architecture maintenance. |
| S1:27 | `10.48550/arxiv.2605.08468` | PYTHALAB-MERA | D — Validation-conditioned memory; later policy lead, not adopted. |
| S1:28 | `10.48550/arxiv.2607.13080` | Inference Economics of Enterprise Coding Agents | D — Cost-ecology lead; access/abstract-level only, not a source for current quantitative claims. |
| S1:29 | `10.48550/arxiv.2605.14859` | Least-Privilege Authorization | N — Permission-policy inference rather than maintenance architecture. |
| S1:30 | `10.48550/arxiv.2602.18571` | Debug2Fix | D — Debugger/subagent lead relevant to optional repair work, not assessed as current evidence. |
| S1:31 | `10.48550/arxiv.2601.17581` | How AI Coding Agents Modify Code | N — Observational pull-request changes, not controlled architectural alternatives. |
| S1:32 | `10.48550/arxiv.2603.15566` | Lore | D — Commit-message memory intervention; keep separate from source-only inheritance. |
| S1:33 | `10.48550/arxiv.2607.03525` | GameEngineBench | C — Primary v1 runtime evaluation and judge/wrapper limitations assessed. |
| S1:34 | `10.48550/arxiv.2605.00803` | Materials-Science Reproduction | N — Scientific reproduction, not assigned architecture maintenance. |
| S1:35 | `10.48550/arxiv.2607.06184` | What Resolve Rate Hides | D — Trajectory diagnostic lead; selected snippets do not establish complete method comparison. |
| S1:36 | `10.48550/arxiv.2607.02134` | Scientific ML Paper Replication | N — Research reproduction workflow rather than the target maintenance estimand. |
| S1:37 | `10.48550/arxiv.2603.17104` | When the Specification Emerges | C — Primary v1 requirement-disclosure and project-memory methods assessed. |
| S1:38 | `10.48550/arxiv.2607.07744` | PERFOPT-Bench | D — Performance optimization/relay-policy lead, outside this bounded primary comparison. |
| S1:39 | `10.48550/arxiv.2605.05138` | Executable World Models for ARC | N — Interactive puzzle/world-model generation, not this maintenance design. |
| S1:40 | `10.48550/arxiv.2603.21698` | Vehicle Aerodynamics Coding Agents | N — Domain workflow blueprint, not controlled downstream package evidence. |
| S2:1 | `10.48550/arxiv.2601.20546` | Verbal creativity | N — Unrelated outcome; architecture term did not identify software maintenance. |
| S2:2 | `10.1002/cncy.70134` | Cytopathology LLM review | N — Different clinical domain. |
| S2:3 | `10.69591/jcai.3.1.1` | AI-Driven Software Architecture Decision Support | D — Potentially relevant conceptual decision-support lead; full methods unavailable/unassessed, not rejected for quality. |
| S2:4 | `10.21203/rs.3.rs-8745792/v1` | Clinical retrieval privacy | N — Clinical modelling architecture, not maintained code. |
| S2:5 | `10.48550/arxiv.2608.28930` | Hallucination probes | N — Model-internal representation, not software architecture. |
| S2:6 | `10.48550/arxiv.2510.01817` | Sparse Query Attention | N — Neural attention architecture, different variable. |
| S2:7 | `10.48550/arxiv.2602.09009` | ANCRe | N — Neural network depth/connections, different variable. |
| S2:8 | `10.1002/inst.70052` | Rules to Agentic Swarms | N — Broad systems/AI position article, not empirical target-package evidence. |
| S2:9 | `10.48550/arxiv.2606.21377` | ARENA | N — Cyber-defense transfer across environments, not code-maintenance packages. |
| S2:10 | `10.1101/2025.04.25.25326437` | Pediatric LLM evaluation | N — Clinical questions, different domain. |
| S2:11 | `10.48550/arxiv.2607.22598` | Didactical teacher assistant | N — Educational assistant, not the maintenance outcome. |
| S2:12 | `10.64898/2025.12.19.25342205` | Dermatology explainable AI | N — Different clinical/human-factors outcome. |
| S2:13 | `10.48550/arxiv.2601.16905` | GRIP unlearning | N — Model unlearning architecture, not source-code organization. |
| S2:14 | `10.48550/arxiv.2601.08070` | Semantic Gravity Wells | N — Negative-instruction behaviour, not architecture maintenance. |
| S2:15 | `10.48550/arxiv.2604.17769` | Reverse Constitutional AI | N — Adversarial data generation, different intervention. |
| S2:16 | `10.1002/iis2.70163` | SysML safety trade-offs | D — Adjacent architecture-design/hazard evaluation; no downstream executable-method assessment here. |
| S2:17 | `10.3390/data11060126` | Dated-text gender embeddings | N — Different semantic modelling domain. |
| S2:18 | `10.48550/arxiv.2512.22568` | Neuroscience for AI | N — AI/neural architecture argument, not maintained software architecture. |
| S2:19 | `10.48550/arxiv.2606.27023` | Medical VQA calibration | N — Different clinical/model-calibration outcome. |
| S2:20 | `10.48550/arxiv.2607.28307` | Text Requirements to Microservice Architectures | D — Architecture synthesis and expert ratings; selected excerpts only, detailed later-maintenance exclusion remains unassessed. |

### G2 targets not independently assessed

These graph targets are retained for reproducibility, not credited as additional evidence in the current proposal. Future searches may prioritize the methods/replication leads if they change a decision; there is no requirement to recursively read every industry-collaboration paper linked from a search-method study.

```text
10.1007/11767718_3
10.1007/978-90-481-9849-8_17
10.1007/bf02919966
10.1007/s10664-008-9060-1
10.1007/s10664-008-9091-7
10.1007/s10664-010-9134-8
10.1016/j.infsof.2010.12.010
10.1016/j.infsof.2016.07.006
10.1016/j.infsof.2020.106294
10.1016/j.infsof.2020.106366
10.1016/j.jss.2013.04.076
10.1109/cesi.2013.6618469
10.1109/csee.1999.755175
10.1109/cseet.2009.22
10.1109/esem.2017.30
10.1109/icre.1998.667818
10.1109/itng.2009.134
10.1109/mc.2008.85
10.1109/ms.2006.147
10.1109/ms.2011.92
10.1109/se.2012.6242350
10.1109/seaa.2019.00061
10.1109/tse.2010.28
10.11139/cj.30.1.10-15
10.1145/1449603.1449609
10.1145/2372251.2372257
10.1145/2460999.2461020
10.1145/2601248.2601268
10.1145/2647648
10.1145/2647648.2647649
```

## Primary repository evidence

At Nu commit `064f7ae92a8506689cd91aff5e6804a375d6ef3d`, the GitHub connector supplied `Projects/Breakout Mmcc/Gameplay.fs` lines 1–150 and `Projects/Breakout ImSim/Gameplay.fs` lines 1–180. These show explicit gameplay-model/manual update logic versus screen/entity properties and dynamic-body interactions. MMCC also calls world effects; do not call it a strictly pure functional core. This is source inspection, not runtime parity, headless feasibility or a published paradigm comparison.

The ALF proposal, plan, agent instructions, source ledger, search-depth audit and CI policy were read at the review head. Historical literature evidence is reused only with its existing declared limits. No private chat material is promoted to independent corroboration of its own synthesis.

## How the reading changed the plan

- Minimal-pair code quality is a direct predecessor; strengthen the contribution around prospective responsibility/change predictions, not a missing-keyword combination.
- Working-predecessor comparisons and inherited broken-state experiments estimate different things; add an explicit claim tier and bounded clean-reference-control option.
- Structural compliance and actual future behavioral obligations are separate outcomes.
- Memory/project-state support is an intervention; source-only inheritance must be distinguished from notes and persistent context.
- Scenario goals determine which contrasts are informative; equal requirements do not require equal architectural edit difficulty.
- Real-engine claims need actual runtime witnesses, with physics/API differences visible rather than silently abstracted away.
- Search and graph limits remain explicit. No empty graph, source count or citation classification establishes novelty or an F#/Nu advantage.

Outstanding queue for a later decision-focused pass: source-level/type-error feedback mechanisms; potentially close architecture decision-support and microservice-synthesis methods; independent follow-ons missing from thin preprint citation graphs. These do not prevent a narrowly labelled A0 feasibility decision, but they prevent claiming this bounded search exhausts the research area.
