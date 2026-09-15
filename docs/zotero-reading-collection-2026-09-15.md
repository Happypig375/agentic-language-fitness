# Zotero core reading collection

**Current update (2026-09-15 HKT):** the user added CodePlan's 2024 publisher PDF. The collection now has thirteen works and **sixteen PDFs**. Earlier acquisition snapshots below remain history; complete reading is recorded separately in the [full-reading index](literature/full-reading/INDEX.md) and [synthesis](literature/full-reading/synthesis.md).

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

## Initial metadata-import verification

The collection was created through Zotero Desktop 9.0.6 and populated through its local Connector `saveItems` endpoint (HTTP 201). Local API readback verified thirteen unique DOIs, collection membership, exact titles, author lists, item types, dates, Extra fields and queue tags. All thirteen records had zero child items at verification; no PDF, snapshot or reading note was attached. No direct library-database modification was used.

At the initial metadata-import checkpoint, PDF identities, hashes, page coverage and reconstruction were pending; no full-reading index or paper completion record was created. The authorized attachment follow-up below updates acquisition status. The experiment allocation remains zero and all construction/execution holds remain unchanged.

The initial publication changed this note and the linked PLAN paragraph. Self-review, all eleven existing CI-routing tests, strict UTF-8 decoding and Git whitespace checks passed locally. Exact publication `eb8e1ccd6c3c3349c972b251978ec6a693bb2400` passed [CI 34878897925](https://github.com/Happypig375/agentic-language-fitness/actions/runs/34878897925) with documentation scope; runtime jobs were skipped.

## Open-access attachment follow-up (2026-09-15 UTC)

The user then explicitly requested automatic attachment of open-access papers. Starting from metadata publication `eb8e1ccd6c3c3349c972b251978ec6a693bb2400`, all thirteen records were checked for existing attachments; none had a PDF. **Fifteen PDF files are now attached to the same thirteen parent records in collection `PKLXQNEE`.** P06 and P11 each retain both the prior-review v1 and newer v2. No duplicate parent records or conditional studies were added.

Acquisition used explicit version URLs at arXiv, the existing ALMA author route, and the public preprint download on the official ICSA program page. P01's conference-hosted file `preprint_draft_53141.pdf` has an EasyChair cover dated June 24, 2026, followed by the paper; its 13-page count includes that cover. The earlier P01 body-access limitation is now resolved for this author preprint, without claiming equivalence to the publisher edition. P02 is the published JSS 69 (2004), pp. 129-147 article hosted by an author; the first-page imprint and DOI were inspected.

CodePlan's [ACM PDF route](https://dl.acm.org/doi/pdf/10.1145/3643757) and linked publication landing route returned HTTP 403. Its [Microsoft author page](https://www.microsoft.com/en-us/research/publication/codeplan-repository-level-coding-using-llms-and-planning-2/) and [author repository](https://github.com/microsoft/CodePlan) establish the publication/preprint lineage. The attached arXiv v1 is explicitly labelled **2023 preprint; not the 2024 publication**. The preferred 2024 published PDF remains unavailable in this pass; do not substitute the preprint's counts or methods as though that edition had been read. No paywall or access-control bypass was used.

Each asset below was checked for PDF format, readable page structure, matching first-page title, and the explicit arXiv version stamp where applicable. Unicode ligatures were normalized for title comparison. Rendered identity pages were also inspected for P01, P02, P03 and P13. This was acquisition and identity checking only: **no complete-paper reading, method reconstruction, supplement review or edition-result comparison occurred**. P06/P11 author lists differ between versions, so the parent metadata and each attachment's edition must remain distinguishable.

| ID | Attached edition / source | Attachment key | PDF pages | Bytes | SHA-256 |
| --- | --- | --- | --- | --- | --- |
| P01 | [Conference author preprint](https://conf.researchr.org/details/icsa-2026/icsa-2026-papers/27/LLMs-for-Architectural-Refactoring-An-Exploratory-study-on-Monoliths-to-Microservice) | `ZKKCQBDZ` | 13 | 13636777 | `04e1da57c02bbe164bba8a3e35391265645f4e555a5a8dcb51a875c252040be2` |
| P02 | [Published article, author copy](https://www.cs.vu.nl/~hans/publications/y2004/alma.pdf) | `45CCEA6L` | 19 | 488665 | `35d116f1311a826abaa4eddc3808849aa9dd75863d13020d91c96050e5c61a2a` |
| P03 | [arXiv v1](https://arxiv.org/pdf/2605.20049v1) | `Z7ZAEPIJ` | 14 | 1252778 | `ff5d78e7ccbf58ca32a4b06e3a8792e40d2872a373c334b84dadc288a6b0b24a` |
| P04 | [arXiv v1](https://arxiv.org/pdf/2606.21804v1) | `L7FG5XKP` | 21 | 5353746 | `b73b5c6a583d06a484f90420566ade6964f73a331e15ec2cde1bbaf628b3ab26` |
| P05 | [arXiv v2](https://arxiv.org/pdf/2603.24755v2) | `46LPN8N7` | 26 | 753356 | `e40b72e59a07c36f46c493fa444309fdb2be15943f5f375d3695b7620e01a218` |
| P06 | [arXiv v1](https://arxiv.org/pdf/2607.02606v1) | `8F2EA7B6` | 18 | 1965871 | `7581c20f348dc6f6733a7eb28e7a8fc5480dc15a694a18ce6d963bae5cd8d456` |
| P06 | [arXiv v2](https://arxiv.org/pdf/2607.02606v2) | `FMTJ9SHC` | 19 | 1888489 | `be24179287e58e3aaede86804adead7f88a47fdc7be52359590bb35c7d4421bc` |
| P07 | [arXiv v1](https://arxiv.org/pdf/2603.27745v1) | `UF73YJF4` | 16 | 4051067 | `2b183e5a43b82bd36d03fba4fd820c8a8cbd71e1bf8e7daf3b6ecfdc64d85c3a` |
| P08 | [arXiv v2](https://arxiv.org/pdf/2606.01522v2) | `VKL33569` | 26 | 1048955 | `50a0cacd987b67bb27034664502ad2db6b237eaff8556fe4a64ead28b3737d55` |
| P09 | [arXiv v3](https://arxiv.org/pdf/2508.21433v3) | `R4Z4K5CW` | 31 | 1380836 | `e40b2fe085fe0a0867b43d845ec3778305d27a8f4d94af409d0d387b69e2866a` |
| P10 | [arXiv v1](https://arxiv.org/pdf/2603.17104v1) | `PF24JPY6` | 19 | 805083 | `72dd6eb6798bf42972d8dc107d8ba012f255ac647a0dda12f8ceee88755d5262` |
| P11 | [arXiv v1](https://arxiv.org/pdf/2607.03525v1) | `A696WU9C` | 17 | 9039204 | `7130bde23c356a89762ed47823f60c979173e4d2e5f4252bf940a8f9a0c12d61` |
| P11 | [arXiv v2](https://arxiv.org/pdf/2607.03525v2) | `WRJ2UKZ3` | 17 | 8677848 | `320b4d2722fef3647ae0896d9bcce43dc42e6531cca3391e3b11e62c0eea7edb` |
| P12 | [arXiv v4](https://arxiv.org/pdf/2603.00601v4) | `RXVC7BGE` | 14 | 1044961 | `4f14a77f038a1647f41ff1fb95e90e7d88f922aa158eef243da5e9ff00ce13d6` |
| P13 | [2023 arXiv v1 preprint](https://arxiv.org/pdf/2309.12499v1) | `5YYZ9ETS` | 34 | 2177115 | `1c66e59351ba27e22fb2c6aeaa3bf4f35681f198a9c3c106f910e4290505315e` |

The local Connector `saveAttachment` endpoint returned HTTP 201 for all fifteen files. API readback checked the intended parent key, PDF content type, source URL and edition label, followed by SHA-256 and size comparison against the actual Zotero-stored file for every attachment. Final inventory confirmed thirteen parent records and fifteen PDFs, with one PDF per work except the two labelled P06/P11 edition pairs. Reusing a previously attached, byte-matching PDF did not create a second copy.

The binaries are stored in Zotero, not committed here. Attachment keys in the table can be resolved through the local API or `zotero://select/library/items/<attachment-key>`. The collection is ready for reading; acquisition does not close the full-reading assignment. The next reader should reuse these assets and hashes, start the actual coverage index when reading begins, and retain the CodePlan published-edition gap. All experiment allocations and construction/execution holds remain unchanged.

## User-supplied publication and completed reading update

CodePlan parent `LLMGIWQM` now has publisher attachment `LS9AUVZE`: **24 pages, 1,202,157 bytes, SHA-256 `c31dec9440c699aaffb5597139e9ea8b13f8409e84f954723a881a58af671e08`**. Its first page identifies PACMSE 1/FSE article 31, July 2024, DOI `10.1145/3643757`, with CC BY 4.0. The user supplied this file; no claim is made that the earlier HTTP 403 route became accessible. Their renamed 2023 preprint attachment is preserved.

The publication was read in full for [P13](literature/full-reading/P13-codeplan.md), and all thirteen chosen core editions now have reconstruction records. Sixteen PDFs represent thirteen works, including historical P06/P11 v1 and CodePlan preprint editions. [Current assets](literature/full-reading/assets.json) separate catalog authors from edition authors and retain exact hashes. No Zotero items were modified during this reading pass. Original arithmetic, bounded artifact checks and proposal revisions are in the synthesis; no allocation or construction follows automatically.

## Novelty, value and rigor follow-up

The user requested adding every new full-reading candidate to this same collection. Three records were added after library-wide DOI/title duplicate checks; the two available open-access PDFs were attached automatically. The user then attached the Lassing publisher PDF. All three papers are now fully read for the [proposal assessment](proposal-novelty-value-validity-2026-09-15.md).

| ID | Added paper | Parent key | PDF attachment | Completion note |
| --- | --- | --- | --- | --- |
| A01 | Lassing et al. (2003), How well can we predict changes at architecture design time? | `DH37JS6Z` | `PDAAF9CS`, user-supplied publisher PDF | `MZ2ZESZ9` |
| A02 | Runeson and Höst (2009), Guidelines for conducting and reporting case study research in software engineering | `VP6XD6XW` | `V37TJNUP`, Lund institutional PDF | `ALQ75MK4` |
| A03 | Peng et al. (2026), Benchmarking the Residual | `PU4ASENH` | `WFVP6YXC`, arXiv v1 | `4BC8QJ4H` |

At this follow-up checkpoint, collection totals were **16 parent works and 19 PDFs**. Connector/local API readback verified destination, exact supplied metadata, attachment parents and stored PDF hashes. The [follow-up ledger](proposal-novelty-value-validity-sources-2026-09-15.md) records byte identities, complete text/visual coverage and methods. Verified completion notes supersede A01's import-time access limit in Extra. The original core assets and historical edition snapshots above remain identifiable. No copyrighted paper bodies were committed and no experimental allocation followed.

## Selection-literature import update (2026-09-16 HKT)

The [selection acquisition record](zotero-selection-acquisition-2026-09-15.md) adds S01–S18 to the same collection, with sixteen automatically attached PDFs for fifteen works. Verified totals are now **34 parent works and 35 PDFs**. The original sixteen parent records and nineteen PDF hashes above remain unchanged. S02/S04 still need copies; S07 is open access but its download is blocked. This acquisition does not change the earlier full-reading records or certify a new full read.
