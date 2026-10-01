# S111 — mobile crowd rendering, implementation bundles and sampled thresholds

**Complete institutional-thesis reading, 2026-10-01 HKT.** Max Turpeinen, *A Performance Comparison for 3D Crowd Rendering using an Object-Oriented system and Unity DOTS with GPU Instancing on Mobile Devices*, KTH, second-cycle 30-credit degree project, 30 June 2020, **TRITA-EECS-EX-2020:490**. [Institutional identity](https://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-280845); [deposited PDF](https://www.diva-portal.org/smash/get/diva2%3A1467022/FULLTEXT01.pdf). This is a thesis, not a controlled estimate for programming paradigms generally. Reader: main Codex session; no experimental reproduction or independent review.

## Identity and coverage

Existing native parent **`V522ITK7`**, PDF **`6V46PGJ8`** and note **`S6DW58XD`** were verified before body reading; memberships `PKLXQNEE`, `74BHFBRZ`, `MBYQJXUF` preserved. The **19-page, 3,977,385-byte** attachment has SHA-256 **`b339eee92d5bc989528df0cd6a01cf92b75e3f543bcdf8477ec06d44877a5307`**. All pages were read in extracted text and visually, including the three blank leaves, Swedish summary, title/degree pages, twelve-page article body and back cover. All **thirteen figures**, including the scenario matrix and eight result plots, and **55 references** were read. Enlarged crops of Figures 5–13 resolve labels and threshold comparisons; no exact numerical dataset was recovered from bar heights.

The work is the mobile comparison cited by [S77](S77-dots-migration.md), not S77's own experiment. Its source, raw frame logs, exact assets and build manifests remain unacquired after the bounded locator search below.

## What is actually compared

The baseline uses Unity GameObjects with attached MonoBehaviours. The alternative combines **DOTS/ECS, Jobs/Burst-related infrastructure and GPU instancing**. It describes preprocessing vertex-position data into textures for GPU use. This is a particular rendering/animation strategy, not the definition of all GPU instancing. The author reports Unity **2019.3.0f3 Personal**, Burst **1.2.1**, Entities **0.5.1**, Xcode **11.4.1**, and iOS **13.4.1**. No code, compiled-job evidence or configuration manifest independently confirms which work actually used Burst or parallel jobs.

Both versions start from matching camera/light/skybox, ground plane, focal box and crowd-spawner settings. They seek visually similar scenes but use **different shaders**, visibly changing appearance in Figures 3–4. GPU instancing is added only to the DOTS implementation. Consequently the comparison tests two implementation packages; it does not isolate ECS storage, multithreading, compiler optimization, instancing, shader work or OO organization.

The two devices are an iPhone 6S, 32 GB, and iPhone XR, 64 GB. Render scales **.81** and **.665** compensate for nominal 1334×750 and 1792×828 screens. Own arithmetic gives approximately **656,428 and 656,163 nominal scaled pixels**, respectively. This is a near area match, not proof of identical render targets, aspect ratios, GPU workload or device state. The author primarily compares implementations within each phone; these are two devices, not a representative smartphone sample.

Four scene families are evaluated per device:

- One original-mesh character and animation, repeated with increasing counts.
- Nine characters with nine animations, adding visual variation.
- One repeated character reduced to 20% of its original polygon count.
- One repeated character reduced to 10%.

The latter two are **fixed mesh simplifications**, not a measured dynamic distance-based LoD system. The author says culling is not used. The scenes provide rendering/animation evidence; navigation, collision avoidance, live component restructuring and post-release maintenance are not evaluated. Variation also changes average mesh/animation complexity, which the author acknowledges. It is therefore not a clean intervention on the number of variants alone. The reduced-mesh tests were added after the baseline performed better than expected; preserve them as exploratory workload extensions.

## Sampling and graph semantics

Each tested configuration is built separately and **run once**. A **single frame** supplies FPS and CPU/GPU processing times after **five minutes**, intended to expose thermal throttling. There is no reported repeated-run distribution, percentile frame time, confidence interval, energy use, memory measurement or temperature trace. The author's qualitative observation of small fluctuations does not provide those quantities.

Figure 5 lists **41 paired device/scene/count configurations, or 82 implementation-specific builds** under our transcription. The text refers to “Table 1,” although this matrix is Figure 5. At least forty further samples varying four/nine characters and animations separately are said to have produced similar results and were omitted; no raw values are supplied here. Approximately twenty minutes per sample explains measurement effort, not application-development productivity.

The result plots combine FPS and milliseconds on separate labeled axes, with a 30-fps target. The text describes replacing favorable sample bars with the 30 mark and collapsing later underperforming samples to the graph floor, except for more of Figure 13's baseline trajectory. Therefore equal plotted bars can be **display conventions**, not equal underlying CPU/GPU times; floor bars are not measured minimum performance. The light-gray legend says **DOTS** even though the methods and captions identify the third series as **GPU**. Interpret it using that explicit description, retaining the label discrepancy.

The sparse tested counts give observed sampled transitions, not exact maximum capacities or a smooth scaling law. Figure 11 labels counts **440/500/540/600/640**, while Figure 5 lists **450/500/550/600/650** for the corresponding family. That unresolved correspondence prevents silently treating the scenario matrix as an exact run manifest.

## Positive and adverse results

The eight plots support the author's broad **six DOTS-favoring / two OO-favoring** account for these implementation packages. The table below records plotted 30-fps samples and first visible drops, not independently verified thresholds or precise digitization of every bar.

| Device / scene | GameObject baseline | DOTS + instancing | Scoped reading |
| --- | --- | --- | --- |
| 6S, original repeated mesh, Fig. 6 | 30 fps at 25; below at 30 | 30 fps at 45; about 27.5 at 50 | Alternative sustains the target at substantially larger sampled count |
| XR, original repeated mesh, Fig. 7 | 30 fps at 110; below at 120 | 30 fps at 100; below at 110 | Baseline advantage; the sampled first drops differ |
| 6S, nine characters/animations, Fig. 8 | 30 fps at 25; below at 30 | 30 fps at 45; below at 50 | Alternative advantage remains; the greater drop relative to its simpler scene is not a baseline victory |
| XR, nine characters/animations, Fig. 9 | Both reach 30 fps at 120 and fall below at 130 | Both reach 30 fps at 120 and fall below at 130 | Baseline retains a higher plotted FPS at 130; same sampled transition |
| 6S, 20% mesh, Fig. 10 | 30 fps at 150; below at 220 | 30 fps at 250; below at 300 | Alternative advantage under static mesh reduction |
| XR, 20% mesh, Fig. 11 | 30 fps at the plotted 440; below at 500 | 30 fps at 600; below at the plotted 640 | Alternative advantage; matrix/axis count discrepancy retained |
| 6S, 10% mesh, Fig. 12 | 30 fps at 200; below at 250 | 30 fps at 450; below at 500 | Substantially higher sampled capacity for the alternative |
| XR, 10% mesh, Fig. 13 | 30 fps at 500; below at 600 | 30 fps at 1,000; below at 1,100 | Alternative retains the target at twice the largest displayed passing baseline count; not an exact capacity ratio |

The discussion claims that both implementations first drop at the same count in every DOTS-adverse case. **Figure 7 contradicts that claim**: the alternative drops at 110 and the baseline at 120. Figure 9 does support a common sampled drop. Preserve the two baseline-favorable results rather than explaining them away through an untested thermal hypothesis.

For larger reduced-mesh scenes the baseline's plotted CPU time rises sharply, while the alternative's CPU/GPU times converge near its limit. The authors attribute this to offloading through instancing. That is a plausible account of the bundled implementation, not an isolated mechanism estimate: there is no GameObject-plus-equivalent-instancing arm, no CPU/GPU ablation and no independent draw-call/compiled-code verification. The favorable results remain relevant despite this attribution boundary.

## Authors' limitations and a dated platform check

The phones stayed plugged into the computer during building and testing. Charging duration and accumulated heat were uncontrolled; baseline builds came first in the initial XR tests. These conditions make device state/order plausible rival explanations but do not demonstrate that either favorable or adverse result is spurious. The versions also use different placement generators: an older random function versus noise from the newer mathematics package, with no common seed. The author's claim that this affects only initialization is not independently checked for resulting visibility, overlap or rendering workload.

The thesis itself proposes adding instancing to the GameObject version, as well as LoD and culling, as future work. The [official Unity 2019.3 instancing manual](https://docs.unity3d.com/2019.3/Documentation/Manual/GPUInstancing.html), introduction/restrictions and script-call sections, confirms that instancing was available for GameObjects/MeshRenderer and suitable draw calls, with shared mesh/material restrictions. It explicitly excludes **SkinnedMeshRenderer** from automatic support. Thus this is a meaningful alternative, but not evidence that the thesis's animated baseline could gain the same result by merely checking a box. Texture baking, compatible shaders and equivalent rendering work would still need specification in any later authorized comparison.

The [Burst 1.2 changelog](https://docs.unity3d.com/Packages/com.unity.burst@1.2/changelog/CHANGELOG.html) supplies the 1.2.1 release entry dated 23 January 2020; selected entry reading verifies version existence, not enabled use in these builds. The thesis's Entities citation points to the 0.2 documentation although its methods name 0.5.1; the attempted 0.5 changelog route remains inaccessible. Keep the stated version and unresolved binding rather than substituting current DOTS behavior.

## Access, synthesis and next work

The institutional landing page and URN remain inaccessible through the web reader, while the already acquired deposited PDF is intact. Exact-title/source and author/GitHub searches return the same PDF, bibliographic mirrors, later citations and a different 2016 student project; they do not identify this experiment's source or raw logs. This is a bounded search outcome, not proof that no release exists. The newly surfaced 2022 multithreading comparison is a conditional method lead; its limited Scite abstract and outgoing citation contexts do not validate its measurements.

**Established alternative:** character batching, representation choices and GPU work placement give concrete implementation alternatives to reasoning only about language or ECS labels. **Measured result:** the selected DOTS/instancing package supports larger sampled crowds in six cases; two original-mesh XR cases favor the baseline. **Residuals:** exact configurations/assets, censored plot values, thermal/order effects, isolated mechanism attribution and variation costs remain unresolved. Maintenance effort, energy, memory and Nu/F# transfer are unmeasured, not demonstrated null effects.

S111 closes S77's mobile-primary-reading dependency and strengthens B05/B06 with positive and adverse rendering results. Continue the less complete C02 type/evolution screen and independently grounded fault-sensitivity methods; retain targeted runtime leads without treating another favorable benchmark as broad-survey completion. No theme closes and all construction/experimental holds remain.
