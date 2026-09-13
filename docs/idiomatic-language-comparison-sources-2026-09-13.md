# Idiomatic language-comparison source ledger

**Date:** 2026-09-13 HKT

**Scope:** bounded, targeted deep research for the F#/C# idiomatic-architecture
comparison. This is a durable DOI/search/access ledger, not a systematic-review
claim, PRISMA record, or statistical evidence synthesis. It records source
identity, edition, access, reading extent, locators, and one transfer limitation.
No source establishes an F# or C# LLM-maintenance effect.

The [research synthesis](idiomatic-language-comparison-research-2026-09-13.md)
contains the argument and recommendations. This ledger is linked from AGENTS.md
and PLAN.md so future agents can retrieve the DOIs without treating the
recommendations as adopted decisions. Research used the connected `codex_apps`
Scite tools and the Deep Research skill/workflow with primary-source checks;
no separate hosted Deep Research engine was invoked. No Scite collection,
Zotero library or account configuration was changed.

## Reading and source conventions

- DOI links below are canonical identifiers. An arXiv DOI identifies a preprint,
  not peer-review certification.
- “Full” means the source was read through the cited article copy; “selected”
  means only the listed methods/results/limitations sections were read; “abs.”
  means abstract only and must not support full-text claims.
- R01–R06 are the architecture/API/notation set from the architecture note.
  R07–R14 are language-quality, typing, feature-usage, and language-comparison
  sources. R15–R18 are context/repository-evolution neighbors. QA-only leads
  are retained separately and are not main patch-outcome evidence.

## Primary source ledger

### R01 — Parnas (1972)

**Identity:** David L. Parnas, “On the Criteria To Be Used in Decomposing
Systems into Modules,” *Communications of the ACM* 15(12), 1053–1058 (1972),
DOI [10.1145/361598.361623](https://doi.org/10.1145/361598.361623).

**Access/extent:** Full six-page ACM reprint in archival copy
[PDF](https://ckrybus.com/static/papers/decomposing_systems_into_modules_1972.pdf);
publisher metadata checked through the DOI/ACM record. Read pp. 1053–1058
(PDF pp. 1–6): introduction/expected benefits, KWIC decompositions, comparison,
criteria, efficiency, and conclusion.

**Use/limitation:** Primary design argument for information hiding and change
localization, not a controlled language or maintenance experiment; KWIC is a
small pedagogical example and efficiency costs are reasoned rather than
randomized.

### R02 — MacCormack, Rusnak & Baldwin (2006)

**Identity:** Alan MacCormack, John Rusnak, and Carliss Y. Baldwin,
“Exploring the Structure of Complex Software Designs: An Empirical Study of
Open Source and Proprietary Code,” *Management Science* 52(7), 1015–1030
(2006), DOI [10.1287/mnsc.1060.0552](https://doi.org/10.1287/mnsc.1060.0552).

**Access/extent:** Final bibliographic record at
[INFORMS](https://pubsonline.informs.org/doi/10.1287/mnsc.1060.0552); read the
authors’ 39-page HBS working-paper copy
[PDF](https://www.hbs.edu/ris/Publication%20Files/05-016.pdf). Selected
reading covered abstract/introduction, methodology §§3–4 (working-paper
pp. 8–17), results §5 (pp. 18–22), discussion §6 (pp. 23–27), and Tables 1–3
(p. 31).

**Use/limitation:** DSM propagation/clustered-cost evidence shows architecture
can alter change reach, but only two Linux/Mozilla products and static
function-call dependencies were studied; propagation cost is not maintainer
time, defect rate, or an F#/C# effect.

### R03 — Ko et al. (2006)

**Identity:** Andrew J. Ko, Brad A. Myers, Michael J. Coblenz, and Htet Htet
Aung, “An Exploratory Study of How Developers Seek, Relate, and Collect
Relevant Information during Software Maintenance Tasks,” *IEEE Transactions
on Software Engineering* 32(12), 971–987 (2006), DOI
[10.1109/TSE.2006.116](https://doi.org/10.1109/TSE.2006.116).

**Access/extent:** IEEE metadata and the authors’ full
[CMU PDF](https://www.cs.cmu.edu/~NatProg/papers/Ko2006SeekRelateCollect.pdf);
deposited [author record](https://www.researchgate.net/publication/3189706_An_Exploratory_Study_of_How_Developers_Seek_Relate_and_Collect_Relevant_Information_during_Software_Maintenance_Tasks)
also checked. Read methods §§3.1–3.2 (pp. 974–975), results §§4.6–4.8
(pp. 977–983), and limitations §5 (pp. 980–982).

**Use/limitation:** Primary maintenance-navigation evidence, but it analyzes
ten experienced Java users on one small unfamiliar Paint program in one IDE;
the authors caution about industry/team generalization and language/tool scope.

### R04 — Green & Petre (1996)

**Identity:** Thomas R. G. Green and Marian Petre, “Usability Analysis of
Visual Programming Environments: A ‘Cognitive Dimensions’ Framework,”
*Journal of Visual Languages & Computing* 7(2), 131–174 (1996), DOI
[10.1006/jvlc.1996.0009](https://doi.org/10.1006/jvlc.1996.0009).

**Access/extent:** Publisher metadata at
[ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1045926X96900099);
authors’ deposited [full text](https://www.researchgate.net/publication/200085937_Usability_Analysis_of_Visual_Programming_Environments_A_%27Cognitive_Dimensions%27_Framework)
read through §§3–6 and Appendix A (PDF pp. 10–41 and Appendix A).

**Use/limitation:** Primary framework and notation analysis for
abstraction/visibility/viscosity trade-offs; the edit-time comparison is an
explicit N=1 straw test and the VPL conclusions are tentative, not a language
ranking or LLM study.

### R05 — Stylos & Myers (2008)

**Identity:** Jeffrey Stylos and Brad A. Myers, “The Implications of Method
Placement on API Learnability,” *SIGSOFT/FSE-16* (2008), pp. 105–112,
DOI [10.1145/1453101.1453117](https://doi.org/10.1145/1453101.1453117).

**Access/extent:** ACM DOI metadata and the authors’ full
[CMU PDF](https://www.cs.cmu.edu/~NatProg/papers/FSE2008-p105-stylos.pdf) were
read. Key locators are methods §4 (printed article pp. 106–107), results §5
(printed p. 108), discussion §6 (printed pp. 108–109), and external validity
§7 (printed pp. 109–110).

**Use/limitation:** Controlled Java API discoverability evidence, but ten Java
programmers used small modified APIs, think-aloud, and blocked ordinary web
search; it did not test F#, C#, production maintenance, or reading/debugging.

### R06 — Endrikat et al. (2014)

**Identity:** Stefan Endrikat, Stefan Hanenberg, Romain Robbes, and Andreas
Stefik, “How Do API Documentation and Static Typing Affect API Usability?”
*ICSE ’14*, 632–642 (2014), DOI
[10.1145/2568225.2568299](https://doi.org/10.1145/2568225.2568299).

**Access/extent:** Open-access institutional record
[UNIBZ](https://bia.unibz.it/esploro/outputs/conferenceProceeding/How-do-API-documentation-and-static/991006493688501241)
verified edition/authors/pages; primary-author [PDF](https://www.inf.unibz.it/~rrobbes/p/ICSE2014-docstypes.pdf)
read selected methods/results/limitations §§3–8 (printed article pp. 634–641).
Development-time ANOVA: typing p=.007, documentation p=.075, interaction
p=.211. Coding-time ANOVA: typing p=.018, documentation p=.008, interaction
p=.426.

**Use/limitation:** Twenty-five students, one Dart task, simplified IDE, and
researcher-written documentation limit transfer; the paper itself says
documentation usefulness/comprehension and all expertise/language contexts
were not established.

### R07 — Hanenberg et al. (2014)

**Identity:** Stefan Hanenberg, Sebastian Kleinschmager, Romain Robbes, Éric
Tanter, and Andreas Stefik, “An Empirical Study on the Impact of Static Typing
on Software Maintainability,” *Empirical Software Engineering* 19(5),
1335–1382 (issue 2014; online 2013), DOI
[10.1007/s10664-013-9289-1](https://doi.org/10.1007/s10664-013-9289-1).

**Access/extent:** Primary author [PDF](https://pleiad.cl/papers/2014/hanenbergAl-emse2014.pdf);
selected methods, results, and §7 Summary and Conclusion (PDF pp. 34–35) read. A Scite retrieval
labelled “fulltext” was rejected because the returned body was unrelated
Spanish repository-search help, not this paper.

**Use/limitation:** Directly relevant static-typing/maintainability experiment,
but its task, language pair, participants, and IDE setting are bounded; it is
not an F#/C# idiom comparison or LLM maintenance study.

### R08 — Uesbeck et al. (2016)

**Identity:** Phillip Merlin Uesbeck, Andreas Stefik, Stefan Hanenberg, Jan
Pedersen, and Patrick Daleiden, “An Empirical Study on the Impact of C++ Lambdas
and Programmer Experience,” *ICSE 2016*, pp. 760–771, DOI
[10.1145/2884781.2884849](https://doi.org/10.1145/2884781.2884849).

**Access/extent:** Author/venue copy
[PDF](https://www.cs.kent.edu/~jmaletic/cs63902/Papers/Merlin16.pdf); main read
covered the abstract, §§4.1–4.3, results/discussion excerpts, and §7
limitations (printed article pp. 764–769).

**Use/limitation:** Randomized two-group C++11 human collection-task experiment
comparing lambdas with iterators, useful for expertise/feature-use burden. It
is not a repository feature-frequency or population study, and does not
establish C#/F# equivalence, production maintenance, or an LLM effect.

### R09 — Prechelt (2000)

**Identity:** Lutz Prechelt, “An Empirical Comparison of Seven Programming
Languages,” *Computer* 33(10), 23–29 (2000), DOI
[10.1109/2.876288](https://doi.org/10.1109/2.876288).

**Access/extent:** Author submission dated 2000-03-14
[PDF](https://ps.ipd.kit.edu/downloads/za_2000_empirical_comparison.pdf); read
introduction, methods/validity discussion, and conclusion.

**Use/limitation:** Classic multi-language benchmark useful for separating
language/runtime dimensions, but its benchmark tasks and period predate modern
F#, C#, tooling, and LLM-assisted maintenance; results are not architectural
or long-horizon repository evidence.

### R10 — Nanz & Furia (2015)

**Identity:** Sebastian Nanz and Carlo A. Furia, “A Comparative Study of
Programming Languages in Rosetta Code,” *ICSE 2015*, pp. 778–788, DOI
[10.1109/ICSE.2015.90](https://doi.org/10.1109/ICSE.2015.90). Related preprint:
[10.48550/arXiv.1409.0252](https://doi.org/10.48550/arXiv.1409.0252), v4
2015-01-22.

**Access/extent:** [arXiv v4 PDF](https://arxiv.org/pdf/1409.0252v4) (first
12-page article) was read for selected §II, §III, RQ1/Table 5, §V, and the
appendix measurement definition; the 293-page supplement was not read in full.
The author ETH PDF access failed with HTTP 403 and was not read.

**Use/limitation:** Uses paired small programs from a 2014 Rosetta Code
snapshot, comparing nonblank/noncomment LOC and runtime; the dataset explicitly
includes F# and C#. It is a small-program benchmark from an old snapshot, not
modern architecture, token/context, longitudinal maintenance, or LLM evidence.

### R11 — Ray et al. (2014)

**Identity:** Baishakhi Ray, Daryl Posnett, Vladimir Filkov, and Premkumar
Devanbu, “A Large-Scale Study of Programming Languages and Code Quality in
GitHub,” *ESEC/FSE 2014*, 155–165, DOI
[10.1145/2635868.2635922](https://doi.org/10.1145/2635868.2635922).

**Access/extent:** Authors’ primary [PDF](https://www.cs.ucdavis.edu/~filkov/papers/lang_github.pdf);
selected introduction, methods, and threats read. Do not mix its original
729-project/80M-SLOC analysis with the later CACM 2017 lineage (DOI
10.1145/3126905), which is not independent evidence here.

**Use/limitation:** Large observational language/code-quality study, but
confounding, classification, repository selection, and causal interpretation
limit transfer; it does not compare paired idiomatic F#/C# implementations or
LLM maintenance.

### R12 — Berger et al. (2019)

**Identity:** Emery D. Berger, Celeste Hollenbeck, Petr Maj, Olga Vitek and
Jan Vitek, “On the Impact of Programming Languages on
Code Quality,” *ACM Transactions on Programming Languages and Systems* 41(4),
Article 21, 1–24 (2019), DOI
[10.1145/3340571](https://doi.org/10.1145/3340571).

**Access/extent:** Scite full-text selections read from the published article:
introduction, repetition, reanalysis, threats, and best-practices sections
(retrieval offsets 0, 8000, and 48000; 8000-character windows). Related
preprint [arXiv v2](https://arxiv.org/abs/1901.10220), DOI
[10.48550/arXiv.1901.10220](https://doi.org/10.48550/arXiv.1901.10220), was
verified for identity.

**Use/limitation:** Reanalysis is methodological caution against weak
language-wide causal claims, not an independent new-data replication and not
direct F#/C# or LLM evidence.

### R13 — Ray/Devanbu/Filkov rebuttal (2019)

**Identity:** Baishakhi Ray, Prem Devanbu and Vladimir Filkov,
“Rebuttal to Berger et al., TOPLAS 2019,”
arXiv v1 2019-11-18, DOI
[10.48550/arXiv.1911.07393](https://doi.org/10.48550/arXiv.1911.07393).

**Access/extent:** [v1 abstract](https://arxiv.org/abs/1911.07393v1) only;
no full-text claims are taken from this record.
The record is retained solely to document the published disagreement and source
lineage.

**Use/limitation:** Abstract-only rebuttal cannot adjudicate the underlying
methodological dispute and should not be used as independent empirical support.

### R14 — Berger et al. rebuttal (2019)

**Identity:** Emery D. Berger, Petr Maj, Olga Vitek and Jan Vitek,
“FSE/CACM Rebuttal²: Correcting A Large-Scale Study of Programming Languages
and Code Quality in GitHub,” arXiv v1 2019-11-27, DOI
[10.48550/arXiv.1911.11894](https://doi.org/10.48550/arXiv.1911.11894).

**Access/extent:** [v1 abstract](https://arxiv.org/abs/1911.11894v1) only;
no full-text claims are taken from this record.
It is retained as the second side of the documented disagreement.

**Use/limitation:** Abstract-only access prevents a substantive resolution of
the rebuttal exchange; it supplies provenance/counterposition, not new causal
evidence.

### R15 — Liu et al. (2024), Lost in the Middle

**Identity:** Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele
Bevilacqua, Fabio Petroni, and Percy Liang, “Lost in the Middle: How Language
Models Use Long Contexts,” *Transactions of the Association for Computational
Linguistics* 12, 157–173 (2024), DOI
[10.1162/tacl_a_00638](https://doi.org/10.1162/tacl_a_00638).

**Access/extent:** Published [ACL PDF](https://aclanthology.org/2024.tacl-1.9.pdf)
read for abstract/introduction, §§2.1–2.3, §3.1, §§4.1–4.2, and §5.

**Use/limitation:** Primary context-position/retrieval evidence, but QA and
synthetic retrieval are not repository maintenance, F#/C#, or human expertise;
nominal context length cannot be treated as a provider limit or authored-byte
causal mechanism.

### R16 — REPOEXEC (Le Hai et al., 2025)

**Identity:** Nam Le Hai, Dung Manh Nguyen, and Nghi D. Q. Bui, “On the Impacts
of Contexts on Repository-Level Code Generation,” *Findings of NAACL 2025*,
1496–1524, DOI
[10.18653/v1/2025.findings-naacl.82](https://doi.org/10.18653/v1/2025.findings-naacl.82).

**Access/extent:** [ACL record](https://aclanthology.org/2025.findings-naacl.82/)
and [PDF](https://aclanthology.org/2025.findings-naacl.82.pdf); selected
methods/context construction, results, and limitations read (§§3–6 and
appendix references).

**Use/limitation:** Executable Python repository-level generation shows context
representation trade-offs, but automatic tests, static dependency extraction,
function-level tasks, and Python-only coverage do not establish maintenance or
F#/C# idiom effects.

### R17 — SWE-EVO (Le et al., 2026 preprint)

**Identity:** Tue Le, Minh Vu Thai Pham, Dung Nguyen Manh, Huy Nhat Phan, and
Nghi D. Q. Bui, “SWE-EVO: Benchmarking Coding Agents in Long-Horizon Software
Evolution Scenarios,” arXiv:2512.18470v6 (2026-05-22), DOI
[10.48550/arXiv.2512.18470](https://doi.org/10.48550/arXiv.2512.18470).

**Access/extent:** [v6 abstract](https://arxiv.org/abs/2512.18470v6) and [v6 HTML](https://arxiv.org/html/2512.18470v6);
selected §§3–4, Appendix E, and §6 read. Version is retained explicitly; do
not substitute an earlier indexed revision.

**Use/limitation:** Release-sized Python evolution is not an inherited
candidate chain, human maintenance, or F#/C# comparison; strict rates are
uncertain with only 48 tasks and repository imbalance.

### R18 — ChainSWE (Jin et al., 2026 preprint)

**Identity:** Qirui Jin et al., “ChainSWE: Benchmarking Coding Agents on
Multi-Bug Software Maintenance,” arXiv:2607.02606v2 (2026-09-01), DOI
[10.48550/arXiv.2607.02606](https://doi.org/10.48550/arXiv.2607.02606).

**Access/extent:** [v2 abstract](https://arxiv.org/abs/2607.02606v2) and [v2 HTML](https://arxiv.org/html/2607.02606v2);
selected §§3.2–3.4, §§4.3–4.5, and §5/Tables 2–4 read. Version v2 is the
current retained identity; no older indexed performance figures are substituted.

**Use/limitation:** Closest inherited-state coding-agent precedent, but
Python-only chains (100 chains/304 bugs/54 repositories), solvability screening,
and model-agent execution do not establish F#/C# architecture or human
maintenance effects.

## Query inventory

### Architecture/API web queries (R01–R06)

Exact web queries recorded in the architecture note:

- `"On the Criteria To Be Used in Decomposing Systems into Modules" DOI ACM`
- `"Exploring the Structure of Complex Software Designs" MacCormack DOI PDF`
- `"An Exploratory Study of How Developers Seek, Relate, and Collect Relevant Information" DOI`
- `"The Implications of Method Placement on API Usability" DOI`
- `Green Petre 1996 cognitive dimensions framework PDF DOI`
- `"Usability analysis of visual programming environments" Green Petre DOI 1996`
- `"How do API documentation and static typing affect API usability?" PDF`
- `Endrikat Hanenberg Robbes 2568299 author pdf`

### Context/repository web queries (R15–R18 and screened leads)

Exact routes recorded in the context note:

- `ChainSWE 2607.02606`
- `SWE-EVO 2512.18470`
- `Lost in the Middle long contexts TACL`
- `repository-level code context LLM benchmark`
- `RepoExec repository-level code generation`
- `SWE-QA repository-level code questions`
- `CodeRepoQA 2412.14764`

## Main Scite query and retrieval log

All S1–S7 calls used `search_literature`, `limit=5`, `offset=0`, no year/date
filter, default relevance order and
`user_intent=language_architecture_comparability`, on 2026-09-13. Totals are
backend matches, not unique relevant studies; only the first five results were
inspected for each call. Ranking and database coverage can change. This is a
replayable targeted search record, not an exhaustive search or a preregistered
systematic review. Earlier searches remain separately dated in the
[2026-09-12 literature ledger](maintenance-literature-review-2026-09-12.md).

| ID | Exact query | Reported total / returned | Selected route |
|---|---|---|---|
| S1 | `("programming languages" AND "code quality")` | 3,399 / 5 | Ray/Berger and their related editions |
| S2 | `"empirical comparison" AND ("programming languages" OR "Rosetta Code")` | 1,007 / 5 | Prechelt |
| S3 | `(FSharp OR "F sharp") AND (CSharp OR "C sharp") AND (maintenance OR architecture OR empirical)` | 171 / 5 | No selected direct comparison among these five; music and software-mining noise |
| S4 | `"static typing" AND (maintenance OR experiment)` | 5,292 / 5 | Endrikat et al. |
| S5 | `FSharp AND CSharp AND software` | 5 / 5 | No selected direct comparison among these five |
| S6 | `"Rosetta Code" AND "comparative study"` | 8 / 5 | Nanz/Furia article and preprint |
| S7 | `"static type systems" AND "maintainability"` | 485 / 5 | Hanenberg's conference predecessor as a route to the journal article |

Returned DOI order, including sources not selected for synthesis:

- S1: `10.1145/3340571`, `10.48550/arxiv.1901.10220`,
  `10.1109/saner.2016.112`, `10.1145/2635868.2635922`, `10.1145/3126905`.
- S2: `10.1109/2.876288`, `10.1145/2688204.2688209`,
  `10.1145/2089155.2089159`, `10.15407/pp2016.02-03.026`,
  `10.2298/csis181012035b`.
- S3: `10.48550/arxiv.2604.15512`, `10.1145/3387940.3392160`,
  `10.56620/2587-9731-2019-4-033-067`, `10.12794/metadc1505161`,
  `10.12794/metadc1248480`.
- S4: `10.15439/2018f240`, `10.1145/2568225.2568299`,
  `10.4204/eptcs.66.4`, `10.1145/1640089.1640093`,
  `10.1145/1529282.1529714`.
- S5: `10.48550/arxiv.2604.15512`, `10.1145/3387940.3392160`,
  `10.1109/tla.2015.7350031`, `10.14232/phd.11239`,
  `10.11606/t.8.2022.tde-14022023-123716`.
- S6: `10.48550/arxiv.1409.0252`, `10.1109/icse.2015.90`,
  `10.18293/seke2015-64`, `10.18293/seke2015-064`,
  `10.33166/aetic.2023.03.005`.
- S7: `10.1109/icpc.2012.6240483`, `10.14232/phd.2948`,
  `10.48550/arxiv.2602.17955`, `10.1109/icse.2017.75`,
  `10.1145/3776681`.

Nonselected topical records were screened at title/abstract level. Multilingual
repository quality, novice notation, runtime/energy comparisons, language mining
and related typing studies were not carried forward into this bounded synthesis;
music results are off topic. These exclusions are scope decisions, not findings
that the papers are wrong. Unread leads must not acquire full-text claims in a
later handoff.

Exact-DOI metadata checks used the same limit/offset and no search term:

- M1: `10.1109/icse.2015.90`, `10.1007/s10664-013-9289-1`,
  `10.1109/2.876288`; all three returned.
- M2: `10.1145/1453101.1453117`, `10.1145/2568225.2568299`,
  `10.1145/2884781.2884849`, `10.1145/3340571`,
  `10.1287/mnsc.1060.0552`; all five returned.
- M3: `10.1162/tacl_a_00638`, `10.18653/v1/2025.findings-naacl.82`,
  `10.48550/arxiv.2512.18470`, `10.48550/arxiv.2607.02606`,
  `10.1109/TSE.2006.116`; all five returned.

### Citation graph G1

`citation_graph` used seeds `10.1145/2635868.2635922` and
`10.1145/3340571`, `direction=in`, `depth=1`, `max_edges=30`,
`include_intent=true`, `include_snippets=false`. Scite expanded the latter seed
with `10.48550/arxiv.1901.10220`. It returned 30 edges and 33 nodes, with
`truncated=true`: all 30 edges were allocated to the Ray seed and the other two
seeds were marked low coverage. Zero returned edges for those seeds is not zero
citations. This capped graph cannot support a consensus or absence claim.

R08 was selected from G1 and checked in its primary copy. The following other
non-seed nodes were title-screened leads, not read as empirical support:

```text
10.1002/smr.1760
10.1002/smr.2319
10.1002/spe.2637
10.1007/978-3-030-05767-1_10
10.1007/978-3-030-20883-7_9
10.1007/978-3-030-32101-7_5
10.1007/978-3-030-58951-6_13
10.1007/978-3-319-47166-2_61
10.1007/978-3-319-48989-6_18
10.1007/978-3-319-67256-4_19
10.1007/978-3-319-99617-2_13
10.1145/2771783.2771787
10.1145/2786805.2786815
10.1145/2851613.2851967
10.1145/2884781.2884812
10.1145/2884781.2884848
10.1145/2901739.2901768
10.1145/3030207.3030221
10.1145/3106237.3106297
10.1145/3127005.3127014
10.1145/3131151.3131163
10.1145/3133850.3133851
10.1145/3133850.3133855
10.1145/3133908
10.1145/3136014.3136030
10.1145/3180155.3180208
10.1145/3769694.3771151
10.2139/ssrn.3147521
10.48550/arxiv.2511.07612
```

Potential follow-up leads include the maintainability-prejudices chapter,
Belief & Evidence, and the exploratory Python paradigm/eye-tracking preprint.
Their metadata is not evidence for their findings. The graph was not expanded
recursively to manufacture an exhaustive review.

### Access, edition and screening safeguards

`read_fulltext` checks on R09 and R10 returned abstract fallbacks, with
`contentDenied=true`; substantive reading used the listed primary copies.
R12 returned usable full-text selections at offsets 0, 8000 and 48000, each
requested with length 8000. Those offsets are a retrieval description, not
stable scholarly locators or evidence that the whole article was read.

For R07, `read_fulltext(doi=10.1007/s10664-013-9289-1, offset=0,
length=8000)` labelled the 7,280-character response `source=fulltext` and
`contentDenied=false`, but its body was unrelated repository-search help in
Spanish. That body was excluded. The title-matched author PDF was used instead.
The service's label is not proof of document identity; this incident is not a
criticism or exclusion of the authentic paper.

Related editions are not independent evidence: Nanz/Furia's arXiv record and
ICSE article are one lineage; Berger's arXiv record and TOPLAS article are one
lineage; Ray's FSE and CACM articles are related editions. Hanenberg's
`10.1109/ICPC.2012.6240483` is a conference predecessor, not a fresh replication
of the journal experiment. Rebuttals document disagreement, not new datasets.
R17/R18 claims use the explicitly pinned primary versions; Scite metadata and
indexed text may reflect older editions. No mixed-version performance estimate
is constructed.

Citation statements were interpreted according to their source and target DOI,
not assumed to be endorsements of a search hit. Supporting/contrasting/mentioning
labels and citation totals were not treated as votes on a hypothesis. No papers,
private access URLs, authentication material or copied private transcripts are
checked into this ledger.

## Excluded-but-screened QA leads

These are retained to avoid absence claims but excluded from the main synthesis
because they evaluate repository QA rather than patch outcomes:

- Ruida Hu et al., “CodeRepoQA: A Large-scale Benchmark for Software
  Engineering Question Answering,” arXiv:2412.14764v1, DOI
  [10.48550/arXiv.2412.14764](https://doi.org/10.48550/arXiv.2412.14764).
- Weihan Peng et al., “SWE-QA: Can Language Models Answer Repository-level
  Code Questions?,” *Findings of ACL 2026*, 8230–8245, DOI
  [10.18653/v1/2026.findings-acl.402](https://doi.org/10.18653/v1/2026.findings-acl.402).

Their existence does not imply direct comparability to coding-agent patch
outcomes; no absence claim is made about other QA or maintenance literature.

The QA leads were read in selected methods/results/limitations sections (not
abstract-only): CodeRepoQA v1 §§2–3 and SWE-QA §§2–3 and limitations. Their
reading did not turn QA scores into executable maintenance outcomes.

## Documentation review and reproducibility

Repository context is bound to construction commit
`72b6cf56509364ace74d16b5ef75c6be5ee30338`; this literature addition changes
documentation only. The 18 references are a selected reading set, not 18
independent experiments: it includes conceptual work, related disputes and
preprints.

Another AI session reviewed the synthesis against research notes and selected
primary copies. It flagged an unsupported student description for the Java API
participants and an architecture-specific description of SWE-EVO's failure
taxonomy. Both were corrected and the reviewer confirmed no open findings in
that assigned scope. Bibliographic integration also corrected the unpublished
ledger's Rosetta Code title/scope, C++ experiment description, printed-page
locators and mistaken attribution of earlier-day searches to this search log.
These are documentation corrections, not changes to experimental observations.

The reviewed draft's SHA-256 was
`b2c3268845c647fd36d2ea1fbf64a63ef4cab6766ee93f86497455f7020ad829`;
the corrected, rechecked synthesis SHA-256 is
`f8f640331ecbc374b0f608b975f6e76c96a92514c7550657bde35171d47f0098`.
These are UTF-8 working-file bytes at review, not a claim of identical Windows
checkout line endings. Git records the published source. This is AI source
review, not human architecture validation or a claim to have reproduced the
papers' experiments.

Focused document validation passed strict UTF-8/replacement-character checks,
74 relative file links, all 18 footnote/source IDs and all 18 corresponding
DOI bindings. `git diff --check` and the no-change check over code, tests,
scripts, protocols, benchmarks and CI configuration passed. A first validator
attempt hashed this ledger instead of the synthesis; its corrected report-hash
check passed. No local fixture build or full test suite was needed for these
documentation-only edits. Exact pushed-commit CI remains the publication check,
not a scientific replication of the cited work.

## Evidence boundary

The ledger supports source traceability only. It does not adopt a treatment,
architecture, protocol, proxy, backend, execution plan, or language preference.
The six architecture/API sources support hypotheses about information hiding,
dependency propagation, discoverability, and abstraction trade-offs; R07–R14
provide bounded language-quality/typing/feature and null/counterevidence; R15–R18
provide context/repository-evolution neighbors. None directly measures an
LLM maintaining paired F# and C# implementations in this repository.
