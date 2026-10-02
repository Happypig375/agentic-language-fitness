# S181 — displayed metrics change judgments of identical code

## Identity and actual coverage

Marvin Wyrich, Andreas Preikschat, Daniel Graziotin and Stefan Wagner, *The Mind Is a Powerful Place: How Showing Code Comprehensibility Metrics Influences Code Understanding*, ICSE 2021, [DOI 10.1109/ICSE43902.2021.00055](https://doi.org/10.1109/ICSE43902.2021.00055). Selected [arXiv v2](https://arxiv.org/pdf/2012.09590v2), February 10, 2021, identified as the postprint after review: twelve pages, 383,725 bytes, SHA-256 `898d0d57be439fc68c00d2e58ea63b0480d86b7d53b74948100e8374dd9b60d9`. Native Zotero parent `LTYWLNHD`, PDF `G7XKIWB3`, note `XWILCJR8`; identity and stored bytes reverified. Publisher-file correspondence remains unverified.

All twelve pages, both figures, Table 1, two equations, seven numbered footnotes and 75 references read. All pages extracted/rendered; visual inspection of pages 5–8 covers the interface, equations, outcome plots, table and method footnotes. A separately bounded [released-package check](S181-displayed-metric-artifact-check.md) covers data, analysis text, task material and selected interface configuration. No author R, Java, browser experiment, model or maintenance task executed.

Live B01/B10/B12 question: can a metric display change developers' judgment independently of changing the code, and does that judgment shift imply a corresponding performance effect?

## Intervention, assignment and measurement

Forty-five German software-engineering master's students participate for course credit, with withdrawal permitted. Java and German proficiency are self-assessed as good; the acceptance fraction is unreported. Two incomplete personality/affect questionnaires are removed globally, leaving **43 participants: twenty displayed value 4, twenty-three displayed value 8**. The retained sample has 41 men and two women, mean age 24.47 and mean Java experience 5.83 years. The package shows both excluded participants were in the value-4 group and had complete task outcomes.

Participants first see two examples with metric values 1 and 9. They then solve the same three slightly modified Apache Java tasks in an IDE-like interface. Each snippet has one class and one method, with JavaDoc that may disagree with the implementation. For five specified inputs per task, participants give both the actual and documented output: thirty scored answers in total. Syntax highlighting, line numbers, occurrence highlighting and tooltips are available on a standardized laptop. Each task is followed by a 0–10 difficulty judgment, with larger values meaning harder code. The summed rating, called perceived understandability (PU), therefore ranges from 0 to 30 with **higher meaning more difficult**.

The displayed difficulty metric is fabricated. All three task displays are 4 in the easier condition or 8 in the harder condition; the code remains identical between conditions. The introductory examples and an investigator's stated expert provenance when asked help make the display credible. All three snippets have actual Cognitive Complexity 19, chosen as a rough difficulty control using the separate validation literature. Equal static scores do not establish equal human difficulty: task two is substantially slower and rated harder in both groups.

The paper describes a randomized, double-blind between-subject design, but footnote 3 ties assignment to participants' **self-chosen timeslots**. Conditions are spread across times of day, and the one or two participants in a slot receive the same treatment. The released data have no slot identifiers, allocation sequence or randomization log. Thus the account supports an assigned display contrast, but not a verified reconstruction of 43 independent individual randomizations. Possible shared-slot dependence and selection into slots remain unresolved. Investigator blinding and concealment of the hypothesis are reported; participants necessarily see their assigned display.

There is no undisplayed-metric control. The 4-versus-8 contrast identifies a difference between these two display packages under the assignment assumptions; it cannot say which is closer to an unanchored judgment or estimate benefit/harm relative to showing no metric.

## Positive judgment effect and uncertain performance effect

| Endpoint | Display 4, n = 20 | Display 8, n = 23 | Reported comparison |
| --- | --- | --- | --- |
| Sum of difficulty ratings | Mean 15.40, SD 4.17, median 14.5 | Mean 20.83, SD 4.23, median 20 | Welch t(40.318) = −4.227, p = .000132; mean-difference 95% CI [−8.02, −2.83]; Cohen d = −1.29, CI [−1.97, −.61] |
| Combined time/accuracy score (TAU) | Mean .37, SD .17, reported median .41 | Mean .37, SD .11, reported median .36 | Wilcoxon W = 256, p = .5385; Cohen d = −.006, CI [−.62, .61] |

**The higher display produces a large increase in perceived difficulty for identical code.** This is affirmative evidence that the display/context affects the reported judgment in these tasks, not merely a complaint about a proxy. The released values reproduce the point estimates. Including all 45 participants with complete task outcomes preserves the effect direction and large standardized difference; see the artifact note. Assignment, convenience sampling and the small task set bound transfer without erasing this result.

TAU multiplies total correctness divided by thirty by `1 − total time / maximum observed total time`. The maximum is 5,219 seconds after complete-case deletion. The slowest retained participant therefore scores zero regardless of correctness. This sample-dependent normalization and product combine two distinct outcomes; a comparable product can conceal different speed/accuracy patterns. It is not a separately validated unit of comprehension, and its null test does not test the equivalence of either component.

**No detectable TAU difference is not evidence of equal performance.** The reported standardized interval spans effects around .6 in either direction. There is no prespecified equivalence margin or equivalence test. The data support a strong rating difference and an imprecisely estimated combined-score difference; they do not establish that anchoring has no effect on task time, correctness or later maintenance.

Footnote 5 says the tests provide evidence for non-normality despite Shapiro p-values above .26 for the rating groups. The released analysis comment instead says no evidence for non-normality, consistent with using Welch's test. The easy-group TAU Shapiro result is .03, explaining the separate rank-test choice. This wording discrepancy does not change the reconstructed rating effect.

## Exploratory traits and mechanism limits

The paper explores eleven experience/personality/affect attributes in each group and pooled, for 33 correlations. It reports coefficients above an absolute .1 threshold without significance claims. Examples include easy-group conscientiousness .46 and experience −.28, versus hard-group experience .24. Pooled conscientiousness and optimism are .14, affect balance −.16 and extraversion −.13. These are exploratory associations in small groups, not randomized moderators or validated resistance predictors.

The pooled table label “within” does not make this a within-person cross-anchor experiment: each participant receives one anchor condition. Absolute distance from the shown metric lacks an unanchored truth criterion and depends on scale bounds and task difficulty. Post-task questionnaires, multiplicity and selection further limit causal claims about personality, optimism or experience overcoming anchoring.

The intervention bundles a numerical cue, its placement, preliminary examples and credibility context. It does not separate numerical anchoring from expectations, demand or response-scale interpretation. The study does not observe defect repair, refactoring, code review decisions or long-term work. Suggestions that validated metrics could improve prioritization or counteract bias remain hypotheses, not measured benefits here.

## Dependencies, transfer and continuation

The [package](https://doi.org/10.5281/zenodo.4498084) corroborates the main data transformation and positive rating result. Its interface files contain the value-4 tasks; the other condition is described but no separate value-8 deployment or assignment log is included. This is a reproducibility limit, not evidence that the reported condition was never run. The original German task forms, individual scored answers and exact allocation also remain unavailable in the bounded release.

**[S185](S185-cognitive-complexity-validation.md)** is now fully reconstructed from its twelve-page arXiv v1 and bounded released aggregation. Nine studies/327 entries is the time subset of ten datasets/427 entries, resolving the earlier passage discrepancy. Preserve positive time/ease associations and mixed correctness evidence; its released dependence and descriptive-filter issues qualify interpretation. Neither the citation nor equal scores establish that S181’s tasks are equally difficult. Displayed-score anchoring and source-score association address distinct questions.

SC117/W264 also retain the 2017/2021 *Automatically Assessing Code Understandability* lineage and the [2018 reanalysis](https://doi.org/10.1145/3196398.3196441). Selected primary passages describe favorable combined-metric prediction from the earlier dataset, not a new human experiment. The original 46-person account and later 63-person journal account require lineage reconstruction before treating their results as interchangeable. A [later Cognitive Complexity evaluation](https://doi.org/10.1016/j.jss.2022.111561) has a primary abstract reporting prediction comparable to traditional measures; that does not refute all metric associations or substitute for its unread method. Other metric-validation and interactive-search placebo routes remain conditional.

For Nu/ISE, S181 makes a concrete distinction: a representation, diagnostic or metric may change reported difficulty without a demonstrated change in independent behavioral outcomes. Preserve judgments as their own useful endpoint and measure claimed performance separately. This neither bans subjective evidence nor establishes an agent, language, exhaustiveness or compactness effect. It complements [S161](S161-metrics-and-judgment.md)'s judgment comparison and [S183](S183-maintenance-metrics.md)'s observed maintenance. S162’s workflow and S185’s validation are now reconstructed; the current survey continuation is GATlab’s theory-map alternative, with type/runtime/oracle gaps still distinct. All experimental holds remain.

| Criterion | Disposition |
| --- | --- |
| Unique | Metric-display interventions and bias in code judgments are prior art; no priority claim for Nu/ISE follows. |
| Valuable | The substantial rating shift demonstrates why displayed cues and independent performance should be distinguished. Practical maintenance benefit/cost remains unmeasured. |
| Scientifically valid | Identical-code comparison and released data support the rating result. Slot assignment, global exclusions, constructed TAU and wide uncertainty limit stronger causal, equivalence and transfer claims. |
