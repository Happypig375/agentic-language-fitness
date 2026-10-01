# S120 — A modularity critique and a preliminary topic measurement

**Complete reading, 2026-10-01 HKT.** Ismael Figueroa and Romain Robbes, *Is Functional Programming Better for Modularity?*, PLATEAU 2015, pp. 49–52, [DOI 10.1145/2846680.2846689](https://doi.org/10.1145/2846680.2846689). Existing native parent **`DVYPKH8Y`**, PDF **`DXQPDY26`**, note **`CLT29LEB`** were verified before selected reading. The four-page publisher-formatted library PDF is **141,434 bytes**, SHA-256 **`0507f0ffe51a0b3e91f0b07efeaf7d4668954c32f7637af18f5b01acf47c87e8`**. All four pages, both panels of Figure 1, five URL footnotes and 21 references were read; all pages were visually inspected. No experiment or author program was executed.

## What the critique establishes

The authors distinguish Hughes's constructive examples of higher-order functions and laziness from a general empirical claim that functional programming improves modularity or productivity. They inspect selected citations: an early survey, an amortized-data-structure paper, and one example from each year 2010–2014. They also acknowledge that many citations are historical or appropriately qualified. Their reported ACM/Google Scholar counts are a dated description of retrieval in 2015, not current citation coverage.

This is a useful argument about the scope of evidence, with concrete quoted examples. It is not a systematic estimate of how often researchers overclaim: selection/coding rules, complete decisions and independent judgments are not supplied. The present reading consumed the quotations in S120, not the full bodies of every quoted paper. A citation to a constructive mechanism does not by itself assert a comparative maintenance effect. The authors' statement that they knew of no relevant large-scale evaluation is dated and scoped; it does not establish present-day absence.

## The GHC study

The empirical component analyzes **one snapshot of `ghc/compiler`**. It does not assign languages, decomposition strategies or maintenance tasks, and it does not measure developer effort, defects, behavioral preservation or changes over time. The software-evolution analysis discussed in section 3 is a proposed complementary approach, not a second experiment performed here.

| Choice | Reported method | Inferential limit |
| --- | --- | --- |
| Topic counts | LDA with `topicmodels` in R, **428** topics from the module count or **63** from top-level subfolder count | Two heuristics, not fitted evidence that these are the true semantic concern counts |
| Text | Full source text, prepared with `tr`/`awk`, or tags from a custom parser | Different lexical representations of the same software, not independent projects |
| Vocabulary | Remove Prelude identifiers; split camelCase and underscore names | Authors acknowledge unfinished normalization; exact preprocessing and selected snapshot matter |
| Scattering | Entropy of a topic's distribution across files | A lexical/topic distribution is a proposed concern proxy, not an observed change burden |
| Tangling | Entropy of topics within a file | Requires the corresponding file/topic distribution and normalization, not merely a count of names |
| Interpretation | Normalize to 0–1; use .5 as a high-entropy reference from the prior topic study | The threshold is not calibrated here against maintenance outcomes or a competing implementation; the now-read S195 predecessor explicitly discourages a universal cutoff |

Figure 1 preserves the concrete observation: several fitted scattering curves are high, while tangling is generally lower and changes with the topic count and text representation. The authors interpret this as suggestive modularity difficulty in GHC and explicitly leave comparative functional-language superiority unsettled. No exact point values, uncertainty intervals, repeated-fit stability or alternative-language counterfactual are supplied. The figure does not show that all modules are poorly designed, that functional programming caused the pattern, or that another paradigm would improve it.

## Surviving preprocessing source and missing experiment material

The cited [experiment page](http://www.inf.ucv.cl/~ifigueroa/doku.php/research/plateau2015) redirects to HTTPS and returns **404** through direct requests; the web tool also cannot open it. The R analysis, fitted distributions, plotting code, complete corpus and exact GHC revision were not acquired. The executable next access step is a recovered author/institutional archive or a lawful attachment containing that specific experiment package. A missing package is not evidence that the published curves are false.

The linked [hothasktags fork](https://github.com/ifigueroap/hothasktags) remains accessible. The selected custom-source commit **`df747c03b5d192ab010253e1379785458b678120`**, dated 7 August 2015, contains the added filtering script. We read five complete files and verified their Git blobs and SHA-256:

| File | Coverage / bytes | SHA-256 |
| --- | --- | --- |
| `Main.hs` | All 701 lines / 32,179 | `ad7346732ad39b451a12e16880b5abc61bf6b5b3f5f510159504be6dcd4d9452` |
| `filterWords.py` | All 34 lines / 828 | `8e4ea999649b16d3166291d20aa3f68bcb0498a8453f49e249aca898295d3d81` |
| `preludeWords.txt` | All 336 lines / 2,292 | `650960e01fd1116fff60a76dfa69437426b22224a458bb500a19b720ea79f324` |
| `hothasktags.cabal` | All 45 lines / 1,507 | `c15e0d0456a264ac2bdb6a1592d8dfab9bb766d4173b07517c6dd11c2c805ec0` |
| `Makefile` | All 17 lines / 339 | `b510e1f29381e7b95fddc5beff3fd969590a7bfa3864682bd3e5d2fcc6655adf` |

The parser extends declaration extraction into many expression/type forms, but it does **not** simply retain every used or declared name. Its expression visitor discards ordinary variable references, while an infix operator takes a separate extraction path. Pattern bindings omit the right-hand side at that declaration case; ordinary type variables and several literal/template forms are intentionally omitted. These are source-level observations, not executed failures. They mean that the chosen lexical vocabulary needs explicit interpretation.

The surrounding tag generator also adds import/export scope. Thus a visible imported name can appear through scope handling even when the expression visitor does not count its use. Qualified names are handled differently during expression extraction and import expansion. Parse failures print a message and omit the file from the database. `filterWords.py` rejects exact first-column strings from its supplied list; it does not itself perform camel-case splitting, topic modeling or entropy calculation. No retrieved execution manifest binds these code paths, flags, parse outcomes or later normalization steps to Figure 1. This prevents treating the source inspection as a reconstruction of the full fitted analysis.

Version history is also bounded. The current fork head **`c7b10a71903e662bc0667a3e2269c94d8b9f3a2f`** is dated 3 August 2016. A different pre-conference history entry, **`5b92e2a1e86cfbfa13bb342bc5b50ad6780706de`**, has no filtering files in its six-entry tree; its first 150 of 427 `Main.hs` lines and complete Cabal/Makefile were inspected only for lineage. A date-filtered history result is not proof of the paper's executed revision. Neither entry replaces the explicitly chosen custom-source commit or certifies publication-time correspondence. Local manifests retain all inspected-file identities; source bodies stay outside Git.

## Consequences and next dependencies

For **B01/B02/B11/B12**, separate a useful composition mechanism, a lexical organization proxy, a task-specific maintenance outcome and a comparative paradigm claim. S120 raises a legitimate question and supplies a preliminary observation. It neither demonstrates a general functional-programming disadvantage nor negates the favorable mechanisms and task outcomes reconstructed elsewhere, including [S90](S90-modularity-program-modifiability.md), [S115](S115-open-data-functions.md) and [S138](S138-compositional-data-types.md).

The [complete S195 foundation](S195-aspects-latent-topics.md) now supplies a material qualification: it explicitly discourages a universal aspect/non-aspect entropy cutoff, leaves maintenance harm open, and restores Java SDK identifiers after finding that removal obscures concerns. Thus S120’s .5 reference and Prelude removal are not validated by an identical final predecessor method. S195 preserves positive selected concern-identification concordance; it does not turn the GHC curves into a measured disadvantage. **S196**, Walker et al.’s Mozilla patch-history analysis, remains the specific original-outcome dependency with abstract/metadata coverage only and an unacquired body. Its native record preceded intended reading. Two S195 publication identities still count as one work.

The C02 continuation also consumes twelve previously unread supplied passages, reaching **95 of 199**, with **104 still unexamined** and later pages open. These extend the alternatives for reusable patterns, representation control and formal transformations without establishing practical benefit. Use the now-complete S195 reconstruction and continue the broader type/oracle/runtime frontiers; no construction, worker or experiment hold is lifted.
