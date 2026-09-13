# Research-frontier source and search ledger

Companion to the [gap/value assessment](research-frontier-gap-assessment-2026-09-14.md).
Retrieval date: **2026-09-14 HKT**. Inspected repository:
`5f919797f746ba5c87c3eea03a28e1c7109004fb`.

## Scope and source conventions

This is an updated, bounded evidence map for architecture, language support and
inherited LLM maintenance. It is not a systematic review or a novelty certificate.
Primary papers support substantive claims; searches and citation graphs provide
leads. Ranking, author claims of novelty, citation classifications and failure to
retrieve a paper are not evidence of an unoccupied research gap.

The main agent screened records and owns research-design reasoning and final
acceptance. One Luna Max worker independently retrieved the closest inherited
maintenance benchmarks read-only. Worker-only reading is labeled below; it is
not main-agent full-paper reading or human scientific review. No benchmark
model/count calls, credentials, adapter changes or live allocation occurred.

Scite search abstracts were often truncated by the service. A search record is
therefore **title/partial-abstract/excerpt screening**, not a full abstract or
paper read. The original broad tool payloads also exceeded the display budget;
their complete hit metadata was retained in session and re-emitted compactly
for screening. The inventory records the actual papers returned, including
off-topic results. It does not count cited references inside a retrieved paper
as independently inspected papers.

## Main-agent search scope

All F1/F2/F3 keyword requests used `date_from=2024-01-01`,
`date_to=2026-09-14`, relevance order and `limit=20`. These are corpus filters,
not verification of publication dates: arXiv metadata sometimes used January 1
as a year placeholder. Primary submission histories determine the editions below.

| ID | Exact search / selection | Returned / reported total |
| --- | --- | --- |
| F1, F1b, F1c | `("large language models" OR "coding agents" OR "LLM") AND ("software architecture" OR "code modularity" OR "technical debt") AND ("maintenance" OR "refactoring" OR "maintainability")`; offsets 0, 20, 40 | 60 / 954 |
| F2 | `("large language models" OR "LLM") AND ("functional programming" OR "immutability" OR "algebraic data types" OR "modular code") AND ("evaluation" OR "experiment" OR "maintenance")`; offset 0 | 20 / 1,922 |
| F3 | `("coding agents" OR "LLM" OR "large language models") AND ("code structure" OR "code health" OR "architectural design") AND ("effect" OR "causal" OR "editing")`; offset 0 | 20 / 6,180 |
| F4 | Exact DOI lookup: `10.48550/arxiv.2608.18645`, `10.1145/3729274`, `10.1109/ase63991.2025.00117`; limit 10 | 3 / 3 |
| F5 | Exact DOI lookup: `10.1145/3793655.3793722`; limit 2 | 1 / 1 |

The 100 keyword rows contain **97 distinct DOIs**. F1 was extended because
directly relevant findings continued beyond the first page: CodeHealth at rank
27, the agent-versus-human maintenance comparison at 28 and SlopCodeBench at
41. F2/F3 were noisy cross-field queries; they were not treated as reliable
absence tests. The F1 limit of 60 remains a practical scope limit, not a
justified saturation boundary. Unscreened results remain unassessed.

Independent web discovery used these literal queries:

```text
"Statically Contextualizing Large Language Models with Typed Holes"
"F#" "C#" "maintenance" "language models" architecture
"code architecture" "LLM" "controlled" maintenance
"code health" "LLM" refactoring study 2026
"10.1145/3793655.3793722"
```

The August CodeHealth test-generation paper was found through web discovery,
not through the first Scite keyword pages. Primary exact-title/DOI and edition
lookups followed. No inference of absence follows from the sparse F#/C# hits.

## Worker search scope and recovery

The bounded worker made two Scite keyword searches, 15 results each, then primary
edition lookups for the selected benchmarks. W1 used `offset=0`, `limit=15`,
no date/type/journal/publisher/DOI/citation filters, and
`user_intent=frontier_maintenance_benchmarks`. W2's query and 15-row response are
retained; other filter settings were not retained in its handoff and are not
inferred here.

```text
W1:
("long-horizon" OR "software evolution" OR "software maintenance") AND ("coding agent" OR "large language model" OR LLM) AND (benchmark OR dataset OR repository)

W2:
("multi-bug" OR "bug chain" OR "multi-issue" OR "software evolution") AND ("coding agent" OR "large language model" OR LLM) AND (benchmark OR repository OR maintenance)
```

The first W1 display truncated four row identifiers. One exact re-request,
with compact metadata output, recovered all 15. No ranking change was observed
among identifiable original rows; the original hidden ordering cannot be
independently verified. W1 ranks below refer to the complete re-request, not a
claim that the first display contained them. The recovered ranks 6–9 were
title-only screened, not full-paper reads. W2 retained all 15 rows.

These searches have 29 distinct DOIs across 30 ranked positions. Re-requesting
W1 does not add 15 independent records. SlopCodeBench and SWE-CI were known
anchors; SWE-Milestone and CodeThread filled the two new benchmark-method slots.
LoopsBench remains abstract-only. The directly relevant
`10.48550/arxiv.2605.06464` remains a full-methods follow-up, not evidence
silently treated as agreeing with the assessment.

## Citation-neighborhood check

FG: `citation_graph`, incoming, depth 1, maximum 60 edges, intent labels enabled,
snippets disabled; seeds `10.48550/arxiv.2601.02200`, `10.1145/3689728`,
`10.48550/arxiv.2603.27745`. Scite expanded the typed-hole seed to its preprint
`10.48550/arxiv.2409.00921`.

The tool returned 10 edges and 13 listed paper records, although its `node_count`
field said 14. The edge list identifies `10.3390/computers14120534` without a
matching paper-metadata record; the inventory retains that unresolved DOI,
without inventing its title. `truncated=false` does not establish coverage:
all 10 edges resolved to the typed-hole journal DOI.
The CodeHealth and NITR seeds had zero resolved edges and were explicitly marked
low coverage. The independently found August follow-up illustrates why this
cannot be interpreted as having no subsequent work. Two promising typed-hole
citers received F4 metadata lookup; their full methods were not audited here.

## Credited primary works and reading extent

### P1 — NITR

- Haichao Zhu et al., *Needle in the Repo: A Benchmark for Maintainability in
  AI-Generated Repository Edits*.
- DOI [10.48550/arXiv.2603.27745](https://doi.org/10.48550/arXiv.2603.27745).
  [Primary v1](https://arxiv.org/html/2603.27745v1), 29 March 2026; preprint.
- Main read introduction/motivating example, §§3–4, result summaries and §6.2.
  Structural checks, multi-step inheritance, tool restrictions and construct
  limits were verified from the body. No artifact execution or oracle audit.

### P2 — CodeHealth and refactoring

- Markus Borg et al., *Code for Machines, Not Just Humans: Quantifying
  AI-Friendliness with Code Health Metrics*.
- Published DOI [10.1145/3793655.3793722](https://doi.org/10.1145/3793655.3793722),
  FORGE 2026, pp. 51–61; publisher lists 21 July 2026 publication.
- Preprint DOI [10.48550/arXiv.2601.02200](https://doi.org/10.48550/arXiv.2601.02200),
  [v1, 5 January 2026](https://arxiv.org/html/2601.02200v1).
- Main read v1 §§3.1–3.4, Tables 2–3, results and §5.4/conclusion. Publisher
  metadata/abstract and selected indexed body corroborate identity; two later
  publisher body finds failed. Statistical details are bound to the inspected
  v1, not an asserted byte-identical published edition. These are one study,
  not independent replications. Authors' CodeScene affiliations are visible;
  proprietary metric validation is not independently reproduced here.

### P3 — CodeHealth and test generation

- Freya Wirdemann et al., *Code Health in LLM-Based Test Generation:
  Effectiveness and Token Efficiency*.
- DOI [10.48550/arXiv.2608.18645](https://doi.org/10.48550/arXiv.2608.18645),
  [v1, 19 August 2026](https://arxiv.org/html/2608.18645v1). Primary landing
  reports acceptance at the SCAM 2026 Engineering Track; no proceedings DOI
  is asserted.
- Main read §§III–V, Tables II–III and conclusion. Scite `read_fulltext`
  returned no text (`contentDenied=true`); F4 returned metadata only. Primary
  HTML supplied the body. This shares authors and Python data with P2, not a
  fully independent replication. Conditional mutation-score denominators,
  one-model scope and language-dependent adjusted associations are retained.

### P4 — Typed-hole contextualization

- Andrew Blinn et al., *Statically Contextualizing Large Language Models with
  Typed Holes*, PACMPL 8(OOPSLA2), 2024.
- DOI [10.1145/3689728](https://doi.org/10.1145/3689728); related preprint
  [10.48550/arXiv.2409.00921](https://doi.org/10.48550/arXiv.2409.00921).
- Scite supplied the first 8,000 of 67,973 indexed body characters, not the
  complete paper. Main additionally read [primary preprint
  v1](https://arxiv.org/html/2409.00921v1), evaluation/ablation §§2.7–2.9,
  TypeScript implementation/results and §4 limits. Claims about semantic
  context distinguish retrieval from diagnostic repair. No deployment changes
  or cross-language causal effect are inferred from this paper.

### P5 — FPEval / FPBench

- Lang et al., *Perish or Flourish? A Holistic Evaluation of Large Language
  Models for Code Generation in Functional Programming*.
- DOI [10.48550/arXiv.2601.02060](https://doi.org/10.48550/arXiv.2601.02060),
  [v1, 5 January 2026](https://arxiv.org/html/2601.02060v1); preprint.
- Main read §§1–2 and beginning of §3, including Table 1. Algorithmic sampling,
  templates and static style checks were verified. No numerical comparative
  effect is reused: surrounding prose and Table 1 have inconsistencies. The
  primary author list says Eric Lang, unlike Scite's Evan Lang metadata.
  The paper's pure-OCaml label and causal training explanations are not adopted.

### P6 — Architectural knowledge and task platforms

- Santilli et al., *SAKE*: DOI
  [10.48550/arXiv.2606.29520](https://doi.org/10.48550/arXiv.2606.29520),
  [v1, 28 June 2026](https://arxiv.org/html/2606.29520v1). Main read abstract,
  introduction and methodology opening, including the explicit knowledge versus
  open-ended design boundary. No full-results or question-quality audit.
- Adnan et al., *ArchBench*: DOI
  [10.48550/arXiv.2603.17833](https://doi.org/10.48550/arXiv.2603.17833),
  [v1, 18 March 2026](https://arxiv.org/html/2603.17833v1). Main read all four
  main-text sections. Primary landing identifies ICSA 2026 Showcase. Task
  coverage and differing implementation readiness were checked; no platform
  installation or leaderboard result reproduction.

### P7 — ToCS

- Grigory Sapunov, *Theory of Code Space: Do Code Agents Understand Software
  Architecture?* DOI
  [10.48550/arXiv.2603.00601](https://doi.org/10.48550/arXiv.2603.00601).
- Primary latest [v4, 18 March 2026](https://arxiv.org/html/2603.00601v4);
  preprint. Scite supplied first 8,000 of 32,285 body characters. Main checked
  the primary v4 §§3 and 6 opening to verify that reported evaluation is
  Construct only, not completed downstream maintenance or belief-revision
  experiments. Abstract-level capability findings are not used as a size law.

### P8 — Inherited-maintenance benchmark editions

The Luna Max worker read the following primary sections. The main agent accepted
the bounded factual extraction and owns its interpretation; this is separate AI
extraction, not an independent human review or rerun of reported experiments.
All six identifiers below are arXiv preprint DOIs; no unverified proceedings
status is inferred.

| Work / DOI | Primary edition | Worker reading extent and scope limit |
| --- | --- | --- |
| SlopCodeBench — [10.48550/arXiv.2603.24755](https://doi.org/10.48550/arXiv.2603.24755) | [v2, 7 May 2026](https://arxiv.org/html/2603.24755v2) | §1, §§2.1–2.4, §3.1; Appendices B.3, C.1–C.5, D/Table 8 and D.1. Python, generated starting architecture; not a supplied-architecture intervention. |
| ChainSWE — [10.48550/arXiv.2607.02606](https://doi.org/10.48550/arXiv.2607.02606) | [v2, 1 September 2026](https://arxiv.org/html/2607.02606v2) | Selected §§1–5, §6; Appendices A.3–A.4, B and C. Python; mined chains of at most five; not a language comparison. |
| SWE-EVO — [10.48550/arXiv.2512.18470](https://doi.org/10.48550/arXiv.2512.18470) | [v6, 22 May 2026](https://arxiv.org/html/2512.18470v6) | §§3.1–3.3, §§4.1–4.3, §6. Python release tasks; release-level aggregate versus inherited agent chain distinguished. |
| SWE-Milestone — [10.48550/arXiv.2603.13428](https://doi.org/10.48550/arXiv.2603.13428) | [v4, 21 July 2026](https://arxiv.org/html/2603.13428v4) | Selected §§1–5, §6; Appendices B.2–B.3 and C.3. Historical milestone reconstruction, selection and test-adequacy limits; not randomized architecture. |
| CodeThread — [10.48550/arXiv.2606.21804](https://doi.org/10.48550/arXiv.2606.21804) | [v1, 19 June 2026](https://arxiv.org/html/2606.21804v1) | §§1–4.2 in primary HTML; selected §§5–6 through four Scite body slices at offsets 0, 8,000, 16,000 and 24,000. Two-step, model-specific filtered population; no human effort measured. |
| SWE-CI — [10.48550/arXiv.2603.03823](https://doi.org/10.48550/arXiv.2603.03823) | [v4, 1 April 2026](https://arxiv.org/html/2603.03823v4) | §§2.1–2.3, §§3.1–3.2, §§4.1–4.4. Iterative test progression; oracle-informed requirements are not our information policy. |

For CodeThread the main agent additionally read primary §§3–4, §5.3 and
Appendices B/C.1 and inspected §6. Existing-test filtering, shared-subset
comparisons and incomplete failure attribution limit an architecture-specific
interpretation. This directly prompted narrowing the gap claim; the result is
not dismissed because it overlaps our intended contribution.

## Claim discipline and unresolved coverage

No primary study here proves an F# advantage or a generic FP-versus-OO effect.
The assessment's proposed intervention, outcomes and sampling requirements are
methodological recommendations, not conclusions asserted by a single paper.
Source appearance in the ledger does not adopt its metric or evaluator.

Before a paper-level novelty assertion, screen the remaining relevant query
results, follow references and citers of included work with an independent
index, verify unassessed close methods, reconcile preprint/proceedings lineages
and update the search near submission. A limited citation graph and broad
keyword ranking cannot certify completeness. The practical next project gate
remains the existing human claim/design review, not benchmark execution.

## DOI decision inventory

`C` means credited for claims in the assessment; `E` means not credited in this
answer. Exclusion is not a finding of low quality or proof of irrelevance.
Promising unread leads remain explicitly pending. `F1b:27`, for example, is
global F1 rank 27. Worker-only records are marked W; descriptive labels explicitly
identified as such are not invented paper titles. DOI case is normalized, not
a new bibliographic identity. Two journal/preprint pairs represent two works,
not four independent studies.

The inventory contains **139 distinct DOI identifiers: 16 credited and 123 not credited**.
That is not a count of full papers read. Reading extent is specified above.

| Query/rank | DOI | Retrieved title or identified label | Decision and reason |
| --- | --- | --- | --- |
| F1:1 | [10.48550/arxiv.2511.04824](https://doi.org/10.48550/arxiv.2511.04824) | Agentic Refactoring: An Empirical Study of AI Coding Agents | E — Relevant empirical refactoring lead; partial abstract only, not full methods assessment. |
| F1:2 | [10.48550/arxiv.2603.17833](https://doi.org/10.48550/arxiv.2603.17833) | ArchBench: Benchmarking Generative-AI for Software Architecture Tasks | C — P6; primary task-platform scope and implementation limits. |
| F1:3, F3:3 | [10.48550/arxiv.2510.12399](https://doi.org/10.48550/arxiv.2510.12399) | A Survey of Vibe Coding with Large Language Models | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1:4 | [10.1117/12.3112488](https://doi.org/10.1117/12.3112488) | An empirical study on self-admitted technical debt (SATD) detection with large language models | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1:5 | [10.64137/31079911/ijmst-v2i2p103](https://doi.org/10.64137/31079911/ijmst-v2i2p103) | Autonomous Code Review Using Large Language Models: A Hybrid Framework for Code Quality Assessment, Refactoring Recommendation, and Technical Debt Reduction | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1:6 | [10.48550/arxiv.2604.08293](https://doi.org/10.48550/arxiv.2604.08293) | CIAO - Code In Architecture Out - Automated Software Architecture Documentation with Large Language Models | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1:7 | [10.48550/arxiv.2512.11922](https://doi.org/10.48550/arxiv.2512.11922) | Vibe Coding in Practice: Flow, Technical Debt, and Guidelines for Sustainable Use | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1:8 | [10.48550/arxiv.2605.06464](https://doi.org/10.48550/arxiv.2605.06464) | To What Extent Does Agent-generated Code Require Maintenance? An Empirical Study | E — Direct longitudinal-maintenance lead; methods unassessed. Modification incidence must not be equated to causal architecture effects. |
| F1:9 | [10.48550/arxiv.2510.23068](https://doi.org/10.48550/arxiv.2510.23068) | Checkstyle+: Reducing Technical Debt Through The Use of Linters with LLMs | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1:10 | [10.48550/arxiv.2601.07786](https://doi.org/10.48550/arxiv.2601.07786) | "TODO: Fix the Mess Gemini Created": Towards Understanding GenAI-Induced Self-Admitted Technical Debt | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1:11, F2:1 | [10.48550/arxiv.2601.02060](https://doi.org/10.48550/arxiv.2601.02060) | Perish or Flourish? A Holistic Evaluation of Large Language Models for Code Generation in Functional Programming | C — P5; primary task and metric construction, not numerical cross-language maintenance effects. |
| F1:12 | [10.48550/arxiv.2603.20415](https://doi.org/10.48550/arxiv.2603.20415) | The Nature of Technical Debt in Research Software | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1:13 | [10.3390/electronics13050816](https://doi.org/10.3390/electronics13050816) | Formal Software Architecture Rule Learning: A Comparative Investigation between Large Language Models and Inductive Techniques | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1:14 | [10.21203/rs.3.rs-9145617/v1](https://doi.org/10.21203/rs.3.rs-9145617/v1) | Automating Best-Practice Refactoring in Java via Multi-Agent Planning and Verification | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1:15 | [10.48550/arxiv.2606.13175](https://doi.org/10.48550/arxiv.2606.13175) | The End of Code Review: Coding Agents Supersede Human Inspection | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1:16 | [10.48550/arxiv.2604.25960](https://doi.org/10.48550/arxiv.2604.25960) | Large Language Models for Multilingual Code Intelligence: A Survey | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1:17, FG, W2:9 | [10.48550/arxiv.2603.27745](https://doi.org/10.48550/arxiv.2603.27745) | Needle in the Repo: A Benchmark for Maintainability in AI-Generated Repository Edits | C — P1; supplied architectural probes and oracle limits, selected primary methods. |
| F1:18 | [10.5281/zenodo.15561007](https://doi.org/10.5281/zenodo.15561007) | Automated Test Suite Enhancement Using Large Language Models With Few-shot Prompting | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1:19 | [10.48550/arxiv.2606.05574](https://doi.org/10.48550/arxiv.2606.05574) | SmellBench: Towards Fine-Grained Evaluation of Code Agents on Refactoring Tasks | E — Close refactoring benchmark lead; excerpts only, no verified methods/results in this update. |
| F1:20 | [10.48550/arxiv.2605.07769](https://doi.org/10.48550/arxiv.2605.07769) | Coding Agents Don't Know When to Act | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1b:21 | [10.63282/3050-9262.ijaidsml-v5i4p129](https://doi.org/10.63282/3050-9262.ijaidsml-v5i4p129) | Intelligent Software Architecture Recovery Using Large Language Models and Graph Neural Networks for Legacy System Modernization | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1b:22, F2:2 | [10.48550/arxiv.2606.29520](https://doi.org/10.48550/arxiv.2606.29520) | SAKE: Software Architectural Knowledge Evaluation Benchmark for Large Language Models | C — P6; primary introduction/method opening on architectural knowledge versus design. |
| F1b:23 | [10.48550/arxiv.2605.02741](https://doi.org/10.48550/arxiv.2605.02741) | AI-Generated Smells: An Analysis of Code and Architecture in LLM and Agent-Driven Development | E — Code/architecture-smell lead; partial abstract only, no downstream causal assessment. |
| F1b:24 | [10.48550/arxiv.2603.00601](https://doi.org/10.48550/arxiv.2603.00601) | Theory of Code Space: Do Code Agents Understand Software Architecture? | C — P7; selected body verifies Construct-only evaluation, not downstream maintenance. |
| F1b:25 | [10.48550/arxiv.2601.13597](https://doi.org/10.48550/arxiv.2601.13597) | AI IDEs or Autonomous Agents? Measuring the Impact of Coding Agents on Software Development | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1b:26 | [10.3390/electronics13091644](https://doi.org/10.3390/electronics13091644) | AI-Driven Refactoring: A Pipeline for Identifying and Correcting Data Clumps in Git Repositories | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1b:27, FG | [10.48550/arxiv.2601.02200](https://doi.org/10.48550/arxiv.2601.02200) | Code for Machines, Not Just Humans: Quantifying AI-Friendliness with Code Health Metrics | C — P2 preprint methods and results; association versus architectural intervention and model/power caveats. |
| F1b:28, W-exact | [10.48550/arxiv.2606.21804](https://doi.org/10.48550/arxiv.2606.21804) | Is Agent Code Less Maintainable Than Human Code? | C — P8; worker and main primary methods on authorship counterfactual; narrows claimed novelty. |
| F1b:29 | [10.4018/979-8-3373-0370-3.ch003](https://doi.org/10.4018/979-8-3373-0370-3.ch003) | AI-Driven Software Maintenance | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1b:30 | [10.48550/arxiv.2605.02163](https://doi.org/10.48550/arxiv.2605.02163) | DocSync: Agentic Documentation Maintenance via Critic-Guided Reflexion | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1b:31 | [10.48550/arxiv.2603.04177](https://doi.org/10.48550/arxiv.2603.04177) | CodeTaste: Can LLMs Generate Human-Level Code Refactorings? | E — Close refactoring lead; partial abstract only, no primary methods assessment. |
| F1b:32 | [10.1007/s10664-026-10858-8](https://doi.org/10.1007/s10664-026-10858-8) | An evaluation study of large language models for addressing code quality issues | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1b:33 | [10.48550/arxiv.2601.16839](https://doi.org/10.48550/arxiv.2601.16839) | AI builds, We Analyze: An Empirical Study of AI-Generated Build Code Quality | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1b:34 | [10.48550/arxiv.2510.22249](https://doi.org/10.48550/arxiv.2510.22249) | Understanding Self-Admitted Technical Debt in Test Code: An Empirical Study | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1b:35 | [10.48550/arxiv.2601.06266](https://doi.org/10.48550/arxiv.2601.06266) | Self-Admitted Technical Debt in LLM Software: An Empirical Comparison with ML and Non-ML Software | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1b:36 | [10.48550/arxiv.2602.07609](https://doi.org/10.48550/arxiv.2602.07609) | Evaluating Large Language Models for Detecting Architectural Decision Violations | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1b:37 | [10.48550/arxiv.2604.00046](https://doi.org/10.48550/arxiv.2604.00046) | Large Language Models for Analyzing Enterprise Architecture Debt in Unstructured Documentation | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1b:38 | [10.48550/arxiv.2604.21699](https://doi.org/10.48550/arxiv.2604.21699) | Can Large Language Models Assist the Comprehension of ROS2 Software Architectures? | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1b:39 | [10.5753/ise.2025.14868](https://doi.org/10.5753/ise.2025.14868) | Evaluating Large Language Models on the Classification of Different Technical Debt Types in Stack Overflow Discussions | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1b:40 | [10.48550/arxiv.2512.21373](https://doi.org/10.48550/arxiv.2512.21373) | AInsteinBench: Benchmarking Coding Agents on Scientific Repositories | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1c:41, W-exact | [10.48550/arxiv.2603.24755](https://doi.org/10.48550/arxiv.2603.24755) | SlopCodeBench: Benchmarking How Coding Agents Degrade Over Long-Horizon Iterative Tasks | C — P8; worker primary methods extraction on inherited iterative generation and cost. |
| F1c:42 | [10.21203/rs.3.rs-10348169/v1](https://doi.org/10.21203/rs.3.rs-10348169/v1) | Agentic AI for Code Quality: A Four-Agent Machine Learning System for Repository Refactoring, Public RAG, Groq Reasoning, and Reinforcement Learning | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1c:43 | [10.21203/rs.3.rs-6688473/v1](https://doi.org/10.21203/rs.3.rs-6688473/v1) | Self-Programming AI: Code-Learning Agents for Autonomous Refactoring and Architectural Evolution | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1c:44 | [10.48550/arxiv.2601.13007](https://doi.org/10.48550/arxiv.2601.13007) | ArchAgent: Scalable Legacy Software Architecture Recovery with LLMs | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1c:45 | [10.48550/arxiv.2602.17955](https://doi.org/10.48550/arxiv.2602.17955) | Mining Type Constructs Using Patterns in AI-Generated Code | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1c:46 | [10.48550/arxiv.2606.14796](https://doi.org/10.48550/arxiv.2606.14796) | Faster Code, Deeper Debt? A Multivocal Literature Review on Technical Debt and Its Early Signs in LLM-Assisted Software Development | E — Relevant multivocal review lead; not full text assessed or primary effect evidence. |
| F1c:47 | [10.21203/rs.3.rs-6786102/v1](https://doi.org/10.21203/rs.3.rs-6786102/v1) | Benchmarking Large Language Models for Data Pipeline Code Generation and Execution | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1c:48 | [10.48550/arxiv.2512.22256](https://doi.org/10.48550/arxiv.2512.22256) | Agentic Software Issue Resolution with Large Language Models: A Survey | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1c:49 | [10.48550/arxiv.2604.03135](https://doi.org/10.48550/arxiv.2604.03135) | AI-Assisted Unit Test Writing and Test-Driven Code Refactoring: A Case Study | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1c:50 | [10.1002/spe.70035](https://doi.org/10.1002/spe.70035) | Detecting Microservice's Architectural Anti‐Pattern Indicators Using Graph Neural Networks | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1c:51 | [10.48550/arxiv.2511.07645](https://doi.org/10.48550/arxiv.2511.07645) | A Self-Improving Architecture for Dynamic Safety in Large Language Models | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1c:52 | [10.1117/12.3105122](https://doi.org/10.1117/12.3105122) | Observatory software management in the era of AI-assisted software engineering | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1c:53 | [10.48550/arxiv.2510.22787](https://doi.org/10.48550/arxiv.2510.22787) | Collaborative LLM Agents for C4 Software Architecture Design Automation | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1c:54 | [10.1117/12.3097590](https://doi.org/10.1117/12.3097590) | A framework for estimating AI-driven savings in software development | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1c:55 | [10.48550/arxiv.2604.04009](https://doi.org/10.48550/arxiv.2604.04009) | Benchmarking and Evaluating VLMs for Software Architecture Diagram Understanding | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1c:56 | [10.48550/arxiv.2601.13139](https://doi.org/10.48550/arxiv.2601.13139) | From Human to Machine Refactoring: Assessing GPT-4's Impact on Python Class Quality and Readability | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1c:57 | [10.3390/software4010003](https://doi.org/10.3390/software4010003) | The Scalable Detection and Resolution of Data Clumps Using a Modular Pipeline with ChatGPT | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1c:58 | [10.1002/smr.70104](https://doi.org/10.1002/smr.70104) | Self‐Admitted Technical Debt Detection Approaches: A Decade Systematic Review | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1c:59 | [10.21203/rs.3.rs-7029913/v1](https://doi.org/10.21203/rs.3.rs-7029913/v1) | Implementation of Large Language Models in Electronic Health Records | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F1c:60 | [10.48550/arxiv.2607.28137](https://doi.org/10.48550/arxiv.2607.28137) | Asymmetric Communication: Large Language Models and Language Games | E — Adjacent software-engineering lead; title/partial-abstract screened, full methods not assessed for this gap. |
| F2:3 | [10.1101/2025.08.26.671083](https://doi.org/10.1101/2025.08.26.671083) | ChatMDV: Democratising Bioinformatics Analysis Using Large Language Models | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F2:4 | [10.48550/arxiv.2601.20727](https://doi.org/10.48550/arxiv.2601.20727) | Audit Trails for Accountability in Large Language Models | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F2:5 | [10.48550/arxiv.2601.16466](https://doi.org/10.48550/arxiv.2601.16466) | Persona Jailbreaking in Large Language Models | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F2:6, FG | [10.1145/3689728](https://doi.org/10.1145/3689728) | Statically Contextualizing Large Language Models with Typed Holes | C — P4; selected Scite body and primary methods on typed context versus correction feedback. |
| F2:7 | [10.48550/arxiv.2604.01851](https://doi.org/10.48550/arxiv.2604.01851) | Can Large Language Models Model Programs Formally? | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F2:8 | [10.48550/arxiv.2604.17377](https://doi.org/10.48550/arxiv.2604.17377) | AnchorMem: Anchored Facts with Associative Contexts for Building Memory in Large Language Models | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F2:9 | [10.1002/iis2.13262](https://doi.org/10.1002/iis2.13262) | Leveraging Large Language Models for Direct Interaction with SysML v2 | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F2:10 | [10.3390/electronics15010056](https://doi.org/10.3390/electronics15010056) | AuditableLLM: A Hash-Chain-Backed, Compliance-Aware Auditable Framework for Large Language Models | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F2:11 | [10.5772/intechopen.1005063](https://doi.org/10.5772/intechopen.1005063) | Perspective Chapter: Integrating Large Language Models and Blockchain in Telemedicine | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F2:12 | [10.48550/arxiv.2606.23459](https://doi.org/10.48550/arxiv.2606.23459) | TriggerBench: Investigating Prospective Memory for Large Language Models | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F2:13 | [10.48550/arxiv.2602.17045](https://doi.org/10.48550/arxiv.2602.17045) | Large Language Models Persuade Without Planning Theory of Mind | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F2:14 | [10.1038/s41746-024-01282-7](https://doi.org/10.1038/s41746-024-01282-7) | Medical large language models are susceptible to targeted misinformation attacks | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F2:15 | [10.5210/fm.v29i2.13567](https://doi.org/10.5210/fm.v29i2.13567) | Notes towards infrastructure governance for large language models | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F2:16 | [10.48550/arxiv.2511.00624](https://doi.org/10.48550/arxiv.2511.00624) | Can Large Language Models Detect Real-World Android Software Compliance Violations? | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F2:17 | [10.1145/3610977.3634999](https://doi.org/10.1145/3610977.3634999) | Generative Expressive Robot Behaviors using Large Language Models | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F2:18 | [10.3390/electronics14163226](https://doi.org/10.3390/electronics14163226) | EVuLLM: Ethereum Smart Contract Vulnerability Detection Using Large Language Models | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F2:19 | [10.1016/j.xhgg.2025.100558](https://doi.org/10.1016/j.xhgg.2025.100558) | A systematic assessment of large language models’ knowledge of rare diseases: How much do large language models know about rare disease? | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F2:20 | [10.48550/arxiv.2601.03432](https://doi.org/10.48550/arxiv.2601.03432) | CodeEval: A pedagogical approach for targeted evaluation of code-trained Large Language Models | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F3:1 | [10.1609/aaaiss.v4i1.31764](https://doi.org/10.1609/aaaiss.v4i1.31764) | Cause and Effect: Can Large Language Models Truly Understand Causality? | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F3:2 | [10.48550/arxiv.2602.04931](https://doi.org/10.48550/arxiv.2602.04931) | Emergent Causal-Geometric Dynamics Across Depth in Large Language Models | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F3:4 | [10.48550/arxiv.2607.25380](https://doi.org/10.48550/arxiv.2607.25380) | Memory for Large Language Models | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F3:5 | [10.48550/arxiv.2605.13773](https://doi.org/10.48550/arxiv.2605.13773) | (How) Do Large Language Models Understand High-Level Message Sequence Charts? | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F3:6 | [10.48550/arxiv.2603.20492](https://doi.org/10.48550/arxiv.2603.20492) | AE-LLM: Adaptive Efficiency Optimization for Large Language Models | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F3:7 | [10.48550/arxiv.2604.15951](https://doi.org/10.48550/arxiv.2604.15951) | Integrating Graphs, Large Language Models, and Agents: Reasoning and Retrieval | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F3:8 | [10.48550/arxiv.2606.21836](https://doi.org/10.48550/arxiv.2606.21836) | AgentDSE: Reasoning-Augmented Architectural Design Space Exploration | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F3:9 | [10.48550/arxiv.2510.04605](https://doi.org/10.48550/arxiv.2510.04605) | Exploring the Power of Diffusion Large Language Models for Software Engineering: An Empirical Investigation | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F3:10 | [10.48550/arxiv.2605.05593](https://doi.org/10.48550/arxiv.2605.05593) | Causal Probing for Internal Visual Representations in Multimodal Large Language Models | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F3:11 | [10.3390/philosophies11020042](https://doi.org/10.3390/philosophies11020042) | Language Without Propositions: Why Large Language Models Hallucinate | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F3:12 | [10.1038/s41598-024-80571-3](https://doi.org/10.1038/s41598-024-80571-3) | Manner implicatures in large language models | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F3:13 | [10.48550/arxiv.2604.09866](https://doi.org/10.48550/arxiv.2604.09866) | Automating Structural Analysis Across Multiple Software Platforms Using Large Language Models | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F3:14 | [10.1002/qub2.70014](https://doi.org/10.1002/qub2.70014) | Large language models for bioinformatics | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F3:15 | [10.3390/bioengineering12050440](https://doi.org/10.3390/bioengineering12050440) | Large Language Models in Genomics—A Perspective on Personalized Medicine | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F3:16 | [10.1186/s12859-024-05847-x](https://doi.org/10.1186/s12859-024-05847-x) | Can large language models understand molecules? | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F3:17 | [10.48550/arxiv.2607.20806](https://doi.org/10.48550/arxiv.2607.20806) | Profiling Lightweight Large Language Models | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F3:18 | [10.21203/rs.3.rs-9653429/v1](https://doi.org/10.21203/rs.3.rs-9653429/v1) | LLM4KT: Enhancing Knowledge Tracing via Large Language Models | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F3:19 | [10.48550/arxiv.2510.06265](https://doi.org/10.48550/arxiv.2510.06265) | Large Language Models Hallucination: A Comprehensive Survey | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F3:20 | [10.1101/2025.11.04.25339501](https://doi.org/10.1101/2025.11.04.25339501) | Evaluating Large Language Models in Interpreting Cervical Cytology | E — Broad-query cross-field or general-model lead; screened metadata does not support this architecture-maintenance claim. |
| F4:1, FG | [10.1109/ase63991.2025.00117](https://doi.org/10.1109/ase63991.2025.00117) | Learning Project-wise Subsequent Code Edits via Interleaving Neural-based Induction and Tool-based Deduction | E — Relevant project-wise edit citer; F4 metadata only, no readable abstract/method verification. |
| F4:2 | [10.48550/arxiv.2608.18645](https://doi.org/10.48550/arxiv.2608.18645) | Code Health in LLM-Based Test Generation: Effectiveness and Token Efficiency | C — P3; primary methods/results and conditional denominators; related-data extension, not independent causal evidence. |
| F4:3, FG | [10.1145/3729274](https://doi.org/10.1145/3729274) | Type-Constrained Code Generation with Language Models | E — Relevant constrained-generation citer; F4 metadata/partial abstract, full methods unassessed. |
| F5:1 | [10.1145/3793655.3793722](https://doi.org/10.1145/3793655.3793722) | Code for Machines, Not Just Humans: Quantifying AI-Friendliness with Code Health Metrics | C — P2 publication identity; Scite metadata and publisher abstract/indexed excerpts. Detailed results bound to preprint. |
| FG | [10.1109/ietc64455.2025.11039478](https://doi.org/10.1109/ietc64455.2025.11039478) | Intelligent Meal Planning: A Generative LLM-Based Autonomous Agent Application | E — Meal-planning application; not software maintenance. |
| FG | [10.1109/isgtmiddleeast65737.2025.11314322](https://doi.org/10.1109/isgtmiddleeast65737.2025.11314322) | Sustainable Energy Management via Integrating Model Context Protocol with Home Assistant | E — Energy-management application; not software maintenance. |
| FG | [10.1109/southeastcon63549.2026.11476670](https://doi.org/10.1109/southeastcon63549.2026.11476670) | Compiler-Guided Inference-Time Adaptation: Improving GPT-5 Programming Performance in Idris | E — Relevant compiler-guided Idris repair lead; methods not assessed, distinct from no-repair architecture condition. |
| FG | [10.1145/3746059.3747646](https://doi.org/10.1145/3746059.3747646) | Denicek: Computational Substrate for Document-Oriented End-User Programming | E — Document-oriented end-user programming; not the assessed coding-agent maintenance contrast. |
| FG | [10.17586/2226-1494-2026-26-3-565-573](https://doi.org/10.17586/2226-1494-2026-26-3-565-573) | Domain-specific code analysis approach | E — Code-analysis citer; metadata only, no assessed causal maintenance contrast. |
| FG | [10.32388/vv1661](https://doi.org/10.32388/vv1661) | Challenges and Paths Towards AI for Software Engineering | E — Broad AI/software-engineering perspective; metadata only, not primary effect evidence. |
| FG | [10.48550/arxiv.2409.00921](https://doi.org/10.48550/arxiv.2409.00921) | Statically Contextualizing Large Language Models with Typed Holes | C — P4 preprint edition; same work as journal DOI, not a second study. |
| FG | [10.48550/arxiv.2604.20835](https://doi.org/10.48550/arxiv.2604.20835) | Parallel-SFT: Improving Zero-Shot Cross-Programming-Language Transfer for Code RL | E — Cross-language training-transfer lead; no architecture/maintenance-method assessment. |
| FG-edge | [10.3390/computers14120534](https://doi.org/10.3390/computers14120534) | (edge only; paper metadata absent) | E — Citation edge only; metadata absent, source content unverified. |
| W1:1, W2:2 | [10.48550/arxiv.2512.18470](https://doi.org/10.48550/arxiv.2512.18470) | SWE-EVO: Benchmarking Coding Agents in Long-Horizon Software Evolution Scenarios | C — P8; worker primary methods extraction distinguishes release tasks from dependent agent chains. |
| W1:2 | [10.48550/arxiv.2512.03549](https://doi.org/10.48550/arxiv.2512.03549) | PARC: An Autonomous Self-Reflective Coding Agent for Robust Execution of Long-Horizon Tasks | E — Scientific/Kaggle execution rather than inherited software maintenance. |
| W1:3 | [10.48550/arxiv.2606.10728](https://doi.org/10.48550/arxiv.2606.10728) | DeNovoSWE: Scaling Long-Horizon Environments for Generating Entire Repositories from Scratch | E — From-scratch repository generation; not an inherited-architecture contrast. |
| W1:4 | [10.48550/arxiv.2608.00267](https://doi.org/10.48550/arxiv.2608.00267) | LoopsBench: From Harness Engineering to Loop Engineering in Coding Agent Evaluation | E — Promising DAG-linked multi-language lead; abstract only, methods not assessed. |
| W1:5 | [10.48550/arxiv.2512.12730](https://doi.org/10.48550/arxiv.2512.12730) | NL2Repo-Bench: Towards Long-Horizon Repository Generation Evaluation of Coding Agents | E — Empty-workspace repository generation; not the maintenance contrast. |
| W1:6 | [10.48550/arxiv.2602.06176](https://doi.org/10.48550/arxiv.2602.06176) | Large Language Model Reasoning Failures | E — Broad reasoning-failure lead; title only recovered, not assessed. |
| W1:7 | [10.48550/arxiv.2603.17104](https://doi.org/10.48550/arxiv.2603.17104) | When the Specification Emerges: Benchmarking Faithfulness Loss in Long-Horizon Coding Agents | E — Evolving-specification lead; title only recovered, methods remain unassessed. |
| W1:8 | [10.48550/arxiv.2602.02619](https://doi.org/10.48550/arxiv.2602.02619) | daVinci-Agency: Unlocking Long-Horizon Agency Data-Efficiently | E — General agency/training lead; title only recovered, not assessed. |
| W1:9 | [10.48550/arxiv.2606.29116](https://doi.org/10.48550/arxiv.2606.29116) | Characterizing Large Language Model Agentic Workflows: A Study on N8n Ecosystem | E — Workflow-ecosystem study; title only recovered, not assessed. |
| W1:10 | [10.48550/arxiv.2607.26777](https://doi.org/10.48550/arxiv.2607.26777) | CodeSpec: Dual Executable Specifications for Agentic Long-Horizon Feature Development | E — Executable-specification development scaffold; no primary maintenance-gap assessment here. |
| W1:11 | [10.1038/s44172-025-00517-z](https://doi.org/10.1038/s44172-025-00517-z) | MechRAG: A Multimodal Large Language Model for Mechanical Engineering | E — Mechanical-engineering RAG, not code maintenance. |
| W1:12 | [10.48550/arxiv.2607.09510](https://doi.org/10.48550/arxiv.2607.09510) | Failure as a Process: An Anatomy of CLI Coding Agent Trajectories | E — Coding-agent process lead; not the closest inherited benchmark in this bounded read. |
| W1:13 | [10.48550/arxiv.2510.23822](https://doi.org/10.48550/arxiv.2510.23822) | ReCAP: Recursive Context-Aware Reasoning and Planning for Large Language Model Agents | E — General long-horizon planning; software-maintenance contrast not assessed. |
| W1:14 | [10.48550/arxiv.2603.06358](https://doi.org/10.48550/arxiv.2603.06358) | A Scalable Benchmark for Repository-Oriented Long-Horizon Conversational Context Management | E — Relevant conversation-management lead; inherited evolution outcome not verified. |
| W1:15 | [10.48550/arxiv.2510.11004](https://doi.org/10.48550/arxiv.2510.11004) | Automating Structural Engineering Workflows with Large Language Model Agents | E — Structural engineering, not software architecture maintenance. |
| W2:1 | [10.48550/arxiv.2607.02606](https://doi.org/10.48550/arxiv.2607.02606) | ChainSWE | C — P8; worker primary methods extraction on code and transcript inheritance. |
| W2:3 | [10.48550/arxiv.2604.16359](https://doi.org/10.48550/arxiv.2604.16359) | LLM log-analysis paper (full title not retained in handoff) | E — Log analysis, not inherited maintenance. |
| W2:4 | [10.48550/arxiv.2603.13428](https://doi.org/10.48550/arxiv.2603.13428) | SWE-Milestone | C — P8; worker primary methods extraction on stateful milestone dependencies. |
| W2:5 | [10.21203/rs.3.rs-10926809/v1](https://doi.org/10.21203/rs.3.rs-10926809/v1) | JNI/code-smell study (full title not retained in handoff) | E — Code-smell study; no direct inherited benchmark assessed. |
| W2:6 | [10.48550/arxiv.2608.07147](https://doi.org/10.48550/arxiv.2608.07147) | Preference/training paper (full title not retained in handoff) | E — Preference/training method, not the maintenance intervention. |
| W2:7 | [10.48550/arxiv.2603.23443](https://doi.org/10.48550/arxiv.2603.23443) | Test-generation-under-evolution paper (full title not retained in handoff) | E — Adjacent test-generation lead, no inherited-code maintenance contrast assessed. |
| W2:8 | [10.21203/rs.3.rs-5589929/v1](https://doi.org/10.21203/rs.3.rs-5589929/v1) | Requirements-engineering review (full title not retained in handoff) | E — Requirements review, not the close benchmark contrast. |
| W2:10 | [10.48550/arxiv.2607.12541](https://doi.org/10.48550/arxiv.2607.12541) | Dockerfile-drift repair paper (full title not retained in handoff) | E — Narrow Dockerfile repair lead, not assessed for the architecture question. |
| W2:11 | [10.48550/arxiv.2606.18733](https://doi.org/10.48550/arxiv.2606.18733) | SWE-Future | E — Adjacent benchmark methodology lead, no full methods read here. |
| W2:12 | [10.1145/3803437.3804877](https://doi.org/10.1145/3803437.3804877) | Agent-evaluation framework (full title not retained in handoff) | E — Broad evaluation framework, not direct maintenance-effect evidence. |
| W2:13 | [10.21203/rs.3.rs-6660357/v1](https://doi.org/10.21203/rs.3.rs-6660357/v1) | Negotiation-agent paper (full title not retained in handoff) | E — Non-code negotiation agents. |
| W2:14 | [10.48550/arxiv.2608.04682](https://doi.org/10.48550/arxiv.2608.04682) | Proactive bug-discovery paper (full title not retained in handoff) | E — Bug discovery without issues; repeated maintenance contrast not assessed. |
| W2:15 | [10.1007/978-0-387-77743-6_21](https://doi.org/10.1007/978-0-387-77743-6_21) | Software-evolution chapter (full title not retained in handoff) | E — 2008 chapter; not current LLM-maintenance evidence. |
| W-exact | [10.48550/arxiv.2603.03823](https://doi.org/10.48550/arxiv.2603.03823) | SWE-CI | C — P8; worker primary methods on oracle-informed iterative requirements; information-policy distinction. |

## Additional web screening

Primary web pages corresponding to inventory DOIs are the same sources, not
additional studies. These 32 other returned/considered URLs were not credited.
No signed access URLs or credentials are retained. A bibliography mentioned
inside a paper was not counted as independently retrieved literature.

| Returned URL | Exclusion reason |
| --- | --- |
| [source](https://dblp.dagstuhl.de/rec/journals/pacmpl/BlinnLKO24.html) | Secondary bibliographic metadata; primary typed-hole paper used. |
| [source](https://github.com/repowise-dev/repowise) | Practitioner project; not primary evidence of maintenance effects. |
| [source](https://hyrax.dev/blog/automated-code-refactoring) | Commercial/practitioner overview; primary studies used instead. |
| [source](https://codescene.com/blog/making-legacy-code-ai-ready-benchmarks-on-agentic-refactoring) | Vendor summary; primary CodeHealth paper used instead. |
| [source](https://www.ai-fokus.se/ai-fokus26-preso/Agentic-AI-Coding-Practices-for-Speed-with-Quality.pdf) | Presentation lead; methods not assessed. |
| [source](https://substack-post-media.s3.us-east-1.amazonaws.com/post-files/145242280/8d42d5d8-37f8-4e6e-b3f5-4e8ccbbe5acd.pdf) | Returned PDF lead, not opened; signed query parameters deliberately omitted. |
| [source](https://www.reddit.com/r/ClaudeCode/comments/1tuf91j/a_code_health_score_that_predicts_which_files/) | Discussion, not primary effect evidence. |
| [source](https://cmu-tcingc.github.io/Final-Reports/TCinGC-Palau-HCF-2025-FinalReport.pdf) | Off-topic project report. |
| [source](https://spillwave.com/writing/engineering-dynamic-context-the-claude-code-architecture-that-survives-production/) | Practitioner context guidance, not independently validated effect evidence. |
| [source](https://ithub.global.ssl.fastly.net/andrei10k/repo-guard) | Tool-project search result; not maintenance-effect evidence. |
| [source](https://www.sciencedirect.com/science/article/pii/S0167739X26002335) | Adjacent code-translation pipeline; full methods not assessed and DOI not inferred. |
| [source](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2026.1759211/full) | AI-assurance/policy lead, outside the maintained-architecture contrast. |
| [source](https://www.scribd.com/document/976042431/Refactoring-vs-Refuctoring-Advancing-the-State-of-AI-Automated-Code-Improvements) | Secondary document host; methods not read. |
| [source](https://www.reddit.com/r/AI_Agents/comments/1w5d8e7/are_coding_agents_missing_an_architecture_layer_i/) | Discussion, not primary effect evidence. |
| [source](https://www.geektak.com/blog/claude-code-architecture-technical-implementation-guide) | Practitioner guide, not controlled maintenance evidence. |
| [source](https://www.reddit.com/r/mcp/comments/1rf7cig/project_i_built_an_mcp_server_that_gives_ai/) | Discussion/tool announcement, not primary effect evidence. |
| [source](https://www.reddit.com/r/softwaredevelopment/comments/1v5fhsd/i_checked_which_codehealth_markers_actually/) | Discussion; primary CodeHealth studies assessed separately. |
| [source](https://su.diva-portal.org/smash/get/diva2%3A2030902/FULLTEXT01.pdf) | Thesis lead; full text not assessed. |
| [source](https://mau.diva-portal.org/smash/get/diva2%3A1984520/FULLTEXT02.pdf) | NPC-pipeline lead, not the maintained-architecture contrast. |
| [source](https://www.reddit.com/r/softwarearchitecture/comments/1urpnxr/how_are_you_enforcing_engineering_standards_with/) | Discussion, not primary effect evidence. |
| [source](https://www.reddit.com/r/claude/comments/1vaitqo/managing_tech_debt_when_the_agent_writes_most_of/) | Discussion, not primary effect evidence. |
| [source](https://www.reddit.com/r/node/comments/1schszw/i_spent_a_week_reading_through_aigenerated_code/) | Discussion, not primary effect evidence. |
| [source](https://en.wikipedia.org/wiki/Comment_%28computer_programming%29) | General encyclopedia entry, not primary effect evidence. |
| [source](https://www.reddit.com/r/videos/comments/1i653in) | Discussion/video result, not primary effect evidence. |
| [source](https://www.reddit.com/r/ExperiencedDevs/comments/1rgz7bs/removed/) | Discussion/removed-post result, not primary effect evidence. |
| [source](https://www.reddit.com/r/ExperiencedDevs/comments/1un73lp/damage_control_devs_high_on_ai_use/) | Discussion, not primary effect evidence. |
| [source](https://www.reddit.com/r/ChatGPT/comments/1sbtvrq/the_productivity_lie_why_ai_tools_make_you_feel/) | Discussion, not primary effect evidence. |
| [source](https://arxiv.org/abs/2608.23283) | Apodex 1.1 general coding-agent model lead; no architecture-treatment methods assessed. |
| [source](https://ouci.dntb.gov.ua/en/works/4KrJaxXg/) | Secondary bibliographic/citation result; primary study used. |
| [source](https://www.researchgate.net/publication/410658938_Code_for_Machines_Not_Just_Humans_Quantifying_AI-Friendliness_with_Code_Health_Metrics) | Secondary publication listing; primary CodeHealth study used. |
| [source](https://ouci.dntb.gov.ua/en/works/lmbPdoEO/) | Secondary bibliographic/citation result; not independent primary evidence. |
| [source](https://ouci.dntb.gov.ua/en/works/9jdMM8dq/) | Secondary bibliographic/citation result; not independent primary evidence. |

## Closed source-decision audit and document checks

Scite answer ID: `alf-research-frontier-gap-2026-09-14`. One
`report_citations` call recorded **16 credited / 155 excluded / 0 skipped**.
The subsequent answer-scoped `citation_report` verified 171 screened source
identifiers, untruncated output, no missing decision reasons and
`retrieval_unlinked=false`. Its retrieved count is null for an answer-scoped
report, not zero and not a completeness measure.

Provenance counts are 110 main-agent Scite identifiers, 29 worker-only
identifiers labeled `other` with their Scite/primary provenance, and 32
additional web URLs. The 16 credited DOI identifiers represent 14 works after
the two journal/preprint pairs are collapsed. Fifteen decisions use the tool's
`full_text` stage for selected body reading; this does not mean 15 papers were
read in full. The publication-only CodeHealth identifier uses metadata/excerpt
screening. All 155 exclusions have reasons; unread close leads are excluded
from claims, not declared disproven or irrelevant.

The main agent self-reviewed inference and claim boundaries, including
CodeThread's selection and the non-significant frontier-model comparisons in
the CodeHealth preprint. The worker supplied separate AI source extraction,
not human expert approval. Local checks validated UTF-8 decoding and 90 relative
file links across the two new notes, AGENTS.md and PLAN.md; publication also
requires whitespace checks and exact-commit CI. This is documentation-only work:
no runtime test, trusted fixture, candidate execution, model/count call, OAuth
staging or scientific treatment was rerun or changed.
