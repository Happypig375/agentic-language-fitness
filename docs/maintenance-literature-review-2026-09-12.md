# Maintenance/context literature scoping ledger

**Date:** 2026-09-12 HKT

**Status:** selected-methods review; not systematic, exhaustive, or proof that
F# wins

## Retrieval record

Connected Scite search_literature/read_fulltext tools were used. An initial
claim that the plugin-management guide was unavailable resulted from checking
a stale version path. The current catalog guide was subsequently read; it
directs use of an already connected integration when suitable. This access-note
correction does not change the retrieved evidence. No installation or permission
change was needed. Search used default relevance, limit 5, offset 0 and no date
filters:

- Q1, "cognitive dimensions" AND (programming OR notation) — backend total
  15,371.
- Q2, ("software evolution" OR "software maintenance") AND ("large language
  models" OR "coding agents") — total 540.
- Q3, architecture AND modularity AND ("maintenance" OR "change propagation")
  — total 80,941.
- Q4, ("F#" OR "F sharp" OR FSharp) AND ("C#" OR "C sharp" OR CSharp) AND
  (maintenance OR architecture OR comprehension) — total 4,630,207; returned
  irrelevant music/chemistry hits.
- Q5, FSharp AND CSharp AND software — total 5; no direct controlled
  comparison appeared among selected metadata.

Counts are backend-reported retrieval totals, not deduplicated or relevant
paper counts. Q4/Q5 do not show that relevant work does not exist. Earlier Q0
results are recorded in [the research-direction note](research-direction-2026-09-12.md).

## Source findings

### R1 — Berger et al. (2019)

[On the Impact of Programming Languages on Code Quality](https://doi.org/10.1145/3340571).
Scite fulltext selected portions read: introduction, methods, repetition,
reanalysis and BEST PRACTICES. The authors reanalyze observational GitHub language-quality
claims, expose classification/data/model problems, and caution against weak
causal interpretation; no independent-new-data reproduction was completed.
BEST PRACTICES emphasizes automation, documentation, sharing, validated labels
and domain experts.

**Proposed implication:** use paired task contracts and qualified reviewers;
avoid language-wide claims and bug-keyword counts. This is methodological
caution, not evidence that languages are equal.

### R2 — ChainSWE (2026)

[Primary v2](https://arxiv.org/html/2607.02606v2), DOI
[10.48550/arXiv.2607.02606](https://doi.org/10.48550/arXiv.2607.02606).
Scite fulltext selected portions read: introduction, dataset construction,
evaluation modes/settings/metrics and initial results. Primary v2 (2026-09-01)
methods, especially §§3.2–3.4 and §§4.3–4.5, confirm an
overlap filter, Qwen3.7-Max solvability selection, a persistent repository with
a fresh conversation (SEQ), and a separately retained transcript (SEQ+MEM).
The benchmark has chronological overlapping bug chains: 100 chains, 304 bugs
and 54 Python repositories. The solvability screen is not imported here.
Execution and success-prefix scoring are distinct. Fresh chat plus persisted
code is precedent, not our novelty. Gold-overlap mining does not justify
scoring arbitrary correct designs by gold-patch footprint.

**Proposed implication:** use primary v2 methods only; do not map indexed
revision performance figures onto v2 or quote percentages here.

### R3 — SWE-EVO (2026)

[Primary v6](https://arxiv.org/html/2512.18470v6), DOI
[10.48550/arXiv.2512.18470](https://doi.org/10.48550/arXiv.2512.18470).
Scite fulltext selected portions read: benchmark construction, task formulation,
metrics and initial setup. Primary v6 (2026-05-22; first version 2025) methods,
especially §§3.1–3.2, describe 48 release-evolution tasks across
seven mature Python projects: pre-release code plus release requirements,
multi-file modification and prior passing regression tests. V6 specifies one
release transition with final-state evaluation, not a PR-by-PR chain; its
default input includes linked PR/issue text (indexed text had release-note-only
material). This is existing-repository evolution precedent, not a within-agent
chain inheriting prior candidate outputs like ChainSWE. It provides no F#/C# or
controlled context-window effect.

**Proposed implication:** treat v6 methods as authority and keep indexed
revision details separate from current abstract/model/results; do not transfer
headline figures.

### R4 — Cognitive Dimensions of Notations

Green and Petre (1996), DOI
[10.1006/jvlc.1996.0009](https://doi.org/10.1006/jvlc.1996.0009), was not read:
Scite had no source, contentDenied=true and zero characters. The alternative
read was Blackwell et al. (2001), [author copy](https://www.cl.cam.ac.uk/users/afb21/publications/CT2001.pdf),
sections on introduction, framework/dimensions, profiles and operationalization
(PDF pages 1-7 portions). The framework supplies task-sensitive vocabulary
including consistency, viscosity, hidden dependencies, diffuseness and
abstraction. Dimensions are not inherently good or bad; notation and
environment matter. This is a proposed mechanism language, not a validated LLM
cognitive score or F# ranking. The primary author bibliography was also used:
[Cognitive Dimensions bibliography](https://www.cl.cam.ac.uk/~afb21/CognitiveDimensions/CDbibliography.html).
The tutorial was not reviewed.

**Proposed implication:** use dimensions as review prompts or hypotheses, not as
an outcome score or language preference.

### R5 — Exploring the Structure of Complex Software Designs: An Empirical Study of Open Source and Proprietary Code

[Publisher DOI](https://doi.org/10.1287/mnsc.1060.0552). Read only the publisher
abstract and the author working-paper introduction:
[working paper](https://www.hbs.edu/ris/Publication%2520Files/05-016.pdf).
The Linux/Mozilla dependency-structure study and purposeful Mozilla redesign
connect architecture changes with organization/design choices. There is no
measured F#/C# LLM effect, and no basis to equate a dependency metric with
maintenance time. Dependency structure is a possible diagnostic, not a
stand-alone quality score.

**Proposed implication:** consider dependency structure alongside regressions,
missed dependencies and cumulative maintenance cost; do not use it alone.

## Search exclusions and limits

Q1’s top hit concerned talim/weaving. Q3 surfaced industrial asset/product
architecture and other non-execution or indirect material; Q2 surfaced a
bug-severity predictor; these remain leads, not support. Q4/Q5 returned
irrelevant metadata among selected hits, not evidence that every hit was
irrelevant.
One Q1-relevant chapter was not read in full. The selected papers do not provide
direct controlled F#/modern-C# longitudinal context evidence.

Web discovery used the exact queries site.hbs.edu "Exploring the Structure of
Complex Software Designs" and "Green" "Petre" "1996" "Cognitive Dimensions"
pdf. These discovery routes do not change the selected-methods scope.

This is not full-paper reading or a systematic review. Citation labels are not
truth votes. Stable DOI/version links and section locators are used instead of
ephemeral character offsets. No raw full text was copied into the repository.
No model/pilot request, OAuth action, external Scite collection write, private
sibling transcript publication or scientific adoption occurred.

## Design-review relevance

The selected material supports only bounded design investigation: qualified
review, existing-repository evolution, explicit scoring distinctions,
task-sensitive architecture vocabulary and dependency diagnostics. It does not
settle language choice, context-window effects, expertise treatment, causality,
large-project generalization or long-term survival. Larger searches and expert
review remain needed before paper-wide novelty/generalization claims.

Potential follow-up is the proposed
[maintenance-context-design-review-2026-09-12.md](maintenance-context-design-review-2026-09-12.md),
linked to [the research-direction note](research-direction-2026-09-12.md). Its
treatments remain proposals requiring review; existing H execution flags and
allocations are unchanged.
