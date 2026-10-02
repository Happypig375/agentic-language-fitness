# S228 — OpenGameEval: client/server checks and temporal observation

Tiantian Zhang, Kartik Ayyar, Mengsha Sun and Lynn Gong. **Using OpenGameEval to Benchmark Agentic AI Assistants for Roblox Studio.** [Roblox Engineering](https://about.roblox.com/newsroom/2025/12/opengameeval-benchmark-agentic-ai-assistants-roblox-studio),17 December2025. Primary practitioner article and bounded public-source reconstruction, read2026-10-02. This is not an additional fully read research paper.

## Identity, editions and actual coverage

Native webpage parent **`ZE9IAQ5W`**, note **`CM3S5ICQ`**, collection `PKLXQNEE`; the record exists before intentional full reconstruction. Parent version5238, type, URL and membership are refreshed. The initial discovery response had exposed the article before record creation; it was not previously credited as a completed reading. All article sections and six substantive figures are now inspected. Decorative header/footer assets are excluded. Four image routes initially fail in the web cache; normal HTTPS downloads succeed. No PDF is involved.

The official repository redirects from `Roblox/open-eval` to `Roblox/open-game-eval`. Inspect [current pin `9070ee70cf7e479f83f6cfe684937a6225ae3b77`](https://github.com/Roblox/open-game-eval/tree/9070ee70cf7e479f83f6cfe684937a6225ae3b77),28 August2026, and [article-date pin `54ef35637acf3f4b5cbe32e05e053f41c8161b7e`](https://github.com/Roblox/open-game-eval/tree/54ef35637acf3f4b5cbe32e05e053f41c8161b7e),17 December2025. The untruncated current tree has150 blobs,86 code-generation eval files and30 debugging files. The historical tree has47 evals. Current paths add40 and omit historical `073_homestore_dynamic_pricing.lua`; the current leaderboard still labels its population87. Exact result-roster correspondence is not established by47+40 arithmetic.

Ten current text files and four historical task counterparts are acquired with Git-blob/SHA-256 verification. Complete reads cover README, release log, current/historical leaderboards and four task scripts. The plugin guide is read at lines1–38 and326–501; the submission client at25–118 and218–250. The four historical diffs are inspected: metadata changes and relocation of health-test configuration leave the checked task bodies unchanged. Other tasks, six detailed model reviews, place files, plugin binary, live service and engine implementation remain uninspected. No account, credential, adapter, model call, installation or game execution is performed.

## What the method contributes

The original47 manually curated scenarios span object/property edits, mechanics, animation, interface and sound tasks in prepared Roblox places. An evaluation can check the edited scene and behavior during play, including client/server interaction and simulated input. Three traffic-light variants deliberately change the surrounding hierarchy and retained scripts. This is direct industrial prior art for context-sensitive interactive-software tasks, beyond isolated function completion.

The article describes expert prompts, reference solutions and human review. Public reference functions in the four inspected scenarios are empty, as the README says is intentional. The reference-testing Studio plugin is a separate authoring path: its guide describes edit checks, server checks and per-client functions, up to eight simulated clients. It runs a supplied reference implementation and does not invoke the assistant. The linked plaintext plugin-source directory is absent from the inspected tree; the binary is not reconstructed. The guide's reset description removes newly created instances, which does not itself establish restoration of modified pre-existing state. Do not equate these documented local mechanics with a verified cloud-service implementation.

The Python client sends the evaluation script and model configuration to the hosted service and polls `evalSucceeded`. A completed job and a passing task are separate fields. Timeout, service error and task failure retain different statuses; its printed success denominator nevertheless includes all requested files. It does not compute the leaderboard's repeated-attempt metrics. Passing all checks is the declared task-level rule, but the full host's check instrumentation and information exposure are not inspected. Sending the script to the service does not establish that the solving model sees its test code.

## Health regeneration: what is actually observed

Task **035**, in the laser-tag place, asks for regeneration beginning two seconds after damage at ten health per second. Setup removes the existing health script and creates a RemoteEvent whose server handler inflicts50 damage. The only populated play-check list is a **single client function**; no server health assertion is supplied in either inspected edition.

The client fires that event, waits0.1 seconds, then starts its clock. Fourteen checks require health exactly50, each followed by a0.1-second wait. It then waits until its own clock reaches2.1 seconds, requires health exactly60, waits one second and requires exactly70. This is useful executable delayed-state observation across a server-triggered damage path. It is more specific than a compile result or screenshot.

Its scope is narrower than the article's general server/timing/rate account:

- Early-regeneration checks cover roughly0.1–1.4 seconds after the client fires the event, not every instant up to two seconds. Scheduler/network delay is not measured against the actual server damage event.
- Exact60/70 endpoints favor a particular discrete update schedule. A continuously integrated ten-per-second implementation beginning at two seconds need not equal60 around2.2 seconds. This is a source-based valid-alternative concern, not a reproduced rejection.
- Observing client health after server damage does not establish that subsequent healing is authoritative on the server or replicated consistently to another client. Repeated damage, timer reset, multiple players, death/respawn and health caps are not checked here.

The bounded source neither proves that the published agents exploited a gap nor calibrates false acceptance/rejection rates. It identifies which intended obligations need separate evidence.

## Traffic lights: detecting changes versus a valid cycle

Task **017** inserts a particular asset into a baseplate and removes scripts. It requires a newly added source container, selects an initially illuminated light by exact transparency, and samples at0.5-second intervals up to ten times. Whenever that same starting light is off and another is on, it increments a counter; three counted observations suffice. **The starting light is never advanced.** A repeated observation of one switched state can therefore increment the counter repeatedly. This does not establish three distinct transitions, an ordered cycle or four-way safety. The asset's initial state and exact transparency conventions are additional dependencies.

Tasks **026 v2/v3** use the suburban intersection. V2 removes traffic and pedestrian scripts and a running flag; v3 retains pedestrian logic while removing traffic scripts. Their checks require a new Workspace `Script` containing the substring `light`, connect to six named spotlights, and wait20 seconds. Red/yellow/green flags are shared across both directions: an `Enabled` change in either direction sets the corresponding color flag. Passing requires all three flags, not an alternating sequence, mutually exclusive greens, minimum durations, changes in every direction or retained pedestrian behavior.

These variants provide meaningful context and integration demands. They also show why implementation-specific source checks, property-change coverage and intended temporal behavior should be recorded separately. The same behavioral assertions are present in the article-date snapshot, so these observations are not artifacts of silently substituting a later rewrite. Runtime/utility behavior and actual agent solutions remain unexecuted.

## Outcomes and evidence lineage

The article's leaderboard image has15 model rows. For example, Gemini3Flash reports **54.68% pass@1,65.73% pass@5 and39.98% all@5** on the original context; the source archive preserves that row. The article reports stronger performance on atomic edits than on contextual tasks, including health/traffic examples. That useful qualitative difficulty pattern is not independently recomputed here; the article does not provide per-case counts sufficient for a new mechanism estimate.

The current expanded leaderboard has seven model rows and a separate eleven-row debugging table. Definitions distinguish one successful attempt, at least one of five, at least three of five (`cons@5`) and all five; these are not interchangeable reliability claims. The stored47-eval archive has24 rows, so its later additions are not a frozen copy of the15-row article image. The30 debugging scenarios derive from15 base scenarios with injected bugs; they are not30 independent production projects or all natural faults. Release/model differences cannot be pooled into an intrinsic language, architecture or progress effect.

Prepared scenarios and native engine integration are useful evidence of a concrete evaluation method. They do not validate every assertion, establish representativeness of professional work, quantify net development benefit, or prove identical timing/network behavior to every deployed player environment. Mutable engine/service/assets, undisclosed prompt/budget details, result-roster binding and missing per-attempt outcomes retain separate limits. Current expected-tool/instance annotations are documented as hidden and non-grading; empty instance annotations mean unannotated, not zero dependencies. The April release log's removal of provisional fields does not describe their later restored state at the August pin.

## Reproducibility identities and survey consequence

Selected SHA-256 identities:

| Object | SHA-256 |
| --- | --- |
| Current health script | `d2fe4a7c2b026b1ed69bb8fdceaf8d541b8cac3ebcca5391939812d06d2e9f58` |
| Historical health script | `c1e58d5527c5972f33138226ed73ede0c02300c74fccf8f4084ab6138d11f853` |
| Current baseplate traffic test | `70fa500a02d2c33fd7b1eaca104a6492b1ae7ede1dcd2cf102fc9b3ee1d0dc95` |
| Current suburban v2 / v3 | `cb916bb742715275bf8c25c7b90140215b3560d42a6f824f731b039ec2da850f` / `f45ad73ac9794832003d51b7577bd96916bd493398da5a78300c56ca904fa85e` |
| Plugin guide | `a9b6b0c64b944d494cf1436493490be911751ee2a1f4310be79f3dd158d63758` |
| Submission client | `69ccf8c48a7530cc535fc86b58c275734a03a6d35a9861d5e8213161e4b595d1` |
| Article leaderboard image | `e8e825bc8e11d359e390d85218c43595ecffdf58d41b17312c4f7ffaa2b0b2e6` |
| Article architecture image | `87458bfaa036e0ac48ffeae3f27d56f014c8e6d4a5f58b5b131c65085c54b2f9` |

All acquisition/image manifests and bodies stay ignored. Published benchmark shortcomings are not a reason to discard adverse ISE results or seek favorable replacement tasks.

Together with S125/S226/S227, this source establishes several existing observation routes: state/trace assertions, scene/callback checks, GUI playtesting and client/server runtime tests. Nu's claimed benefits require an explicit relation to these mechanisms and their obligations, not a claim that interactive behavior has no prior evaluation method. No D1 source-convention benefit or permission to build an oracle follows.

**Next consequential action:** return to the unconsumed C05 supplied abstracts, selecting additional agent/language/evolution methods only when they change the claim map. OpenGame's primary baseline and incremental playtesting remain specific conditional dependencies. Preserve the unresolved source/result bindings, empirical Nu benefit and unrelated live/type-evolution gaps as different kinds of uncertainty.
