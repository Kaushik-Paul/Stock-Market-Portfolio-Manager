"""Keep non-JSON output from corrupting an MCP stdio connection."""

import json
import os
import signal
import subprocess
import sys
import threading
from collections.abc import Sequence
from typing import BinaryIO


def _forward_stdin(source: BinaryIO, destination: BinaryIO) -> None:
    try:
        while chunk := os.read(source.fileno(), 65536):
            destination.write(chunk)
            destination.flush()
    except (BrokenPipeError, OSError):
        pass
    finally:
        try:
            destination.close()
        except OSError:
            pass


def _is_jsonrpc_message(line: bytes) -> bool:
    try:
        message = json.loads(line)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return False
    return isinstance(message, dict) and message.get("jsonrpc") == "2.0"


def proxy_stdio(command: Sequence[str]) -> int:
    if not command:
        print(
            "Usage: python -m main.mcp_servers.stdio_proxy COMMAND [ARG ...]",
            file=sys.stderr,
        )
        return 2

    try:
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=None,
            bufsize=0,
        )
    except OSError as exc:
        print(f"Unable to start MCP server: {exc}", file=sys.stderr)
        return 1

    assert process.stdin is not None
    assert process.stdout is not None

    def forward_signal(signum: int, _frame: object) -> None:
        try:
            process.send_signal(signum)
        except ProcessLookupError:
            pass

    signal.signal(signal.SIGINT, forward_signal)
    signal.signal(signal.SIGTERM, forward_signal)

    threading.Thread(
        target=_forward_stdin,
        args=(sys.stdin.buffer, process.stdin),
        daemon=True,
    ).start()

    for line in iter(process.stdout.readline, b""):
        if _is_jsonrpc_message(line):
            sys.stdout.buffer.write(line)
            sys.stdout.buffer.flush()
        elif line.strip():
            sys.stderr.buffer.write(line)
            sys.stderr.buffer.flush()

    return process.wait()


if __name__ == "__main__":
    raise SystemExit(proxy_stdio(sys.argv[1:]))
