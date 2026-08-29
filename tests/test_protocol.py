import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from alf.protocol import (
    EXPECTED_IMAGE_ID,
    canonical_json_hash,
    classify_failure,
    freeze_cell,
    load_frozen_manifest,
    sha256,
    tracked_text_sha256,
    validate_cell,
    verify_image_archive,
    write_frozen_manifest,
)


ROOT = Path(__file__).parents[1]
DEFINITION = ROOT / "protocols" / "variance-v1" / "definition.json"
SCHEDULE = ROOT / "protocols" / "variance-v1" / "schedule.json"


def valid_probe() -> dict:
    return {
        "os": "Windows",
        "platform": "Windows-10-test",
        "architecture": "AMD64",
        "cpu": "test cpu",
        "physical_memory_bytes": 8_000_000_000,
        "python": "3.12.2",
        "git": "git version 2.46.2",
        "dotnet": "10.0.302",
        "docker_client": "27.2.0",
        "docker_server": "27.2.0",
        "image_id": EXPECTED_IMAGE_ID,
        "image_platform": "linux/amd64",
        "image_size_bytes": 630_000_000,
        "container_codex": "codex-cli 0.149.1",
        "container_dotnet": "10.0.302",
    }


def valid_archive_verification() -> dict:
    archive = json.loads(DEFINITION.read_text(encoding="utf-8"))["image_archive"]
    return {
        "path": archive["path"],
        "bytes": archive["bytes"],
        "sha256": archive["sha256"],
        "verified": True,
    }


class CellRepository:
    def __init__(self):
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name).resolve()
        self.definition_path = self.root / "protocols" / "variance-v1" / "definition.json"
        self.schedule_path = self.root / "protocols" / "variance-v1" / "schedule.json"
        self.benchmark_path = self.root / "benchmarks" / "pilot" / "manifest.json"

        self.definition_path.parent.mkdir(parents=True)
        self.benchmark_path.parent.mkdir(parents=True)
        shutil.copy2(ROOT / "Dockerfile.codex-agent", self.root / "Dockerfile.codex-agent")

        task_entries = []
        task_hashes = {}
        for task_id in ("001-priority", "002-overdue"):
            relative = Path("benchmarks") / "pilot" / "tasks" / task_id / "task.md"
            target = self.root / relative
            target.parent.mkdir(parents=True)
            shutil.copy2(ROOT / relative, target)
            task_entries.append({"id": task_id, "prompt": relative.as_posix()})
            task_hashes[task_id] = tracked_text_sha256(target)

        self.benchmark = {"schema_version": 1, "id": "test", "tasks": task_entries}
        self.schedule = json.loads(SCHEDULE.read_text(encoding="utf-8"))
        self.definition = json.loads(DEFINITION.read_text(encoding="utf-8"))
        self.definition["task_hashes"] = task_hashes
        self.flush()
        (self.root / ".gitignore").write_text("results/\n", encoding="utf-8")

    def flush(self) -> None:
        self.benchmark_path.write_text(
            json.dumps(self.benchmark, indent=2) + "\n", encoding="utf-8"
        )
        self.definition["benchmark_manifest_sha256"] = tracked_text_sha256(self.benchmark_path)
        self.schedule_path.write_text(
            json.dumps(self.schedule, indent=2) + "\n", encoding="utf-8"
        )
        self.definition_path.write_text(
            json.dumps(self.definition, indent=2) + "\n", encoding="utf-8"
        )

    def close(self) -> None:
        self.directory.cleanup()


class ProtocolTests(unittest.TestCase):
    def test_tracked_text_hash_normalizes_line_endings(self):
        with tempfile.TemporaryDirectory() as directory:
            lf = Path(directory) / "lf.txt"
            crlf = Path(directory) / "crlf.txt"
            changed = Path(directory) / "changed.txt"
            lf.write_bytes(b"one\ntwo\n")
            crlf.write_bytes(b"one\r\ntwo\r\n")
            changed.write_bytes(b"one\ntres\n")
            self.assertEqual(tracked_text_sha256(lf), tracked_text_sha256(crlf))
            self.assertNotEqual(tracked_text_sha256(lf), tracked_text_sha256(changed))

    def test_tracked_text_hash_normalizes_lone_cr(self):
        with tempfile.TemporaryDirectory() as directory:
            lf = Path(directory) / "lf.txt"
            cr = Path(directory) / "cr.txt"
            lf.write_bytes(b"one\ntwo\n")
            cr.write_bytes(b"one\rtwo\r")
            self.assertEqual(tracked_text_sha256(lf), tracked_text_sha256(cr))

    def test_invalid_utf8_is_reported_for_definition_and_prompt(self):
        repo = CellRepository()
        try:
            repo.definition_path.write_bytes(b"{\xff")
            report = validate_cell(repo.root, repo.definition_path)
        finally:
            repo.close()
            self.assertFalse(report["ok"])
        self.assertIn("invalid definition JSON", report["errors"][0])

        repo = CellRepository()
        try:
            prompt = repo.root / "benchmarks" / "pilot" / "tasks" / "001-priority" / "task.md"
            prompt.write_bytes(b"bad\xff")
            report = validate_cell(repo.root, repo.definition_path)
        finally:
            repo.close()
        self.assertFalse(report["ok"])
        self.assertTrue(any("invalid UTF-8 tracked text" in error for error in report["errors"]))
    def test_tracked_definition_and_generated_schedule_are_valid(self):
        report = validate_cell(ROOT, DEFINITION)
        self.assertTrue(report["ok"], report["errors"])
        first = [block["order"][0] for block in report["schedule"]["formal"]]
        self.assertEqual(
            first,
            ["csharp", "csharp", "fsharp", "csharp", "fsharp", "csharp", "fsharp", "fsharp", "csharp", "fsharp"],
        )

    def test_definition_path_outside_repository_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            outside = Path(directory) / "definition.json"
            outside.write_text("{}", encoding="utf-8")
            report = validate_cell(ROOT, outside)
        self.assertFalse(report["ok"])
        self.assertIn("escapes repository", report["errors"][0])

    def test_schema_hash_and_policy_tampering_fail_closed(self):
        repo = CellRepository()
        try:
            cases = (
                ("schema_version", 2, "schema_version"),
                ("benchmark_manifest_sha256", "0" * 64, "hash mismatch"),
                ("artifact_policy", {}, "artifact_policy"),
                ("image_archive", {"path": "x", "bytes": 1, "sha256": "bad", "local_image_id": "bad"}, "image_archive"),
            )
            for field, value, expected in cases:
                with self.subTest(field=field):
                    original = repo.definition[field]
                    repo.definition[field] = value
                    repo.definition_path.write_text(json.dumps(repo.definition), encoding="utf-8")
                    report = validate_cell(repo.root, repo.definition_path)
                    self.assertFalse(report["ok"])
                    self.assertTrue(any(expected in error for error in report["errors"]))
                    repo.definition[field] = original
                    repo.flush()
        finally:
            repo.close()

    def test_duplicate_tasks_and_schedule_tampering_fail_closed(self):
        repo = CellRepository()
        try:
            repo.benchmark["tasks"].append(dict(repo.benchmark["tasks"][0]))
            repo.flush()
            report = validate_cell(repo.root, repo.definition_path)
            self.assertFalse(report["ok"])
            self.assertTrue(any("unique" in error for error in report["errors"]))

            repo.benchmark["tasks"].pop()
            repo.schedule["formal"][2]["order"] = ["csharp", "fsharp"]
            repo.flush()
            report = validate_cell(repo.root, repo.definition_path)
            self.assertFalse(report["ok"])
            self.assertTrue(any("schedule" in error for error in report["errors"]))
        finally:
            repo.close()

    def test_referenced_path_traversal_and_root_raw_path_are_rejected(self):
        repo = CellRepository()
        try:
            repo.definition["schedule_file"] = "../escape.json"
            repo.definition["raw_root"] = "."
            repo.definition_path.write_text(json.dumps(repo.definition), encoding="utf-8")
            report = validate_cell(repo.root, repo.definition_path)
        finally:
            repo.close()
        self.assertFalse(report["ok"])
        self.assertTrue(any("escapes repository" in error for error in report["errors"]))
        self.assertTrue(any("repository root" in error for error in report["errors"]))

    def test_freeze_rejects_dirty_git_before_probe(self):
        repo = CellRepository()
        probe_called = False

        def probe(*_args):
            nonlocal probe_called
            probe_called = True
            return valid_probe()

        try:
            with patch("alf.protocol._git", return_value=" M changed"):
                with self.assertRaisesRegex(ValueError, "dirty"):
                    freeze_cell(repo.root, repo.definition_path, _probe=probe)
        finally:
            repo.close()
        self.assertFalse(probe_called)

    def test_freeze_rejects_unavailable_and_mismatched_probes(self):
        repo = CellRepository()
        try:
            unavailable = valid_probe()
            unavailable["cpu"] = "unavailable"
            with patch("alf.protocol._git", side_effect=["", "a" * 40]):
                with self.assertRaisesRegex(ValueError, "environment probe unavailable"):
                    freeze_cell(repo.root, repo.definition_path, _probe=lambda *_: unavailable)

            mismatch = valid_probe()
            mismatch["image_id"] = "sha256:" + "0" * 64
            with patch("alf.protocol._git", side_effect=["", "a" * 40]):
                with self.assertRaisesRegex(ValueError, "image ID mismatch"):
                    freeze_cell(repo.root, repo.definition_path, _probe=lambda *_: mismatch)
        finally:
            repo.close()

    def test_archive_verifier_checks_file_size_and_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "image.tar"
            archive.write_bytes(b"retained image")
            metadata = {
                "path": str(archive),
                "bytes": archive.stat().st_size,
                "sha256": sha256(archive),
            }
            report = verify_image_archive(metadata)
            self.assertTrue(report["verified"])
            metadata["bytes"] += 1
            with self.assertRaisesRegex(ValueError, "byte count"):
                verify_image_archive(metadata)

    def test_write_manifest_is_hashed_under_ignored_root_and_never_overwrites(self):
        repo = CellRepository()
        target = repo.root / "results" / "variance-v1" / "resolved-manifest.json"
        try:
            with patch("alf.protocol._git", side_effect=["", "", "a" * 40]):
                written = write_frozen_manifest(
                    repo.root,
                    repo.definition_path,
                    target,
                    _probe=lambda *_: valid_probe(),
                    _archive_verifier=lambda *_: valid_archive_verification(),
                )
            value = json.loads(written.read_text(encoding="utf-8"))
            claimed = value.pop("manifest_sha256")
            self.assertEqual(claimed, canonical_json_hash(value))
            self.assertEqual(value["image_id"], EXPECTED_IMAGE_ID)
            self.assertEqual(value["git_head"], "a" * 40)
            with patch("alf.protocol._git", return_value=""):
                with self.assertRaises(FileExistsError):
                    write_frozen_manifest(
                        repo.root,
                        repo.definition_path,
                        target,
                        _probe=lambda *_: valid_probe(),
                        _archive_verifier=lambda *_: valid_archive_verification(),
                    )
        finally:
            repo.close()

    def test_write_manifest_rejects_unignored_and_outside_targets(self):
        repo = CellRepository()
        try:
            with patch("alf.protocol._git", side_effect=ValueError("not ignored")):
                with self.assertRaisesRegex(ValueError, "not ignored"):
                    write_frozen_manifest(
                        repo.root,
                        repo.definition_path,
                        repo.root / "results" / "variance-v1" / "manifest.json",
                        _probe=lambda *_: valid_probe(),
                        _archive_verifier=lambda *_: valid_archive_verification(),
                    )
            with patch("alf.protocol._git", return_value=""):
                with self.assertRaisesRegex(ValueError, "raw_root"):
                    write_frozen_manifest(
                        repo.root,
                        repo.definition_path,
                        repo.root / "outside.json",
                        _probe=lambda *_: valid_probe(),
                        _archive_verifier=lambda *_: valid_archive_verification(),
                    )
        finally:
            repo.close()

    def test_load_manifest_rejects_self_hash_and_embedded_tampering(self):
        repo = CellRepository()
        target = repo.root / "results" / "variance-v1" / "resolved-manifest.json"
        try:
            with patch("alf.protocol._git", side_effect=["", "", "a" * 40]):
                write_frozen_manifest(
                    repo.root,
                    repo.definition_path,
                    target,
                    _probe=lambda *_: valid_probe(),
                    _archive_verifier=lambda *_: valid_archive_verification(),
                )
            original = json.loads(target.read_text(encoding="utf-8"))

            tampered = dict(original)
            tampered["image"] = "different:image"
            target.write_text(json.dumps(tampered), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "manifest hash mismatch"):
                load_frozen_manifest(repo.root, target)

            tampered = json.loads(json.dumps(original))
            tampered["definition"]["description"] = "tampered"
            unsigned = dict(tampered)
            unsigned.pop("manifest_sha256")
            tampered["manifest_sha256"] = canonical_json_hash(unsigned)
            target.write_text(json.dumps(tampered), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "embedded protocol"):
                load_frozen_manifest(repo.root, target)
        finally:
            repo.close()

    def test_load_manifest_requires_ignored_location_clean_matching_head(self):
        repo = CellRepository()
        target = repo.root / "results" / "variance-v1" / "resolved-manifest.json"
        try:
            with patch("alf.protocol._git", side_effect=["", "", "a" * 40]):
                write_frozen_manifest(
                    repo.root,
                    repo.definition_path,
                    target,
                    _probe=lambda *_: valid_probe(),
                    _archive_verifier=lambda *_: valid_archive_verification(),
                )
            with patch("alf.protocol._git", side_effect=["", "", "b" * 40]):
                with self.assertRaisesRegex(ValueError, "HEAD"):
                    load_frozen_manifest(repo.root, target)
            with patch("alf.protocol._git", side_effect=["", " M dirty"]):
                with self.assertRaisesRegex(ValueError, "dirty"):
                    load_frozen_manifest(repo.root, target)

            outside = repo.root / "outside-manifest.json"
            shutil.copy2(target, outside)
            with self.assertRaisesRegex(ValueError, "raw_root"):
                load_frozen_manifest(repo.root, outside)
        finally:
            repo.close()

    def test_failure_precedence_keeps_timeout_before_accounting(self):
        args = {
            "protocol_ok": True,
            "accounting_ok": False,
            "auth_ok": True,
            "provider_ok": True,
            "host_ok": True,
            "timed_out": True,
            "agent_ok": False,
            "evaluator_ok": True,
        }
        self.assertEqual(classify_failure(**args), "timeout")
        args.update(timed_out=False, accounting_ok=True, agent_ok=True)
        self.assertIsNone(classify_failure(**args))


if __name__ == "__main__":
    unittest.main()
