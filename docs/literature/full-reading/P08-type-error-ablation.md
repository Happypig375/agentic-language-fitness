# P08 - Type-Error Ablation and AI Coding Agents

## Identity and coverage

Shriram Krishnamurthi and Matthew Flatt, DOI `10.48550/arXiv.2606.01522`, arXiv v2, June 25, 2026; submitted manuscript, not a verified accepted journal article. Main Codex AI reader consumed all 26 PDF pages, references and disclosure. Rendered pp. 6, 8, 10, 12-14, 16, 18-19 cover all six tables, three figures and the complete experimental prompt. Zotero `VKL33569`, hash in [assets](assets.json).

## Population and intervention

Ten small Shplait programs (54-113 LOC) implement familiar undergraduate algorithms. Claude-assisted author construction produces tested correct programs, then six single type-error mutations each (60 chaffs). Every chaff must type-fail and fail at least five dynamic tests; tests were iteratively hardened against these mutations. Mirrored operands deliberately include difficult blame locations. These are selected, highly localized faults, not naturally sampled maintenance issues (pp. 5-8, 22).

The same Shplait source and typed-oriented minimal-edit prompt are used in four conditions: **all** returns the unification expression stack and locations; **proximate** returns one blamed expression/location; **min** returns conflicting types; **untyped** disables type checking and returns dynamic test failures (pp. 8-11). A discovered bug means min includes a location on 32 chaffs and none on 28. These are different task strata, not a randomized location ablation. Thirty-nine proximate reports hit the injected line; 21 do not. The untyped condition jointly changes checking and feedback content/volume; it does not isolate the causal effect of having a type system.

Mode pragmas are inserted by the oracle into a blank source line after editing, preserving line numbering and hiding the condition marker. A fresh aider process/context and source copy are used per trial; compiled caches are removed. The agent receives the language manual and built-in reference read-only, edits only `code.rhm` using SEARCH/REPLACE, and gets initial and subsequent oracle output. The test files are withheld but their failures are feedback; **there is no separate held-out evaluation suite** (pp. 9-11). Same-program repeated mutations/runs are not independent language samples.

Qwen2.5-Coder:14b via Ollama/aider is run ten sweeps of 240 trials (2,400). Haiku-4.5 plain and alpha-renamed conditions each have another 2,400 trials, clarified by table 6 and supplement. The primary result section specifies 600 seconds, although procedure text says five minutes; Haiku uses 300 seconds. Aider also stops after three reflection retries or a no-edit reply. Hardware varied; insufficient-VRAM jobs were cancelled and resubmitted (counts not reported). Cross-model timing is therefore not a fair fixed-resource comparison (pp. 11, 16, 19).

## Outcomes, contrary evidence and arithmetic

For Qwen, figure 3 gives successes of 201/600 untyped (33.5%), 250/600 min (41.67%), 287/600 proximate (47.83%) and 317/600 all (52.83%). All minus untyped is 19.33 percentage points; all minus proximate is 5 points. Successful trials usually finish on the first edit (median one, means at most 1.3). Thus this is mostly evidence about a useful initial diagnosis rather than recovery through many iterations (pp. 12-15).

The aggregate trend contains strong reversals: AVL chaff 3 succeeds 10/10 with min/proximate but 2/10 with all; Dijkstra chaff 2 succeeds 10/10 proximate but 0/10 all. Qwen's no-location bin has min 34.6% versus proximate 32.9%. Haiku plain is near ceiling; its no-location ordering test is not significant (p=.30). Obfuscated Haiku has a nonmonotonic min dip, including worse results than untyped. Renaming also changes formatting, and logs show frequent recognition of familiar algorithms; this is not proof that names or training familiarity are irrelevant (pp. 14, 16-18).

The reported 854/872 = 97.94% semantic success conditional on type-correct final submissions applies to the three typed conditions and this selected single-fault corpus. It is not a substitute for independent behavior tests in ALF. The same corpus was constructed by models related to those tested. Page's ordered test uses chaff/run blocks (280 and 320); the Haiku Jonckheere-Terpstra analysis treats calls as independent rather than blocking by chaff. API-call independence does not remove shared task difficulty; generalization would require task/program clustering and repeated-model uncertainty (pp. 12-19). No p-values are recomputed here.

More verbose type feedback can still use fewer total tokens than dynamic-only logs: Qwen mean input 7,380 all versus 11,384 untyped (table 6). Repeated context is charged again per turn. This does not establish an optimal diagnostic byte limit or a provider context threshold.

## Supplement inspection and limits

The paper's concept DOI `10.5281/zenodo.20481462` resolves to [version 20847171](https://doi.org/10.5281/zenodo.20847171), June 25. The 2,718,888-byte tar.gz was downloaded and verified against MD5 `40883226de78385f4c8eed58755f711c`; 7,601 archive entries were inventoried without extraction/execution. Read-only inspection covered README, `harness/oracle.sh`, `prompt.txt` and `run_experiment.sh`. README identifies MIT harness code and CC-BY-NC-SA-4.0 data; original bodies remain outside Git. It pins Shplait `bcbfd4aeb4033b626ebdcb06837da2b88468f45d`, explicitly omits cluster scripts, and distinguishes analysis reproduction from end-to-end reproduction.

The released harness additionally retries rate-limited API trials up to six attempts, restoring source between attempts. Its final token/cost parsing reads the last attempt's log while elapsed time includes the retry interval; that is not a complete attempted-usage ledger. `success` is detected by the substring `SUCCESS` in the agent log rather than an independently rerun final oracle. These are source-bound accounting/oracle limitations, not evidence that a published row is necessarily misclassified. The runtime program, archived output adjudication, dependency versions and full analysis were not rerun. The released default timeout is 300, with a CLI override; historical primary 600-second runs still rely on the paper/omitted cluster setup. The artifact prompt adds documentation instructions beyond the displayed shortened prompt.

## ALF implication

Retain useful **current** type/test diagnostics and separate diagnostic content from stale-history management. Reject any blanket claim that shorter feedback helps, all history harms, or type-checking suffices for behavior. Keep apparatus failures and every attempted debit distinct from candidate failure; use an independent final oracle and a fixed feedback/repair contract. Nothing here supports a general F#/C# or Nu advantage.
