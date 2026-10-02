# S202 — Infragenie and maintainer evidence

**Full target-chapter reading, 2026-10-02 HKT.** Ricardo Ferreira, Filipe F. Correia and Paulo G. G. Queiroz, *Infragenie: Living Software Architecture Diagrams From Docker Compose Files*, ECSA2025 Tracks and Workshops, LNCS15982, publisher2026,pp.12–20, DOI [10.1007/978-3-032-04403-7_2](https://doi.org/10.1007/978-3-032-04403-7_2). Maintainers give favorable ratings to automatically generated architecture documentation. The released data preserve weaker expectations about making changes faster or using the tool for planning, alongside concrete feedback about missing information and update burden. Neither the questionnaire nor merged diagram contributions measure a causal maintenance-time saving.

Existing native Zotero `BLSJ932C` / note `5GM3C82Y` preceded reading. PDF **`XCPAWZUF`v4827** is the **400-page proceedings**,31,788,294bytes,SHA-256 `30bb82b7a7faed92c3754208f70a55559b007c90f8c6b9fae65b2d413051cd0f`. The target occupies **PDF35–43 / printed12–20**, nine pages. All nine target pages were read as text, including22 references and the data-availability statement. PDF35,37,38,40,41 were visually inspected, covering all six figures, the domain-model diagram and example deployment diagram. The other target pages are text-only; the rest of the proceedings is not read. The native attachment has no URL, so its acquisition route is not inferred. The2025 event/online metadata and2026 publisher edition are preserved separately.

## Mechanism and what stays current

The prototype takes a GitHub repository and branch, finds `docker-compose.yml` files through the GitHub API and transforms them into an intermediate architecture model. Service definitions become entities, service names become node names, container names become component names, and properties become component attributes. The model includes containment, connectors, ports, artifacts, networks and property maps. A second transformation produces PlantUML and a rendered diagram. The workflow creates a PR adding that diagram and can update the README.

This is a concrete way to recover a useful deployment/component view from an already maintained declarative artifact. It does not infer the entire source-level or dynamic architecture. Information absent from Compose, environment-specific configurations and implicit inter-service relations may remain missing. The paper proposes extensions to other IaC formats; it does not establish their implemented coverage. Model extensibility is distinct from demonstrated extraction coverage.

Automatic generation on request is also distinct from automatic detection and propagation of every future architectural change. The questionnaire explicitly asks whether automatic change detection without manual intervention would improve the tool, and the released comments describe manual regeneration/editor burdens. No running application, PR-creation workflow, OAuth path or update pipeline was exercised during this reading.

## Sampling and the actual observations

The authors search for active GitHub repositories created since2018, active sinceNovember2021 and containing a Compose file. They report a frame of22,447 repositories and a randomly selected378-repository subset after purposive eligibility filtering. Each selected project receives a generated diagram through a PR plus a questionnaire invitation. The released materials do not recover the full sampling frame, random seed or unique invited-maintainer mapping.

The paper reports197 open,116 closed and65 merged PRs, and36 completed questionnaires. The released CSV reproduces those **row counts**, but contains **373 distinct PR URLs across366 repository paths**. Five URLs occur twice; one duplicate pair has conflicting open/merged states. Thus378 rows are not verified378 distinct repositories or independent invitations. No snapshot timestamps or rule settle that conflicting state; do not silently deduplicate and call the result the original study.

The nominal questionnaire yield is36/378=9.52% of reported invitations, with the denominator caveat above. Anonymous response data have no project/PR key linking individual answers to merged status, and no respondent-uniqueness verification is reconstructed. Random selection from eligible repositories does not remove nonresponse or volunteer selection. PR closure can reflect submission format or perceived advertising, as the authors acknowledge, rather than diagram quality alone.

Among the36 responses,28 select experience categories of at least five years. The CSV contains24 distinct country labels, including variant labels for the same place; this is not independently verified24-country diversity. Participants report substantial UML/text-diagram familiarity, but disagreement/neutrality remain, especially for particular UML diagram types. No strong disagreement alone cannot establish adequate expertise.

The questionnaire is inspired by a technology-acceptance framework. It asks for opinions, intentions and suggestions after presenting the tool/diagram, rather than assigning a timed modification or measuring later productivity. The final chapter describes mandatory closed questions and optional comments; the archived form permits an optional comparison response following the prior-diagram question. Its nineteen numbered questions include matrix subitems beyond those reported in the chapter. The PDF print header is19September2022, whereas the archived release is23May2025; this identifies the instrument copy, not an exact date for every response.

## Positive results and denominator repair

Passive counts from the36 released rows reproduce the main favorable documentation results. Agreement combines Agree and Strongly agree, preserving the original item/denominator rather than treating all favorable items as one effect.

| Perceived documentation property | Agreement /36 |
| --- | --- |
| Complete | 26 (72.2%) |
| Consistent | 28 (77.8%) |
| Precise | 26 (72.2%) |
| Easier to consult | 30 (83.3%) |
| Easier to understand | 27 (75.0%) |
| Easier to maintain | 20 (55.6%) |
| Easier to update | 22 (61.1%) |
| Diagram provides a complete architecture view | 22 (61.1%) |
| Diagram provides the most relevant elements | 33 (91.7%) |

The figure labels round category percentages, so their sums need not reproduce unrounded aggregate percentages. These ratings support perceived documentation usefulness in the responding sample. Completeness/precision were not checked against an independently reconstructed architecture oracle, and no comparative significance test or maintenance-effect estimate is supplied by the chapter's use of the word “significantly.”

Twelve respondents say they had a prior diagram. Among these twelve, seven rate Infragenie better, two much better, two neutral and one worse: **9/12=75%** favorable. The paper combines that count with **78%**. Two respondents who say they had no prior diagram nevertheless supply favorable comparison answers. Across all fourteen nonblank comparisons,11/14=78.6% are favorable.

The inspected notebook cells44/46 count all valid comparison choices, without conditioning on the prior-diagram answer. Their category rounding gives57% better plus21% much better, consistent with the printed78%. The artifact therefore explains a plausible denominator source, while the chapter's claimed nine-of-twelve comparison remains75%. It would be misleading to report78% of all participants preferring the new diagram or to discard the favorable9/12 result because of this error.

## The supplement qualifies the maintenance/adoption claim

Several released questionnaire outcomes, not shown in the chapter's main figures, are more cautious. They remain expectations or intentions rather than observed performance.

| Item | Agreement /36 | Neutral /36 |
| --- | --- | --- |
| Helps plan future architectural changes | 23 | 9 |
| Helps understand the impact of changes | 18 | 14 |
| Increases confidence while changing architecture | 11 | 19 |
| Helps implement architectural changes faster | **7** | **22** |
| Considering adding generated diagrams to projects | 21 | 11 |
| Considering using the tool to visualize/plan changes | **3** | **25** |
| Considering using it in new projects | 21 | 10 |
| Would improve with automatic change detection/update | **32** | 3 |

The remaining responses in each row disagree or strongly disagree. In particular, only19.4% expect faster implementation and8.3% express the specified planning-use intention. These do not estimate a negative productivity effect, but they challenge a blanket conversion of favorable documentation ratings into strong maintenance/adoption expectations.

All40 nonempty comments across the four open outcome/comment fields were read. They describe useful service details, port information, standard notation and a reported typo discovery, alongside absent connections, non-Compose infrastructure, dev/prod file selection, restricted editing and difficult connection creation. Some respondents value editability for adding missing information while finding it impractical to keep that work current. Others describe the PR/web workflow as intrusive, slow or immature and request CI integration. These are self-reports, not timed costs or verified defect detections. No participant-level comments or demographic rows are republished here.

The65 merged **rows** are evidence of some accepted contributions, with the duplicate/state caveats. They do not establish65 distinct sustained adopters, long-term synchronization, reduced effort or correctness of subsequent architectural changes.

## Released package: exact coverage and limits

The paper's [Zenodo v1.2 package](https://doi.org/10.5281/zenodo.15496366), released23May2025, was acquired normally and added to the existing parent as ZIP **`NNVMI98F`v4911**. It is **14,967,237bytes**, SHA-256 `db0c6423e4cfd09f29907460a70ce1b778659c16815d9c821f9f67a06cf6f800`, matching published MD5 `df8773c538b4f2a7eb89b036786918a7`; native stored bytes were rehashed. Its twelve ZIP entries comprise nine files and three directories, under release-root suffix `e611663`. That short directory suffix is not claimed as a separately verified full Git commit. The Zenodo record declares CC-BY4.0. The live tool homepage timed out; artifact access is independent of that endpoint.

| Selected artifact | Bytes | SHA-256 | Actual inspection |
| --- | --- | --- | --- |
| `README.md` | 931 | `a0f0824b504ed3c56e1e9556d2f9e02f3a94c5e8e98ca5718e39d2ccc9855aa8` | Complete text; some named paths differ from actual archive filenames |
| `Infragenie survey.pdf` | 276,379 | `a4f766c1ca048748a528b8edbf08c705ad1b7ae88a6a1c09834de80ad4a2853d` | All nine pages text/visual, all nineteen questions and matrix choices |
| `raw_results.csv` | 25,919 | `b133e1f5428a7f7bfa7bb1290e6932d6864953d603aa161194c1666f77a29b80` | 36 rows,43 headers; all closed-outcome distributions, selected demographics and all four open outcome/comment fields. Free-text study-area/current-role values not read |
| `pull_requests_list.csv` | 24,659 | `8b8eef982bcc79b642eff6ba3197a963f5fcae9f070a1c00cb3d95032728c1a1` | All378 URL/state rows passively counted; URL/repository multiplicity and duplicate-state conflicts checked. Individual live PR contents not read |
| `participants_characterization.ipynb` | 78,090 | `d85b1a060e889dbc458217acac63700bb0b1504cdf56e18f227a3a8c29f9d12d` | Source cells3,5,9,56lines: loading, literal country grouping and experience grouping |
| `pull_request_analysis.ipynb` | 63,025 | `2d0e592aabc28ac164e454238cc4eab034f0560d7fea2566a33dc3a1a1291530` | Source cells2–6,8,99lines: commented fetching/concatenation, input, state counts and percentages |
| `tool_analysis.ipynb` | 2,621,000 | `14c14d2ccd4d85f2dcde3d9bc2452957956af8242b43813df900b3258fe964f9` | Source cells3,4,23,24,43–47,49,343lines: loading, Likert normalization/rounding, outcomes, comparison denominator, intention and improvement |

Notebook indices are zero-based. The total is **nineteen selected cells /498 source lines**, not a complete notebook or cached-output review. The PR notebook refers to `pull_requests_list_with_state.csv`, absent under that name from the ZIP; the provided `pull_requests_list.csv` already includes state values. The source's fetching and package-installation cells were not run. No notebook was executed, dependency installed, live PR status refreshed or message/PR sent.

The13,653,457-byte onboarding video is acquired inside the ZIP but remains unwatched, as do the unselected notebook cells/outputs. The package does not contain the full repository-sampling frame, prototype implementation or an independent architecture reference set. Passive distribution and duplicate checks reconstruct the supplied data at their stated scope, not the complete study workflow.

## Survey consequence and continuation

For B01/B08/B10/B11, the method supplies a useful concrete alternative: derive a reviewable architecture view from declarative deployment artifacts and let maintainers judge it. The evidence supports favorable documentation perceptions and some accepted contributions, while the supplement exposes narrower planning/effort expectations and recurring integration burden. “Living” should specify what triggers regeneration, which inputs determine the view, how manual additions survive, and how fidelity is checked.

This is a distinct case from S199's live design-pattern documentation, despite overlapping authors and a citation link. No independent replication of S199's tasks or participants is established. Neither study identifies a Nu-specific runtime, type-feedback or correctness benefit. The remaining automatic-update/fidelity and longitudinal maintenance effects are empirical or implementation gaps, rather than an unread publication.

**Next consequential action:** read acquired S204's industrial coupling/defect method to settle its temporal ordering, module-size/developer-activity controls and defect-type variation. This addresses a different population and outcome from the three newly reconstructed developer/tool studies. Retain independent runtime/type/oracle routes, the comparative AOP review and residual source/data questions; no construction or experiment follows from this checkpoint.
