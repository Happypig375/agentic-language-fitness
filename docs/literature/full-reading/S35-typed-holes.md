# S35 — Static contextualization with typed holes

**Full read, 2026-09-16:** Andrew Blinn, Xiang Li, June Hyung Kim and Cyrus Omar, *Statically Contextualizing Large Language Models with Typed Holes*, PACMPL 8/OOPSLA2, article 288, DOI [10.1145/3689728](https://doi.org/10.1145/3689728). Read [arXiv 2409.00921v1](https://arxiv.org/abs/2409.00921v1), 2 September 2024, with October ACM imprint; publisher equivalence not independently compared.

Zotero parent `3B9UDAWZ`, PDF `UUZ43AXJ`, collection `PKLXQNEE`; 31 pages, 16,837,277 bytes; SHA-256 `4e5602e399f70350ccfabaf06706552504b905a869ee27b4f02232cc33d9cb0d`. Every page and reference consumed; all 19 numbered figures, result matrices, listings and API definitions inspected, with visual checks of all figure pages. No separate main-PDF appendix. Main reading complete; no model/IDE experiment reproduced.

## Method and closest overlap

The Hazel assistant retrieves the expected type, recursively relevant type definitions and a bounded list of type-related function headers for a hole, then optionally returns static errors for at most two corrective rounds. An informal Hazel tutorial/few-shot prompt is developed from observed error patterns. Header selection is a proof-of-concept, using type relationships, locality and completeness rather than a learned semantic relevance oracle.

MVUBench comprises five authored, small, pure model–view–update applications: tasks are completion of their update functions, with 10–15 held-out behavioral tests each. The alternatives include no added context, exhaustive application context and simple vector retrieval from a synthetic combined codebase. GPT-4-0613 is instruction-tuned; StarCoder2-15B receives a different prompt and no iterative repair. TypeScript is a close translation, with relevant headers manually supplied because the language server did not expose a satisfactory general method.

This is direct prior art for D3 and much of broad D1: an ML-family language, sum types, MVU state transitions, type-relevant context, compiler feedback and executed behavioral tests already occur together. An F# port or a Codex model label is not a new contribution. The experiment completes a missing function; it does not assign a source convention and observe how an autonomous agent preserves behavior under later domain changes.

## Results and inference limits

Figure 8's aggregate is **mean percentage of tests passed**, not percentage of fully solved applications. For Hazel/GPT-4, types+headers rise from 48 to 76 with error rounds; exhaustive context rises from 54 to 79. Figure 18 gives 73 to 80 for TypeScript types+headers and 70 to 76 for exhaustive context. These are printed descriptive values over five programs, not independent task-population estimates or proof of equivalence.

The paper itself supplies contrary/limiting evidence: StarCoder's type-appropriate headers hurt two Hazel cases; a single misleading retrieved chunk disproportionately harms the vector baseline; exhaustive context is competitive; the no-context condition is intentionally impoverished; useful headers presuppose already implemented helpers. The comparison does not show superiority over a modern tool-using agent that can freely inspect source. Different tutorials, prompting, models and language implementations do not isolate training prevalence or language superiority.

The stated 320 main trials (p. 14) do not reconcile with its own `8 configurations × 5 programs × 20 trials = 800`. Additional retrieval baselines are separate. The artifact's demonstration scripts deliberately use fewer repeats, so they do not silently repair the paper's denominator. Character counts for retrieved versus exhaustive context are not active token-window usage or total cost; correction rounds change cumulative traffic.

## Critical artifact inspection

[Zenodo artifact 12669479](https://doi.org/10.5281/zenodo.12669479) has one 14,909,411,219-byte ZIP, advertised MD5 `c43f8a87b238fb7ca3b6489f15ae1531`. The full archive/model was **not** downloaded and that whole-file digest is not verified. Bounded HTTP range requests read the central directory (47,020 entries) and seven selected text/data members; ZIP CRC checks and local SHA-256 cover those members. The authors publish the archive password and request that benchmark sketches not be reposted openly; no sketches or extraction dumps are committed here.

Fully read root/Hazel/TypeScript guides, Hazel `run.sh`, Hazel `util/collate_data.sh` and TypeScript's GPT types-and-headers driver. The Hazel driver enumerates five programs, eight static-context/error configurations and four baseline configurations, with one demonstration repeat and a 180-second command timeout. The TypeScript driver enumerates five programs and eight configurations, also one repeat. The root guide distinguishes these low-cost demonstrations from the paper's 20 repeats. No credentials, service, model, Docker image or author executable was used.

The paper-table exhaustive CSV has 200 rows, twenty for each of five program × two error-round cells. This checks **that baseline's** membership, not the full ablation dataset or its stated 320. Full raw-trajectory reconstruction, language-server internals, test adequacy and the remaining archive are unexamined. Selected source hashes are retained locally; this is bounded method inspection, not experimental reproduction.

## Discovery consequence

D3 is not recommended as a standalone F# context contribution on present evidence. For D1/D5, compare policies with the same available source and behavioral specification; do not manufacture a benefit by withholding definitions from a weak baseline. Use actual changes and preserved temporal/domain requirements if the claim concerns maintenance. Keep compilation, partial tests, all-obligation success and costs separate. TRACE (S36) is promoted to check whether subsequent-edit propagation already resolves the proposed distinction.
