# S127 — Type names without checking: useful information and misleading information

**Complete publication reading, 2026-10-01 HKT; printed-data reconstruction, no experimental reproduction.** Samuel Spiza and Stefan Hanenberg, *Type Names without Static Type Checking already Improve the Usability of APIs (As Long as the Type Names are Correct): An Empirical Study*, Modularity 2014, pp. 99–108. DOI [10.1145/2577080.2577098](https://doi.org/10.1145/2577080.2577098).

## Identity and coverage

Zotero parent `A5IQHAYH`, PDF `9UFFAUQS`, note `5QEJ8NXI` existed before body reading. The library PDF has **ten pages, 480,715 bytes**, SHA-256 `85b88a06f983bacca47063cf7abe4407e63a40f290c9460b82c9aba75b81dab1`. All ten pages, five figures, four tables and 28 references were read. The opening and PDF pp. 4–8 were visually inspected, including both complete code figures, design allocation, boxplots, interaction plots and raw table. Every printed participant row in Table 2 was reconstructed. No source/test/interaction-log archive was acquired or executed.

The live B02/B10/B12 question is whether source-level type information helps separately from automatic checking, and what incorrect information costs. S117/S126 combine those mechanisms. S127 changes the information available within one language, but has no checker-enabled arm and does not assign D1's exhaustive-versus-fallback convention.

## Intervention, tasks and participants

The study uses the then-current Dart facility for optional type names while omitting automatic type checks. Its finding concerns that historical configuration, not modern Dart semantics. Both treatments use a Java-like subset; advanced Dart features are excluded. A basic Emperior editor supplies syntax highlighting, a source tree and runnable tests, without ordinary IDE completion/navigation facilities. Each task stops when the supplied hidden-source tests pass; those tests check the constructed object structure. Their pass is assumed to mean correctness, without an independent held-out behavior check.

Twenty volunteer undergraduates in at least their fifth semester were randomly split into two groups of ten. Tasks 1–3 use both type-names (TN) and no-type-names (No TN) conditions, with opposite condition orders and structurally renamed game/car-insurance domains. Renaming reduces direct repetition but does not remove task-dependent carryover. The paper does not establish a separately crossed domain/treatment allocation beyond the described two sequences. The implementation and Ubuntu 11.04 boot image ran on ThinkPad R60 machines with 1 GB RAM, over a month.

The three API-construction tasks are modified **CIT3–5 from S117**, deliberately chosen because they had shown comparatively large favorable effects for static typing. That supports a targeted mechanism probe on responsive tasks; it does not estimate the prevalence or average benefit of arbitrary development work. The API requires finding and constructing several objects, without loops or conditionals. The authors changed the former email domain to car insurance and altered tasks to reduce the risk from a participant already knowing the previous publication.

Task 4 supplies faulty car-insurance code and compares an incorrect type name with no type name **between subjects only**. The call passes a `ThirdParty` where the intended argument is its `getPaymentHandling()` result, while the faulty declaration misleadingly requests `ThirdParty`. The task begins with the faulty program, avoiding time spent constructing it. Three participants leave before this task: IDs 1/14/17. The printed groups retain nine No TN and eight TN participants. Reasons for those departures are not given.

Every task has a forty-minute limit. Unfinished attempts receive **2,400 seconds**, even though actual completion would take longer. These are capped measurements, not observed completion times for every participant. All assigned tasks 1–3 remain in the table; task 4 has explicit missing participants. Its different task kind, design and retained sample prevent treating the two task sets as a clean factorial test of information correctness.

## Reconstructed outcomes

Table 2 contains twenty rows, 120 measurements for tasks 1–3 and seventeen for task 4. All forty per-condition sums and twenty differences match their constituent entries exactly. Descriptive means and medians below use the printed, capped measurements.

| Outcome | Type names | No type names | Boundary |
| --- | --- | --- | --- |
| Task 1 mean / median seconds | 1,045.95 / 894 | 1,681.05 / 1,630 | Two participants are slower with names; one is tied at the cap. |
| Task 2 mean / median seconds | 750.70 / 597.5 | 995.20 / 840.5 | Nine of ten TN-first participants are slower with names; all ten No-TN-first participants are faster with names. |
| Task 3 mean / median seconds | 1,007.55 / 832 | 1,243.35 / 1,134 | Five participants are slower with names. |
| Sum of tasks 1–3, mean seconds | 2,804.20 | 3,919.60 | Four participants have a higher TN sum, all TN-first. |
| Task 4 mean / median seconds | 1,025.625 / 811, n=8 | 364 / 351, n=9 | Incorrect names are adverse; one TN attempt reaches the cap. |

Tasks 1–3 contain **eight capped attempts across six people**, seven No TN and one TN. Table 2 identifies IDs 1/2/5/9/14/17; subjects 2 and 17 each have two capped attempts. The prose's “eight subjects” confuses attempts with participants. Its Task 1 statement that subject 17 is slower also conflicts with the printed 2,400/2,400 tie. These corrections preserve the substantial favorable timing pattern and do not convert capped values into completed solutions.

For Task 4, the fastest TN participant takes 536 seconds and is faster only than the slowest No TN participant at 562 seconds. The remaining TN values exceed the No TN range. The paper reports a Mann–Whitney result of p<.001. This is a strong adverse pattern on this one selected repair, with one capped observation and three absent participants; neither natural frequency of wrong annotations nor total real-project cost is measured.

## Statistical claims and mechanism limits

The authors' per-round repeated-measures ANOVA uses task as a within-subject factor and type information as a between-subject factor. The reported type-information result is p=.15 in round 1 and p<.01 in round 2; reported partial eta-squared values are .11 and .33. Task and interaction results motivate further taskwise testing. The latter includes between-group Mann–Whitney tests, order-specific paired Wilcoxon tests and a pooled paired analysis. These reported tests were not independently rerun; no general multiplicity adjustment or censoring model is given.

The pooled paired analysis favors names for tasks 1 and 3 (p<.05), while task 2 is inconclusive (p>.2). In task 2 each order group favors its second exposure. This is consistent with material carryover but does not identify an exact learning effect. Separate significance classifications also do not establish equivalence in the nonsignificant cells. Correct type information has a bounded observed benefit; it is not a benefit for every participant, task or first encounter.

The authors infer that the effect of names is weaker than names plus checking in S117. That is a **cross-study interpretation**, not a randomized incremental-checker estimate: language, modified tasks, domains, cohort and runtime messages differ. The deliberately selected favorable predecessor tasks further limit a general comparison. A checker-enabled same-task arm would be needed to identify that incremental treatment here.

For wrong names, the proposed explanation—that people trust the declaration and search in the wrong classes—is explicitly speculation, without a measured navigation mechanism. A checker enforcing declared relationships may expose this particular inconsistency; type consistency alone does not establish that all domain intentions or future behaviors are correct. The paper's language-design recommendations are consequently broader than its directly measured task outcomes.

## Implications and continuation

Source information can affect API work even when no automatic static check is performed. Correct names can help; incorrect names can impose a cost. This directly qualifies a synthesis that credits every static-language advantage to diagnostics or assumes additional source guidance is uniformly beneficial. It does not establish an agent-context saving, a Nu advantage, modern-language soundness, or a diagnostic-versus-behavior equivalence.

S128's already acquired Eclipse comparison and S129's documentation comparison are the next primary controls for tool opportunity and alternative information. The bibliography reuses already recorded Prechelt–Tichy checking, Mayer API use and Hanenberg's dynamically favorable experiment; their primary methods remain necessary rather than credited from this paper. Optional-typing practice and generic/cast burden remain conditional routes in the existing C02/citation screen. Ref. 25 is a submitted debugging manuscript, not evidence of a verified published independent replication. No unchanged predecessor decision was resubmitted as new screening.

**Unique:** unresolved; type information has a direct prior intervention distinct from checking. **Valuable:** selected human API gains and a wrong-information repair cost are measured; typical prevalence, net work and Nu/agent transfer are not. **Scientifically valid:** the table, assignment limits, caps and attrition are reconstructed; checker increment and the trust/navigation explanation are unidentified. ISE equivalence, oracle and feasibility remain unvalidated, and all experimental holds remain.
