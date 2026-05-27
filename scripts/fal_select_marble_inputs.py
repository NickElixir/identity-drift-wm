#!/usr/bin/env python3
"""Select Marble input photos with fal OpenRouter Vision."""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


FAL_QUEUE_URL = "https://queue.fal.run/openrouter/router/vision"
PRIMARY_MODEL = "openai/gpt-4o"
FALLBACK_MODEL = "google/gemini-2.5-flash"

SATELLITE_LAYOUT = """Satellite layout reference from the user's Yandex Maps screenshot:
- The target space is a central green courtyard inside/along Skoltech at Bolshoy Boulevard 30c1.
- Long white roof/building strips surround the courtyard.
- A curved wood/glass building edge borders one side.
- The useful scene should cover the courtyard as a path-planning environment: lawn, open paved/cobblestone paths, colonnade/glass facade, white ribbed facade, and pass-through/underpass connections.
- Do not optimize for nearby parking, roadside cars, or bike storage.
"""


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
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def request_json(method: str, url: str, fal_key: str, payload: dict | None = None) -> dict:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Authorization": f"Key {fal_key}"}
    if payload is not None:
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {url} failed: HTTP {exc.code}\n{details}") from exc


def poll_result(submit: dict, fal_key: str, poll_seconds: int, timeout_minutes: int) -> dict:
    request_id = submit["request_id"]
    status_url = submit["status_url"]
    response_url = submit["response_url"]
    deadline = time.time() + timeout_minutes * 60
    while time.time() < deadline:
        status = request_json("GET", status_url, fal_key)
        state = status.get("status")
        print(f"{request_id}: {state}", flush=True)
        if state == "COMPLETED":
            return request_json("GET", response_url, fal_key)
        if state in {"FAILED", "CANCELLED"}:
            raise RuntimeError(json.dumps(status, ensure_ascii=False, indent=2))
        time.sleep(poll_seconds)
    raise TimeoutError(f"fal request timed out: {request_id}")


def extract_json(text: str) -> dict:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", stripped, flags=re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0))


def manifest_text(path: Path | None) -> str:
    if not path:
        return ""
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines()[1:]:
        index, file_path, _sheet, _label = line.split(",", 3)
        rows.append(f"{index}: {file_path}")
    return "Exact dataset manifest. Use only these indices and file paths:\n" + "\n".join(rows)


def build_prompt(mode: str, manifest: str) -> str:
    if mode == "smoke":
        return f"""{SATELLITE_LAYOUT}

{manifest}

You are checking whether this contact sheet can be used for Marble world input selection.
Return strict JSON only with keys:
- sheet_summary: string
- best_candidate_indices: array of up to 5 integers
- reject_indices: array of integers
- notes: string

Prefer central Skoltech courtyard photos useful for drone path-planning. Reject parking, bikes, humans, and near-duplicates.
"""

    return f"""{SATELLITE_LAYOUT}

{manifest}

Task: choose the best 5 REAL courtyard photos from the contact sheets for a first Marble world generation aimed at drone path-planning and VR/Oculus demo.

You will see:
1. A generated Reve anchor image showing desired object placement.
2. Five indexed contact sheets from the private VR Dataset.

Return strict JSON only with this schema:
{{
  "selected": [
    {{
      "index": 23,
      "file": "VR Dataset/IMG_20260527_154723.jpg",
      "zone": "colonnade_glass_wood_facade",
      "why": "short reason",
      "risk": "short risk"
    }}
  ],
  "backup_candidates": [
    {{"index": 0, "file": "...", "zone": "...", "why": "..."}}
  ],
  "rejected_duplicate_groups": [
    {{"indices": [23, 24, 25], "keep": 23, "reason": "short reason"}}
  ],
  "rejected_categories": {{
    "parking_or_road": [66, 67],
    "bikes": [103],
    "humans": [49],
    "not_courtyard": [1]
  }},
  "overall_rationale": "short rationale"
}}

Selection requirements:
- Select exactly 5 real photos from VR Dataset, not the generated anchor.
- Every selected item must use an exact index and exact file path from the manifest above.
- Never invent file paths. Never output index 0.
- Cover these zones with minimal duplication:
  1. colonnade/glass/wood facade,
  2. central lawn/courtyard,
  3. open paved plaza/white ribbed facade,
  4. underpass/pass-through,
  5. route continuation/opposite side.
- Prefer images with overlap to neighboring selected views, but avoid choosing multiple frames from the same short camera position.
- Reject parking, cars-only photos, bike storage, people, and photos unrelated to the central courtyard.
- The final set will be combined with the Reve anchor as the first Marble input image.
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sheets", nargs="+", type=Path, required=True)
    parser.add_argument("--anchor", type=Path)
    parser.add_argument("--manifest", type=Path, default=Path("analysis/contact_sheets/vr_dataset/manifest.csv"))
    parser.add_argument("--model", default=PRIMARY_MODEL)
    parser.add_argument("--fallback-model", default=FALLBACK_MODEL)
    parser.add_argument("--mode", choices=["smoke", "full"], default="full")
    parser.add_argument("--out-dir", type=Path, default=Path("results/vlm_selection"))
    parser.add_argument("--poll-seconds", type=int, default=3)
    parser.add_argument("--timeout-minutes", type=int, default=10)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    load_dotenv(Path(".env"))
    fal_key = os.environ.get("FAL_KEY")
    if not fal_key and not args.dry_run:
        print("Set FAL_KEY before running this script.", file=sys.stderr)
        return 2

    image_paths: list[Path] = []
    if args.mode == "full":
        if not args.anchor:
            print("--anchor is required in full mode", file=sys.stderr)
            return 2
        image_paths.append(args.anchor.expanduser().resolve())
    image_paths.extend(sheet.expanduser().resolve() for sheet in args.sheets)
    for path in image_paths:
        if not path.exists():
            print(f"Image not found: {path}", file=sys.stderr)
            return 2

    prompt = build_prompt(args.mode, manifest_text(args.manifest))
    payload = {
        "image_urls": ["<data-url-redacted>" for _ in image_paths],
        "prompt": prompt,
        "system_prompt": "Return strict JSON only. Do not use markdown.",
        "model": args.model,
        "temperature": 0,
        "max_tokens": 2500 if args.mode == "full" else 1000,
    }
    if args.dry_run:
        print(json.dumps({"images": [str(path) for path in image_paths], "payload": payload}, indent=2))
        return 0

    payload["image_urls"] = [data_url(path) for path in image_paths]
    errors = []
    result = None
    used_model = args.model
    for model in [args.model, args.fallback_model]:
        payload["model"] = model
        try:
            submit = request_json("POST", FAL_QUEUE_URL, fal_key, payload)
            print(f'{submit["request_id"]}: submitted model={model}', flush=True)
            result = poll_result(submit, fal_key, args.poll_seconds, args.timeout_minutes)
            used_model = model
            break
        except Exception as exc:
            errors.append(f"{model}: {exc}")
            print(f"model failed: {model}: {exc}", file=sys.stderr)
    if result is None:
        print("\n".join(errors), file=sys.stderr)
        return 1

    output_text = result.get("output", "")
    parsed = extract_json(output_text)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    out = args.out_dir / f"marble_input_selection_{args.mode}_{stamp}.json"
    record = {
        "mode": args.mode,
        "model": used_model,
        "images": [str(path) for path in image_paths],
        "result": result,
        "parsed": parsed,
    }
    out.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    print(out)
    print(json.dumps(parsed, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
