# S89 — Information hiding, changeable decisions and physical implementation

**Complete journal reading, 2026-09-30.** D. L. Parnas, *On the Criteria To Be Used in Decomposing Systems into Modules*, Communications of the ACM 15(12), 1053–1058 (December 1972), [DOI 10.1145/361598.361623](https://doi.org/10.1145/361598.361623). Zotero parent `BI6JDWHB`, PDF `SSAJ46EJ`, note `GIXWRS9Z`.

All six publisher pages, API descriptions, eleven references and footnotes were read in text and rendered images; there are no numbered figures or tables. The [university-hosted journal copy](https://john.cs.olemiss.edu/~hcc/csci555/notes/localcopy/Parnas_Criteria_Decomposing.pdf) has 586,637 bytes, SHA-256 `b3eafb67d5a9f91d5996ccf953e44297b72cee4b8e732dbf28caa3c29e233001`. The earlier 1971 technical report and later anthology/deposit editions were identified but not fully read or compared. No implementation, user experiment or performance result was reproduced.

## Mechanism and relevant distinction

B01/B02/B05/B06/B11 concern the origins of change-locality arguments, the difference between architectural and language claims, and implementation costs. Here, a module is a **responsibility assignment**, not necessarily a function, class, separately compiled file or runtime object. The objective is to isolate difficult or likely-to-change decisions behind interfaces, permitting work on each part with less knowledge of other implementations. This is established prior reasoning for evolution; it is not a distinct Nu invention.

The KWIC example accepts lines of words and prints their circular shifts in alphabetic order. One decomposition follows processing stages: input, circular shifting, alphabetizing, output and control. Its stages share concrete storage/index representations. The alternative adds a line-storage abstraction, with character/word access and mutation operations, and accesses shifts/order through specified operations. It hides whether representations are packed, stored wholly in memory, precomputed or generated on demand.

The paper explicitly allows both designs to use identical algorithms and representations, even identical assembled executable code. What changes is the partition into work assignments and the information exposed at boundaries. This distinguishes a source-organization claim from a physical layout/runtime claim. It does not establish that arbitrary alternative Nu packages are behaviorally equivalent or have the same execution costs.

## Reconstructed change scenarios and limits

| Anticipated change | Conventional decomposition | Information-hiding decomposition |
| --- | --- | --- |
| Input format | Local to input | Local to input; no claimed advantage for this case |
| Keeping all lines in memory | Shared representation affects multiple stages | Intended to remain within line storage |
| Character packing/layout | Other stages know the layout | Intended to remain within line storage |
| Storing versus computing circular shifts | Shift, alphabetizer and output interfaces expose the choice | Intended to remain behind shift operations |
| Eager versus incremental/on-demand ordering | Output assumes a completed index | Ordering operations can hide when work happens |

These are source-level arguments about selected anticipated changes, not measured rates over a sampled future-change distribution. They depend on preserving the external contract. Choosing the relevant decisions is itself design work; the paper does not validate a prospective selector, estimate its cost or establish how often those changes occur in practice. It acknowledges that this small system does not itself exhibit all the large-project problems used to motivate the example.

Parnas also diagnoses a flaw in his own alternative interface: it unnecessarily fixes the enumeration order of circular shifts. That rules out producing shifts already sorted, where alphabetization could do nothing. A revised contract would preserve which shifts exist, uniqueness and a way to find the originating line while hiding their order. This is a concrete example of an abstraction's **semantic contract** restricting evolution even when internal storage is hidden. The revised interface is a design argument, not a reported randomized comparison or an automatically verified refactoring.

The APIs include setters/deletion and required setup calls: `CSSETUP` precedes shift queries and `ALPH` precedes ordered lookup. Information hiding here is compatible with mutation and has temporal preconditions. It is not equivalent to immutable state or a proof that well-typed calls preserve all old/new obligations. More precise module specifications are delegated to other publications.

## Performance, reuse and evidence class

Fine-grained access implemented through elaborate procedure calls can be substantially slower than the stage-oriented design. The proposed remedy is to maintain a useful source representation while compiling/assembling efficient inline code or specialized transfers. The paper calls for tooling that maintains the mapping between these representations; it supplies no quantitative overhead, memory, build-time or maintenance-cost comparison. Read this alongside Casanova's generated implementation and S79/S80's compound performance changes: logical boundaries alone do not determine physical cost.

A compiler/interpreter example reports that hiding register representation, search and rule-interpretation decisions allowed the same decomposition to cover different execution strategies. The journal gives a brief account and points to the report for detail. It also separates information hiding from a hierarchical uses/dependency relation: one can expose poor interfaces while retaining a hierarchy, or hide decisions without that partial order. A hierarchy adds the ability to remove upper layers and reuse lower functionality. These mechanisms are related but not interchangeable metrics.

The paper cites classroom use, small-scale observations and a translator project; it gives no controlled sample, quantitative maintenance outcomes, uncertainty estimates or independent comparison. Its comprehensibility comparison is explicitly a subjective judgment. Its value here is a detailed mechanism and counterexample, not an empirically calibrated effect size. Acknowledging these limits preserves its contribution rather than treating every nonexperimental source as failed evidence.

## Three criteria and remaining primary paths

**Unique:** information hiding, anticipated-change decomposition, distinct source/runtime representations and their efficiency tradeoff are established prior mechanisms. Nu-specific priority requires a narrower mechanism-level comparison, not a broad claim to invent change-locality or decoupling. **Valuable:** the scenarios identify decisions whose isolation could matter, while actual task prevalence, agent success and net cost remain unmeasured. **Scientifically valid:** separate logical decomposition, implementation, tooling and expected change distribution; test complete behavioral contracts, including timing and allowed reorganizations. The theory does not validate D1, revive D2 execution or prove a runtime-neutral architecture effect.

S82's parameter/global manipulation tests one interface dimension and therefore does not refute this whole criterion. The positive modularity studies promoted as S90/S92 and the industrial design-metric study S91 can test different parts of the argument; their methods remain pending. S93's structured-design criterion is a distinct foundational comparison, with its original/reprint edition unresolved. The 2001 coffee predecessor S94 is promoted to clarify outcome/task lineage rather than enlarge an independent-study count.

SC18 returned seven identities for three requested titles: the journal, report, anthology and deposit variants of this paper, plus S92; the Korson/Vaishnavi chapter was not matched. Exact metadata do not make these Parnas variants independent evidence. SC19 follows the module-specification paper and information-distribution report cited here, plus extension/contraction and program-family papers surfaced by C09. Full specifications, report/compiler details, later retrospective accounts and edition equivalence remain explicit follow-up limits; the journal reading is complete without claiming those sources read.
