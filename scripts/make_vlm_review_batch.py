#!/usr/bin/env python3
"""Create a JSONL batch for VLM scoring of extracted Marble frames."""

from __future__ import annotations

import argparse
import base64
import csv
import json
from pathlib import Path


RUBRIC = """You are evaluating identity preservation in a generated 3D world.
Compare the reference car image against the Marble walkthrough frame.

Return strict JSON with these keys:
- same_car_identity_1_7: integer 1-7
- wheel_identity_1_7: integer 1-7
- body_shape_1_7: integer 1-7
- color_material_1_7: integer 1-7
- target_car_visible: boolean
- extra_cars_present: boolean
- severe_occlusion_or_blur: boolean
- short_reason: one concise sentence

Scoring:
1 = completely different or not evaluable
4 = partially preserved, obvious drift
7 = strongly preserved

Focus on the target white car, not the whole scene quality."""


def data_url(path: Path) -> str:
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--model", default="gpt-4.1-mini")
    args = parser.parse_args()

    reference_url = data_url(args.reference.expanduser().resolve())
    rows = list(csv.DictReader(args.manifest.expanduser().open(encoding="utf-8")))
    args.out.parent.mkdir(parents=True, exist_ok=True)

    with args.out.open("w", encoding="utf-8") as handle:
        for row in rows:
            frame_path = Path(row["frame_path"]).expanduser().resolve()
            payload = {
                "custom_id": f'{row["run_id"]}_{row["frame_index"]}_{row["label"]}',
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": args.model,
                    "temperature": 0,
                    "response_format": {"type": "json_object"},
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": RUBRIC},
                                {"type": "text", "text": "Reference image:"},
                                {"type": "image_url", "image_url": {"url": reference_url}},
                                {
                                    "type": "text",
                                    "text": f'Marble frame {row["frame_index"]} ({row["label"]}, {row["timestamp_sec"]}s):',
                                },
                                {"type": "image_url", "image_url": {"url": data_url(frame_path)}},
                            ],
                        }
                    ],
                },
            }
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")

    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
