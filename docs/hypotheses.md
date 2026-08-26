# Hypotheses

These should be preregistered before the main experiment wherever possible.

## H1 — Language effect

Programming language has a statistically significant effect on total agent trajectory cost after controlling for task and model.

## H2 — Raw brevity is insufficient

Final source-token count explains only part of total agent cost; retry, reasoning, compilation, and semantic-recovery costs remain substantial.

## H3 — Semantic compression beats opaque compression

Representations that remove reconstructible redundancy while preserving meaningful names and standard abstractions reduce agent cost more reliably than code-golf-style lexical compression.

## H4 — Verification tradeoff

Stronger static verification may reduce first-pass compile success but lowers defect escape and/or cumulative repair cost.

## H5 — Familiarity interaction

High training familiarity matters more for weaker models and one-shot tasks. Its relative importance falls when agents have strong compiler/test/documentation loops.

## H6 — Scale interaction

Languages with higher semantic density/locality gain relative advantage as repository size and required context increase.

## H7 — Maintenance interaction

A language can lose initial generation benchmarks while winning cumulative fresh-agent maintenance cost.

## H8 — F# / C# shared-platform hypothesis

Under matched .NET workloads, F# requires less repository context/semantic recovery than C#, but may incur additional syntax/idiom repair due to lower model familiarity.

The novel claim is not merely that either effect exists; it is whether the first dominates over a long maintenance horizon.

## H9 — Capability crossover

F#'s relative performance improves with agent capability and tool use because stronger agents rely less on memorized language-specific examples and can exploit compiler feedback more effectively.

## H10 — Descriptive-token value

Removing semantically informative natural-language identifiers harms task performance disproportionately to the tokens saved.
