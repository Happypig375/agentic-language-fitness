# Literature search-depth audit (2026-09-14)

**Inspected source:** `49caefdf0b08029e2b5eeb81b958bfde3fdab331`.
Fetched upstream before editing; local HEAD and origin/main matched.
**Question:** Was reading the first five results per query enough, and would
later results have improved the research context?
**Disposition:** research-method correction and bounded sensitivity audit;
no scientific treatment or execution decision is adopted.

## Answer and correction

No, not for a defensible account of literature coverage or the research gap.
Five was a retrieval cap, not an evidence-based stopping rule. The earlier
records describe bounded searches, but that qualification does not establish
adequate coverage for the broader research-positioning questions.

Also, five retrieved records did **not** mean five full papers read. Search
responses commonly supplied titles and truncated abstracts or selected
excerpts. Selected papers received abstract or body access, with limits recorded
in the earlier ledgers. Retrieval, screening, full-text assessment and synthesis
must remain distinct.

The prior searches can support specific, qualified claims and provisional
hypotheses where their cited sources suffice. They cannot establish that the
most relevant evidence was found, that contrary evidence was exhausted, or
that no prior study answers the question. In particular, “no direct verification
found in this bounded search” must not become “no such research exists.”

Yes: deeper results actually added useful context in this audit. The main
agent checked that the three P2 selections below were absent from the existing
docs/PLAN/AGENTS DOI records. This is a demonstrated limitation of the cutoff,
not a guess that more search might help.

## What later results changed

Positions below are positions in the returned query pages on this date, not
quality rankings or stable bibliographic identifiers.

| Discovery | Paper and verified access | Additional context and limits |
| --- | --- | --- |
| P2 position 17 | Toczé et al., *Maintainability of functional reactive programs in a telecom server software* (2016), [10.1145/2851613.2851954](https://doi.org/10.1145/2851613.2851954). Entire indexed body read; not an independent visual inspection of the original figures. | Haskell FRP versus C++ OO prototypes of a simplified LTE protocol. Four experts assessed the code; three other domain experts helped construct the questionnaire. Separate ratings favored FRP overall, but direct comparison rated overall maintainability, modularity and understandability equally. FRP was more compact, while OO was faster. Expert ratings and size metrics are not observed longitudinal maintenance effort, and language/framework/paradigm change together. |
| P2 position 27 | MacQueen, *Should ML be Object-Oriented?* (2002), [10.1007/s001650200010](https://doi.org/10.1007/s001650200010). Introduction/overview body inspected, not the entire paper. | A scholarly language-design argument about ML functions/modules versus class-based OO mechanisms is closer to the user's coherence question than an unqualified functional-versus-OO label. It supplies conceptual vocabulary, not empirical proof that F# maintenance is cheaper or that modern C# is inferior. |
| P2 position 35 | Avgustinov et al., *Modularity first* (2008), [10.1145/1353482.1353486](https://doi.org/10.1145/1353482.1353486). Complete abstract only; body access denied. | Reimplementing an AspectJ compiler frontend with JastAdd provides a modularity/tooling-package lead. It illustrates why a whole implementation mechanism may matter; the abstract does not isolate language effects or establish long-term maintenance savings. Quantitative claims are not carried into our design. |
| M2 position 20 | Puma Pucho et al., *Refactoring Python Code with LLM-Based Multi-Agent Systems* (2025), [10.5753/sbes.2025.11033](https://doi.org/10.5753/sbes.2025.11033). Complete abstract rechecked by main; body unavailable through Scite. | The abstract reports applying a pipeline to 1,719 files and improving structural metrics, while also reporting 281 syntactically invalid outputs without a validation agent. This is a direct caution against equating compact/modular output with successful maintenance. Full methods and behavioral correctness remain unassessed. |
| M2 position 21 | Jang et al., *StoryCoder* (2026), [10.48550/arxiv.2604.14631](https://doi.org/10.48550/arxiv.2604.14631), [primary v1, 16 April 2026](https://arxiv.org/html/2604.14631v1). Worker read selected methods/results/limitations; main checked primary introduction, setup and generator/solver distinctions. | Narrative reformulation on programming benchmarks is adjacent evidence that task presentation can influence decisions and generated structure. Open-model conditions can use a different model to generate the narrative. This is not maintained-software architecture, an isolated size effect or a long-term maintenance outcome. No narrative prompting treatment is adopted. |
| M3 position 23 | Chen et al., *Bridging Code Graphs and Large Language Models for Better Code Understanding* (CGBridge), [10.48550/arxiv.2512.07666](https://doi.org/10.48550/arxiv.2512.07666), [primary v1, 8 December 2025](https://arxiv.org/html/2512.07666v1). Worker read the indexed body; main checked primary method, Table 1 and §§4.1–4.4. | Trained graph-to-model representations improve selected summarization/translation outcomes across code models; simply serializing graphs can underperform text-only baselines. This strengthens the need to separate information presentation, trained assistance and model identity from software architecture. It is not a maintenance or F#/C# experiment. The inspected identity is the arXiv version; embedded conference metadata is not separately verified. |

The telecom paper is especially informative because its detailed results are
more mixed than its favorable conclusion. The authors infer maintainability
from compactness, but their direct overall maintainability comparison is equal.
Our inference is to retain distinct outcomes and the prototype/expertise/package
limitations, not to average these into a universal paradigm ranking.

The LLM papers add plausible mechanisms and confounds, not verification of the
proposed human-expertise-to-model-capability analogy. In particular, a neural
model's architecture, an agent pipeline's architecture, a representation of code,
and the architecture of the software being maintained are different variables.
The current literature leaves both capability-threshold and scaffolding
hypotheses open. None of these findings reverses or justifies tuning away the
existing larger F# reference envelopes.

## What a defensible next review would require

The following is a proposed research-review procedure, not a claim that it has
already been completed and not an experimental amendment.

1. Define the questions and inclusion rules first. Separate human architectural
   maintenance, idiomatic language/package comparisons, LLM representation and
   capability, and measurement validity. Keep conceptual mechanisms, empirical
   maintenance outcomes and adjacent generation benchmarks in separate evidence
   categories; do not exclude contrary/null findings for lacking an advantage.
2. Screen the eligible results of the prespecified searches, not just the first
   page. Use synonymous terms and an independent index/source to check coverage.
   Retrieve in manageable batches; if time limits the screen, disclose the exact
   unexamined range instead of calling the search complete.
3. Follow references and citing papers from the included studies, covering
   different research communities. Repeatedly retrieving the same five records
   under related queries is not independent evidence of coverage.
4. Obtain and assess decision-critical primary methods, outcomes and limitations.
   Record version/DOI lineages, populations, tasks, comparison conditions,
   confounds, effect direction and uncertainty. Unavailable full text remains
   unresolved; it is neither proof of low quality nor confirmation of the abstract.
5. Use a prespecified stopping procedure: complete the defined search scope and
   iterate backward/forward citation screening until no new eligible studies are
   added within that scope. Check the review against an independent search and
   known relevant studies, then perform a dated update before publication.
   That is stronger than a fixed top-N cutoff but still not a guarantee of
   finding every paper in disconnected or poorly indexed communities.

This approach follows the distinction between a diverse start set, iterative
citation screening and full-paper inclusion assessment in Wohlin's snowballing
guidelines, [10.1145/2601248.2601268](https://doi.org/10.1145/2601248.2601268)
([author PDF](https://www.wohlin.eu/ease14.pdf), introduction and §3 inspected).
The loop's stopping condition is no new eligible papers, not five hits.

Wohlin et al.'s hybrid-search study,
[10.1016/j.infsof.2022.106908](https://doi.org/10.1016/j.infsof.2022.106908),
further distinguishes a planned database-plus-snowballing procedure from ad hoc
top-ups. Selected introduction/related-work and final discussion/validity/
conclusion sections were read. Its findings depend on the start set and study
scope; they do not prescribe a universally sufficient hit count. Our capped
single-seed graph below is an exploratory check, **not** that full procedure.

For the project, the appropriate next research step is a structured evidence
map and deeper assessment of the relevant pending leads, before claiming a
research gap. There is no need to read every irrelevant hit end to end. There
is a need to distinguish why each lead was screened out, deferred or included.
A second human assessment of consequential inclusion and causal interpretations
would improve a paper-facing review; this AI audit is not that assessment.

## Reproducible search and access record

Connected Scite, 2026-09-14 HKT, intent `search_depth_audit`, default relevance,
no date filters. Search totals are service-reported matches, not eligible-study
counts. Offsets are zero-based; table positions are one-based.

| Query | Exact term / lookup | Pages and returned counts |
| --- | --- | --- |
| P2 | `"functional programming" AND "object-oriented" AND ("maintenance" OR "modularity" OR "maintainability")` | Total 2,627. Control offset 0/limit 5 returned 5; offsets 5, 15, 25/limit 10 returned 10 each. First five matched the earlier P2 inventory. |
| M2 | `"large language models" AND ("code modularity" OR "modular code") AND ("small" OR "size" OR "scale")` | Total 93. Offsets 5 and 15/limit 10 returned 10 each; worker-owned retrieval. |
| M3 | `"large language models" AND ("code comprehension" OR "program comprehension") AND ("complexity" OR "architecture")` | Total 406. Offsets 5 and 15/limit 10 returned 10 each; worker-owned retrieval. Position 15 was repeated at position 16 across page boundaries. |
| Methods | Title lookups for `Guidelines for snowballing in systematic literature studies and a replication in software engineering` and `Successful combination of database search and snowballing for identification of primary studies in systematic literature studies` | Offset 0/limit 10; 7 total/returned DOI records, including same-title deposits. |
| G | Incoming graph from `10.1109/tse.2004.43`; depth 1, max_edges 25, include_intent true, include_snippets false | 25 edges/26 nodes including seed; **truncated=true**. Seed coverage 25 and no low-coverage warning do not negate truncation or missing non-DOI links. |

P2 added 30 rows beyond its first five; M2/M3 added 40 rows with one exact DOI
duplicate. Thus the deeper keyword pages returned **70 rows / 69 distinct DOIs**;
with the five P2 control rows, **75 rows / 74 distinct DOIs**. These are records
screened, not 69 full papers read. No claim of saturation follows from now
having reached position 25 or 35. The page overlap also illustrates why ranked
pagination needs a deduplicated inventory.

Main exact-DOI lookups rechecked the three selected worker leads, the two graph
leads identified below, MacQueen and the 2022 methods paper. These repeated
lookups are not new studies. The graph supplied a human-maintenance series and
a review lead, but neither was sufficiently accessible/assessed for new claims.
The earlier [publisher learning-curve lead](https://www.sciencedirect.com/science/article/abs/pii/S0950584908000505)
was retried and returned HTTP 403; web search
`"S0950584908000505" "learning"` returned no hits. Its DOI and findings remain
unverified, not silently inferred from the URL.

Main Scite body access: telecom offsets 0/7000, requests 7000/8000, all 13,922
indexed characters; MacQueen first 7,000 of 61,166; Modularity first complete
1,356-character abstract; refactoring complete 1,655-character abstract;
2022 methods offsets 0/47842, requests 7000/8000 of 55,842 indexed characters.
The 2014 methods tool returned an 821-character abstract; primary author-PDF
sections supplied the procedure. The maintenance-series chapter returned no
readable text. Offsets describe this retrieval only and are not stable
identities if Scite re-indexes the text.

The Luna Max worker screened all 40 M2/M3 rows and examined three selected leads:
refactoring abstract; StoryCoder first 32,000 of 45,596 indexed characters,
including method/results/limitations; CGBridge all 38,462 indexed characters.
Main primary checks are declared in the table above. We do not claim that
search snippets or a worker's selection alone verified an empirical result.
No licensed bodies or private access URLs were saved to the repository.

## Screened-record inventory

“Not selected” below means not used as substantive support in **this bounded
answer**. Relevant unassessed leads are retained for the future review; this is
not a systematic exclusion judgment or a finding of falsity/low quality.
Unless otherwise stated, the reading extent is title plus returned abstract
snippet/excerpts, not a complete abstract or full paper. G records were only
title-triaged except for the two declared access checks.

### Keyword pages

| Query / position | DOI / title | Decision / reason |
| --- | --- | --- |
| P2 / 1 | [10.1145/2846680.2846689](https://doi.org/10.1145/2846680.2846689) — Is functional programming better for modularity? | Not selected: Control: previously screened conceptual modularity comparison; not re-evaluated here. |
| P2 / 2 | [10.21015/vtse.v13i3.2216](https://doi.org/10.21015/vtse.v13i3.2216) — A Comparative Study of Object-Oriented, Procedural, and Functional Programming Paradigms in Microservice Architecture | Not selected: Control: previously abstract-only microservices comparison; full methods remain unassessed. |
| P2 / 3 | [10.66472/paf.v1i1.23](https://doi.org/10.66472/paf.v1i1.23) — Comparative Evaluation of Functional, Object Oriented, and Declarative Programming Paradigms for Scalability and Maintainability in Distributed Data Processing Applications | Not selected: Control: previously abstract-only distributed-data comparison; full methods remain unassessed. |
| P2 / 4 | [10.1109/wse.2012.6320536](https://doi.org/10.1109/wse.2012.6320536) — Normalizing object-oriented class styles in JavaScript | Not selected: Control: JavaScript class-style normalization, not selected maintenance evidence. |
| P2 / 5 | [10.1109/cseet49119.2020.9206213](https://doi.org/10.1109/cseet49119.2020.9206213) — An Observational Study on the Maintainability Characteristics of the Procedural and Object-Oriented Programming Paradigms | Not selected: Control: previously retained procedural/OO observational lead; no new effect direction assessed. |
| P2 / 6 | [10.22541/au.175915460.00864426/v1](https://doi.org/10.22541/au.175915460.00864426/v1) — Toward Functional Programming | Not selected: C# functional-feature integration lead; methods and maintenance outcomes not assessed. |
| P2 / 7 | [10.48550/arxiv.1707.02590](https://doi.org/10.48550/arxiv.1707.02590) — Refinable Function : An Object-oriented Approach to Procedure Modularity | Not selected: Procedure-modularity mechanism proposal; not a verified inherited-maintenance comparison. |
| P2 / 8 | [10.1002/9781119281313.ch2](https://doi.org/10.1002/9781119281313.ch2) — Functional Programming | Not selected: Programming-paradigm chapter; not a selected empirical maintenance study. |
| P2 / 9 | [10.48550/arxiv.2111.13384](https://doi.org/10.48550/arxiv.2111.13384) — $φ$-Calculus: Object-Oriented Formalism | Not selected: OO formalism proposal; not a selected maintenance outcome study. |
| P2 / 10 | [10.1007/978-1-84882-745-5_6](https://doi.org/10.1007/978-1-84882-745-5_6) — Object-Oriented Programs | Not selected: Program-verification chapter; not maintenance effort evidence. |
| P2 / 11 | [10.2307/j.ctv7h0rx7.7](https://doi.org/10.2307/j.ctv7h0rx7.7) — Object-Oriented Programs: | Not selected: Program-verification chapter; same-title lineage not treated as independent evidence. |
| P2 / 12 | [10.52589/bjcnit-facsojao](https://doi.org/10.52589/bjcnit-facsojao) — Detailed Study of the Object-Oriented Programming (OOP) Features in Python | Not selected: Broad OOP exposition; human-readability claims not methodologically assessed. |
| P2 / 13 | [10.52783/jier.v5i2.2466](https://doi.org/10.52783/jier.v5i2.2466) — Optimizing Java applications with advanced functional programming: a comparative Analysis of Java, Scala, and Kotlin | Not selected: Java/Scala/Kotlin comparison lead; outcome methods need full-text assessment. |
| P2 / 14 | [10.3390/app14125083](https://doi.org/10.3390/app14125083) — Puzzle Pattern, a Systematic Approach to Multiple Behavioral Inheritance Implementation in Object-Oriented Programming | Not selected: Inheritance-pattern mechanism lead; not assessed as a controlled maintenance outcome. |
| P2 / 15 | [10.1017/cbo9780511811432.015](https://doi.org/10.1017/cbo9780511811432.015) — Object-Oriented Languages | Not selected: Language chapter; no selected empirical maintenance comparison. |
| P2 / 16 | [10.1017/cbo9781139174930.015](https://doi.org/10.1017/cbo9781139174930.015) — Object-Oriented Languages | Not selected: Same-title language chapter; not counted as an independent study. |
| P2 / 17 | [10.1145/2851613.2851954](https://doi.org/10.1145/2851613.2851954) — Maintainability of functional reactive programs in a telecom server software | Credited: Selected: full indexed body adds mixed ratings, package confounding and performance tradeoff. |
| P2 / 18 | [10.1007/978-3-642-55195-6_11](https://doi.org/10.1007/978-3-642-55195-6_11) — FooPar: A Functional Object Oriented Parallel Framework in Scala | Not selected: Parallel Scala framework; maintenance effects not assessed. |
| P2 / 19 | [10.1007/978-3-540-69149-5_13](https://doi.org/10.1007/978-3-540-69149-5_13) — Modular Reasoning in Object-Oriented Programming | Not selected: Formal modular reasoning; not selected empirical maintenance outcome evidence. |
| P2 / 20 | [10.1017/cbo9780511811449.015](https://doi.org/10.1017/cbo9780511811449.015) — Object-Oriented Languages | Not selected: Same-title language chapter; not counted as an independent study. |
| P2 / 21 | [10.1007/978-3-642-13821-8_12](https://doi.org/10.1007/978-3-642-13821-8_12) — Evaluating Maintainability with Code Metrics for Model-to-Model Transformations | Not selected: Transformation-code metric lead; direct maintenance-outcome validity not assessed. |
| P2 / 22 | [10.1109/imtc.1997.604040](https://doi.org/10.1109/imtc.1997.604040) — An object-oriented model of measurement systems | Not selected: Measurement-system model; outside selected software-maintenance comparison. |
| P2 / 23 | [10.1109/19.728800](https://doi.org/10.1109/19.728800) — An object-oriented model of measurement systems | Not selected: Same-title measurement-system model; no independent maintenance result assessed. |
| P2 / 24 | [10.5485/tmcs.2007.0159](https://doi.org/10.5485/tmcs.2007.0159) — Teaching multiparadigm programming based on object-oriented experiences | Not selected: Multiparadigm teaching lead; not a model-maintenance outcome. |
| P2 / 25 | [10.1016/j.infsof.2008.02.001](https://doi.org/10.1016/j.infsof.2008.02.001) — Object-oriented transformations for extracting aspects | Not selected: Aspect-extraction transformations; not selected maintenance burden evidence. |
| P2 / 26 | [10.1109/step.1997.615494](https://doi.org/10.1109/step.1997.615494) — An overview of object-oriented design metrics | Not selected: OO metrics overview; not an audited causal maintenance result. |
| P2 / 27 | [10.1007/s001650200010](https://doi.org/10.1007/s001650200010) — Should ML be Object-Oriented? | Credited: Selected: language-design coherence argument; introductory body inspected, not empirical proof. |
| P2 / 28 | [10.22452/mjcs.vol23no3.4](https://doi.org/10.22452/mjcs.vol23no3.4) — Maintainability Dynamic Metrics Data Collection Based On Aspect-Oriented Technology | Not selected: Dynamic-metric collection lead; outcome validation not assessed. |
| P2 / 29 | [10.1016/0168-9002(94)91548-2](https://doi.org/10.1016/0168-9002(94)91548-2) — Object-oriented software construction at ALS | Not selected: Title only; no abstract returned, substantive relevance unresolved. |
| P2 / 30 | [10.1109/wcre.2008.58](https://doi.org/10.1109/wcre.2008.58) — Reconsidering Classes in Procedural Object-Oriented Code | Not selected: Design-erosion/refactoring lead; further methods assessment remains open. |
| P2 / 31 | [10.52842/conf.acadia.2014.053](https://doi.org/10.52842/conf.acadia.2014.053) — Imperative / Functional / Object-Oriented: an alternative ontology of programmatic paradigms for design | Not selected: Programming for design applications; not selected maintenance outcome evidence. |
| P2 / 32 | [10.1016/s0167-6423(02)00108-9](https://doi.org/10.1016/s0167-6423(02)00108-9) — Object-oriented tree traversal with JJForester | Not selected: Language-processing integration mechanism; maintenance comparison not assessed. |
| P2 / 33 | [10.2991/emim-16.2016.78](https://doi.org/10.2991/emim-16.2016.78) — Design and Analysis of Object-Oriented Embedded Device Detection Method | Not selected: Embedded-device detection method; outside selected architecture-maintenance question. |
| P2 / 34 | [10.1145/2384577.2384583](https://doi.org/10.1145/2384577.2384583) — Object-oriented programming with gradual abstraction | Not selected: Experimental language abstraction mechanism; maintenance effects not assessed. |
| P2 / 35 | [10.1145/1353482.1353486](https://doi.org/10.1145/1353482.1353486) — Modularity first | Credited: Selected adjacent lead: compiler rewrite abstract; tooling package changed, no long-term maintenance trial established. |
| M2 / 6 | [10.48550/arxiv.2603.24629](https://doi.org/10.48550/arxiv.2603.24629) — Sketch2Simulation: Automating Flowsheet Generation via Multi Agent Large Language Models | Not selected: Flowsheet orchestration; not code-maintenance evidence. |
| M2 / 7 | [10.1177/00811750261421220](https://doi.org/10.1177/00811750261421220) — Computational Basis of Large Language Models’ Decision Making in Social Simulation | Not selected: Social-simulation context effects, not code. |
| M2 / 8 | [10.48550/arxiv.2605.06901](https://doi.org/10.48550/arxiv.2605.06901) — Reflections and New Directions for Human-Centered Large Language Models | Not selected: Broad interaction/design discussion; not the selected maintenance contrast. |
| M2 / 9 | [10.48550/arxiv.2602.10140](https://doi.org/10.48550/arxiv.2602.10140) — Can Large Language Models Implement Agent-Based Models? An ODD-based Replication Study | Not selected: Representation-to-model generation lead; maintenance and size effects unassessed. |
| M2 / 10 | [10.3390/pharmaceutics17101274](https://doi.org/10.3390/pharmaceutics17101274) — Pharmacometrics in the Age of Large Language Models: A Vision of the Future | Not selected: Domain-workflow perspective; no selected empirical maintenance outcome. |
| M2 / 11 | [10.48550/arxiv.2510.18861](https://doi.org/10.48550/arxiv.2510.18861) — Streamlining Acceptance Test Generation for Mobile Applications Through Large Language Models: An Industrial Case Study | Not selected: Test-generation lead; architecture-mediated maintenance not assessed. |
| M2 / 12 | [10.48550/arxiv.2601.22139](https://doi.org/10.48550/arxiv.2601.22139) — Reasoning While Asking: Transforming Reasoning Large Language Models from Passive Solvers to Proactive Inquirers | Not selected: Interaction/training effects; not selected code-maintenance evidence. |
| M2 / 13 | [10.48550/arxiv.2602.11411](https://doi.org/10.48550/arxiv.2602.11411) — Improving the Robustness of Large Language Models for Code Tasks via Fine-tuning with Perturbed Data | Not selected: Perturbation/robustness lead; methods and maintenance transfer need assessment. |
| M2 / 14 | [10.3390/buildings16091722](https://doi.org/10.3390/buildings16091722) — Large Language Model-Based Method for HVAC System Control Code Automatic Generation | Not selected: Domain control-code generation; maintenance outcomes unassessed. |
| M2 / 15 | [10.48550/arxiv.2606.03047](https://doi.org/10.48550/arxiv.2606.03047) — ModuLoop : Low-Level Code Generation using Modular Synthesizer and Closed-Loop Debugger for Robotic Control | Not selected: Robotic generation/debugging scaffold; no selected inherited-maintenance outcome. |
| M2 / 16 | [10.48550/arxiv.2512.15000](https://doi.org/10.48550/arxiv.2512.15000) — DreamPRM-Code: Function-as-Step Process Reward Model with Label Correction for LLM Coding | Not selected: Decomposition/reward/scaling lead; maintenance transfer unassessed. |
| M2 / 17 | [10.48550/arxiv.2604.17261](https://doi.org/10.48550/arxiv.2604.17261) — &inator: Correct, Precise C-to-Rust Interface Translation | Not selected: Interface translation and constraints; not selected architecture-maintenance comparison. |
| M2 / 18 | [10.48550/arxiv.2604.04168](https://doi.org/10.48550/arxiv.2604.04168) — A Semi-Automated Annotation Workflow for Paediatric Histopathology Reports Using Small Language Models | Not selected: Non-code annotation workflow. |
| M2 / 19 | [10.48550/arxiv.2510.21881](https://doi.org/10.48550/arxiv.2510.21881) — GeoThought: A Dataset for Enhancing Mathematical Geometry Reasoning in Vision-Language Models | Not selected: Non-code visual reasoning. |
| M2 / 20 | [10.5753/sbes.2025.11033](https://doi.org/10.5753/sbes.2025.11033) — Refactoring Python Code with LLM-Based Multi-Agent Systems: An Empirical Study in ML Software Projects | Credited: Selected: complete abstract exposes static-metric/correctness distinction; full methods unavailable. |
| M2 / 21 | [10.48550/arxiv.2604.14631](https://doi.org/10.48550/arxiv.2604.14631) — StoryCoder: Narrative Reformulation for Structured Reasoning in LLM Code Generation | Credited: Selected: prompt-representation mechanism, not inherited architecture or clean size effect. |
| M2 / 22 | [10.1093/jamiaopen/ooad046](https://doi.org/10.1093/jamiaopen/ooad046) — AnnoDash, a clinical terminology annotation dashboard | Not selected: Clinical annotation dashboard; not code-maintenance comparison. |
| M2 / 23 | [10.48550/arxiv.2512.07921](https://doi.org/10.48550/arxiv.2512.07921) — DeepCode: Open Agentic Coding | Not selected: Agent information-flow lead; maintenance effects not audited. |
| M2 / 24 | [10.48550/arxiv.2607.14456](https://doi.org/10.48550/arxiv.2607.14456) — Beyond Generalist LLMs: Specialist Agentic Systems for Structured Code Workflow Execution | Not selected: Specialist workflow lead; maintenance outcome not verified. |
| M2 / 25 | [10.21203/rs.3.rs-4372886/v1](https://doi.org/10.21203/rs.3.rs-4372886/v1) — VisionVerse: Dynamic Video Question Answering Through Retrieval-Augmented Generation | Not selected: Video question answering, not code maintenance. |
| M3 / 6 | [10.48550/arxiv.2606.31725](https://doi.org/10.48550/arxiv.2606.31725) — Do Machines Struggle Where Humans Do? LLM and Human Comprehension of Obfuscated Code | Not selected: Relevant human/LLM representation lead; architecture and maintenance transfer unassessed. |
| M3 / 7 | [10.48550/arxiv.2603.17821](https://doi.org/10.48550/arxiv.2603.17821) — CodeT5-RNN: Reinforcing Contextual Embeddings for Enhanced Code Comprehension | Not selected: Neural-model architecture/comprehension lead, not maintained-software architecture. |
| M3 / 8 | [10.48550/arxiv.2605.06910](https://doi.org/10.48550/arxiv.2605.06910) — Benchmarking Large Language Models for IoC Recovery under Adversarial Code Obfuscation and Encryption | Not selected: Security/obfuscation robustness; not selected maintenance comparison. |
| M3 / 9 | [10.48550/arxiv.2512.12117](https://doi.org/10.48550/arxiv.2512.12117) — Citation-Grounded Code Comprehension: Preventing LLM Hallucination Through Hybrid Retrieval and Graph-Augmented Context | Not selected: Retrieval/context lead; longitudinal maintenance effects unassessed. |
| M3 / 10 | [10.5281/zenodo.15561007](https://doi.org/10.5281/zenodo.15561007) — Automated Test Suite Enhancement Using Large Language Models With Few-shot Prompting | Not selected: Testing/prompting lead; architecture effects unassessed. |
| M3 / 11 | [10.48550/arxiv.2602.06687](https://doi.org/10.48550/arxiv.2602.06687) — Evaluating and Enhancing the Vulnerability Reasoning Capabilities of Large Language Models | Not selected: Vulnerability reasoning/scaffolding; not selected maintenance outcome. |
| M3 / 12 | [10.48550/arxiv.2301.06627](https://doi.org/10.48550/arxiv.2301.06627) — Dissociating language and thought in large language models | Not selected: General capability paper, not selected code-architecture evidence. |
| M3 / 13 | [10.48550/arxiv.2512.08145](https://doi.org/10.48550/arxiv.2512.08145) — Chat with UAV -- Human-UAV Interaction Based on Large Language Models | Not selected: Robotics system architecture, not the maintenance comparison. |
| M3 / 14 | [10.48550/arxiv.2511.02869](https://doi.org/10.48550/arxiv.2511.02869) — Analysis of AdvFusion: Adapter-based Multilingual Learning for Code Large Language Models | Not selected: Code adaptation/capability lead; family/training/task confounds need assessment. |
| M3 / 15 | [10.2139/ssrn.6678899](https://doi.org/10.2139/ssrn.6678899) — Semantic and Lexical Retrieval-Augmented Large Language Models for Code Summarization | Not selected: Summarization/context lead; abstract/excerpt only, maintenance effects unassessed. |
| M3 / 16 | [10.2139/ssrn.6678899](https://doi.org/10.2139/ssrn.6678899) — Semantic and Lexical Retrieval-Augmented Large Language Models for Code Summarization | Not selected: Exact duplicate of preceding page's position 15; one DOI decision. |
| M3 / 17 | [10.21203/rs.3.rs-5348871/v1](https://doi.org/10.21203/rs.3.rs-5348871/v1) — On the Performance of Large Language Models on Introductory Programming Assignments | Not selected: Introductory generation, not inherited maintenance. |
| M3 / 18 | [10.48550/arxiv.2601.12274](https://doi.org/10.48550/arxiv.2601.12274) — Hybrid Concolic Testing with Large Language Models for Guided Path Exploration | Not selected: Solver/LLM testing scaffold; not the selected architecture-maintenance effect. |
| M3 / 19 | [10.48550/arxiv.2510.24031](https://doi.org/10.48550/arxiv.2510.24031) — LLMLogAnalyzer: A Clustering-Based Log Analysis Chatbot using Large Language Models | Not selected: Operational log/RAG lead; causal architecture effect unassessed. |
| M3 / 20 | [10.48550/arxiv.2510.22396](https://doi.org/10.48550/arxiv.2510.22396) — PortGPT: Towards Automated Backporting Using Large Language Models | Not selected: Relevant backporting-maintenance lead; abstract only, architecture/model comparison unresolved. |
| M3 / 21 | [10.3390/app15126836](https://doi.org/10.3390/app15126836) — Impact of Developer Queries on the Effectiveness of Conversational Large Language Models in Programming | Not selected: Prompt/context confound lead; not a model comparison. |
| M3 / 22 | [10.3233/faia251283](https://doi.org/10.3233/faia251283) — ASMA-Tune: Unlocking LLMs’ Assembly Code Comprehension via Structural-Semantic Instruction Tuning | Not selected: Structural-comprehension lead; full text unavailable, maintenance interaction unresolved. |
| M3 / 23 | [10.48550/arxiv.2512.07666](https://doi.org/10.48550/arxiv.2512.07666) — Bridging Code Graphs and Large Language Models for Better Code Understanding | Credited: Selected: trained structural representation across models; not maintained architecture or isolated size effect. |
| M3 / 24 | [10.1145/3524610.3527904](https://doi.org/10.1145/3524610.3527904) — Anchoring code understandability evaluations through task descriptions | Not selected: Relevant human comprehension/task-framing lead; no LLM experiment assessed. |
| M3 / 25 | [10.3390/electronics13234584](https://doi.org/10.3390/electronics13234584) — Evaluating Causal Reasoning Capabilities of Large Language Models: A Systematic Analysis Across Three Scenarios | Not selected: General reasoning/model comparison; not selected code-maintenance evidence. |

### Methods lookups

| Discovery | DOI / title | Decision / reason |
| --- | --- | --- |
| Methods | [10.1016/j.infsof.2022.106908](https://doi.org/10.1016/j.infsof.2022.106908) — Successful combination of database search and snowballing for identification of primary studies in systematic literature studies | Credited: Selected review-method guidance; not evidence of F#/C# outcomes. |
| Methods | [10.1145/2601248.2601268](https://doi.org/10.1145/2601248.2601268) — Guidelines for snowballing in systematic literature studies and a replication in software engineering | Credited: Selected review-method guidance; not evidence of F#/C# outcomes. |
| Methods | [10.60692/568pm-64w28](https://doi.org/10.60692/568pm-64w28) — Successful combination of database search and snowballing for identification of primary studies in systematic literature studies | Not selected: Same-title hybrid-search deposit/version lead; not counted as another independent methods study. |
| Methods | [10.48550/arxiv.2307.02612](https://doi.org/10.48550/arxiv.2307.02612) — Successful Combination of Database Search and Snowballing for Identification of Primary Studies in Systematic Literature Studies | Not selected: Same-title hybrid-search deposit/version lead; not counted as another independent methods study. |
| Methods | [10.60692/kw4rm-ey461](https://doi.org/10.60692/kw4rm-ey461) — Successful combination of database search and snowballing for identification of primary studies in systematic literature studies | Not selected: Same-title hybrid-search deposit/version lead; not counted as another independent methods study. |
| Methods | [10.60692/1r4jg-nnz83](https://doi.org/10.60692/1r4jg-nnz83) — Successful combination of database search and snowballing for identification of primary studies in systematic literature studies | Not selected: Same-title hybrid-search deposit/version lead; not counted as another independent methods study. |
| Methods | [10.60692/q7f2y-sb224](https://doi.org/10.60692/q7f2y-sb224) — Successful combination of database search and snowballing for identification of primary studies in systematic literature studies | Not selected: Same-title hybrid-search deposit/version lead; not counted as another independent methods study. |

### Citation-neighborhood check

| Discovery | DOI / title | Decision / reason |
| --- | --- | --- |
| G incoming | [10.1007/11586012_16](https://doi.org/10.1007/11586012_16) — Improving the Software Inspection Process | Not selected: Citation-neighborhood lead; title-level triage only, not assessed as substantive support in this bounded audit. |
| G incoming | [10.1007/978-3-319-49094-6_1](https://doi.org/10.1007/978-3-319-49094-6_1) — The Relationship Between Software Process, Context and Outcome | Not selected: Citation-neighborhood lead; title-level triage only, not assessed as substantive support in this bounded audit. |
| G incoming | [10.1007/978-3-540-32179-8_5](https://doi.org/10.1007/978-3-540-32179-8_5) — Challenges and Recommendations when Increasing the Realism of Controlled Software Engineering Experiments | Not selected: Citation-neighborhood lead; title-level triage only, not assessed as substantive support in this bounded audit. |
| G incoming | [10.1007/978-3-540-75563-0_29](https://doi.org/10.1007/978-3-540-75563-0_29) — A Comparison of Two Approaches to Safety Analysis Based on Use Cases | Not selected: Citation-neighborhood lead; title-level triage only, not assessed as substantive support in this bounded audit. |
| G incoming | [10.1007/978-3-540-87875-9_50](https://doi.org/10.1007/978-3-540-87875-9_50) — Safety Hazard Identification by Misuse Cases: Experimental Comparison of Text and Diagrams | Not selected: Citation-neighborhood lead; title-level triage only, not assessed as substantive support in this bounded audit. |
| G incoming | [10.1007/978-3-642-01156-6_29](https://doi.org/10.1007/978-3-642-01156-6_29) — The industry is our lab — Organisation and Conduct of Empirical Studies in Software Engineering at Simula | Not selected: Citation-neighborhood lead; title-level triage only, not assessed as substantive support in this bounded audit. |
| G incoming | [10.1007/978-3-642-01156-6_30](https://doi.org/10.1007/978-3-642-01156-6_30) — A Series of Controlled Experiments on Software Maintenance | Not selected: Relevant human-maintenance synthesis lead; exact DOI lookup and body attempt returned no readable text. Unassessed, not negative evidence. |
| G incoming | [10.1007/978-3-642-16373-9_4](https://doi.org/10.1007/978-3-642-16373-9_4) — Information Use in Solving a Well-Structured IS Problem: The Roles of IS and Application Domain Knowledge | Not selected: Citation-neighborhood lead; title-level triage only, not assessed as substantive support in this bounded audit. |
| G incoming | [10.1007/978-3-642-16782-9_1](https://doi.org/10.1007/978-3-642-16782-9_1) — Comparing Two Techniques for Intrusion Visualization | Not selected: Citation-neighborhood lead; title-level triage only, not assessed as substantive support in this bounded audit. |
| G incoming | [10.1007/978-3-642-24485-8_13](https://doi.org/10.1007/978-3-642-24485-8_13) — Identifying the Weaknesses of UML Class Diagrams during Data Model Comprehension | Not selected: Citation-neighborhood lead; title-level triage only, not assessed as substantive support in this bounded audit. |
| G incoming | [10.1007/978-3-642-54092-9_3](https://doi.org/10.1007/978-3-642-54092-9_3) — An Experiment on Self-configuring Database Queries | Not selected: Citation-neighborhood lead; title-level triage only, not assessed as substantive support in this bounded audit. |
| G incoming | [10.1007/978-3-642-55128-4_26](https://doi.org/10.1007/978-3-642-55128-4_26) — An Exploration of Code Quality in FOSS Projects | Not selected: Citation-neighborhood lead; title-level triage only, not assessed as substantive support in this bounded audit. |
| G incoming | [10.1016/b978-0-12-804206-9.00006-4](https://doi.org/10.1016/b978-0-12-804206-9.00006-4) — Why theory matters | Not selected: Citation-neighborhood lead; title-level triage only, not assessed as substantive support in this bounded audit. |
| G incoming | [10.1016/j.jss.2009.09.017](https://doi.org/10.1016/j.jss.2009.09.017) — Identification of refactoring opportunities introducing polymorphism | Not selected: Citation-neighborhood lead; title-level triage only, not assessed as substantive support in this bounded audit. |
| G incoming | [10.1016/j.jss.2010.11.918](https://doi.org/10.1016/j.jss.2010.11.918) — Identifying Extract Class refactoring opportunities using structural and semantic cohesion measures | Not selected: Citation-neighborhood lead; title-level triage only, not assessed as substantive support in this bounded audit. |
| G incoming | [10.1049/sfw2.12010](https://doi.org/10.1049/sfw2.12010) — Automated class diagram elicitation using intermediate use case template | Not selected: Citation-neighborhood lead; title-level triage only, not assessed as substantive support in this bounded audit. |
| G seed | [10.1109/tse.2004.43](https://doi.org/10.1109/tse.2004.43) — Evaluating the effect of a delegated versus centralized control style on the maintainability of object-oriented software | Not selected: Previously retained human expertise study; seed only, no new result asserted here. |
| G incoming | [10.1142/s0218194016500431](https://doi.org/10.1142/s0218194016500431) — Software Maintainability: Systematic Literature Review and Current Trends | Not selected: Relevant review lead; only a truncated abstract was returned; not audited or used as substantive support. |
| G incoming | [10.1145/2430536.2430539](https://doi.org/10.1145/2430536.2430539) — Facilitating the transition from use case models to analysis models | Not selected: Citation-neighborhood lead; title-level triage only, not assessed as substantive support in this bounded audit. |
| G incoming | [10.1145/2699696](https://doi.org/10.1145/2699696) — Documenting Design-Pattern Instances | Not selected: Citation-neighborhood lead; title-level triage only, not assessed as substantive support in this bounded audit. |
| G incoming | [10.1145/2699697](https://doi.org/10.1145/2699697) — aToucan | Not selected: Citation-neighborhood lead; title-level triage only, not assessed as substantive support in this bounded audit. |
| G incoming | [10.1145/2970276.2970323](https://doi.org/10.1145/2970276.2970323) — Identifying domain elements from textual specifications | Not selected: Citation-neighborhood lead; title-level triage only, not assessed as substantive support in this bounded audit. |
| G incoming | [10.1287/isre.2014.0515](https://doi.org/10.1287/isre.2014.0515) — <b>Research Note</b>—How Semantics and Pragmatics Interact in Understanding Conceptual Models | Not selected: Citation-neighborhood lead; title-level triage only, not assessed as substantive support in this bounded audit. |
| G incoming | [10.4018/jdm.2017040102](https://doi.org/10.4018/jdm.2017040102) — Effects of Domain Familiarity on Conceptual Modeling Performance | Not selected: Citation-neighborhood lead; title-level triage only, not assessed as substantive support in this bounded audit. |
| G incoming | [10.4018/jismd.2013040102](https://doi.org/10.4018/jismd.2013040102) — Empirical Evaluation of Test Driven Modeling | Not selected: Citation-neighborhood lead; title-level triage only, not assessed as substantive support in this bounded audit. |
| G incoming | [10.5402/2012/259064](https://doi.org/10.5402/2012/259064) — Empirical Studies for the Assessment of the Effectiveness of Design Patterns in Migration between Software Architectures of Embedded Applications | Not selected: Citation-neighborhood lead; title-level triage only, not assessed as substantive support in this bounded audit. |

## Source audit, review and project boundary

Scite audit ID: `alf-literature-search-depth-audit-2026-09-14`.
The single decision submission accepted **8 credited / 100 excluded / 0 skipped**:
107 distinct DOI records and one failed web-access lead. There are eight
credited sources, not eight empirical maintenance studies. One page-duplicate
DOI is logged once in that audit and twice at its observed positions above.
The answer-scoped report was not truncated and reported no missing reasons
or unlinked retrievals. Provenance is 71 main-session Scite records, 36
worker-only Scite records explicitly labeled other/worker provenance, and
one web lead. A citation audit documents decisions; it does not certify search
coverage, scientific validity or PRISMA compliance.

The installed agent-deployment guidance kept the deeper LLM retrieval with one
read-only Luna Max worker while the main agent handled the independent
functional/OO search, primary-source verification and methodological synthesis.
This is AI extraction plus main-agent self-review, not independent human review.
The imported SUBAGENT_ROUTING.md path was absent; installed global guidance
and the agent-deployment skill supplied the available routing instructions.

Only this note, PLAN.md and the concise AGENTS.md pointer are changed.
The previous literature ledgers and original results remain intact. Three
changed documents passed strict UTF-8 and 81 relative file-link target checks;
108 inventory rows resolve to 107 distinct DOIs and eight credited sources.
The initial one-off row counter also matched the Methods query-summary row;
requiring a DOI-linked inventory row corrected the check without changing data.
Staged whitespace is checked before publication. These are path/count checks,
not external-link, model or candidate tests. Exact containing-commit CI must be checked after publication;
it is not inferred from the prior commit's green run or available at this
pre-publication writing checkpoint.

No workload, adapter, protocol, model roster, budget, context treatment, OAuth
staging, execution authorization or frozen result changed. The next experimental
decision remains human review of the existing maintenance construction. H flags
stay false and allocations zero. The immediate research limitation is unresolved
coverage and full-text assessment, not permission to execute.
