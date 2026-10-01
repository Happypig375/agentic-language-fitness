# S195 — Detecting dispersed concerns and testing their consequences

**Complete reading, 2026-10-01 HKT.** Pierre F. Baldi, Cristina V. Lopes, Erik J. Linstead and Sushil K. Bajracharya, *A Theory of Aspects as Latent Topics*, OOPSLA 2008, pp. 543–562. The native record uses the Crossref-verified SIGPLAN Notices identity, [10.1145/1449955.1449807](https://doi.org/10.1145/1449955.1449807); the [university dataset bibliography](https://ics.uci.edu/~lopes/datasets/SDS_source-repo-18k.html) independently supplies the associated proceedings DOI [10.1145/1449764.1449807](https://doi.org/10.1145/1449764.1449807). These are publication identities of one work, not independent studies. The acquired university-hosted PDF prints OOPSLA’08 and the proceedings ISBN; exact correspondence to the final Notices issue was not established.

Native parent **`E5T8XVIL`**, PDF **`AHYATC7W`**, note **`UFXLJDRL`** existed before intended body reading. Stored PDF bytes were reverified: **20 pages, 1,772,115 bytes**, SHA-256 **`4808341ae1081ea6fb083e5f85ea9947aaac5810984964b08c6c17062c35698b`**. All twenty pages, the full bibliography, six figures, twelve tables, displayed equations and footnotes were consumed; every page was visually inspected. Figure 6 is effectively image-only in extraction and was also inspected in a rotated rendering. Its selected concern/file matrix was read visually, not transcribed cell by cell or substituted for the unacquired full matrix. No author program, benchmark or candidate experiment was run.

## Three distinct questions

The introduction separates the existence of scattered/tangled concerns, their alleged harm to development, and the alleged improvement from AspectJ-style remodularization. The study addresses the **first** question. Section 6 explicitly leaves the second open, citing Eaddy et al. as related evidence; the third is not tested. This distinction is part of the authors’ own framing.

The useful result is a concrete, largely automated way to identify lexical concern mixtures at repository and project scales, with selected agreement against earlier JHotDraw aspect-mining findings. It is not a maintenance intervention, a causal paradigm comparison or a validation of an entropy threshold for harmful design. The authors also explicitly caution against extrapolating their Java results to other languages or representations without further validation.

## Representation, corpus and measurement

Sourcerer downloaded approximately 12,000 projects, primarily from SourceForge and Apache, and excluded distributions without source. Table 1 describes **4,632 projects, 366,287 files, 47,640 packages, 426,102 classes, 47,664 interfaces, 2,694,339 methods, 1,320,067 fields and 38.7 million LOC**, attributed to 9,250 developers. These are corpus/entity counts, not independent maintenance trials. The infrastructure maintains project releases and parses source into an entity database; it does not measure development outcomes here.

LDA represents files as bags of selected words, infers mixtures of topics within files and words within topics, and requires a chosen topic count. Section 3 describes symmetric Dirichlet priors, posterior sampling and parameter estimation. The paper does not provide a complete executed configuration, seed/convergence record or package binding the fitted matrices to an exact corpus release. These specification limits remain after a full publication reading.

Vocabulary selection is consequential and was refined by qualitative interpretability:

| Representation | Reported observation |
| --- | --- |
| Full source text | Large computational cost; a strong copyright topic, which the authors intentionally exclude to focus on code |
| Class/interface names | 49,521-word vocabulary; topics too general and closer to file names than implementation content |
| Add method names | 89,232 words; still insufficient implementation detail |
| Final representation | Class/interface names, method/field signatures, called-method names and SDK names; common English words and comments removed; **141,136 words** |

Crucially, an initial stop list **removed Java SDK names**, but the authors **restored them** because standard-library names helped expose concerns such as logging. The final representation retains those names. S120’s removal of Prelude identifiers therefore does not reproduce this particular final choice, even though it cites S195 as its methodological predecessor. Neither choice is automatically wrong; they require separate concern-validity evidence.

Scattering is entropy over files for a topic; tangling is entropy over topics for a file. Entropy is normalized by the logarithm of the distribution’s dimension. Zero describes a single occupied category and one a uniform distribution. Section 3.2 explicitly treats entropy as continuous and discourages forcing an aspect/non-aspect boundary. It does **not** validate **.5** as a maintenance-harm cutoff. As a mathematical illustration of the normalization, a uniform distribution over `k` of `N` categories has normalized entropy `log(k) / log(N)`; the same threshold need not identify the same number of affected files in differently sized corpora. This illustration is our algebra, not another experiment or a claim that the actual mixtures are uniform.

## Actual observations and validation

The whole-repository model uses **125 topics**. Table 2 supplies all 125 normalized scattering values; our extraction/visual check finds **123 above .5**, with a range **.46562778–.830006642**. Familiar topics include strings, collections, exceptions, logging, persistence and GUI events. Widespread vocabulary in these functions is the observation; a defect rate or cost of changing them is not observed.

The five selected project studies cover JHotDraw 6.0 beta 1, Jikes RVM 2.4.4, PDFBox 0.7.2, JNode and CoffeeMud. Figure 2 plots fifty ordered topic points for each project; sorting shows the distribution, not a sequence of increasing model sizes. Exact JNode/CoffeeMud versions are not supplied. The corpus sizes range from 370 files for PDFBox to approximately 6,200 for JNode. Project-specific topics are usually less scattered than general-purpose ones, with CoffeeMud a stated exception.

CoffeeMud is a useful game-specific boundary: its high-scattering topic concerns mobile-object communication. The authors need domain information to interpret the names, then hypothesize that game wrappers around general networking explain the result. They explicitly do not investigate that explanation further. Necessary coordination can be dispersed; this result does not measure a game-engine fault, maintenance burden or the benefit of a different architecture.

Tangling examples retain legitimate functional breadth. High-scoring JHotDraw files include bundled sample applications and a unit test exercising several capabilities; low-scoring files include exceptions and narrowly focused event/utility code. Five high and five low whole-corpus examples are selected illustrations, not independently adjudicated design-quality labels.

The authors fit a two-parameter inverse-logistic curve to sorted tangling values in five projects and the whole repository. Table 11 reports **R² .8985–.9630**, averaging approximately **.9473**. This describes fit to those sorted distributions, not explained maintenance effort, held-out prediction or six independent replications: the project data and whole repository overlap. The functional form is unbounded near its ends, visible in Figure 5, despite entropy itself being bounded. One minor arithmetic discrepancy is preserved: the six printed beta values average **.43658**, against the table’s **.43808**; the R² mean agrees. No original fit was rerun.

JHotDraw validation compares selected prior identifier, fan-in, dynamic, manual and revision-mining findings. Table 12 lists **seventeen matched concern categories**. The authors assign names using the top words, file associations and project documentation; Figure 6 omits topics identified as testing and displays only selected file rows. A reported prior ordering is recovered: persistence **.65**, undo **.63**, figure selection **.46**. Selected concern co-occurrences also agree. These are positive, bounded concordance results.

Three prior categories are not explicitly found: consistent behavior, contract enforcement and the composite pattern. The authors argue that some are structural specifications rather than lexical concerns. The paper acknowledges that prior methods lack a common benchmark. It supplies no complete independently labeled precision/recall or inter-rater calibration. Unsupervised fitting removes the need for training labels; representation choices, topic count and human interpretation still matter.

## Supplement access and lineage

The printed [results supplement](http://sourcerer.ics.uci.edu/oopsla08/results.html) fails in the web tool. Direct HTTP and HTTPS requests each time out after eighteen seconds. An exact-URL Internet Archive CDX query restricted to successful HTML returns an empty list. This is a bounded unsuccessful route, not proof that no archived copy exists. The fitted matrices, complete project results, exact implementation/configuration and run manifest remain unacquired. A lawful archived author package or library attachment containing these exact results is the executable next access step.

The accessible [18,000-project dataset page](https://ics.uci.edu/~lopes/datasets/SDS_source-repo-18k.html) describes an archive dated **22 April 2010**, cites this paper and supplies its proceedings identity. It does not certify that the larger later tarball equals the 2008 4,632-project analysis input or contains its fitted results. Only the page was read: **5,308 bytes**, SHA-256 **`44dc1f88ff93394f25f5e4eb8adb22e1b08b1c96acb6b85d826ddb89b5f95a0c`**. Neither that tarball nor the linked CWI derivatives were downloaded. Related slides and earlier topic-method records returned in search remain leads, not additional complete readings.

## Survey consequence

For **B01/B02/B05/B11/B12**, S195 provides a concrete concern-identification mechanism and selected validation. Preserve those positive results while separating a fitted lexical distribution, its interpretation as a concern, change locality, and actual maintenance outcomes. S120’s high-entropy reference and standard-library filtering receive the qualifications above; S195 does not establish an FP disadvantage or negate earlier favorable task results.

S196’s original Mozilla patch-history method is the next relevant empirical contrast: patch scattering, review selection and change outcomes differ from static lexical entropy. Its body remains unacquired at this checkpoint. Eaddy et al.’s cited defect study is another conditional primary-outcome route, not a result adopted from this bibliography. Continue accessible type, runtime and temporal-oracle methods if this access route remains blocked. No theme is closed and all experimental holds remain.
