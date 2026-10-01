# S176 — LLM test proxies depend on inputs, aggregation and the selected population

## Identity and actual reading

Junda Zhao, Shurui Zhou and Eldan Cohen, *Do Coverage and Mutation Scores of LLM-Generated Test Suites Correlate with Their Effectiveness? (Replicability Study)*, [arXiv 2607.22880v1](https://arxiv.org/abs/2607.22880v1), submitted 2026-07-24. The first page reports PACMSE 3/ISSTA, Article ISSTA002, October 2026, related DOI `10.1145/3832093`. Exact Crossref lookup returned 404 and Scite did not return that ACM DOI; publisher binding remains unverified. The primary arXiv history lists v1 only.

Native Zotero parent `TVQQNSQI`, note `69PKTUIC`, PDF `KWWIAYUI` existed before body reading. [PDF](https://arxiv.org/pdf/2607.22880v1): **24 pages, 1,155,818 bytes**, SHA-256 `9ee979180b0f82d76328c34066360eaa69ad1877bfb08cef7a699285988857e7`; stored bytes reverified. All 24 pages, four figures, fourteen tables, two methodological footnotes and 61 references read on 2026-10-01. Twelve visual pages (3/6/7/9/10/11/12/13/14/15/16/17) cover every figure/table and the four code panels in Figure 4. No appendix appears in this edition.

The [bounded artifact check](S176-proxy-artifact-check.md) separately records pinned source, cached output and all 105 released CSVs. The paper is fully read; the whole package and original execution are not reproduced. No model, Java, mutation tool, notebook, author sampler or installation ran.

Live B07/B12 question: does [S170](S170-mutant-correlation.md)'s size/correlation finding transfer to LLM generation, and which comparison supports a positive proxy claim? The authors explicitly call this a **conceptual**, not direct, replication.

## Population, prompts and information

The paper starts with Defects4J v3.0's 854 defects across seventeen Java projects and selects **318 focal methods** changed by historical fixes. It requires presence in both buggy/fixed versions, non-private accessibility and a relevant developer trigger. Consequently, added/deleted methods, inaccessible methods and nonqualifying fixes fall outside the population. The artifact's selector accepts only public/protected methods, a narrower rule than the paper's inclusion of package-private methods.

Eleven named models supply thirteen settings because two hybrid models have reasoning enabled/disabled. These are not thirteen independent model families. The claimed generation total is **8,268 suites = 318 × 13 × 2 inputs**, with 101,123 individual tests. The released unsized CSVs contain 8,268 rows but their generated-test fields sum to 92,560; preprocessing versus raw-generation correspondence remains unresolved. Each CSV's 318 rows share 233 bug IDs, so focal methods are not 318 independent real faults.

The model sees the focal implementation plus signatures, fields, constructors and neighboring API context. The released example explicitly requests high line and branch coverage. Thus the tested prompt already favors two measured proxies; this is not a neutral estimate for every testing workflow. Temperature zero is reported, without repeated generations establishing deterministic outputs or session reliability.

Fixed inputs supply a regression-style task; buggy inputs supply an existing-bug-exposure task. Effective detection requires at least one generated test that passes on the fixed version and fails on the corresponding buggy version. Fixed-code generation followed by historical buggy-code testing uses information from the completed repair; it does not prospectively measure unseen future regressions. Figure 4 gives a concrete implementation-imitation example: a faulty equality method induces an assertion endorsing its erroneous result. That example is evidence of a possible mechanism, not its prevalence.

Compilation repair and test removal occur in the released harness. Oracle validation on the two versions, structural coverage and the green suite passed to mutation need not involve exactly the same surviving tests. The study does not establish an independent specification for arbitrary behavior or a universal guarantee that historical fixed code is fault-free.

## What is correlated with what?

The sampling unit is a **draw of 100 focal-method suites**, with 1,000 distinct draws per model in the supplied loop. Different draws overlap; they are not independent generated experiments. The combined view pools within-model draws, the intra-model view analyzes one model and the inter-model view aggregates each model setting to one point.

The paper describes fixed-size samples of three, five or ten tests, restricted to suites with enough tests. The current source and saved data instead retain many smaller suites, including some zero-test rows. This materially limits the claim that size was held exactly constant; see the artifact table. The conceptual contrast with S170 also changes project pools to focal-method pools, generators, eligibility and aggregation. Its causal explanation cannot be attributed to the arrival of LLMs alone.

Average aggregation gives each eligible method a mean contribution. Accumulated aggregation divides summed hits by summed opportunities, so large methods/classes carry more weight. Raw mutation uses all generated mutants; normalized mutation uses covered mutants. The paper says mutation is focal-method scoped, but the supplied wrapper targets a class and parses its aggregate PIT summary. It supplies no focal-method restriction in the inspected path. The paper/README identify CodeCover for coverage, while archived metadata and the inspected execution path distinguish ordinary coverage from CodeCover's condition metric; exact all-metric binding remains unresolved.

Pearson and Kendall correlations are descriptive associations, without a held-out predictive evaluation. The paper repeatedly emphasizes significant coefficients among many metric/size/view comparisons and uses conventional strength bands. Its resampled observations share rows, and thirteen configurations share tasks and model families. Neither many draws nor small nominal p-values establish independent evidence or universal calibration.

## Positive findings and their limits

For fixed-code inputs, Table 10 reports an inter-model correlation of **.861** between average branch coverage and detection; Table 13 reports **.863** between average raw mutation score and detection. The passive CSV arithmetic reproduces .860969 and .863312 using the supplied count target. These positive associations survive inspection and must not be discarded because other methods or views have weak correlations.

The count target is equivalent to a rate with a common denominator such as all 318 attempted methods. It differs from detection conditional on each model's retained, compilation-eligible methods, whose counts range from 155 to 218 in the fixed-input data. Descriptive conditional-rate calculations give .650 and .694, respectively. Those are **different estimands**, not replacement “corrected” coefficients or a new hypothesis test. A report must state which failure/eligibility population it describes.

The inter-model fixed-size raw-mutation coefficients are also reproduced from the saved rows, approximately .702/.695/.833 for three/five/ten. However, those rows violate the stated exact-size rule. The observed ranking signal is evidence under the released capped/retained workflow; it cannot by itself establish independence from test count. Average/accumulated and raw/normalized forms differ substantially, so “mutation score is predictive” is too broad without the variant.

Combined and intra-model correlations are generally weaker. Useful between-model association does not mean that increasing a score in one model's suite causes more detection, nor does it provide the same decision rule as S170's top-score suite selection. This is an aggregation distinction, not a contradiction.

For buggy inputs, the paper reports weak coverage–detection associations but omits the complete coefficient set. **It does not perform mutation analysis on buggy inputs.** Its footnote argues that a conventional green-suite mutation workflow would remove the very tests exposing the existing bug. That is a scope restriction, not evidence that a measured buggy-input mutation correlation was weak or that all conceivable mutation methods are impossible. The released buggy-input model roster also lacks one original setting at size ten, and the size-three arithmetic slightly exceeds the paper's own .4 “weak” threshold. The blanket wording needs its actual configuration and rounding limits.

## Integration costs and transfer

Test counts, compilation/pass rates and proxy scores do not measure net cost. A fraction of usable outputs omits model price/latency, prompt extraction, repeated repair, execution, instrumentation and human interpretation. The paper's cost-effectiveness language therefore cannot establish net resource superiority.

Training-data contamination is acknowledged. Different outputs under buggy/fixed prompts do not exclude contamination combined with prompt sensitivity. Java historical fixes, selected methods, one prompting workflow and thirteen related settings limit transfer to evolving interactive applications, independent state/temporal obligations or a fixed coding agent's maintenance success.

The result strengthens two useful distinctions: validate behavior independently of the implementation being changed, and state whether a metric supports model comparison, suite selection or within-suite improvement. It supplies positive model-comparison evidence under specific conditions, not a complete oracle or a causal source-convention effect.

| Criterion | Disposition |
| --- | --- |
| Unique | Correct/incorrect input, documentation-assisted oracles and proxy validation have prior methods; ISE priority remains unconfirmed. |
| Valuable | Fixed-input cross-model association is concrete positive evidence. User effort, net costs, future regressions and Nu transfer remain unmeasured. |
| Scientifically valid | Reconstruct inputs, aggregation, retention and denominators before extrapolating. The released size filter and measurement-scope differences qualify stronger claims without erasing the favorable associations. |

## Consequential continuation

S177's thirteen-page arXiv v3 is acquired to reconstruct the direct incorrect-code intervention; S178's twenty-three-page arXiv v2 is acquired for positive documentation/oracle evidence, with its twenty-two-page final-journal correspondence unresolved; S179's eleven-page author paper is acquired to settle the original coverage/size method. All have native records before continued reading and retain abstract/opening-only scope at this checkpoint.

The parent workflow `10.1145/3691620.3695529` and the unit-testing survey `2506.15227` remain conditional metadata leads. Primary TOGBench and proof-based coverage titles are conditional routes, not newly validated results; secondary workflow summaries require primary verification. Read S169's existing evaluation framework and return to the practice/type/runtime gaps as well as these specific dependencies. The [search ledger](../nu-background-searches-2026-09-30.md) preserves actual queries and open continuations; no thematic closure or experimental start follows.
