#!/usr/bin/env bash
set -euo pipefail
probe_base=/tmp/alf-e3a-native-build-zavnIH
probe_output=$(mktemp -d "$probe_base/probe-single-response-XXXXXX")
for probe_mode in baseline tool-call; do
  docker run --rm --name "alf-e3a-single-response-$probe_mode" --network none \
    --read-only --tmpfs /tmp:rw,size=256m,nosuid,nodev \
    --user "$(id -u):$(id -g)" --cpus 2 --memory 6g --memory-swap 6g \
    --pids-limit 512 --cap-drop ALL --security-opt no-new-privileges \
    --mount "type=bind,source=$probe_base/codex-native-single-response,target=/native-codex,readonly" \
    --mount "type=bind,source=$probe_base/e3a_codex_check-resumed.py,target=/checker.py,readonly" \
    --mount "type=bind,source=$probe_output,target=/output" \
    --entrypoint python3 \
    sha256:5d3e97d195dbbe7e47e47055e46f8c6f15fb9553be0c7ef19ed0060756fc7116 \
    /checker.py --codex /native-codex --expect-no-tools \
    --config features.no_tools=true --config features.single_response=true \
    --config features.code_mode_host=false --fixture "$probe_mode" \
    --output "/output/$probe_mode.json"
done
printf 'PROBE_OUTPUT=%s\n' "$probe_output"
