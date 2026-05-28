#!/usr/bin/env python3
"""Generate a Marble world from local image input via the World Labs API."""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import socket
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
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def request_json(method: str, url: str, api_key: str, payload: dict | None = None) -> dict:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"WLT-Api-Key": api_key}
    if payload is not None:
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {url} failed: HTTP {exc.code}\n{details}") from exc


def upload_file(upload_url: str, required_headers: dict, image_path: Path) -> None:
    content_type = mimetypes.guess_type(image_path.name)[0] or "application/octet-stream"
    headers = dict(required_headers or {})
    headers.setdefault("Content-Type", content_type)
    payload = image_path.read_bytes()
    last_error: Exception | None = None

    for attempt in range(1, 4):
        request = urllib.request.Request(
            upload_url,
            data=payload,
            headers=headers,
            method="PUT",
        )
        try:
            with urllib.request.urlopen(request, timeout=300) as response:
                if response.status >= 300:
                    raise RuntimeError(f"Upload failed: HTTP {response.status}")
                return
        except urllib.error.HTTPError as exc:
            details = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Upload failed: HTTP {exc.code}\n{details}") from exc
        except (BrokenPipeError, TimeoutError, socket.timeout, urllib.error.URLError) as exc:
            last_error = exc
            if attempt == 3:
                break
            time.sleep(2**attempt)

    raise RuntimeError(f"Upload failed after retries: {image_path}") from last_error


def media_asset_id_from_response(prepared: dict) -> str:
    media_asset = prepared.get("media_asset") or {}
    media_asset_id = (
        media_asset.get("id")
        or media_asset.get("media_asset_id")
        or prepared.get("media_asset_id")
        or prepared.get("id")
    )
    if media_asset_id:
        return media_asset_id

    safe_prepared = dict(prepared)
    if "upload_info" in safe_prepared:
        upload_info = dict(safe_prepared["upload_info"] or {})
        if "upload_url" in upload_info:
            upload_info["upload_url"] = "<redacted>"
        safe_prepared["upload_info"] = upload_info
    raise KeyError(
        "Could not find media asset id in prepare_upload response:\n"
        + json.dumps(safe_prepared, indent=2)
    )


def world_from_operation(operation: dict) -> dict:
    response = operation.get("response") or {}
    if "world" in response:
        return response["world"] or {}
    return response


def operation_status(operation: dict) -> str:
    metadata = operation.get("metadata") or {}
    progress = metadata.get("progress") or {}
    return (
        progress.get("status")
        or operation.get("status")
        or ("DONE" if operation.get("done") else "PENDING")
    )


def append_jsonl(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def parse_azimuths(raw: str | None, count: int) -> list[int | None]:
    if not raw:
        return [None] * count

    values = [value.strip() for value in raw.split(",") if value.strip()]
    if len(values) != count:
        raise ValueError(f"Expected {count} azimuths, got {len(values)}")
    return [int(value) for value in values]


def media_content(media_asset_id: str) -> dict:
    return {
        "source": "media_asset",
        "media_asset_id": media_asset_id,
    }


def upload_media_asset(image_path: Path, api_key: str) -> str:
    extension = image_path.suffix.lower().lstrip(".")
    if extension == "jpeg":
        extension = "jpg"

    prepare_payload = {
        "file_name": image_path.name,
        "kind": "image",
        "extension": extension,
    }
    prepared = request_json(
        "POST",
        f"{API_BASE}/media-assets:prepare_upload",
        api_key,
        prepare_payload,
    )
    upload_info = prepared["upload_info"]
    upload_file(
        upload_info["upload_url"],
        upload_info.get("required_headers", {}),
        image_path,
    )
    return media_asset_id_from_response(prepared)


def build_world_prompt(
    media_asset_ids: list[str],
    prompt: str,
    azimuths: list[int | None],
    reconstruct_images: bool,
    disable_recaption: bool,
) -> dict:
    if len(media_asset_ids) == 1:
        world_prompt = {
            "type": "image",
            "image_prompt": {
                **media_content(media_asset_ids[0]),
            },
            "text_prompt": prompt,
        }
        if disable_recaption:
            world_prompt["disable_recaption"] = True
        return world_prompt

    multi_image_prompt = []
    for media_asset_id, azimuth in zip(media_asset_ids, azimuths):
        item = {
            "content": media_content(media_asset_id),
        }
        if azimuth is not None:
            item["azimuth"] = azimuth
        multi_image_prompt.append(item)

    world_prompt = {
        "type": "multi-image",
        "multi_image_prompt": multi_image_prompt,
        "reconstruct_images": reconstruct_images,
        "text_prompt": prompt,
    }
    if disable_recaption:
        world_prompt["disable_recaption"] = True
    return world_prompt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("images", nargs="+", type=Path)
    parser.add_argument("--display-name", required=True)
    prompt_group = parser.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument("--prompt")
    prompt_group.add_argument("--prompt-file", type=Path)
    parser.add_argument(
        "--azimuths",
        help="Comma-separated azimuths in degrees for multi-image input.",
    )
    parser.add_argument(
        "--reconstruct-images",
        action="store_true",
        help="Use Marble reconstruction mode for multi-image input; required for 5-8 images.",
    )
    parser.add_argument(
        "--disable-recaption",
        action="store_true",
        help="Ask Marble to use the provided text prompt as-is.",
    )
    parser.add_argument("--model", default="marble-1.1")
    parser.add_argument("--out", type=Path, default=Path("results/marble_api_runs.jsonl"))
    parser.add_argument("--poll-seconds", type=int, default=30)
    parser.add_argument("--timeout-minutes", type=int, default=45)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate inputs and print the request shape without uploading or generating.",
    )
    args = parser.parse_args()

    load_dotenv(Path(".env"))
    api_key = os.environ.get("WORLDLABS_API_KEY")
    if not api_key and not args.dry_run:
        print("Set WORLDLABS_API_KEY before running this script.", file=sys.stderr)
        return 2

    image_paths = [image.expanduser().resolve() for image in args.images]
    for image_path in image_paths:
        if not image_path.exists():
            print(f"Image not found: {image_path}", file=sys.stderr)
            return 2

    if len(image_paths) > 8:
        print("Marble multi-image input supports up to 8 images.", file=sys.stderr)
        return 2

    try:
        azimuths = parse_azimuths(args.azimuths, len(image_paths))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    reconstruct_images = args.reconstruct_images or len(image_paths) > 4

    if args.prompt_file:
        prompt = args.prompt_file.expanduser().read_text(encoding="utf-8").strip()
    else:
        prompt = args.prompt

    if args.dry_run:
        placeholder_ids = [f"<media_asset_id_{index + 1}>" for index in range(len(image_paths))]
        print(
            json.dumps(
                {
                    "display_name": args.display_name,
                    "model": args.model,
                    "input_images": [str(path) for path in image_paths],
                    "world_prompt": build_world_prompt(
                        placeholder_ids,
                        prompt,
                        azimuths,
                        reconstruct_images,
                        args.disable_recaption,
                    ),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    media_asset_ids = []
    for image_path in image_paths:
        media_asset_ids.append(upload_media_asset(image_path, api_key))

    generation_payload = {
        "display_name": args.display_name,
        "model": args.model,
        "world_prompt": build_world_prompt(
            media_asset_ids,
            prompt,
            azimuths,
            reconstruct_images,
            args.disable_recaption,
        ),
    }
    operation = request_json(
        "POST",
        f"{API_BASE}/worlds:generate",
        api_key,
        generation_payload,
    )

    operation_id = operation["operation_id"]
    append_jsonl(
        args.out,
        {
            "event": "operation_started",
            "input_images": [str(path) for path in image_paths],
            "display_name": args.display_name,
            "operation_id": operation_id,
            "operation": operation,
        },
    )
    print(f"{operation_id}: started", flush=True)

    deadline = time.time() + args.timeout_minutes * 60
    while not operation.get("done"):
        if time.time() > deadline:
            raise TimeoutError(f"Operation timed out: {operation_id}")
        status = operation_status(operation)
        print(f"{operation_id}: {status}; polling in {args.poll_seconds}s", flush=True)
        time.sleep(args.poll_seconds)
        operation = request_json(
            "GET",
            f"{API_BASE}/operations/{operation_id}",
            api_key,
        )

    append_jsonl(
        args.out,
        {
            "event": "operation_finished",
            "input_images": [str(path) for path in image_paths],
            "display_name": args.display_name,
            "operation_id": operation_id,
            "operation": operation,
        },
    )

    if operation.get("error"):
        print(json.dumps(operation["error"], indent=2), file=sys.stderr)
        return 1

    world = world_from_operation(operation)
    print(world.get("world_marble_url", "World generated; URL not found in response."))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
