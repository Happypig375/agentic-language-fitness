# S199 — Live documentation of design-pattern instances

**Complete publication reading, 2026-10-02 HKT.** Filipe Lemos, Filipe F. Correia, Ademar Aguiar and Paulo G. G. Queiroz, *Live software documentation of design pattern instances*, PeerJ Computer Science 10:e2090, 16 August 2024, DOI [10.7717/peerj-cs.2090](https://doi.org/10.7717/peerj-cs.2090). Reader: the main Codex AI session. All **40 pages** were consumed as text, including the references; **29 pages** were visually inspected: page 1 and pages 7–34. This covers **all seventeen figures and six tables**. No appendix is present. This is a full publication reconstruction with a bounded, separately specified [artifact/data check](S199-live-pattern-artifact-check.md), not execution of the plugin, SPSS, participant tasks or an independent replication.

The existing native Zotero record preceded reading: parent `VCVMUNHF`, note `375RVXDV`, user-attached PDF `ZI4QFK6X`; **11,345,128 bytes**, SHA-256 **`95d72a0cb7bb0381c679caf6b47e6b1abdff653e356244fb1025ca9027da312e`**. The PDF has no recorded acquisition URL. Its opening page confirms the published title, four authors, date and DOI. Original memberships `PKLXQNEE`, `MBYQJXUF` and `NDU9BTP7` are preserved. The [publisher](https://peerj.com/articles/cs-2090/) and [PMC record](https://pmc.ncbi.nlm.nih.gov/articles/PMC11419627/) are alternate locators, not additional studies or newly completed HTML readings.

## Positive result and its scope

Twenty-one master's students performed small, prepared Java tasks. The eleven using DesignPatternDoc generally finished faster and consulted external documents less than the ten using IntelliJ with equivalent prepared pattern information in PDFs and manually drawn diagrams. Released task times reproduce approximately **62% less time on the three comprehension subtasks** and **53% less time across all six subtasks**. The implementation-only Command task has a null result and a slightly slower experimental mean. These are useful positive and null outcomes for this tool comparison.

The treatment combines automatic pattern detection, diagram generation, information inside the editor, updating feedback and a brief tutorial. The control requires external lookup and manual drawing. Consequently, the result does not isolate immediate feedback from automation, presentation or location. The authors acknowledge this bundle and propose stronger comparisons. Long-term documentation consistency, onboarding/installation effort, professional productivity and semantic correctness after future program changes were not measured.

## Mechanism and preparation — pp.1–20

The background distinguishes several degrees of liveness and surveys design-pattern documentation/detection tools. Its searches cover October 2019–January 2020 and an October 2023 update using IEEE/Google Scholar and stated English-language/topic criteria. Tables 1–2 summarize ten approaches and forty tools. These are the authors' review, not forty primary papers independently read here; this search description does not establish exhaustive field recall.

DesignPatternDoc is an IntelliJ Java plugin. DP-CORE supplies static detection for **Abstract Factory, Bridge, Builder, Command, Observer and Visitor**. Detection runs every few seconds or when typing stops. The authors report that DP-CORE was the candidate detector they could successfully run. That is a concrete integration constraint; the assertion that a machine capable of running the IDE can run the plugin efficiently is not a latency or scaling benchmark.

Detected instances first enter a volatile store. A developer accepts an instance before it becomes persistent documentation, can ignore a suggestion, or can document an instance manually. Accepted instances are kept in IntelliJ XML configuration suitable for version control. The design explicitly calls for concurrent access to the accepted store. The model separates pattern definitions, roles and links from instances, intents and participating program elements.

The user sees inline role hints, a diagram on hover, and a panel beside the editor. Renaming is reflected in documented participants and can be undone. Missing roles produce warnings with edit/delete quick fixes. PlantUML supplies diagrams. The public plugin README adds a Graphviz dependency for full UML rendering. Defining another pattern manually does **not** automatically extend DP-CORE's detector. Prepared examples, supported language/patterns and accepted metadata therefore matter to the observed experience.

The paper variously describes its system as level 4 and as levels 4/5, while later placing level 5 in future work. The reconstructed features above are firmer evidence than assigning it an unambiguous validated level-5 label. None of these levels implies execution of a live program world, migration of state or checking external/temporal effects.

Role coverage is a structural aid, not a behavioral oracle. A complete-looking Command instance may still fail to wire or invoke the intended action. Likewise, accepting a detected pattern does not prove that the detector's interpretation matches the program's intent. The prototype's source repository was located and its README read; implementation files, detector accuracy and exact correspondence to the study build were not independently inspected or executed.

## Experiment — pp.20–29 and released protocols

The participants were twenty-one Porto MIEIC/MESW master's students with prior pattern experience. The paper reports random assignment to ten control and eleven experimental participants, but does not describe the randomization procedure. Three pilots are separate. Similar background-question means describe this small sample; they do not establish equal ability.

Sessions used a **preconfigured remote IntelliJ environment**, approximately fifty minutes overall: background questions, a two-minute experimental-group tutorial, approximately forty-five minutes of tasks and a final questionnaire. Both groups received a GoF reference card. Control participants received PDFs containing the prepared pattern information and used draw.io for diagrams; experimental participants used the plugin. Installation/setup time is outside the comparison.

| Scenario | Identification/planning subtask | Follow-up subtask |
| --- | --- | --- |
| Observer | T11: identify the pattern in a news-notification example | T12: document it with a UML diagram |
| Command | T21: find the missing participant in a light-control example | T22: implement the missing behavior |
| Abstract Factory | T31: recognize the design and plan adding Giraffe | T32: implement **and document** the extension |

The paper occasionally says four tasks, but the released instructions and data specify these **three scenarios and six subtasks**. T32 cannot be interpreted as pure documentation time. The study's researcher observed remotely, timed subtasks, counted documentation accesses and used think-aloud. At completion, the researcher checked submitted code/diagrams and gave correctness feedback; this actual control must not be erased by saying that no correctness check occurred. The process was unblinded and permitted reaching a working solution.

External-document accesses were counted when participants left the IDE for the supplied documents/reference and returned. Experimental internal accesses include features such as hover/editor suggestions. These categories have different interaction costs; their counts are not a common unit of attention or mental context switching. The authors report losing submitted participant code and diagrams after analysis because of a logistical mistake. Therefore the released package does not permit independent re-scoring of those outcomes today.

The released control questionnaire has a draw.io-familiarity item absent from the five-background-variable analysis table. The experimental questionnaire additionally asks fifteen feature-specific questions absent from the main three final-question variables. Those instrument/reporting differences are retained as limits; individual response bodies and identifying fields were not read or reproduced here.

## Results retained, with the released numbers checked

The following are **own descriptive calculations** from the released 21-row numerical table. Means are seconds; reductions compare experimental with control means. They are not new participant observations, re-executed SPSS results or confidence intervals.

| Subtask | Control mean, n=10 | Experimental mean, n=11 | Experimental change |
| --- | ---: | ---: | ---: |
| T11, identify Observer | 585.80 | 117.27 | 79.98% less time |
| T12, document Observer | 325.50 | 55.55 | 82.94% less time |
| T21, identify missing Command role | 211.80 | 114.91 | 45.75% less time |
| T22, implement Command behavior | 475.30 | 483.91 | **1.81% more time** |
| T31, identify/plan factory extension | 468.50 | 243.09 | 48.11% less time |
| T32, implement/document factory extension | 462.20 | 163.27 | 64.67% less time |
| Sum of all six | 2,529.10 | 1,178.00 | **53.42% less time** |

The authors report statistically favorable timing for five subtasks and no significant difference for T22. The small T22 difference is not an equivalence result. They regard that task as poorly aligned with the plugin's assistance; it remains an informative boundary rather than a reason to discard the observation. The comprehension sum T11+T21+T31 is 1,266.10 versus 475.27 seconds, reproducing the approximately 62% claim. T12+T32 is 787.70 versus 218.82 seconds, but calling that a documentation-only effect would erase T32's implementation component.

Several reporting discrepancies can be located without replacing the positive result with a catalogue of faults:

- The prose assigns **468→243 seconds /48%** to T32, but those are the T31 values. The table and released data give **462→163 seconds /64.67%** for T32. Both comparisons remain favorable.
- The advertised **89% reduction** in external accesses uses **46 versus 5** accesses for T11, rather than totals across tasks, and does not normalize the unequal group sizes. Across all tasks, mean external accesses are **24.10 versus 4.55**, an **81.14%** reduction per participant. Experimental internal accesses average **18**; much activity moves inside the IDE rather than disappearing. Adding differently defined internal/external events does not produce a validated cognitive-cost metric.
- The printed spread columns reproduce **standard errors**, rather than standard deviations, to rounding precision. This distinction matters when interpreting variability.
- The prose's rank-test task list differs from the table and released syntax: the latter use T11, T12 and T32, while T22 is analyzed with a t-test. The twelve reported Mann–Whitney “r” values closely match **z²/N**, rather than the usual **|z|/√N**. The [artifact check](S199-live-pattern-artifact-check.md) states the arithmetic and its limits; no exact p-values were regenerated.
- Final Q1/Q2 ratings favor the experimental group, consistent with the reported ease of understanding/using patterns, while a hypothesis-direction label in the table/text points the other way. Q3 has no declared significant difference; that is not proof that remote delivery had no effect.

## Artifact lineage and remaining method limits

The [versioned study package](https://zenodo.org/records/10849702), DOI **10.5281/zenodo.10849702**, is v1.0, published 21 March 2024, with concept DOI **10.5281/zenodo.10849701**. These identify one release lineage, not two datasets. The GitHub v1.0 tag resolves to `a81f66b6324dcf3c65b467bc9be9b07e9d08023d`. The ZIP is **2,713,128 bytes**, SHA-256 **`6e724fe2185e9cd4a917afe3ef1810cb3a6bfcad2503c1e13ddfc3b2642fca71`**, MD5 `b7d64042ddbb4912a567e9b8cc63dc94`, matching Zenodo. It is preserved as native attachment `9F3DW85F`, version 4753. Archive member timestamps are in May 2022; package publication, study timing and plugin implementation version are distinct.

The bounded check consumed the README, SPSS syntax, numerical CSV, all seventeen Java starter files, both participant protocols and the prepared Command diagram. XML was structurally parsed with selected sections read. Raw response CSVs were inspected only for headers/counts; the reference-card body and SAV file were not read. See the separate check for exact page coverage and hashes. No plugin build, installation, task execution or author statistical program was run.

The starter tasks make the contrast concrete. T22 requires a concrete command plus its wiring, not merely adding a label to a diagram. The factory example includes a valid Pig fallback; adding Giraffe does not inherently require eliminating it. That is an observed task property, **not** an explicit-enumeration versus catch-all experiment. The paper's fully qualified participant-name description and the released XML's simple names also leave implementation/version correspondence unproved, rather than demonstrating an executed defect.

For B08/B10, S199 connects visible design information to favorable short-task outcomes under a prepared tool bundle, with a useful implementation-only null. It leaves detector false positives, large-project responsiveness, notification burden, integration/training cost, long-term maintenance and professional adoption unresolved. For B01/B02/B04/B09, structural warnings and immediate visual updates remain distinct from desired successor behavior, live-state compatibility and temporal correctness. Nothing here establishes a Nu, F#/C# or fixed-agent D1 advantage.

The bounded follow-on search finds three other citing works after removing a seed self-loop, not three independent replications. A primary abstract for Infragenie supplies a consequential maintainer-rating follow-up; DP-LARA supplies a detector-method lead. Their bodies are unread. Read the already acquired original S194 modularity replication next to settle allocation, ability and outcome handling, while retaining those practice and positive concern/defect paths. The broader survey and experimental holds remain in force.
