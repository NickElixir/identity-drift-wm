#!/usr/bin/env python3
"""Poll an existing World Labs operation without creating a new generation."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


API_BASE = "https://api.worldlabs.ai/marble/v1"


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def get_json(url: str, api_key: str) -> dict:
    request = urllib.request.Request(url, headers={"WLT-Api-Key": api_key}, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GET {url} failed: HTTP {exc.code}\n{details}") from exc


def operation_status(operation: dict) -> str:
    metadata = operation.get("metadata") or {}
    progress = metadata.get("progress") or {}
    return (
        progress.get("status")
        or operation.get("status")
        or ("DONE" if operation.get("done") else "PENDING")
    )


def world_from_operation(operation: dict) -> dict:
    response = operation.get("response") or {}
    return response.get("world") or response


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("operation_id")
    parser.add_argument("--poll-seconds", type=int, default=30)
    parser.add_argument("--timeout-minutes", type=int, default=45)
    parser.add_argument("--out", type=Path, default=Path("results/marble_api_runs.jsonl"))
    args = parser.parse_args()

    load_dotenv(Path(".env"))
    api_key = os.environ.get("WORLDLABS_API_KEY")
    if not api_key:
        print("Set WORLDLABS_API_KEY before running this script.", file=sys.stderr)
        return 2

    deadline = time.time() + args.timeout_minutes * 60
    operation = get_json(f"{API_BASE}/operations/{args.operation_id}", api_key)
    while not operation.get("done"):
        if time.time() > deadline:
            raise TimeoutError(f"Operation timed out: {args.operation_id}")
        print(
            f"{args.operation_id}: {operation_status(operation)}; polling in {args.poll_seconds}s",
            flush=True,
        )
        time.sleep(args.poll_seconds)
        operation = get_json(f"{API_BASE}/operations/{args.operation_id}", api_key)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("a", encoding="utf-8") as handle:
        handle.write(
            json.dumps(
                {
                    "event": "operation_polled",
                    "operation_id": args.operation_id,
                    "operation": operation,
                },
                ensure_ascii=False,
            )
            + "\n"
        )

    if operation.get("error"):
        print(json.dumps(operation["error"], indent=2), file=sys.stderr)
        return 1

    world = world_from_operation(operation)
    world_id = world.get("world_id") or world.get("id")
    world_url = world.get("world_marble_url")
    if not world_url and world_id:
        world_url = f"https://marble.worldlabs.ai/world/{world_id}"
    print(world_url or json.dumps(world, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
