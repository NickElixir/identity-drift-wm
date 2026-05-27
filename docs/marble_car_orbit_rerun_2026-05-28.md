# Marble Car Orbit Rerun Prep

Date: 2026-05-28

## Goal

Improve the Skoltech HoverAI Marble scene so the yellow demo car is more usable
as a complete object that can be approached and orbited. The previous world is
good enough spatially, but the car degrades from alternate views and appears
partly smeared into the surrounding reconstruction.

## New Generated Reference

Generated a new photorealistic rear-right / side reference image:

```text
results/marble_inputs/skoltech_hoverai_car_rear_right_reference.png
```

Image properties:

- 1536x1024 PNG
- yellow taxi-style crossover visible from rear-right three-quarter angle
- clear cobblestone space around the car
- Skoltech-like white ribbed facade, wood overhang, concrete columns, and glass
  facade in the background

This image is intended as the second input after the existing Reve anchor, so
Marble sees both a front/three-quarter view and a rear/side view of the same car.

Generated one additional Reve remix reference for the sculpture side profile and
car orbit composition:

```text
results/marble_inputs/skoltech_hoverai_reve_side_face_car_reference.png
```

This replaces the weaker shaded scene-only photo
`VR Dataset/IMG_20260527_154615.jpg` in the next Marble dry run. It preserves
the liked side-face composition while cleaning up the car and leaving clearer
walkable pavement around it.

## Prompt

Use:

```text
prompts/marble_skoltech_hoverai_scene_car_orbit.txt
```

This prompt makes the car the primary object, asks for one consistent complete
3D vehicle, and explicitly requests clear walkable space around all sides.

## Dry Run

Dry-run passed with `type: multi-image`, `reconstruct_images: true`, and
`disable_recaption: true`.

## Real Generation Command

Run only after confirming Marble credit spend:

```bash
python3 scripts/marble_generate_world.py \
  "results/marble_inputs/skoltech_hoverai_reve_anchor_4x3.png" \
  "results/marble_inputs/skoltech_hoverai_car_rear_right_reference.png" \
  "results/marble_inputs/skoltech_hoverai_reve_side_face_car_reference.png" \
  "VR Dataset/IMG_20260527_154723.jpg" \
  "VR Dataset/IMG_20260527_154804.jpg" \
  "VR Dataset/IMG_20260527_154855.jpg" \
  "VR Dataset/IMG_20260527_154948.jpg" \
  --display-name "Skoltech HoverAI demo plaza car orbit Reve side face" \
  --model marble-1.1 \
  --prompt-file prompts/marble_skoltech_hoverai_scene_car_orbit.txt \
  --disable-recaption
```

Expected QA focus:

- car visible and complete from multiple sides;
- enough clearance to walk/orbit around the car;
- no extra cars;
- car not smeared into pavement, glass, bushes, or building facade;
- route under columns and toward pass-through remains navigable.
