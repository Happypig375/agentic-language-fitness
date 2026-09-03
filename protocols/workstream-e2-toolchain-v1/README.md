# Workstream E2 toolchain baseline

This protocol measures source shape and ordinary .NET toolchain cost without a
coding agent or model request. It covers the clean baseline plus eight
cumulative gold stages for matched F# and C# projects: 18 canonical states in
all.

`definition.json` freezes:

- LF-normalized UTF-8 source identities and static source/project metrics;
- `tiktoken==0.14.0` with the `o200k_base` encoding as a documented token proxy;
- exact restore, Release build, and no-build evaluator command shapes;
- five deterministic paired rounds (90 schedule entries), with a balanced
  language-first order at every stage; and
- the `github-actions-ubuntu-24.04-dotnet10.0.302-offline-v1` environment
  profile.

The frozen definition SHA-256 is
`09d5669fd554e611b4df505454a40f06a0e9b2a23c4a16a28c9cc94d640067f7`.

## Verify the freeze

```text
python scripts/alf.py --manifest benchmarks/successor/manifest.json e2 check \
  --definition protocols/workstream-e2-toolchain-v1/definition.json
```

The checked definition is platform-independent; its source hashes normalize
line endings before hashing and tokenization. Checking requires the pinned
tokenizer and performs no build, network, or model activity.

## Execute the baseline

Use the manual `run_e2` input of `.github/workflows/ci.yml` at an exact reviewed
commit. The job first passes Linux and Windows validation, builds that commit's
container image, seeds one fixed NuGet package cache, and then runs the frozen
schedule in a network-disabled, read-only container. Each schedule entry gets a
fresh workspace (`restore`, `build`, `run`, evaluate) and an immediate repeat in
that same workspace (`build`, `run`, evaluate); the OS page cache is neither
cleared nor described as cold/warm.

Command streams and attempt metadata are retained only in the external Actions
artifact. The publishable JSON/Markdown report contains hashes, counts,
distributions, environment identity, and explicit missingness, but no source,
test-case, command-output, host-path, or credential text. A separate offline
audit reconciles that report against every raw evidence file before the result
can be accepted.

There is no adaptive extension or silent retry. Any state, evaluator,
environment, cache-identity, persistence, or evidence-audit failure rejects the
attempt.
