# Research-direction context checkpoint

**Date:** 2026-09-12 HKT

**Status:** accepted research direction; proposals below require amendment/review

## Purpose and scope

The current comparison is F# versus C# for architectural coherence, context
usefulness and large-project, long-term maintenance under bounded-context agent
maintenance. This is not a greenfield throwaway-generation question. The goal
is architectural durability as an agent maintains an existing repository.

F# feature composition and default consistency may lower maintenance burden;
modern C# records, patterns and other idioms are allowed. This is a hypothesis,
not an assumption that F# wins or a reason to award beauty points. Domain,
language and framework expertise are relevant knowledge assumptions and limits;
they must be stated honestly rather than silently treated as noise.

No new protocol version, acceptance count, scientific score, live allocation,
OAuth staging, model/count request, experimental execution, framework, proxy or
backend is adopted by this note. Existing H flags remain false and allocations
remain zero. The standalone H human-review packet and frozen artifacts remain
the authoritative pre-execution material for that workstream.

## Accepted direction

The durable target is architectural coherence and context usefulness during
long-term maintenance of large existing projects by bounded-context agents.
Modern, strong C# idioms belong in the comparison. Tiny H/orderflow tasks cannot
establish a large-project or long-term effect; independent repositories are
needed. Creation/training cost is outside scope unless explicitly measured.

## Assistant proposals requiring design review

- Keep the preceding repository and its history, while separating framework or
  tool faults from candidate defects. The primary H condition should not give
  compiler/test repair feedback; any repair condition should be separate. A
  fresh episode chat may carry durable code/docs without malformed-tool clutter.
- Compare supplied expert-reviewed idiomatic architecture for comprehension,
  decision quality and software-budget coverage with creating/maintaining
  inherited agent architecture under requirements, resources and support
  constraints; do not polish outcomes toward equality.
- Count necessary documentation, framework contracts and source. API/library
  abstractions are not free knowledge. Do not conflate code/output/context
  maxima: authored-byte proxies are not verified provider context limits.
- Fit is not decision quality. One-language-only fit contributes coverage, not
  an accuracy advantage, and identical input should not be redispatched solely
  for different offline budget labels.
- Preregister failure, rollback and continuation rules. Preserve every chain
  and failure; do not reward cheap early failure as efficiency. Outcomes should
  include correctness with prior invariants, regressions, missed dependencies,
  cumulative maintenance cost and survival, context usefulness, and explicit
  architecture drift.
- Treat semantic growth as interacting obligations. Growth APIs are not needed
  for the Task008 summary solution, but preservation obligations still matter;
  do not use padding or representation renaming as a size substitute.

These are design proposals, not user-adopted treatments or live permission.

## Read-only H finding

Current H does not reach the legacy E3a repair loop. The pinned base source is
b256f0eadd95ebd18e104dcae3bb1515712867d0. The path is [scripts/h_run.py](../scripts/h_run.py)
-> [src/alf/h_run.py](../src/alf/h_run.py) -> [src/alf/h.py](../src/alf/h.py)
-> dispatcher;
post-submit evaluation occurs and invalid actions terminate. H2 accepted reads
add turns but do not create diagnostic repairs. The main mismatch is a summary
Task008, not a deep architecture decision; growth APIs are unnecessary for
that summary, and selected caps have the same fit mask. A prior scout claim of
a legacy loop was retracted and must not be repeated.

## Evidence leads and limits

The Nu source lead is pinned public commit
064f7ae92a8506689cd91aff5e6804a375d6ef3d. [MyGame.fs](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Nu/Nu.Template.Mmcc.Game/MyGame.fs#L10)
lines 10-74 show a state union, Message transitions, Command world effects,
and declarative Definitions/Content. [WorldTypes.fs](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Nu/Nu/World/WorldTypes.fs#L1967)
lines 1967-1971 show a mutable World wrapper; [WorldModule2.fs](https://github.com/bryanedds/Nu/blob/064f7ae92a8506689cd91aff5e6804a375d6ef3d/Nu/Nu/World/WorldModule2.fs#L3150)
lines 3150-3156 pass World to both Message and Command. Thus effect
separation is a convention/signature support, not language-enforced purity.
Technical know-how and prior Ox/Xi lineage are confounds; public source links
are evidence leads, not controlled productivity results. The local reference
is ../Nu Chat Analysis (the user called it ../nu-chat-analysis); private source
transcripts remain private and are not a public evidence dependency.

Scite was accessed on 2026-09-12 with the term "programming languages" AND
"code quality",
limit 3, offset 0. It returned metadata/excerpts including Berger et al.,
*On the Impact of Programming Languages on Code Quality* ([DOI 10.1145/3340571](https://doi.org/10.1145/3340571)), its duplicate arXiv
preprint ([10.48550/arXiv.1901.10220](https://doi.org/10.48550/arXiv.1901.10220)),
and Kochhar et al. ([DOI 10.1109/SANER.2016.112](https://doi.org/10.1109/SANER.2016.112)). This was
only a capability probe, not full-text review or systematic search. Rediscover
access in a future session; seek contrary/null evidence, architecture and
maintenance work, comprehension/expertise, and longitudinal LLM evaluation.

## Open decisions and next action

Human/design review must decide the maintenance unit, repository sampling frame,
expertise treatment, architecture-review rubric, repair separation, context
measurement and survival horizon. It must also decide how to measure support and
framework burden without introducing a new framework or remote layer. Do not
infer these decisions from H results, citations or fit checks.

Next resumable action: conduct literature-backed maintenance/context design
alignment and draft a bounded design amendment for review. Adoption of changed
treatments, building replacements, or live execution requires a separate
decision. Preserve the current H checkpoint, source/specification identities
and all frozen artifacts.

## Summary for handoff

The accepted question concerns F#/C# architectural durability during bounded
agent maintenance of large existing projects. F# composition/defaults and
modern C# idioms are competing hypotheses; expertise and prior know-how matter.
The longitudinal design, metrics, repair split and sampling frame remain
assistant proposals requiring review. Current H is not an E3a repair loop, and
Scite/Nu materials are limited evidence leads. No code, protocol, execution,
allocation or provider claim changed. Continue bounded design investigation;
separate review governs any treatment adoption or execution.

**Changed locations:** AGENTS.md, PLAN.md, and this new file.
