# difficulty-v1 protocol (definition pending freeze)

This is the non-counting Workstream C difficulty pilot over the independently
approved eight-task C3 chain. It uses the completed strongest configuration,
`gpt-5.4` with medium reasoning, so difficulty is calibrated before any lower
capability follow-up. A future Luna cell would require its own preregistration.

The four conditions are F#/C# crossed with descriptive/deterministic C3
representations. The pilot uses Williams row 1 exactly:
`[fsharp-descriptive,csharp-descriptive,csharp-deterministic,fsharp-deterministic]`.
There is no randomization or seed. No formal blocks are scheduled; any future
formal cell must repeat complete four-row superblocks.

After review and a clean commit, freeze with:

```text
python scripts/alf.py protocol validate --definition protocols/difficulty-v1/definition.json
python scripts/alf.py protocol freeze --definition protocols/difficulty-v1/definition.json --output results/difficulty-v1/resolved-manifest.json
```

The four ordered pilot runs use `--order williams-01`, positions 1 through 4,
and condition-specific manifests selected by the harness. Every attempt and
raw JSONL/usage artifact is retained outside Git. Retry only infrastructure
invalid attempts; the first candidate outcome is the immutable primary.
Abort the affected trajectory on protocol, provenance, technical representation
scanner, evaluator, or accounting failure. A technical scanner failure is
infrastructure-invalid. Candidate-caused representation drift is observational:
continue the correctness chain unchanged, retain the immutable candidate
outcome, and mark the affected representation analysis non-interpretable. This
pilot is non-counting and cannot authorize a formal run without a later freeze.

The exact frozen run commands are:

```text
python scripts/alf.py --manifest benchmarks/successor/representation-v1/descriptive.manifest.json run --language fsharp --agent command --model gpt-5.4 --timeout 600 --require-usage --protocol-manifest results/difficulty-v1/resolved-manifest.json --block-id pilot-01 --order williams-01 --attempt-id pilot-01-fsharp-descriptive-01 --position 1 --output results/difficulty-v1
python scripts/alf.py --manifest benchmarks/successor/representation-v1/descriptive.manifest.json run --language csharp --agent command --model gpt-5.4 --timeout 600 --require-usage --protocol-manifest results/difficulty-v1/resolved-manifest.json --block-id pilot-01 --order williams-01 --attempt-id pilot-01-csharp-descriptive-01 --position 2 --output results/difficulty-v1
python scripts/alf.py --manifest benchmarks/successor/representation-v1/deterministic.manifest.json run --language csharp --agent command --model gpt-5.4 --timeout 600 --require-usage --protocol-manifest results/difficulty-v1/resolved-manifest.json --block-id pilot-01 --order williams-01 --attempt-id pilot-01-csharp-deterministic-01 --position 3 --output results/difficulty-v1
python scripts/alf.py --manifest benchmarks/successor/representation-v1/deterministic.manifest.json run --language fsharp --agent command --model gpt-5.4 --timeout 600 --require-usage --protocol-manifest results/difficulty-v1/resolved-manifest.json --block-id pilot-01 --order williams-01 --attempt-id pilot-01-fsharp-deterministic-01 --position 4 --output results/difficulty-v1
```
