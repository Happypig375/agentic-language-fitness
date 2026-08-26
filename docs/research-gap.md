# Research gap and contribution claim

## Narrow claim

To the best of the scoped literature search completed on **2026-08-26**, no existing benchmark causally compares **semantically equivalent repositories implemented in different programming languages** while all of the following are held or measured:

- shared runtime and library ecosystem;
- identical natural-language maintenance requests;
- common black-box behavioral tests;
- inherited repository state across a chain of changes;
- fresh agent process/context for each change;
- complete token, tool, compilation, test, elapsed-time, context, and defect measurements.

The claim is not that no multilingual, longitudinal, context, or token-cost benchmark exists. Strong examples exist for each component separately. The gap is their controlled combination.

## Proposed contribution

1. **Paired repository methodology.** F# and C# implementations target the same .NET runtime and external protocol, reducing ecosystem and task confounds.
2. **Fresh-context maintenance chains.** Every change receives a new agent context while inheriting the prior code, operationalizing semantic recovery cost.
3. **Lifetime cost accounting.** The unit of analysis is the complete agent trajectory and accumulated maintenance cost, not final source length or one-shot Pass@1.
4. **Mechanism-oriented ablations.** Formatting, naming, type inference, idiomaticity, compiler feedback, and documentation access can be varied independently.
5. **Open, provider-neutral harness.** Adapters capture standardized artifacts without tying the benchmark to one model vendor.

## Falsification conditions

The gap or project rationale would weaken materially if prior work is found that already combines matched cross-language repositories, inherited maintenance, fresh contexts, and trajectory cost. The substantive hypothesis would be weakened if:

- language effects vanish after controlling for model familiarity and toolchain feedback;
- source/context footprint does not predict agent cost at repository scale;
- F# and C# differ mainly because the implementations are not behaviorally or architecturally comparable;
- results fail to replicate across model families and agent harnesses;
- small savings are dominated by stochastic variance or environment setup cost.

## What the pilot can and cannot establish

The two-task pilot establishes that the protocol is executable and that matched chained results can be collected. It cannot estimate a stable language effect, generalize to real repositories, or support a claim that F# is more agent-friendly. Those require larger matched systems, longer chains, repeated runs, randomization, and preregistered analysis.
