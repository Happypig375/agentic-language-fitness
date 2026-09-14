# Core full-paper reading index

Completed the thirteen-paper reading and evidence-driven revision on 2026-09-15 HKT, starting at `7259e8dc494de172da3721c890bebcf3d6a18d68`. This is the coverage record for the core targets in [PLAN](../../../PLAN.md), not a record of experimental reproduction or human approval. Reader: the main Codex AI session. Read the [synthesis and next decision](synthesis.md) for human review. Missing methods/artifacts and the clipped P04 prompt tail remain explicit; they are not silently completed.

The Zotero collection is `PKLXQNEE` (ALF - Core Paper Reading Queue, 2026-09-15). [assets.json](assets.json) records actual attachment identities, PDF hashes, page counts and edition labels. Local file paths and copyrighted extracted text remain outside Git. Resolve an attachment via Zotero's local API or `zotero://select/library/items/<key>`.

The user supplied CodePlan's 2024 publication as attachment `LS9AUVZE`: 24 PDF pages, 1,202,157 bytes, SHA-256 `c31dec9440c699aaffb5597139e9ea8b13f8409e84f954723a881a58af671e08`. Its first page confirms DOI `10.1145/3643757`, July 2024, PACMSE 1/FSE article 31. The former publisher-PDF access gap is closed. Sixteen PDFs are present for thirteen works; editions are not independent studies.

`Full read` means every PDF page was consumed and all figures/tables/equations inspected where relevant. `Methods` additionally records necessary supplement inspection and remaining specification gaps. Extraction success never changes either status automatically.

| ID | Chosen edition / attachment | Full read | Methods | Last consumed / next action | Note |
| --- | --- | --- | --- | --- | --- |
| P01 | Conference author preprint / `ZKKCQBDZ` | Complete, PDF 1-13 | Reconstructed; checksum-verified supplement inspected, aggregate rerun not performed | All figures/tables; released prompt and CSV membership checked | [P01](P01-architectural-refactoring.md) |
| P02 | JSS 2004 / `45CCEA6L` | Complete, PDF 1-19 | Procedure reconstructed; confidential data and cost-model ambiguity retained | Figures 1-7, tables 1-5, equations 1-2 inspected | [P02](P02-alma.md) |
| P03 | arXiv v1 / `Z7ZAEPIJ` | Complete, PDF 1-14 | Procedure reconstructed; private data and filtering/budget details unavailable | Figures 1-2, tables 1-4, equation 1 inspected | [P03](P03-code-cleanliness.md) |
| P04 | arXiv v1 / `L7FG5XKP` | Complete, PDF 1-21; prompt-image tail clipped on p. 17 | Reconstructed; artifact/scaffold and denominator gaps retained | All appendices and image-based prompts inspected | [P04](P04-codethread.md) |
| P05 | arXiv v2 / `46LPN8N7` | Complete, PDF 1-26 | Reconstructed; publication-time evaluator/raw inclusion gaps retained | All appendices, figures/tables/equations and prompts inspected | [P05](P05-slopcodebench.md) |
| P06 | arXiv v1 / `8F2EA7B6`; v2 / `FMTJ9SHC` | v2 complete, PDF 1-19; v1 historical comparison pp. 4-9 | Reconstructed with artifact/denominator limits; v2 caption changes retained | All v2 appendices/prompts and v1 changed result captions inspected | [P06](P06-chainswe.md) |
| P07 | arXiv v1 / `UF73YJF4` | Complete, PDF 1-16 | Reconstructed; inventory and current structural-check discrepancies retained | All figures/tables/listings and case 001 artifact inspected | [P07](P07-needle-in-repo.md) |
| P08 | arXiv v2 / `VKL33569` | Complete, PDF 1-26 | Reconstructed; checksum-verified supplement inspected, runtime/accounting limits retained | All tables/figures, prompt, oracle and run script inspected | [P08](P08-type-error-ablation.md) |
| P09 | arXiv v3 / `R4Z4K5CW` | Complete, PDF 1-31 | Reconstructed; source, CSV membership and accounting limitations retained | All appendices, prompts and figures/tables/equations inspected | [P09](P09-complexity-trap.md) |
| P10 | arXiv v1 / `PF24JPY6` | Complete, PDF 1-19 | Reconstructed; judge, exposure and intervention/accounting gaps retained | All appendices, prompts, figures/tables; released scorer inspected | [P10](P10-slump.md) |
| P11 | arXiv v1 / `A696WU9C`; v2 / `WRJ2UKZ3` | v2 complete, PDF 1-17; v1 changed pp. 1, 15-16 compared | Reconstructed; artifact unavailable and judge/reporting gaps retained | All appendices, figures/tables; historical figure changes inspected | [P11](P11-gameenginebench.md) |
| P12 | arXiv v4 / `RXVC7BGE` | Complete, PDF 1-14 | Reconstructed; proxy, replay and paper/code differences retained | All appendices, figures/tables; prompts, scoring and passive controls inspected | [P12](P12-tocs.md) |
| P13 | PACMSE 2024 / `LS9AUVZE` | Complete, PDF 1-24 | Reconstructed; implementation/private-data and oracle limits retained | Figures 1-6, tables 1-6 and algorithm 1 inspected | [P13](P13-codeplan.md) |

Conditional readings retain their triggers in the [base handoff](../../full-paper-reading-handoff-2026-09-14.md) and [Nu addendum](../../nu-form-factors-and-research-leads-2026-09-14.md); all ten are explicitly deferred in the synthesis because their associated mechanisms/protocol claims are not adopted here. No additional experiment, construction or model allocation is authorized by this record.
