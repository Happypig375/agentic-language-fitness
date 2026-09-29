# Project identity: Interactive Software Evolution

The user requested renaming `agentic-language-fitness` everywhere except the current working directory. **Interactive Software Evolution (ISE)** is the internal codename. The starting point remains characterizing **Nu's claimed innovations** against prior work, with separate assessments of uniqueness, value and scientific validity. The name does not establish any result or authorize experiments. [PLAN](../PLAN.md) and the [background survey](literature/nu-background-survey-2026-09-30.md) retain the current scope.

## Current identities

| Surface | Current identity |
| --- | --- |
| GitHub repository and Python distribution | `interactive-software-evolution` |
| Python package, module launcher and installed command | `ise`, `python -m ise`, `ise` |
| Repository launcher | `python scripts/ise.py` |
| Current CI container tags | `interactive-software-evolution:ci` and `interactive-software-evolution:e2-<commit>` |
| Research collection | ISE / Nu innovation research; existing Zotero item and collection keys remain stable |
| Windows working directory | `C:\Users\hadri\source\repos\interactive-software-evolution`; the user subsequently moved the directory between sessions |

Both local editable installations were refreshed after the directory moved. The external `SourceRepos` archive folders now use `interactive-software-evolution-images` and `interactive-software-evolution-raw-runs`; old directory paths remain junctions so frozen archive pins resolve without altering stored bytes. The validator retains the original literal pin because it validates historical definitions.

Automatic approval review rejected deletion of obsolete generated package metadata with the reason `blocked by policy`. The metadata was instead preserved in the ignored rename backup directory, outside the import path; no files were deleted.

## Recorded evidence and compatibility

Past measurements, source fixtures, serialized schema identifiers, pinned image names/digests, transcripts and frozen protocol definitions retain their recorded identities. Replacing a string inside those records would change their hashes or their interpretation. Historical `ALF_*` adapter variables, `.alf` sidecars and `alf.*` record schemas are protocol interfaces rather than the current project branding. Their consumers remain compatible.

`alf`, `python -m alf`, `scripts/alf.py` and the legacy import namespace continue to resolve the existing tooling. Current instructions and CI use `ise`. The original `src/alf/representation.py` is kept byte-for-byte because the published C3 source manifest identifies both its path and its hash. `ise.representation` exposes that same module, preserving regeneration and audit behavior. This is a retained generator for historical evidence, not a second implementation.

The E3a review packet explicitly describes itself as a regenerable review record, not a frozen protocol. Its current source-path/hash map is refreshed for the package move. All other packet fields—including scientific specification, candidate payloads, budgets, schedule, prior review disposition and live authority—must remain identical. The original packet remains in Git history. No new execution approval is inferred from refreshed source identities.

Ordinary project documentation, current source references, GitHub links, package metadata and the active launchers use the new name. The user's untracked `uv.lock` receives only the distribution-name substitution and stays untracked. Dated raw reports, frozen protocol material and the archived plan preserve their original wording.

## Verification record

Local verification passed: **548 unit tests** in 296.882 seconds; eight current/legacy launcher checks across Python 3.12 and the Python 3.13 virtual environment; the byte-identical C3 generator; and all 446 protected-file comparisons except the explicitly regenerable E3a source map. Only `text_lf_sha256` changed in that packet; scientific and authority fields remained identical. Git whitespace validation passed. Both editable installations resolve the new directory, and the old distribution is absent from installed metadata.

Zotero readback confirms the new collection name, 90 parents and 98 PDFs. Existing bibliographic fields and memberships are preserved. The rename was committed and pushed as `74bd0d250434fef5a2d336abef16886ab2722cee`. [CI run 36617580114](https://github.com/Happypig375/interactive-software-evolution/actions/runs/36617580114) completed successfully: scope, full Windows validation and full Linux validation passed; the separate maintenance and optional E2 baseline jobs were skipped. This verifies the selected engineering checks, without authorizing experimental execution. The relocated portable image retains SHA-256 `55ee85f0656cef429d1cd40edced79782d54abb7b2180c9770c14bea06828ddf`.
