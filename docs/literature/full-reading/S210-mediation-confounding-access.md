# S210 — statistical equivalence and causal interpretation

## Identity, coverage and corrected access state

David P. MacKinnon, Jennifer L. Krull and Chondra M. Lockwood, *Equivalence of the Mediation, Confounding and Suppression Effect*, Prevention Science 1(4), 173–181, 2000, [DOI 10.1023/A:1026595011371](https://doi.org/10.1023/A:1026595011371). Native parent/note **`QTSTS2UA`/`I7K3563T`** preceded intentional body reading. A later native refresh discovered the supplied PDF **`D76N7HLH`**, version 5043: **nine pages, 81,725 bytes**, SHA-256 `a81f22048bf6804cc8a3e0ebad79d5abf54285d8bed91b2b3c43395787d01b0d`. Its title, authors and printed pages match the original journal. This supersedes the earlier access-limited status; it is not a successful retry of the failed web routes.

**All nine pages are read textually and visually**, including the single figure, single table, five numbered equations, four footnotes and 48 references. Extraction loses Greek letters, signs and operators; the images supply those parts. Own elementary arithmetic checks the two printed examples. No original-data analysis, simulation or author program was executed.

SC137 and W369–W371 previously supplied only abstract/indexed passages and outgoing citation contexts. The Springer PDF route returned HTML; ASU publication/supplement routes reached institutional login; PMC returned a browser check; EuropePMC XML/web, BioC and existing LibKey routes did not supply a PDF. Those attempts remain historical facts, not present publication-access barriers. The separately linked seven-page simulation supplement remains unread/unacquired.

## Reconstructed method

The paper distinguishes a mediator on an asserted causal pathway, a covariate used to adjust a relationship, and a suppressor whose inclusion reveals an opposing association. Its principal result is that **the same OLS coefficient calculation can describe all three interpretations**. An observed coefficient change cannot determine the direction or causal status of the underlying relations.

Using the paper's notation, Equations 1–3 fit:

```text
Y = intercept + tau X + error
Y = intercept + tau' X + beta Z + error
Z = intercept + alpha X + error
```

The difference `tau − tau'` equals the product `alpha beta` in this linear setup. Crucially, **alpha is estimated by regressing Z on X**. It is not obtained by algebraically inverting a regression of X on Z. This directly resolves the original-method dependency of [S168](S168-suite-size-confounding.md). Our qualification: the finite-sample OLS identity requires compatible observations/specification; causal meaning and inferential assumptions are additional. It is not a logistic coefficient identity, as [S209](S209-logistic-mediation.md) explains.

The article states multivariate-normal/error assumptions for its discussion. Equation 4 gives a first-order delta-method variance, `beta² Var(alpha) + alpha² Var(beta)`. Equation 5 adds the product of the two variances, described as exact under independence or a second-order approximation. These are assumption-specific uncertainty formulas, not proof of a causal mechanism. The nine-page article provides no raw observations or executable analysis.

Table 1 distinguishes the signs of population direct and third-variable effects from sample coefficient changes. With a null population third-variable effect, a sample can still appear to show mediation or suppression. Opposing direct and indirect pathways can also cancel in the total effect: therefore requiring a statistically significant total association before considering a pathway can miss inconsistent mediation. This is useful contrary evidence to a rule that a total-effect null implies every mechanism is absent; it does not license selecting favorable pathways after seeing results.

## Worked evidence and limits

The first example uses a prevention-program study of 31 school teams, fifteen receiving the intervention and sixteen forming a comparison group. The reported total association with the intention outcome is **−.139**, versus **−.181** after including the selected mediator. The mediator-path estimates are **.573** and **.073**, with standard errors **.105** and **.014**. Their product is positive, opposing the beneficial total direction in this example.

Own arithmetic gives product **.041829**, first-order SE **.01109526**, and a normal 95% interval **[.02008, .06358]**, reproducing the reported .042/.011/[.020,.064] to precision. Thus the paper demonstrates how a favorable aggregate result can coexist with an adverse component pathway. This is a reconstructed numerical illustration, not independent causal validation of the program or a software effect. The article does not provide individual data, detailed allocation or cluster-adjustment implementation, so those aspects of the originating study are not independently reconstructed here.

The second example uses the same project to illustrate age adjustment of the association between vertical leap and bench-press performance. The coefficient changes **8.55 → 3.42**, yielding **5.13** with reported SE .868 and interval [3.42,6.83]. Arithmetic with the rounded inputs gives [3.42872,6.83128]; the small lower-end difference is compatible with unavailable unrounded inputs and is not evidence of an invalid result. These two examples are not independent datasets.

Footnote 4 reports that an external simulation found accurate estimates/standard errors for sample sizes at least fifty under its normal-data model. Because the supplement remains unavailable, this is **the article's report**, not a reconstructed simulation, a universal sample-size rule or a validation of software-study data.

The paper explicitly requires theory, timing, design and accumulated evidence to distinguish interpretations; model fit alone cannot do so. Some explanatory language is broader than a causal identification result: randomizing an intervention does not by itself randomize its mediator or remove mediator–outcome confounding. Likewise, a causal common cause can affect the outcome when manipulated, so the paper's suggestion that manipulating a confounder should leave effects unchanged is not universal. These are limits on extending its discussion, not a rejection of the OLS identity or worked arithmetic.

## ISE disposition

S210 closes the selected publication-method gap: coefficient change is a statistical quantity whose causal interpretation needs separate support, and the third-variable regression has a definite direction. Together with S209, it strengthens the bounded interpretation of S168 without altering S168's useful reduction/prioritization outcomes. Preserve adverse components, null total effects and sampling uncertainty; do not substitute fitted adjustment or successful residual checks for identification.

The original data and seven-page supplement remain distinct unresolved artifacts. They are unnecessary to establish the displayed OLS identity and do not block the independent **B04/B06 persistent-vector/iterator/transient sequence** readings. No experiment or additional worker is authorized by this method closure.
