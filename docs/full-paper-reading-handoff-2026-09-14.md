# Full-paper evidence reconstruction: next maintainer assignment

**Requested 2026-09-14; starting head `fc4762b636421f6fc6aba2eca473cd1bf9c89ad1`.** This document defines the next literature assignment. It does not report that any PDF has been newly downloaded or read in full. Prior reviews retain their actual selected-section/abstract reading status. Read with [PLAN.md](../PLAN.md) and [the scite procedure](research-loop-and-scite.md).

## 1. Decision and boundary

Before requesting A0 construction, reconstruct the evidence, methods, assumptions, results and implications from the complete papers underlying the active proposal. Reassess whether prospective architecture-package predictions, inherited-state controls and any later feedback/context intervention form an informative gap. The objective is **a defensible evidence-to-design reconstruction**, not a larger citation count or a generic paper-summary collection.

The assignment includes lawful PDF acquisition/reuse, full reading, targeted primary-artifact inspection, small model-free arithmetic checks, synthesis, corrections to the active proposal/plan and direct publication of those documents. It does not authorize A0/A1 construction, reference-change implementation, a candidate adapter, replication runs, model/count probes, extra paid review workers, recruitment, OAuth staging or new experimental allocation. All existing live holds remain in place.

The user's new reading-first instruction supersedes the previous immediate handoff to an A0 authorization decision. A0 remains a possible downstream decision **after** this evidence reconstruction and its review; it is not presumed to survive unchanged.

## 2. Core PDFs to acquire and read in full

This is a bounded priority list of **11 works**, not all 60 DOI identifiers in the last discovery audit. All eleven are queued for full-PDF reconstruction. Their descriptions below are **questions to resolve**, not conclusions to copy from the earlier summaries. Start acquisition of P01 early because the previous pass could access only an official abstract; continue with accessible papers while pursuing lawful access rather than stalling the entire queue.

### Batch A — architecture rationale, nearest comparisons and validity of the gap

| ID | Paper | DOI to resolve/download | Prior-review edition / acquisition hint | Reconstruct and decide |
| --- | --- | --- | --- | --- |
| P01 | LLMs for Architectural Refactoring: An Exploratory Study on Monoliths to Microservices | `10.1109/ICSA66085.2026.00033` | ICSA 2026 proceedings; previous body access failed. Use publisher, authorized institution or verified author manuscript; verify deposit lineages rather than guess them. | What architectural alternatives are actually constructed, which baselines/metrics/experts are used, and are later behavioral changes tested? Does it occupy more of the proposed gap than the abstract review could establish? |
| P02 | Architecture-level modifiability analysis (ALMA) | `10.1016/S0164-1212(03)00080-3` | JSS 2004; prior author route: `https://www.cs.vu.nl/~hans/publications/y2004/alma.pdf`. Verify manuscript versus published edition. | Recover the full analysis process, alternative-comparison goals, scenario elicitation/selection, validation, evidence and limitations. Which parts justify prospective prediction cards, and which require new validation for agents? |
| P03 | Does Code Cleanliness Affect Coding Agents? A Controlled Minimal-Pair Study | `10.48550/arXiv.2605.20049` | Prior-review arXiv v1. | Reconstruct pair construction in both directions, changed architecture/quality properties, task sampling, sensitive/insensitive controls, model/harness policy, test adequacy and statistics. Recheck exactly what remains distinct in ALF. |
| P04 | Is Agent Code Less Maintainable Than Human Code? (CodeThread) | `10.48550/arXiv.2606.21804` | Prior-review arXiv v1. | Reconstruct predecessor generation, acceptance/filtering, current versus future requirements, downstream-task matching, behavior checks, regression analysis and limits. Determine which inherited-state comparison is actually identifiable. |
| P05 | SlopCodeBench: Benchmarking How Coding Agents Degrade Over Long-Horizon Iterative Tasks | `10.48550/arXiv.2603.24755` | Prior-review arXiv v2; do not mix v1 sample counts with v2. | Recover complete task/trajectory construction, specification disclosure, reset and feedback rules, cumulative/isolated scoring, structural metrics, human-code comparison, prompt interventions and failures. Which outcomes already answer the proposed question? |
| P06 | ChainSWE: Benchmarking Coding Agents on Multi-Bug Software Maintenance | `10.48550/arXiv.2607.02606` | Prior-review arXiv v1. | Reconstruct oracle-predecessor, inherited-state, fresh/persistent and subagent conditions from the actual protocol and appendices. Identify jointly changed factors, filtering and reset rules; do not infer a clean memory effect from a mode name. |
| P07 | Needle in the Repo: A Benchmark for Maintainability in AI-Generated Repository Edits | `10.48550/arXiv.2603.27745` | Prior-review arXiv v1. | Reconstruct starter shaping, probes, architecture constraints, functional/structural oracles and scoring. Separate declared conformance from demonstrated downstream maintenance benefit; challenge ALF's package/oracle novelty. |

### Batch B — feedback, memory, requirements and runtime evidence

| ID | Paper | DOI to resolve/download | Prior-review edition | Reconstruct and decide |
| --- | --- | --- | --- | --- |
| P08 | Type-Error Ablation and AI Coding Agents | `10.48550/arXiv.2606.01522` | arXiv v2; earlier scite body had no verified version marker. | Read all reporting modes, injected errors, model/manual exposure, repair oracle, budgets, ablations, statistical units and limitations. When is diagnostic detail beneficial, and what cannot transfer from this language/task population? |
| P09 | The Complexity Trap: Simple Observation Masking Is as Efficient as LLM Summarization for Agent Context Management | `10.48550/arXiv.2508.21433` | arXiv v3, including the revised scaffold/generalization and hybrid material. This DOI is not COMPASS. | Reconstruct exact retained/masked material, tuning, baselines, accounting, caches, budgets and denominators. Distinguish cost reduction from maintained accuracy, and old observations from useful active feedback. |
| P10 | When the Specification Emerges: Benchmarking Faithfulness Loss in Long-Horizon Coding Agents | `10.48550/arXiv.2603.17104` | Prior-review arXiv v1. | Recover progressive/upfront information, persistent commitments, notes/project-state interventions, scoring and structural judgements. Decide which information must remain equal in source-only inherited maintenance. |
| P11 | GameEngineBench: Evaluating Coding Agents on Real C++ Runtime Environments | `10.48550/arXiv.2607.03525` | Prior-review arXiv v1. | Recover real runtime setup, engine/task selection, test and judge roles, wrapper differences, native dependencies, nondeterminism and validation limits. Decide what a credible Nu A0 runtime/oracle witness must demonstrate. |

Resolve arXiv DOIs at `https://arxiv.org/abs/<identifier>` and download the selected version using `https://arxiv.org/pdf/<identifier>vN`. A DOI identifies the work, not the exact PDF bytes. The editions above reconstruct the previous review; verify current primary version history on acquisition. Preserve the historical-claim edition and record any newer edition separately. If it changes relevant methods/results, read the new edition fully and compare affected historical passages; never silently overwrite old results or count versions as independent experiments.

### Copyable core DOI import list

```text
10.1109/ICSA66085.2026.00033
10.1016/S0164-1212(03)00080-3
10.48550/arXiv.2605.20049
10.48550/arXiv.2606.21804
10.48550/arXiv.2603.24755
10.48550/arXiv.2607.02606
10.48550/arXiv.2603.27745
10.48550/arXiv.2606.01522
10.48550/arXiv.2508.21433
10.48550/arXiv.2603.17104
10.48550/arXiv.2607.03525
```

### Conditional full readings — promote only for the stated decision

These are not quietly mandatory extra studies. Record `promoted` with a reason or `deferred` with its trigger. A conditional source may not support a detailed methods claim until it has the required reading evidence.

| DOI | Paper | Trigger |
| --- | --- | --- |
| `10.1145/3759163.3760429` | Evolution of Functional UI Paradigms | Retaining a substantive functional-UI architectural lineage or trade-off explanation for the chosen case. Conceptual examples do not establish an agent effect. |
| `10.1007/s10664-008-9102-8` | Guidelines for conducting and reporting case study research in software engineering | Finalizing the formal comparative-case protocol, triangulation or generalization argument beyond this initial evidence reconstruction. |
| `10.1016/j.infsof.2022.106908` | Successful combination of database search and snowballing for identification of primary studies in systematic literature studies | Designing/claiming a systematic hybrid literature search rather than the current bounded reconstruction. |
| `10.48550/arXiv.2606.00408` | Masking Stale Observations Helps Search Agents -- Until It Doesn't: A Regime Map and Its Mechanism | Proposing or claiming novelty for a new masking, repair-history or context-policy experiment. Verify its actual domain and methods before transferring it to coding. |

Other relevant deferred records remain in the existing ledgers. Promote a newly found near-duplicate or decisive counterexample when it could change the current decision; record the scope change. Do not recursively download every reference or turn a bounded reconstruction into an unending search.

## 3. Acquisition, identity and storage

First inspect existing approved Project/Library files, reference-manager attachments and local paper storage. Reuse an already available matching PDF instead of creating another library or assuming a citation means a file exists. This instruction does not authorize moving, uploading or sharing the user's library. No new connector/storage service or automated downloader framework is needed.

For each paper record DOI, full title/authors, publication status, chosen version/date, primary landing/PDF URL, actual retrieval date, PDF SHA-256, page count, supplement identities and an actual retrievable file/attachment reference. Record existing attachment IDs when available. Never invent a mounted path, access result or PDF hash. Distinguish accepted manuscript, published version, preprint and supplemental deposit.

Use lawful publisher, arXiv, author/institutional routes or user-provided PDFs. Check for corrected/retracted editions. A publisher denial, abstract-only page or unrelated PDF is not a full paper. P01 is access-limited until a verified body is actually obtained. An access flag in scite is not a download confirmation.

Keep PDF binaries and extracted copyrighted bodies in an approved noncommitted location; do not bulk-commit them into the repository or assume that an open-access flag permits redistribution. Commit our original paraphrases, metadata, short permitted quotations, page locators and small derived calculations with provenance. The reading record must locate the PDF without exposing access tokens, credentials or private absolute paths.

If a core paper remains unavailable after checking existing files and legitimate routes, log the attempts, continue the accessible core, and return a precise DOI/upload/access request. Mark the overall handoff `partial/access-blocked`, not complete, and keep claims depending on that paper unresolved. Do not fabricate its methods or exclude it on scientific merit.

## 4. What counts as fully read

Read the entire verified paper: abstract, introduction, theory/formalism, methods, experiments or cases, all results, discussion, limitations, conclusion, footnotes, captions and appendices. Inspect the bibliography for relevant leads; this does not require reading every cited work. Read separately hosted supplements when they define the treatment, outcome, exclusion, prompts or analysis on which the claim depends. Missing such material remains an explicit method-reconstruction limitation.

Use PDF text extraction for navigation and continuous reading, and render original pages to inspect tables, equations, diagrams, code listings and ambiguous layout. When using Chat's web PDF reader, use its screenshot facility for the PDF analysis; in a local agent use the available PDF renderer/vision tool. Do not substitute OCR unless the document cannot otherwise be read. A text extractor having processed every byte does not mean the agent read every section.

Track actual page/section ranges consumed, figures/tables checked, appendices/supplements covered, undeciphered passages and unresolved terms. Use both PDF page index and printed page/section/table identifiers when they differ. Do not invent coverage from scite character offsets or an author's abstract. `read_fulltext` with `hasMore: true`, a citation-snippet mosaic, HTML selected sections, or a prior assistant summary cannot close this full-PDF assignment by itself.

A `full_read_complete` paper has a verified PDF, complete coverage record and a written reconstruction with locators. Keep `method_reconstruction_complete` separate: a paper may be fully read yet omit code, parameters or raw data essential to replicate its conclusions. Likewise, distinguish paper reading, artifact inspection, arithmetic verification and experimental reproduction; this assignment does not rerun the papers' experiments.

## 5. Per-paper reconstruction, not just a summary

For each core paper create/update a concise structured note under `docs/literature/full-reading/`. Use stable short IDs from the table, e.g. `P04-codethread.md`. The directory is a home for notes, not another workflow framework. Every nontrivial evidence claim needs PDF/section/table locators.

| Component | Required reconstruction |
| --- | --- |
| Identity and coverage | Exact work/version/PDF hash, full-read coverage, supplement/artifact availability, reviewer identity/type and remaining unknowns. |
| Research problem and contribution | What was unknown to the authors, the question they actually test, and their claimed contribution. Distinguish the authors' claim from our judgement. |
| Evidence-generating method | Population/case, source sampling, construction and filtering; treatment and comparator; assignment/randomization; independent unit versus repeats; baseline/predecessor validity; sequence and persistence. |
| Agent or architecture conditions | Model/scaffold/version, prompts, documentation, source access, tools, diagnostic/test feedback, memory, budgets, retries, stop rules, and bundled changes. Use `not reported` rather than guess. |
| Outcomes and oracle | Exact success/maintenance/cost definitions, structural versus behavioral judgement, exposure of tests/holdouts, missingness, validity and judge calibration. |
| Results and arithmetic | Main effect direction and magnitude, numerator/denominator, unit and uncertainty; important null/contrary results and ablations. Recompute headline percentages/ratios from published numbers where possible and preserve code/output. Do not reconstruct absent raw trials or p-values from plots alone. |
| Threats and alternatives | Reported limitations plus our construct/internal/external/statistical critique. Identify selection, leakage, pseudo-replication, confounded interventions, unsupported equivalence and resource accounting. |
| Implications for ALF | What is supported, not identified, contradicted or unresolved; what transfers, what does not; the exact proposal sentence, control, outcome, workload or authority implication to revise. |

For conceptual/formal papers such as ALMA, adapt the empirical rows: reconstruct definitions, assumptions, logical chain, scenarios/case evidence, counterexamples and validation scope. Do not invent a sample size or effect estimate because the template has a results field.

Inspect the authors' released protocol, prompts, evaluator/configuration and analysis artifacts read-only when needed to disambiguate a method. Record repository commit/file locators, licensing and discrepancies between paper and code. Do not execute untrusted code or launch its model-backed reproduction by default. A source-bound discrepancy is a finding to resolve, not permission to choose whichever account best favors ALF.

## 6. Cross-paper synthesis and actual plan changes

After Batch A, checkpoint the nearest-method comparison. After Batch B, complete one synthesis under `docs/literature/full-reading/synthesis.md`, with:

1. **Evidence matrix:** maintained-program organization, language, predecessor correctness, inheritance/reset, feedback, memory, task exposure, oracle, outcomes and independent units for each study. Explicitly show when two named conditions also differ in authority or information.
2. **Claim audit:** each consequential claim in the current proposal and earlier source audits maps to a full-paper finding and status: retained, narrowed, corrected/withdrawn, or unresolved. Preserve old notes; write visible corrections instead of retroactively upgrading partial readings.
3. **Method reconstruction:** a minimally implementable description of the relevant predecessor/memory/feedback controls and scoring rules, noting every unreported parameter. Distinguish reuse from genuinely new method. No new runner is built in this assignment.
4. **Implication map:** useful current diagnostics versus resolved history; source density versus architectural locality; inherited defects versus latent maintainability; policy outcome versus general architecture effect. Reconstruct support and counterevidence rather than force consensus across different tasks/models.
5. **Decision:** retain the bounded architecture case, narrow/reframe it, replicate/adapt an existing design, or stop that direction. State the practical decision served, strongest rival, observation that would falsify the claim, remaining evidence gaps and smallest informative next test.

Concrete decision rules:

| Full-paper finding | Required action |
| --- | --- |
| A closest paper already covers the claimed gap/control | Remove the novelty claim. Specify replication, a substantive distinct estimand or an explicitly justified extension; do not rescue novelty by naming Nu. |
| Predecessor filtering or feedback policies invalidate an earlier comparison | Correct the synthesis and proposed control before freezing. Preserve the old experiments under their original interpretation. |
| Useful type diagnostics help, but historical masking has different effects | Separate information content from history exposure; revise or defer the repair-insulation proposal. Do not conclude either all feedback is noise or all masking helps. |
| Runtime/scoring relies on a weak judge, unavailable fixture or incomparable API | Tighten the A0 oracle/credibility requirement or choose a different case; do not treat the paper's acceptance as validation of our oracle. |
| The reference-control or case-selection method is feasible and fits the target claim | Reuse it with its assumptions stated. Recalculate the sample/resource proposal rather than silently add conditions. |
| Reading leaves an essential claim unresolved | Mark the claim unresolved and identify the exact missing source/data or decision. Do not begin construction on a positive inference from absence. |

Based on that synthesis, edit the active standalone proposal, PLAN and AGENTS consistently; update the research-loop procedure or metrics/design notes only when a concrete correction requires it. Commit the changes directly without a PR. Do not automatically implement A0, start the 192+5 proposal, switch backend/model, or expand into subagents/H after finishing the reading.

## 7. Scite's role during the assignment

Use exact DOI/title lookups to verify metadata, edition lineages, notices and acquisition routes. Use body search to locate passages, not to substitute snippets for the PDF. Page `read_fulltext` by actual returned characters and search results by effective page size; inspect `source`, `contentDenied` and `hasMore`.

Use backward/forward citation checks only for a close unresolved control or claim uncovered while reading. Record graph seeds/direction/coverage/truncation and exact context. Low coverage is not lack of related work; a supporting label is not proof of our hypothesis. Keep new leads decision-linked and separately staged.

At a completed synthesis or interrupted handoff, record the actual considered source decisions once with a new answer/review ID using `report_citations`, then inspect `citation_report`. Retain full-read status independently of the binary cited/excluded field. A fully read paper may be uncredited; an abstract-only paper may be credited narrowly but is not fully read. Acquisition-pending, conditional and inaccessible papers are not scientific exclusions. Do not relabel the earlier 60-source audit as this full-reading pass or claim PRISMA completeness from the service report.

## 8. Checkpoints, completion and return

Use `docs/literature/full-reading/INDEX.md` as the single live progress/asset index once reading starts. Include each core ID, DOI, chosen version, actual asset reference/hash, access/coverage/reconstruction status, note path, last verified page and next action. Do not mark everything complete in advance. The current setup commit only defines this assignment.

After each paper, save its note and progress. After a batch, reconcile cross-paper contradictions and checkpoint the document changes. This does not require returning to Chat after every paper. Continue the bounded accessible core and synthesis unless a material access/tool/permission issue or a decisive scope change requires a handoff. No extra model workers are implicitly authorized.

A completed handoff contains all eleven core reconstruction records, or an explicitly incomplete/access-blocked list; the cross-paper evidence/claim matrix; corrected current proposal/plan; actual source-decision report; exact commit and relevant CI status; and one concrete next decision. Conditional readings are promoted or explicitly deferred with their trigger. Full reading is not automatically full reproducibility or a systematic-review certificate.

If quota/context/tool limits interrupt the work, first commit the partial records when writing still works. Record exact completed DOI/version/page coverage, unresolved extraction and the next PDF/page. Do not fill gaps from memory or label the batch complete. Report the saved commit and request a continuation prompt when additional tool quota is required; do not promise background completion or repeat finished reading without cause.

**Return after the evidence-driven revision for human disposition.** A0 may then be proposed, narrowed or rejected. Nothing in this reading handoff allocates experimental generations.

## Setup verification scope

The setup pass checked the existing repository handoff, prior reading extents and DOI identities. Primary arXiv landing/version pages were checked for the nine core arXiv works; scite exact metadata lookups covered the remaining core identities and four conditional leads. This was metadata and reading-queue preparation, not fresh full-PDF reading. Preserve those distinctions in subsequent reports.
