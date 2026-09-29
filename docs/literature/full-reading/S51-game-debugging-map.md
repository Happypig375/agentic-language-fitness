# S51 — Game-debugging map: a bounded search, not absence of prior art

**Full reading completed 2026-09-29.** Adrien Vanègue, Valentin Bourcier, Fabio Petrillo and Steven Costiou, *Debugging Video Games: A Systematic Mapping*, DEBT 2023, DOI [10.1145/3605155.3605865](https://doi.org/10.1145/3605155.3605865). The live question is whether game-debugging practice and temporal verification are sufficiently understood to ground Nu's claimed advantages, and which contrary or closer methods must be followed.

## Edition and actual coverage

Read all ten PDF pages of [HAL v1](https://inria.hal.science/hal-04139070v1): the repository cover and nine manuscript pages, including all sections, the search listing, three plots, the 21-row table and 37 references. MuPDF renders of PDF pages 4, 5 and 10 confirmed the plots, table and consequential bibliography discrepancies. The manuscript still carries a `Conference'17` template header; it is not evidence of a separate 2017 publication. The HAL cover identifies the 2023 workshop and deposit date, 23 June 2023. Publisher pagination is 23–30; complete equivalence to that eight-page proceedings layout was not checked.

Zotero parent `R9VLWGV8`, attachment `ATUR5YZ4`; 666,106 bytes; SHA-256 `983dbe8358cc2b5ee16db61eb44b7ff52b5115d1fa389aec0fa6d94b22364475`. The generated repository-cover date does not turn the paper into a 2026 study. No source code, empirical experiment or review search was reproduced. Referenced studies are discovery leads unless separately read; reading this map does not confer their full-reading status.

## What the search establishes

The research question concerns the state of the art **and practice** of video-game debugging. The authors report one Scopus search using title/abstract/keyword terms for debugging and video/computer games, restricted to computer science: 89 retrieved, 18 selected, plus three from citation follow-up, for **21 included studies**. Inclusion covers bug identification/analysis, debugging techniques and challenges. Exclusion covers studies whose main aim is not game debugging, games used to demonstrate an unrelated topic, and work not peer reviewed.

The stated backward/forward snowballing adds three studies; the account describes initially one backward depth and further references encountered during extraction. It does not give a reproducible per-seed/per-round frontier, a complete excluded list, an explicit search execution date, independent screening assignments, disagreement resolution or an extraction agreement measure. Those are limits of the reported method, not proof that the authors did none of these activities.

Figures 2–3 classify the selected corpus: seven AI approaches, five tools, two lessons-learned reports, two frameworks and five other approaches; eight automatic-detection topics, four visual-debugging topics, three debugging-technique topics and six others. These are **paper counts**, not proportions of developers, debugging work, defects or useful interventions. They do not estimate Nu task prevalence or expected maintenance savings.

The authors acknowledge the narrow query, single database, possible inclusion ambiguity and missing practitioner evidence, and propose broader terms, additional databases and interviews. Their statement that there is no academic/practical body of knowledge should therefore be narrowed to **limited practice evidence and fragmented, context-specific methods in this search**. It cannot establish no prior art, no useful debugging methods or no industry tooling. Section 4 is explicitly an illustrative discussion, not a systematic survey of every debugger evaluated on a game.

## Relevant distinctions and limits

- Temporal monitoring requires observable events and suitable properties; recording/replaying inputs and sampling times is already represented by Perez/Nilsson, S46. Deterministic replay remains conditional on captured inputs, time, random choices, effects and scheduling. Merely choosing a functional language is not the mechanism demonstrated by this map.
- Tool scope differs: FRP games, real-time strategy behavior authoring, network/distributed games, interactive narratives, visual anomalies and particular simulation environments. These are reasons to state transfer boundaries, not to discard close prior art because it does not cover every game.
- Section 4.2 reuses S43's small Pong comprehension task. Our direct S43 reading already establishes its task and intervention limits; the map is not an independent replication. It also reports no measured developer-effectiveness improvement for Timelapse's game example, a consequential contrary lead that needs the original experiment before its result is credited.
- Claims about volatile specifications, weak testing practices and economic constraints are secondary interpretations, principally of Murphy-Hill et al. and testing surveys. They do not establish that test-driven development is impossible, that a particular Nu project avoids these constraints, or that all studios behave similarly. The original practitioner studies are needed before using prevalence or workflow claims.
- Bug detection, explaining a state, localizing a cause, editing a fix, preserving old behavior and reducing total effort are different endpoints. A successful visualization or temporal assertion does not establish complete maintenance success.

## Bounded source discrepancies

Table 1 dates *An Intelligent IDE for Behavior Authoring in Real-Time Strategy Games* to **1993**, while reference 36 dates it to **2021**. The [author-hosted first page](https://sites.cc.gatech.edu/fac/ashwin/papers/er-08-08.pdf) and [AAAI volume](https://aaai.org/proceeding/vol-4-no-1-2008-fourth-artificial-intelligence-and-interactive-digital-entertainment-conference/) identify **AIIDE 2008**. Only identity/first-page information was checked, not that paper's complete methods. Figure 1's earliest-period count must not be used as a verified historical trend. Other dates were not exhaustively repaired, and no corrected chart was invented.

Reference 15 lacks a title/year despite a corresponding table entry. Reference 36's date mismatch and the retained template header reinforce the need for edition and identity checks; they do not invalidate every qualitative observation or the existence of the 21 listed works.

## Consequences and follow-up decisions

**Unique:** generic game replay, temporal assertions and specialized debugging are established topics. This map does not establish novelty for Nu or D1, and limited field coverage cannot rescue a firstness claim.

**Valuable:** practical pain and task diversity are plausible motivations. The source supplies neither representative practice frequencies nor comparative Nu benefit. Keep task prevalence, realistic workflow costs and net benefit unresolved.

**Scientifically valid:** require observable and independently judged behavioral obligations, explicit effect/scheduling boundaries, credible existing tools and tasks across relevant defect families. Do not pool comprehension, visual detection and successful repair as a common outcome. No new experiment is authorized.

Consequential leads retained after the full read:

| Lead | Decision and live question |
| --- | --- |
| S46/S47 FRP testing and verification | Closest temporal-method overlap; continue acquisition/reading. S46's Scite body request returned only an abstract. S47 now has indexed full text through Scite, so its methods are accessible even though attempted PDF routes remain blocked. |
| *Interactive record/replay for web application debugging*, DOI `10.1145/2501988.2502050` | Promote for direct scrutiny of the map's null-effect interpretation and replay/tool costs; exact Scite identity verified. |
| *An Exploratory Literature Study on Live-Tooling in the Game Industry*, LIVE 2019 | Promote for industry-tool coverage and the gap between academic indices and practitioner mechanisms; author preprint and workshop listing identified, no DOI verified, full reading pending. |
| *Cowboys, Ankle Sprains, and Keepers of Quality*, DOI `10.1145/2568225.2568226` | Primary practitioner-method follow-up if claims about game-workflow prevalence are retained; exact identity verified, methods not yet read. |
| Virmani et al. iIDE; other detection, distributed, visual and narrative tools | Retain conditional on a specific mechanism/task claim. Identity correction alone does not justify importing an efficacy result or reading all 21 works indiscriminately. |

The follow-up is claim driven. The 21-paper set is neither a mandatory completion list nor an adequate stopping boundary for the broader Nu question.
