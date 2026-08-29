from __future__ import annotations

import ntpath
import os
import re
import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Any


_DRIVE = re.compile(r"^[A-Za-z]:")
_TOP_LEVEL_DESTINATIONS = {".git", ".alf", "bin", "obj"}
_CHECK_KEYS = {"file_exists", "text_contains", "text_not_contains"}
_WINDOWS_RESERVED_STEMS = {
    "con",
    "prn",
    "aux",
    "nul",
    *(f"com{index}" for index in range(1, 10)),
    *(f"lpt{index}" for index in range(1, 10)),
}


def _parts(value: Any, *, field: str) -> tuple[str, ...]:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} must be a non-empty relative path")
    normalized = value.replace("\\", "/")
    if normalized.startswith("/") or normalized.startswith("//") or _DRIVE.match(normalized):
        raise ValueError(f"{field} must be relative")
    parts = tuple(normalized.split("/"))
    if any(part in ("", ".", "..") for part in parts):
        raise ValueError(f"{field} contains an empty, dot, or dot-dot segment")
    for part in parts:
        if ":" in part:
            raise ValueError(f"{field} contains an NTFS alternate-data-stream separator")
        if part.endswith((".", " ")):
            raise ValueError(f"{field} contains a component ending in dot or space")
        if part.split(".", 1)[0].casefold() in _WINDOWS_RESERVED_STEMS:
            raise ValueError(f"{field} contains a reserved Windows device name")
    return parts


def _is_windows() -> bool:
    return os.name == "nt"


def _root_relative_parts(path: Path, root: Path, *, field: str) -> tuple[str, ...]:
    """Return a lexical relative path; use-time handle checks are the boundary."""
    path_absolute = Path(os.path.abspath(path))
    root_absolute = Path(os.path.abspath(root))
    try:
        relative = path_absolute.relative_to(root_absolute)
    except ValueError as exc:
        raise ValueError(f"{field} escapes its root") from exc
    parts = tuple(relative.parts)
    if not parts:
        raise ValueError(f"{field} must identify a file beneath its root")
    return parts


@dataclass(frozen=True)
class Artifact:
    source_root: Path
    source_parts: tuple[str, ...]
    target_root: Path
    target_parts: tuple[str, ...]
    target_relative: str

    @property
    def source(self) -> Path:
        return self.source_root.joinpath(*self.source_parts)

    @property
    def target(self) -> Path:
        return self.target_root.joinpath(*self.target_parts)


def _require_posix_primitives(*, create: bool = False) -> tuple[int, int]:
    directory = getattr(os, "O_DIRECTORY", 0)
    nofollow = getattr(os, "O_NOFOLLOW", 0)
    supports_dir_fd = getattr(os, "supports_dir_fd", set())
    if not directory or not nofollow or os.open not in supports_dir_fd:
        raise ValueError("secure descriptor-relative path operations are unavailable")
    if create and os.mkdir not in supports_dir_fd:
        raise ValueError("secure descriptor-relative directory creation is unavailable")
    return directory, nofollow


def _close_fds(fds: list[int]) -> None:
    for fd in reversed(fds):
        try:
            os.close(fd)
        except OSError:
            pass


def _posix_parent_chain(
    root: Path,
    parts: tuple[str, ...],
    *,
    field: str,
    create: bool,
) -> tuple[list[int], int | None]:
    directory, nofollow = _require_posix_primitives(create=create)
    flags = os.O_RDONLY | directory | nofollow | getattr(os, "O_CLOEXEC", 0)
    try:
        root_fd = os.open(root, flags)
    except OSError as exc:
        raise ValueError(f"{field} root cannot be opened safely") from exc
    fds = [root_fd]
    try:
        root_info = os.fstat(root_fd)
    except Exception:
        _close_fds(fds)
        raise
    if not stat.S_ISDIR(root_info.st_mode):
        _close_fds(fds)
        raise ValueError(f"{field} root is not a directory")

    try:
        for component in parts[:-1]:
            try:
                child_fd = os.open(component, flags, dir_fd=fds[-1])
            except FileNotFoundError:
                if not create:
                    return fds, None
                try:
                    os.mkdir(component, 0o755, dir_fd=fds[-1])
                except FileExistsError:
                    pass
                try:
                    child_fd = os.open(component, flags, dir_fd=fds[-1])
                except OSError as exc:
                    raise ValueError(f"{field} parent changed during secure creation") from exc
            except OSError as exc:
                raise ValueError(f"{field} contains an unsafe parent component") from exc
            # Transfer ownership before any verification that can raise.
            fds.append(child_fd)
            if not stat.S_ISDIR(os.fstat(child_fd).st_mode):
                raise ValueError(f"{field} contains a non-directory parent component")
        return fds, fds[-1]
    except Exception:
        _close_fds(fds)
        raise


def _posix_open_regular(
    root: Path,
    parts: tuple[str, ...],
    *,
    field: str,
    allow_missing: bool,
    single_link: bool,
) -> int | None:
    _, nofollow = _require_posix_primitives()
    fds, parent_fd = _posix_parent_chain(root, parts, field=field, create=False)
    if parent_fd is None:
        _close_fds(fds)
        if allow_missing:
            return None
        raise ValueError(f"{field} is missing")
    try:
        try:
            fd = os.open(
                parts[-1],
                os.O_RDONLY | nofollow | getattr(os, "O_CLOEXEC", 0),
                dir_fd=parent_fd,
            )
        except FileNotFoundError as exc:
            if allow_missing:
                return None
            raise ValueError(f"{field} is missing") from exc
        except OSError as exc:
            raise ValueError(f"{field} cannot be opened without following links") from exc
        try:
            info = os.fstat(fd)
            if not stat.S_ISREG(info.st_mode) or (single_link and info.st_nlink != 1):
                raise ValueError(f"{field} must be a safe regular file")
        except Exception:
            os.close(fd)
            raise
        return fd
    finally:
        _close_fds(fds)


def _posix_open_target(root: Path, parts: tuple[str, ...], *, field: str) -> int:
    _, nofollow = _require_posix_primitives(create=True)
    fds, parent_fd = _posix_parent_chain(root, parts, field=field, create=True)
    assert parent_fd is not None
    flags = os.O_WRONLY | nofollow | getattr(os, "O_CLOEXEC", 0)
    try:
        try:
            fd = os.open(parts[-1], flags, dir_fd=parent_fd)
        except FileNotFoundError:
            try:
                fd = os.open(
                    parts[-1],
                    flags | os.O_CREAT | os.O_EXCL,
                    0o644,
                    dir_fd=parent_fd,
                )
            except FileExistsError:
                try:
                    fd = os.open(parts[-1], flags, dir_fd=parent_fd)
                except OSError as exc:
                    raise ValueError(f"{field} changed during secure creation") from exc
            except OSError as exc:
                raise ValueError(f"{field} cannot be created safely") from exc
        except OSError as exc:
            raise ValueError(f"{field} cannot be opened without following links") from exc
        try:
            info = os.fstat(fd)
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                raise ValueError(f"{field} must be a single-link regular file")
            os.ftruncate(fd, 0)
        except Exception:
            os.close(fd)
            raise
        return fd
    finally:
        _close_fds(fds)


class _WindowsApi:
    GENERIC_READ = 0x80000000
    GENERIC_WRITE = 0x40000000
    FILE_READ_ATTRIBUTES = 0x00000080
    FILE_SHARE_READ = 0x00000001
    CREATE_NEW = 1
    OPEN_EXISTING = 3
    FILE_ATTRIBUTE_NORMAL = 0x00000080
    FILE_ATTRIBUTE_DIRECTORY = 0x00000010
    FILE_ATTRIBUTE_REPARSE_POINT = 0x00000400
    FILE_FLAG_BACKUP_SEMANTICS = 0x02000000
    FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000
    FILE_TYPE_DISK = 1
    FILE_BEGIN = 0
    ERROR_FILE_NOT_FOUND = 2
    ERROR_PATH_NOT_FOUND = 3
    ERROR_FILE_EXISTS = 80
    ERROR_ALREADY_EXISTS = 183

    def __init__(self) -> None:
        try:
            import ctypes
            from ctypes import wintypes

            self.ctypes = ctypes
            self.wintypes = wintypes

            class ByHandleFileInformation(ctypes.Structure):
                _fields_ = [
                    ("dwFileAttributes", wintypes.DWORD),
                    ("ftCreationTime", wintypes.FILETIME),
                    ("ftLastAccessTime", wintypes.FILETIME),
                    ("ftLastWriteTime", wintypes.FILETIME),
                    ("dwVolumeSerialNumber", wintypes.DWORD),
                    ("nFileSizeHigh", wintypes.DWORD),
                    ("nFileSizeLow", wintypes.DWORD),
                    ("nNumberOfLinks", wintypes.DWORD),
                    ("nFileIndexHigh", wintypes.DWORD),
                    ("nFileIndexLow", wintypes.DWORD),
                ]

            self.ByHandleFileInformation = ByHandleFileInformation
            self.kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            self.kernel32.CreateFileW.argtypes = [
                wintypes.LPCWSTR,
                wintypes.DWORD,
                wintypes.DWORD,
                wintypes.LPVOID,
                wintypes.DWORD,
                wintypes.DWORD,
                wintypes.HANDLE,
            ]
            self.kernel32.CreateFileW.restype = wintypes.HANDLE
            self.kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
            self.kernel32.CloseHandle.restype = wintypes.BOOL
            self.kernel32.GetFileInformationByHandle.argtypes = [
                wintypes.HANDLE,
                ctypes.POINTER(ByHandleFileInformation),
            ]
            self.kernel32.GetFileInformationByHandle.restype = wintypes.BOOL
            self.kernel32.GetFileType.argtypes = [wintypes.HANDLE]
            self.kernel32.GetFileType.restype = wintypes.DWORD
            self.kernel32.GetFinalPathNameByHandleW.argtypes = [
                wintypes.HANDLE,
                wintypes.LPWSTR,
                wintypes.DWORD,
                wintypes.DWORD,
            ]
            self.kernel32.GetFinalPathNameByHandleW.restype = wintypes.DWORD
            self.kernel32.CreateDirectoryW.argtypes = [wintypes.LPCWSTR, wintypes.LPVOID]
            self.kernel32.CreateDirectoryW.restype = wintypes.BOOL
            self.kernel32.ReadFile.argtypes = [
                wintypes.HANDLE,
                wintypes.LPVOID,
                wintypes.DWORD,
                ctypes.POINTER(wintypes.DWORD),
                wintypes.LPVOID,
            ]
            self.kernel32.ReadFile.restype = wintypes.BOOL
            self.kernel32.WriteFile.argtypes = self.kernel32.ReadFile.argtypes
            self.kernel32.WriteFile.restype = wintypes.BOOL
            self.kernel32.SetFilePointerEx.argtypes = [
                wintypes.HANDLE,
                ctypes.c_longlong,
                ctypes.POINTER(ctypes.c_longlong),
                wintypes.DWORD,
            ]
            self.kernel32.SetFilePointerEx.restype = wintypes.BOOL
            self.kernel32.SetEndOfFile.argtypes = [wintypes.HANDLE]
            self.kernel32.SetEndOfFile.restype = wintypes.BOOL
            self.invalid_handle = ctypes.c_void_p(-1).value
        except Exception as exc:
            raise ValueError("required Win32 safe-path APIs are unavailable") from exc

    def _error(self, message: str) -> OSError:
        code = self.ctypes.get_last_error()
        return OSError(code, f"{message}: {self.ctypes.FormatError(code)}")

    def open(self, path: str, access: int, share: int, disposition: int, flags: int) -> int:
        handle = self.kernel32.CreateFileW(path, access, share, None, disposition, flags, None)
        if handle == self.invalid_handle:
            raise self._error("CreateFileW failed")
        return int(handle)

    def close(self, handle: int) -> None:
        if not self.kernel32.CloseHandle(handle):
            raise self._error("CloseHandle failed")

    def info(self, handle: int) -> Any:
        result = self.ByHandleFileInformation()
        if not self.kernel32.GetFileInformationByHandle(handle, self.ctypes.byref(result)):
            raise self._error("GetFileInformationByHandle failed")
        return result

    def file_type(self, handle: int) -> int:
        return int(self.kernel32.GetFileType(handle))

    def final_path(self, handle: int) -> str:
        needed = self.kernel32.GetFinalPathNameByHandleW(handle, None, 0, 0)
        if not needed:
            raise self._error("GetFinalPathNameByHandleW failed")
        buffer = self.ctypes.create_unicode_buffer(needed + 1)
        written = self.kernel32.GetFinalPathNameByHandleW(handle, buffer, len(buffer), 0)
        if not written or written >= len(buffer):
            raise self._error("GetFinalPathNameByHandleW failed")
        return buffer.value

    def create_directory(self, path: str) -> None:
        if self.kernel32.CreateDirectoryW(path, None):
            return
        code = self.ctypes.get_last_error()
        if code not in (self.ERROR_FILE_EXISTS, self.ERROR_ALREADY_EXISTS):
            raise self._error("CreateDirectoryW failed")

    def read_all(self, handle: int) -> bytes:
        chunks: list[bytes] = []
        while True:
            buffer = self.ctypes.create_string_buffer(64 * 1024)
            count = self.wintypes.DWORD()
            if not self.kernel32.ReadFile(handle, buffer, len(buffer), self.ctypes.byref(count), None):
                raise self._error("ReadFile failed")
            if count.value == 0:
                return b"".join(chunks)
            chunks.append(buffer.raw[: count.value])

    def truncate_and_write(self, handle: int, data: bytes) -> None:
        if not self.kernel32.SetFilePointerEx(handle, 0, None, self.FILE_BEGIN):
            raise self._error("SetFilePointerEx failed")
        if not self.kernel32.SetEndOfFile(handle):
            raise self._error("SetEndOfFile failed")
        offset = 0
        while offset < len(data):
            chunk = data[offset : offset + 64 * 1024]
            buffer = self.ctypes.create_string_buffer(chunk)
            count = self.wintypes.DWORD()
            if not self.kernel32.WriteFile(handle, buffer, len(chunk), self.ctypes.byref(count), None):
                raise self._error("WriteFile failed")
            if count.value == 0:
                raise OSError("WriteFile made no progress")
            offset += count.value


_WINDOWS_API: _WindowsApi | None = None


def _get_windows_api() -> _WindowsApi:
    global _WINDOWS_API
    if not _is_windows():
        raise ValueError("Win32 safe-path APIs requested on a non-Windows host")
    if _WINDOWS_API is None:
        _WINDOWS_API = _WindowsApi()
    return _WINDOWS_API


def _win_normalized(path: str) -> str:
    return ntpath.normcase(ntpath.normpath(path))


def _win_beneath(path: str, root: str) -> bool:
    normalized_path = _win_normalized(path)
    normalized_root = _win_normalized(root)
    try:
        return ntpath.commonpath([normalized_path, normalized_root]) == normalized_root
    except ValueError:
        return False


def _win_close_all(api: _WindowsApi, handles: list[int]) -> None:
    for handle in reversed(handles):
        try:
            api.close(handle)
        except OSError:
            pass


def _win_open_raw(
    api: _WindowsApi,
    path: str,
    *,
    access: int,
    share: int,
    disposition: int,
    flags: int,
    allow_missing: bool,
) -> int | None:
    try:
        return api.open(path, access, share, disposition, flags)
    except OSError as exc:
        if allow_missing and exc.errno in (api.ERROR_FILE_NOT_FOUND, api.ERROR_PATH_NOT_FOUND):
            return None
        raise


def _win_verify_directory(api: _WindowsApi, handle: int, *, field: str) -> str:
    info = api.info(handle)
    if api.file_type(handle) != api.FILE_TYPE_DISK:
        raise ValueError(f"{field} is not on a regular disk filesystem")
    if not info.dwFileAttributes & api.FILE_ATTRIBUTE_DIRECTORY:
        raise ValueError(f"{field} contains a non-directory component")
    if info.dwFileAttributes & api.FILE_ATTRIBUTE_REPARSE_POINT:
        raise ValueError(f"{field} contains a reparse point")
    return api.final_path(handle)


def _win_verify_regular(
    api: _WindowsApi,
    handle: int,
    *,
    field: str,
    root_final: str,
    single_link: bool,
) -> None:
    info = api.info(handle)
    if api.file_type(handle) != api.FILE_TYPE_DISK:
        raise ValueError(f"{field} is not a regular disk file")
    if info.dwFileAttributes & (api.FILE_ATTRIBUTE_DIRECTORY | api.FILE_ATTRIBUTE_REPARSE_POINT):
        raise ValueError(f"{field} must be a regular file, not a directory or reparse point")
    if single_link and info.nNumberOfLinks != 1:
        raise ValueError(f"{field} must be a single-link regular file")
    if not _win_beneath(api.final_path(handle), root_final):
        raise ValueError(f"{field} escapes its opened root")


def _win_parent_chain(
    root: Path,
    parts: tuple[str, ...],
    *,
    field: str,
) -> tuple[_WindowsApi, list[int], str, str | None]:
    api = _get_windows_api()
    directory_flags = api.FILE_FLAG_BACKUP_SEMANTICS | api.FILE_FLAG_OPEN_REPARSE_POINT
    try:
        root_handle = api.open(
            os.path.abspath(root),
            api.FILE_READ_ATTRIBUTES,
            api.FILE_SHARE_READ,
            api.OPEN_EXISTING,
            directory_flags,
        )
    except OSError as exc:
        raise ValueError(f"{field} root cannot be opened safely") from exc
    handles = [root_handle]
    try:
        root_final = _win_verify_directory(api, root_handle, field=f"{field} root")
        current = root_final
        for component in parts[:-1]:
            path = ntpath.join(current, component)
            try:
                child = _win_open_raw(
                    api,
                    path,
                    access=api.FILE_READ_ATTRIBUTES,
                    share=api.FILE_SHARE_READ,
                    disposition=api.OPEN_EXISTING,
                    flags=directory_flags,
                    allow_missing=True,
                )
            except OSError as exc:
                raise ValueError(f"{field} parent cannot be opened safely") from exc
            if child is None:
                return api, handles, root_final, None
            # Transfer ownership before attributes/final-path verification.
            handles.append(child)
            child_final = _win_verify_directory(api, child, field=field)
            if not _win_beneath(child_final, root_final):
                raise ValueError(f"{field} parent escapes its opened root")
            current = child_final
        return api, handles, root_final, current
    except Exception:
        _win_close_all(api, handles)
        raise


def _win_parent_chain_create(
    root: Path,
    parts: tuple[str, ...],
    *,
    field: str,
) -> tuple[_WindowsApi, list[int], str, str]:
    api = _get_windows_api()
    directory_flags = api.FILE_FLAG_BACKUP_SEMANTICS | api.FILE_FLAG_OPEN_REPARSE_POINT
    try:
        root_handle = api.open(
            os.path.abspath(root),
            api.FILE_READ_ATTRIBUTES,
            api.FILE_SHARE_READ,
            api.OPEN_EXISTING,
            directory_flags,
        )
    except OSError as exc:
        raise ValueError(f"{field} root cannot be opened safely") from exc
    handles = [root_handle]
    try:
        root_final = _win_verify_directory(api, root_handle, field=f"{field} root")
        current = root_final
        for component in parts[:-1]:
            path = ntpath.join(current, component)
            try:
                child = _win_open_raw(
                    api,
                    path,
                    access=api.FILE_READ_ATTRIBUTES,
                    share=api.FILE_SHARE_READ,
                    disposition=api.OPEN_EXISTING,
                    flags=directory_flags,
                    allow_missing=True,
                )
                if child is None:
                    # Existing parents stay locked without write/delete sharing
                    # while this single namespace component is created.
                    api.create_directory(path)
                    child = _win_open_raw(
                        api,
                        path,
                        access=api.FILE_READ_ATTRIBUTES,
                        share=api.FILE_SHARE_READ,
                        disposition=api.OPEN_EXISTING,
                        flags=directory_flags,
                        allow_missing=False,
                    )
                    assert child is not None
            except OSError as exc:
                raise ValueError(f"{field} parent cannot be created safely") from exc
            # Transfer ownership before attributes/final-path verification.
            handles.append(child)
            child_final = _win_verify_directory(api, child, field=field)
            if not _win_beneath(child_final, root_final):
                raise ValueError(f"{field} parent escapes its opened root")
            current = child_final
        return api, handles, root_final, current
    except Exception:
        _win_close_all(api, handles)
        raise


def _win_open_regular(
    root: Path,
    parts: tuple[str, ...],
    *,
    field: str,
    allow_missing: bool,
    single_link: bool,
) -> tuple[_WindowsApi, int] | None:
    api, parents, root_final, parent_final = _win_parent_chain(root, parts, field=field)
    if parent_final is None:
        _win_close_all(api, parents)
        if allow_missing:
            return None
        raise ValueError(f"{field} is missing")
    try:
        path = ntpath.join(parent_final, parts[-1])
        try:
            handle = _win_open_raw(
                api,
                path,
                access=api.GENERIC_READ | api.FILE_READ_ATTRIBUTES,
                share=api.FILE_SHARE_READ,
                disposition=api.OPEN_EXISTING,
                flags=api.FILE_FLAG_OPEN_REPARSE_POINT,
                allow_missing=allow_missing,
            )
        except OSError as exc:
            raise ValueError(f"{field} cannot be opened safely") from exc
        if handle is None:
            return None
        try:
            _win_verify_regular(
                api,
                handle,
                field=field,
                root_final=root_final,
                single_link=single_link,
            )
        except Exception:
            api.close(handle)
            raise
        return api, handle
    finally:
        _win_close_all(api, parents)


def _win_open_target(root: Path, parts: tuple[str, ...], *, field: str) -> tuple[_WindowsApi, int]:
    api, parents, root_final, parent_final = _win_parent_chain_create(root, parts, field=field)
    try:
        path = ntpath.join(parent_final, parts[-1])
        access = api.GENERIC_WRITE | api.FILE_READ_ATTRIBUTES
        try:
            handle = _win_open_raw(
                api,
                path,
                access=access,
                share=0,
                disposition=api.OPEN_EXISTING,
                flags=api.FILE_FLAG_OPEN_REPARSE_POINT,
                allow_missing=True,
            )
            if handle is None:
                try:
                    handle = api.open(
                        path,
                        access,
                        0,
                        api.CREATE_NEW,
                        api.FILE_ATTRIBUTE_NORMAL | api.FILE_FLAG_OPEN_REPARSE_POINT,
                    )
                except OSError as exc:
                    if exc.errno not in (api.ERROR_FILE_EXISTS, api.ERROR_ALREADY_EXISTS):
                        raise
                    handle = api.open(
                        path,
                        access,
                        0,
                        api.OPEN_EXISTING,
                        api.FILE_FLAG_OPEN_REPARSE_POINT,
                    )
        except OSError as exc:
            raise ValueError(f"{field} cannot be created safely") from exc
        try:
            _win_verify_regular(
                api,
                handle,
                field=field,
                root_final=root_final,
                single_link=True,
            )
        except Exception:
            api.close(handle)
            raise
        return api, handle
    finally:
        _win_close_all(api, parents)


def _secure_probe_regular(
    root: Path,
    parts: tuple[str, ...],
    *,
    field: str,
    single_link: bool,
) -> bool:
    if _is_windows():
        opened = _win_open_regular(
            root, parts, field=field, allow_missing=True, single_link=single_link
        )
        if opened is None:
            return False
        api, handle = opened
        api.close(handle)
        return True
    fd = _posix_open_regular(
        root, parts, field=field, allow_missing=True, single_link=single_link
    )
    if fd is None:
        return False
    os.close(fd)
    return True


def _secure_read(
    root: Path,
    parts: tuple[str, ...],
    *,
    field: str,
    single_link: bool,
) -> bytes | None:
    if _is_windows():
        opened = _win_open_regular(
            root, parts, field=field, allow_missing=True, single_link=single_link
        )
        if opened is None:
            return None
        api, handle = opened
        try:
            return api.read_all(handle)
        finally:
            api.close(handle)
    fd = _posix_open_regular(
        root, parts, field=field, allow_missing=True, single_link=single_link
    )
    if fd is None:
        return None
    try:
        chunks: list[bytes] = []
        while True:
            chunk = os.read(fd, 64 * 1024)
            if not chunk:
                return b"".join(chunks)
            chunks.append(chunk)
    finally:
        os.close(fd)


def _secure_write(root: Path, parts: tuple[str, ...], data: bytes, *, field: str) -> None:
    if _is_windows():
        api, handle = _win_open_target(root, parts, field=field)
        try:
            api.truncate_and_write(handle, data)
        finally:
            api.close(handle)
        return
    fd = _posix_open_target(root, parts, field=field)
    try:
        offset = 0
        while offset < len(data):
            written = os.write(fd, data[offset:])
            if written == 0:
                raise OSError("write made no progress")
            offset += written
    finally:
        os.close(fd)


def artifact_plan(
    root: Path,
    manifest: dict[str, Any],
    language: str,
    task: dict[str, Any],
    workspace: Path,
) -> list[Artifact]:
    """Validate a complete gold copy plan without mutating the workspace."""
    if language not in manifest.get("languages", {}):
        raise ValueError(f"unknown language {language!r}")
    cfg = manifest["languages"][language]
    benchmark_root_value = (
        getattr(manifest, "manifest_parent", None)
        or (root / "benchmarks/pilot")
    )
    benchmark_root = Path(benchmark_root_value)
    gold = task.get("gold", {}).get(language) if isinstance(task.get("gold"), dict) else None
    if isinstance(gold, str):
        entries = [{"source": gold, "target": cfg.get("source_file")}]
    elif (
        isinstance(gold, dict)
        and set(gold) == {"files"}
        and isinstance(gold["files"], list)
        and gold["files"]
    ):
        entries = gold["files"]
    else:
        raise ValueError(f"gold[{language}] must be a path or a non-empty files object")

    result: list[Artifact] = []
    seen: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict) or set(entry) != {"source", "target"}:
            raise ValueError(f"gold[{language}].files[{index}] must contain exactly source and target")
        source_repo_parts = _parts(entry.get("source"), field="gold source")
        target_parts = _parts(entry.get("target"), field="gold target")
        if target_parts[0].casefold() in _TOP_LEVEL_DESTINATIONS:
            raise ValueError("gold target cannot write to metadata/build destination")
        target_relative = "/".join(target_parts)
        folded = "/".join(part.casefold() for part in target_parts)
        if folded in seen:
            raise ValueError("gold targets must be unique under case-folded normalization")
        seen.add(folded)
        source_parts = _root_relative_parts(
            root.joinpath(*source_repo_parts), benchmark_root, field="gold source"
        )
        result.append(
            Artifact(
                source_root=benchmark_root,
                source_parts=source_parts,
                target_root=workspace,
                target_parts=target_parts,
                target_relative=target_relative,
            )
        )

    # Validate every source and target before returning any usable plan. These
    # opens are repeated by copy_artifacts because the filesystem is mutable.
    for artifact in result:
        if not _secure_probe_regular(
            artifact.source_root,
            artifact.source_parts,
            field="gold source",
            single_link=False,
        ):
            raise ValueError("gold source must be an existing regular file")
        _secure_probe_regular(
            artifact.target_root,
            artifact.target_parts,
            field="gold target",
            single_link=True,
        )
    return result


def copy_artifacts(plan: list[Artifact]) -> None:
    """Reopen every path from its root and copy only through verified handles."""
    if not isinstance(plan, list) or any(not isinstance(item, Artifact) for item in plan):
        raise ValueError("artifact copy plan is invalid")

    # Revalidate the entire mutable plan before the first write.
    for artifact in plan:
        if not _secure_probe_regular(
            artifact.source_root,
            artifact.source_parts,
            field="gold source",
            single_link=False,
        ):
            raise ValueError("gold source changed or disappeared")
        _secure_probe_regular(
            artifact.target_root,
            artifact.target_parts,
            field="gold target",
            single_link=True,
        )

    for artifact in plan:
        data = _secure_read(
            artifact.source_root,
            artifact.source_parts,
            field="gold source",
            single_link=False,
        )
        if data is None:
            raise ValueError("gold source changed or disappeared")
        _secure_write(
            artifact.target_root,
            artifact.target_parts,
            data,
            field="gold target",
        )


def checks_for_language(
    task: dict[str, Any], language: str, languages: set[str]
) -> dict[str, Any]:
    raw = task.get("workspace_checks", {})
    if raw is None or not isinstance(raw, dict):
        raise ValueError("workspace_checks must be an object")
    if not raw:
        return {key: [] for key in _CHECK_KEYS}
    if set(raw) != languages:
        raise ValueError("workspace_checks must declare exactly every manifest language")
    if language not in languages:
        raise ValueError(f"unknown workspace-check language {language!r}")
    for sibling_language in languages:
        sibling = raw[sibling_language]
        if not isinstance(sibling, dict) or set(sibling) != _CHECK_KEYS:
            raise ValueError(
                "each language workspace_checks object must have exactly the check keys"
            )
        for key in _CHECK_KEYS:
            if not isinstance(sibling[key], list):
                raise ValueError(f"workspace_checks[{sibling_language}].{key} must be a list")
    selected = raw[language]
    return {key: list(selected[key]) for key in _CHECK_KEYS}


def merge_workspace_checks(workspace: Path, checks: dict[str, Any]) -> dict[str, Any]:
    """Normalize a complete check plan without reading candidate-controlled files."""
    if not isinstance(checks, dict) or set(checks) != _CHECK_KEYS:
        raise ValueError("workspace checks must have exactly the check keys")
    normalized = {key: [] for key in _CHECK_KEYS}
    for key in _CHECK_KEYS:
        values = checks[key]
        if not isinstance(values, list):
            raise ValueError(f"{key} must be a list")
        for item in values:
            if key == "file_exists":
                parts = _parts(item, field="workspace check path")
                if parts[0].casefold() in _TOP_LEVEL_DESTINATIONS:
                    raise ValueError("workspace check cannot target metadata/build destination")
                normalized[key].append("/".join(parts))
            else:
                if (
                    not isinstance(item, dict)
                    or set(item) != {"path", "text"}
                    or not isinstance(item.get("text"), str)
                ):
                    raise ValueError(f"{key} entries require exactly path and text")
                parts = _parts(item.get("path"), field="workspace check path")
                if parts[0].casefold() in _TOP_LEVEL_DESTINATIONS:
                    raise ValueError("workspace check cannot target metadata/build destination")
                normalized[key].append({"path": "/".join(parts), "text": item["text"]})
    return normalized


def check_workspace(workspace: Path, checks: dict[str, Any] | None) -> dict[str, Any]:
    supplied = checks or {}
    if not isinstance(supplied, dict) or not set(supplied) <= _CHECK_KEYS:
        raise ValueError("workspace checks contain unknown keys")
    checks = merge_workspace_checks(
        workspace, {key: supplied.get(key, []) for key in _CHECK_KEYS}
    )
    report: dict[str, Any] = {
        "ok": True,
        "file_exists": [],
        "text_contains": [],
        "text_not_contains": [],
    }

    paths: list[tuple[str, ...]] = []
    for value in checks["file_exists"]:
        paths.append(_parts(value, field="workspace check path"))
    for key in ("text_contains", "text_not_contains"):
        for item in checks[key]:
            paths.append(_parts(item["path"], field="workspace check path"))

    # Validate the whole current check plan before reading any candidate file.
    # A missing regular file is a failed check; an unsafe component is an error.
    for parts in paths:
        _secure_probe_regular(
            workspace,
            parts,
            field="workspace check",
            single_link=True,
        )

    for value in checks["file_exists"]:
        parts = _parts(value, field="workspace check path")
        passed = _secure_probe_regular(
            workspace,
            parts,
            field="workspace check",
            single_link=True,
        )
        report["file_exists"].append({"path": value, "passed": passed})
        report["ok"] = report["ok"] and passed

    for key, contains in (("text_contains", True), ("text_not_contains", False)):
        for item in checks[key]:
            parts = _parts(item["path"], field="workspace check path")
            data = _secure_read(
                workspace,
                parts,
                field="workspace check",
                single_link=True,
            )
            try:
                text = None if data is None else data.decode("utf-8")
            except UnicodeError:
                text = None
            passed = text is not None and (
                (item["text"] in text) if contains else (item["text"] not in text)
            )
            report[key].append(
                {"path": item["path"], "text": item["text"], "passed": passed}
            )
            report["ok"] = report["ok"] and passed
    return report
