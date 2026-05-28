# Marble V3 Result: Self-Driving Car, Anton Smit, Mirror Frames

Date: 2026-05-28

## Result

- World URL: `https://marble.worldlabs.ai/world/419c6bf8-95e8-4648-87c4-bf0b0a47ca22`
- Operation ID: `c926c99e-7fd2-4312-a12e-b821bcd18a34`
- Model: `marble-1.1`
- Status: `SUCCEEDED`
- Cost: 1600 credits

## Input Set

1. `results/marble_inputs/skoltech_objects_v3/01_overview_self_driving_car_anton_mirror.png`
2. `results/marble_inputs/skoltech_objects_v3/02_self_driving_car_focus.png`
3. `results/marble_inputs/skoltech_objects_v3/06_self_driving_car_rear_seedream.png`
4. `results/marble_inputs/skoltech_objects_v3/03_anton_front_focus.png`
5. `results/marble_inputs/skoltech_objects_v3/04_anton_back_focus_repaired_nano.png`
6. `results/marble_inputs/skoltech_objects_v3/05_mirror_frame_focus.png`
7. `VR Dataset/IMG_20260527_154723.jpg`
8. `VR Dataset/IMG_20260527_154840.jpg`

Prompt:

```text
prompts/marble_skoltech_objects_v3_self_driving_car_anton_mirror.txt
```

## Quick QA From CDN Panorama

Status: `quick_mixed`

What improved:

- Skoltech courtyard geometry is coherent enough for a quick walkthrough check:
  cobblestone route, lawn, curved wood facade, white ribbed facade, and glass
  entrance are all readable.
- Self-driving car identity is stronger than the previous yellow-car runs:
  white body, black graphics, roof sensor bar, windows, and wheels are visible.
- Mirrored frame sculpture is present on the right side and reads as a
  freestanding rectangular frame object.
- Central cobblestone route appears mostly open in the panorama.

Main issues:

- Marble duplicated the self-driving car despite the prompt requesting one car.
- Anton Smit sculpture is present, but the face drifted into a black-and-white
  graphic mask on ribs rather than preserving the colorful layered material.
- Interactive walkthrough/orbit behavior still needs manual verification in
  Marble.

## Generation Notes

The first launch attempt failed before `worlds:generate` during media upload
with `BrokenPipeError`; no operation was created and no new `operation_started`
entry appeared in `results/marble_api_runs.jsonl`.

`scripts/marble_generate_world.py` was updated to retry transient upload PUT
failures. The second launch created operation
`c926c99e-7fd2-4312-a12e-b821bcd18a34` and completed successfully.
