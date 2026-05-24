# Marble Quality Check

## Purpose

Evaluate whether a generated Marble world is good enough for the identity-drift
pilot before spending time on recording and downstream metrics.

## Quick QA

Run this immediately after a Marble world is generated.

1. Open the `world_marble_url`.
2. Find the target car from the input image.
3. Check whether the car is recognizable from the best available view.
4. Check whether the wheel/rim design is close to the input image.
5. Check whether Marble added extra cars or distracting objects.
6. Check whether the car can be approached and orbited in the browser viewer.
7. Check whether the panorama view and walk view tell the same story.

Record the result in `results/marble_runs.csv`:

- `quick_pass`: usable for controlled recording.
- `quick_mixed`: useful for discussion, but not clean enough for scoring.
- `quick_fail`: do not record; adjust prompt or input.

## Controlled Recording

If quick QA passes, record one scoring walkthrough:

1. Start from the view closest to the input image.
2. Keep the target car centered and fully visible.
3. Orbit clockwise at roughly constant distance.
4. Pause at 8 positions:
   front/input-like, front-left, left, rear-left, rear, rear-right, right,
   front-right.
5. Avoid exploring the full environment during the scoring clip.
6. Save the file as `recordings/{run_id}_marble_walkthrough.mp4`.

Record a separate free-exploration video only for presentation visuals.

## First Result Notes

World:
`https://marble.worldlabs.ai/world/5519284a-551c-4dbb-a055-c7944c669109`

Observed from screenshots:

- Panorama view is strong and visually coherent.
- Target white car is recognizable from the front/right three-quarter view.
- Wheel identity is partially preserved on the visible side.
- Marble added multiple extra cars despite the prompt saying one primary car.
- Front geometry and local blur show visible identity drift.
- The world is useful as a first demonstration of identity drift, but should be
  marked `quick_mixed` unless the controlled orbit is surprisingly stable.
