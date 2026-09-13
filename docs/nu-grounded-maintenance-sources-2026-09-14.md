# Nu-grounded methodology: sources and search record

Companion to the [methodological clarification](nu-grounded-maintenance-methodology-2026-09-14.md).
Date: **2026-09-14 HKT**. ALF source:
`7800549dd3ed598a4a7cfda235406ed2114f9537`.

This is bounded methodology/example research, not a systematic review, a
certificate of architecture quality or adoption of a new experiment. Search
hits are title/partial-abstract/excerpt screening unless body reading is stated.
The main agent owns methods and acceptance. A read-only Luna Max worker extracts
local Nu/public-code evidence; that is AI extraction, not human expert review.

## Primary method sources and reading extent

| Source | Verified identity / reading | Use and limitation |
| --- | --- | --- |
| Runeson and Höst, case-study guidelines | [10.1007/s10664-008-9102-8](https://doi.org/10.1007/s10664-008-9102-8), online 2008, journal issue 2009. Main read publisher §§2.1–2.5 and §§3.1–3.3 selected text. Scite served the abstract only; Lund PDF retrieval failed, then publisher HTML supplied methods. | Intentional cases, unit definitions, evidence triangulation and method distinctions. The recommendation applies these principles; no blanket claim that case studies cannot contain quantitative analyses is adopted. |
| Baltes and Ralph, sampling guidance | [10.1007/s10664-021-10072-8](https://doi.org/10.1007/s10664-021-10072-8), 2022; related [10.48550/arXiv.2002.07764](https://doi.org/10.48550/arXiv.2002.07764), [v6, 20 October 2021](https://arxiv.org/html/2002.07764v6). Main read introduction, §§2.1.1–2.1.3 and §6.2; publisher metadata/abstract checked. | Purposive selection versus claims of representativeness. Same study, not independent journal/preprint evidence. **Reject Scite's misassociated journal abstract**, which discussed teaching literature reviews; its fallback body repeated the wrong abstract. Primary sources supplied the relevant text. |
| Bengtsson et al., ALMA | [10.1016/S0164-1212(03)00080-3](https://doi.org/10.1016/S0164-1212(03)00080-3), 2004. Main read author-hosted PDF §§4.1–4.6 selected methods and §8; Scite provided no readable body. | Scenario elicitation, prediction versus stress/comparison goals, impact-analysis limits. Does not itself measure agent maintenance or establish a causal F# advantage. |
| Barr et al., test-oracle survey | [10.1109/TSE.2014.2372785](https://doi.org/10.1109/TSE.2014.2372785), IEEE TSE 2015. Scite partial abstract, author/institutional abstract and indexed PDF front matter read; no full-survey assessment. | Running tests versus determining correct behavior. Its relevance to outside-LLM evaluators is explicitly our inference, not a contemporary LLM result. |

## Published F# system examples

| Work | Primary source / extent | Limit |
| --- | --- | --- |
| Steinlechner, Haaser, Maierhofer and Tobler, *Attribute Grammars for Incremental Scene Graph Rendering* | [10.5220/0007372800770088](https://doi.org/10.5220/0007372800770088), GRAPP/VISIGRAPP 2019, pp. 77–88. Publisher indexed full-paper/landing confirms identity; main read author preprint abstract and §3, especially §§3.1–3.2. | Real mixed F#/C# declarative/incremental graphics architecture, not a controlled maintainability comparison. A second Scite DOI, `10.5220/0007372800002108`, has the same title/authors but unresolved edition relation; not counted as another study or used as the canonical citation. |
| Dzik et al., *MBrace: Cloud Computing with Monads* | [10.1145/2525528.2525531](https://doi.org/10.1145/2525528.2525531), PLOS 2013. Scite exact DOI returned title *MBrace*; indexed project PDF supplies subtitle/authors/front matter and abstract/introduction. Direct PDF and ACM body opens failed. | Example of an implemented F# model/runtime, not reviewed performance or maintainability evidence. No claim about current production support. |

Other retrieved F# leads, including VoxLogicA, F# history, WebSharper/distributed
applications and an SSRN F# game-engine paper, remain unassessed for the specific
architectural-maintenance claim. An SSRN/arXiv identifier alone does not establish
peer review. The F# publications site and project pages supplied discovery leads,
not independent controlled evidence.

## Search limits

No dates, citation thresholds or publication-type filters were used in the Scite
searches below. Requests were relevance ordered, offset zero. Broad `F#`,
`FSharp` and `Aardvark` queries returned many unrelated architecture, imaging,
music and animal records; exact-title/DOI lookup and primary methods were needed.
These noisy results are not evidence that relevant F# work is absent. No search
is claimed to have reached saturation.

The exact phrase `"Nu game engine"` returned zero Scite records. That bounds only
this query/index; it is not a claim that Nu has never appeared in a paper.

| ID | Exact selection | Returned / reported total |
| --- | --- | --- |
| M1 | `("case study" OR "controlled experiment") AND ("software architecture" OR "software maintenance") AND (guidelines OR sampling OR randomization)`; limit 15 | 15 / 10541 |
| M2 | `("F#" OR "F sharp" OR "FSharp") AND ("software architecture" OR "game engine" OR "industrial application" OR "case study")`; limit 20 | 20 / 1000036 |
| M3 | Exact titles: `Guidelines for conducting and reporting case study research in software engineering`; `Sampling in Software Engineering Research: A Critical Review and Guidelines`; `Architecture-level modifiability analysis (ALMA)`; `The Oracle Problem in Software Testing: A Survey`; `The early history of F#`; `Using Functional Programming for Development of Distributed, Cloud and Web Applications in F#`; limit 12 | 7 / 7 |
| M4 | `FSharp AND (architecture OR application OR industrial OR framework)`; limit 15 | 15 / 60 |
| M5 | `("WebSharper" OR "MBrace" OR "Aardvark" OR "FSharp.Data") AND (functional OR programming)`; limit 15 | 15 / 2403 |
| M6 | Exact titles: `Attribute Grammars for Incremental Scene Graph Rendering`; `MBrace: Cloud Computing with Monads`; `VoxLogicA: A Spatial Model Checker for Declarative Image Analysis`; limit 8 | 4 / 4 |
| M7 | Exact DOIs: `10.1145/2525528.2525531`; `10.5220/0007372800770088`; `10.5220/0007372800002108`; limit 5 | 3 / 3 |
| M8 | `"Nu game engine"`; limit 15 | 0 / 0 |

## DOI decision inventory

The initial M1–M8 queries' 79 returned positions contain **74 distinct DOI identifiers**.
Seven identifiers are credited, representing six works after the sampling
journal/preprint pair is collapsed. The other 67 are not credited;
unread relevant leads are not thereby judged low quality. Only selected body
sections of four identifiers were read, as recorded above. Search excerpts
and paper bibliographies are not full-paper reading or additional screened
studies. DOI case is normalized, not a new identity.

| Query/rank | DOI | Retrieved title | Decision and reason |
| --- | --- | --- | --- |
| M1:1 | [10.5220/0004417900250035](https://doi.org/10.5220/0004417900250035) | Transparent Persistence Appears Problematic for Software Maintenance - A Randomized, Controlled Experiment | E — Relevant controlled-maintenance experiment; no full-methods reading needed for selected methodology anchors. |
| M1:2 | [10.14236/ewic/ease2010.13](https://doi.org/10.14236/ewic/ease2010.13) | A Controlled Experiment on Team Meeting Style in Software Architecture Evaluation | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M1:3 | [10.1109/esem.2007.38](https://doi.org/10.1109/esem.2007.38) | The Impact of Group Size on Software Architecture Evaluation: A Controlled Experiment | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M1:4 | [10.1109/icsa.2017.10](https://doi.org/10.1109/icsa.2017.10) | On the Understandability of Semantic Constraints for Behavioral Software Architecture Compliance: A Controlled Experiment | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M1:5 | [10.1109/icse.2005.1553589](https://doi.org/10.1109/icse.2005.1553589) | The value of a usability-supporting architectural pattern in software architecture design: a controlled experiment | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M1:6 | [10.18293/seke2019-232](https://doi.org/10.18293/seke2019-232) | Complex Networks Analysis for Software Architecture: a Case Study on Hibernate (P) | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M1:7 | [10.1109/icsm.2003.1235421](https://doi.org/10.1109/icsm.2003.1235421) | Critical success factors in software maintenance: a case study | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M1:8 | [10.12681/eadd/20666](https://doi.org/10.12681/eadd/20666) | Evaluation and improvement of software architecture | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M1:9 | [10.1016/j.jss.2009.04.052](https://doi.org/10.1016/j.jss.2009.04.052) | Enriching software architecture documentation | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M1:10 | [10.1007/s10664-024-10601-1](https://doi.org/10.1007/s10664-024-10601-1) | Understanding security tactics in microservice APIs using annotated software architecture decomposition models – a controlled experiment | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M1:11 | [10.1007/s10664-007-9052-6](https://doi.org/10.1007/s10664-007-9052-6) | Comparing distributed and face-to-face meetings for software architecture evaluation: A controlled experiment | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M1:12 | [10.21203/rs.3.rs-7499060/v1](https://doi.org/10.21203/rs.3.rs-7499060/v1) | Refactoring in Software Maintenance and Development: Application with Case Study | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M1:13 | [10.1007/978-3-319-09970-5](https://doi.org/10.1007/978-3-319-09970-5) | Software Architecture | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M1:14, M2:9 | [10.1103/physreve.72.026107](https://doi.org/10.1103/physreve.72.026107) | Network motifs in computational graphs: A case study in software architecture | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M1:15 | [10.15224/978-1-63248-044-6-61](https://doi.org/10.15224/978-1-63248-044-6-61) | Measurement of Software Maintenance from User Satisfaction Perspective A Case Study | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M2:1 | [10.1109/iwssd.1998.667926](https://doi.org/10.1109/iwssd.1998.667926) | Performance evaluation of a software architecture: a case study | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M2:2 | [10.1142/s0218194007003410](https://doi.org/10.1142/s0218194007003410) | SOFTWARE ARCHITECTURE DECOMPOSITION USING ATTRIBUTES | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M2:3 | [10.1109/tse.2008.87](https://doi.org/10.1109/tse.2008.87) | Linking Model-Driven Development and Software Architecture: A Case Study | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M2:4 | [10.1145/2371401.2371415](https://doi.org/10.1145/2371401.2371415) | Pushouts in software architecture design | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M2:5 | [10.2139/ssrn.5362782](https://doi.org/10.2139/ssrn.5362782) | Fsge: An Experimental F# Game Engine for 2d Games | E — FSGE F# game-engine lead; SSRN identity alone does not verify peer review, methods unassessed. |
| M2:6 | [10.1007/978-3-031-12597-3_7](https://doi.org/10.1007/978-3-031-12597-3_7) | Exploring Scheduling Algorithms for Parallel Task Graphs: A Modern Game Engine Case Study | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M2:7 | [10.1117/1.jei.22.1.013001](https://doi.org/10.1117/1.jei.22.1.013001) | Software architecture for time-constrained machine vision applications | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M2:8 | [10.1016/b978-0-12-407768-3.00003-3](https://doi.org/10.1016/b978-0-12-407768-3.00003-3) | Software Architecture | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M2:10 | [10.1007/978-1-4842-3153-1_5](https://doi.org/10.1007/978-1-4842-3153-1_5) | Software Architecture | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M2:11 | [10.1007/979-8-8688-0285-0_7](https://doi.org/10.1007/979-8-8688-0285-0_7) | Software Architecture | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M2:12 | [10.1007/978-3-540-39800-4_11](https://doi.org/10.1007/978-3-540-39800-4_11) | Software Architecture and Dependability | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M2:13 | [10.21236/ada441133](https://doi.org/10.21236/ada441133) | Decentralized Software Architecture | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M2:14 | [10.1145/2480361.2371415](https://doi.org/10.1145/2480361.2371415) | Pushouts in software architecture design | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M2:15 | [10.1016/b978-0-12-407768-3.00018-5](https://doi.org/10.1016/b978-0-12-407768-3.00018-5) | Software Architecture Definition | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M2:16 | [10.1504/ijguc.2019.10018612](https://doi.org/10.1504/ijguc.2019.10018612) | Impact of software architecture on execution time: a power window TACLeBench case study | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M2:17 | [10.1109/9780471742036.ch11](https://doi.org/10.1109/9780471742036.ch11) | Software Architecture | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M2:18 | [10.1504/ijguc.2019.098216](https://doi.org/10.1504/ijguc.2019.098216) | Impact of software architecture on execution time: a power window TACLeBench case study | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M2:19 | [10.1002/cpe.6522](https://doi.org/10.1002/cpe.6522) | On the distributed software architecture of a data analysis workflow: A case study | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M2:20 | [10.1007/978-3-540-89694-4_57](https://doi.org/10.1007/978-3-540-89694-4_57) | Genetic Synthesis of Software Architecture | E — Broad-query architecture/case-study lead; not full-methods assessed or used to support this Nu comparison. |
| M3:1 | [10.1007/s10664-008-9102-8](https://doi.org/10.1007/s10664-008-9102-8) | Guidelines for conducting and reporting case study research in software engineering | C — Primary publisher selected methods support intentional case selection, unit definitions, triangulation and random assignment distinction; Scite abstract only. |
| M3:2 | [10.48550/arxiv.2002.07764](https://doi.org/10.48550/arxiv.2002.07764) | Sampling in Software Engineering Research: A Critical Review and Guidelines | C — Primary v6 selected sections on purposive sampling and representativeness; same work as journal DOI, not a replication. |
| M3:3, M5:7 | [10.1145/3386325](https://doi.org/10.1145/3386325) | The early history of F# | E — Relevant F# language-history source; no body audit of implemented-project architecture evidence. |
| M3:4 | [10.1109/tse.2014.2372785](https://doi.org/10.1109/tse.2014.2372785) | The Oracle Problem in Software Testing: A Survey | C — Author/institutional abstract and indexed PDF front matter distinguish test execution from correct-result oracles; not an LLM-era empirical result. |
| M3:5 | [10.1007/s10664-021-10072-8](https://doi.org/10.1007/s10664-021-10072-8) | Sampling in software engineering research: a critical review and guidelines | C — Primary publisher identity/abstract verified; Scite's unrelated abstract rejected. Detailed guidance bound to related v6 preprint. |
| M3:6 | [10.48550/arxiv.1512.01690](https://doi.org/10.48550/arxiv.1512.01690) | Using Functional Programming for Development of Distributed, Cloud and Web Applications in F# | E — Relevant F# distributed/web applications lead; primary abstract only, peer-review status not verified. |
| M3:7 | [10.1016/s0164-1212(03)00080-3](https://doi.org/10.1016/s0164-1212(03)00080-3) | Architecture-level modifiability analysis (ALMA) | C — Author PDF selected scenario-elicitation/impact methods and empirical foundation; no Scite full text. Methodological precedent, not agent-effect evidence. |
| M4:1 | [10.1118/1.3590363](https://doi.org/10.1118/1.3590363) | Image filtering as an alternative to the application of a different reconstruction kernel in CT imaging: Feasibility study in lung cancer screening | E — Cross-field/name-collision or adjacent-method lead; not evidence for the assessed F# architecture question. |
| M4:2 | [10.1111/trf.17092](https://doi.org/10.1111/trf.17092) | National Blood Foundation 2021 Research and Development summit: Discovery, innovation, and challenges in advancing blood and biotherapies | E — Cross-field/name-collision or adjacent-method lead; not evidence for the assessed F# architecture question. |
| M4:3, M6:1 | [10.1007/978-3-030-17462-0_16](https://doi.org/10.1007/978-3-030-17462-0_16) | VoxLogicA: A Spatial Model Checker for Declarative Image Analysis | E — Relevant VoxLogicA F# system lead; architecture methods not assessed in this bounded clarification. |
| M4:4 | [10.48550/arxiv.2603.04270](https://doi.org/10.48550/arxiv.2603.04270) | Grid-agnostic volume of fluid approach with interface sharpening and surface tension for compressible multiphase flows | E — Cross-field/name-collision or adjacent-method lead; not evidence for the assessed F# architecture question. |
| M4:5 | [10.1002/mp.13127](https://doi.org/10.1002/mp.13127) | Towards context‐sensitive CT imaging — organ‐specific image formation for single (SECT) and dual energy computed tomography (DECT) | E — Cross-field/name-collision or adjacent-method lead; not evidence for the assessed F# architecture question. |
| M4:6 | [10.48550/arxiv.2604.15512](https://doi.org/10.48550/arxiv.2604.15512) | Empirical Investigation of Quantum Computing Toolchains and Algorithms : Mining Stack Overflow Repository | E — Cross-field/name-collision or adjacent-method lead; not evidence for the assessed F# architecture question. |
| M4:7 | [10.7202/1014080ar](https://doi.org/10.7202/1014080ar) | "Spells": Jack Behrens: Fiona's Flute. Dialogue. Peter Racine Fricker: Two Spells for Solo Flute. Ballade for Flute and Piano, Op. 68. Bagatelles for Clarinet and Piano, Op. 83. Jack Behrens, piano; Robert Riseling, clarinet; Tsuyoshi Tsutsumi, violoncello; Fiona Wilkinson, flute. Orion Master Recordings ORS 83455 | E — Cross-field/name-collision or adjacent-method lead; not evidence for the assessed F# architecture question. |
| M4:8 | [10.1121/1.2936002](https://doi.org/10.1121/1.2936002) | Smart sound environments: merging intentional soundscapes, nonspeech audio cues and ambient intelligence | E — Cross-field/name-collision or adjacent-method lead; not evidence for the assessed F# architecture question. |
| M4:9 | [10.1109/tla.2015.7350031](https://doi.org/10.1109/tla.2015.7350031) | Biomedical Data Management and Processing -A New Framework | E — Cross-field/name-collision or adjacent-method lead; not evidence for the assessed F# architecture question. |
| M4:10 | [10.5755/j01.itc.43.1.4586](https://doi.org/10.5755/j01.itc.43.1.4586) | Monadic Foundations for Promises in Jason | E — Cross-field/name-collision or adjacent-method lead; not evidence for the assessed F# architecture question. |
| M4:11 | [10.25148/etd.fi14071172](https://doi.org/10.25148/etd.fi14071172) | Hermes, a Concerto for Violoncello and Orchestra | E — Cross-field/name-collision or adjacent-method lead; not evidence for the assessed F# architecture question. |
| M4:12 | [10.1039/c0gc00384k](https://doi.org/10.1039/c0gc00384k) | Heteroatom doped carbons prepared by the pyrolysis of bio-derived amino acids as highly active catalysts for oxygen electro-reduction reactions | E — Cross-field/name-collision or adjacent-method lead; not evidence for the assessed F# architecture question. |
| M4:13 | [10.14418/wes01.1.223](https://doi.org/10.14418/wes01.1.223) | Twentieth-Century Compositional Resources | E — Cross-field/name-collision or adjacent-method lead; not evidence for the assessed F# architecture question. |
| M4:14 | [10.1145/3387940.3392160](https://doi.org/10.1145/3387940.3392160) | Mining Hypernyms Semantic Relations from Stack Overflow | E — Cross-field/name-collision or adjacent-method lead; not evidence for the assessed F# architecture question. |
| M4:15 | [10.55502/the.2021.4.62](https://doi.org/10.55502/the.2021.4.62) | The Great Béla Bartók: An International and Interdisciplinary Perspective | E — Cross-field/name-collision or adjacent-method lead; not evidence for the assessed F# architecture question. |
| M5:1 | [10.1111/j.1439-0264.2012.01169.x](https://doi.org/10.1111/j.1439-0264.2012.01169.x) | Functional Morphology of the Aardvark Tail | E — Cross-field/name-collision or adjacent-method lead; not evidence for the assessed F# architecture question. |
| M5:2 | [10.31219/osf.io/cdbm6](https://doi.org/10.31219/osf.io/cdbm6) | Aardvark: Composite Visualizations of Trees, Time-Series, and Images | E — Cross-field/name-collision or adjacent-method lead; not evidence for the assessed F# architecture question. |
| M5:3 | [10.1080/00970050.1984.10614434](https://doi.org/10.1080/00970050.1984.10614434) | Arnie the Aardvark: An Innovative Cancer Education Program for the Primary Grades | E — Cross-field/name-collision or adjacent-method lead; not evidence for the assessed F# architecture question. |
| M5:4 | [10.1109/tvcg.2024.3456193](https://doi.org/10.1109/tvcg.2024.3456193) | Aardvark: Composite Visualizations of Trees, Time-Series, and Images | E — Cross-field/name-collision or adjacent-method lead; not evidence for the assessed F# architecture question. |
| M5:5 | [10.25959/23222240](https://doi.org/10.25959/23222240) | Sustainable Travel and Tourism: Applying the Green Globe Program to Aardvark Adventures Tasmania | E — Cross-field/name-collision or adjacent-method lead; not evidence for the assessed F# architecture question. |
| M5:6 | [10.3106/mammalstudy.27.121](https://doi.org/10.3106/mammalstudy.27.121) | Functional morphology of the forelimb muscles in an aardvark. | E — Cross-field/name-collision or adjacent-method lead; not evidence for the assessed F# architecture question. |
| M5:8 | [10.25959/23222240.v2](https://doi.org/10.25959/23222240.v2) | Sustainable Travel and Tourism: Applying the Green Globe Program to Aardvark Adventures Tasmania | E — Cross-field/name-collision or adjacent-method lead; not evidence for the assessed F# architecture question. |
| M5:9 | [10.1101/2025.10.03.680257](https://doi.org/10.1101/2025.10.03.680257) | Aardvark: Sifting through differences in a mound of variants | E — Cross-field/name-collision or adjacent-method lead; not evidence for the assessed F# architecture question. |
| M5:10 | [10.1007/s11263-007-0066-8](https://doi.org/10.1007/s11263-007-0066-8) | From Aardvark to Zorro: A Benchmark for Mammal Image Classification | E — Cross-field/name-collision or adjacent-method lead; not evidence for the assessed F# architecture question. |
| M5:11 | [10.25959/23222240.v1](https://doi.org/10.25959/23222240.v1) | Sustainable Travel and Tourism: Applying the Green Globe Program to Aardvark Adventures Tasmania | E — Cross-field/name-collision or adjacent-method lead; not evidence for the assessed F# architecture question. |
| M5:12 | [10.1093/bioinformatics/btad509](https://doi.org/10.1093/bioinformatics/btad509) | AARDVARK: an automated reversion detector for variants affecting resistance kinetics | E — Cross-field/name-collision or adjacent-method lead; not evidence for the assessed F# architecture question. |
| M5:13 | [10.1101/2024.11.09.622767](https://doi.org/10.1101/2024.11.09.622767) | Eye features and retinal photoreceptors of the nocturnal aardvark (Orycteropus afer, Tubulidentata) | E — Cross-field/name-collision or adjacent-method lead; not evidence for the assessed F# architecture question. |
| M5:14 | [10.2514/6.1989-2976](https://doi.org/10.2514/6.1989-2976) | The Aardvark AIS-R Manager's Aide - Knowledge based support for Air Force program managers | E — Cross-field/name-collision or adjacent-method lead; not evidence for the assessed F# architecture question. |
| M5:15 | [10.1007/11940197_14](https://doi.org/10.1007/11940197_14) | Dynamic Architecture Extraction | E — Aardvark namesake architecture-extraction tool, not the verified F# graphics platform. |
| M6:2 | [10.48550/arxiv.1811.05677](https://doi.org/10.48550/arxiv.1811.05677) | VoxLogicA: a Spatial Model Checker for Declarative Image Analysis (Extended Version) | E — Related VoxLogicA extended preprint; methods unassessed, not independent of proceedings. |
| M6:3, M7:2 | [10.5220/0007372800770088](https://doi.org/10.5220/0007372800770088) | Attribute Grammars for Incremental Scene Graph Rendering | C — Canonical publisher identity and author preprint selected implementation sections verify real mixed F#/C# graphics architecture; no maintenance-effect claim. |
| M6:4, M7:3 | [10.5220/0007372800002108](https://doi.org/10.5220/0007372800002108) | Attribute Grammars for Incremental Scene Graph Rendering | E — Same-title/author scene-graph record with unresolved edition relation; canonical publisher DOI used, not an additional study. |
| M7:1 | [10.1145/2525528.2525531](https://doi.org/10.1145/2525528.2525531) | MBrace | C — Scite DOI identity plus indexed project-paper front matter/abstract/introduction verify F# workflow/runtime example; full methods not read. |

## Primary recheck of the candidate gap

Following the user's permission to revise the analysis for research value, the
main agent revisited the primary editions of
[CodeThread v1](https://arxiv.org/html/2606.21804v1),
[Needle in the Repo v1](https://arxiv.org/html/2603.27745v1), and
[SlopCodeBench v2](https://arxiv.org/html/2603.24755v2).
Their DOI identities are [10.48550/arXiv.2606.21804](https://doi.org/10.48550/arXiv.2606.21804),
[10.48550/arXiv.2603.27745](https://doi.org/10.48550/arXiv.2603.27745), and
[10.48550/arXiv.2603.24755](https://doi.org/10.48550/arXiv.2603.24755).
Reading here covered CodeThread's introduction and §§3.1–3.3; Needle's
starter-shaping and dual-oracle methods (§§3.2–3.3) and motivating example;
and SlopCodeBench's inherited-workspace/fresh-conversation method passages.
These are selected sections, not new complete-paper reviews.

CodeThread changes prior authorship; Needle tests compliance with supplied
architectural boundaries; SlopCodeBench tracks agents' evolving implementations.
The proposed extension is to compare plausible, specified architectural
alternatives by subsequent behavioral outcomes. This distinction supports
investigating the gap; it is not an exhaustive absence claim. The
[prior frontier ledger](research-frontier-gap-sources-2026-09-14.md) retains
the broader search, versions and related work. These three identifiers are
additional credited web-primary rechecks, outside the 74 Scite identifiers above.

## Nu source extraction and limits

The user-requested neighboring analysis supplied discovery and a pinned public
Nu checkout. Its private conversations were not used as public empirical data,
quoted, published or modified. Public source identity is
`bryanedds/Nu@064f7ae92a8506689cd91aff5e6804a375d6ef3d`.
One read-only Luna Max worker extracted source leads; the main agent checked
the root README, two empty templates, the stub-world test and commit identity,
and owns the interpretation. This is AI source extraction and self-review,
not human expert validation.

| Public source at that pin | Evidence and boundary |
| --- | --- |
| [Root README](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/ReadMe.md#L5) | Advertises MMCC and ImSim and names both Breakout tutorials. Architectural-quality/promotional claims are not adopted as empirical results. A worker's initially wrong nested README path was caught and corrected before publication. |
| [MMCC empty template](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Nu/Nu.Template.Mmcc.Empty/MyGame.fs#L7) and [ImSim empty template](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Nu/Nu.Template.ImSim.Empty/MyGame.fs#L7) | First-class application styles in one language/engine. The templates differ in behavior/details; no matched maintenance pair is established. |
| [World types](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Nu/Nu/World/WorldTypes.fs#L1939) | Snapshot-oriented state with a mutable wrapper, not purity enforced throughout the engine. |
| [World update branch](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Nu/Nu/World/WorldModule.fs#L297) and [Gaia undo/redo](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Nu/Nu.Gaia/Gaia.fs#L505) | Imperative versus copying paths and snapshot use are concrete design leads. No maintenance benefit was measured. |
| [Event graph](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Nu/Nu/EventGraph/EventGraph.fs#L49) | Event-state organization is inspectable; not a claim that this is event sourcing or a globally pure engine. |
| [Stub-world test](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Nu/Nu.Tests/WorldTests.fs#L15) | Static source calls initialization, a stub world and a one-frame run. This investigation performed no build/run and did not establish a working headless candidate sandbox. |

Curated material did not yield a verified Nu-specific public issue/PR task.
The examples in the methodology note are illustrations, not mined instances.
The extracted [F# compiler PR 772](https://github.com/dotnet/fsharp/pull/772)
and [Lerna issue 1636](https://github.com/lerna/lerna/issues/1636) concern
governance and are excluded as engine-maintenance task evidence. The historical
[Xi lineage](https://github.com/bryanedds/Xi/tree/4de3fd3ad9b9f39a39343d60566fcb13cddec728)
is not an independently authored comparator. No unavailable/private historical
engine is nominated as a public control.


## Follow-up: lineage and research-gap fit

The user clarified that MMCC adapts MVU and ImSim adapts ImGui, and that the
Breakout samples are intended to behave alike. This is retained as user-supplied
design history and intended behavior, not an independently tested result.
The main agent added a concrete, unadopted architecture-by-change-family
hypothesis rather than treating documented ancestry as the contribution.

Two initial Scite requests failed connector validation because `user_intent`
exceeded its configured 100-character maximum. They returned **no search
results**, not zero matches. Both were corrected and succeeded; the successful
queries below have no date/type/citation filters, offset zero.

| ID | Exact selection | Returned / reported total |
| --- | --- | --- |
| M9 | `("model-view-update" OR "immediate mode GUI" OR "immediate-mode GUI")`; limit 15 | 15 / 41 |
| M10 | Exact DOIs `10.4230/LIPIcs.ECOOP.2020.14` and `10.48550/arXiv.1910.11108`; limit 5 | 2 / 2 |

These 17 positions add 15 distinct Scite DOI identifiers to M1–M8:
**96 positions / 89 distinct Scite identifiers** overall. One additional DOI
is credited, 14 excluded; the related preprint/artifact are not separate studies.
At initial screening the whole Scite set credited eight identifiers representing
seven works, after collapsing the sampling journal/preprint pair. The later
user-triggered metadata correction below changes one exclusion to a citation;
do not mistake missing fields for a negative relevance judgment.

| Query/rank | DOI | Title | Decision and reason |
| --- | --- | --- | --- |
| M9:1 | [10.18420/vrar2022_1678](https://doi.org/10.18420/vrar2022_1678) | Exploring the immediate mode GUI concept for graphical user interfaces in mixed reality applications | E — Relevant immediate-mode mixed-reality lead; DOI retrieval failed, no methods or maintenance-effect assessment. |
| M9:2 | [10.31673/2412-9070.2025.022617](https://doi.org/10.31673/2412-9070.2025.022617) | Analysis of approaches to adaptive layout and element identifiers in Immediate Mode GUI for its use in Unity | E — Relevant MVU/IMGUI application lead; title only, no comparative maintenance methods assessed. |
| M9:3 | [10.1145/3550356.3552373](https://doi.org/10.1145/3550356.3552373) | The instance model-view update problem in AADL | E — AADL model/view consistency problem, not the selected MVU GUI architecture comparison. |
| M9:4 | [10.1145/3550355.3552396](https://doi.org/10.1145/3550355.3552396) | Solving the instance model-view update problem in AADL | E — AADL model/view consistency problem, not the selected MVU GUI architecture comparison. |
| M9:5, M10:1 | [10.48550/arxiv.1910.11108](https://doi.org/10.48550/arxiv.1910.11108) | Model-View-Update-Communicate: Session Types meet the Elm Architecture | E — Related extended preprint of the credited ECOOP paper; no independent study or body assessment here. |
| M9:6, M10:2 | [10.4230/lipics.ecoop.2020.14](https://doi.org/10.4230/lipics.ecoop.2020.14) | Model-View-Update-Communicate: Session Types Meet the Elm Architecture | C — Publisher abstract and institutional refereed metadata establish MVU formalization/session-typing lineage; not maintenance-effect evidence. |
| M9:7 | [10.1145/3356590.3356623](https://doi.org/10.1145/3356590.3356623) | A Model-View-Update Framework for Interactive Web Audio Applications | E — Relevant MVU/IMGUI application lead; title only, no comparative maintenance methods assessed. |
| M9:8 | [10.1145/3550356.3559083](https://doi.org/10.1145/3550356.3559083) | OSATE-DIM solves the instance model-view update problem in AADL | E — AADL model/view consistency problem, not the selected MVU GUI architecture comparison. |
| M9:9 | [10.4230/darts.6.2.13](https://doi.org/10.4230/darts.6.2.13) | Model-View-Update-Communicate: Session Types Meet the Elm Architecture (Artifact) | E — Related evaluated artifact, not an independent maintenance experiment; body not read. |
| M9:10 | [10.21105/joss.02791](https://doi.org/10.21105/joss.02791) | s4rdm3x: A Tool Suite to Explore Code to Architecture Mapping Techniques | E — Adjacent application or architecture lead; methods not assessed for the selected maintenance contrast. |
| M9:11 | [10.1145/3394171.3414542](https://doi.org/10.1145/3394171.3414542) | SOMHunter: Lightweight Video Search System with SOM-Guided Relevance Feedback | E — Adjacent application or architecture lead; methods not assessed for the selected maintenance contrast. |
| M9:12 | [10.1109/oceanse.2019.8867434](https://doi.org/10.1109/oceanse.2019.8867434) | Stonefish: An Advanced Open-Source Simulation Tool Designed for Marine Robotics, With a ROS Interface | E — Adjacent application or architecture lead; methods not assessed for the selected maintenance contrast. |
| M9:13 | [10.21504/rur.32900561](https://doi.org/10.21504/rur.32900561) | Demo Elm code for complex interactions and a design pattern to handle them | E — Elm demo/related version, not verified peer-reviewed maintenance evidence. |
| M9:14 | [10.21504/rur.32900561.v1](https://doi.org/10.21504/rur.32900561.v1) | Demo Elm code for complex interactions and a design pattern to handle them | E — Elm demo/related version, not verified peer-reviewed maintenance evidence. |
| M9:15; M11:1 | [10.1117/12.3020480](https://doi.org/10.1117/12.3020480) | Real-time adaptive optics control with a high level programming language | C after user correction — Scite omitted metadata even on exact lookup; Crossref confirms SPIE title/identity, and the related primary preprint establishes combined state-machine/event/ImGui architecture. See correction below; initial exclusion was access-only. |

Fowler's [publisher abstract/metadata](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2020.14)
and [institutional record](https://eprints.gla.ac.uk/223081/) were inspected.
The latter explicitly records refereed status. No full proof or empirical
maintenance evaluation was read or claimed. The related preprint is
`10.48550/arXiv.1910.11108`; the related artifact is
`10.4230/DARTS.6.2.13`. Neither is credited as independent evidence.

The main read the [official Elm architecture overview](https://guide.elm-lang.org/architecture/)
and Dear ImGui's [primary maintainer explanation](https://github.com/ocornut/imgui/wiki/About-the-IMGUI-paradigm),
especially its API/state definition and warning about umbrella terms.
These are practitioner documentation, not peer-reviewed maintenance results.
The Nu README directly attributes ImSim to ImGui; the MMCC-to-MVU historical
attribution here remains the user's statement, supported in form by the code
but not independently established as a historical claim.

A read-only worker inspected the two pinned Breakout trees. Both implement the
same named screens and game genre. The user confirms intended parity. However,
[ImSim gameplay](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Projects/Breakout%20ImSim/Gameplay.fs#L75)
uses physics-body/collision results, while
[MMCC gameplay](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Projects/Breakout%20Mmcc/Gameplay.fs#L85)
updates model coordinates and performs explicit intersection tests.
That difference matters to selecting comparable contracts; it is not proof
that the games fail their intended purpose. UI/control wiring in
[ImSim](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Projects/Breakout%20ImSim/Breakout.fs#L24)
and [MMCC](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Projects/Breakout%20Mmcc/Breakout.fs#L16)
is another possible contrast. No build, gameplay observation, equivalence test,
new task or adapter was performed.

Web follow-up searches were `"Model-View-Update" Fowler ECOOP`,
`"immediate mode" "graphical user interfaces" paper architecture` and
`site:github.com/bryanedds/Nu MMCC MVU`. They provided lineage and related leads,
not a comprehensive novelty search. An accidental placeholder URL open was
rejected and supplied no evidence; the subsequent actual DOI open for
`10.18420/vrar2022_1678` also failed. No absence/quality inference follows.

## Supplementary web access and discovery inventory

Web access was used to obtain primary methods, resolve F# example identities
and recheck the closest prior interventions. It was not a second systematic
database search. The table preserves 72 distinct URLs from the retained web
initial discovery/access responses (W1–W72), followed by 28 lineage-query
and primary-document URLs (W73–W100). Alternate copies of credited papers map to their
DOI decisions above; they are not additional studies. Other entries are
title/snippet-level leads not used for effect claims. An excerpt from another
paper's bibliography is not body reading of either paper.

Access failures retained: Lund's linked guideline PDF and an initial DOI
redirect failed before the canonical publisher HTML succeeded; Scite supplied
no ALMA body; MBrace's direct project PDF/ACM body opens failed; the scene-graph
publisher landing later returned 502 after indexed primary metadata was
available. Sampling's misassociated Scite abstract was rejected. Do not infer
a paper's quality from access failure.

| ID | Web source | Decision / relation to credited work |
| --- | --- | --- |
| W1 | [source](https://mbrace.io/mbrace-plos.pdf) | Primary MBrace indexed paper; credited through its DOI. Direct body open failed. |
| W2 | [source](https://repositum.tuwien.at/bitstream/20.500.12708/2984/2/Rainer%20Bernhard%20-%202017%20-%20Interactive%20shape%20detection%20in%20Out-Of-Core%20point%20clouds...pdf) | Adjacent or cross-field discovery lead; not assessed as evidence for this architectural-maintenance comparison. |
| W3 | [source](https://aardvark-community.github.io/ag-for-scenegraphs/grapp-preprint.pdf) | Primary scene-graph paper/metadata access path; canonical DOI credited, not another study. |
| W4 | [source](https://www.cg.tuwien.ac.at/research/publications/2021/Nowak_2021/Nowak_2021-Master%20Thesis.pdf) | Adjacent or cross-field discovery lead; not assessed as evidence for this architectural-maintenance comparison. |
| W5 | [source](https://link.springer.com/article/10.1007/s11740-022-01133-y) | Adjacent or cross-field discovery lead; not assessed as evidence for this architectural-maintenance comparison. |
| W6 | [source](https://citeseerx.ist.psu.edu/document?doi=48cc75efb2d29e96c0b8db720b3ef5f4224579ba&repid=rep1&type=pdf) | Namesake Aardvark architecture-extraction paper, not the selected graphics platform. |
| W7 | [source](https://nordic.designsociety.org/download-publication/40672/SYNTHESIS%2BOF%2BFUNCTIONAL%2BMODELS%2BFROM%2BUSE%2BCASES%2BUSING%2BTHE%2BSYSTEM%2BSTATE%2BFLOW%2BDIAGRAM%3A%2BA%2BNESTED%2BSYSTEMS%2BAPPROACH) | Adjacent or cross-field discovery lead; not assessed as evidence for this architectural-maintenance comparison. |
| W8 | [source](https://github.com/aardvark-platform/aardvark.rendering/blob/master/AGENTS.md) | Project/platform discovery lead; no comparative maintenance methods assessed at this page. |
| W9 | [source](https://fsharp.org/teaching/research) | Discovery bibliography only; primary paper identities checked separately. |
| W10 | [source](https://aardvarkians.com/) | Project/platform discovery lead; no comparative maintenance methods assessed at this page. |
| W11 | [source](https://websharper.com/) | Project/platform discovery lead; no comparative maintenance methods assessed at this page. |
| W12 | [source](https://www.vrvis.at/en/news-events/news/aardvark-from-a-library-to-an-important-tool-in-visual-computing) | Project/platform discovery lead; no comparative maintenance methods assessed at this page. |
| W13 | [source](https://arxiv.org/abs/1512.01690) | Related F# applications preprint already screened under its Scite DOI; peer-review/architecture-effect claim unverified. |
| W14 | [source](https://www.nature.com/articles/s41586-025-08897-0) | Adjacent or cross-field discovery lead; not assessed as evidence for this architectural-maintenance comparison. |
| W15 | [source](https://portal.research.lu.se/en/publications/adopting-a-component-based-software-architecture-for-an-industria/) | Adjacent or cross-field discovery lead; not assessed as evidence for this architectural-maintenance comparison. |
| W16 | [source](https://journals.sagepub.com/doi/10.1177/1063293X20958930) | Adjacent or cross-field discovery lead; not assessed as evidence for this architectural-maintenance comparison. |
| W17 | [source](https://www.sciencedirect.com/science/article/abs/pii/S0167642324000108) | Adjacent or cross-field discovery lead; not assessed as evidence for this architectural-maintenance comparison. |
| W18 | [source](https://www.nuget.org/packages/Aardvark.Base.Incremental/5.3.19) | Project/platform discovery lead; no comparative maintenance methods assessed at this page. |
| W19 | [source](https://developers.websharper.com/docs/v4.x/cs/overview.html) | Project/platform discovery lead; no comparative maintenance methods assessed at this page. |
| W20 | [source](https://en.wikipedia.org/wiki/MBrace) | Secondary listing/discussion or namesake result; not used as primary architectural-effect evidence. |
| W21 | [source](https://en.wikipedia.org/wiki/Multitier_programming) | Secondary listing/discussion or namesake result; not used as primary architectural-effect evidence. |
| W22 | [source](https://en.wikipedia.org/wiki/TFX_Program) | Secondary listing/discussion or namesake result; not used as primary architectural-effect evidence. |
| W23 | [source](https://arxiv.org/abs/1501.04935) | Adjacent or cross-field discovery lead; not assessed as evidence for this architectural-maintenance comparison. |
| W24 | [source](https://arxiv.org/abs/2007.12082) | Adjacent or cross-field discovery lead; not assessed as evidence for this architectural-maintenance comparison. |
| W25 | [source](https://arxiv.org/abs/2303.10025) | Adjacent or cross-field discovery lead; not assessed as evidence for this architectural-maintenance comparison. |
| W26 | [source](https://www.reddit.com/r/fsharp/comments/hj4aj4) | Secondary listing/discussion or namesake result; not used as primary architectural-effect evidence. |
| W27 | [source](https://en.wikipedia.org/wiki/General_Dynamics%E2%80%93Boeing_AFTI/F-111A_Aardvark) | Secondary listing/discussion or namesake result; not used as primary architectural-effect evidence. |
| W28 | [source](https://www.reddit.com/r/fsharp/comments/1oveyag) | Secondary listing/discussion or namesake result; not used as primary architectural-effect evidence. |
| W29 | [source](https://en.wikipedia.org/wiki/General_Dynamics_F-111_Aardvark) | Secondary listing/discussion or namesake result; not used as primary architectural-effect evidence. |
| W30 | [source](https://en.wikipedia.org/wiki/Aardvark_%28disambiguation%29) | Secondary listing/discussion or namesake result; not used as primary architectural-effect evidence. |
| W31 | [source](https://link.springer.com/article/10.1007/s10664-021-10072-8) | Primary sampling-paper access path; credited through its journal/preprint DOI records, not an additional study. |
| W32 | [source](https://portal.research.lu.se/en/publications/guidelines-for-conducting-and-reporting-case-study-research-in-so/) | Alternate copy/listing of the credited case-study guidelines; primary publisher used, not another study. |
| W33 | [source](https://www.cs.vu.nl/~hans/publications/y2004/alma.pdf) | Primary ALMA methods PDF; credited through the ALMA DOI, not an additional study. |
| W34 | [source](https://arxiv.org/abs/2002.07764) | Primary sampling-paper access path; credited through its journal/preprint DOI records, not an additional study. |
| W35 | [source](https://www.researchgate.net/publication/220277640_Hst_M_Guidelines_for_Conducting_and_Reporting_Case_Study_Research_in_Software_Engineering_Empirical_Software_Engineering_14_131-164) | Alternate copy/listing of the credited case-study guidelines; primary publisher used, not another study. |
| W36 | [source](https://springerlink.fh-diploma.de/article/10.1007/s10664-008-9102-8) | Alternate copy/listing of the credited case-study guidelines; primary publisher used, not another study. |
| W37 | [source](https://doi.org/10.1007/s10664-008-9102-8) | Alternate copy/listing of the credited case-study guidelines; primary publisher used, not another study. |
| W38 | [source](https://www.scitepress.org/publishedPapers/2019/73728/pdf/index.html) | Primary scene-graph paper/metadata access path; canonical DOI credited, not another study. |
| W39 | [source](https://www.scitepress.org/PublishedPapers/2019/73728/) | Primary scene-graph paper/metadata access path; canonical DOI credited, not another study. |
| W40 | [source](https://www.cse.chalmers.se/~feldt/advice/runeson_2009_emse_case_study_guidelines.pdf) | Alternate copy/listing of the credited case-study guidelines; primary publisher used, not another study. |
| W41 | [source](https://www.researchgate.net/publication/370788967_Attribute_Grammars_for_Incremental_Scene_Graph_Rendering) | Secondary listing of the unresolved same-title scene-graph edition; canonical publisher DOI used. |
| W42 | [source](https://www.scitepress.org/Papers/2019/73728/73728.pdf) | Primary scene-graph paper/metadata access path; canonical DOI credited, not another study. |
| W43 | [source](https://www.csc.ncsu.edu/research/colloquia/2011-12/unrestricted_media/2011-10-21_Runeson_slides.pdf) | Alternate copy/listing of the credited case-study guidelines; primary publisher used, not another study. |
| W44 | [source](https://www.lu.se/publikation/216a6bb2-bb55-4f2a-a9a1-a4079268ae80) | Alternate copy/listing of the credited case-study guidelines; primary publisher used, not another study. |
| W45 | [source](https://portal.research.lu.se/en/publications/tutorial-case-studies-in-software-engineering) | Adjacent or cross-field discovery lead; not assessed as evidence for this architectural-maintenance comparison. |
| W46 | [source](https://portal.research.lu.se/sv/publications/guidelines-for-conducting-and-reporting-case-study-research-in-so/) | Alternate copy/listing of the credited case-study guidelines; primary publisher used, not another study. |
| W47 | [source](https://scispace.com/papers/guidelines-for-conducting-and-reporting-case-study-research-q10xdzyou5) | Alternate copy/listing of the credited case-study guidelines; primary publisher used, not another study. |
| W48 | [source](https://lup.lub.lu.se/search/publication/216a6bb2-bb55-4f2a-a9a1-a4079268ae80) | Alternate copy/listing of the credited case-study guidelines; primary publisher used, not another study. |
| W49 | [source](https://publications.lib.chalmers.se/records/fulltext/238429/238429.pdf) | Adjacent or cross-field discovery lead; not assessed as evidence for this architectural-maintenance comparison. |
| W50 | [source](https://odr.chalmers.se/bitstreams/0e0e6355-0c3f-4387-87c7-caf1aa82eb05/download) | Adjacent or cross-field discovery lead; not assessed as evidence for this architectural-maintenance comparison. |
| W51 | [source](https://link.springer.com/article/10.1007/s10664-008-9102-8) | Alternate copy/listing of the credited case-study guidelines; primary publisher used, not another study. |
| W52 | [source](https://arxiv.org/html/2002.07764v6) | Primary sampling-paper access path; credited through its journal/preprint DOI records, not an additional study. |
| W53 | [source](https://discovery.ucl.ac.uk/id/eprint/1471263/) | Alternate oracle-survey copy/listing; canonical DOI credited using institutional/author abstract and indexed front matter. |
| W54 | [source](https://www.researchgate.net/publication/276255185_The_Oracle_Problem_in_Software_Testing_A_Survey) | Alternate oracle-survey copy/listing; canonical DOI credited using institutional/author abstract and indexed front matter. |
| W55 | [source](https://philmcminn.com/publications/barr2015.pdf) | Alternate oracle-survey copy/listing; canonical DOI credited using institutional/author abstract and indexed front matter. |
| W56 | [source](https://discovery.ucl.ac.uk/id/eprint/1471263/1/06963470.pdf) | Alternate oracle-survey copy/listing; canonical DOI credited using institutional/author abstract and indexed front matter. |
| W57 | [source](https://web.eecs.umich.edu/~weimerw/2025-481F/readings/testoracles.pdf) | Alternate oracle-survey copy/listing; canonical DOI credited using institutional/author abstract and indexed front matter. |
| W58 | [source](https://philmcminn.com/publications/) | Adjacent or cross-field discovery lead; not assessed as evidence for this architectural-maintenance comparison. |
| W59 | [source](https://dblp.org/rec/journals/tse/BarrHMSY15.html) | Alternate oracle-survey copy/listing; canonical DOI credited using institutional/author abstract and indexed front matter. |
| W60 | [source](https://bishtref.com/articles/10.1109/tse.2014.2372785) | Alternate oracle-survey copy/listing; canonical DOI credited using institutional/author abstract and indexed front matter. |
| W61 | [source](https://dspace.usthb.dz/items/43d5fb71-d468-4877-83c4-cfc0bfe4cc2d/full) | Alternate oracle-survey copy/listing; canonical DOI credited using institutional/author abstract and indexed front matter. |
| W62 | [source](https://philmcminn.com/publications/oracles) | Adjacent or cross-field discovery lead; not assessed as evidence for this architectural-maintenance comparison. |
| W63 | [source](https://pure.kaist.ac.kr/en/publications/the-oracle-problem-in-software-testing-a-survey/) | Alternate oracle-survey copy/listing; canonical DOI credited using institutional/author abstract and indexed front matter. |
| W64 | [source](https://dspace.usthb.dz/items/43d5fb71-d468-4877-83c4-cfc0bfe4cc2d) | Alternate oracle-survey copy/listing; canonical DOI credited using institutional/author abstract and indexed front matter. |
| W65 | [source](https://explore.metascienceobservatory.org/papers/W2041713059) | Alternate oracle-survey copy/listing; canonical DOI credited using institutional/author abstract and indexed front matter. |
| W66 | [source](https://www.mendeley.com/catalogue/f6b6c74e-6a25-3c31-a8d1-d39b9e830ad4/) | Alternate oracle-survey copy/listing; canonical DOI credited using institutional/author abstract and indexed front matter. |
| W67 | [source](https://scispace.com/papers/the-oracle-problem-in-software-testing-a-survey-45arxvh6yl?references_page=10) | Alternate oracle-survey copy/listing; canonical DOI credited using institutional/author abstract and indexed front matter. |
| W68 | [source](https://orbilu.uni.lu/bitstream/10993/48254/1/rwemalika-thesis.pdf) | Adjacent or cross-field discovery lead; not assessed as evidence for this architectural-maintenance comparison. |
| W69 | [source](https://prl.korea.ac.kr/papers/icse23-diver.pdf) | Adjacent or cross-field discovery lead; not assessed as evidence for this architectural-maintenance comparison. |
| W70 | [source](https://idus.us.es/server/api/core/bitstreams/de5bdd89-22e6-4bdf-b793-d07a93d8744e/content) | Adjacent or cross-field discovery lead; not assessed as evidence for this architectural-maintenance comparison. |
| W71 | [source](https://en.wikipedia.org/wiki/Test_oracle) | Secondary listing/discussion or namesake result; not used as primary architectural-effect evidence. |
| W72 | [source](https://en.wikipedia.org/wiki/Fuzzing) | Secondary listing/discussion or namesake result; not used as primary architectural-effect evidence. |
| W73 | [source](https://github.com/bryanedds/Nu) | Moving repository landing page; architectural claims are bound to the inspected pinned public source instead. |
| W74 | [source](https://eprints.gla.ac.uk/223081/) | MVU publication/preprint access path; ECOOP DOI credited, not an independent study or proof of a Nu maintenance effect. |
| W75 | [source](https://www.research.ed.ac.uk/files/150064590/Model_View_Update_Communicate_FOWLER_DOA08042020_AFV.pdf) | MVU publication/preprint access path; ECOOP DOI credited, not an independent study or proof of a Nu maintenance effect. |
| W76 | [source](https://www.researchgate.net/publication/394461243_ALGORITHM_AND_SOFTWARE_IMPLEMENTATION_OF_IMMEDIATE_MODE_INTERFACE_FOR_VISUALIZATION_SYSTEMS) | Adjacent or secondary discovery lead; not used as evidence of architecture-specific maintenance effects. |
| W77 | [source](https://drops.dagstuhl.de/storage/00lipics/lipics-vol166-ecoop2020/LIPIcs.ECOOP.2020.14/LIPIcs.ECOOP.2020.14.pdf) | MVU publication/preprint access path; ECOOP DOI credited, not an independent study or proof of a Nu maintenance effect. |
| W78 | [source](https://arxiv.org/abs/1910.11108) | MVU publication/preprint access path; ECOOP DOI credited, not an independent study or proof of a Nu maintenance effect. |
| W79 | [source](https://solhsa.com/files/atanua080326.pdf) | Practitioner/thesis implementation lead; no controlled maintenance-effect methods assessed. |
| W80 | [source](https://en.wikipedia.org/wiki/Immediate_mode_%28computer_graphics%29) | Adjacent or secondary discovery lead; not used as evidence of architecture-specific maintenance effects. |
| W81 | [source](https://pretalx.com/juliacon-2022/talk/GXTYSA/) | Practitioner/thesis implementation lead; no controlled maintenance-effect methods assessed. |
| W82 | [source](https://www.dreamler.com/blog/immediate-mode-graphical-user-interface-imgui/) | Practitioner/thesis implementation lead; no controlled maintenance-effect methods assessed. |
| W83 | [source](https://git.lmao.ch/mirrors/Nuklear/src/commit/af049ba0ad6a2f2b97433dee89e246c97869694a) | Adjacent or secondary discovery lead; not used as evidence of architecture-specific maintenance effects. |
| W84 | [source](https://gist.github.com/bryanedds?direction=asc&sort=updated) | Adjacent or secondary discovery lead; not used as evidence of architecture-specific maintenance effects. |
| W85 | [source](https://www.researchgate.net/publication/2953839_Composing_User_Interfaces_with_InterViews) | Adjacent or secondary discovery lead; not used as evidence of architecture-specific maintenance effects. |
| W86 | [source](https://unresearch.ing/ggui_retro) | Adjacent or secondary discovery lead; not used as evidence of architecture-specific maintenance effects. |
| W87 | [source](https://ru.wikipedia.org/wiki/%D0%93%D1%80%D0%B0%D1%84%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9_%D0%B8%D0%BD%D1%82%D0%B5%D1%80%D1%84%D0%B5%D0%B9%D1%81_%D0%BD%D0%B5%D0%BC%D0%B5%D0%B4%D0%BB%D0%B5%D0%BD%D0%BD%D0%BE%D0%B3%D0%BE_%D1%80%D0%B5%D0%B6%D0%B8%D0%BC%D0%B0) | Adjacent or secondary discovery lead; not used as evidence of architecture-specific maintenance effects. |
| W88 | [source](https://github.com/geon2419/imgui) | Adjacent or secondary discovery lead; not used as evidence of architecture-specific maintenance effects. |
| W89 | [source](https://studfile.net/preview/429264/page%3A3/) | Adjacent or secondary discovery lead; not used as evidence of architecture-specific maintenance effects. |
| W90 | [source](https://handwiki.org/wiki/Immediate_mode_GUI) | Adjacent or secondary discovery lead; not used as evidence of architecture-specific maintenance effects. |
| W91 | [source](https://www.reddit.com/r/C_Programming/comments/1gamtnc) | Adjacent or secondary discovery lead; not used as evidence of architecture-specific maintenance effects. |
| W92 | [source](https://de.wikipedia.org/wiki/Model_View_Update) | Adjacent or secondary discovery lead; not used as evidence of architecture-specific maintenance effects. |
| W93 | [source](https://en.wikipedia.org/wiki/List_of_widget_toolkits) | Adjacent or secondary discovery lead; not used as evidence of architecture-specific maintenance effects. |
| W94 | [source](https://en.wikipedia.org/wiki/Casey_Muratori) | Adjacent or secondary discovery lead; not used as evidence of architecture-specific maintenance effects. |
| W95 | [source](https://en.wikipedia.org/wiki/X_Window_System) | Adjacent or secondary discovery lead; not used as evidence of architecture-specific maintenance effects. |
| W96 | [source](https://arxiv.org/abs/2207.12701) | Adjacent or secondary discovery lead; not used as evidence of architecture-specific maintenance effects. |
| W97 | [source](https://arxiv.org/abs/2409.00921) | Typed-hole MVU benchmark already assessed in the frontier ledger; not newly body-read or counted as proof of MMCC/ImSim effects. |
| W98 | [source](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2020.14) | MVU publication/preprint access path; ECOOP DOI credited, not an independent study or proof of a Nu maintenance effect. |
| W99 | [source](https://github.com/ocornut/imgui/wiki/About-the-IMGUI-paradigm) | Primary maintainer API/state definition and limits of umbrella labels; practitioner rationale, not controlled maintenance evidence. |
| W100 | [source](https://guide.elm-lang.org/architecture/) | Official architecture overview: model, view and message-driven updates, with practice-origin account; no maintenance-effect validation. |

## User-triggered metadata correction

After the first citation audit closed, the user supplied the missing title for
`10.1117/12.3020480`. An exact Scite lookup (M11, `dois` containing only
that DOI, limit 1) again returned one record with no title, an empty abstract
and `contentDenied=true`. Therefore the metadata problem persisted through
two queries; whether it is temporary or an indexing/connector defect is
undetermined. It is not an evidence-based exclusion for relevance or quality.
M11 raises the search-position total to **97**, leaving **89** distinct Scite
DOIs. The corrected Scite decisions are nine credited / 80 excluded.

The [Crossref DOI record](https://api.crossref.org/works/10.1117%2F12.3020480)
verifies *Real-time adaptive optics control with a high level programming
language*, SPIE, *Adaptive Optics Systems IX*, published 3 September 2024.
The user correction is accepted after that independent identity check.
Direct DOI/publisher opening failed. Main read the
[primary preprint v1](https://arxiv.org/html/2407.07207v1),
[10.48550/arXiv.2407.07207](https://doi.org/10.48550/arXiv.2407.07207),
especially the introduction and §§2.4–2.5. This is a related edition, not a
second independent system study or a full-paper review.

The Julia system combines hierarchical state machines, event messages and
Dear ImGui. This is a concrete counterexample to a false binary between
explicit-state architecture and immediate-mode interfaces. It does not measure
agent maintenance or establish a superiority claim. The methodology note was
refined accordingly: compare source-level responsibility placement, not
umbrella categories. The original access-only exclusion and its reason remain
identifiable in the first audit; the corrected row and audit supersede it.

The related [ALMA experience paper](https://doi.org/10.1016/S0164-1212(01)00113-3)
was also considered at publisher abstract/intro level earlier and not credited
beyond the selected 2004 ALMA methods anchor. It is separately recorded in the
audit, outside the Scite-retrieved DOI set.

The correction's additional retrieval paths are below. Primary-paper/registry
URLs map to their credited DOI; secondary listings and bibliography-only hits
are not additional evidence.

| Source | Relation / decision |
| --- | --- |
| [source](https://arxiv.org/abs/2407.07207) | Primary preprint access path; credited through its DOI, not an additional study. |
| [source](https://www.researchgate.net/publication/382145370_Real-time_adaptive_optics_control_with_a_high_level_programming_language) | Metadata/discussion/discovery or unrelated bibliography result; paper interpretation uses the primary preprint and Crossref identity. |
| [source](https://jglobal.jst.go.jp/public/202402201189429880) | Metadata/discussion/discovery or unrelated bibliography result; paper interpretation uses the primary preprint and Crossref identity. |
| [source](https://www.researchgate.net/publication/383718249_Real-time_adaptive_optics_control_with_a_high_level_programming_language) | Metadata/discussion/discovery or unrelated bibliography result; paper interpretation uses the primary preprint and Crossref identity. |
| [source](https://www.researchgate.net/profile/Olivier-Lardiere) | Metadata/discussion/discovery or unrelated bibliography result; paper interpretation uses the primary preprint and Crossref identity. |
| [source](https://www.emergentmind.com/papers/2407.07207) | Metadata/discussion/discovery or unrelated bibliography result; paper interpretation uses the primary preprint and Crossref identity. |
| [source](https://www.spiecareercenter.org/documents/ConferencesExhibitions/Programs/2024/AS24-Technical-Program-Exhibit-Guide.pdf) | Metadata/discussion/discovery or unrelated bibliography result; paper interpretation uses the primary preprint and Crossref identity. |
| [source](https://discourse.julialang.org/t/case-study-real-time-hardware-control-for-adaptive-optics-with-julia/117155) | Metadata/discussion/discovery or unrelated bibliography result; paper interpretation uses the primary preprint and Crossref identity. |
| [source](https://www.proceedings.com/content/076/076780webtoc.pdf) | Metadata/discussion/discovery or unrelated bibliography result; paper interpretation uses the primary preprint and Crossref identity. |
| [source](https://www.researchgate.net/figure/Schematic-of-the-RTC-pipeline-configured-for-the-SPIDERS-instrument-14-17_fig1_382145370) | Metadata/discussion/discovery or unrelated bibliography result; paper interpretation uses the primary preprint and Crossref identity. |
| [source](https://scirate.com/search?q=au%3ALardiere_O+in%3Aastro-ph) | Metadata/discussion/discovery or unrelated bibliography result; paper interpretation uses the primary preprint and Crossref identity. |
| [source](https://discourse.julialang.org/t/how-to-create-standalone-applications-for-windows-with-a-g-ui-in-julia-1-11-or-1-12/127823?page=3) | Metadata/discussion/discovery or unrelated bibliography result; paper interpretation uses the primary preprint and Crossref identity. |
| [source](https://jglobal.jst.go.jp/en/public/202402201189429880) | Metadata/discussion/discovery or unrelated bibliography result; paper interpretation uses the primary preprint and Crossref identity. |
| [source](https://discourse.julialang.org/t/how-to-create-standalone-applications-for-windows-with-a-g-ui-in-julia-1-11-or-1-12/127823/75) | Metadata/discussion/discovery or unrelated bibliography result; paper interpretation uses the primary preprint and Crossref identity. |
| [source](https://accelresearching.com/accel-zinc-picolinate-50mg/?_=%2Fsearch%2F%23nLw79nwZb1b3uPkZUsgpm5M%3D&query=Marois%2C+C&searchtype=author) | Metadata/discussion/discovery or unrelated bibliography result; paper interpretation uses the primary preprint and Crossref identity. |
| [source](https://www.seruvenyayinevi.com/Webkontrol/uploads/Fck/socialaralk2024_2.pdf) | Metadata/discussion/discovery or unrelated bibliography result; paper interpretation uses the primary preprint and Crossref identity. |
| [source](https://wacci2024.github.io/assets/files/AbstractBookWACCI2024.pdf) | Metadata/discussion/discovery or unrelated bibliography result; paper interpretation uses the primary preprint and Crossref identity. |
| [source](https://arxiv.org/html/2407.07207v1) | Primary preprint access path; credited through its DOI, not an additional study. |
| [source](https://api.crossref.org/works/10.1117%2F12.3020480) | Registry title, publisher, venue and publication date credited through SPIE DOI, not a separate work. |

## Closed source-decision audits and checks

Initial answer ID `alf-nu-grounded-methodology-2026-09-14` recorded
**15 credited / 183 excluded / 0 skipped**, with 198 screened source identities.
This snapshot predates the user's adaptive-optics metadata correction.

The complete corrected answer ID
`alf-nu-grounded-methodology-corrected-2026-09-14` supersedes those decisions:
**17 credited / 201 excluded / 0 skipped**, with 218 screened source identities.
Its answer-scoped verification is untruncated, has no missing reasons and
`retrieval_unlinked=false`. The tool's retrieved total is null for an
answer-scoped report, not zero and not proof of search completeness.

The corrected set contains 89 Scite DOI identities, 123 web-source identities,
five `other` identities (pinned public code, three source-discovery leads and
Crossref), and one attributed user clarification. The 17 credited identities
include 13 publication/preprint DOIs representing 11 works after the sampling
and adaptive-optics edition pairs are collapsed, two primary practitioner
documents, one pinned codebase and one user-intent attribution. These are not
17 independent empirical studies. Eleven decisions use the tool's
`full_text` stage for selected paper/code/document reading, not eleven
completely read papers. Do not add the two audit totals together.

Main-agent self-review checked claim boundaries, primary versus practitioner
evidence, treatment versus author/engine confounding, intended versus tested
parity, architectural compatibility and the future-gold/live hold. The worker's
read-only source extraction is separate AI evidence, not human review. Local
validation passed 11 CI-routing regressions and strict UTF-8/local-link checks;
final whitespace validation and CI are tied to the exact publication. No engine
build, fixture reconstruction, candidate execution, model/count call, OAuth
staging or scientific treatment was run or changed.
