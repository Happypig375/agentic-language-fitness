# S129 — Documentation, declared types and the cost of reading

**Complete publication reading, 2026-10-01 HKT; printed-data reconstruction, no experimental reproduction.** Stefan Endrikat, Stefan Hanenberg, Romain Robbes and Andreas Stefik, *How Do API Documentation and Static Typing Affect API Usability?*, ICSE 2014, pp. 632–642. DOI [10.1145/2568225.2568299](https://doi.org/10.1145/2568225.2568299).

## Identity and coverage

Zotero parent `V9U5DEEL`, PDF `LFW2MH4J`, note `VIUS9E3I` preceded body reading. The selected library PDF has **eleven pages, 231,318 bytes**, SHA-256 `9d8a108275b97db5c02de319f7c0a8d9a4a845a8545e88cd5c7a44e47bdaf62f`. All eleven pages, six figures, seven tables and 34 references were read. The opening and PDF pp. 4–9 were visually inspected, including both code/documentation examples, allocation, raw table and all outcome plots. All 25 participant columns were reconstructed. The separately acquired institutional copy retains its earlier hash/edition boundary; complete equivalence was not asserted.

The live B02/B08/B10/B11/B12 questions concern alternative information, type/documentation interaction and full effort accounting. This is a separate factorial experiment, not S117/S126's shared dataset or S127's names-only treatment. No task code, six original German documentation files, tests, complete logs or videos were acquired or executed. Figure2 is explicitly an abridged translated example, not those original documents.

## Treatments, task and sample

The randomized 2×2 between-subject design crosses the authors' static/dynamic Dart conditions with presence/absence of external documentation. Declared type names are removed in the dynamic source. The paper specifies neither an exact Dart version nor a detailed checker invocation/configuration; it does not isolate declarations from checking as S127 does. Do not infer current Dart semantics or an independently verified diagnostic treatment from the labels alone.

Everyone receives a basic syntax-highlighting editor, source tree and test buttons on a single monitor. Full API source is available, with no comments/JavaDoc, and supplied tests are runnable but their source hidden. Development time runs from task delivery until all those tests pass. That endpoint is not a separately held-out behavioral oracle. The approximately 2,000-line API avoids standard-library objects and complex control flow, limiting variation in library knowledge.

The single measured task configures a delivery of a kitchen to a customer using the nearest suitable store and carrier. It entails finding/constructing/configuring API objects and can be solved without loops or conditionals. The task kind deliberately follows earlier cases favorable to static typing, while the authors also expect documentation to help. Other repair task families were considered but excluded. A warmup and unspecified pilot preceded the main study; pilot size/results and participant overlap are not given.

Documentation comprises six German ASCII files of one to six kilobytes each. Explanations and code examples include relevant and irrelevant API uses, with their placement randomized. Examples overlap solution operations but are not the exact solution. The authors say documentation is equivalent across typing groups and aim for good, accurate documentation; the original files were not available for independent equivalence/quality verification.

The analysis retains 25 male students aged 22–30, in at least their fifth semester, from Duisburg–Essen and Koblenz–Landau. Two other participants were removed—one machine crash made data unreadable and one nonnative German speaker reported incomplete understanding—and one dropped out. This implies 28 entrants, but excluded participants' assigned groups, outcomes and dropout reason are not supplied. Random assignment aimed at nearly balanced groups; retained cell sizes are 7/6/6/6. This is not an all-assigned outcome analysis.

Three retained attempts are unfinished and recorded at **11,460 seconds**: IDs8/20/23, all without documentation. Table2's stars and the first sentence of §4.1 agree; the next sentence mistakenly names13 rather than8 as the typed nonfinisher. Subject13 has an unstarred8,363 seconds. The planned maximum session duration is five hours, but the exact derivation of the 11,460-second task limit is not explained. These values are censored observations, not actual successful completion times.

## Reconstructed outcomes and measured documentation use

All 25 identities `coding time = development time − documentation-viewing time` hold exactly in the printed table. The following descriptives retain the three capped attempts and distinguish them from completions:

| Group | Retained / completed | Mean total seconds | Mean documentation-viewing seconds | Mean remainder seconds |
| --- | --- | --- | --- | --- |
| Typed, documentation | 7 / 7 | 3,860.00 | 626.14 | 3,233.86 |
| Typed, no documentation | 6 / 5 | 7,051.67 | 0 | 7,051.67 |
| Untyped, documentation | 6 / 6 | 8,193.67 | 1,515.33 | 6,678.33 |
| Untyped, no documentation | 6 / 4 | 8,782.50 | 0 | 8,782.50 |

The typed/documented cell has the lowest mean. All thirteen documentation recipients access it, with30–175 switches and338–1,901 seconds viewing it. Their mean individual viewing/total ratio is18.76%; group-specific means are18.56% and18.99%. The paper's15–23% and12–22-minute intervals concern pooled mean estimates, not bounds covering each participant. Viewing includes searching, reading, understanding and thinking. It establishes use, not accurate comprehension or usefulness by itself; the authors acknowledge that distinction.

All thirteen documented attempts finish, compared with nine of twelve undocumented attempts. This is a favorable descriptive success pattern, not a separately established causal correctness effect; exclusions, small cell sizes, time limits and the supplied-test endpoint remain relevant.

## Total time, subtraction and interaction

For total development time, the author-reported two-factor ANOVA favors typing (p=.007, partial eta-squared .30). Documentation is inconclusive at the conventional .05 threshold (p=.075, .14), and the interaction is nonsignificant (p=.211). Marginal t-test summaries give a typing advantage interval of912–5,353 seconds and a documentation advantage interval of−391–4,496 seconds. The latter permits both a small disadvantage and a substantial advantage; it is not evidence of no documentation benefit.

Variance homogeneity fails the Levene check (p<.034). The authors state that nonparametric checks confirm the findings but give no corresponding statistics or complete procedure. Marginal t-tests are also reported. These are reported analyses, not independently rerun models; the treatment of unfinished attempts as if they completed at the limit further constrains their estimand.

For the remainder called coding time, both typing (ANOVA p=.018) and documentation (p=.008) favor shorter values, with interaction still nonsignificant (p=.426). The corresponding reported intervals are323–5,082 seconds for typing and810–5,386 for documentation. This supports a difference in an observed time component under the assigned conditions.

**Subtracting viewing time does not identify prior comprehension.** The remaining interval still includes code reading, search, tests, thinking and other actions; it is not pure typing/editing effort. Removing a post-assignment time component does not recreate the unobserved session of a developer who already knows the documentation. Earlier reading may change later behavior, and reuse across future tasks was not observed. For B11's information-cost question, the whole task cost remains consequential; an amortized-documentation claim requires a stated reuse population and actual longitudinal evidence.

**Reinforcement is a descriptive hypothesis, not an established interaction.** Mean documentation-associated reductions are3,191.67 seconds in typed groups versus588.83 in untyped groups. That describes the sample's difference of differences, but the reported interaction p=.211 does not substantiate the abstract/conclusion's stronger claim that documentation and typing reinforce each other. It also does not prove their effects independent or equivalent. A significant typing main effect is not a demonstration of a significant simple effect in each documentation stratum.

## Exploratory navigation and transfer

File-switch means are313.57/616.67/614.50/646.67 for groups1–4. The file-switch ANOVA's typing/documentation results are p=.067/.064, with interaction p=.129. After subtracting switches into documentation, the reported code-switch result favors documentation (p=.007), while typing (p=.143) and interaction (p=.256) are nonsignificant. Proxy definitions therefore matter. These observational outcomes do not identify the mediator of the total-time benefit.

The paper describes fewer documentation visits later in sessions, more tests in dynamically typed conditions and mostly relevant source viewing. It supplies no raw half-session or test-launch table sufficient to reconstruct these statements. The proposed faster API learning remains an explanation for future investigation. The authors explicitly note that fewer files could instead move effort to scrolling; a file-switch count cannot be equated with information volume, agent context or useful knowledge.

S117/S126, S127, S128 and S129 jointly support bounded human API/type-information benefits under several settings, with selected adverse/null results retained. They do not isolate the incremental checker effect, establish representative task frequencies, or assign explicit-current-case versus catch-all evolution. The same research lineage, related task construction and incomplete source packages also limit claims of independent broad replication.

Next use the already identified Prechelt–Tichy checking comparison and dynamically favorable task-design studies to challenge this API-centered evidence, while returning to C02's actual coverage/extensibility methods. Documentation accuracy/evolution, knowledge-pushing, UML and professional API-learning sources in the bibliography remain conditional when their distinct practice or cost claims matter; their effects are not credited from this paper's summaries. S121/S122's accessible coordination lineage remains open across the wider survey.

**Unique:** unresolved; typing, source information and documentation already have direct empirical comparisons. **Valuable:** a selected task's favorable typing result and documented-completion pattern are concrete; net general benefit, reuse and Nu/agent transfer remain unmeasured. **Scientifically valid:** allocation, printed identities and censoring are reconstructed; interaction, prior-learning counterfactual, navigation causality and original apparatus remain unresolved. ISE feasibility and all experimental holds are unchanged.
