# Zotero core reading collection

**Prepared 2026-09-15 UTC; queue source `2cc51940181dd7adb885ff68de1f02b260221166`.** The user requested pulling the latest repository changes and creating a Zotero collection for adding PDFs. The checkout fast-forwarded from `73d0a23` to that source; the unrelated untracked `uv.lock` was preserved.

The top-level collection in My Library is **ALF - Core Paper Reading Queue (2026-09-15)**, key `PKLXQNEE`. Its local selection URI is `zotero://select/library/collections/PKLXQNEE`.

## Records and scope

The collection contains exactly the thirteen core works specified by the [base handoff](full-paper-reading-handoff-2026-09-14.md) and [P12/P13 extension](nu-form-factors-and-research-leads-2026-09-14.md). Each record has its original P01–P13 tag, the shared `ALF core reading` tag, full title, authors, DOI, publication date, source URL and edition/acquisition hints in Extra. Conditional readings and other discovery hits were not promoted.

| ID | Paper | DOI | Zotero item key |
| --- | --- | --- | --- |
| P01 | LLMs for Architectural Refactoring: An Exploratory Study on Monoliths to Microservices | `10.1109/ICSA66085.2026.00033` | `S76KXR3C` |
| P02 | Architecture-level modifiability analysis (ALMA) | `10.1016/S0164-1212(03)00080-3` | `F9W52X95` |
| P03 | Does Code Cleanliness Affect Coding Agents? A Controlled Minimal-Pair Study | `10.48550/arXiv.2605.20049` | `DMRG56CT` |
| P04 | Is Agent Code Less Maintainable Than Human Code? (CodeThread) | `10.48550/arXiv.2606.21804` | `FJMUKCZT` |
| P05 | SlopCodeBench: Benchmarking How Coding Agents Degrade Over Long-Horizon Iterative Tasks | `10.48550/arXiv.2603.24755` | `WG2ALA8Q` |
| P06 | ChainSWE: Benchmarking Coding Agents on Multi-Bug Software Maintenance | `10.48550/arXiv.2607.02606` | `KDR3Z9UV` |
| P07 | Needle in the Repo: A Benchmark for Maintainability in AI-Generated Repository Edits | `10.48550/arXiv.2603.27745` | `PZJFA3SG` |
| P08 | Type-Error Ablation and AI Coding Agents | `10.48550/arXiv.2606.01522` | `TUJJ7JU4` |
| P09 | The Complexity Trap: Simple Observation Masking Is as Efficient as LLM Summarization for Agent Context Management | `10.48550/arXiv.2508.21433` | `NXQAZ5K8` |
| P10 | When the Specification Emerges: Benchmarking Faithfulness Loss in Long-Horizon Coding Agents | `10.48550/arXiv.2603.17104` | `ZB685P9D` |
| P11 | GameEngineBench: Evaluating Coding Agents on Real C++ Runtime Environments | `10.48550/arXiv.2607.03525` | `RJ9GV3AP` |
| P12 | Theory of Code Space: Do Code Agents Understand Software Architecture? | `10.48550/arXiv.2603.00601` | `R833TUNQ` |
| P13 | CodePlan: Repository-Level Coding using LLMs and Planning | `10.1145/3643757` | `LLMGIWQM` |

These are metadata records: ten preprints, two journal articles and one conference paper. CodePlan uses the published DOI; `10.48550/arXiv.2309.12499` is retained in Extra as a related preprint/access lead, without creating another study record.

## Metadata and edition checks

Exact DOI metadata was retrieved from Crossref for P01/P02/P13 and DataCite for the ten arXiv works. Each item's Extra field records its registry URL. All thirteen DOI identities and titles matched the queue; the library check found no existing DOI/title matches before import. This is identity verification, not a new literature synthesis or full reading.

ArXiv landing pages and DataCite version histories identify newer v2 editions for [ChainSWE](https://arxiv.org/abs/2607.02606) and [GameEngineBench](https://arxiv.org/abs/2607.03525). Their records preserve both the handoff's v1 PDF link and the newer v2 link. Other prior-review arXiv hints remain P03/P04/P07/P10 v1, P05/P08 v2, P09 v3 and P12 v4. Imported arXiv dates describe the current registry edition. No method/result comparison between editions was performed. The later reader must preserve historical editions and examine relevant revisions under the existing handoff rules.

## Verification and next action

The collection was created through Zotero Desktop 9.0.6 and populated through its local Connector `saveItems` endpoint (HTTP 201). Local API readback verified thirteen unique DOIs, collection membership, exact titles, author lists, item types, dates, Extra fields and queue tags. All thirteen records had zero child items at verification; no PDF, snapshot or reading note was attached. No direct library-database modification was used.

The user can attach PDFs to the corresponding records. PDF identities, hashes, page coverage and reconstruction remain pending; no full-reading index or paper completion record was created by this metadata-only task. The experiment allocation remains zero and all construction/execution holds remain unchanged.

Repository changes are confined to this note and the linked PLAN paragraph. Self-review, all eleven existing CI-routing tests, strict UTF-8 decoding and Git whitespace checks passed locally. Applicable CI scope is documentation; runtime checks are not revalidation evidence for this task. Verify the documentation CI run on the exact containing publication.
