#!/usr/bin/env python3
"""A deliberately small, loopback-only CONNECT transport for chatgpt.com."""
from __future__ import annotations

import argparse
import json
import os
import select
import socket
import sys
import threading
import time
import uuid
from pathlib import Path

ALLOW = ("chatgpt.com", 443)
MAX_HEADER = 8192
MAX_CLIENTS = 8
HEADER_TIMEOUT = 30.0
CONNECT_TIMEOUT = 15.0
DEFAULT_IDLE_TIMEOUT = 900.0


def parse_connect(data: bytes) -> None:
    if len(data) > MAX_HEADER or b"\r\n\r\n" not in data:
        raise ValueError("incomplete or oversized headers")
    lines = data.split(b"\r\n")
    try:
        method, authority, version = lines[0].decode("ascii").split(" ")
    except (UnicodeDecodeError, ValueError) as exc:
        raise ValueError("malformed request") from exc
    if method != "CONNECT" or version not in ("HTTP/1.0", "HTTP/1.1"):
        raise ValueError("CONNECT required")
    host, sep, port = authority.rpartition(":")
    if not sep or host.lower() != ALLOW[0] or port != str(ALLOW[1]):
        raise ValueError("destination not allowed")
    for line in lines[1:]:
        if not line:
            break
        if b":" not in line:
            raise ValueError("malformed header")
        name, value = line.split(b":", 1)
        name = name.decode("ascii").strip().lower()
        value = value.decode("ascii").strip()
        if name in {"proxy-authorization", "authorization", "proxy-authenticate"} or "@" in value:
            raise ValueError("credentials are not allowed")


def relay(
    left: socket.socket, right: socket.socket, idle_timeout: float = DEFAULT_IDLE_TIMEOUT
) -> tuple[int, int]:
    total = [0, 0]
    left.settimeout(None)
    right.settimeout(None)
    while True:
        ready, _, _ = select.select((left, right), (), (), idle_timeout)
        if not ready:
            return tuple(total)
        for source in ready:
            chunk = source.recv(65536)
            if not chunk:
                return tuple(total)
            target = right if source is left else left
            target.sendall(chunk)
            total[0 if source is left else 1] += len(chunk)


class Proxy:
    def __init__(
        self,
        port: int,
        idle_timeout: float = DEFAULT_IDLE_TIMEOUT,
        ready_file: Path | None = None,
    ):
        self.port = port
        self.idle_timeout = idle_timeout
        self.ready_file = ready_file
        self.stop = threading.Event()
        self.listener: socket.socket | None = None
        self.slots = threading.BoundedSemaphore(MAX_CLIENTS)

    def publish_ready(self) -> None:
        """Atomically publish the owning PID only after the listener is bound."""
        if self.ready_file is None:
            return
        temporary = self.ready_file.with_name(
            f"{self.ready_file.name}.{os.getpid()}.tmp"
        )
        with temporary.open("x", encoding="ascii", newline="\n") as handle:
            handle.write(f"{os.getpid()}\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, self.ready_file)

    def log(self, kind: str, **fields: object) -> None:
        # Never log URLs, headers, payloads, or credentials.
        record = {"ts": int(time.time()), "kind": kind, **fields}
        print(json.dumps(record, separators=(",", ":")), file=sys.stderr, flush=True)

    def handle(self, client: socket.socket, peer: tuple[str, int]) -> None:
        connection_id = uuid.uuid4().hex
        upstream = None
        established = False
        try:
            if peer[0] != "127.0.0.1":
                raise PermissionError("loopback only")
            client.settimeout(HEADER_TIMEOUT)
            data = b""
            while b"\r\n\r\n" not in data:
                data += client.recv(min(2048, MAX_HEADER + 1 - len(data)))
                if not data or len(data) > MAX_HEADER:
                    raise ValueError("invalid headers")
            parse_connect(data)
            upstream = socket.create_connection(ALLOW, CONNECT_TIMEOUT)
            client.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")
            established = True
            remainder = data.split(b"\r\n\r\n", 1)[1]
            if remainder:
                upstream.sendall(remainder)
            inbound, outbound = relay(client, upstream, self.idle_timeout)
            self.log("closed", connection_id=connection_id, bytes_in=inbound + len(remainder), bytes_out=outbound)
        except Exception as exc:
            self.log("error" if established else "rejected", connection_id=connection_id, error=type(exc).__name__)
            if not established:
                try:
                    client.sendall(b"HTTP/1.1 403 Forbidden\r\nConnection: close\r\n\r\n")
                except OSError:
                    pass
        finally:
            for sock in (client, upstream):
                if sock:
                    try:
                        sock.close()
                    except OSError:
                        pass
            self.slots.release()

    def run(self) -> None:
        with socket.socket() as listener:
            self.listener = listener
            if hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
                listener.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
            else:
                listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.bind(("127.0.0.1", self.port))
            listener.listen(MAX_CLIENTS)
            listener.settimeout(0.5)
            self.publish_ready()
            self.log("ready", bind="127.0.0.1", port=listener.getsockname()[1])
            while not self.stop.is_set():
                try:
                    client, peer = listener.accept()
                except socket.timeout:
                    continue
                if not self.slots.acquire(blocking=False):
                    client.close()
                    self.log("rejected", error="concurrency")
                    continue
                threading.Thread(target=self.handle, args=(client, peer), daemon=True).start()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--idle-timeout", type=float, default=DEFAULT_IDLE_TIMEOUT)
    parser.add_argument("--ready-file", type=Path)
    args = parser.parse_args(argv)
    if not 0 <= args.port <= 65535:
        parser.error("port must be between 0 and 65535")
    if not 60 <= args.idle_timeout <= 3600:
        parser.error("idle timeout must be between 60 and 3600 seconds")
    try:
        Proxy(args.port, args.idle_timeout, args.ready_file).run()
    except KeyboardInterrupt:
        return 130
    except OSError as exc:
        print(f"proxy failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
