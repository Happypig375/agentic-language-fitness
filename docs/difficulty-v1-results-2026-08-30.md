# difficulty-v1 results — 2026-08-30

## Cell and provenance

`difficulty-v1` is the non-counting Workstream C pilot over the matched
eight-task chain and the crossed F#/C# × descriptive/deterministic
representation treatment. It ran Williams row 1 exactly:
`[fsharp-descriptive, csharp-descriptive, csharp-deterministic,
fsharp-deterministic]`. One row is a calibration observation, not a
counterbalanced estimate.

The cell was frozen from clean Git commit
`edc6f3cacfba2aac428a4c60ae426b1cf8f2922d`. GitHub Actions run
`33269820641` is green for that commit on Linux and Windows. The resolved
manifest records:

- definition SHA-256
  `0241059175e1b822aabdb0cd577d4afb2fc0243b136442055ef275afb90687ce`;
- schedule SHA-256
  `276df97ee3ce0c1102e24e512aee9698d3a551d675b53bf5557748804bd4c561`;
- internal manifest SHA-256
  `c7754684dd999ac21a7a4bac5c0f6c71c4c03f363a0a10e5e81baac1b8c6ca3d`;
- resolved-manifest file SHA-256
  `fe34d218e7a62a6341d85d5f548e5aad5c041e99ad8c605b464c0ecd7ce37e51`;
- requested/provider-exposed model `gpt-5.4`, medium reasoning;
- image `alf-codex:0.149.1`, ID
  `sha256:0320a60c5b2628cebeb2c897bbf80da949f3b9bb99fa61f5a3475c7276328756`;
- verified image-archive SHA-256
  `55ee85f0656cef429d1cd40edced79782d54abb7b2180c9770c14bea06828ddf`.

The model identifier records the requested configuration but does not by
itself establish an immutable provider backend.

Raw data are retained outside Git at
`X:\backup20260827\Archives\SourceRepos\agentic-language-fitness-raw-runs\difficulty-v1`.
The read-only sibling checksum manifest is
`difficulty-v1.sha256-manifest.json`: 960 files, 27,269,126 bytes, tree
SHA-256
`7f6895b0322c7b04c37d5acd1bf00ebf7b96ca327ab885a43766840c8d0a76f3`,
and manifest-file SHA-256
`b564036d0aed88cbecc689f599a42e4998732921657896270563cb2ae1277f8a`.
Source and archive inventories match exactly. The archive scan found no
credential-bearing filenames, populated credential markers, or alternate
data streams.

## Attempt accounting

Six attempts are retained. Four are immutable primaries, one for each
scheduled position. Two pre-candidate/infrastructure failures were retried
sequentially under the frozen retry policy and remain excluded; they were not
silently replaced.

| Position | Attempt | Disposition | Tasks passed | Full audit | Metric inclusion |
| ---: | --- | --- | ---: | --- | --- |
| 1 | `pilot-01-fsharp-descriptive-01` | primary, chain complete | 8/8 | pass | success/time, usage, paired performance, representation |
| 2 | `pilot-01-csharp-descriptive-01` | infrastructure-invalid; protocol failure; retryable | 3/4 | expected fail | excluded |
| 2 | `pilot-01-csharp-descriptive-02` | primary; candidate failure at Task 007 | 6/7 | pass | success/time, usage, paired performance, representation |
| 3 | `pilot-01-csharp-deterministic-01` | primary, chain complete | 8/8 | pass | success/time, usage, paired performance, representation |
| 4 | `pilot-01-fsharp-deterministic-01` | infrastructure-invalid; protocol failure; retryable | 4/5 | expected fail | excluded |
| 4 | `pilot-01-fsharp-deterministic-02` | primary, chain complete | 8/8 | pass | success/time, usage, paired performance; representation excluded |

The first position-2 attempt reached the Task 004 authentication preflight,
whose subprocess timed out after 30 seconds despite emitting `Logged in using
ChatGPT`. It produced no candidate events or terminal usage record. The first
position-4 attempt reached Task 005, where the Windows host decoded captured
UTF-8 as CP1252, raised `UnicodeDecodeError`, and then failed before writing the
usage sidecar. Both failures are apparatus failures, not candidate outcomes.

The retained `result.json` SHA-256 values, in attempt order, are:

- `becf9f44cb9ffc95951cb626d412d57b115508b1b3e22d08825b7f0ecdcba026`
  (F# descriptive primary);
- `08e989c474ce50fea954b4c9d11a534e0884626e139f0b9f987c8f04c94605ec`
  (C# descriptive infrastructure-invalid attempt);
- `28f97d8a04a0ee0ce0a16a550fc524b67bcd449c2bd0df769b6639dd5b9bc322`
  (C# descriptive primary);
- `5c5811a051bc559b20f4843a559d09791ff48f01d36e6239bb9d7767466fade5`
  (C# deterministic primary);
- `67b59d9d9dc549a516212e3b144009066127a62587a741401e9a2abb4dcd6098`
  (F# deterministic infrastructure-invalid attempt);
- `57c0e09862908d11b13333f557df08e04e6d3e75b0b7847a96bd2429c86010b7`
  (F# deterministic primary).

## Primary observations

| Condition | Chain | Wall s | Agent s | Evaluator s | Input | Cached input | Output | Reasoning output |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| F# descriptive | 8/8 | 1,442.531 | 1,290.437 | 140.016 | 1,249,035 | 1,099,264 | 24,406 | 2,864 |
| C# descriptive | 6/7 | 626.188 | 579.704 | 40.734 | 701,288 | 646,656 | 16,596 | 1,109 |
| C# deterministic | 8/8 | 692.719 | 651.547 | 36.922 | 760,107 | 687,872 | 22,783 | 1,220 |
| F# deterministic | 8/8 | 1,453.078 | 1,294.640 | 147.436 | 1,063,190 | 980,480 | 23,146 | 1,964 |

Cached input is a component of input, not an additional token quantity. All
four primaries have valid aggregate accounting and usage.

Three of four primary chains completed all eight tasks. Across primaries,
30/31 executed task envelopes passed. The C# descriptive primary built and
passed its behavioral cases at Task 007, but failed the frozen structural
workspace checks for the required `public static class OrderFlowEngine` and
`OrderFlowEngine.Handle` entry point; the chain therefore stopped before Task
008. This retained candidate outcome supplies late, non-dominated task and
trajectory variation. It is one stochastic observation, not evidence that its
language or representation caused the failure.

## Representation integrity

The F# descriptive, C# descriptive, and C# deterministic primaries remained
interpretable under the technical representation scanner. The F# deterministic
primary remains valid for correctness, time, usage, and paired-performance
accounting, but is excluded from representation analysis.

That candidate reintroduced the descriptive alias `order` during Task 001.
The deterministic arm's opposite/reintroduced-alias counts then grew across
Tasks 001–008 as `3, 7, 28, 46, 50, 52, 78, 87`. The scanner itself remained
technically valid (`ok=true`); the frozen policy correctly treated this as
candidate-caused observational drift and marked the representation effect
non-interpretable without stopping the correctness chain.

## Interpretation and next action

The longer-chain difficulty gate is met: the strongest configuration is no
longer saturated, and the pilot produced a late acceptance failure without
impossible-task domination. Workstream C's benchmark recalibration can close
for chain difficulty and language-neutral equivalence.

The crossed representation comparison is not a clean causal estimate. It has
only one Williams row, condition is inseparable from position and stochastic
trajectory, and one primary lost treatment integrity. The observations support
no language advantage, representation advantage, significance claim, or
cross-cell pooling with the historical pair or variance-v2.

The Windows UTF-8 apparatus repair is committed at
`73001e1fce14b367c5e257113e328fcfddfc349e` and passed cross-platform GitHub
Actions run `33275928430` (Linux 4m05s, Windows 5m27s; Node 20 deprecation
annotations only). That apparatus gate is closed.

The next scientific milestone is Workstream D multi-configuration feasibility
design: choose at least three model/agent configurations, preregister
metric-specific outcomes and exclusions, derive repetitions from pilot
variance, and use complete counterbalanced blocks. Any formal representation
follow-up must also specify how treatment drift is prevented or analyzed.
Every future paid/model cell requires a new versioned definition, independent
review, a clean committed checkpoint, verified pinned artifacts, and a new
clean freeze.
