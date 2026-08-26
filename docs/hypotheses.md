# Hypotheses

These hypotheses should be preregistered after the pilot fixes task difficulty and measurement reliability.

## H1 — Language effect

Programming language has a statistically detectable effect on complete agent trajectory cost after controlling for task, repository, model, harness, and run order.

## H2 — Raw brevity is insufficient

Final source-token count explains only part of total agent cost. Familiarity, reasoning, retrieval, compilation, tests, and retries account for additional variance.

## H3 — Repository-size interaction

Relative language effects increase as repositories grow because context retrieval and repeated reading become a larger share of lifetime cost.

## H4 — Maintenance crossover

A language may cost more on initial implementation yet cost less over repeated fresh-context maintenance. Rankings based on one-shot generation need not match lifetime rankings.

## H5 — Verification mediation

Stronger compiler/type-checker feedback reduces escaped defects but may increase visible repair iterations. Net cost depends on defect penalties and agent capability.

## H6 — Familiarity mediation

Low training exposure raises syntax/API errors and reasoning cost. Documentation retrieval, examples, and compiler feedback reduce—but may not eliminate—the disadvantage.

## H7 — Semantic compression

Removing deterministically recoverable redundancy can reduce context cost without harming correctness, whereas removing intent-bearing names or introducing unfamiliar shorthand increases semantic recovery cost.

## H8 — Capability interaction

More capable tool-using agents depend less on memorized language frequency and more on the language/toolchain's representational and verification properties.

## H9 — Shared-runtime control

The F#–C# difference is smaller and more interpretable than comparisons across unrelated ecosystems because runtime, libraries, build system, and deployment model are held substantially constant.

## H10 — Error compounding

Failures and awkward representations introduced early in a chain increase later maintenance cost even when later tasks are otherwise identical.
