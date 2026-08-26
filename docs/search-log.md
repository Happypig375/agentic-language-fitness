# Literature search log

Last run: **2026-08-26**

## Scope

Question: whether published work already compares the cumulative coding-agent cost of maintaining semantically equivalent software in different programming languages under inherited repository state.

## Sources searched

- arXiv title/abstract/full-text search
- ACL Anthology
- official benchmark websites and GitHub repositories
- backward and forward links from the closest benchmark papers
- general web search for newly released 2026 benchmarks not yet well indexed

## Query families

Queries combined variants of:

- `coding agent` / `software engineering agent` / `LLM code`
- `programming language comparison` / `multilingual` / `low-resource language`
- `token cost` / `trajectory cost` / `context efficiency`
- `repository maintenance` / `software evolution` / `iterative extension`
- `chained` / `sequential bugs` / `fresh context` / `accumulated state`
- `matched repositories` / `implementation-agnostic tests` / `code translation`
- `compiler feedback` / `static analysis` / `execution`
- `code compression` / `formatting` / `tokenization` / `semantic-preserving`

Exact-identifier follow-ups were run for all close papers and their benchmark sites.

## Inclusion criteria

A work was retained when it contributed evidence on at least one of:

1. programming language as an LLM/agent treatment;
2. repository-level or project-level coding;
3. inherited or iterative software maintenance;
4. agent trajectory/context/token measurement;
5. behaviorally equivalent cross-language evaluation;
6. low-resource language familiarity or compiler feedback;
7. semantics-preserving source/token transformations.

## Exclusion criteria

Works were deprioritized when they addressed only human language preference, runtime performance of human-written programs, generic natural-language tokenization without code relevance, non-executable opinion pieces, or code completion without a mechanism relevant to the research question.

## Important correction during review

The first pass incorrectly treated fresh-context inherited maintenance as part of the open gap. ChainSWE directly implements that condition for sequential Python bug fixing, while SlopCodeBench and SWE-CI cover closely related iterative-evolution settings. The repository's claim was narrowed before merge to the controlled **cross-language** treatment.

## Reproducibility limits

This was not a formal database-exported systematic review: there is no exhaustive hit count, deduplication flow, or risk-of-bias instrument. Before preregistration or submission, repeat the search in ACM Digital Library, IEEE Xplore, Scopus/Web of Science where accessible, Google Scholar/Semantic Scholar citation graphs, and relevant 2026 conference proceedings. Freeze a dated bibliography and record exact queries and screening decisions.
