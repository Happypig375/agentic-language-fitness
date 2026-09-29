# X01: Cross-index recall check

Query: `static typing software maintenance`; requested years 1970–2026 and ten records per source. This is a supplemental recall check for the wider Nu background, not a complete type/maintenance survey. All ten supplied arXiv abstracts were screened; all ten Crossref records lacked abstracts and remain uncertain rather than excluded. No primary bodies were read in X01.

Per-source hits: Semantic Scholar=0 (error), OpenAlex=0 (error), arXiv=10, OpenReview=0 (error), Crossref=10, DBLP=0 (error). **20 unique; 0 merged duplicates; 1 filtered as irrelevant; 19 retained.** No score threshold. The unfiltered set is `cross-index-types.json` beside this report.

Citations are the returned index counts, not impact estimates; arXiv did not supply citation metrics, shown as “unavailable” rather than zero. Dates and venue labels are returned metadata, pending consequential edition checks.

| # | Title | Date | Venue | Citations | Score | Sources |
| --- | --- | --- | --- | ---: | ---: | --- |
| [1](https://doi.org/10.1007/s10664-013-9289-1) | An empirical study on the impact of static typing on software maintainability | 2014-10 | Empirical Software Engineering | 70 | 3 | crossref |
| [2](https://doi.org/10.1109/icsm.2007.4362642) | Computation of Static Execute After Relation with Applications to Software Maintenance | 2007-10 | 2007 IEEE International Conference on Software Maintenance | 10 | 3 | crossref |
| [3](https://doi.org/10.1109/csmr.2006.53) | Static evaluation of software architectures | 2006 | Conference on Software Maintenance and Reengineering (CSMR'06) | 52 | 2 | crossref |
| [4](https://doi.org/10.1109/ase.2009.80) | Static Typing for Ruby on Rails | 2009-11 | 2009 IEEE/ACM International Conference on Automated Software Engineering | 18 | 2 | crossref |
| [5](https://doi.org/10.1109/csmr.2009.51) | Static Security Analysis Based on Input-Related Software Faults | 2009 | 2009 13th European Conference on Software Maintenance and Reengineering | 6 | 2 | crossref |
| [6](https://doi.org/10.1007/3-540-60954-7_44) | Static typing | 1996 | Lecture Notes in Computer Science Object Technologies for Advanced Software | 1 | 2 | crossref |
| [7](https://doi.org/10.1109/icsm.2005.84) | Static analysis of object references in RMI-based Java software | 2005 | 21st IEEE International Conference on Software Maintenance (ICSM'05) | 1 | 2 | crossref |
| [8](http://arxiv.org/abs/2602.14046v1) | Every Maintenance Has Its Exemplar: The Future of Software Maintenance through Migration | 2026-02-15 | arXiv | unavailable | 2 | arxiv |
| [9](http://arxiv.org/abs/1806.09774v1) | How Do Static and Dynamic Test Case Prioritization Techniques Perform on Modern Software Systems? An Extensive Study on GitHub Projects | 2018-06-26 | arXiv | unavailable | 2 | arxiv |
| [10](http://arxiv.org/abs/2406.04710v2) | Morescient GAI for Software Engineering (Extended Version) | 2024-06-07 | arXiv | unavailable | 2 | arxiv |
| [11](http://arxiv.org/abs/2108.02133v1) | The Impact of Traceability on Software Maintenance and Evolution: A Mapping Study | 2021-08-04 | arXiv | unavailable | 2 | arxiv |
| [12](http://arxiv.org/abs/2607.01850v1) | Technical Debt Friction for Maintenance Prioritization: An Industrial Multi-Case Study | 2026-07-02 | arXiv | unavailable | 2 | arxiv |
| [13](http://arxiv.org/abs/2306.06030v2) | Analyzing Maintenance Activities of Software Libraries | 2023-06-09 | arXiv | unavailable | 2 | arxiv |
| [14](https://doi.org/10.1109/icsm.1997.624245) | Intraprocedural static slicing of binary executables | 1997 | 1997 Proceedings International Conference on Software Maintenance | 55 | 1 | crossref |
| [15](https://doi.org/10.1109/icsm.1996.565037) | Binary translation: static, dynamic, retargetable? | 1996 | Proceedings of International Conference on Software Maintenance ICSM-96 | 37 | 1 | crossref |
| [16](https://doi.org/10.1109/csmr.2013.66) | Static Analysis of Data-Intensive Applications | 2013-03 | 2013 17th European Conference on Software Maintenance and Reengineering | 7 | 1 | crossref |
| [17](http://arxiv.org/abs/2109.10971v1) | Developers Perception of Peer Code Review in Research Software Development | 2021-09-22 | arXiv | unavailable | 1 | arxiv |
| [18](http://arxiv.org/abs/2207.01254v1) | The Present and Future of Bots in Software Engineering | 2022-07-04 | arXiv | unavailable | 1 | arxiv |
| [19](http://arxiv.org/abs/1710.09055v2) | We Don't Need Another Hero? The Impact of "Heroes" on Software Development | 2017-10-25 | arXiv | unavailable | 1 | arxiv |

**Model Knowledge:** no additional unverified references added.

## Overview

The 20 returned records span typing, static analysis, architecture, regression testing and maintenance practice. One abstract clearly concerned a different inclusion question. The retained 19 contain unresolved relevance, not 19 validated methods or independent empirical comparisons. Four connector failures leave substantial coverage gaps.

## Trends

This small, capped result set mixes older static-analysis/architecture papers with recent maintenance and AI agendas. The date pattern is a retrieval artifact, not evidence that field activity rose or fell. Software-maintenance/reengineering venues dominate the Crossref subset; arXiv publication status needs separate checks. Name variants and paper editions have not been reconciled across a broader corpus.

## Key themes

- Types and static feedback: [1], [4], [6] are direct mechanism/method leads; the missing Crossref abstracts prevent importing outcomes.
- Structure and change analysis: [2], [3], [14], [16] provide prospective architecture, slicing and data-analysis leads.
- Regression and maintenance information: [8], [9], [11] concern migration, prioritization and traceability, with different endpoint and cost boundaries.
- AI, review and maintenance organization: [10], [12], [13], [17]–[19] are contextual or method leads; abstracts do not establish a Nu or coding-agent effect.

## Keywords frequency

Document frequency in the 19 retained titles, using the named technical words below; synonyms are not merged.

| Keyword | Count |
| --- | ---: |
| software | 13 |
| static | 11 |
| maintenance | 5 |
| typing | 3 |
| analysis | 3 |

## Most cited by accepted paper

“Accepted” here means retained after this screen, including uncertain records. Missing arXiv metrics are omitted from ranking.

| Rank | Title | Year | Citations |
| --- | --- | --- | ---: |
| 1 | [An empirical study on the impact of static typing on software maintainability](https://doi.org/10.1007/s10664-013-9289-1) | 2014 | 70 |
| 2 | [Intraprocedural static slicing of binary executables](https://doi.org/10.1109/icsm.1997.624245) | 1997 | 55 |
| 3 | [Static evaluation of software architectures](https://doi.org/10.1109/csmr.2006.53) | 2006 | 52 |
| 4 | [Binary translation: static, dynamic, retargetable?](https://doi.org/10.1109/icsm.1996.565037) | 1996 | 37 |
| 5 | [Static Typing for Ruby on Rails](https://doi.org/10.1109/ase.2009.80) | 2009 | 18 |

## Most cited by first author

Exact returned author strings are used; `C. Cifuentes` and `Cifuentes` are not silently merged without an identity check. These are within-result-set totals, not author career totals.

| Rank | Author | Papers in set | Total citations |
| --- | --- | ---: | ---: |
| 1 | Stefan Hanenberg | 1 | 70 |
| 2 | C. Cifuentes | 1 | 55 |
| 3 | J. Knodel | 1 | 52 |
| 4 | Cifuentes | 1 | 37 |
| 5 | Jong-hoon An | 1 | 18 |

## Recommendations for reading

1. [6] Static typing (1996): check the conceptual treatment before importing modern empirical claims.
2. [3] Static architecture evaluation (2006): separate measurable source properties from demonstrated maintenance outcomes.
3. [1] Static typing and maintainability (2014): inspect assignment, human population, task and feedback controls for the Nu/F# question.
4. [11] Traceability mapping (2021): inspect link-maintenance costs and industrial-evidence gaps.
5. [12] Technical-debt friction (2026): examine practitioner/context dependence and prospective versus post-change information.

These are an initial reading path within X01, not a five-paper ceiling or automatic promotion of every retained item. Continue relevant prior-art, contrary-evidence and citation paths across the wider survey.

## Connector errors

```text
[dblp] Error on query 'static typing software maintenance': Expecting value: line 1 column 1 (char 0)
[open_alex] Error on query 'static typing software maintenance': 401 Client Error: Unauthorized for url: https://api.openalex.org/works?search.semantic=static+typing+software+maintenance&filter=publication_year%3A1970-2026&sort=relevance_score%3Adesc&page=1&per-page=10
[openreview] Error on query 'static typing software maintenance': openreview not installed. pip install openreview-py
[semantic_scholar] Error on query 'static typing software maintenance': 403 Client Error: Forbidden for url: https://api.semanticscholar.org/graph/v1/paper/search?query=static+typing+software+maintenance&offset=0&limit=10&fields=title%2Cauthors%2Cyear%2Cabstract%2CcitationCount%2Curl%2Cvenue%2CpublicationDate%2CexternalIds&year=1970-2026
```

No connector failure establishes absence. No extra dependencies, OAuth or purchases were used to bypass these failures. Unexamined service continuations and alternative queries remain open.
