#!/usr/bin/env python3
"""Model-free predecessor payload and sandbox-preflight check."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path, help="absolute repository root")
    args = parser.parse_args()
    root = args.root.resolve()
    sys.path.insert(0, str(root / "src"))
    from alf.config import load_manifest
    from alf.e3a_codex import CodexOAuthAdapter
    from alf.e3a_sandbox import DockerEvaluator
    from alf.protocol import canonical_json_hash
    from alf.workstream_e3a import (candidate_payload, development_cases,
                                    read_json, snapshot)
    packet = root / "protocols/workstream-e3a-v1"
    spec = read_json(packet / "specification.json")
    manifest = load_manifest(root, spec["manifest"])
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, text=True,
                            capture_output=True, check=True).stdout.strip()
    result = {"git_head": commit, "specification_sha256": canonical_json_hash(spec),
              "manifest": spec["manifest"], "languages": {}, "passed": True}
    cap = spec["authority"]["max_replay_bytes"]
    selected = []
    for task_id in spec["tasks"]:
        stage = next(i for i, task in enumerate(manifest["tasks"]) if task["id"] == task_id)
        for language in spec["languages"]:
            payload = candidate_payload(root, manifest, language, task_id)
            replay_bytes = CodexOAuthAdapter.replay_size(payload)
            selected.append((language, task_id, stage, replay_bytes))
    if len(selected) != 6 or len({(language, task_id) for language, task_id, _, _ in selected}) != 6:
        raise ValueError("expected six distinct predecessor checks")
    for language in spec["languages"]:
        rows = result["languages"][language] = []
        evaluator = DockerEvaluator(root, manifest, spec, language)
        try:
            preparation = evaluator.prepare()
            print(json.dumps({"language": language, "event": "preparation", "preparation": preparation}), flush=True)
            for selected_language, task, stage, replay_bytes in selected:
                if selected_language != language:
                    continue
                source = snapshot(root, manifest, language, stage)
                evaluation = evaluator.evaluate(source, development_cases(manifest, stage), time.monotonic() + 120)
                record = {"language": language, "event": "evaluation", "task_id": task, "stage": stage, "replay_bytes": replay_bytes,
                             "replay_within_cap": replay_bytes <= cap,
                             "evaluation": evaluation}
                rows.append(record)
                print(json.dumps(record), flush=True)
                result["passed"] &= replay_bytes <= cap and evaluation.get("passed") is True
        finally:
            evaluator.close()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
