# S58 — dynamic dependency ordering in virtual environments

**Full reading completed 2026-09-29.** Marum, Jones and Cunningham, *Dependency Graph-based Reactivity for Virtual Environments*, IEEE VRW 2020, pp. 246–253, [DOI 10.1109/VRW50115.2020.00052](https://doi.org/10.1109/VRW50115.2020.00052). Zotero parent `2TB38CQ8`, newly present publisher PDF `KYB82NS2`: eight pages, 244,829 bytes, SHA-256 `c558b49ed8c985bb674f5ceda4a1a23bfc7cacf44c4d117feab7b2c80a3a88e4`. This library file was copied read-only; the session did not download it.

The [earlier extracted-author-body reading](../S57-S58-reactive-game-ordering-reading-2026-09-29.md) covered all sections, algorithms, tables and 28 references. The publisher file now verifies the edition, both figures, both algorithms and both result tables, with page renders 3–7. Publisher prose and references were also checked; the earlier visual/typographic gaps are closed. This is an extension of S57, not an independent replication. No implementation, benchmark or human study was executed by this review.

## What is actually compared

The C#/Unity framework discovers component relationships and executes selected `ReactiveUpdate` callbacks in dependency order within one ordinary event. Changed values/components must be exposed as fields or properties. Cyclic dependencies are omitted and execute non-reactively; Unity/.NET internals and other scripts lie outside the mechanism. Object identity uses type/name/parent-property assumptions, while the paper's requirement of no cross-frame dependencies narrows its scope (pp. 248–250).

Figure 1 shows dependencies and a permissible component order. Figure 2 shows a generated arithmetic expression, its tree and an order that evaluates operands before dependent operators. These illustrate the intended mechanism. They do not prove that every real scene's dependencies are captured. Rendered algorithms correct S57's empty-queue condition but retain ambiguous edge direction and references to `C1` in its null branch; deletion handling and traversal must not be inferred as a verified executable specification.

The comparison uses a random expression-tree family, default Unity3D and the authors' UniRx application, on Unity version printed as 2019 3.0. At each cycle the oracle compares node values with precomputed expected values, including between structural changes. The two scenarios each report 100 **user cycles**, not 100 independent games. Tree sizes, generation distributions, repeats and uncertainty are incompletely reported.

| Scenario | Unity / UniRx / framework total errors | Reported cycle latency | Visible errors |
| --- | --- | --- | --- |
| No structural modifications | 95 / 15 / 15 | 5 / 5 / 1 | Zero for every comparator |
| Insert/delete/modify nodes | 100 / 80 / 20 | 7 / 20 / 1 | Zero for every comparator |

These reproduce publisher Tables 1–2 (p. 251). The second-scenario Unity prose says 95%, conflicting with the table's 100; this review preserves the discrepancy. Error totals, cycles containing errors and conditional errors-per-cycle are different units in the report. The visibility criterion is persistence across a rendered frame, not a perceptual user test. The tables cannot establish the discussion's smoother-user-experience claim.

Initial graph construction/sorting averages 198 ms and rebuilding takes up to 100 ms. More rigorous timing is future work (pp. 250–251). No equivalence test or uncertainty bounds establish zero performance cost. Internal consistency, wall-clock responsiveness, visible behavior and maintenance effort therefore remain separate outcomes.

## Baseline and Nu implications

The paper itself acknowledges Script Execution Order settings in section 2.2 despite broader introductory wording about unavailable order control. The [Unity 2019.3 manual](https://docs.unity3d.com/2019.3/Documentation/Manual/class-MonoManager.html) confirms ordering **between MonoBehaviour classes**, separately for event categories. That is narrower than discovering changing dependencies among component instances. This primary documentation check supports requiring credible configured alternatives; it does not establish that the setting alone solves the paper's dynamic problem or changes its measured results. Only this manual page's relevant text was inspected, not its screenshot or the whole manual.

**Unique:** dynamic game-update coordination has a direct predecessor; a precise Nu mechanism remains unconfirmed. **Valuable:** complete internal propagation and recovery are useful targets, but Nu maintenance savings and user-perceived gains remain unmeasured. **Scientifically valid:** retain all attempts and old/new obligations, distinguish transition/recovery/visible outcomes, include cycles and external effects, and evaluate credible configured baselines under common access. The expression-tree family and author implementations do not justify a general engine effect. ISE's source equivalence, oracle, task diversity and accounting remain unvalidated; allocation is zero.

S59 is the already acquired generalization of this lineage and remains a consequential reading. Earlier VR/FRP, GUI and robotics references are conditional on adopting their exact guarantees. The earlier source audit records citation discovery and acquisition failures; publisher completion changes S58's reading state without counting those historical screens again.
