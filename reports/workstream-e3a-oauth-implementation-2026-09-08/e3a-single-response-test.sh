#!/usr/bin/env bash
set -euo pipefail
cd /build/source-lf
just test --cargo-profile dev-small -p codex-api -p codex-core -p codex-features \
    --test-threads 3 \
    -E 'test(client::tests::) | test(sse::responses::tests::) | test(no_tools_feature_fails_closed_in_session_without_followup) | test(single_response) | package(codex-features)' \
    2>&1 | tee /build/single-response-tests-01.log
cd codex-rs
cargo build --locked --profile dev-small -p codex-cli \
    2>&1 | tee /build/single-response-build-01.log
