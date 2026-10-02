# S208 — design patterns across two game versions

## Identity and coverage

Apostolos Ampatzoglou and Alexander Chatzigeorgiou, *Evaluation of object-oriented design patterns in game development*, Information and Software Technology 49(5), 445–454, May 2007, [DOI 10.1016/j.infsof.2006.07.003](https://doi.org/10.1016/j.infsof.2006.07.003). Crossref verifies the publication identity. The [institutional revised manuscript](https://ruomoplus.lib.uom.gr/bitstream/8000/652/1/Evaluation%20of%20object-oriented%20design%20patterns%20in%20game%20development%20-%20Revised.pdf) has fourteen pages, 234,425 bytes, SHA-256 `e382e3ce1a58a563104e55ba8e97b0bf394cb46fcdb59d15983f751547ff91b6`. Its 2019 PDF conversion timestamp is not the publication date.

Native parent/note **`5WKSPRPU`/`2VDA84H7`** preceded body reading; attached PDF **`G74VZPZM`** was verified against the downloaded bytes. All fourteen manuscript pages, ten figures, two tables and twenty-nine references are read. Visual pages **3–12** cover every figure and table. A tool result requesting pp.11–14 and later renders was truncated; these pages were explicitly reread/viewed in smaller calls before crediting completion. No original game, pattern detector or metric tool is executed, and no original source archive or metric export is acquired in this pass. The calculations below use the printed tables.

This is a complete reading of the **revised author manuscript**, not verified equivalence with the ten-page final publisher edition. W365's DOI web open fails; the registry's Elsevier linking route returns HTTP200 but only 2,682 bytes of HTML. W366's ScienceDirect article request returns403. Final-edition differences remain unresolved; failed access is not evidence of a changed result.

## Mechanisms and comparison

Sections 2–3 distinguish game-design patterns from software organization and illustrate **Strategy, Observer, State and Bridge**: selection among chess algorithms, football-training notifications, level-of-detail behavior and independently extensible model/rendering-style hierarchies. These explain established alternatives to a single monolithic dispatch or rigid class combination. They do not measure frame time, memory, allocation, notification lifecycle correctness or actual extension effort. The State discussion's atomic update claim concerns a single state reference, not general concurrency or temporal correctness.

Section 4 selects two open-source games because their code and multiple versions are available and at least one version contains a pattern. **Cannon Smash** is C++; **Ice Hockey Manager (IHM)** is Java. C++ patterns are identified through manual inspection and reverse-engineering tools; Java additionally uses the pattern detector cited as reference 28. Metrics are obtained with a CASE/reverse-engineering tool; the metric references include Borland Together 6.1 documentation. Exact tool configuration, raw exports, source checksums and a full detection validation are not supplied.

This is an observational comparison of **two version pairs**, not randomized pattern assignment, a language experiment or a comparison of behaviorally equivalent refactorings. Later versions also add functionality. No developers perform measured maintenance tasks; no elapsed work, comprehension score, defect outcome, test oracle, game performance or adoption cost is observed. Methods that the introduction cites as favorable human-maintenance comparisons remain distinct sources, not outcomes reproduced here.

The seven metrics are LOC; number of classes (NOC); attribute complexity (AC); two weighted-method measures (WMPC1 sums method cyclomatic complexity, WMPC2 reflects method/parameter counts); coupling factor (CF, noninheritance relationships divided by possible relationships); and lack of cohesion (LCOM, based on method pairs and shared attributes). The paper describes aggregate metric values as member averages; the LOC/NOC columns are project/package counts. The attribute weights, CF scaling/rounding and complete tool rules are not reconstructed from the cited manuals. Thus a lower mean class score or coupling density does not establish less total complexity, fewer absolute dependencies or lower measured human effort.

## Cannon Smash

The evaluated releases are **0.4.5 and 0.4.6**, although the then-current game is 0.6.6. Release 0.4.5 introduces multiplayer and dispatches three incoming data types through a switch in `Event`; 0.4.6 delegates to an `ExternalData` hierarchy with PV/BV/PS/Null subclasses. The later current version reportedly has five reading strategies. Figures 6–8 show the original association, switch and revised hierarchy. This is a concrete extensibility mechanism, but the study does not time an additional-data-type task or establish an equivalent-case/catch-all comparison.

| Scope/version | LOC | Classes | AC | WMPC1 | WMPC2 | CF | LCOM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Event0.4.5 | 743 | — | 36 | 55 | 44 | — | 213 |
| Event0.4.6 | 472 | — | 43 | 42 | 43 | — | 211 |
| Project0.4.5 | 8,711 | 43 | 17 | 26 | 19 | 6 | 36 |
| Project0.4.6 | 9,711 | 54 | 14 | 23 | 19 | 5 | 37 |

Table 1 supports favorable local complexity changes: `Event` WMPC1 falls **23.64%**, and its LCOM improves slightly, **0.94%**. The authors attribute its higher AC to an unrelated added variable. At project level WMPC1 falls 11.54%, CF falls 16.67%, WMPC2 is unchanged, and LCOM **rises 2.78%**, rather than improving. LOC rises 11.48% and classes 25.58%. The prose's generalized cohesion improvement is therefore too broad for this table.

The authors attribute four added classes and about 3% of added lines to the pattern, calling this four of nine classes, 44.4%. The table instead has **eleven** added classes, 54−43; four of eleven would be 36.36%. Original source/metric output would be needed to resolve the denominator. The observed favorable selected-class result survives; neither this discrepancy nor a class-average reduction identifies a whole-project causal effect.

## Ice Hockey Manager

The releases are **0.1.1 and 0.1.2**; the then-current version is 0.2. The first already contains eight detected pattern instances; the second contains twenty-six. The comparison is therefore **more/different patterns plus other evolution**, not patterns versus none. The enumerated second-version counts sum to 26; Bridge is discussed in the worked example but not listed among the detector's named categories. Exact classification correspondence remains unverified.

The worked “Bridge–State” example separates `Player` into goalkeeper/field-player subclasses and links players to an independently specialized attribute hierarchy. It removes conditional handling in `PlayerAttributes`. The diagrams establish the described organization, not observed runtime changes of player position or measured correctness of state transitions. Table 2 summarizes all eighteen additional detected instances and other version changes, rather than isolating the two discussed patterns.

| Scope/version | LOC | Classes | AC | WMPC1 | WMPC2 | CF | LCOM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| PlayerAttributes0.1.1 | 535 | — | 91 | 78 | 110 | — | 2,237 |
| PlayerAttributes0.1.2 | 169 | — | 81 | 41 | 35 | — | 218 |
| Player package0.1.1 | 1,107 | 6 | 36 | 26 | 34 | — | 404 |
| Player package0.1.2 | 1,173 | 13 | 26 | 15 | 18 | — | 91 |
| Project0.1.1 | 8,680 | 86 | 37 | 14 | 14 | 9 | 50 |
| Project0.1.2 | 10,522 | 132 | 33 | 14 | 17 | 5 | 28 |

The selected class's WMPC1/WMPC2 fall **47.44%/68.18%**, and LCOM falls 90.25%. The package's values also improve, while LOC and class counts increase. Project CF and LCOM fall 44.44%/44%; AC falls 10.81%, WMPC1 stays 14 and WMPC2 **rises 21.43%**. The authors themselves acknowledge stable or slightly increased system-level complexity, potentially reflecting added functionality. Preserve those mixed results rather than treating every system metric as favorable or dismissing the substantial local changes.

Own arithmetic finds two further reporting mismatches. Package WMPC1/WMPC2 fall **42.31%/47.06%** from the table, not the prose's 43.6%/57.3%. Project classes rise **53.49%** (86→132), not 25.6%; project LOC rises 21.22%, agreeing with the paper. Package size increases 116.67% in classes and 5.96% in LOC. These are reconstructions of displayed values; unrounded or differently scoped original output is not available to resolve the discrepancies.

## Interpretation and next action

The evidence supports **concrete organization mechanisms and favorable selected-class/package structural changes alongside larger projects and mixed system metrics**. It does not directly measure maintainability as developer work. Pattern presence, new functionality, version, class count and changing aggregate denominators move together. Smaller classes and lower coupling density may be useful, but their relationship to actual change cost remains an empirical question rather than an effect estimated by this paper. No inference about Nu's comparative benefit or D1's explicit cases versus equivalent catch-all is licensed.

[S207](S207-game-pattern-development.md)'s lower counted LOC is not a contradiction: it compares different teams completing a supplied project, with preparation/reuse and instruction bundled into the treatment; S208 compares larger successor versions with new features. [S75](S75-game-smells-perception.md) contributes practice priorities and perceptions; [S184](S184-smells-maintenance-effort.md) contributes observed maintenance work with conditional modeling. Keeping those outcomes separate yields a stronger background than pooling them as generic evidence that patterns improve maintainability.

The bibliography retains consequential **unread** predecessors: Prechelt and colleagues' 2001 patterns-versus-simpler-solutions maintenance experiment; Vokáč and colleagues' 2004 replication in a programming environment; Bieman/Jain/Yang's 2001 industrial change study; and Huston's 2001 pattern/metric analysis. S208 mentions both favorable experiments and greater change-proneness of pattern classes, including the possibility that central classes receive more changes. These are title/reference and citing-context leads only, not four additional reconstructed methods or independent confirmations.

The selected S207/S208 reading gap is closed at the stated editions; source archives, original metrics and S207 task/scoring materials remain unresolved. Next return to acquired **S168**, whose later suite-size adjustment claim directly challenges the causal interpretation left open by [S165](S165-adequacy-size-methodology.md). It can change how oracle sensitivity evidence is interpreted and balances the recent game/practice emphasis. The new pattern predecessors remain conditional on their ability to change a specific claim; more pattern citations alone do not establish Nu's value.
