#!/usr/bin/env bash
set -euo pipefail
cd /build/source-lf
git apply --check /build/e3a-single-response-repair-05.patch
git apply /build/e3a-single-response-repair-05.patch
cargo fmt --manifest-path codex-rs/Cargo.toml -- --config imports_granularity=Item
just fix -p codex-core -p codex-api -p codex-features --locked --profile dev-small \
    2>&1 | tee /build/single-response-lint-05.log
git diff --check
