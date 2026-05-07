#!/usr/bin/env python3
"""Basic MCP ABAP connection validator for TRM."""

from __future__ import annotations

import argparse
import os
import socket
import sys
from pathlib import Path


REQUIRED_KEYS = ("SAP_HOST", "SAP_PORT", "SAP_CLIENT", "SAP_USERNAME")


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        raw = line.strip()
        if not raw or raw.startswith("#") or "=" not in raw:
            continue
        key, value = raw.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate MCP ABAP connection settings")
    parser.add_argument("--from-env", action="store_true", help="Load variables from .env file")
    parser.add_argument("--host", help="SAP host")
    parser.add_argument("--port", help="SAP port")
    parser.add_argument("--client", help="SAP client")
    parser.add_argument("--user", help="SAP username")
    parser.add_argument("--timeout", type=float, default=5.0, help="TCP timeout in seconds")
    return parser.parse_args()


def get_config(args: argparse.Namespace) -> dict[str, str]:
    if args.from_env:
        load_env_file(Path(".env"))

    cfg = {
        "SAP_HOST": args.host or os.getenv("SAP_HOST", ""),
        "SAP_PORT": args.port or os.getenv("SAP_PORT", ""),
        "SAP_CLIENT": args.client or os.getenv("SAP_CLIENT", ""),
        "SAP_USERNAME": args.user or os.getenv("SAP_USERNAME", ""),
    }
    return cfg


def validate_required(cfg: dict[str, str]) -> list[str]:
    missing = [k for k in REQUIRED_KEYS if not cfg.get(k)]
    if missing:
        return [f"Missing required variable(s): {', '.join(missing)}"]

    errors: list[str] = []
    if not cfg["SAP_PORT"].isdigit():
        errors.append("SAP_PORT must be numeric")

    if not cfg["SAP_CLIENT"].isdigit() or len(cfg["SAP_CLIENT"]) not in (2, 3):
        errors.append("SAP_CLIENT should be a 2-3 digit SAP client value")

    return errors


def check_tcp(host: str, port: int, timeout: float) -> tuple[bool, str]:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True, f"TCP connectivity OK: {host}:{port}"
    except Exception as exc:  # noqa: BLE001 - broad for clear CLI output
        return False, f"TCP connectivity FAILED: {host}:{port} ({exc})"


def main() -> int:
    args = parse_args()
    cfg = get_config(args)

    errors = validate_required(cfg)
    if errors:
        for err in errors:
            print(f"ERROR: {err}")
        return 1

    print("Configuration check OK")
    print(f"- SAP_HOST={cfg['SAP_HOST']}")
    print(f"- SAP_PORT={cfg['SAP_PORT']}")
    print(f"- SAP_CLIENT={cfg['SAP_CLIENT']}")
    print(f"- SAP_USERNAME={cfg['SAP_USERNAME']}")

    ok, message = check_tcp(cfg["SAP_HOST"], int(cfg["SAP_PORT"]), args.timeout)
    print(message)
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
