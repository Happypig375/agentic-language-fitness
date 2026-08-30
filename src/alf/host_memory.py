"""Small, deterministic host-memory probes used by the candidate wrapper."""
from __future__ import annotations

import ctypes
import json
import platform
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def probe_host_memory() -> dict[str, Any]:
    system = platform.system()
    if system == "Windows":
        class State(ctypes.Structure):
            _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
        state = State(); state.dwLength = ctypes.sizeof(State)
        if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(state)):
            raise OSError("GlobalMemoryStatusEx failed")
        return {"platform": "Windows", "total_physical_bytes": state.ullTotalPhys,
                "available_physical_bytes": state.ullAvailPhys,
                "total_commit_bytes": state.ullTotalPageFile,
                "available_commit_bytes": state.ullAvailPageFile}
    if system == "Linux":
        values: dict[str, int] = {}
        for line in Path("/proc/meminfo").read_text(encoding="ascii").splitlines():
            key, _, raw = line.partition(":")
            parts = raw.strip().split()
            if parts and parts[0].isdigit():
                values[key] = int(parts[0]) * (1024 if len(parts) > 1 and parts[1] == "kB" else 1)
        total = values["MemTotal"]; available = values.get("MemAvailable", values.get("MemFree", 0))
        limit = values.get("CommitLimit", total); committed = values.get("Committed_AS", 0)
        return {"platform": "Linux", "total_physical_bytes": total,
                "available_physical_bytes": available, "total_commit_bytes": limit,
                "available_commit_bytes": max(0, limit - committed)}
    raise OSError(f"unsupported host platform: {system}")


def evaluate_host_memory(requirement: dict[str, Any]) -> dict[str, Any]:
    result = {"observed_at": _now(), "thresholds": {
        "minimum_available_physical_bytes": requirement["minimum_available_physical_bytes"],
        "minimum_available_commit_bytes": requirement["minimum_available_commit_bytes"],}}
    try:
        result.update(probe_host_memory())
        result["ok"] = (result["available_physical_bytes"] >= result["thresholds"]["minimum_available_physical_bytes"]
                         and result["available_commit_bytes"] >= result["thresholds"]["minimum_available_commit_bytes"])
        result["probe_error"] = None
    except Exception as exc:
        result.update({"platform": platform.system(), "probe_error": str(exc), "ok": False})
    return result


def parse_requirement(value: str | None) -> dict[str, int] | None:
    if not value:
        return None
    parsed = json.loads(value)
    if not isinstance(parsed, dict):
        raise ValueError("host_memory must be an object")
    result: dict[str, int] = {}
    for name in ("minimum_available_physical_bytes", "minimum_available_commit_bytes"):
        item = parsed.get(name)
        if isinstance(item, bool) or not isinstance(item, int) or item <= 0:
            raise ValueError(f"{name} must be a positive integer")
        result[name] = item
    return result
