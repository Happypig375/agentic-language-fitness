# Reading-pass verification and publication scope

**2026-09-15 HKT.** Starting source: `7259e8dc494de172da3721c890bebcf3d6a18d68`, branch `main`, upstream `origin/main`. A final fetch completed before publication. The unrelated untracked `uv.lock` was preserved. This is main-session self-review, not another AI reviewer or human approval.

Local verification passed:

- Thirteen reconstruction notes and sixteen distinct recorded PDFs; all sixteen local Zotero files matched their recorded byte counts and SHA-256 hashes. Zotero API readback confirmed thirteen collection parents and sixteen PDFs, including CodePlan's user-supplied publication.
- All committed JSON parsed, edition title/author/date fields were present, and the two original Python analysis files parsed. Recomputing both outputs matched the saved JSON exactly. The released CSV has no duplicate instance IDs within groups; fifty-ID hybrid comparisons preserve discordant outcomes and do not claim statistical equivalence.
- All 128 local Markdown links resolved in the final link check, including this validation note. UTF-8/replacement-character and Git whitespace checks passed.
- All eleven existing CI-routing regression tests passed: `python3 -m unittest discover -s tests -p test_ci_scope.py -v`. Their intentional malformed-event fixtures printed conservative full-scope messages; these are passing regression cases.
- The Scite decision/report check accepted all 41 provenance records, with no missing reasons or truncation; thirteen are full-read studies. Primary metadata/notice limits are recorded separately.

Reproduce the retained numerical checks with:

```text
python docs/literature/full-reading/published_arithmetic.py
python docs/literature/full-reading/artifact_csv_check.py /path/to/experiment_instance_costs_sweagent.csv
```

The CSV URL/commit/hash are in [artifact-csv-check.json](artifact-csv-check.json); do not substitute a moving release unnoticed. [Published arithmetic](published-arithmetic.json) uses rounded paper cells, not raw-trial estimates. The generated notes/JSON contain original analysis and metadata, not PDF bodies or private library paths.

Self-review reconciled the proposal, PLAN and AGENTS with the [synthesis](synthesis.md): restrictive package-policy inference, unselected inherited/reference controls, separate behavioral/proxy outcomes, conditional deferrals and A0-only human disposition. Source/code discrepancies remain explicit rather than repaired in third-party projects. No runtime/runner, protocol, frozen result, OAuth setting or allocation changed.

The analysis `.py` and `.json` files fall outside the repository's prose-only CI allowlist, so this publication requires the **full model-free Linux/Windows matrix** under the existing classifier. No local full-suite or candidate/model execution is claimed. The final handoff reports the actual exact pushed commit and completed CI result; a pending run is not a pass. The matrix checks repository fixtures and infrastructure, not paper reproducibility, Nu case validity or scientific approval.
