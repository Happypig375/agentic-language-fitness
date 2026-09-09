"""Reproduce the bounded pre-execution evidence extracts; no experiment runs."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
SOURCES = {
    "native.json": ("results/h1-h2-remote-acceptance-02/native-final-01.json", None),
    "host-fixtures-attempt03.json": ("results/h1-h2-fixtures-final-03/report.json", "trusted_fixtures"),
    "sandbox-attempt01.json": ("results/h1-h2-remote-sandbox-01/sandbox-output/report.json", "trusted_fixtures"),
    "host-fault-repair.json": ("results/h1-h2-fault-repair-01.json", None),
    "remote-core-fsharp-fault-repair.json": (
        "results/h1-h2-remote-sandbox-01/fixed-core-fsharp-subtract-overdue.json", None),
    "fault-identity-comparison.json": (
        "results/h1-h2-remote-sandbox-01/fault-identity-comparison.json", None),
    "remote-expanded-fsharp-fault-repair.json": (
        "results/h1-h2-remote-sandbox-01/fixed-expanded-fsharp-subtract-overdue.json", None),
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


artifacts = []
for destination, (relative, key) in SOURCES.items():
    source = ROOT / relative
    raw = source.read_bytes()
    output = raw if key is None else canonical(json.loads(raw)[key])
    (HERE / destination).write_bytes(output)
    artifacts.append({"artifact": destination, "artifact_sha256": sha(output),
                      "source": relative, "source_sha256": sha(raw),
                      "operation": "unmodified-copy" if key is None else f"extract-json-key:{key}"})

index = {
    "scope": "model-free-preexecution-evidence-not-candidate-observations",
    "artifacts": artifacts,
    "evidence_summary": {
        "native": {"checks_passed": 52, "external_provider_requests": 0, "oauth_staged": False},
        "host_attempt03": {"positive_targets_passed": 8, "positive_targets_total": 8,
                           "semantic_faults_caught": 27, "semantic_faults_total": 28,
                           "current_identical_fault_variants": 26,
                           "changed_fault_variants_requiring_replay": 2,
                           "status": "failed-aggregate"},
        "sandbox_attempt01": {"positive_targets_passed": 8, "positive_targets_total": 8,
                              "semantic_faults_caught": 27, "semantic_faults_total": 28,
                              "current_identical_fault_variants": 26,
                              "changed_fault_variants_requiring_replay": 2,
                              "status": "failed-aggregate"},
        "host_fault_repair": {"scope": "core-fsharp-subtract-overdue-only", "caught": True,
                              "build_returncode": 0, "runtime_returncode": 0,
                              "status": "single-repair-pass-not-replacement-aggregate"},
        "remote_core_fault_repair": {"scope": "core-fsharp-subtract-overdue-only",
                                     "status": "separate-repair-evidence"},
        "remote_expanded_fault_repair": {"scope": "expanded-fsharp-subtract-overdue-only",
                                         "status": "separate-repair-evidence"},
        "fault_identity_comparison": {"total_variants": 28, "unchanged": 26,
                                      "changed": ["core-fsharp-subtract-overdue",
                                                  "expanded-fsharp-subtract-overdue"],
                                      "changed_variant_replays_passed": 2},
    },
    "reproduction": [
        ".venv/Scripts/python.exe reports/workstream-h1-h2-preexecution-2026-09-09/evidence/collect.py",
        ".venv/Scripts/python.exe -m unittest tests.test_h_fixtures -v",
        "python3 scripts/h_native_check.py --codex <pinned-native> --output <new-output>  # inside the hardened Linux native-probe container",
        ".venv/Scripts/python.exe scripts/h_check.py --output-dir <new-output-dir> --build-fixtures",
        "python3 scripts/h_check.py --permit-activation --sandbox --output-dir <new-output-dir>  # exact pinned image and SDK",
        ".venv/Scripts/python.exe scripts/h_check.py --permit-activation --sandbox --fixture-image-id <ci-sdk-fixture-image> --output-dir <new-output-dir>  # model-free CI fixture mode only",
    ],
    "limitations": ["No model, provider, OAuth, candidate, or scientific trajectory was run.",
                    "Failed aggregate attempts remain failed; 26 variants are identity-unchanged and two F# subtract-overdue variants require separate repair evidence.",
                    "Publication commit and exact CI are reported separately; both remote repaired cases are explicitly included."],
}
(HERE / "index.json").write_bytes(canonical(index))
