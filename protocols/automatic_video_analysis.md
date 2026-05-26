# Automatic Video Analysis

## Goal

Produce a reproducible, defensible analysis of a Marble walkthrough in under one
hour.

## Recommended pipeline

1. Extract 8 deterministic frames from the walkthrough video.
2. Score each frame with a fixed VLM rubric.
3. Use human review only to confirm obvious failures and choose screenshots for
   slides.

## Why this pipeline

Pixel metrics such as SSIM or pHash are weak for orbit videos because the camera
view changes. They can still be reported for the input-like frame, but they
should not be the main claim for side/rear views.

VLM scoring is not fully objective, but it is reproducible if the same model,
temperature, prompt, input image, and frame set are recorded. It also measures
the actual research construct more directly: whether the car identity, wheels,
body shape, and color are preserved.

## Commands

Extract frames:

```bash
python3 scripts/extract_orbit_frames.py \
  "/Users/nikolai/Documents/Skoltech/VR&AR&Haptics/haval_f7_1.mov" \
  --run-id car_01
```

Create a VLM review batch:

```bash
python3 scripts/make_vlm_review_batch.py \
  --reference inputs/dw_ai_2d/car_01.png \
  --manifest results/extracted_frames/car_01/frames_manifest.csv \
  --out results/vlm_batches/car_01_review.jsonl
```

The JSONL file contains base64-encoded images and is treated as a local
submission artifact rather than a git-tracked result.

## Current recording note

`haval_f7_1.mov` was recorded as a practical walkthrough, not a perfect
constant-radius orbit. Uniform extraction still gives a reproducible sample, but
frames 7-8 are more top-down/world-view than strict car-orbit views. Treat this
as the first automated walkthrough analysis, and record a tighter orbit if the
defense needs cleaner frame-to-frame comparison.

## Limitations

- Uniform frame extraction assumes the recording covers the orbit at roughly
  steady pace. If the video contains long setup or UI pauses, set `--start` and
  `--end` manually.
- VLM scores can vary by provider and model version. Record model name, date,
  and prompt.
- VLMs may over-focus on scene aesthetics. The rubric explicitly asks it to
  evaluate the target car identity.
- Full-frame SSIM/pHash are confounded by camera pose, UI overlays, and
  background changes.
- No automatic method replaces the need to show representative frames in the
  defense slides.
