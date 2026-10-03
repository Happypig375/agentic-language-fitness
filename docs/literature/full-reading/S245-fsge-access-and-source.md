# S245 — Fsge: immutable sprite updates and a Unity comparison

Jeffrey Peter Kesselman, *Fsge: An Experimental F# Game Engine for 2d Games*, [SSRN5362782](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5362782), [DOI10.2139/ssrn.5362782](https://doi.org/10.2139/ssrn.5362782), posted **23 July 2025**. Main-agent complete chosen-publication reading, 2026-10-04: **all13 pages, text and visuals**, including two cover pages, the11-page manuscript, one results table, two plots and14 bibliography entries. There is no appendix. This is an explicitly unreviewed preprint, not a verified ACM proceedings publication.

The paper supplies a consequential positive game result: an engine using immutable F# object updates can outperform its chosen Unity comparison on larger sprite loads. The authors explicitly limit this to their engine/workload comparison. Different rendering systems, an unbound measured build and absent history/frame-tail observations prevent a language-effect or Nu-cost inference.

## Identity, access and native holdings

DOI/title/edition checks cover **1,275 top-level /269 collection records** before creating parent **`V5RFB2HU`5493** and note **`BGYANVHT`5494** in `PKLXQNEE`. Registration precedes selected reading; W501's automatically supplied abstract is earlier bounded exposure. SC162 requests20 and returns one exact identity without a body. Its full-text endpoint returns zero characters/contentDenied=true; canonical and ordinary SSRN delivery routes return403.

The later native reconciliation discovers imported-file attachment **`WGHMBQ94`5497** before changing any note. Its uploader and acquisition route are not inferred from the attachment's absent URL. The PDF is **308,669 bytes**, SHA-256 **`799102ccfb11ffd53c7a15cc33e833a9833006fa8db6a9d803b85b21e948904d`**, MD5 `e800555e4a52e790a65c4d6afa564211`. Local bytes,13-page extraction and all13 rendered pages are inspected. This resolves primary-body access; the earlier denial remains an access-history fact.

The first cover says *The F# Game Engine (FSGE)*; the22July2025 cover letter precedes a main title *FSharpGameEngine: An open source 2D Game Engine in F# for Education and Research*. Its ACM-style reference has template/2024 placeholders. The repeated SSRN5362782 watermark binds the body to this preprint despite the title variants. These are not three publications. The14 bibliography entries include two SFML.Net entries; their presence is not fourteen independent full readings.

## Question, construction and comparison

PDF pp7–9 (§§2–3) define acceptability relative to an established engine performing the same intended graphics task. The F# engine uses **SFML.Net** for graphics, Newtonian motion and screen wrapping written in F#. Unity3D2023 uses its rendering/sprite-motion facilities plus C# wrapping, classic behavior components and **IL2CPP**; its ECS alternative is explicitly untested. Both implementations are described as naive and unoptimized.

The workloads move and rotate **10,100,1,000,10,000,100,000 and1,000,000 asteroids**. Each measures100 frames, stores per-frame FPS in RAM, then writes CSV for spreadsheet analysis. This retains measurement rows, not previous game worlds. The F# motion implementation cannot handle a period below1ms, so Unity's reported comparison is capped at1,000FPS. The paper acknowledges possible hidden Unity performance below1,000 objects.

Unity renders its2D scene through3D-plane machinery; the F# engine renders in pixel space. The paper therefore disavows a general F# versus C#/C++ speed conclusion. Its claim that all sprites are replaced each frame concerns the immutable state update model; it does not establish copying every texture/native resource or retaining historical roots.

The architecture separates application-facing interfaces from manager plugins. Attributes identify managers; assembly scanning registers implementations; interface lookup returns a first implementation or a list. State is pushed toward the application, with effects at non-F# interfaces. This is a concrete substitution mechanism, not an evaluated live migration, state-preservation or maintenance-effort protocol. §3.1 announces an architecture illustration but no diagram is actually present on the inspected page.

## Reported outcomes and their denominator

The PDF p10 table and p11 line/bar plots give the same six comparisons:

| Moving/rotating objects | Capped Unity mean FPS | F# mean FPS |
| ---: | ---: | ---: |
| 10 | 1,000 | 990 |
| 100 | 1,000 | 1,000 |
| 1,000 | 805 | 1,000 |
| 10,000 | 79 | 147 |
| 100,000 | 7 | 20 |
| 1,000,000 | 1 | 10 |

Preserve the favorable larger-load result and the10-object990-versus1,000 cell; the prose's low-load ceiling summary does not erase that difference. Better relative scaling at the largest loads does not imply a particular interactive deadline:20 or10FPS would not meet a60FPS requirement. The two plots are presentations of the same table, not independent replications.

The declared estimator averages per-frame FPS. It is not automatically reciprocal mean frame time, a frame-time percentile or the proportion meeting a deadline. The paper gives no raw100-frame series, run repetitions, uncertainty intervals, hardware specification, exact Unity/runtime patch, effective collector mode, allocation/heap/GC-pause measurements or retained-history-depth contrast. Its short-lived-allocation explanation is the author's proposed mechanism, not a measured mediation result. These limits narrow transfer without negating its scoped feasibility observation.

Future work explicitly includes richer physics, particles, sound,3D, Unity ECS, Unreal and closer2D renderers such as GameMaker/Cocos2d. The simple motion comparison does not measure those workloads, race reduction, debugging or change/adoption effort.

## Source correspondence: three dated states

The paper names FSFramework and FSharpGameEngine but prints the **same FSFramework URL for both**. The current GitHub API returns404 for that framework path; older cached web HTML shows a2024 listing. This is a source-binding gap, not proof the package never existed or that another repository is automatically its alias.

The earlier [FSharpGameEngine pin](https://github.com/profK/FSharpGameEngine/tree/8ec46ebb9bc44f8c1bbc3848ad27d9973cdf5677), **`8ec46ebb9bc44f8c1bbc3848ad27d9973cdf5677`**,20February2024, is closer to the described SFML design. Its complete tree has67 entries/52 files, one branch and no tags/releases. Seven complete files, **549 lines**, are read:

| Files | Lines | What they establish |
| --- | ---: | --- |
| `GraphicsManagerSFML/GraphicsManagerSFML.fsproj`, `Library.fs` | 24+110 | net8.0/SFML.Net2.5.1; graphics effects and a reused image/sprite resource supplied with a draw transform. |
| `TDE3ManagerInterfaces/GraphicsManagerInterface.fs` | 50 | Window, image and transform interfaces; operations include native effects. |
| `TwoDEngine3/TwoDEngine3.fsproj`, `Program.fs` | 45+49 | net8.0/FSFramework1.0.0-preview-1; runtime assembly scanning/registration and entry into `Asteroids.Start`. |
| `TwoDEngine3/Asteroids.fs`, `NewtonianObject.fs` | 224+47 | Record-copy motion/wrapping and list replacement, shared image references, mutable variables holding current lists. The entry-point demo begins with ten asteroids, input/collisions and a delta-time gate above10ms. |

This source corroborates immutable object replacement with resource reuse, but its interactive demo is **not the paper's six-size100-frame measurement loop**. The inspected files/tree provide no matching CSV packet or Unity benchmark. No measured collector, allocation amount, source defect incidence or run result is inferred by executing them.

The [TwoDEngine3.5 README](https://github.com/profK/TwoDEngine3.5/blob/2d547af139a54fa3b4b6197263aa1c89e68793da/README.md), pin **`2d547af139a54fa3b4b6197263aa1c89e68793da`**,28February2024, is fully read. Mechanical comparison finds **51 identical Git-blob file identities; only README differs** from the earlier52-file tree. Its claim of **4FPS for10,000 moving/rotating sprites** differs from the later paper's147FPS. Without a matched workload/build/hardware packet, this remains a dated source-version discrepancy, not an independent replication or a falsification of the paper.

The later [FSGE pin](https://github.com/profK/FSGE/tree/33005da420374359346e0d1e60690c54d5fd5c43), **`33005da420374359346e0d1e60690c54d5fd5c43`**,7November2025, instead uses Silk/OpenGL. Its145-entry master tree, three branches and no tags/releases are inventoried. Seven complete files/**911 lines** are read: Graphics2D project/interface16+206; SilkGraphicsOGL project/WindowGL30+255; UnitTests project/tests69+220; Asteroids project115. They establish net8.0, plugin/native-resource boundaries and interactive/property tests, not performance denominators. The game-loop file and other branch bodies are not read. This later backend cannot silently stand in for the measured SFML edition.

The later `UnitTests.zip` has272 entries,36,668,946 bytes, SHA-256 **`8fb3edcef2efc52ce036531bdef3c683d78c453391be992d576842771ae477bc`**. Its mechanical inventory finds no PDF/DOCX/CSV/TSV/XLSX; a matched text file is an absolute build-file list. Bodies/binaries are not executed or credited as another source reading. Author discovery inspected135 repository names and sixteen selected descriptions; the earlier `trash` tree227 entries was a path screen only.

Two **locally assembled selected-source bundles**, not author releases, preserve the inspected files:

| Native attachment | Bytes/members | SHA-256 |
| --- | --- | --- |
| `34XEF7I8`5499: later source and earlier one-line README | 12,480 /9 | `5da49b14f95eeed6bb5e31e8f399e8c841758140e60682b34e168f11de5f4c4f` |
| `DAJTEI6Z`5503: earlier SFML files, TwoDEngine3.5 README and manifests | 10,417 /10 | `35e804d05926b6603f42f25dc6db108b0b4ba418d2e419d9293d3ed71cab70f0` |

Stored PDF/bundle bytes and selected source identities are verified. No author code, game, compiler, test or benchmark executes. Copyrighted bodies and extraction dumps remain outside public Git.

## Consequence and next action

B05/B06 now have a read favorable F# game comparison, with explicit rendering and source-version boundaries. The remaining artifact action is to locate the **measured SFML and Unity builds plus six raw100-frame series/configuration**, not reacquire an already-read paper. The printed framework URL, current author trees and supplied attachment do not yet identify that packet.

Combine this result with [DATAS's positive/adverse server trade-offs](coreclr-datas-guidance-2026-10-04.md), without transferring either to Nu history cost. Follow the retained Tardis managed snapshot/replay method for a consequential history-representation/cost dependency. Raw-artifact correspondence, unknown Nu benefit and still-unread independent methods remain different gaps. All experimental holds persist.
