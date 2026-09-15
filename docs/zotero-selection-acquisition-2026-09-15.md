# Zotero selection-literature acquisition checkpoint

**2026-09-15; queue source `033bb2c`.** The user requested `git pull`, collection of the additional literature, automatic attachment of open-access PDFs, and manual handling of unavailable publisher sources. The checkout fast-forwarded from `78c2eea` to `033bb2c`; the unrelated untracked `uv.lock` was preserved.

**Import completed and verified 2026-09-16 HKT (2026-09-15 UTC).** Eighteen S01–S18 papers and sixteen PDFs for fifteen works were added to the existing collection. It now contains **34 parent works and 35 PDFs**. Independent local API and stored-file readback verified the new records and attachments; the original sixteen parent records and nineteen PDF hashes are unchanged. Three works still need PDFs, as listed below.

At publication `9be45f6`, this batch was staged but not imported because another session was using the Run JavaScript window. The user clarified that it was working on a different collection and had finished. The prepared import then ran as one collection-specific JavaScript call through native window controls, without shared mouse, keyboard or clipboard input. The script cleared its own marked editor content after completion.

Destination remains **ALF - Core Paper Reading Queue (2026-09-15)**, collection `PKLXQNEE`, user library 1. [Living reading program](literature/selection-priority-reading-2026-09-15.md) owns reading priorities; this is an acquisition record, not a new full-reading or evidence-closure claim.

## Imported records and assets

| ID | Zotero parent | Work | DOI | Attached PDF edition(s) |
| --- | --- | --- | --- | --- |
| S01 | `IQXQNNN7` | ASlib: A benchmark library for algorithm selection | `10.1016/j.artint.2016.04.003` | arxiv-v3, 36 pages |
| S02 | `ILICHNU6` | Using Generative Artificial Intelligence for Suggesting Software Architecture Patterns from Requirements | `10.1007/978-3-031-66336-9_19` | PDF still needed |
| S03 | `XGKNHB3A` | Failure-Aware Enhancements for Large Language Model (LLM) Code Generation: An Empirical Study on Decision Framework | `10.48550/arXiv.2602.02896` | arxiv-v1, 7 pages |
| S04 | `6EX7AWI8` | MicroRec: Leveraging Large Language Models for Microservice Recommendation | `10.1145/3643991.3644916` | PDF still needed |
| S05 | `NNMHM5DQ` | Generative AI for software architecture. Applications, challenges, and future directions | `10.1016/j.jss.2025.112607` | arxiv-v2, 26 pages; publisher-trepo-multipart, 20 pages |
| S06 | `JWF6FAFE` | Algorithm selection on a meta level | `10.1007/s10994-022-06161-4` | publisher, 34 pages |
| S07 | `3B7596AC` | Can large language models support machine learning implementation in product development? A comparative analysis and perspectives | `10.1017/pds.2025.10100` | PDF still needed |
| S08 | `ATDVX5GR` | ArchBench: Benchmarking Generative-AI for Software Architecture Tasks | `10.48550/arXiv.2603.17833` | arxiv-v1, 5 pages |
| S09 | `XBISAYTM` | Can AI Agents Generate Microservices? How Far are We? | `10.48550/arXiv.2603.09004` | arxiv-v1, 12 pages |
| S10 | `5ZWBZGH6` | MARS: Modular Agent with Reflective Search for Automated AI Research | `10.48550/arXiv.2602.02660` | arxiv-v3, 66 pages |
| S11 | `XSVXJ83C` | Compiling Large Multi-Modal Requirement Documents into Runnable Software Systems: From an Agentic Test-Driven Perspective | `10.48550/arXiv.2602.13723` | arxiv-v6, 24 pages |
| S12 | `SRP4EDCM` | Mining Architectural Quality Under Agentic AI Adoption: A Causal Study of Java Repositories | `10.48550/arXiv.2606.13298` | arxiv-v1, 16 pages |
| S13 | `A66HMDDL` | Sustainability evaluation of software architectures: a systematic review | `10.1145/2000259.2000263` | author-preprint, 10 pages |
| S14 | `27IDJICS` | Measuring Architecture Sustainability | `10.1109/ms.2013.101` | author-preprint, 11 pages |
| S15 | `C92CFZDN` | Impact of Experience and Team Size on the Quality of Scenarios for Architecture Evaluation | `10.14236/ewic/ease2008.1` | open-indexed-copy, 10 pages |
| S16 | `PL6GQJCW` | Algorithm Selection for Combinatorial Search Problems: A Survey | `10.1609/aimag.v35i3.2460` | publisher, 13 pages |
| S17 | `RRKTU3PA` | Building Software by Rolling the Dice: A Qualitative Study of Vibe Coding | `10.48550/arXiv.2512.22418` | arxiv-v2, 23 pages |
| S18 | `6WG9KCWH` | Technical Dimensions of Programming Systems | `10.22152/programming-journal.org/2023/7/13` | journal-arxiv-v1, 59 pages |

## Download identities

All sixteen files have a valid PDF signature, readable page structure, matching title on the first two pages, a recorded SHA-256, and visually inspected first-page title/edition information. This is identity coverage only, not complete-paper text, figure, table, appendix or method coverage. Supplement reconstruction and publisher/preprint method comparisons remain pending.

| ID / edition | Attachment key | Source PDF | Pages | Bytes | SHA-256 |
| --- | --- | --- | --- | --- | --- |
| S01 / arxiv-v3 | `ZJPH5PL3` | [PDF](https://arxiv.org/pdf/1506.02465v3) | 36 | 698249 | `08d9eff968d0311cfafbf21601986424fdee7f087a01ba473bf19893119d0e1b` |
| S03 / arxiv-v1 | `BHQG6SH6` | [PDF](https://arxiv.org/pdf/2602.02896v1) | 7 | 136220 | `36af4b38153b236978bb7d6c60ad9e2a533d075f95187809512093d8fa6d22d3` |
| S05 / arxiv-v2 | `FRBPI6HV` | [PDF](https://arxiv.org/pdf/2503.13310v2) | 26 | 1350974 | `6a007713f361d98be2e69b7b8e1149f6e600e7d2da454393466477bbe06420a8` |
| S05 / publisher-trepo-multipart | `3PLW2WXT` | [PDF](https://trepo.tuni.fi/bitstream/handle/10024/231421/Generative_AI_for_software_architecture._Applications_challenges_and_future_directions.pdf?sequence=1&isAllowed=y) | 20 | 2874703 | `8239ace1dfdf85a30e219fe8cc054459fd6f477be437c831117f87650ad03e7f` |
| S06 / publisher | `YFI7MN3P` | [PDF](https://link.springer.com/content/pdf/10.1007/s10994-022-06161-4.pdf) | 34 | 1626625 | `c1eaafb1ec78191bcf4ef7d04186feaaf63bb7ba31db1d3939a28e6f3b5e6820` |
| S08 / arxiv-v1 | `NLRFPSRA` | [PDF](https://arxiv.org/pdf/2603.17833v1) | 5 | 4919024 | `9a07b5984d2ec41a4fad07779a8c1a2f7b33f7e6c0d0b4d7bfa32ee27a08285e` |
| S09 / arxiv-v1 | `8WYKMNBM` | [PDF](https://arxiv.org/pdf/2603.09004v1) | 12 | 616761 | `fedfc5de4dfb6f1eddb0441b81c5972930d683a5035e83688cc7f2faaf6745eb` |
| S10 / arxiv-v3 | `EALLR4ZF` | [PDF](https://arxiv.org/pdf/2602.02660v3) | 66 | 3659239 | `017fad55cfef0d7a956c5ee018b419343b3890aaec707daf90f0bc3ec549dd1d` |
| S11 / arxiv-v6 | `SGZ9QM88` | [PDF](https://arxiv.org/pdf/2602.13723v6) | 24 | 769797 | `32703318ef94161499f3d2607a4362f04a879b2ac93afd3a3c183f6f1aba0ef3` |
| S12 / arxiv-v1 | `AAHFBSK9` | [PDF](https://arxiv.org/pdf/2606.13298v1) | 16 | 414131 | `9f883d4c236362e8f7ed951dd9741be31e4bd756b744087cd43a2e2360d0d6d7` |
| S13 / author-preprint | `ICP4IGIF` | [PDF](https://www.koziolek.de/docs/Koziolek2011-QoSA-preprint2.pdf) | 10 | 274064 | `eb16cdc4013f600b3a599b392963f633604e13c79b197deb3f5da5b7e81fef68` |
| S14 / author-preprint | `KFYU6XVJ` | [PDF](https://www.koziolek.de/docs/Koziolek2013-IEEE-SW-preprint.pdf) | 11 | 384134 | `1551ddbfc92387a9f9aa229f03abb2f8954c9fa1b50b3a0c3c48deebdd129df4` |
| S15 / open-indexed-copy | `4LVZLJAD` | [PDF](https://pdfs.semanticscholar.org/289d/041ad3e4058bbc09918b691ec725ab10c21d.pdf) | 10 | 149380 | `9d4907759bf78c9b2d14068a9f62ad8cbb8e607141b31810db8047618050b28f` |
| S16 / publisher | `QXR3P45X` | [PDF](https://ojs.aaai.org/aimagazine/index.php/aimagazine/article/view/2460/2438) | 13 | 271099 | `5fceb00e1c07a39c867c1d87662809aedecfe33ee92f0ce8440cc552e032f0b4` |
| S17 / arxiv-v2 | `ZNT9P6I3` | [PDF](https://arxiv.org/pdf/2512.22418v2) | 23 | 1221334 | `4c4c4f74e19ccafc738b448b1b2cafa09a6cf844d931cdeb533b39968806dd8b` |
| S18 / journal-arxiv-v1 | `S7GV7XAC` | [PDF](https://arxiv.org/pdf/2302.10003v1) | 59 | 786339 | `6ceb8c14e573b59c646e28b8dec1fbb4419127508b4b2778623265848f50404b` |

S01 uses the accepted arXiv v3 preprint, not an asserted identical publisher file. S05 now has the published 20-page article and the 26-page v2 preprint: the publisher lists eight authors, including Noman Ahmad, while v2 lists seven. Its publisher imprint gives online availability 2025-09-17 and the January 2026 issue. The Trepo response wrapped the PDF in one multipart file part; only that part was extracted, without rewriting the PDF.

S06 was published online 2022-04-18 and appears in the April 2023 issue. S10 is v3, S11 v6 and S17 v2 according to the checked DataCite histories. S11 carries related DOI `10.1145/3832196` and an October 2026 imprint; its August 2026 arXiv version is available, but that future issue date is not elapsed as of this checkpoint. S17 retains a placeholder ACM DOI/template date, so its record uses the verified arXiv identity. S13/S14 are author preprints; S15 is an openly indexed PDF copy; S16 is the original publisher PDF; S18 is the journal-linked arXiv PDF with the published imprint.

## PDFs still needed

| ID | Source and current access result | Next action |
| --- | --- | --- |
| S02 | [Architecture-pattern suggestions](https://doi.org/10.1007/978-3-031-66336-9_19): Springer PDF request returned a chapter HTML page, not a PDF; author/institution route also inaccessible. Scite reports non-OA. | User supplies the chapter PDF. |
| S04 | [MicroRec](https://doi.org/10.1145/3643991.3644916): ACM PDF request returned HTTP 403; official conference identity and complete Crossref authors were checked. No open copy found in the targeted routes. | User supplies the paper PDF. An HTTP 403 alone is not proof of a paywall. |
| S07 | [Product-development recommendations](https://doi.org/10.1017/pds.2025.10100): Cambridge identifies open access, but the PDF/registry routes returned HTTP 403 with a Cloudflare challenge; the public ResearchGate PDF route also returned 403. A further public-PDF request through Zotero's native downloader on 2026-09-16 HKT returned 403 too. | User may attach the OA PDF when accessible in their browser. It is not classified as closed access. |

No access purchase, author contact, authentication change or access-control bypass occurred. Other failed routes remain local acquisition records; failure of a particular route did not establish that its work was closed.

## Metadata, import verification and limits

One exact Scite lookup requested 20 records at offset 0 and returned all 20 requested identities: the eighteen works plus the S01/S05 preprint lineages. This was metadata/access checking, not a new discovery sweep, method reconstruction or novelty audit. No new citation-decision report was submitted for these unchanged reading priorities. Crossref supplied eleven published-work records and DataCite supplied seven primary preprint records; supplementary histories identified the S01/S05/S18 editions. Two initial Crossref HTTP 429 responses succeeded on later individual requests.

Library-wide DOI, normalized-title and known alternate-DOI checks found no existing S01–S18 parents before import; the JavaScript rechecked identities inside a Zotero transaction. It created eighteen parent records, copied the sixteen verified local PDFs through Zotero's native attachment API, checked attachment hashes before reuse, and wrote a completion receipt. The batch ran from 16:20:19 to 16:21:04 UTC on 2026-09-15 (00:20–00:21 HKT on 2026-09-16).

Independent readback verified all eighteen parent keys, collection membership, exact titles, DOI identities, full author lists, types, dates, Extra fields and queue tags. All sixteen stored PDFs matched their expected SHA-256 and byte size, parent, edition label and source URL. A second library-wide identity check found exactly one parent per queued work. The original sixteen parents' API records and nineteen stored-PDF hashes matched their earlier records. The final collection has 34 parent works and 35 PDFs; S05 has two labelled editions, while S02/S04/S07 have none. These three records carry the `ALF PDF needed` tag.

Local staging is outside Git in the task-specific `alf-selection-collection-20260915` temporary directory. It contains the manifest, source PDFs, acquisition records, first-page renders, completed import receipt and independent verification record. Durable parent/attachment keys and hashes are recorded above. No copyrighted PDF bodies or extraction dumps are committed.

## Research criteria remain at their existing evidence level

| Criterion | Disposition at this acquisition checkpoint |
| --- | --- |
| Unique (Scite) | Unresolved. Exact identities/access routes do not reconstruct the closest papers or establish priority. |
| Valuable | Useful in principle as the adoption-choice question in the current proposal; realized benefit, analysis cost and simpler alternatives remain untested. |
| Scientifically valid | Proposed information boundaries and comparisons are coherent; case equivalence, measurement, sampling and apparatus remain unvalidated. Acquisition does not complete the protocol. |

The [current review](selection-evidence-closure-2026-09-15.md) and [PLAN](../PLAN.md) retain the scientific authority. No new full read, human review, A0/A1 construction, candidate execution or experiment allocation occurred.

Local validation passed: all eleven existing CI-routing tests, JavaScript syntax checking, the import receipt/API/stored-file checks above, PDF byte/page-structure checks, and the four changed documents' UTF-8, local-link, table and whitespace checks. This documentation update does not revalidate runtime behavior or the scientific method. Publication CI is reported with its exact head, actual documentation scope and runtime-job skips.
