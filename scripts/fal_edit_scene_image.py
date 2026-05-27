#!/usr/bin/env python3
"""Create an edited scene image through fal.ai image-edit models."""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


FAL_QUEUE_BASE = "https://queue.fal.run"
DEFAULT_MODEL = "fal-ai/bytedance/seedream/v4/edit"


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def data_url(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{payload}"


def request_json(method: str, url: str, fal_key: str, payload: dict | None = None) -> dict:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Authorization": f"Key {fal_key}"}
    if payload is not None:
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {url} failed: HTTP {exc.code}\n{details}") from exc


def download(url: str, out: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=300) as response:
        out.write_bytes(response.read())


def build_input_payload(args: argparse.Namespace, prompt: str, image_urls: list[str]) -> dict:
    if "nano-banana" in args.model:
        input_payload = {
            "prompt": prompt,
            "num_images": args.num_images,
            "aspect_ratio": "auto",
            "output_format": "png",
            "safety_tolerance": "4",
            "limit_generations": True,
            "image_urls": image_urls,
        }
    elif "reve" in args.model and "remix" in args.model:
        input_payload = {
            "prompt": prompt,
            "image_urls": image_urls,
            "aspect_ratio": "4:3",
            "num_images": args.num_images,
            "output_format": "png",
        }
    else:
        input_payload = {
            "prompt": prompt,
            "image_size": args.image_size,
            "num_images": args.num_images,
            "max_images": args.max_images,
            "enable_safety_checker": True,
            "enhance_prompt_mode": "standard",
            "image_urls": image_urls,
        }

    if args.seed is not None:
        input_payload["seed"] = args.seed
    return input_payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("images", nargs="+", type=Path)
    parser.add_argument("--prompt-file", type=Path, required=True)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--image-size", default="auto")
    parser.add_argument("--num-images", type=int, default=1)
    parser.add_argument("--max-images", type=int, default=1)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--out-dir", type=Path, default=Path("results/fal_edits"))
    parser.add_argument("--poll-seconds", type=int, default=5)
    parser.add_argument("--timeout-minutes", type=int, default=15)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    load_dotenv(Path(".env"))
    fal_key = os.environ.get("FAL_KEY")
    if not fal_key and not args.dry_run:
        print("Set FAL_KEY before running this script.", file=sys.stderr)
        return 2

    image_paths = [path.expanduser().resolve() for path in args.images]
    for path in image_paths:
        if not path.exists():
            print(f"Image not found: {path}", file=sys.stderr)
            return 2
    if len(image_paths) > 10:
        print("Seedream edit accepts up to 10 input images.", file=sys.stderr)
        return 2

    prompt = args.prompt_file.expanduser().read_text(encoding="utf-8").strip()
    input_payload = build_input_payload(
        args,
        prompt,
        ["<data-url-redacted>" for _ in image_paths],
    )

    if args.dry_run:
        print(
            json.dumps(
                {
                    "model": args.model,
                    "images": [str(path) for path in image_paths],
                    "input": input_payload,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    input_payload = build_input_payload(args, prompt, [data_url(path) for path in image_paths])
    submit = request_json("POST", f"{FAL_QUEUE_BASE}/{args.model}", fal_key, input_payload)
    request_id = submit["request_id"]
    status_url = submit["status_url"]
    response_url = submit["response_url"]
    print(f"{request_id}: submitted", flush=True)

    deadline = time.time() + args.timeout_minutes * 60
    while time.time() < deadline:
        status = request_json("GET", status_url, fal_key)
        state = status.get("status")
        print(f"{request_id}: {state}", flush=True)
        if state == "COMPLETED":
            break
        if state in {"FAILED", "CANCELLED"}:
            print(json.dumps(status, ensure_ascii=False, indent=2), file=sys.stderr)
            return 1
        time.sleep(args.poll_seconds)
    else:
        raise TimeoutError(f"fal request timed out: {request_id}")

    result = request_json("GET", response_url, fal_key)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / f"{request_id}.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    for index, image in enumerate(result.get("images", []), start=1):
        url = image["url"]
        suffix = Path(url.split("?", 1)[0]).suffix or ".jpg"
        out_path = args.out_dir / f"{request_id}_{index:02d}{suffix}"
        download(url, out_path)
        print(out_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
