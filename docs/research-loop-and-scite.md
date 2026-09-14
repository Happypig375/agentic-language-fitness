# Research loop and scite procedure

**2026-09-14 — current maintainer method.** Read with [PLAN.md](../PLAN.md). This is a decision procedure, not a claim that every past search was systematic, and not permission to launch experiments or paid review agents.

## 1. Two loops, with a decision at the end

The **research-positioning loop** is:

```text
question and intended decision
  -> closest competing methods and explanations
  -> primary-source assessment, including contrary evidence
  -> claim/estimand correction
  -> minimum discriminating design or explicit unresolved blocker
  -> record the decision and stop this pass
```

The **experimental loop** begins only after its own authorization: freeze the question, treatment, information, oracle, units and limits; execute the specified check; audit; interpret against the prespecified alternatives; decide whether to replicate, change the question or stop. Outcome-driven changes belong to a new documented decision, never an invisible amendment of old results.

Reading, retrieving, reviewing, constructing and running are different activities. A larger bibliography, a new design document or a more elaborate harness is not progress unless it changes what can be claimed or decided. Conversely, an unassessed close predecessor cannot be ignored because reading it might remove the proposed novelty.

## 2. Start each literature pass with a short decision card

Record in the focused source ledger, not another sprawling framework:

- the exact claim or methodological choice under review;
- what evidence would support, weaken or redirect it;
- the populations, interventions and outcomes that count as close work;
- known relevant papers that a reasonable search should recover;
- sources, terms, editions and boundaries planned for this pass;
- the stopping/deferral rule and the decision needed at handoff.

For this project, distinguish the architecture of the **software being maintained**, the **model**, and the **agent harness**. Search terms such as architecture, memory, agents and alternatives occur in many unrelated fields. Inspect retrieved records; a Boolean-looking query is not proof the service interpreted it as intended.

## 3. Discover with scite; do not mistake retrieval for assessment

Use exact DOIs for known papers. Validate title, authors, edition and publication venue against a primary source when an identity matters. Normalize DOI case for deduplication, but keep preprint versions and publication lineages explicit. A journal DOI, arXiv DOI and repository deposit can describe one work. A generic January 1 date in an index is not the actual release date.

For discovery, use technical synonyms and modest pages. Record exact queries, effective limits, offsets, returned counts and reported totals. If a request for 25 returns an effective page of 20, continue at 20, not 25. Deduplicate records across overlapping ranked pages. A reported total is not the count of relevant studies.

Do not stop at the first five records. Neither does a proper review require reading thousands of irrelevant results end to end: reformulate a noisy query, use a known-relevant start set and citation links, and disclose unexamined ranges. Excluding an unrelated title is different from excluding a relevant study after reading its methods.

Search results contain metadata, often truncated abstracts, selected excerpts and citation statements. None establishes that a full paper was read. Record the actual assessment stage. Do not infer result strength from a title, a citation tally, access flags or a secondary site's summary.

## 4. Read decision-critical primary methods and limitations

With `read_fulltext`, check the returned `source`, `contentDenied`, `returnedChars`, `totalChars` and `hasMore`. `source: abstract` is not body access. Page by the returned character count when continued reading is needed. Offsets are session-dependent; persist stable edition/section descriptions, not offsets alone as permanent locators.

A readable response must match the intended DOI/title/version. Misassociated body text is unusable until resolved. Empty full text is an access/indexing failure, not evidence that the study is weak or irrelevant. Follow primary publisher, author, institutional or versioned preprint routes; document denials and the actual fallback used. Read figures/tables from the original page when their contents matter rather than trusting scrambled extraction.

For a close experiment, extract at least:

| Field | Why it matters |
| --- | --- |
| Assigned intervention and comparator | Is it code quality, architecture, predecessor authorship, model capability or harness policy? |
| Starting-state correctness and filtering | Does the study compare working predecessors or carry broken ones forward? |
| Task sampling and reference construction | What population or deliberate stress scenario is represented? |
| Information, tools, feedback and memory | Are later agents seeing tests, diagnostics, summaries or hidden prior context? |
| Outcome and oracle | Behavior, structural compliance, human judgement, LLM rating, cost or a mixture? |
| Independent unit and uncertainty | Repeated runs are not new projects or task families. |
| Limitations and counterevidence | Which claim would exceed the tested scope? |
| Consequence for ALF | What specific sentence, measurement or design choice changes? |

Keep quotations minimal. The ledger should contain our concise interpretation and precise locators, not copies of copyrighted bodies. Abstract-only evidence can motivate a lead but cannot justify a detailed claim that its methods definitely omit our proposed outcome.

## 5. Snowball with explicit coverage checks

Start from several relevant communities, not one favorable paper. `citation_graph` edges run from citing source `s` to cited target `t`. Incoming edges find follow-ons; outgoing edges find foundations. Record seeds, direction, depth, cap, automatic edition expansion, `seed_coverage`, `low_coverage_seeds` and `truncated`.

A zero-edge arXiv graph can reflect DOI/index coverage. A capped graph can miss relevant edges even when a seed has many citations. Neither establishes absence of follow-on work. Fall back to the primary bibliography and independent keyword/index searches where the decision requires it.

Smart-citation labels are discovery aids, not votes on our hypothesis. Inspect the actual citing passage and its context. A supporting statement about a search procedure does not support an architecture-maintenance claim. Labels such as uses baseline, reuses data, critiques an assumption or motivates a question should be our text-grounded interpretation, not an invented service classification.

Do not expand every retrieved bibliography recursively. Follow links that can change the current decision, retain a queue of relevant unassessed leads, and distinguish this bounded practice from a fully specified systematic database-plus-snowballing review.

## 6. Finish the evidence-to-design loop

For consequential claims retain:

```text
claim / question
source identity + inspected edition/sections
what the study actually establishes
limitations / unresolved access / competing explanation
design consequence and decision owner
```

Use separate statuses: credited for a stated claim; screened out with reason; relevant but deferred; access-limited; duplicate edition; metadata mismatch. A deferred source is not a rejected scientific result. Preserve null/adverse evidence and previous wrong interpretations with a visible correction rather than silently cleaning the history.

At the end, call `report_citations` once with the actual credited and not-credited sources, provenance and reasons; inspect `citation_report` for missing reasons or rejected entries. Its binary cited/excluded record is an answer-provenance log. Use explanatory reasons for deferred records and retain the richer ledger statuses. A generated funnel does not certify PRISMA completeness, systematic-review quality, full-paper coverage or novelty.

When formatting a bibliography, use retrieved metadata and check ambiguous identities; do not assume automated formatting repairs an incorrect underlying record. Linked preprint/published versions are not independent replications.

## 7. Stop based on the decision, not a citation quota

A bounded critical review may conclude that the proposal is ready for a **small feasibility decision**, while its novelty assessment remains provisional. State which search ranges or relevant methods remain unassessed. Before a strong publication novelty claim, complete a separately defined search scope and its backward/forward assessment; a top-N cutoff is not saturation.

Return immediately when a close predecessor changes the gap, a required source cannot be assessed, a proposed experiment cannot distinguish the leading alternatives, or new scientific authority is needed. Stop the pass once its reviewed decision and unresolved queue are recorded. Repeatedly adding adjacent citations without changing the design should not delay a justified model-free feasibility decision.

No new experiment is automatically justified by finding a gap. High research value requires an informative question, credible contrast, valid observable outcome and feasible design. It cannot be guaranteed by literature volume or by choosing an unstudied named technology.

## Methodological grounding and limits

Wohlin, Kalinowski and Felizardo, [10.1016/j.infsof.2022.106908](https://doi.org/10.1016/j.infsof.2022.106908), distinguish a planned hybrid search from ad hoc complementary searches and discuss retaining borderline decisions. This pass read the introduction/search-strategy discussion, not the entire study through scite. The older [search-depth audit](literature-search-depth-audit-2026-09-14.md) records the project's demonstrated first-five failure and prior assessment of snowballing guidance. These sources motivate the procedure; they do not certify its completion here.
