# Research loop and scite procedure

**Updated 2026-09-14.** This is a working procedure, not a claim that every previous review completed a systematic search. Follow [PLAN.md](../PLAN.md) for the current decision and authority. A search, citation report, review or local freeze does not authorize an experiment.

## 1. Begin with the decision, not a bibliography target

Write a short decision card: question; target population or case; proposed treatment and outcome; strongest rival explanation; what evidence could overturn the interpretation; inclusion boundary; and the smallest next action the review can justify. Distinguish maintained-program architecture from neural-model, agent-harness and deployment architecture.

The loop is:

```text
question and falsifier
  -> closest methods and contrary evidence
  -> explicit change to claim/control/measurement
  -> smallest informative feasibility check
  -> evidence and proceed/narrow/redirect decision
```

A new paper or workstream name is not progress unless it changes one of those decisions. Maintain a decision-linked deferred queue instead of trying to read every adjacent topic before doing a bounded feasibility check.

## 2. Retrieve close known methods before broad discovery

Use exact DOI/title lookups for known close predecessors, checking title, authors, edition and primary provenance. Then use targeted keyword searches, relevant bibliographies and citation graphs. A known close work missing from the first keyword page is a recall warning, not proof it is irrelevant. Query terms such as architecture and maintenance attract other domains; screen their actual target variables.

Record exact query, filters, sort order, requested/effective limit, offset, returned count and reported total. Advance by the effective page size, not a requested size that the service reduced. Keep unexamined ranges explicit. Exhausting a narrow query is not saturation of a field; examining 20 or 40 of a broad query is not a full screen. Reformulation after noisy output is legitimate, but record it.

Separate retrieval positions, literal identifiers, work/version lineages, screened abstracts and bodies actually read. Related arXiv/conference/journal identifiers may name one work. Matching titles are a lead, not proof of identity. Do not double-count versions or duplicate posts as independent replications.

## 3. Read and verify what supports the design

Inspect decision-critical methods, inputs, treatment assignment, feedback, starting-state filters, oracle, units, exclusions and limitations. Abstracts are useful for screening; they rarely establish what a study did not test. Create a claim -> source/version/section -> limitation -> design consequence row.

For `read_fulltext`, inspect `source`, `contentDenied`, returned characters, offset, total and `hasMore`. A readable/OA metadata flag does not prove a body was returned. A fallback abstract or a few excerpts are not a whole-paper review. A character range in scite's extracted text is not automatically a page/section range in the publisher edition.

Confirm DOI/title and the primary edition before using results. For an updated preprint, do not mix old sample counts or conclusions with new methods. If the indexed body has no version identity, use it for discovery and verify consequential claims against a pinned primary edition. Record the edition originally read and the one that governs the final claim.

If scite cannot supply a body, follow an authorized primary publisher, author or preprint route. Record the actual extent read and remaining access limits. Do not treat an inaccessible close predecessor as scientifically excluded; retain it as access-limited/deferred. Do not use generated overviews or vendor summaries as substitutes for a study's methods.

When analyzing a PDF, inspect the relevant rendered pages as well as parsed text when layout, tables or diagrams matter. Do not claim an entire-paper or figure review from one screenshot.

## 4. Use citation contexts as evidence, not votes

For `citation_graph`, `s` is the citing source and `t` the cited target. Record seeds, direction, depth, edge cap, returned nodes/edges, truncation, per-seed coverage and low-coverage flags. Zero incoming edges on a low-coverage preprint say nothing reliable about absence of follow-on work.

A paragraph with several citations may return an edge to one reference while mentioning several other studies. Resolve the title/DOI explicitly rather than assume the closest phrase identifies that edge. Read the citing paragraph/section when needed to classify whether it uses a baseline, extends a method, disputes a claim or merely supplies background. Supporting/contrasting/mentioning labels guide discovery; none is a vote proving our hypothesis.

Graph-discovered nodes are leads until read. Follow the nodes that could change the present decision and defer others with a reason. A graph cap or quota limit is a resource boundary, not saturation.

## 5. Preserve opposing mechanisms and genuine uncertainty

Seek a credible result against the preferred explanation. In this project, useful current compiler diagnostics must be distinguished from resolved history, redundant warnings and stale source. Source compactness, code organization, retrieval and hidden model reasoning are different variables. A paper about pruning old observations does not show that less information about the active error helps.

Compare treatments at the level of actual authority, initial state and feedback, not their names. A fresh-conversation experiment can still carry notes; a no-repair experiment is not a delegated-repair intervention. A clean-predecessor contrast already existing elsewhere is a reusable method, not our novelty.

If stronger claims need a missing control, require that control or narrow the claim before the run. Do not increase the apparatus until every imaginable confound is eliminated. State which uncertainty the next bounded experiment can actually resolve.

## 6. Record source decisions once, then verify

Maintain richer repository statuses:

- **C — credited:** used for a specific bounded claim/design consequence, with actual reading extent;
- **D — deferred/access-limited:** relevant or potentially relevant but not resolved in this pass;
- **N — not used for this question:** actual scope mismatch, with reason;
- edition/duplicate relationship as a separate identity field where verified.

Near completion, call `report_citations` once for the full considered set, not only the papers cited in prose. Use DOI identities when available and record actual provenance, stage and reason. If the service exposes only `cited`/`excluded`, map D to excluded/not-credited with an explicit deferral reason; do not present it as merit rejection. Stage `full_text` must still state whether only selected methods were read.

Then inspect `citation_report` for accepted counts, skipped/malformed records, missing reasons, truncation and linkage warnings. The answer-scoped retrieved count may be null. Service-generated screening language is an audit convenience, not a PRISMA certification, comprehensive field review or proof of novelty. Keep the search-range and work/version ledger in the repository even when the service accepts all decisions.

## 7. End with a decision and an executable boundary

The review should state: which prior method is closest; what changed in the design; what observation would now challenge it; which evidence is deferred; why the next feasibility check is worth doing; and what is not authorized. Record reviewer identity/type and independence honestly. A second AI session is not a human expert.

Do not write a new proposal just because more papers were found. Revise the active proposal and PLAN consistently; preserve earlier reports and frozen protocols. Stop the literature pass when the bounded decision is supported, unless a newly found close source could overturn it. Reopen the relevant search before a stronger novelty or publication claim, not before every routine engineering fix.

## Worked audit for the current review

The [2026-09-14 design-discrimination audit](pro-review-design-discrimination-sources-2026-09-14.md) demonstrates these distinctions: effective pagination, known close methods recovered outside the keyword prefix, latest-edition checks, useful-diagnostic counterevidence, a corrected title/DOI lookup, low-coverage incoming graphs, and the full 60-identifier decision record. Those 60 identifiers are not 60 papers read or 60 independent studies.
