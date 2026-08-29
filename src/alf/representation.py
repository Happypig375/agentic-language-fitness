from __future__ import annotations

import base64
import copy
import hashlib
import importlib.metadata
import json
import re
import shutil
import subprocess
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .benchmark_artifacts import artifact_plan
from .config import Manifest
from .metrics import snapshot_repository


SOURCE_COMMIT = "4e58677e0bfff18c2104298ad35fc4e801bbd052"
VERSION = "c3-representation-v1"
DOMAIN = "alf-c3-role-v1"
DEFAULT_OUTPUT = Path("benchmarks/successor/representation-v1")
SOURCE_MANIFEST = Path("benchmarks/successor/manifest.json")
TIKTOKEN_VERSION = "0.14.0"
TIKTOKEN_ENCODING = "o200k_base"

PREFIXES = {
    "local-variable": "loc_",
    "private-member": "mem_",
    "private-helper-type": "typ_",
    "private-helper-function": "fun_",
}

CSHARP_KEYWORDS = {
    "abstract", "as", "base", "bool", "break", "byte", "case", "catch",
    "char", "checked", "class", "const", "continue", "decimal", "default",
    "delegate", "do", "double", "else", "enum", "event", "explicit",
    "extern", "false", "finally", "fixed", "float", "for", "foreach",
    "goto", "if", "implicit", "in", "int", "interface", "internal", "is",
    "lock", "long", "namespace", "new", "null", "object", "operator", "out",
    "override", "params", "private", "protected", "public", "readonly", "ref",
    "return", "sbyte", "sealed", "short", "sizeof", "stackalloc", "static",
    "string", "struct", "switch", "this", "throw", "true", "try", "typeof",
    "uint", "ulong", "unchecked", "unsafe", "ushort", "using", "virtual",
    "void", "volatile", "while", "add", "alias", "and", "ascending", "async",
    "await", "by", "descending", "dynamic", "equals", "file", "from", "get",
    "global", "group", "init", "into", "join", "let", "managed", "nameof",
    "nint", "not", "notnull", "nuint", "on", "or", "orderby", "partial",
    "record", "remove", "required", "scoped", "select", "set", "unmanaged",
    "value", "var", "when", "where", "with", "yield",
}

FSHARP_KEYWORDS = {
    "abstract", "and", "as", "assert", "base", "begin", "class", "default",
    "delegate", "do", "done", "downcast", "downto", "elif", "else", "end",
    "exception", "extern", "false", "finally", "fixed", "for", "fun",
    "function", "global", "if", "in", "inherit", "inline", "interface",
    "internal", "lazy", "let", "match", "member", "module", "mutable",
    "namespace", "new", "not", "null", "of", "open", "or", "override",
    "private", "public", "rec", "return", "sig", "static", "struct", "then",
    "to", "true", "try", "type", "upcast", "use", "val", "void", "when",
    "while", "with", "yield",
}

PUBLIC_BY_LANGUAGE = {
    "csharp": {
        "Customer", "Order", "Request", "Response", "TransitionResponse",
        "SummaryResponse", "OrderFlow", "Program", "Main", "OrderFlowEngine",
        "Handle", "Options", "Id", "Tier", "CreatedAt", "Status", "Priority",
        "DueAt", "Operation", "Orders", "AsOf", "ToStatus", "Ids", "Pending",
        "Processing", "Completed", "Cancelled", "Overdue", "error",
    },
    "fsharp": {
        "Customer", "Order", "Request", "Response", "TransitionResponse",
        "SummaryResponse", "OrderFlow", "Program", "OrderFlowEngine", "handle",
        "options", "id", "tier", "createdAt", "status", "priority", "dueAt",
        "customer", "operation", "orders", "asOf", "toStatus", "ids", "pending",
        "processing", "completed", "cancelled", "overdue", "error",
    },
}
PUBLIC_IDENTIFIERS = set().union(*PUBLIC_BY_LANGUAGE.values())


class RepresentationError(RuntimeError):
    pass


@dataclass(frozen=True)
class Occurrence:
    token: str
    ordinal: int
    offset: int
    length: int


@dataclass(frozen=True)
class RoleSpec:
    role_id: str
    role_class: str
    csharp: str
    fsharp: str
    helper: bool = False
    first_task: str | None = None

    def source(self, language: str) -> str:
        return self.csharp if language == "csharp" else self.fsharp


ROLE_SPECS = (
    RoleSpec("local.input-line", "local-variable", "line", "input"),
    RoleSpec("local.request", "local-variable", "request", "request"),
    RoleSpec("local.response", "local-variable", "response", "response"),
    RoleSpec("local.exception", "local-variable", "ex", "ex"),
    RoleSpec("local.order-item", "local-variable", "order", "order"),
    RoleSpec("helper.is-status", "private-helper-function", "IsStatus", "isStatus", True, "007-query-engine-refactor"),
    RoleSpec("helper.is-active", "private-helper-function", "IsActive", "isActive", True, "007-query-engine-refactor"),
    RoleSpec("helper.normalize-orders", "private-helper-function", "NormalizeOrders", "normalizeOrders", True, "007-query-engine-refactor"),
    RoleSpec("helper.ready", "private-helper-function", "Ready", "ready", True, "007-query-engine-refactor"),
    RoleSpec("helper.overdue", "private-helper-function", "Overdue", "overdue", True, "007-query-engine-refactor"),
    RoleSpec("helper.at-risk", "private-helper-function", "AtRisk", "atRisk", True, "007-query-engine-refactor"),
    RoleSpec("helper.is-vip", "private-helper-function", "IsVip", "isVip", True, "007-query-engine-refactor"),
    RoleSpec("helper.canonical-target", "private-helper-function", "CanonicalTarget", "canonicalTarget", True, "007-query-engine-refactor"),
    RoleSpec("helper.transition", "private-helper-function", "Transition", "transition", True, "007-query-engine-refactor"),
    RoleSpec("helper.summarize", "private-helper-function", "Summarize", "summarize", True, "008-summary-api"),
)


@dataclass(frozen=True)
class Snapshot:
    language: str
    relative_path: str
    stage: str
    source_path: Path
    data: bytes

    @property
    def key(self) -> str:
        return f"{self.language}:{self.relative_path}"


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def _compact_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(_json_bytes(value))


def _repo_relative(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError as exc:
        raise RepresentationError(f"path escapes repository root: {path}") from exc


class _Scanner:
    def __init__(self, source: bytes, language: str) -> None:
        if language not in ("csharp", "fsharp"):
            raise RepresentationError(f"unsupported language: {language}")
        try:
            self.text = source.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise RepresentationError("source is not canonical UTF-8") from exc
        self.source = source
        self.language = language
        self.identifiers: list[tuple[str, int, int]] = []
        self.protected: list[tuple[int, int]] = []
        self.byte_offsets = [0]
        total = 0
        for char in self.text:
            total += len(char.encode("utf-8"))
            self.byte_offsets.append(total)

    def _error(self, message: str, index: int) -> RepresentationError:
        line = self.text.count("\n", 0, index) + 1
        return RepresentationError(f"{message} at line {line}")

    def _record_protected(self, start: int, end: int) -> None:
        if end > start:
            self.protected.append((start, end))

    def _line_is_directive(self, index: int) -> bool:
        line_start = self.text.rfind("\n", 0, index) + 1
        return not self.text[line_start:index].strip()

    def _comment_end(self, index: int, end: int, *, record: bool) -> int | None:
        if self.text.startswith("//", index):
            finish = self.text.find("\n", index + 2, end)
            finish = end if finish < 0 else finish
            if record:
                self._record_protected(index, finish)
            return finish
        opener = "/*" if self.language == "csharp" else "(*"
        closer = "*/" if self.language == "csharp" else "*)"
        if not self.text.startswith(opener, index):
            return None
        pos = index + 2
        depth = 1
        while pos < end:
            if self.language == "fsharp" and self.text.startswith(opener, pos):
                depth += 1
                pos += 2
                continue
            if self.text.startswith(closer, pos):
                depth -= 1
                pos += 2
                if depth == 0:
                    if record:
                        self._record_protected(index, pos)
                    return pos
                continue
            pos += 1
        raise self._error("unterminated block comment", index)

    def _ordinary_string_end(
        self,
        prefix_start: int,
        quote_index: int,
        end: int,
        *,
        verbatim: bool,
        quote: str = '"',
        record: bool,
    ) -> int:
        pos = quote_index + 1
        while pos < end:
            char = self.text[pos]
            if quote == '"' and verbatim and char == '"' and pos + 1 < end and self.text[pos + 1] == '"':
                pos += 2
                continue
            if char == quote:
                finish = pos + 1
                if record:
                    self._record_protected(prefix_start, finish)
                return finish
            if not verbatim and char == "\\":
                if pos + 1 >= end:
                    raise self._error("unterminated escape sequence", pos)
                pos += 2
                continue
            if not verbatim and char in "\r\n":
                raise self._error("unterminated string literal", prefix_start)
            pos += 1
        raise self._error("unterminated string literal", prefix_start)

    def _string_prefix(self, index: int, end: int) -> tuple[str, int, bool] | None:
        for prefix in ("$@\"", "@$\""):
            if self.text.startswith(prefix, index) and index + 3 <= end:
                return "interpolated", index + 2, True
        if self.text.startswith("$\"", index) and index + 2 <= end:
            return "interpolated", index + 1, False
        if self.text.startswith("@\"", index) and index + 2 <= end:
            return "ordinary", index + 1, True
        if index < end and self.text[index] == '"':
            return "ordinary", index, False
        return None

    def _find_interpolation_end(self, start: int, end: int) -> tuple[int, int]:
        stack: list[str] = []
        separator: int | None = None
        ternary_depth = 0
        pos = start
        pairs = {"(": ")", "[": "]", "{": "}"}
        while pos < end:
            comment_end = self._comment_end(pos, end, record=False)
            if comment_end is not None:
                pos = comment_end
                continue
            prefix = self._string_prefix(pos, end)
            if prefix is not None:
                kind, quote_index, verbatim = prefix
                if self.text.startswith('"""', quote_index):
                    raise self._error("raw strings are unsupported", pos)
                if kind == "interpolated":
                    pos = self._interpolated_end(pos, quote_index, end, verbatim=verbatim, record=False)
                else:
                    pos = self._ordinary_string_end(pos, quote_index, end, verbatim=verbatim, record=False)
                continue
            char = self.text[pos]
            if char == "'":
                pos = self._ordinary_string_end(pos, pos, end, verbatim=False, quote="'", record=False)
                continue
            if char in pairs:
                stack.append(pairs[char])
                pos += 1
                continue
            if char in ")]":
                if not stack or stack[-1] != char:
                    raise self._error("unbalanced interpolation delimiter", pos)
                stack.pop()
                pos += 1
                continue
            if char == "}":
                if stack:
                    if stack[-1] != "}":
                        raise self._error("unbalanced interpolation delimiter", pos)
                    stack.pop()
                    pos += 1
                    continue
                return pos, separator if separator is not None else pos
            if not stack and separator is None:
                if char == ",":
                    separator = pos
                elif char == ":":
                    if ternary_depth:
                        ternary_depth -= 1
                    else:
                        separator = pos
                elif char == "?":
                    following = self.text[pos + 1] if pos + 1 < end else ""
                    if following not in ("?", ".", "["):
                        ternary_depth += 1
            pos += 1
        raise self._error("unterminated interpolation expression", start - 1)

    def _interpolated_end(
        self,
        prefix_start: int,
        quote_index: int,
        end: int,
        *,
        verbatim: bool,
        record: bool,
    ) -> int:
        pos = quote_index + 1
        literal_start = prefix_start
        while pos < end:
            char = self.text[pos]
            if verbatim and char == '"' and pos + 1 < end and self.text[pos + 1] == '"':
                pos += 2
                continue
            if char == '"':
                finish = pos + 1
                if record:
                    self._record_protected(literal_start, finish)
                return finish
            if not verbatim and char == "\\":
                if pos + 1 >= end:
                    raise self._error("unterminated interpolated escape", pos)
                pos += 2
                continue
            if not verbatim and char in "\r\n":
                raise self._error("unterminated interpolated string", prefix_start)
            if char == "{" and pos + 1 < end and self.text[pos + 1] == "{":
                pos += 2
                continue
            if char == "}" and pos + 1 < end and self.text[pos + 1] == "}":
                pos += 2
                continue
            if char == "}":
                raise self._error("unescaped interpolation brace", pos)
            if char == "{":
                close, code_end = self._find_interpolation_end(pos + 1, end)
                if record:
                    self._record_protected(literal_start, pos + 1)
                    self._scan(pos + 1, code_end)
                    self._record_protected(code_end, close)
                literal_start = close
                pos = close + 1
                continue
            pos += 1
        raise self._error("unterminated interpolated string", prefix_start)

    def _scan(self, start: int, end: int) -> None:
        pos = start
        while pos < end:
            char = self.text[pos]
            if char.isspace():
                pos += 1
                continue
            if char == "#" and self._line_is_directive(pos):
                finish = self.text.find("\n", pos + 1, end)
                finish = end if finish < 0 else finish
                self._record_protected(pos, finish)
                pos = finish
                continue
            comment_end = self._comment_end(pos, end, record=True)
            if comment_end is not None:
                pos = comment_end
                continue
            if self.text.startswith('"""', pos) or self.text.startswith('$"""', pos):
                raise self._error("raw strings are unsupported", pos)
            prefix = self._string_prefix(pos, end)
            if prefix is not None:
                kind, quote_index, verbatim = prefix
                if kind == "interpolated":
                    pos = self._interpolated_end(pos, quote_index, end, verbatim=verbatim, record=True)
                else:
                    pos = self._ordinary_string_end(pos, quote_index, end, verbatim=verbatim, record=True)
                continue
            if char == "'":
                pos = self._ordinary_string_end(pos, pos, end, verbatim=False, quote="'", record=True)
                continue
            if char == "`":
                raise self._error("backtick identifiers are unsupported", pos)
            if ord(char) > 127 and (char.isalpha() or char.isdigit() or char == "_"):
                raise self._error("non-ASCII identifiers are unsupported", pos)
            if char == "@" and pos + 1 < end and (self.text[pos + 1].isalpha() or self.text[pos + 1] == "_"):
                token_start = pos + 1
                token_end = token_start + 1
                while token_end < end and (self.text[token_end].isascii() and (self.text[token_end].isalnum() or self.text[token_end] == "_")):
                    token_end += 1
                self.identifiers.append((self.text[token_start:token_end], token_start, token_end))
                pos = token_end
                continue
            if char.isascii() and (char.isalpha() or char == "_"):
                token_end = pos + 1
                while token_end < end:
                    current = self.text[token_end]
                    if not (current.isascii() and (current.isalnum() or current == "_")):
                        break
                    token_end += 1
                self.identifiers.append((self.text[pos:token_end], pos, token_end))
                pos = token_end
                continue
            pos += 1

    def run(self) -> tuple[list[Occurrence], list[bytes]]:
        self._scan(0, len(self.text))
        raw_rows: list[tuple[int, int, str]] = []
        for token, start, end in self.identifiers:
            raw_rows.append((self.byte_offsets[start], self.byte_offsets[end], token))
        raw_rows.sort(key=lambda row: (row[0], row[1], row[2]))
        seen: set[tuple[int, int, str]] = set()
        occurrences: list[Occurrence] = []
        previous_end = -1
        for offset, finish, token in raw_rows:
            key = (offset, finish, token)
            if key in seen:
                raise RepresentationError(f"duplicate identifier span at byte {offset}")
            seen.add(key)
            if offset < previous_end:
                raise RepresentationError(f"overlapping identifier span at byte {offset}")
            previous_end = finish
            occurrences.append(Occurrence(token, len(occurrences), offset, finish - offset))

        protected_spans = sorted(set(self.protected))
        previous_end = -1
        chunks: list[bytes] = []
        for start, end in protected_spans:
            byte_start, byte_end = self.byte_offsets[start], self.byte_offsets[end]
            if byte_start < previous_end:
                raise RepresentationError("overlapping protected lexical spans")
            previous_end = byte_end
            chunks.append(self.source[byte_start:byte_end])
        return occurrences, chunks


def _lex(source: bytes, language: str) -> tuple[list[Occurrence], list[bytes]]:
    return _Scanner(source, language).run()


def scan_identifiers(source: bytes, language: str) -> list[Occurrence]:
    return _lex(source, language)[0]


def _digest(role_class: str, role_id: str, used: set[str]) -> str:
    if role_class not in PREFIXES:
        raise RepresentationError(f"unknown role class: {role_class}")
    payload = DOMAIN.encode("utf-8") + b"\0" + role_class.encode("utf-8") + b"\0" + role_id.encode("utf-8")
    encoded = base64.b32encode(hashlib.sha256(payload).digest()).decode("ascii").lower().rstrip("=")
    prefix = PREFIXES[role_class]
    for length in range(10, len(encoded) + 1, 2):
        candidate = prefix + encoded[:length]
        if candidate not in used and candidate not in CSHARP_KEYWORDS and candidate not in FSHARP_KEYWORDS:
            return candidate
    raise RepresentationError(f"replacement digest exhausted for {role_id}")


def _git_blob(root: Path, relative: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{SOURCE_COMMIT}:{relative}"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise RepresentationError(f"source commit does not contain {relative}: {result.stderr.decode(errors='replace').strip()}")
    return result.stdout


def _require_pinned_file(root: Path, path: Path) -> bytes:
    relative = _repo_relative(root, path)
    if not path.is_file():
        raise RepresentationError(f"pinned source is missing: {relative}")
    committed = _git_blob(root, relative)
    result = subprocess.run(
        ["git", "diff", "--quiet", SOURCE_COMMIT, "--", relative],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise RepresentationError(f"source drift from {SOURCE_COMMIT}: {relative}")
    # Git blob bytes are the cross-platform canonical source. A checkout may
    # contain CRLF due to core.autocrlf without representing source drift.
    return committed


def _gold_entries(task: dict[str, Any], language: str, source_file: str) -> list[tuple[str, str]]:
    gold = task["gold"][language]
    if isinstance(gold, str):
        return [(gold, source_file)]
    return [(entry["source"], entry["target"]) for entry in gold["files"]]


def _load_snapshots(root: Path, manifest: dict[str, Any]) -> list[Snapshot]:
    snapshots: list[Snapshot] = []
    for language in sorted(manifest["languages"]):
        cfg = manifest["languages"][language]
        base = (root / cfg["base"]).resolve()
        expected_base = (root / "benchmarks" / "successor" / "repos" / language).resolve()
        try:
            base.relative_to(expected_base)
        except ValueError as exc:
            raise RepresentationError(f"unexpected baseline root for {language}: {base}") from exc
        for path in sorted(
            item for item in base.rglob("*")
            if item.is_file() and not ({".git", ".alf", "bin", "obj", "__pycache__"} & set(item.relative_to(base).parts))
        ):
            relative = f"baseline/{path.relative_to(base).as_posix()}"
            snapshots.append(Snapshot(language, relative, "baseline", path, _require_pinned_file(root, path)))
        for task in manifest["tasks"]:
            for source, target in _gold_entries(task, language, cfg["source_file"]):
                source_path = (root / source).resolve()
                expected_gold = (root / "benchmarks" / "successor" / "gold" / language / task["id"]).resolve()
                try:
                    source_path.relative_to(expected_gold)
                except ValueError as exc:
                    raise RepresentationError(f"unexpected gold source for {language}/{task['id']}: {source}") from exc
                target_path = Path(target)
                if target_path.is_absolute() or ".." in target_path.parts:
                    raise RepresentationError(f"unsafe gold target: {target}")
                relative = f"gold/{task['id']}/{target_path.as_posix()}"
                snapshots.append(Snapshot(language, relative, task["id"], source_path, _require_pinned_file(root, source_path)))
    keys = [snapshot.key for snapshot in snapshots]
    if len(keys) != len(set(keys)):
        raise RepresentationError("duplicate source snapshot key")
    return snapshots


def _line_and_column(data: bytes, offset: int) -> tuple[int, int]:
    prefix = data[:offset].decode("utf-8", errors="strict")
    return prefix.count("\n") + 1, len(prefix.rsplit("\n", 1)[-1]) + 1


def _helper_snapshot_allowed(spec: RoleSpec, snapshot: Snapshot) -> bool:
    if not spec.helper or not snapshot.relative_path.startswith("gold/"):
        return False
    parts = snapshot.relative_path.split("/")
    task_id = parts[1]
    filename = parts[-1]
    if task_id not in ("007-query-engine-refactor", "008-summary-api"):
        return False
    if spec.first_task == "008-summary-api" and task_id != "008-summary-api":
        return False
    expected = "OrderFlowEngine.cs" if snapshot.language == "csharp" else "OrderFlowEngine.fs"
    return filename == expected


def _overdue_occurrence_allowed(snapshot: Snapshot, occurrence: Occurrence) -> bool:
    text = snapshot.data.decode("utf-8")
    char_start = len(snapshot.data[:occurrence.offset].decode("utf-8"))
    char_end = char_start + len(occurrence.token)
    if snapshot.language == "csharp":
        suffix = text[char_end:]
        match = re.match(r"\s*(.)", suffix, flags=re.DOTALL)
        return bool(match and match.group(1) == "(")
    line_start = text.rfind("\n", 0, char_start) + 1
    line_end = text.find("\n", char_end)
    line_end = len(text) if line_end < 0 else line_end
    line = text[line_start:line_end].strip()
    if line.startswith("let private overdue"):
        return True
    if not line.startswith("overdue"):
        return False
    suffix = line[len("overdue"):].lstrip()
    return bool(suffix and suffix[0] not in "=:")


def _role_kind(spec: RoleSpec, snapshot: Snapshot, occurrence: Occurrence) -> str:
    text = snapshot.data.decode("utf-8")
    char_start = len(snapshot.data[:occurrence.offset].decode("utf-8"))
    line_start = text.rfind("\n", 0, char_start) + 1
    line_end = text.find("\n", char_start)
    line_end = len(text) if line_end < 0 else line_end
    before = text[line_start:char_start]
    after = text[char_start + len(occurrence.token):line_end]
    if spec.helper:
        if snapshot.language == "csharp":
            return "declaration" if "private static" in before else "reference"
        return "declaration" if re.search(r"\blet\s+private\s*$", before) else "reference"
    if snapshot.language == "csharp":
        if occurrence.token == "line" and re.search(r"\bstring\?\s*$", before):
            return "declaration"
        if occurrence.token == "ex" and re.search(r"\bException\s*$", before):
            return "declaration"
        if re.search(r"\b(?:var|Request|Response|Order|object|string)\??\s*$", before):
            return "declaration"
        if occurrence.token == "order" and re.match(r"\s*=>", after):
            return "declaration"
        return "reference"
    if occurrence.token == "input" and re.search(r"\|\s*$", before) and re.match(r"\s*->", after):
        return "declaration"
    if occurrence.token == "ex" and re.search(r"\bwith\s*$", before) and re.match(r"\s*->", after):
        return "declaration"
    if re.search(r"\b(?:let|fun)\s+$", before) or (re.search(r"\|\s*$", before) and re.match(r"\s*->", after)):
        return "declaration"
    if re.search(r"\($", before) and re.match(r"\s*:\s*[A-Za-z]", after):
        return "declaration"
    return "reference"


def _mapping_and_inventory(snapshots: list[Snapshot]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    scanned: dict[str, list[Occurrence]] = {}
    protected: dict[str, list[bytes]] = {}
    all_tokens: set[str] = set()
    for snapshot in snapshots:
        if snapshot.source_path.suffix.lower() not in (".cs", ".fs"):
            scanned[snapshot.key], protected[snapshot.key] = [], []
            continue
        rows, chunks = _lex(snapshot.data, snapshot.language)
        scanned[snapshot.key], protected[snapshot.key] = rows, chunks
        all_tokens.update(row.token for row in rows)

    used = set(all_tokens) | PUBLIC_IDENTIFIERS | CSHARP_KEYWORDS | FSHARP_KEYWORDS
    replacements: dict[str, str] = {}
    mapping_roles: list[dict[str, Any]] = []
    for spec in ROLE_SPECS:
        replacement = _digest(spec.role_class, spec.role_id, used)
        used.add(replacement)
        replacements[spec.role_id] = replacement
        mapping_roles.append({
            "role_id": spec.role_id,
            "role_class": spec.role_class,
            "source": {"csharp": spec.csharp, "fsharp": spec.fsharp},
            "replacement": replacement,
        })

    snapshot_rows: dict[str, Any] = {}
    for snapshot in snapshots:
        snapshot_rows[snapshot.key] = {
            "language": snapshot.language,
            "relative_path": snapshot.relative_path,
            "source_sha256": _sha256(snapshot.data),
            "identifier_count": len(scanned[snapshot.key]),
        }

    inventory_roles: list[dict[str, Any]] = []
    declaration_totals: dict[str, dict[str, int]] = {}
    for spec in ROLE_SPECS:
        by_snapshot: dict[str, list[dict[str, Any]]] = {}
        declaration_totals[spec.role_id] = {"csharp": 0, "fsharp": 0}
        for snapshot in snapshots:
            included: list[dict[str, Any]] = []
            eligible_scope = not spec.helper or _helper_snapshot_allowed(spec, snapshot)
            if eligible_scope:
                for occurrence in scanned[snapshot.key]:
                    if occurrence.token != spec.source(snapshot.language):
                        continue
                    if spec.role_id == "helper.overdue" and not _overdue_occurrence_allowed(snapshot, occurrence):
                        continue
                    kind = _role_kind(spec, snapshot, occurrence)
                    line, column = _line_and_column(snapshot.data, occurrence.offset)
                    row = {
                        "token": occurrence.token,
                        "ordinal": occurrence.ordinal,
                        "offset": occurrence.offset,
                        "length": occurrence.length,
                        "line": line,
                        "column": column,
                        "kind": kind,
                    }
                    included.append(row)
                    if kind == "declaration":
                        declaration_totals[spec.role_id][snapshot.language] += 1
            by_snapshot[snapshot.key] = included
        inventory_roles.append({
            "role_id": spec.role_id,
            "role_class": spec.role_class,
            "source": {"csharp": spec.csharp, "fsharp": spec.fsharp},
            "replacement": replacements[spec.role_id],
            "occurrences": by_snapshot,
        })

    missing_declarations = {
        role_id: counts for role_id, counts in declaration_totals.items()
        if any(counts[language] == 0 for language in ("csharp", "fsharp"))
    }
    if missing_declarations:
        raise RepresentationError(f"roles lack paired declarations: {missing_declarations}")

    exclusions_by_snapshot: dict[str, list[dict[str, str]]] = {}
    helper_specs = [spec for spec in ROLE_SPECS if spec.helper]
    for snapshot in snapshots:
        rows: list[dict[str, str]] = []
        for spec in helper_specs:
            if _helper_snapshot_allowed(spec, snapshot):
                continue
            if any(row.token == spec.source(snapshot.language) for row in scanned[snapshot.key]):
                rows.append({"identifier": spec.source(snapshot.language), "reason": "outside-private-engine-treatment-scope"})
        exclusions_by_snapshot[snapshot.key] = rows

    mapping = {
        "schema_version": 1,
        "algorithm_domain": DOMAIN,
        "roles": mapping_roles,
    }
    inventory = {
        "schema_version": 1,
        "source_commit": SOURCE_COMMIT,
        "snapshots": snapshot_rows,
        "roles": inventory_roles,
        "declarations_by_role_and_language": declaration_totals,
    }
    exclusions = {
        "schema_version": 1,
        "entries": [
            {"id": "public-dto-types", "names": ["Customer", "Order", "Request", "Response", "TransitionResponse", "SummaryResponse"]},
            {"id": "serializer-fields", "names": ["Id/id", "Tier/tier", "CreatedAt/createdAt", "Status/status", "Priority/priority", "DueAt/dueAt", "Customer/customer", "Operation/operation", "Orders/orders", "AsOf/asOf", "ToStatus/toStatus", "Ids/ids", "Pending/pending", "Processing/processing", "Completed/completed", "Cancelled/cancelled", "Overdue/overdue", "error/error"]},
            {"id": "entrypoints-and-files", "names": ["OrderFlow", "Program", "Main", "OrderFlowEngine", "Handle/handle", "Program.cs", "Program.fs", "OrderFlowEngine.cs", "OrderFlowEngine.fs", "OrderFlow.csproj", "OrderFlow.fsproj"]},
            {"id": "language-specific", "names": ["priorityOf", "query", "compareReady", "compareDuePriorityId", "running", "Options/options"]},
            {"id": "early-public-helpers", "names": [spec.csharp + "/" + spec.fsharp for spec in helper_specs]},
            {"id": "unmatched-private-identifiers", "names": ["ids", "selected", "matches", "target", "source", "expected", "actual"]},
        ],
        "public_identifiers": {language: sorted(names) for language, names in PUBLIC_BY_LANGUAGE.items()},
        "public_serializer_literals": ["error"],
        "per_snapshot": exclusions_by_snapshot,
    }
    return mapping, inventory, exclusions


def _edits_for_snapshot(inventory: dict[str, Any], snapshot: Snapshot) -> list[dict[str, Any]]:
    edits: list[dict[str, Any]] = []
    expected_sha = inventory["snapshots"][snapshot.key]["source_sha256"]
    if _sha256(snapshot.data) != expected_sha:
        raise RepresentationError(f"source hash drift for {snapshot.key}")
    ordinals = {row.ordinal: row for row in scan_identifiers(snapshot.data, snapshot.language)} if snapshot.source_path.suffix.lower() in (".cs", ".fs") else {}
    for role in inventory["roles"]:
        for occurrence in role["occurrences"][snapshot.key]:
            ordinal = occurrence["ordinal"]
            scanned = ordinals.get(ordinal)
            if scanned is None or scanned.token != occurrence["token"] or scanned.offset != occurrence["offset"] or scanned.length != occurrence["length"]:
                raise RepresentationError(f"inventory occurrence drift for {snapshot.key} ordinal {ordinal}")
            edits.append({
                **occurrence,
                "role_id": role["role_id"],
                "replacement": role["replacement"],
            })
    edits.sort(key=lambda row: (row["offset"], row["length"], row["role_id"]))
    previous_end = -1
    for edit in edits:
        if edit["offset"] < previous_end:
            raise RepresentationError(f"overlapping edits for {snapshot.key}")
        previous_end = edit["offset"] + edit["length"]
    return edits


def _apply_edits(source: bytes, edits: list[dict[str, Any]]) -> tuple[bytes, list[dict[str, Any]]]:
    chunks: list[bytes] = []
    applied: list[dict[str, Any]] = []
    source_pos = 0
    output_pos = 0
    for edit in edits:
        offset, length = edit["offset"], edit["length"]
        original = edit["token"].encode("utf-8")
        replacement = edit["replacement"].encode("ascii")
        if source[offset:offset + length] != original:
            raise RepresentationError(f"edit token mismatch at byte {offset}")
        unchanged = source[source_pos:offset]
        chunks.extend((unchanged, replacement))
        output_pos += len(unchanged)
        applied.append({
            **edit,
            "output_offset": output_pos,
            "output_length": len(replacement),
        })
        output_pos += len(replacement)
        source_pos = offset + length
    chunks.append(source[source_pos:])
    return b"".join(chunks), applied


def _reverse_edits(transformed: bytes, applied: list[dict[str, Any]]) -> bytes:
    chunks: list[bytes] = []
    pos = 0
    for edit in applied:
        offset, length = edit["output_offset"], edit["output_length"]
        replacement = edit["replacement"].encode("ascii")
        if transformed[offset:offset + length] != replacement:
            raise RepresentationError(f"replacement token mismatch at byte {offset}")
        chunks.extend((transformed[pos:offset], edit["token"].encode("utf-8")))
        pos = offset + length
    chunks.append(transformed[pos:])
    return b"".join(chunks)


def _hash_matched_transform(data: bytes, source: bytes, deterministic: bytes) -> bytes:
    digest = _sha256(data)
    if digest == _sha256(source):
        return deterministic
    if digest == _sha256(deterministic):
        return data
    raise RepresentationError("input is neither the pinned source nor its deterministic output")


def _public_sequence(data: bytes, language: str, excluded_offsets: set[int] | None = None) -> list[str]:
    excluded = excluded_offsets or set()
    return [
        row.token for row in scan_identifiers(data, language)
        if row.token in PUBLIC_BY_LANGUAGE[language] and row.offset not in excluded
    ]


def _manifest_contract(manifest: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(manifest)
    value.pop("id", None)
    value.pop("representation_provenance", None)
    for language, cfg in value["languages"].items():
        cfg["base"] = f"<base:{language}>"
    for task in value["tasks"]:
        for language, gold in task["gold"].items():
            if isinstance(gold, str):
                task["gold"][language] = f"<source:{Path(gold).name}>"
            else:
                for entry in gold["files"]:
                    entry["source"] = f"<source:{Path(entry['source']).name}>"
    return value


def _rewrite_manifest(original: dict[str, Any], treatment: str, artifact_name: str = "representation-v1") -> dict[str, Any]:
    manifest = copy.deepcopy(original)
    manifest["id"] = f"successor-order-flow-representation-{treatment}"
    manifest["representation_provenance"] = {
        "definition": "definition.json",
        "generator_version": VERSION,
        "source_commit": SOURCE_COMMIT,
        "treatment": treatment,
    }
    prefix = f"benchmarks/successor/{artifact_name}/transformed/{treatment}"
    for language, cfg in manifest["languages"].items():
        cfg["base"] = f"{prefix}/{language}/baseline"
    for task in manifest["tasks"]:
        for language, gold in task["gold"].items():
            stage_prefix = f"{prefix}/{language}/gold/{task['id']}"
            if isinstance(gold, str):
                task["gold"][language] = f"{stage_prefix}/{Path(gold).name}"
            else:
                for entry in gold["files"]:
                    entry["source"] = f"{stage_prefix}/{Path(entry['target']).as_posix()}"
    return manifest


def _stage_groups(snapshots: Iterable[Snapshot]) -> dict[str, dict[str, list[Snapshot]]]:
    groups: dict[str, dict[str, list[Snapshot]]] = {"csharp": {}, "fsharp": {}}
    for snapshot in snapshots:
        groups[snapshot.language].setdefault(snapshot.stage, []).append(snapshot)
    for language in groups:
        for stage in groups[language]:
            groups[language][stage].sort(key=lambda item: item.relative_path)
    return groups


def _token_metrics(directory: Path, files: list[Snapshot], treatment: str, encoding: Any) -> dict[str, Any]:
    repository = snapshot_repository(directory)
    canonical_files = []
    for snapshot in files:
        output = directory / Path(snapshot.relative_path).name
        canonical_files.append({"path": output.name, "utf8": output.read_text(encoding="utf-8")})
    canonical_input = _compact_json_bytes({"files": canonical_files})
    token_ids = encoding.encode(canonical_input.decode("utf-8"))
    token_stream = _compact_json_bytes(token_ids)
    return {
        **repository,
        "treatment": treatment,
        "canonical_input_sha256": _sha256(canonical_input),
        "tiktoken_count": len(token_ids),
        "tiktoken_ids_sha256": _sha256(token_stream),
    }


def _metrics_report(output: Path, snapshots: list[Snapshot]) -> dict[str, Any]:
    try:
        package_version = importlib.metadata.version("tiktoken")
    except importlib.metadata.PackageNotFoundError as exc:
        raise RepresentationError("tiktoken is required to build representation metrics") from exc
    if package_version != TIKTOKEN_VERSION:
        raise RepresentationError(f"tiktoken version must be {TIKTOKEN_VERSION}, found {package_version}")
    import tiktoken

    encoding = tiktoken.get_encoding(TIKTOKEN_ENCODING)
    groups = _stage_groups(snapshots)
    result: dict[str, Any] = {
        "proxy": {
            "package": "tiktoken",
            "version": package_version,
            "encoding": TIKTOKEN_ENCODING,
            "interpretation": "offline source proxy; not provider billing or Codex accounting",
            "canonical_input": "compact sorted JSON with path and UTF-8 text for each stage file",
        },
        "languages": {},
    }
    numeric = ("source_files", "source_bytes", "source_lines", "approx_lexical_tokens", "tiktoken_count")
    for language, stages in groups.items():
        language_rows: dict[str, Any] = {}
        for stage, files in stages.items():
            descriptive_dir = output / "transformed" / "descriptive" / language / ("baseline" if stage == "baseline" else f"gold/{stage}")
            deterministic_dir = output / "transformed" / "deterministic" / language / ("baseline" if stage == "baseline" else f"gold/{stage}")
            descriptive = _token_metrics(descriptive_dir, files, "descriptive", encoding)
            deterministic = _token_metrics(deterministic_dir, files, "deterministic", encoding)
            language_rows[stage] = {
                "descriptive": descriptive,
                "deterministic": deterministic,
                "signed_delta_deterministic_minus_descriptive": {name: deterministic[name] - descriptive[name] for name in numeric},
            }
        result["languages"][language] = language_rows
        _write_json(output / "reports" / language / "metrics.json", {
            "language": language,
            "proxy": result["proxy"],
            "snapshots": language_rows,
        })
    return result


def _coverage_report(
    inventory: dict[str, Any],
    transformed_counts: dict[str, dict[str, int]],
) -> tuple[dict[str, Any], int, int]:
    by_role: dict[str, Any] = {}
    total_eligible = 0
    total_transformed = 0
    snapshot_keys = sorted(inventory["snapshots"])
    for role in inventory["roles"]:
        role_rows: dict[str, Any] = {}
        for key in snapshot_keys:
            eligible = len(role["occurrences"][key])
            transformed = transformed_counts[role["role_id"]][key]
            total_eligible += eligible
            total_transformed += transformed
            if eligible == transformed == 0:
                coverage = None
                status = "absent"
            elif eligible == 0:
                coverage = None
                status = "unexpected"
            else:
                coverage = transformed / eligible
                status = "covered" if transformed == eligible else ("deficit" if transformed < eligible else "surplus")
            role_rows[key] = {
                "eligible": eligible,
                "transformed": transformed,
                "coverage": coverage,
                "status": status,
            }
        by_role[role["role_id"]] = role_rows
    return by_role, total_eligible, total_transformed


def _coverage_complete(coverage_by_role: dict[str, Any]) -> bool:
    return all(
        row["eligible"] == row["transformed"]
        for role_rows in coverage_by_role.values()
        for row in role_rows.values()
    )


def _input_provenance(root: Path, manifest_path: Path, manifest: dict[str, Any], snapshots: list[Snapshot]) -> dict[str, Any]:
    manifest_bytes = _require_pinned_file(root, manifest_path)
    prompt_hashes: dict[str, Any] = {}
    for task in manifest["tasks"]:
        prompt = (root / task["prompt"]).resolve()
        data = _require_pinned_file(root, prompt)
        prompt_hashes[task["id"]] = {"path": _repo_relative(root, prompt), "sha256": _sha256(data)}
    generator_path = Path(__file__).resolve()
    files: dict[str, dict[str, str]] = {"csharp": {}, "fsharp": {}}
    for snapshot in snapshots:
        files[snapshot.language][snapshot.relative_path] = _sha256(snapshot.data)
    return {
        "schema_version": 1,
        "source_commit": SOURCE_COMMIT,
        "original_manifest": {"path": _repo_relative(root, manifest_path), "sha256": _sha256(manifest_bytes)},
        "task_prompts": prompt_hashes,
        "generator_source": {"path": _repo_relative(root, generator_path), "sha256": _sha256(generator_path.read_bytes())},
        "files": files,
    }


def _artifact_hashes(output: Path) -> dict[str, Any]:
    files: dict[str, str] = {}
    for path in sorted(item for item in output.rglob("*") if item.is_file() and item.name != "artifact-hashes.json"):
        files[path.relative_to(output).as_posix()] = _sha256(path.read_bytes())
    return {"schema_version": 1, "algorithm": "sha256", "self_excluded": True, "files": files}


def _validate_generated_manifests(root: Path, output: Path, artifact_name: str) -> int:
    count = 0
    workspace = output / ".manifest-plan-workspace"
    workspace.mkdir()
    try:
        for name in ("descriptive.manifest.json", "deterministic.manifest.json"):
            manifest = Manifest(json.loads((output / name).read_text(encoding="utf-8")))
            manifest.manifest_parent = output.resolve()
            actual_prefix = _repo_relative(root, output)
            for task in manifest["tasks"]:
                for language, gold in task["gold"].items():
                    if isinstance(gold, str):
                        task["gold"][language] = gold.replace(
                            f"benchmarks/successor/{artifact_name}", actual_prefix, 1
                        )
                    else:
                        for entry in gold["files"]:
                            entry["source"] = entry["source"].replace(
                                f"benchmarks/successor/{artifact_name}", actual_prefix, 1
                            )
            for language in manifest["languages"]:
                for task in manifest["tasks"]:
                    artifact_plan(root, manifest, language, task, workspace)
                    count += 1
    finally:
        workspace.rmdir()
    return count


def _build_representation_into(root: Path, output: Path, artifact_name: str = "representation-v1") -> dict[str, Any]:
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    manifest_path = root / SOURCE_MANIFEST
    original = json.loads(_require_pinned_file(root, manifest_path).decode("utf-8"))
    snapshots = _load_snapshots(root, original)
    mapping, inventory, exclusions = _mapping_and_inventory(snapshots)
    _write_json(output / "mapping.json", mapping)
    _write_json(output / "role-inventory.json", inventory)
    _write_json(output / "exclusions.json", exclusions)

    exact_spans = True
    descriptive_identity = True
    reverse_identity = True
    protected_identity = True
    public_identity = True
    idempotent_noop = True
    observed_public_source = {"csharp": set(), "fsharp": set()}
    observed_public_deterministic = {"csharp": set(), "fsharp": set()}
    source_identifier_tokens: set[str] = set()
    generated_hashes: dict[str, dict[str, dict[str, str]]] = {
        "descriptive": {"csharp": {}, "fsharp": {}},
        "deterministic": {"csharp": {}, "fsharp": {}},
    }
    transformed_counts = {
        role["role_id"]: {snapshot.key: 0 for snapshot in snapshots}
        for role in inventory["roles"]
    }
    for snapshot in snapshots:
        edits = _edits_for_snapshot(inventory, snapshot)
        deterministic, applied = _apply_edits(snapshot.data, edits)
        descriptive = snapshot.data
        exact_spans = exact_spans and len(applied) == len(edits)
        descriptive_identity = descriptive_identity and descriptive == snapshot.data
        reverse_identity = reverse_identity and _reverse_edits(deterministic, applied) == snapshot.data
        if snapshot.source_path.suffix.lower() in (".cs", ".fs", ".csproj", ".fsproj"):
            source_rows, source_chunks = _lex(snapshot.data, snapshot.language)
            deterministic_rows, deterministic_chunks = _lex(deterministic, snapshot.language)
            source_identifier_tokens.update(row.token for row in source_rows)
            deterministic_token_counts: dict[str, int] = {}
            for row in deterministic_rows:
                deterministic_token_counts[row.token] = deterministic_token_counts.get(row.token, 0) + 1
            for role in inventory["roles"]:
                transformed_counts[role["role_id"]][snapshot.key] = deterministic_token_counts.get(role["replacement"], 0)
            protected_identity = protected_identity and source_chunks == deterministic_chunks
            excluded_offsets = {edit["offset"] for edit in edits}
            source_public = _public_sequence(snapshot.data, snapshot.language, excluded_offsets)
            descriptive_public = _public_sequence(descriptive, snapshot.language, excluded_offsets)
            deterministic_public = _public_sequence(deterministic, snapshot.language)
            public_identity = public_identity and source_public == descriptive_public == deterministic_public
            observed_public_source[snapshot.language].update(source_public)
            observed_public_deterministic[snapshot.language].update(deterministic_public)
            stem = Path(snapshot.relative_path).stem
            if stem in PUBLIC_BY_LANGUAGE[snapshot.language]:
                observed_public_source[snapshot.language].add(stem)
                observed_public_deterministic[snapshot.language].add(stem)
        idempotent_noop = idempotent_noop and _hash_matched_transform(deterministic, snapshot.data, deterministic) == deterministic
        for treatment, data in (("descriptive", descriptive), ("deterministic", deterministic)):
            destination = output / "transformed" / treatment / snapshot.language / snapshot.relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            generated_hashes[treatment][snapshot.language][snapshot.relative_path] = _sha256(data)

    descriptive_manifest = _rewrite_manifest(original, "descriptive", artifact_name)
    deterministic_manifest = _rewrite_manifest(original, "deterministic", artifact_name)
    original_contract = _manifest_contract(original)
    manifest_contract_equal = (
        _manifest_contract(descriptive_manifest) == original_contract
        and _manifest_contract(deterministic_manifest) == original_contract
    )
    _write_json(output / "descriptive.manifest.json", descriptive_manifest)
    _write_json(output / "deterministic.manifest.json", deterministic_manifest)

    definition = {
        "schema_version": 1,
        "id": VERSION,
        "source_commit": SOURCE_COMMIT,
        "algorithm": "sha256-role-digest-v1",
        "algorithm_domain": DOMAIN,
        "languages": ["csharp", "fsharp"],
        "treatments": ["descriptive", "deterministic"],
        "snapshot_count": {language: sum(1 for snapshot in snapshots if snapshot.language == language) for language in ("csharp", "fsharp")},
    }
    _write_json(output / "definition.json", definition)
    _write_json(output / "generator-version.json", {
        "version": VERSION,
        "source_commit": SOURCE_COMMIT,
        "algorithm_domain": DOMAIN,
    })
    source_manifest = _input_provenance(root, manifest_path, original, snapshots)
    source_manifest["generated_files"] = generated_hashes
    _write_json(output / "source-manifest.json", source_manifest)

    metrics = _metrics_report(output, snapshots)
    coverage_by_role, eligible, transformed = _coverage_report(inventory, transformed_counts)
    replacements = [role["replacement"] for role in mapping["roles"]]
    collision_checks = {
        "replacement_unique": len(replacements) == len(set(replacements)),
        "no_public_identifier_collision": not (set(replacements) & PUBLIC_IDENTIFIERS),
        "no_source_identifier_collision": not (set(replacements) & source_identifier_tokens),
        "no_keyword_collision": not (set(replacements) & (CSHARP_KEYWORDS | FSHARP_KEYWORDS)),
    }
    paired_declarations = all(
        all(counts[language] > 0 for language in ("csharp", "fsharp"))
        for counts in inventory["declarations_by_role_and_language"].values()
    )
    invariants = {
        "coverage_complete": eligible > 0 and _coverage_complete(coverage_by_role),
        "paired_declarations": paired_declarations,
        "replacement_collisions_absent": all(collision_checks.values()),
        "descriptive_byte_identity": descriptive_identity,
        "exact_identifier_spans_only": exact_spans and reverse_identity,
        "protected_lexical_bytes_unchanged": protected_identity,
        "public_identifier_sequence_unchanged": public_identity,
        "declared_public_inventory_exact": all(
            observed_public_source[language] == PUBLIC_BY_LANGUAGE[language]
            and observed_public_deterministic[language] == PUBLIC_BY_LANGUAGE[language]
            for language in ("csharp", "fsharp")
        ),
        "manifest_contract_unchanged": manifest_contract_equal,
        "hash_matched_reapplication_is_noop": idempotent_noop,
    }
    if not all(invariants.values()):
        raise RepresentationError(f"representation invariant failed: {invariants}")

    reports = {
        "schema_version": 1,
        "source_commit": SOURCE_COMMIT,
        "roles": len(inventory["roles"]),
        "occurrences": eligible,
        "declarations": sum(sum(values.values()) for values in inventory["declarations_by_role_and_language"].values()),
        "coverage": transformed / eligible,
        "coverage_by_role": coverage_by_role,
        "collisions": 0 if all(collision_checks.values()) else 1,
        "collision_checks": collision_checks,
        "invariants": invariants,
        "public_inventory": {
            language: {
                "declared": sorted(PUBLIC_BY_LANGUAGE[language]),
                "source_observed": sorted(observed_public_source[language]),
                "deterministic_observed": sorted(observed_public_deterministic[language]),
            }
            for language in ("csharp", "fsharp")
        },
        "manifest_contract_sha256": _sha256(_compact_json_bytes(original_contract)),
        "metrics": metrics,
        "behavioral_validation": {
            "status": "pending-external-model-free-validation",
            "required": [
                "python scripts/alf.py --manifest benchmarks/successor/representation-v1/descriptive.manifest.json validate",
                "python scripts/alf.py --manifest benchmarks/successor/representation-v1/deterministic.manifest.json validate",
            ],
        },
    }
    _write_json(output / "reports.json", reports)
    plan_count = _validate_generated_manifests(root, output, artifact_name)
    reports["manifest_artifact_plans_validated"] = plan_count
    _write_json(output / "reports.json", reports)
    _write_json(output / "artifact-hashes.json", _artifact_hashes(output))
    return {
        "output": str(output),
        "roles": reports["roles"],
        "occurrences": reports["occurrences"],
        "coverage": reports["coverage"],
        "manifest_artifact_plans_validated": plan_count,
        "ok": True,
    }


def _validated_output(root: Path, output: Path | None) -> Path:
    successor = (root / "benchmarks" / "successor").resolve()
    target = (output if output is not None else root / DEFAULT_OUTPUT).resolve()
    if target.parent != successor or not re.fullmatch(r"representation-v1(?:-[a-z0-9][a-z0-9-]*)?", target.name):
        raise RepresentationError("representation output must be a versioned direct child of benchmarks/successor")
    return target


def build_representation(root: Path, output: Path | None = None) -> dict[str, Any]:
    root = root.resolve()
    target = _validated_output(root, output)
    backup = target.parent / f".{target.name}.backup"
    if backup.exists():
        raise RepresentationError(f"stale representation backup requires manual recovery: {backup}")
    temporary = target.parent / f".{target.name}.tmp-{uuid.uuid4().hex}"
    try:
        report = _build_representation_into(root, temporary, target.name)
        if target.exists():
            target.rename(backup)
        try:
            temporary.rename(target)
        except Exception:
            if backup.exists() and not target.exists():
                backup.rename(target)
            raise
        if backup.exists():
            shutil.rmtree(backup)
        report["output"] = str(target)
        return report
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)


def _validate_recorded_sources(root: Path, target: Path) -> None:
    source_manifest_path = target / "source-manifest.json"
    if not source_manifest_path.is_file():
        raise RepresentationError("source-manifest.json is missing")
    recorded = json.loads(source_manifest_path.read_text(encoding="utf-8"))
    if recorded.get("source_commit") != SOURCE_COMMIT:
        raise RepresentationError("recorded source commit differs from generator")
    checks: list[tuple[str, str, bool]] = []
    original = recorded.get("original_manifest", {})
    checks.append((original.get("path", ""), original.get("sha256", ""), True))
    generator = recorded.get("generator_source", {})
    checks.append((generator.get("path", ""), generator.get("sha256", ""), False))
    for prompt in recorded.get("task_prompts", {}).values():
        checks.append((prompt.get("path", ""), prompt.get("sha256", ""), True))
    for path, expected, pinned in checks:
        candidate = root / path
        if not path or not candidate.is_file():
            raise RepresentationError(f"recorded input drift: {path or '<missing path>'}")
        data = _require_pinned_file(root, candidate) if pinned else candidate.read_bytes()
        if _sha256(data) != expected:
            raise RepresentationError(f"recorded input drift: {path}")

    manifest_path = root / recorded["original_manifest"]["path"]
    manifest = json.loads(_require_pinned_file(root, manifest_path).decode("utf-8"))
    current_snapshots = {snapshot.key: snapshot for snapshot in _load_snapshots(root, manifest)}
    for language, files in recorded.get("files", {}).items():
        for relative, expected in files.items():
            key = f"{language}:{relative}"
            snapshot = current_snapshots.get(key)
            if snapshot is None or _sha256(snapshot.data) != expected:
                raise RepresentationError(f"recorded source drift: {key}")
    if set(current_snapshots) != {
        f"{language}:{relative}"
        for language, files in recorded.get("files", {}).items()
        for relative in files
    }:
        raise RepresentationError("recorded source snapshot set drift")


def _tree_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): _sha256(path.read_bytes())
        for path in sorted(item for item in root.rglob("*") if item.is_file())
    }


def check_representation(root: Path, output: Path | None = None) -> dict[str, Any]:
    root = root.resolve()
    target = _validated_output(root, output)
    if not target.is_dir():
        raise RepresentationError(f"representation artifact directory is missing: {target}")
    _validate_recorded_sources(root, target)
    before = _tree_hashes(target)
    temporary = target.parent / f".{target.name}.check-{uuid.uuid4().hex}"
    try:
        generated = _build_representation_into(root, temporary, target.name)
        expected = _tree_hashes(temporary)
        if before != expected:
            missing = sorted(set(expected) - set(before))
            stale = sorted(set(before) - set(expected))
            changed = sorted(path for path in set(before) & set(expected) if before[path] != expected[path])
            raise RepresentationError(f"representation artifacts are stale: missing={missing}, extra={stale}, changed={changed}")
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
    after = _tree_hashes(target)
    if after != before:
        raise RepresentationError("representation check modified the checked artifact tree")
    return {
        **generated,
        "output": str(target),
        "checked_files": len(before),
        "write_free": True,
        "ok": True,
    }
