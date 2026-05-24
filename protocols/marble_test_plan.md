# Marble Test Plan

## Goal
Test whether World Labs Marble preserves the visual identity of a car when a
DW AI 2D composite is converted into a navigable 3D car visualization world.

## Current plan
1. Select 4 pilot DW AI images for the free Marble tier.
2. Generate one Marble world per image using single-image input.
3. Record a controlled orbit path around the car, not a generic room tour.
4. Extract 8 frames per walkthrough at repeatable orbit positions.
5. Score identity drift against the original/DW AI input image.
6. Decide whether to upgrade to Standard for the full 10-world experiment,
   multi-image tests, and export options.

First successful world:
`https://marble.worldlabs.ai/world/5519284a-551c-4dbb-a055-c7944c669109`.
Quick status: `quick_mixed` because the target car is recognizable and the
panorama is strong, but extra cars and local front/body drift are visible.

## Marble settings
- Model: Marble 1.1 (`marble-1.1`) for the pilot. Use Marble 1.1 Plus
  (`marble-1.1-plus`) only if we specifically need a larger explorable world
  after the identity preservation test works.
- Input mode: single image
- Prompt:
  "Create a realistic outdoor dealership forecourt centered on the exact same
  car from the reference image. Preserve the car identity: same body silhouette,
  paint color, proportions, wheel/rim design, tire size, trim details, lights,
  windows, and visible damage or unique markings. Keep the car fully visible
  with clear open space around it so a camera can walk around the vehicle. Use
  neutral daylight, simple asphalt or concrete ground, subtle shadows, and a
  clean background with no visual clutter. Generate one primary car only. Avoid
  changing the car into another model, adding extra vehicles, occluding the
  wheels, cropping the car, changing the wheel design, adding readable license
  plate text, inventing large decals, or placing the vehicle indoors."
- Output needed now: screen recording plus screenshots/frames
- Output needed later: optional splat, panorama, or mesh export if Standard/Pro
  is used

## Environment strategy
- Use a fixed simple outdoor setting for all pilot worlds. This keeps the test
  closer to outdoor DW AI reference photos while preserving experimental
  consistency across cars.
- Do not ask Marble to reconstruct the exact street/background from each input
  photo in the main experiment. That is a harder task and would mix car identity
  drift with environment reconstruction drift.
- Optional presentation clip: after the scoring run, record a more exploratory
  walk through the generated world if it looks visually compelling.

## Input image strategy
- Primary research condition: single DW AI output image per car. This is the
  cleanest test of identity drift because Marble must infer unseen sides of the
  car from the same consumer image that the real product produces.
- Optional stronger visualization condition: multiple images of the same car
  from front, left, right, and back, only if all images show the same target
  wheel design and consistent lighting. This is better for making a stable
  showroom, but it changes the experiment because Marble receives more identity
  evidence.
- Do not mix real original photos with DW AI wheel composites in the same
  multi-image prompt unless the mismatch is explicitly part of the test.

## Pilot acceptance criteria
- The same car remains recognizable in at least 6 of 8 sampled views.
- Wheel design remains close to the input in at least 6 of 8 sampled views.
- No severe body-shape mutation in front, side, or rear-adjacent views.
- License plates are blurred before any public slide, screenshot, or video.

## Recording route
Use the same route for every Marble world:

1. Start at the conditioned view that most closely matches the input image.
2. Keep the car centered and fully visible.
3. Walk/orbit clockwise around the car at roughly constant distance.
4. Pause briefly at 8 positions: front/input-like, front-left, left side,
   rear-left, rear, rear-right, right side, front-right.
5. Avoid walking far into the generated world during the scoring recording.
6. Record a separate free exploration clip only for presentation visuals.

## File layout
- `inputs/dw_ai_2d/`: selected DW AI input images
- `recordings/`: Marble walkthrough videos
- `results/`: metrics and annotation tables

## Immediate run checklist
1. Put 4 selected DW AI images into `inputs/dw_ai_2d/`.
2. Open Marble on desktop.
3. For each image, create a single-image world with the prompt above.
4. Name worlds `car_01` to `car_04`.
5. Record a 360 degree walkthrough for each world.
6. Save videos as `recordings/car_01_marble_walkthrough.mp4`, etc.
7. Capture or extract 8 orbit frames per video for scoring.

## Optional API run
If `WORLDLABS_API_KEY` is available, generate a world without the Marble UI:

```bash
cp .env.example .env
# Then paste your API key into .env:
# WORLDLABS_API_KEY=...

python3 scripts/marble_generate_world.py \
  inputs/dw_ai_2d/car_01.jpg \
  --display-name car_01_marble_pilot \
  --model marble-1.1 \
  --prompt-file prompts/marble_outdoor_forecourt.txt
```

The script appends operation results to `results/marble_api_runs.jsonl` and
prints the Marble world URL when generation completes.

## Unity export note
Marble worlds can be moved into Unity, but the export path matters:

- Collider Mesh (GLB): lightweight geometry for collisions and rough spatial
  layout. Useful for quick Unity testing, but not intended as final visual
  rendering.
- High-quality Mesh (GLB): better Unity-compatible visual asset, with detailed
  geometry and texture/vertex-color variants. It can take up to an hour to
  generate and requires an export-capable plan.
- Splats (SPZ/PLY): best visual fidelity for Marble-style rendering, but Unity
  needs a Gaussian splat renderer/plugin rather than the default mesh pipeline.

For this project, use Marble browser recordings for the core experiment first.
Use Unity import only as an optional VR/AR integration step after the identity
drift pilot succeeds.
