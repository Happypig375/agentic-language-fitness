# Nu form factors: practitioner claims, research mechanisms and reading leads

**Date:** 2026-09-14. **ALF basis:** `ec2226e50b6a2de11e7cb2e2f2d7cd0d1d27dbd1`. Requested before a later agent retrieves the PDFs. Read with [PLAN.md](../PLAN.md), the [full-paper handoff](full-paper-reading-handoff-2026-09-14.md) and this pass's [discovery ledger](nu-form-factors-discovery-ledger-2026-09-14.md).

**Status:** practitioner-source reading, paginated literature discovery and selected HTML/body inspection. Not completion of the full-PDF assignment, human review, a new systematic review, or authorization for A0, candidate calls, PDF redistribution or a new harness. No paper below is marked fully read in this pass. Existing results and the eleven core paper IDs remain unchanged.

## 1. What the Nu sources actually motivate

The [Nu FAQ](https://github.com/bryanedds/Nu/wiki/Frequently-Asked-Questions), in the returned revision dated March 23, 2026, warns against gratuitous abstraction and prioritizes domain suitability over maximal type safety. It describes concrete MMCC hazards: conflicting model updates, parent/child ownership, and repeated content evaluation under event fan-out. These are author-documented design constraints, not controlled comparative findings.

The [API selection guide](https://github.com/bryanedds/Nu/wiki/Choosing-Between-ImSim-and-MMCC-For-Your-Game), returned revision January 14, 2026, presents a trade-off between proximity of related code and temporal coupling. The [ImSim article](https://vsynchronicity.wordpress.com/2024/11/18/immediate-mode-all-the-things-with-nu-game-engine/) demonstrates a scoped-identity, declarative alternative to MMCC, not an opposition between functional and nonfunctional programming. Article publication is November 18, 2024; the displayed update is July 1, 2025.

The technical sections of [nu-chat-analysis](https://github.com/Happypig375/nu-chat-analysis/blob/59f2bdee94575a087eda6b5278dcafdd68084a46/analysis/derived/bryanedds-nu-synthesis/report.md) reinforce a domain-first interpretation. That document is a derived AI synthesis: follow its underlying source records before asserting implementation details. It is not independent corroboration of the FAQ or a controlled maintenance study. Current pinned executable source outranks old chat and generated reports.

The blog's September 7, 2026 simplicity article was visible through a search excerpt but could not be opened in this pass. Its linked FAQ addition was not in the returned FAQ revision. Do not combine the cached pages into an invented latest version. The homepage also contains explicitly simulated expert dialogues; these are not interviews, endorsements or independent evidence from the named people. This pass excludes those attributed statements from scientific support.

## 2. Refine the hypothesis without another wholesale pivot

The promising hypothesis is **appropriate factoring of responsibility**, not more abstractions, more static guarantees, fewer characters or an automatically superior language.

Three mechanisms must remain distinguishable:

1. **Representation size:** how much of the selected source/interface bundle occupies a request.
2. **Reasoning locality:** which ownership, ordering and interaction facts have to be recovered and kept consistent for this particular change.
3. **Programming-system support:** which details an already implemented runtime, compiler, inspector or repair policy supplies reliably instead of asking the agent to reimplement or infer them.

A program can be short but require many implicit assumptions. A longer program can expose a stable contract that makes most implementations unnecessary for a change. Moving responsibility into an engine does not eliminate it: record the editable boundary and whether the task changes application logic, engine contracts or the hidden implementation. Conversely, charging an application task for understanding an entire immutable library is not automatically fair.

**Lexical locality is not semantic locality.** Adjacent statements can still depend on a delicate execution order. Dispersed functions can implement a simple, explicit protocol. Which is easier depends on the change and available navigation tools. Do not define the preferred treatment using low file counts, short functions or a static metric and then use that same metric as proof of its advantage.

The original language/context motivation is retained, but neither Nu documentation nor this search proves an F# advantage for agents. Existing F# size counterexamples remain valid. A claim about human comprehensibility is not automatically a claim about a model's representations or training familiarity.

## 3. Source-inspired scenario questions for the later A0 review

These are proposed discriminators, not implemented changes or predictions already validated on Nu. A future authorized A0 must bind them to its exact source, runtime and requirements. At most two witnesses per package remains the existing cap; the table is a selection menu, not four new required tasks.

| Candidate change demand | Question to predict before implementation | Rival or adverse case to preserve |
| --- | --- | --- |
| Parent/child state ownership or reversible gameplay transition | Does an explicit owner localize the change and prevent conflicting updates? | A locally natural child update may violate the actual ownership protocol; stronger architecture can impose more obligations. |
| Dynamic identity, lifecycle or declaration-order change | Does nearby declaration/interaction code reduce coordination, or does order sensitivity create mistakes? | A reference implementation can accidentally make one ordering appear uniquely correct; score behavior and declared lifecycle rules. |
| Burst events needing one coherent transition | Does batch processing preserve semantics without broad coordination? | Physics scheduling, diffing and event volume may dominate; this may be a runtime/API comparison rather than an architectural one. |
| Change spanning a domain rule and an effect boundary | Can the rule be modified without duplicating or leaking it into unrelated handlers? | A compact helper may merely conceal a special-case implementation; track the responsibility actually changed. |

For each selected witness, add to the existing prediction card: information the agent must recover; temporal constraints; state owner; what is delegated to the runtime/compiler; and the tool access required to observe these facts. Retain uncertainty and the counterexample where the other package may be easier. Match requirements, not resulting patch size or navigation count.

Capabilities shared by both Nu styles cannot explain a difference between them. In particular, a shared engine facility should not be claimed as an MMCC-only benefit without pinned-source evidence. Similarly, a no-tools/no-feedback candidate cannot demonstrate the practical benefit of an interactive inspector, hot reload or gameplay undo. Keep source organization and interactive workflow claims separate; do not add those facilities silently to the primary policy.

## 4. Literature that changes the reading questions

### A. A framework for programming systems, not a quality score

*Technical Dimensions of Programming Systems* (`10.22152/programming-journal.org/2023/7/13`) explicitly distinguishes language notation from the broader development system. The authors' [HTML presentation](https://tomasp.net/techdims/) treats its dimensions as trade-offs, not universally good/bad endpoints; it also distinguishes reusable factoring from automation. This is a conceptual vocabulary, not causal evidence that a particular design improves maintenance.

Together with Green and Petre's Cognitive Dimensions (`10.1006/jvlc.1996.0009`, metadata checked, full paper pending), it suggests describing visibility, hidden dependencies, resistance to change, domain mapping and available feedback. Do not transplant human cognitive labels into a model score. Define observable task/trajectory evidence instead, then test whether it supports the proposed mechanism.

### B. Human reactive-programming findings are mixed by API and measurement

The [authors' publication abstract](https://www.rescala-lang.com/publications) for `10.1109/TSE.2017.2655524` reports a human comprehension comparison of reactive programs and Observer-style code. This is a reason to investigate organization, not a result about LLMs or Nu.

For RxJS/Bacon.js, `10.1002/spe.3435` uses structural metrics and human tasks/questionnaires. Its [publisher abstract](https://onlinelibrary.wiley.com/doi/10.1002/spe.3435) reports that metric and task-completion advantages do not coincide. The first 8,000 characters of scite's 161,620-character body were read; the rest and the PDF were not. Recover the full methods before transferring any effect or sampling claim.

The [readability-metrics case](https://arxiv.org/abs/2110.15246), `10.48550/arXiv.2110.15246`, is a useful caution about proxy validity. A scite graph tagged its citation of the human comprehension study as contrasting, but it evaluates static metrics on a refactored project, not a direct human replication. Do not report the label as refutation of the human study.

### C. A newly recovered close predecessor: Theory of Code Space

`10.48550/arXiv.2603.00601`, [v4 HTML](https://arxiv.org/html/2603.00601v4), studies architectural-map construction under partial observability. Selected sections 3, 6.5 and 7 were read. Its evaluated scope is Construct; later revision/use are described separately. It explicitly identifies map-reporting and prompt effects. Therefore graph-report accuracy is not transparent access to internal understanding, and asking for repeated maps can change the treatment.

**Reading consequence:** this work must be assessed before broad architecture-understanding, map-measurement or active/passive novelty claims. In ALF, behavioral change outcomes should remain distinct from auxiliary self-reports. A belief probe that spends tokens, supplies a scratchpad or changes attention is not neutral just because it is exempt from an action counter. Do not copy neutral filenames, planted constraints or a one-action-per-file budget without checking their workload implications. The paper's small synthetic scope also must not be generalized into a result about real inherited maintenance.

### D. A close planning/control predecessor: CodePlan

`10.1145/3643757` is the 2024 publication; `10.48550/arXiv.2309.12499` is a related preprint, not another independent study. The [2024 author page](https://www.microsoft.com/en-us/research/publication/codeplan-repository-level-coding-using-llms-and-planning-2/) describes incremental dependencies, may-impact analysis and planned multi-location edits. The earlier [2023 page](https://www.microsoft.com/en-us/research/publication/codeplan-repository-level-coding-using-llms-and-planning/) reports a different evaluation count. Use the chosen edition, not mixed results. Only author abstracts/metadata were checked here.

**Reading consequence:** supplying and maintaining a dependency plan is established prior art. The remaining ALF question is whether a credible application's organization reduces the recovery/coordination burden under declared support, not whether a dependency-aware controller can ever help. A future controller-provided map is an information intervention and its cost/quality must be recorded.

### E. The tool-by-abstraction interaction has an empirical predecessor

`10.1109/ICSE48619.2023.00058`, *Does the Stream API Benefit from Special Debugging Facilities?*, directly names a loops/streams and debugger comparison. Only identity was verified through scite and the publisher listing; **no direction or magnitude of its result is claimed**. It is a targeted future full-reading lead for any argument that abstraction benefits appear only with suitable tooling. Human debugging results still require separate validation for model-based repair.

## 5. Changes to the later reading assignment

Keep P01–P11 and their actual unread/partially read status. The handoff already permits promotion of a decisive close source. Record two **gap-critical additions** without renumbering or duplicating the existing queue:

| Addition | DOI | Full-reading purpose |
| --- | --- | --- |
| P12 — Theory of Code Space | `10.48550/arXiv.2603.00601` | Start from the reviewed v4 and verify current history. Reconstruct evaluated versus roadmap capabilities, synthetic construction, probing interventions, scoring/alternative answers and evidence for downstream utility. |
| P13 — CodePlan | `10.1145/3643757` | Prefer the publication, with `10.48550/arXiv.2309.12499` retained as a lineage/access lead. Reconstruct plan/dependency updates, available tools, validity checks, task scope and baseline information. |

These two are additional full-read targets before completing the gap reconstruction, not papers already read in full. Continue accessible original Batch A while acquiring them. Promote only the following mechanism-specific readings when their associated claim is actually retained:

| Conditional DOI | Trigger |
| --- | --- |
| `10.22152/programming-journal.org/2023/7/13` | Operationalizing the programming-system/form-factor description. Author HTML can guide questions, but is not the later full-PDF coverage record. |
| `10.1006/jvlc.1996.0009` | Using Cognitive Dimensions to justify specific task/notation measures. |
| `10.1109/TSE.2017.2655524` and `10.1002/spe.3435` | Transferring reactive-comprehension or API-usability claims; read together to retain their different populations and measures. |
| `10.1109/ICSE48619.2023.00058` | Proposing an abstraction × debugging/repair-tool interaction. |

Read the metric counterpoint `10.48550/arXiv.2110.15246` before relying on metric-based reactive-programming superiority or disagreement. The existing conditional Functional UI paper remains in the prior handoff. Other discovered papers stay deferred with a reason; do not make all 108 retrieved identities another mandatory queue.

## 6. What the PDF reconstruction should now deliver

Add a small practitioner-claim table to the existing synthesis, not a second parallel workflow. For each claim record: exact source/version; mechanism; scope and rival; closest empirical or conceptual evidence; what the full paper identifies; and what ALF would have to observe to test the transfer.

The full reader must specifically decide:

- Whether the architecture case's value survives the ToCS/CodePlan overlap, and whether it needs a narrower question or a reuse/replication framing.
- Whether organization is being measured through future correctness or merely through conformity, size and an elicited map.
- Which information is implicit, compiler/runtime-provided, or actually retrieved, and which policy makes it visible.
- Whether any claimed tool benefit is available in the candidate's allowed interface. Keep source-only, interactive and insulated-repair policies distinct.
- Which source-inspired predictions remain credible after reading the complete methods and limitations. Revise claims and controls, not historical outcomes or preferred-language selection.

This is still **read -> reconstruct -> revise -> return for review**, not read -> automatically implement A0 or add a worker. The active no-repair policy is not changed here. A stronger interactive claim can be deferred without forcing a new factorial or delaying the bounded source-package question indefinitely.

## 7. Provenance and present scope

The current pass read Nu wiki/blog prose, technical portions of the pinned derived archive, selected primary HTML, one scite body prefix, metadata and citation contexts. It used 20-item search limits and paginated both broad queries beyond their first pages. The exact search/graph/identity ledger follows separately. No PDF was retrieved or certified fully read, no Nu runtime was executed, no experiment was authorized, and no scorer, source target, allocation or backend was changed.
