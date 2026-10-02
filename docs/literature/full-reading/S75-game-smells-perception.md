# S75 — game-specific problems, practitioner judgments and measurement

## Identity and coverage

Vittoria Nardone, Biruk Asmare Muse, Mouna Abidi, Foutse Khomh and Massimiliano Di Penta, *Video Game Bad Smells: What They Are and How Developers Perceive Them*, ACM TOSEM 32(4), 2023, [DOI 10.1145/3563214](https://doi.org/10.1145/3563214). Native parent/note/PDF **`FBZH4JWN`/`9M6Z8I6S`/`Z5ZYXLL5`** were verified before continuing the body. The [author manuscript](https://mdipenta.github.io/files/tosem-gamesmells.pdf) has 36 pages, 745,655 bytes, SHA-256 `84473800d3b298824bb8bae3323762a079cda65fb8b01543cb0f916fe575fdeb`. Its placeholder 2021 date, volume and DOI are not the bibliographic identity. Crossref identifies the 35-page final publication, published 26 May 2023; that edition returns HTTP403 and its correspondence remains unresolved.

All 36 author-manuscript pages, eight figures, three tables, footnotes and 62 references read. Visual pages **1,3,5,7,10,11,15,16,19,21,25,29** include every figure/table; other pages are text-only. This closes the author-edition reading, not final-edition access.

The [Zenodo package](https://doi.org/10.5281/zenodo.6720644), a version of concept DOI `10.5281/zenodo.6327678`, is acquired and attached as **`5PWPYBPR`** under the same parent. ZIP: 1,206,388 bytes, SHA-256 `649d0d32a45da579ba7c846e1acd50a544f019f87e54ef6e92375533872139a2`; its declared MD5 verifies. Metadata identifies CC-BY-4.0, a March 2022 publication date and June 2022 update. Full text of the 19-page questionnaire and 16-page catalog appendix is read; visual coverage is questionnaire 1,4,6,18 and appendix 1,4,6,12,15. CSV/workbook structure and own passive aggregates are inspected. Individual survey comments are not exhaustively recoded; the 31 archived forum HTML bodies are inventoried, not independently reread. [Artifact reconstruction](S75-game-smells-artifact-check.md) records identities, reproduced counts and version mismatches. No author code, detector, game or experiment is executed.

## Question and study construction

The study elicits a catalog from developer discussions and asks professionals how critical its descriptions seem. It does **not** measure the prevalence of smells in a representative game-code population, observed maintenance effort, frame times, bug reduction or the effect of removing a smell. That distinction preserves its useful contribution: concrete practitioner concerns and contested tradeoffs that a code-only architectural argument can miss.

Sections 2.1–2.3 query 13 selected forums plus Google. Selection combines known communities, engine popularity and forum lists; sources not actually discussing development are excluded. Initial smell/antipattern/bad-practice terms are extended with maintainability, performance and technical-debt terms; general forums receive game-specific qualifiers. The authors use Selenium/BeautifulSoup and additional filtering where a forum implements OR instead of the intended conjunction. Those are their acquisition tools, not tools executed here.

The paper reports 3,170 candidate links and a proportionally stratified 550-link sample; 22 inaccessible links are replaced, giving 572 considered links. Four authors code, with two annotators assigned to each link and the first 40 jointly calibrated. A shared evolving label list allows existing labels or new ones; every link is jointly discussed afterward, including initially agreed cases. This is a transparent cooperative elicitation procedure, not independently validated classification accuracy.

Reported rounds comprise 340,102,130 links. The initial 81 labels become 52 after merging 29 into 13 and removing 13; two later rounds add four labels each. A final merge of 30 labels into ten and removal of twelve yields 28 smells in five categories: design/logic, multiplayer, animation, physics and rendering. Later rounds still contribute three and two final labels; the authors acknowledge incomplete saturation. The claimed sampling confidence/margin concerns the chosen link frame under its assumptions; it does not establish taxonomy completeness. The package's duplicate links and unmatched round inventories further limit literal reconstruction of the sampling procedure.

The reported annotation cost is approximately 96 person-hours plus 13 meeting hours and offline refinement. This is evidence about the elicitation work, not game-maintenance cost.

## Recruitment, instrument and outcomes

Sections 2.4–2.6 use LinkedIn keywords, top-ranked profiles and manual checks of industrial game experience. The search takes the top 200 per keyword result set, then connection acceptance precedes sending the survey. Of 642 invited professionals, 76 respond, **11.84%**. The collaborator used to pilot the approximately 20-minute questionnaire is excluded. This is a relevance-ranked, connection- and response-selected sample, not probability sampling of all game developers.

Ratings use five stars: one not critical, three neutral, five highly critical. Respondents may skip unfamiliar topics and add comments. Descriptions often include an adverse consequence or suggested remedy before the rating; consequently, agreement with a problematic vignette is not evidence that the named implementation choice is intrinsically harmful. The questionnaire also contains five additional rated items absent from the final plots; this lineage is not silently reduced to a 28-item administered instrument.

Sixty-one people provide some demographic information. Paper and package agree on major engine/language counts: Unity 44, Unreal 27, Blender 11, CryEngine 2; C/C++ and C# 45 each. Multiple selections are allowed. Education has 60 nonblank responses and role 59 in the package. Published experience counts/medians do not match the package columns: the latter has 56 game-experience values with median three years and 48 software-experience values with median five, whereas the paper reports 54/five and 46/three respectively. Both package ranges are 0.5–24 years. No undocumented exclusions, header swap or corrected demographic analysis is invented. The manuscript promises analysis of experience effects but supplies no identifiable such estimate in the read edition.

## Positive results and important disagreements

Own arithmetic over all 76 anonymized rows reproduces **all 28 plotted denominators and all 84 rounded negative/neutral/positive percentages** in Figures 4–8. Nineteen of the 28 final items have a majority of valid ratings at four or five stars. Denominators vary from 58 to 76; these are within-item respondents, not 76 independent replications per item. Missing expertise and fatigue can affect comparisons between categories; neutral is not a verified lack-of-expertise category.

| Described problem | Critical/highly critical | Interpretation supported by the instrument |
| --- | ---: | --- |
| Frequent runtime object creation/destruction |63/76,83%|Allocation/pooling concerns are salient under frequent instantiation; comments preserve small-project and prototyping exceptions|
| Weak temporization |61/76,80%|Frame-dependent updates and synchronization deserve explicit attention|
| Lack of separation of concerns |58/75,77%|Respondents endorse separating mixed input, physics, animation and rendering responsibilities|
| Poorly designed object-state management |47/75,63%|State complexity concerns matter; this does not compare equivalent pattern-based and conditional implementations|
| Dependencies between objects |36/75,48%|The questionnaire describes unnecessarily repeated reference retrieval; this is not a clean measure of structural coupling alone|
| Static classes versus singletons |25/75,33%|No majority endorses the proposed smell; comments describe conditional choices and alternatives|
| IDE-created static coupling |24/74,32%|Views are mixed: 23 negative and 27 neutral, with convenience and dependency-inspection benefits reported|
| Client state |60/66,91%|The actual vignette permits unauthorized changes to another player's object, narrower than all client-side state storage|
| Heavy physics updates |55/63,87%|Repeated runtime work is considered consequential; no frame-time benefit is measured|
| Unoptimized rendering |51/61,84%|Visible runtime cost is salient; this is not an evaluation of a renderer or optimization|

The paper's qualitative interpretation is that respondents prioritize tangible gameplay/performance effects and tolerate some maintenance compromises. Preserve that positive practice evidence and its context: frequency, scale, target hardware, engine facilities, whether physics is applicable, and whether work is a prototype or production system. These statements do not estimate a causal priority effect, a lifecycle economic return or a universal professional preference.

Sections 3.1 and 4 also retain contrary views: caching/direct references can avoid repeated dynamic lookup; IDE wiring supports designers and inspection tools; early pooling can make prototyping cumbersome; forcing design patterns into a simple state model can add complexity. The appendix explicitly permits ordinary conditional state handling when a pattern complicates the task. Animation/rendering expertise is partly outside the recruited developer population. Its lower ratings therefore cannot establish that those problems are objectively less severe.

## Constructs, temporal obligations and transfer

The same label can combine distinct mechanisms. Search by name, repeated tag comparisons and component lookup are not identical operations. The dependency question mixes lookup frequency with organizational coupling. The state-management vignette bundles complex branching with ownership concerns. Thus these ratings cannot validate a single metric of compactness, decoupling, functional purity, explicit cases or ECS structure.

Temporal and asset concerns are concrete additions to the Nu background: inconsistent update timing, late joins disrupting existing players, state ownership, texture synchronization, physics-versus-animation ordering and hidden scene/asset dependencies. Additional responses mention execution order, broad animator transitions and cross-discipline asset changes that invalidate existing animations or physics. These motivate declaring the relevant behavior and source/asset boundary in a future authorized evaluation; a successful compilation or warning repair cannot establish these outcomes. Neither the broad-transition comment nor a state-pattern example evaluates D1's equivalent explicit-case/catch-all comparison.

The catalog is not a verified repair manual. Appendix p.12 repeats a rigging remedy under collider settings; p.15 leaves a template sentence as the aliasing correction. The binary-serialization example is not a demonstrated multiplayer security remedy, and protocol/performance statements drawn from forum discussions are not benchmarked here. No backend, transport or security decision follows from these suggestions. Illustrative examples were chosen for explanatory clarity, and not every statement is tied to independent measured evidence.

Compared with [S184](S184-smells-maintenance-effort.md), S75 measures professional judgments about game-specific descriptions, whereas S184 observes effort and fits conditional models in one web-maintenance case. Their units, exposures and endpoints differ. S75's favorable salience results do not overturn S184's conditional smell null, and neither establishes that all architectural improvements help or that smells never matter. [S76](S76-ecs-entity-references.md)/[S77](S77-dots-migration.md) supply different workload-bound runtime observations; no shared Nu benefit estimate exists.

For the survey, use S75 to connect an architectural mechanism to a concrete practitioner problem and competing costs, then seek evidence about the actual outcome. Preserve both programming and asset/tool work, setup burden, gameplay/temporal correctness and runtime cost; do not substitute a smell count for all of them. The residual comparative benefit question is empirical. Final-publication correspondence and package lineage remain separate evidence gaps.

## Consequential continuation

S75's references identify positive design-pattern evidence that could challenge an overly adverse maintenance synthesis. W361 recovers primary routes for **S207**, Figueiredo/Ramalho's 2015 game-development comparison, and **S208**, Ampatzoglou/Chatzigeorgiou's 2007 game-version/metric evaluation. Native records are created before body reading. Read S207's treatment, participants, task, timing and correctness first, then distinguish S208's structural metrics and version changes from measured work. UnityLinter, the game-specific anti-pattern catalog and game-pattern defect study remain conditional primary-method leads, not completed readings or independent corroboration. Broader runtime, persistence, oracle and type-evolution frontiers remain open; no experimental allocation changes.
