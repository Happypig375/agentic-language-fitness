# S45 — reactive API usage and developer-question topics

**Full publication reading completed 2026-09-29.** Zimmerle, Gama, Castor and Mota Filho, *Mining the Usage of Reactive Programming APIs: A Study on GitHub and Stack Overflow*, MSR 2022, pp. 203–214, [DOI 10.1145/3524842.3527966](https://doi.org/10.1145/3524842.3527966). Zotero parent `KMWWG24E`, publisher PDF `FFQQL8VI`: twelve pages, 621,094 bytes, SHA-256 `2f6ff8f9eca077d23e8fb38f9c98239bed1b121e15013d670415ca5b0ceed8f7`. This PDF appeared in the existing library; it was not downloaded by this session.

All twelve pages, sections 1–7, seven figures, six tables and 36 references were read. Rendered pages 5, 6 and 9 cover all seven figures, including paired frequency panels. Selected author artifacts were inspected and their aggregates recalculated; repository mining, topic modeling and author scripts were not executed. This reading resolves the usage/prevalence follow-up identified by S40, while retaining the distinction between usage and ease of use.

## Questions, samples and measurement

The work asks which ReactiveX operators occur in projects, which reactive topics appear on Stack Overflow, and how operators in selected topics overlap with operators in projects. It does not compare functional and imperative game architectures or measure maintenance outcomes.

The GitHub procedure searches repositories using library names and a ten-star threshold, excludes official ReactiveX owners and filters files by language and a library mention. Its January 7, 2022 sample contains 1,430 RxJava, 797 RxJS and 401 RxSwift repositories: 2,628 in total. The paper's larger search totals and intermediate star-filter counts are separate denominators. One tarball could not be processed. Library-name search, popularity filters and public hosting limit coverage; the authors' description of a population does not establish a census of all projects using the libraries.

Operator recognition uses regular expressions after removing comments and strings, rather than resolved semantic bindings. The false-positive check finds four selected collection-library imports in 156 of 14,377 Java files, then inspects sixteen of those files. Its reported 62% actual Rx calls in that subset is not an overall precision estimate for every operator, language or repository. The 1.09% file fraction is not a measured false-positive rate.

The Stack Overflow corpus contains **47,404 records comprising questions and accepted answers**, from February 2011 to December 2021, selected through eight library tags and deduplicated across queries. An answer inherits its question's title during text construction. This is neither 47,404 independent questions nor a sample of all developers or debugging episodes.

Topic modeling varies the topic count from ten to 35, uses perplexity to inform manual selection, and chooses 23 topics with 1,000 iterations and alpha/beta 0.01. Two authors inspect twenty leading words and fifteen sampled posts per topic; a third mediates labeling disagreements. The labels remain analyst-dependent. Popularity uses question views, favorites and scores. Difficulty uses the proportion of questions without an accepted answer and the delay between a question's creation and its accepted answer's **creation**. The latter is not the time at which acceptance occurred, nor measured debugging effort.

## Findings and bounded artifact reconstruction

Most distinct operator names occur at least once somewhere in the selected projects. This does not mean a typical project or developer uses nearly the entire API. The merged usage proportion is a vocabulary-level measure; raw call frequency, repository-level prevalence and per-project average calls are different quantities. Rare operators and heavily concentrated use coexist with a high fraction used somewhere.

The three author-linked repositories were pinned before inspecting selected files:

| Artifact | Revision and actual inspection |
| --- | --- |
| [Operator scraping](https://github.com/carloszimm/rx-scraping-msr22/tree/44ecc6284b54d928d1abedb18573d7d6863e1d90) | Untruncated 72-entry tree and selected three-library operator inventories; no documentation scraping rerun |
| [GitHub mining](https://github.com/carloszimm/gh-mining-msr22/tree/ac60e666b472fe523c5e5806cb2d320a3ace5952) | Untruncated 156-entry tree, selected README prose, operator inventories, all three released frequency maps, repository-search code and both utilization scripts; no remine or complete implementation audit |
| [Stack Overflow mining](https://github.com/carloszimm/so-mining-msr22/tree/124763ee7a319800c09b035ae111a6d0ac668515) | Untruncated 201-entry tree, topic/difficulty aggregate tables and result-processing code; corpus, LDA runs and remaining downloaded support files not fully inspected |

Recalculation from the released frequency maps yields **223/237 RxJava names, 112/112 distinct RxJS names and 65/66 RxSwift names** used at least once. Their merged vocabulary contains **295/310** used names, or 95.161%, consistent with the paper's rounded 95.2%.

There is a small inventory discrepancy worth preserving. The paper says RxJS has 113 operators. Its mining inventory has 113 entries but duplicates `partition`, leaving 112 distinct names. The upstream scraper inventory has 112 entries/111 distinct names; the mining inventory additionally includes `subscribe`. The released frequency map has 112 keys, all positive. Thus the reported 100% usage survives the distinct-name calculation, while the stated vocabulary size needs qualification. This does not validate every underlying match or establish that duplicate entries inflated any call count.

The three frequency JSON SHA-256 values, in Java/JS/Swift order, are `9c87895ae8b8f9774d7e0f094317f64e0cf44c747c2fcd8971880c02e1a0e51f`, `65d43ce8c2cd183035665b7620bc8baeada30a226f5d36cb274000a0f37f4f85` and `7e4df53a102da7a929bb9e4f0da591e3469549f0c5893c34cad163f6aa8a6726`. The inspected SO processing script hashes to `346524f0739feefb320eaab49ecf0a962d496cceb10d7f246ab7f6929bfd406f`; its code explicitly restricts difficulty/popularity to questions and computes answer-creation latency. These are bounded reconstruction checks, not independent data collection or experimental reproduction.

The 23 published topic counts sum to 47,404. Six stream-related topics sum to 17,250 records, about 36.4%. Testing/debugging has 1,219 records, 2.6% of the corpus; 49% of its questions have no accepted answer, and its reported median answer-creation delay is 3.3 hours. Those statistics describe this selected corpus and proxy definition. They do not measure the percentage of working time spent debugging or the benefit of a proposed tool.

The operator comparisons use three topics selected for popularity/difficulty. Figure 5's rank-position agreement is below ten percent; Figures 6–7 compare unordered overlap among the fifteen most/least frequent operators. A broadly shared core vocabulary can produce overlap without predicting an individual developer's difficulty. The paper's inference from widespread use to sufficient simplicity is not a directly measured usability outcome; S40 supplies separate, limited human evidence.

## Consequences and follow-up

**Unique:** reactive API usage, question-topic mining and developer difficulty are established research subjects. None establishes priority for a Nu lifecycle or D1 contrast. **Valuable:** stream lifecycle, error handling and debugging are concrete concerns, but selected post frequencies and missing accepted answers cannot estimate Nu's expected maintenance benefit. **Scientifically valid:** define the population, unit, exposure and behavioral endpoint before using prevalence to select tasks; keep source conventions, adoption, usability and maintenance success separate. Nu/ALF source equivalence, oracle sensitivity, task diversity and accounting remain unvalidated. New experimental allocation stays zero.

Reference 4 promotes **S60**, [Alabor and Stolze's professional-debugging study](https://doi.org/10.1145/3427763.3428313), to examine why specialized tools may fail to enter normal practice. Its [full reading is now complete](S60-professional-reactive-debugging.md), distinguishing observed avoidance from an untested integration-cost explanation. Reference 21 supplies **S61**, [REScala programming experience](https://doi.org/10.1145/3191697.3214337), acquired as conditional architectural/idiom context after its first page. Existing S39/S43/S49/S56 readings are reused. General mining/LDA methods remain conditional on adopting that design.

The incoming Scite graph requested at most twenty edges and returned nine edges/ten nodes without truncation or a low-coverage flag. Four works were already screened; the remaining five identities were checked by exact DOI with `limit:20`. A Combine-specific topic study and an education study remain conditional; general cross-platform mining and cloud-cost mining are outside the active claims, with the latter's preprint consolidated. The graph is not a field-completeness guarantee. Exact-title lookup of S60/S61 also requested twenty and returned two. The [source audit](../nu-literature-sources-2026-09-29.md) records all eleven new/changed source decisions, including the three bounded artifacts.
