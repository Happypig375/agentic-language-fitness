# S75 — passive package reconstruction

This is a supplement to the [S75 reading](S75-game-smells-perception.md), not another publication or independent replication. Source: [Zenodo version 6720644](https://doi.org/10.5281/zenodo.6720644), concept `6327678`, metadata version index 4, last version at retrieval. ZIP MD5 `e42daeca2c0acfe05fc48b135ae034a8`, SHA-256 `649d0d32a45da579ba7c846e1acd50a544f019f87e54ef6e92375533872139a2`, 1,206,388 bytes; native attachment `5PWPYBPR`. Acquisition, own aggregation and full study reproduction are distinct.

All CSV rows and workbook cells needed for the counts below are parsed without executing macros, formulas, author code or games. The workbooks contain zero formula cells in the parsed sheets. Their legends, column meanings and aggregate relationships are read; this is not an independent recoding of all discussions. Workbook color-based removal markers are not exhaustively reconstructed. Source bodies and individual responses remain outside Git.

| Package member | Bytes | SHA-256 |
| --- | ---: | --- |
|`survey-final-results.csv`|44,704|`c1e059cb9ce36c6e518af1783e6a7cdd1af85c2228d554637d1798af4baa9f7f`|
|`SurveyHero-Questionnaire.pdf`|106,331|`23ed5787c9da664a18198a248af9e00607bbd20738d02132b9588047e4310acf`|
|`appendix.pdf`|199,559|`543fad5f41dd1b7be5c022cbd53a14c0ddb0f5d1714bddbb1865d1f4b7bb812d`|
|`all_forum_links.csv`|380,292|`ff3e84f752ceae7c3e5dbdab820e3913af637b3a71e8901223ba2eea0a56f016`|
|`final-classification-game-smells.csv`|29,138|`0b4d5a231f751fc5226525242a88090065b6fb3ddf212302466cf0feb2155b12`|
|`final-smell-category.csv`|1,710|`2acfc435dfe1b0853eb2a0292a031760eb72aadb0127b4272c8c404c1225ab40`|
|`validation_rounds.xlsx`|124,366|`1bb55efbd9999c469a7c31f05d83adfd404687372f23441babe0f95eeb9e13e7`|
|`label_rounds.xlsx`|39,696|`a3cab2fc158a8473bae422bfaebe2629ede0b8eff36a8607cb74825557cf746d`|

README and invitation are fully read. The invitation describes voluntary, confidential, approximately 20-minute participation. The 19 candidate-forum rows and three forum-selection URLs are inspected as provenance, not visited as fresh searches. The package inventories 31 archived HTML examples and their mapping; their bodies are not independently inspected. The two supplement PDFs are completely text-read, with visual pages specified in the main note.

## What reproduces

The survey CSV has 76 distinct IDs, 76 rows of exactly 85 columns and 33 numeric rating columns paired with optional comments. All nonblank ratings are integers 1–5. For each of the 28 final plotted items, own counts aggregate 1+2 as negative, 3 as neutral and 4+5 as positive, using that item's nonblank denominator. Every Figure 4–8 denominator and all 84 integer-rounded percentages agree. Five questionnaire/CSV items are absent from the final plots: separated controller inputs, failure to transfer objects, separated animation state, separated physics computation and inefficient rendering. No undocumented rationale or aggregation of their scores is assumed.

Nineteen final items have more than 50% positive ratings. Exact positive counts, in each figure's descending-positive order:

| Figure/category | Positive/valid counts |
| --- | --- |
|4, design/logic|63/76,61/76,58/75,47/75,47/75,40/75,36/75,25/75,24/74|
|5, multiplayer|60/66,52/66,48/66,37/61|
|6, animation|37/62,35/60,33/61,29/60,28/62,25/59|
|7, physics|55/63,46/61,25/62|
|8, rendering|51/61,48/61,48/62,35/58,28/59,24/60|

This verifies descriptive arithmetic, not independent agreement with the code labels, respondent representativeness, a significance test, performance effects or refactoring benefit. The 76 rows are shared across items; no pseudo-independent sample of 28×76 observations is constructed.

## What does not fully reconcile

**Discovery frame:** the all-links file reproduces 3,170 rows but has 3,166 unique literal rows and **2,744 unique literal URL strings**. Fifteen source labels include two names for Game Development Stack Exchange. Query spellings also differ. Literal URL counting is not canonical thread deduplication. The archive does not by itself establish the reported probability sampling frame or the replacement sequence.

**Validation rounds:** excluding headers, the three sheets have 339,106,136 nonempty URL rows, **581 total/575 distinct literal URLs**, versus paper 340,102,130 and 572 total. Resolved true/false/missing counts are respectively 98/241/0,25/76/5,29/102/5. First/second annotator Boolean judgments are both populated in 338,99,128 rows; 81,20,29 of those pairs differ. These are a descriptive check of a narrow binary field, not an invented reliability estimate for the evolving multicategory taxonomy. The sample/replacement/exclusion mapping remains unresolved.

**Labels:** workbook label rows are 52,56,61 for rounds 1–3, with four and five explicit new-label notes; the manuscript instead says 52,56,60. The cleaning sheet retains 61 labels and six explicit removal notes, with color also part of its documented convention. The final-grouping sheet has 50 source-label rows. The final catalog CSV has 30 rows/29 distinct literal rows: duplicated inefficient-transfer entry, an additional inefficient-rendering item and a misspelled physics category. The 16-page appendix and manuscript describe 28 final smells. These objects represent different stages; no automatic assumption that they are equivalent is justified.

**Final classifications:** 142 rows contain 136 distinct literal URLs and 30 literal smell strings, including capitalization and wording differences. Category totals are rendering 65, design/logic 47, multiplayer 10, animation 10 and physics 10. They are coded-post records, not smell prevalence over game repositories. Neither a 142/3,170 prevalence estimate nor universal saturation follows.

**Demographics/instrument:** any demographic answer occurs in 61 rows, education in 60, role in 59. Numeric experience fields have 56 game-development values, median 3, and 48 software-development values, median 5; both range 0.5–24. This differs from the manuscript's counts and reversed medians. Multiple-choice engine/language counts reproduce. The questionnaire shows required markers for the language and engine questions despite the manuscript's blanket optional-demographics description. Blank-template names/contact fields do not appear in the released CSV. No personal identity reconstruction is attempted.

**Prose versus plots:** manuscript p.14's 21%/23% static-coupling sentence does not match Figure 4 or the data's 24 positive/23 negative/27 neutral out of 74. Statements calling neutral responses a majority for rigging or the two least-endorsed rendering items are inaccurate: neutral counts are 24/60,19/59,24/60 respectively. The central plotted pattern nevertheless reproduces. The additional-suggestion category counts cover 14 stated suggestions while the text mentions 22 split rows; no complete row-to-category assignment is supplied here.

These mismatches limit exact process, final-edition and instrument lineage. They do not erase the reproduced 28-item ratings or the contextual comments presented in the manuscript. The next useful verification would require the final publication and a stage/exclusion mapping, rather than treating this package as a fully reproduced study or running new respondents/games.
