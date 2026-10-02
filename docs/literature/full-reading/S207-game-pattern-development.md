# S207 — game development with prepared pattern classes

## Identity and coverage

Roberto Tenorio Figueiredo and Geber Lisboa Ramalho, *GOF design patterns applied to the Development of Digital Games*, SBGames 2015, Computing Track, pp.1–8, [primary proceedings PDF](https://www.sbgames.org/sbgames2015/anaispdf/computacao-full/146712.pdf). Native parent/note **`X5R8ZTSR`/`2AXV78B8`** are created after DOI/title/URL deduplication and before body reading; PDF **`AU87ZI74`** is attached and its native bytes verified. Eight pages, 1,006,350 bytes, SHA-256 `88601db3e89c346316c14c39c1e5b47eb03684776e8718eb54eb77bca3f0b493`.

All eight pages, thirteen figures (twelve class diagrams and one three-panel game image), the unnumbered six-row results table and seventeen references read. Visual pages 3–8 include every figure and the table; pp.1–2 are text-only. Web W363 returns lines0–437 of609, ending partway through p.6; native text closes the remainder. The ordinary download initially returns HTTP406; a normal request with PDF Accept and browser User-Agent headers returns the verified PDF. No GUI, authentication workaround or paid access is used.

The paper's `http://www.osfedera.com/get/federa/Dis_final.zip` link promises the complete 23-pattern exposition. Both the printed HTTP and corresponding HTTPS routes fail with connection errors in W364. Its exact contents, original participant code, ready-made classes, requirement sheets, tests and logs remain unavailable in this pass. The failed supplement route does not establish absence of those materials. No author code or game is run; arithmetic below is own reconstruction from the printed table.

## What is proposed and what is compared

Section 4 provides didactic before/after design examples for **Builder, Prototype, Singleton, Flyweight, Observer and State**. It describes varied enemy construction, cloning, instance uniqueness, shared versus individual enemy data, subscriber notification and character-state behavior. These are prior organizational mechanisms, not six comparative trials. The examples do not benchmark allocation, memory or runtime performance, and class diagrams alone do not verify all lifecycle, access, ordering or behavior claims. In particular, the State example is a polymorphic representation alternative; it does not compare equivalent explicit-case and catch-all matches.

Section 5 is a separate classroom comparison involving six teams of three FACAPE computing students: **18 students but six team-level observations**, three per condition. The authors try to balance C# and game-development experience; no random allocation procedure, balance table or individual ability measurement is reported. The experiment chooses only **Singleton, Prototype and Facade**, based on feasibility and time. Facade is not one of the six illustrated patterns above, and most illustrated patterns are not evaluated.

The day before development, teams A/B/C receive instruction on those three patterns, reportedly without game-specific application hints. D/E/F receive no corresponding explanation. All teams receive an ongoing project, game requirements and images, with one computer per team and Visual Studio 2010/XNA installed. A/B/C additionally receive **ready-made pattern classes**. The authors explicitly intend to demonstrate reuse of that supplied code. The treatment therefore combines instruction, prepared implementation resources and a requested design approach; it does not isolate source organization from those resources.

The task is a one-screen spaceship game: player and enemies shoot in opposite directions; three hits kill the player and ten enemy kills win. A prize goes to the team finishing all specifications first. This is completion of a supplied game project, not a sequence of later maintenance changes, an adoption-cost study or a professional comparison. The full requirements, whether/how testing is performed, the completion rubric, bug definition and adjudication, assistance, permitted resources and precise timing/stopping rules are not reported. The one-day teaching and production of reusable classes are outside the displayed implementation times.

## Observed outcomes and arithmetic

| Team | Prepared-pattern condition | Approximate time | Completeness | Bugs | LOC | Classes |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
|A|Yes|6h50m|100%|0|246|21|
|B|Yes|6h36m|90%|1|253|23|
|C|Yes|6h05m|100%|0|218|25|
|D|No|7h40m|100%|1|345|15|
|E|No|9h45m|80%|1|259|1|
|F|No|6h40m|100%|1|251|6|

Own arithmetic gives average implementation time **390⅓ versus 481⅔ minutes**, about **91⅓ minutes or 18.96% lower** in the prepared-pattern condition. The paper prints 6h31m versus 8h02m and approximately 18.9%; that small difference comes from minute summaries, not a reversal of the result. Median team times are 396 versus 460 minutes. The faster pattern result is a legitimate descriptive finding under the reported bundle; no p-value, uncertainty interval or independent repeated-task comparison is supplied.

Each condition has two fully complete teams, while the other teams achieve 90% and 80%. The averages are 96⅔% versus 93⅓%. One versus three bugs are reported; all three comparison teams have one bug. Preserve this favorable observed quality direction while retaining the unspecified oracle and different completion levels. These are not times to one demonstrably common fully correct endpoint. Do not discard B/E to create a favorable completed-only mechanism estimate or treat their partial output as missing at random.

The printed **717 versus 855 LOC are sums**, although p.8 calls them averages. Actual team means are **239 versus 285**. The relative reduction **16.14%** remains correct because each group contains three teams. Whether supplied classes, inherited starter code, comments or generated code are included is not specified; fewer counted lines do not establish a smaller total delivered system or a lower lifecycle investment. Mean class counts are **23 versus 7⅓**, approximately **3.14×**. The source organization uses more classes while the reported code-line count is lower; class count, LOC, typed effort and runtime memory remain distinct outcomes.

## Interpretation and survey consequence

This paper supplies **favorable small-sample evidence for a prepared pattern/reuse teaching package**, not merely an opinion about patterns. That positive observation should remain in the survey. Three teams per condition, imperfectly described allocation, one game, prize-driven completion, different instruction/code resources and unreported outcome validation prevent attributing the entire difference to patterns alone or estimating transfer to professional game maintenance. A claim about all GoF patterns, net preparation-plus-development cost, frame time, future extensibility or Nu is not tested.

The six design examples remain useful alternatives to language-specific novelty claims. However, the broad statements that productivity improvement is already proved and that this is a first systematic application are not adopted as review conclusions. In the related-work paragraph, a game-defect study is attributed to Björk/Holopainen although the bibliography separately includes Ampatzoglou and colleagues' 2011 defect study. The latter is the consequential primary lead already retained from S75; the ambiguous citation does not create another empirical case.

[S75](S75-game-smells-perception.md) cites S207 as positive game-development evidence. The primary method now narrows that account to its supplied-code/training bundle and clarifies the LOC total/mean error without erasing the improvement. [S184](S184-smells-maintenance-effort.md)'s conditional effort model addresses different work and exposure. For prospective research value, account for preparation and reusable assets separately from current-task work, keep correctness/completeness beside time, and identify which resource or design difference is actually assigned. This is a measurement consequence, not authorization to construct a new trial.

[S208](S208-game-pattern-evaluation.md) is now reconstructed from its fourteen-page revised manuscript. It measures structural proxies across larger successor game versions with added features, which is not a contradictory result for this study's supplied-code classroom comparison. The next selected method is acquired S168 on suite-size adjustment, a direct dependency of the oracle-evidence interpretation. The unavailable S207 exposition and original task/scoring materials remain explicit access/method gaps; independent runtime, persistence, oracle and type-evolution work continues.
