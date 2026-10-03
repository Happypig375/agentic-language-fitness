# S240 — Endless-runner pooling: complete indexed text, missing visuals

Aditya Cipta Rahadian, Iwan Setiawan and George Pri Hartawan, *Analisis Penerapan Metode Object Pooling pada Game 2D Endless Runner*, **Pixel 15(2), 254–266 (2022)**, [DOI 10.51903/pixel.v15i2.770](https://doi.org/10.51903/pixel.v15i2.770). Main-agent reading began 2026-10-03 and continued 2026-10-04 HKT. Crossref and the publisher identify 5 December 2022; the current landing page translates the title into English. These are one work, not two studies.

## Actual coverage and access

Native **`Y5VD4GHT` / `MK5B4ELA`**, collection **`PKLXQNEE`**, precede selected body reading. Read all **363 indexed lines spanning 13 publisher-PDF pages**, including five main sections and 15 references, through the [publisher PDF web extraction](https://journal.stekom.ac.id/index.php/pixel/article/download/770/660). The visual figures and their embedded text are **not** covered. No local PDF bytes, attachment, PDF hash, full-publication credit or reproduction is claimed.

The ordinary PDF GET, published viewer URL and two conventional public URL variants return403. Web screenshots requested for PDF pages1/10/11 fail with cache misses. The publisher landing is readable; its PDF link leads to the same viewer. ResearchGate offers an author-copy request rather than a public full text; no contact is made. DIAJENG supplies metadata. Garuda's index can be downloaded, but its selected article's original/download links point back to the same publisher URLs. The separate Saari thesis lead remains metadata-unresolved after its handle and PDF return403; no selected thesis body is read.

## What the readable method establishes

Sections3–4 describe two C#/Unity versions of one simple desktop endless runner using the same game data. The changed method handles **ground segments**: repeated creation/destruction versus reuse through activation/deactivation. Three ground templates are chosen randomly; the player runs automatically and jumps to avoid falling. The hierarchy description says the non-pooled container holds four to five ground objects and the pool adds unavailable objects as needed. It does not establish a fixed prewarmed capacity, identical random seeds, a complete reset contract or a trace-equivalence check. This is a closer pooling treatment than [S239's optimization bundle](S239-unity-mobile-optimization.md), which it explicitly cites as instructional background.

The author reports two months developing/analyzing the game, Unity-profiler inspection in the editor and Task Manager inspection of desktop executables on three laptop models. That duration is not a controlled implementation-effort comparison. Readable text does not specify Unity/backend versions, exact processors, sampling duration, repetition/ordering, uncertainty or a measured frame-time/GC-pause distribution.

| Reported comparison, non-pooled → pooled | Scope |
| --- | --- |
| Unity profiler | Total used314.9 →307.5 MB; reserved approximately0.50 GB →485 MB; reported system-used0.94 →0.93 GB (§4.5). The prose treats memory categories as a total without a sound displayed derivation. Figures18/20 remain necessary to verify labels and actual selected measurements. |
| Lenovo G41-35 | Executable memory109.3 →104.5 MB in the narrative for Figures19/21. The screenshots are unavailable, so their CPU values and memory-column definition are not inferred. |
| Asus X441U / X411U | CPU4.9% →3.9%; memory106.6 →105.5 MB (§4.6). The text gives inconsistent model labels; do not choose one by guesswork. |
| Acer Z-14 | CPU7.4% →6.5%; memory64.6 →63.4 MB (§4.6). These are reported utilization/memory observations, not execution time or throughput estimates. |

The authors also report smoother play and occasional lag with repeated creation/destruction. Retain that favorable experience at its descriptive scope. The much larger percentage gains attributed to *Fundamentals of HTML5 Game Optimization* belong to another source; they are neither this study's outcome nor evidence that it measured a comparable speedup. Three laptop labels do not create three independent research teams or known repeated trials.

## Disposition and executable next step

Credit a concrete direct-pooling case and its modest reported resource differences **provisionally at indexed-text scope**. Do not use it as a GC-tail measurement, full-reading completion or a refutation of S239's larger bundle result. The outstanding claim-limiting material is the publisher edition's figures, especially the flow/hierarchy diagrams and profiler/Task Manager screenshots on printed pages263–264. Reuse the existing native record when an accessible publisher or author-copy PDF appears; verify edition, bytes, all figures and labels before upgrading. Independent versioned Unity guidance can resolve current pooling/collector contracts now, without waiting for this access gap or running an experiment.
