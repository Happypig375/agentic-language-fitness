# CI validation scope

The user requested omitting irrelevant older checks or restructuring CI on
2026-09-14. This changes engineering validation scheduling, not scientific
protocols, frozen results or execution authority.

## Why restructure

The literature-only publication `5d9ad460738112a8dfe55f2de8eaad74bef35823`
passed [CI 34774846703](https://github.com/Happypig375/agentic-language-fitness/actions/runs/34774846703),
attempt 1: Linux took 14m37s and Windows 16m21s. Both repeated .NET construction,
historical workstream checks and, on Linux, sandbox/container checks despite
only AGENTS.md, PLAN.md and a research note changing.

The older checks are not all obsolete. H preparation, E3a and historical
C3/D/E2 artifacts share helpers and source inputs. Their existing full suite
is retained; clearly unrelated pushes do not need to run it.

## Routing

[ci_scope.py](../scripts/ci_scope.py) owns the explicit path rules;
[ci.yml](../.github/workflows/ci.yml) owns the jobs. No external path-filter
action, service, dependency graph engine or new package is required.

| Change/event | Selected validation |
| --- | --- |
| Ordinary known-range branch push changing only root README.md, AGENTS.md, PLAN.md, references.md or Markdown under docs/ | Fast routing regressions, changed-Markdown UTF-8 and Git whitespace checks; no ALF install, .NET or Docker. |
| Same kind of push confined to the maintenance allowlist, optionally plus the prose above | Fast checks, then all unit tests and the trusted maintenance fixture/fault/inherited-failure audit on Linux and Windows. |
| Shared implementation, CI/configuration, other benchmark/protocol/report inputs, or any unrecognized path | Fast checks plus the unchanged full Linux/Windows validation matrix. |
| Pull request, workflow_dispatch, tag, new-branch or forced push, malformed/missing event data, unavailable base/diff | Full matrix; uncertainty never chooses a skip. |

The maintenance allowlist contains its module, CLI and test file; construction
metadata and contract; guidance and episode Markdown; cases/faults JSON; seed
files; and reference/fault patches. Other new inputs remain full-suite changes
until their isolation is established. Protocol Markdown, benchmark task prompts
and H contracts are **not** ordinary prose for this policy. Even currently
non-executable subtree READMEs and protocol amendments conservatively use the
full route. File extensions alone do not determine scope.

Maintenance uses shared `h_fixtures`, `h0` and E2 tokenizer definitions. Changes
to those helpers select full CI. If another workstream starts consuming an
allowlisted path, update the rules and tests in that same implementation change.

The workflow always starts, rather than using workflow-level path exclusions.
Job conditions select the expensive work. This retains an exact-commit CI result;
a green prose-only run means the **selected fast checks** passed, not that the
runtime or old protocols were revalidated. GitHub distinguishes job skips from
workflow path-filter skips; the latter can leave required checks pending.
[Job conditions](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-jobs-with-conditions),
[workflow path filters](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#onpushpull_requestpull_request_targetpathspaths-ignore).

The scope step compares the entire push's before/after commits with a local
NUL-delimited Git diff. It does not use only HEAD's parent, a truncated webhook
file list or a paginated changed-files API. Rename detection is disabled so both
the old and new paths affect the decision. Deleted paths are classified too.
Detection errors fall back to full validation; failed fast checks keep the
existing validate-linux/validate-windows jobs red through their explicit guard.
An absent or unrecognized scope output also defaults to the full matrix.
No failed job is ignored or converted into a pass.

The fast prose checks do not validate links, Markdown rendering, scientific
claims or approval. Human review and the live-execution hold remain unchanged.

## Reproduction and full validation

```text
python -m unittest discover -s tests -p test_ci_scope.py -v
python scripts/ci_scope.py --base 49caefdf0b08029e2b5eeb81b958bfde3fdab331 --head 5d9ad460738112a8dfe55f2de8eaad74bef35823
```

The second command selects `docs` for the three-file literature publication.
It checks changed Markdown in the current checkout, so use a checkout matching
the selected head when reproducing content validation, not just classification.
Regression coverage includes the explicit input boundaries, ordinary versus
conservative events, unknown bases, more than one API page of changes,
multi-commit pushes, renames, deletions and malformed UTF-8.

Use the existing Actions **Run workflow** entry point for a full model-free
validation. Leave `run_e2` false unless the optional frozen E2 baseline is
specifically wanted and within the applicable authorization. Its existing
manual-only default, prerequisites, image, network isolation and audit commands
are unchanged. No OAuth staging or model/candidate dispatch is added by CI.

## Review and evidence

The dependency mapping was extracted read-only by a Luna Max worker. The main
agent owns the classifier, workflow integration and acceptance. A separate
Sol High AI review identified an empty/unknown-output fail-open case before
publication. The full-job predicates were corrected and workflow-contract
regression coverage added. The same reviewer rechecked the correction and found
no remaining material issue in that bounded scope. All 11 focused tests and
the three-file literature-commit replay passed locally; staged whitespace is
checked before publication. No local full-suite run is claimed. This
is not human scientific approval.
The source inspected before this change is `5d9ad460738112a8dfe55f2de8eaad74bef35823`.
Local routing tests and replay checks do not establish actual GitHub execution;
verify CI on the containing implementation commit after push. Because the CI
implementation itself changed, that publication selects the full matrix.

No historical validation command or archived experiment was deleted. Skipped
checks must be described as skipped, and actual CI scope must accompany later
validation claims. This policy adds no experimental allocation or treatment.
