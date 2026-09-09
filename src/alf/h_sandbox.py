"""H-specific trusted-baseline adapter for the existing isolated evaluator."""
from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any, Mapping

from .config import Manifest
from .e3a_sandbox import DockerEvaluator


class HSandboxEvaluator:
    """Materialize only trusted predecessor source, then delegate unchanged."""

    def __init__(self, baseline: Mapping[str, str], language: str, spec: dict,
                 *, fixture_image_id: str | None = None):
        if language not in {"csharp", "fsharp"}:
            raise ValueError("unsupported H language")
        if fixture_image_id is not None and spec.get("execution_authorized") is True:
            raise ValueError("fixture image cannot be used by an activated H specification")
        self._temporary = tempfile.TemporaryDirectory(prefix="alf-h-baseline-")
        root = Path(self._temporary.name).resolve()
        base = root / "baseline"
        base.mkdir()
        suffixes = {".cs", ".fs", ".csproj", ".fsproj"}
        for name, text in baseline.items():
            if (Path(name).name != name or Path(name).suffix.casefold() not in suffixes
                    or not isinstance(text, str) or "\x00" in text or "\r" in text):
                self._temporary.cleanup()
                raise ValueError("unsafe trusted H baseline")
            (base / name).write_text(text, encoding="utf-8", newline="\n")
        project = "OrderFlow.csproj" if language == "csharp" else "OrderFlow.fsproj"
        source_file = "Program.cs" if language == "csharp" else "Program.fs"
        if project not in baseline or source_file not in baseline:
            self._temporary.cleanup()
            raise ValueError("trusted H baseline lacks project/program")
        manifest = Manifest({"schema_version": 1, "id": "h-private-baseline",
            "languages": {language: {"base": "baseline", "project_file": project,
                                      "source_file": source_file}},
            "baseline_cases": [], "tasks": []})
        manifest.manifest_parent = root
        try:
            self._inner = DockerEvaluator(root, manifest, spec, language,
                                          fixture_image_id=fixture_image_id)
        except BaseException:
            self._temporary.cleanup()
            raise

    def prepare(self) -> dict[str, Any]:
        return self._inner.prepare()

    def evaluate(self, source: dict[str, str], cases: list[dict], deadline: float) -> dict[str, Any]:
        return self._inner.evaluate(source, cases, deadline)

    def close(self) -> None:
        try:
            self._inner.close()
        finally:
            self._temporary.cleanup()

