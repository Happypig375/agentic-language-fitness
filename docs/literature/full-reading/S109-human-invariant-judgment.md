# S109 — Human classification of generated invariants

**Complete reading, 2026-10-01 HKT.** Matt Staats, Shin Hong, Moonzoo Kim and Gregg Rothermel, *Understanding User Understanding: Determining Correctness of Generated Program Invariants*, ISSTA 2012, pp. 188–198, registered [DOI 10.1145/2338965.2336776](https://doi.org/10.1145/2338965.2336776). Existing native parent **`388WNPAS`**, PDF **`VTX7T4JI`**, note **`WMJUI3VN`** were verified before continuing the selected reading. All eleven pages, six figures (including the two code examples), three tables, nine footnotes and 32 references were consumed; all pages were visually inspected. No participant study, author analysis or subject program was executed.

The [institutional PDF](https://orbilu.uni.lu/bitstream/10993/10975/1/staats-invariant-understanding-issta-2012.pdf) is **398,541 bytes**, SHA-256 **`944e5cab89b3e5f9aa0430110f7b08d23cd6c3291a15adbe669ca488b861ef55`**. The current [author-laboratory copy](https://swtv.kaist.ac.kr/files/publications/international_conference/staats-invariant-understanding-issta-2012.pdf) is byte-identical. The repository labels it a publisher postprint, but its HTML DOI `10.1145/04000800.2336776` conflicts with the registered identity; the PDF prints the conference/ISBN without a DOI. Its visibly repeated word in the introduction and numerical inconsistencies below are present in the PDF, not solely extraction artifacts. Exact final-publisher correspondence remains unverified; the identical mirror adds no edition or independent-study count.

## Task and reference behavior

The study asks whether people can classify generated JML invariants against **current source behavior**, under an explicit assumption that the given program is correct. It intentionally avoids asking what the program ought to do. This is a regression-preservation exercise, not a test of whether people can identify intended new requirements, adjudicate a changed domain or design a complete temporal oracle.

Daikon generates method postconditions and class invariants from **1,000 Randoop test inputs per case example**. Preconditions are removed: they introduce intended-use questions and confused pilot participants. The generation suite was chosen to yield both correct and incorrect candidates, rather than a representative prevalence sample of production invariants. The annotation format and auxiliary Daikon function definitions are supplied to participants.

The reference labels have asymmetric strength. After approximately ten static-checking tools proved unusable for these programs/invariants, the authors try to falsify candidates using **100,000 Randoop inputs**, a separate manually written random harness run for **24 hours**, and manual inspection by **three authors**. Candidates that survive are accepted as correct. Thus a demonstrated counterexample establishes an incorrect invariant for the tested semantics; surviving testing and inspection do not prove correctness. The authors explicitly acknowledge that label error can affect their measured human accuracy. This is extensive reference-label work, not an independent formal specification of intended behavior.

## Assignment, populations and denominators

The two classroom studies share a task but differ in participants, preparation, time and program versions. They are not a controlled comparison of education or expertise.

| Design element | KAIST | KNU |
| --- | --- | --- |
| Participants analyzed | Eleven graduate students | Nineteen undergraduates; twenty initially, one Matrix participant declined to complete |
| Presentation | Ninety minutes, English | Thirty minutes, Korean |
| Initial source-familiarization task | Write five invariants, twenty-five minutes | Same task, twenty minutes |
| Classifying supplied invariants | Sixty minutes | Thirty-five minutes |
| Program versions | Larger reduced Matrix/PolyFunction | Further reduced Matrix/PolyFunction; StackAr unchanged |

Each person is randomly assigned **one** of three classes. Both tasks use **paper printouts**, motivated by insufficient computers at KNU and comparability between studies. No IDE, execution or static-analysis assistance is provided. This condition matters when comparing the earlier study cited by S109, which used ESC/Java support and a different verification outcome. S109’s adverse observations are not an isolated replication that disproves the usefulness of that earlier tool-assisted workflow.

Table 1 distinguishes source/invariant units:

| Case | KAIST: NCSS / methods / invariants | KNU: NCSS / methods / invariants | Reported correct-label fraction, KAIST / KNU |
| --- | --- | --- | --- |
| StackAr | 35 / 9 / 85 | 35 / 9 / 85 | 64.7% / 64.7% |
| Matrix | 135 / 23 / 127 | 122 / 21 / 88 | 81.9% / 79.5% |
| PolyFunction | 150 / 22 / 124 | 110 / 18 / 84 | 79.0% / 83.3% |

The rounded fractions correspond to **55/30, 104/23 and 98/26** accepted-correct/refuted candidates at KAIST, and **55/30, 70/18 and 70/14** at KNU. These are candidate items repeatedly judged by the assigned participants, not that many independently assigned users. Figure 2’s classification increments indicate groups of **3/4/4** and **7/6/6**, respectively; the latter are inconsistent with the section 4.2 shorthand “5–6 students.” This is a reconstruction from the displayed increments and cohort totals, not recovered participant allocation data.

Participants may leave an answer **unknown** because of uncertainty or time. Figure 1 separates correct/incorrect reference labels and true/false/unknown responses; footnote 6 says statistical analyses exclude unknown responses and use firm answers. The complete response matrix and analysis code were not recovered. Preserve that missingness explicitly: neither abstention nor a complement of an aggregate success rate can automatically be reported as an explicit wrong judgment under all denominators.

## Results that should be retained

Table 2 reports the following **mean percentages correctly classified**, separated by reference-label class. These are six study/case summaries, not a single pooled human-oracle failure rate.

| Study / case | Accepted-correct candidates correctly accepted | Refuted candidates correctly rejected |
| --- | --- | --- |
| KAIST StackAr | 90.9% | 55.5% |
| KAIST Matrix | 75.9% | 73.9% |
| KAIST PolyFunction | 71.4% | 46.1% |
| KNU StackAr | 74.5% | 41.4% |
| KNU Matrix | 69.0% | 60.1% |
| KNU PolyFunction | 68.3% | 54.7% |

Both false acceptance and false rejection visibly occur. Correctly accepting accepted-correct candidates is easier on average than rejecting refuted candidates; the authors report paired, two-sided permutation p-values **.038** and **.004** across eleven/nineteen users. Those scoped adverse results survive the reporting and reference-label limitations. The paper does not measure resulting bug detection, wasted repair time, trust, adoption or overall tool cost: section 6.3 explicitly leaves those outcomes to future work.

Some printed summaries disagree. The abstract and later discussion give **9.1–31.7%** for misclassified correct candidates, while the introduction says **9.1–39.8%**. Section 4.1 gives a **41.6%** KAIST lower mean for incorrect candidates, against Table 2’s **46.1%**. We retain the table cells above and do not silently select a pooled rate from conflicting prose. The unknown-response denominator still needs the original package before precise error-rate reconstruction.

The smaller-program hypothesis is **not supported**: all six KNU pairwise permutation tests have p-values **.06–.98**. This does not establish equivalent performance or show that complexity is irrelevant. Each program bundles functionality, source, generated assertions and reference-label mix, with small assigned groups. The KAIST comparisons are not tested for insufficient sample size. Repeated invariant judgments do not create additional independently assigned participants.

Invariant difficulty has a broad middle rather than a clean easy/hard split. The exploratory correlations between item difficulty and the average overall success of people who solve it are positive in ten of twelve study/case/correctness combinations (**.32–1.0**); two approximately **−.1** correlations are marked nonsignificant. Both axes are derived from the same response matrix and the latter conditions on success for that item. These are useful descriptive patterns, not independently validated prediction or an identified causal explanation. The exploratory operator/size/GPA/experience/confidence analyses find no stable strong relation; their limited samples and extensive comparisons do not establish absence of those influences.

## Concrete failure modes

The authors’ qualitative inspection provides actionable examples without claiming that all mistakes share one cause:

- **Ambiguous sentinel values:** a stack can return `null` for empty state and, under the paper’s stated example, for an explicitly pushed null value. The inferred equivalence between null result and empty stack therefore fails. The stated state is a counterexample to the two printed predicates; the modified implementation itself was not recovered or executed here.
- **Unchecked state setters:** the Matrix class can expose dimensions/storage changes that violate a plausible representation relationship. Many participants correctly reject these candidates, while some cases are overlooked. Intended use and current permitted behavior differ.
- **Auxiliary predicate semantics:** the paper reports that its `pairwiseEqual(null, null)` helper returns false. A visually trivial constructor equality can therefore fail on a permitted null argument. Figure 6 shows Matrix code despite a StackAr caption. The helper’s standalone source and actual execution remain unverified here.

These examples help distinguish language-level validity, assumed API contracts, helper semantics and intended behavior. Suggested explanations, stronger falsification and better filtering are proposals in this study, not measured successful interventions.

## Data access and next use

The printed `http://pswlab.kaist.ac.kr/data/` host now fails DNS resolution through both HTTP and HTTPS, and the web reader cannot open it. An exact successful-HTML Internet Archive query returns four distinct index captures. The [21 December 2012 index](https://web.archive.org/web/20121221070641/http://pswlab.kaist.ac.kr:80/data/) was fully inspected: **24,424 bytes**, SHA-256 **`ecaf8cb047aa714758e57d31842871ba2ba964ddc48f85cc0c698ef676dfecaf`**.

Its [study-file page](https://web.archive.org/web/20121221070534/http://pswlab.kaist.ac.kr/data/staats-KAIST-invar-study-data.zip/view) explicitly identifies the paper’s raw data and advertises **`staats-KAIST-invar-study-data.zip`, 717,143 bytes**. The retrieved HTML is **20,023 bytes**, SHA-256 **`b027fcf2590c42b605fad16e4a3cf376408ea522b7a7a5f77dcc166291576228`**. The archive prefix query returns only that view page; its exact linked download returns **404 HTML**, not a ZIP. The analogous current laboratory `/data/` route also returns404. Exact-filename web search returns no results. These are bounded access failures, not proof that the dataset is lost everywhere.

The raw responses, annotations, adjusted Java subjects, questionnaires and analysis package remain unacquired. Recovering that named package through a lawful author/institutional archive or library attachment is the executable next step for the unknown-answer denominator and Table 2 reconstruction. No duplicate PDF or empty ZIP attachment was added to Zotero.

For **B07/B09/B12**, S109 closes S104’s specific primary-reading dependency: human review is fallible under a concrete, time-limited paper classification task, and reference labels themselves require justification. Keep observed errors, abstention, refuted versus accepted-correct labels, and intended versus current behavior separate. Do not transfer a “half wrong” slogan to all human oracles, tool-assisted verification, modern models or Nu evolution. Continue S110’s model-steering mechanism and the independent fault-sensitivity methods; no new apparatus or experiment is authorized.
