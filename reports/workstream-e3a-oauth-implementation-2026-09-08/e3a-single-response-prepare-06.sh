#!/usr/bin/env bash
set -euo pipefail
cd /build/source-lf/codex-rs
# Resumed cycle: the Option repair is already applied. No patch is reapplied.
cargo fmt -- --config imports_granularity=Item 2>&1 | tee /build/single-response-format-06.log
just fix -p codex-core -p codex-api -p codex-features --locked --profile dev-small \
    2>&1 | tee /build/single-response-lint-06.log
git diff --check
