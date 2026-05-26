#!/usr/bin/env python3
"""Extract reproducible orbit-evaluation frames from a walkthrough video."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import cv2


DEFAULT_LABELS = [
    "front_or_input_like",
    "front_left",
    "left",
    "rear_left",
    "rear",
    "rear_right",
    "right",
    "front_right",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--out-dir", type=Path, default=Path("results/extracted_frames"))
    parser.add_argument("--start", type=float, default=0.05, help="Start fraction of video duration.")
    parser.add_argument("--end", type=float, default=0.95, help="End fraction of video duration.")
    parser.add_argument("--count", type=int, default=8)
    args = parser.parse_args()

    video_path = args.video.expanduser().resolve()
    if not video_path.exists():
        raise FileNotFoundError(video_path)

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = frame_count / fps if fps else 0
    if not duration:
        raise RuntimeError("Could not determine video duration.")

    out_dir = args.out_dir / args.run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    labels = DEFAULT_LABELS if args.count == 8 else [f"frame_{i + 1:02d}" for i in range(args.count)]
    for index in range(args.count):
        if args.count == 1:
            fraction = (args.start + args.end) / 2
        else:
            fraction = args.start + (args.end - args.start) * index / (args.count - 1)
        timestamp = duration * fraction
        frame_index = min(frame_count - 1, max(0, round(timestamp * fps)))
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ok, frame = cap.read()
        if not ok:
            raise RuntimeError(f"Could not read frame {frame_index} at {timestamp:.2f}s")

        frame_path = out_dir / f"{args.run_id}_{index + 1:02d}_{labels[index]}.jpg"
        cv2.imwrite(str(frame_path), frame, [int(cv2.IMWRITE_JPEG_QUALITY), 92])
        rows.append(
            {
                "run_id": args.run_id,
                "frame_index": index + 1,
                "label": labels[index],
                "timestamp_sec": f"{timestamp:.3f}",
                "video_frame": frame_index,
                "frame_path": str(frame_path),
            }
        )

    cap.release()

    manifest_path = out_dir / "frames_manifest.csv"
    with manifest_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    metadata_path = out_dir / "video_metadata.json"
    metadata_path.write_text(
        json.dumps(
            {
                "video": str(video_path),
                "run_id": args.run_id,
                "fps": fps,
                "frame_count": frame_count,
                "duration_sec": duration,
                "width": width,
                "height": height,
                "start_fraction": args.start,
                "end_fraction": args.end,
                "count": args.count,
                "manifest": str(manifest_path),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(manifest_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
