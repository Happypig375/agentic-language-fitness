# Wider background search and decision ledger

**2026-09-30 HKT. In progress.** This ledger extends the [survey map](nu-background-survey-2026-09-30.md), preserving the earlier [source audit](nu-literature-sources-2026-09-29.md) as history. Raw service responses and lawful local extracts are retained in ignored `.artifacts/nu-background-20260930/`; retrieved bodies are not committed.

## Retrieval

| ID | Service / exact query | Request / actual return | Coverage and next action |
| --- | --- | --- | --- |
| C01 | Native Consensus: `Functional programming immutable state game engine software architecture maintenance` | `page_size=100`, `page=1`; 100 records | All titles inspected; abstracts and editions being screened. Relevant late-ranked Casanova and maintainability leads show that the old twenty-result prefix was insufficient for this query. Further page/reformulation pending; 100 is not a service-total or field-total claim. |
| C02 | Native Consensus: `Algebraic data types exhaustive pattern matching software evolution maintenance` | `page_size=100`, `page=1`; 99 records | All titles inspected; extensibility, partial-but-sufficient matches, schema evolution and pattern-coverage leads retained for primary checks. Fewer than 100 does not prove exhaustion. |
| C01 p2 | Same exact C01 query | `page_size=100`, `page=2`; 99 records | All titles inspected; no exact URL repeat against its first page. Work/edition relationships remain to resolve. Page 3 or reformulation remains open. |
| C02 p2 | Same exact C02 query | `page_size=100`, `page=2`; 100 records | All titles inspected; no exact URL repeat against its first page. Page 3 and focused type/evolution reformulations remain open. |
| C03 | Native Consensus: `persistent immutable data structures memory allocation garbage collection game performance` | `page_size=100`, `page=1`; 99 records | All titles inspected; selected index text screened below. Persistent nonvolatile memory produces substantial noise; functional persistence/locality/GC reformulations and continuation remain open. |
| C04 | Native Consensus: `software modularity coupling change propagation maintenance empirical study` | `page_size=100`, `page=1`; 100 records | All titles inspected; selected index text screened below. Prospective metrics, actual edit footprint, co-change and effort are different variables; primary methods and continuation remain open. |
| C05 | Native Consensus: `large language models code generation static types functional programming software evolution` | `page_size=100`, `page=1`; 100 records | All titles inspected; selected index text screened below. Type-feedback, typed repair and functional-language lineages retained. Further pages/reformulation remain open. |
| X01 | Paper-search skill: `static typing software maintenance` | 1970–2026, requested ten per source; arXiv 10, Crossref 10, four other connectors failed; 20 unique records reported | Cross-index recall check, not the broad survey boundary. Abstract screen and full report pending. No score threshold. Unexamined source continuations remain. |

Native Consensus supplied numbered records with abstracts and exact paper URLs. Its return is an index representation, not proof of metadata correctness or primary full-text coverage. Consequential findings will be checked at primary sources. The initial responses contain no sign-up/upgrade/usage-counter message. Distinguish native Consensus from the older app connector, whose results require a separate fetch before citation.

The seven native pages above total **697 retrieved occurrences**, not 697 independent works or full readings. Every title was inspected. The following supplied abstracts/index texts were also consumed: C01 p1 positions **1, 2, 10, 11, 16, 19, 20, 26, 29, 37, 40, 42**; C01 p2 **12, 13, 20, 23, 25, 36, 43, 62, 67, 72, 77, 99**; C03 **5, 9, 10, 18, 19, 32, 54, 57, 63, 74, 95, 97**; C04 **2, 13, 19, 32, 46, 59, 67, 75, 86, 90, 97**; C05 **4, 6, 46, 57, 90, 98**. No completed abstract-screen set is claimed for C02. Remaining abstracts are unexamined, not excluded.

C01 p1 position 99 has a mismatched anaesthesia-editorial DOI and functional-programming text; no claim is credited to that identity. C03 includes durable nonvolatile-memory studies whose meaning of persistence differs from versioned functional structures, and a title collision between introductory material and Okasaki's book. C04 surfaces contrary/null interpretations of high coupling and metric-based maintainability. The two Yamashita 2013 records (`10.1007/s10664-013-9250-3`, `10.1016/j.infsof.2013.08.002`) may share their six-developer/four-system dataset; the Oliva 2015 paper and later thesis may also overlap. Those are lineage checks, not independent replications. Arisholm's actual-change weighting (`10.1016/j.infsof.2006.01.002`) must not be imported as a decision-time variable. These are primary-reading leads, not borrowed effect estimates.

## Scite retrieval and citation follow-up

Every literature call used **`limit: 20`**, including exact-identity queries that had fewer matches. No date, citation or venue filters were added.

| ID | Exact query / parameters | Actual records | Coverage / continuation |
| --- | --- | --- | --- |
| SC01 | `"Casanova" AND (game OR games)`, offset 0 | 20; reported total 5,972 | Noisy author/name results motivated the title-field reformulation. An unsaved repeat is not another completed screen. Remaining range not exhausted. |
| SC02 | title parameter `Casanova`, offset 0 | 20; reported total 1,314 | Broad name noise; reformulated with explicit title-field syntax. Remaining range not exhausted. |
| SC03 | `title:Casanova AND (game OR compiler OR encapsulation OR coroutine)`, offsets 0 and 20 | 20 and 12; reported total 32 | All 32 titles inspected. The second page's twelve records were outside the game DSL. This query's reported range is covered; it does not exhaust game-language prior art. |
| SC04 | Exact DOI list: `10.1145/3427763.3428312`, `10.1007/s10664-013-9289-1`, `10.1145/1140335.1140352`, `10.1145/2784731.2784748` | 4 | Identities checked. The GADT record points to a new edition (`10.1145/2858949.2784748`); this is not a retraction or independent replication. Bodies other than S71 remain uncredited here. |
| G01 | S71 incoming citation graph, depth 1, maximum 20 edges, snippets enabled | 6 edges, 7 nodes; not truncated; no low-coverage flag | Edges point from citing source to cited target. The resolved neighborhood is not complete field coverage. Full primary follow-up remains open below. |
| SC05 | Exact six G01 neighbor DOIs plus `10.1145/3485532` and `10.1145/3411763.3451515` | 8 | All metadata/context results inspected. S72/S73 promoted; their full readings remain pending. Proceedings metadata and irrelevant circuit evidence are separated in S71's note. |

G01's neighbor identities are `10.1145/3486605.3486787` (Trampoline variables), `10.1145/3828690` (Citrus), `10.1145/3638380.3638395` (creative practices), `10.1145/3638380` (proceedings-level record with a mismatched access link), `10.22152/programming-journal.org/2025/9/2` (S73) and `10.1145/3746059.3747646` (Denicek). Trampoline variables, creative practice and Denicek remain relevant unexamined methods. Citrus concerns superconducting circuitry and is not credited for interactive-software maintenance. S73's characterization of state migration must be checked against S71's actual type-changing construction. S72's 2021 OOPSLA paper and earlier CHI abstract require lineage reconciliation, not two independent sample counts.

## Primary acquisition and actual reading

Stable IDs S68–S71 were assigned after checking existing Zotero DOI/title identities. Native API import and readback preserved the earlier **86 parents and 93 PDF hashes** while adding four parents and three PDFs. The user then supplied S69/S70 attachments, giving **90 parents = 87 literature works + three public-source records, and 98 PDF attachments**, verified on 2026-09-30. Seven topic subcollections remain. Renaming the root collection/tags preserved keys, bibliographic fields and memberships. The root is `PKLXQNEE`, named **ISE - Nu Innovation Research (2026-09-15)**. Acquisition, full reading and reproduction remain separate.

| ID / DOI | Parent / attachment | Edition and actual state | Live claim / next action |
| --- | --- | --- | --- |
| S68 / `10.1145/3412843` | `DD3VVL3D` / `973Z9SVH` | [CWI author preprint](https://ir.cwi.nl/pub/30601/30601.pdf), 102 pages; only pp. 1–8 text consumed | Game-language alternatives and survey recall. Read remaining taxonomy/methods and catalog; reconcile the 37-page publication metadata with this longer author file. |
| S69 / `10.1145/2305484.2305533` | `GFRLS35S` / user attachment `UTSHL7TK` | Six-page user PDF, title verified. Separate [CiteSeer copy](https://citeseerx.ist.psu.edu/document?doi=2b0ab16b01c3b8ebe0e3f4f966890dcf7476edae&repid=rep1&type=pdf): all six pages of text consumed; rendered pp. 3 and 6 inspected, pp. 2/4/5 and edition comparison pending | Shared-world snapshot/rules/coroutine predecessor and performance denominators. Partial, not included in the complete count. Earlier author URL 404 is historical access information. |
| S70 / `10.1016/j.entcom.2017.03.001` | `M256NA5R` / user attachment `R2A6BM28` | Seventeen-page user PDF, title verified; body unread | Encapsulation, scheduling and networking/runtime tradeoffs. The earlier IRIS 403 access gap is closed; full methods are queued. |
| S71 / `10.1145/3427763.3428312` | `WTCS6U8P` / main `2SE6UYG6`, appendix `K5VAA3KX`; note `EAZ27AU9` | [Author paper](https://www.manuelbaerenz.de/essence-of-live-coding/EssenceOfLiveCoding.pdf), all 13 pages; [author appendix](https://www.manuelbaerenz.de/essence-of-live-coding/EssenceOfLiveCodingAppendix.pdf), all four pages; complete relevant visuals/definitions/references | [Complete reading](full-reading/S71-live-state-migration.md): generic migration preserves required types, not arbitrary application invariants. Finite-exception/higher-order-state, clocks/effects and cost limits remain; no artifact execution. |
| S72 / `10.1145/3485532` | No existing DOI/title match; locally acquired, not yet imported | [Author OOPSLA paper](https://jlubin.net/assets/oopsla21.pdf), 30 pages; abstract consumed, body pending | Actual functional-programming workflow, type feedback and authoring. Compare the earlier CHI abstract before treating its sessions/interviews as independent. |
| S73 / `10.22152/programming-journal.org/2025/9/2` | No existing DOI/title match; locally acquired, not yet imported | [Author schema-evolution paper](https://tomasp.net/academic/papers/schema/paper.pdf), 34 pages; opening pp. 1–4 consumed, p. 5 partial, remainder pending | Code/data/schema migration dimensions and S71 citation accuracy. Article dated 2024-10-15 in the 2025 volume; retain both dates. |

| Local lawful asset | Bytes | SHA-256 |
| --- | ---: | --- |
| S68 author preprint | 9,670,399 | `154d88b68b64053e3d3b7b457d338b28d804180d827acb7dad1c7a50cf50208e` |
| S69 user PDF | 499,164 | `4edc92bc68d610e81ae3aebbc5b7e99ddc44a494fef6ffd196e0b60120e57da3` |
| S69 CiteSeer copy | 325,228 | `1da9812bbac49fcd18c9343514bb83ce41d9baebfece58629bf39776825faedb` |
| S70 user PDF | 2,051,278 | `a1b4a6ac47014fcde102553ef27682fe42cfe9a120a3e37a5e37548e64cb224d` |
| S71 main | 487,824 | `a6332c5f19c4566c0e457cc99424097471aed18080dfb17ebcc7618f9ffc2e54` |
| S71 appendix | 399,558 | `34004622b8d4f95d16370e39583990b615e61a3b146d43432aa43f597d00d8dc` |
| S72 author PDF | 853,504 | `f047c0a15757eb982e72f49308246de8246f059bb513dd8cd4c101624e0c59ba` |
| S73 author PDF | 1,401,364 | `c164aa76ab4ac142338435bc85c22335aad52edff645653be87ca8fdf766a4e3` |

The live complete-reading count is **63 = thirteen P + three A + forty-seven S**. The preceding 62-work assessment remains a dated decision-specific snapshot. S68–S70 and S72/S73 are not silently counted. No publisher PDFs, extracted bodies or private transcripts are committed. The next work is primary reading and consequential search/citation follow-up across the open survey themes, with experimental allocation still zero.

## Cross-index connector errors

The successful services remain usable. These errors bound X01 coverage and are preserved verbatim; no OAuth, paid service or dependency installation was attempted to work around them.

```text
[dblp] Error on query 'static typing software maintenance': Expecting value: line 1 column 1 (char 0)
[open_alex] Error on query 'static typing software maintenance': 401 Client Error: Unauthorized for url: https://api.openalex.org/works?search.semantic=static+typing+software+maintenance&filter=publication_year%3A1970-2026&sort=relevance_score%3Adesc&page=1&per-page=10
[openreview] Error on query 'static typing software maintenance': openreview not installed. pip install openreview-py
[semantic_scholar] Error on query 'static typing software maintenance': 403 Client Error: Forbidden for url: https://api.semanticscholar.org/graph/v1/paper/search?query=static+typing+software+maintenance&offset=0&limit=10&fields=title%2Cauthors%2Cyear%2Cabstract%2CcitationCount%2Curl%2Cvenue%2CpublicationDate%2CexternalIds&year=1970-2026
```

## Audit status

The completed S71 reading and its direct citation/type-authoring follow-up set were submitted once as `nu_background_s71_20260930`. Scite accepted **two credited source identities and eight not-credited identities, zero skipped**. The two credited identities are one work and its author appendix. Six relevant leads remain deferred (mapped to `excluded/out_of_scope` because the tool has no deferred status), one circuit paper is off-topic and one proceedings record is not an independent study. S73's `full_text` stage explicitly means only its opening pages were read.

The inspected `citation_report` showed ten considered identities, no missing reasons, no retrieval-link warning and no truncation; answer-scoped retrieved count was null. This audit covers that completed segment, not all 697 native Consensus occurrences, unfinished Casanova readings or unchanged historical decisions. Other considered sets remain in progress. The tool's screening terminology does not certify systematic-review completeness.
