# S186 — runtime anomalies, monitoring practice and observable obligations

**Source:** Monika Steidl, Benedikt Dornauer, Michael Felderer, Rudolf Ramler, Mircea-Cristian Racasan and Marko Gattringer, *How Industry Tackles Anomalies during Runtime: Approaches and Key Monitoring Parameters*, SEAA 2024, pp. 364–372, DOI [10.1109/SEAA64295.2024.00062](https://doi.org/10.1109/SEAA64295.2024.00062). Read [arXiv 2408.07816v1](https://arxiv.org/pdf/2408.07816v1), 14 August 2024, on 2026-10-01. Publisher byte/content correspondence remains unverified.

**Identity and coverage:** native parent `BBVLN5T2`, note `YNG5TK2P`, PDF `9GFEUNP5`, created before intentional body reading. Reverified **nine pages, 698,337 bytes**, SHA-256 `ef2c380243e71a4729ff6d3ca6fc8fffafc37b945ca601b8507a4454ae5bb2f3`. All pages, Figure 1, Tables I–II, the numbered table footnote and 45 references read; all pages extracted/rendered, pages **3, 4 and 6** visually inspected for both tables and the taxonomy. No separate appendix or formal algorithm/proof. The [artifact check](S186-runtime-anomaly-artifact-check.md) records all five supplement PDFs, bounded spreadsheet inspection and own count checks. Main Codex reading, not independent review or experimental reproduction.

## Decision and method

The live B07/B10/B11/B12 question is what monitoring reveals about evolving software and which costs remain outside a successful source edit or test run. The closest rival explanation is that apparent benefit comes from familiar instrumentation, domain knowledge and operational workflow rather than a language or architectural mechanism. Useful contrary evidence would include successful automated diagnosis, rules that adapt well, or monitoring whose overhead itself causes failure. All three appear as scoped practitioner reports here; this is not a measured comparison of Nu or repair agents.

The paper combines fifteen semi-structured interviews at twelve companies with a focused microservice literature review. Participants were recruited through the authors' networks for experience with monitoring/anomaly detection across domains, company sizes and roles. Three pairs share companies: G/J, H/K and M/N. Interviewee, company, system, incident and literature-paper counts are different units. The sample includes monoliths, embedded/PLC systems and microservices, whereas the literature inclusion is microservice-focused. Neither sampling frame estimates industry prevalence.

Interviews ran October 2023–February 2024 with two interviewers and two pilots. The article describes 30–60 minutes; the supplement lists **28–67 minutes**. Inductive coding addresses definitions and approaches; a logs/traces/metrics framework structures the monitoring-parameter analysis. Authors discuss coding disagreements and check interpretations with participants. Public material consists of selected, sometimes mixed-language coded accounts and methods, not the raw recordings/transcripts. The interview guide introduces an early explainability model before eliciting examples and explicitly asks about energy. Responses therefore cannot establish unprompted demand or spontaneous priority for those ideas.

The review extends Soldani and Brogi, DOI `10.1145/3501297`, using the Google Scholar query `anomaly detection runtime monitoring microservices` in June 2023 and December 2023–January 2024. It reports recovering 50% of seed papers and adding thirty older papers. From 92 identified entries, 36 are selected for industry/real-life evaluation data. Eligibility favors post-2015 peer-reviewed microservice runtime work and excludes artificial benchmark-only fault injection, among other boundaries. This is useful targeted discovery, not demonstrated full recall or evidence that controlled faults are scientifically unsuitable. The supplement has a nineteen-row sample review; its published 94.7% agreement is not a whole-corpus reliability estimate. The exact denominator remains unresolved below.

## Reported benefits and costs

All twelve sampled companies reportedly use rules. Two also develop AI approaches, and four use commercial tools with AI capabilities; these are overlapping categories, not randomized or mutually exclusive treatment arms. Rules are valued for existing tool support, understandable configuration, fast detection and relatively low training/computation burdens. Participants describe identifying expensive queries, accounting for expected variation and checking established conditions quickly. Well-written, tested rules can work well; a rule that recognizes `sudo` but omits `su` illustrates an incomplete specified condition, not a theorem about rule-based monitoring.

The costs include domain-specific threshold design, ongoing maintenance, missed unforeseen cases and false alarms. Supplement examples attribute false alarms to Prometheus, Nagios and log rules as well as commercial AI-associated tooling. Operators sometimes ignore alerts or reduce their frequency. These accounts lack common fault sets, exposure times, detection thresholds and false-positive denominators; they cannot establish that either approach has a lower error rate. Changing logging quality, workload, hardware or software changes the detection problem.

AI-related reports retain their positive scope. H describes time saved by automated root-cause support when its diagnosis is correct; G describes accommodating seasonality. Other accounts describe explainability, labeling, training/retraining and computation burdens. One internal clustering effort reportedly finds useful patterns but is not production-ready because of data quality. Aggregating data makes analysis cheaper while losing detail. Potential future advantages and practitioner satisfaction are distinct from measured detection accuracy, saved person-time or a causal comparison.

The released literature coding contains **23 AI / 13 non-AI rows**. Using its printed bibliographic years, **16 of 20 rows dated 2021–2023 are AI-coded**, reproducing the reported 80% recent-literature figure. This describes the authors' selected literature and coding, not deployment prevalence, comparative effectiveness or independent datasets. Some work shares evaluation platforms and some bibliographic rows bundle or misidentify publications; the artifact note preserves these boundaries. The paper's observation of no marked domain differences is qualitative, not a statistical equivalence result.

## Concrete temporal and operational cases

Table II contains nine retrospective examples, retained as reported cases rather than newly observed incidents:

| Case | Reported trigger and observation | Consequence for the survey |
| --- | --- | --- |
| B1 | Archived versions accumulate filesystem inodes on shared NFS storage; response times rise across services. | A resource lifecycle and shared dependency matter beyond the locally edited component. |
| C1 | A released memory leak causes garbage-collection/memory symptoms and eventual failure after days. | Observation duration and accumulated state affect exposure. |
| D1 | A Kubernetes service is restarted when a RAM condition is reached. | Symptom containment and removal of the underlying defect are distinct outcomes. |
| F1 | An orchestration process exhausts heap space while continuing to run, with slow responses and no obvious logged error. | Successful process liveness and absent error logs do not establish acceptable behavior. |
| F2 | Unbounded numeric input causes a crash and a difficult-to-interpret Japanese log message. | Input obligations, failure manifestation and diagnostic usability are separate. |
| J1 | Slow/leaking backend libraries allow asynchronous work to accumulate. | Pending work and queue delay can matter before a terminal failure. |
| L1 | Added logging creates excessive I/O and brings down the system. | Observability has a reported adverse resource effect; instrumentation is part of the system. |
| M1 | Capacity appears adequate around 500 users, then degrades or fails beyond the boundary. | Workload and scaling policy condition observed behavior. |
| O1 | A routine using little CPU repeatedly writes flash until wear degrades performance. | Short CPU measurements can miss long-horizon physical-resource costs. |

The supplement adds a reported health-check restart when a thread pool expands slowly despite functionally correct behavior, and container startup dependencies that cause repeated retries. These are additional accounts from the same interviews, not independent replications. A finite successful replay need not expose delayed growth, accumulated work or environmental startup ordering. Conversely, these accounts do not prove that all such failures require a new runtime or language.

## Signals, ground truth and integration

Figure 1 organizes a useful observation vocabulary. Logs can expose templates, frequency, severity, expected heartbeats and event/execution patterns. Traces can expose HTTP statuses, latency, invocation paths and graph structure. Metrics include queue lengths/waiting, CPU, memory/cache/pools, network, storage and sometimes energy. A parameter such as response time may come from multiple modalities; the channels are not independent replications. Some proposed trace-structure comparisons come from the literature rather than interview adoption.

Interpretation requires an expected condition, workload and observation horizon. High CPU may be expected, autoscaling changes resource relationships, and an unexpected drop may matter as much as a spike. Missing output can reflect either normal inactivity or failure; heartbeats can help but do not prove all obligations. Slow sampling can miss events, fine sampling can add noise/cost, and aggregation can erase patterns. The same I/O or latency symptom can arise from different causes. Correlation or a warning is therefore not a complete semantic/temporal oracle or confirmed root cause.

Energy is an elicited potential parameter with limited reported measurement, constrained by hardware access and cloud visibility. The supplement's positive/negative mention counts cannot be read as adoption counts. The planned explainability model, TrainTicket injections and future real-data evaluation are not results of this study. Selected industry data in a cited method do not by themselves establish sound labels, independent evaluation or successful transfer.

## Disposition and next action

S186 supplies independent practitioner-method evidence alongside S162's emergency-change accounts. It strengthens the requirement to distinguish expected behavior, observable signal, fault diagnosis, response action, recovery and retained obligations. It preserves credible monitoring benefits as well as maintenance/false-alarm/overhead costs. It supplies neither a Nu advantage nor a validated independent oracle or numerical adoption estimate.

Return next to the already acquired **S93 original structured-design paper**. After the recent metrics and operational-practice readings, its mechanism for decomposition/coupling/cohesion is a more consequential unresolved foundation for B01/B09/B11 than automatically expanding the newest microservice citation neighborhood. S187/S188 remain acquired mechanism/benchmark dependencies, and S95, S185 and the type/oracle continuations remain open. Soldani/Brogi's review and Islam et al.'s positive industrial deployment are conditional primary-method leads; their metadata/abstracts are not adopted full-method results. No experiment, installation or additional worker is authorized.

| Criterion | Disposition |
| --- | --- |
| Unique | Runtime observation and anomaly handling have substantial prior methods and practice; no Nu priority claim follows. |
| Valuable | Reported diagnosis, fast detection and adaptation benefits coexist with missed behavior, false alarms and observation costs. Their comparative magnitude and Nu transfer remain unknown. |
| Scientifically valid | Interviews and inspectable coding support bounded accounts and a useful taxonomy. Sampling, elicitation, method/edition gaps and unavailable raw data limit prevalence, comparative and causal conclusions. |
