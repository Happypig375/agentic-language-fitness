# S02 — architecture-pattern suggestions from requirements

**Full chapter read and bounded artifact reconstruction, 2026-09-16 HKT.** Reader: main Codex AI session. [Living queue](../selection-priority-reading-2026-09-15.md) owns priority; [PLAN](../../../PLAN.md) owns authority. This is neither training reproduction nor human review.

## Identity and coverage

Gustrowsky, López Villarreal and Alférez, **Using Generative Artificial Intelligence for Suggesting Software Architecture Patterns from Requirements**, 2024, DOI [10.1007/978-3-031-66336-9_19](https://doi.org/10.1007/978-3-031-66336-9_19). The user-supplied attachment is the complete 675-page IntelliSys proceedings volume. The target chapter occupies **PDF pages 285–294, printed pages 274–283**. Only that chapter is certified fully read; the other 665 pages are not.

| Asset | Verified identity |
| --- | --- |
| Zotero collection / parent / attachment | `PKLXQNEE` / `ILICHNU6` / `MZKQ7PD7` |
| Stored PDF | 73,334,144 bytes; 675 pages |
| SHA-256 | `916bbd72a82e215109f35b6caacc44258b001e01c0672945815e165f46ee99ff` |
| Text coverage | All ten target pages, including all 14 references |
| Visual checks | Title/DOI on p. 285; all four figures on pp. 287, 289, 291, 292; no numbered chapter tables or appendix |

The original volume remains attached intact. Extraction and renders stay outside Git. Scite exact identity was checked; its response omitted the editorial-notices field, so this record does not certify absence of notices.

## What was tested

The decision object is a **pattern name and explanation**, among MVC, microservices and client–server, given a textual requirement. Title, description, precondition, postcondition and sequence are supplied; the pattern field is left for completion. There are no competing source implementations, implemented changes or measured maintenance trajectories.

PDF pp. 288–290 describe a ChatGPT-generated, manually labeled dataset of 32 requirements and fine-tuning Llama 2 7B using 4-bit QLoRA/SFTTrainer on two RTX A4000 GPUs. Reported settings include five epochs, learning rate 0.0005 and LoRA rank/alpha 64. Inference uses temperature 0.85, top-k 0, 190 new tokens and repetition penalty 1.13. Generation settings are discussed alongside output improvement; a separate development boundary for that tuning is not specified sufficiently for reconstruction.

PDF pp. 290–292 describe ten test requirements, reportedly outside training, assessed manually by expected-pattern agreement and explanation fluency. The paper gives three MVC, three microservices and four client–server cases, with 70% successful identification. It reports no unmodified-model control, independent label adjudication, repeated-run uncertainty or downstream implementation comparison. Fluency and a chosen pattern label cannot establish that alternative architectures are unsuitable.

## What the released artifact does and does not resolve

Inspected [author repository](https://github.com/JoelLV/Software_Architecture_Gen/tree/97a0ee66b8e6e9acccd72304ec9bc0ec0d2a21e7), pinned at `97a0ee66b8e6e9acccd72304ec9bc0ec0d2a21e7`: all ten `Results.md` examples; CSV/JSONL record structure and counts; converter, training loader and launch configuration. Source inspection is bounded and is not evidence that the current commit generated the published results.

| Check | Finding and limit |
| --- | --- |
| Expected-label distribution | Current `Results.md` has **3 MVC / 4 microservices / 3 client–server**, differing from the chapter's 3/3/4. |
| Ten-example arithmetic | Tests 1, 4, 5, 6, 7 and 8 give six unambiguous single-pattern matches. Test 2 returns client–server, microservices and event-driven together. Counting inclusion of the expected microservices label gives seven; requiring one matching recommendation gives six. The published adjudication rule does not resolve this ambiguity. This is a recount of the current artifact, not a corrected published accuracy estimate. |
| Input boundary | Test 3 already contains a service-oriented-architecture label and explanation, while its separate expected label is microservices. A frozen input manifest is needed to establish which content the reported test actually exposed. |
| Training file | 59 nonblank JSON-shaped records: 27 prefixed with `//` and 32 without that prefix. The inspected loader uses `load_dataset("text", ..., split="train")`; that loader does **not** discard comment-prefixed lines. The 32 unprefixed records therefore do not by themselves establish the claimed training membership. Prefixes were stripped only in the audit parser, without modifying source bytes. |
| Title overlap | Test 10 shares “Customer Support Ticketing System” with two file records. Its detailed requirements differ from the training entry, which is labeled client–server. Title overlap is a lead about independence, **not proof of identical test leakage**. Other test titles had no normalized exact match. |
| Configuration | `train_model.sh` specifies rank and alpha **100**, whereas the chapter reports 64. The dataset converter does not emit the comment prefixes present in the inspected file. No immutable model/run manifest reconciles these differences in the inspected material. |

Artifact fingerprints: `Results.md` SHA-256 `279efff84aaf178cf8a7730554234db79fbcd9cf7e4b7c47f91be353d72b129c`; JSONL `c9174fa4a2ff7f0e2a50077b271a9ad90f437b775f6075e46264759a2870aa93`; `train_code.py` `6cbdbfdae2af1824db26afdb45f61e72c2eea51fdf09a1ec1025502d90dc2bc3`; `train_model.sh` `0b7b13ba6276d4b25258690cdfa9c22c8f3cebd747462a8b185a860d7b3744d7`.

The chapter's conceptual method is reconstructable. Exact training membership, published-run configuration, test input and multi-label adjudication remain unresolved. No fine-tuning, model inference or retrospective rule adjustment was performed.

## Consequence for ALF and next reading

**Retain with a narrower source claim:** architecture recommendation is prior art, and this chapter evaluates named-pattern advice. **Do not** import its 70% headline as a maintenance effect or characterize it as experimentally refuted by a moving repository.

**Strengthen the specification:** retain all behaviorally valid implementations; freeze advice inputs and scoring units; predeclare abstention/multiple-choice handling; preserve development/evaluation membership and exact configurations. A plausible explanation is not measured decision value.

The Scite follow-up identifies newer architecture-document/view-generation studies. Their titles and the selected primary abstracts justify keeping them as conditional leads; they were not fully read or collectively ruled out. Existing **S05/S08** take priority for locating executable architecture evaluation. **S20/S23** are stronger immediate selection-comparator readings than another demonstration of plausible pattern prose. The [next-reading decision record](../selection-reading-next-2026-09-16.md) preserves those distinctions and the three unresolved criteria.
