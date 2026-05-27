# Marble Result: Skoltech HoverAI Reve Side-Face Rerun

Date: 2026-05-28

## Result

- Operation: `16881893-855f-4b7c-9125-aad1afab6e2f`
- Status: `SUCCEEDED`
- Model: `marble-1.1`
- Credits: `1600`
- World: https://marble.worldlabs.ai/world/e142c27a-1e8b-4f4e-bef5-24d52d1623b1
- Collider mesh: https://cdn.marble.worldlabs.ai/e142c27a-1e8b-4f4e-bef5-24d52d1623b1/232ec5bc.glb
- Panorama: https://cdn.marble.worldlabs.ai/e142c27a-1e8b-4f4e-bef5-24d52d1623b1/af54a366-d99c-4d68-8435-ae9bfab6215a_panos/rgb_0.png
- Thumbnail: https://cdn.marble.worldlabs.ai/e142c27a-1e8b-4f4e-bef5-24d52d1623b1/2a206685-1040-48c3-8450-c9fc9cf4227b_sand_mpi/thumbnail.webp

Raw operation records were appended locally to
`results/marble_api_runs.jsonl`.

## Input

Generated from the 7-image car-orbit set:

1. `results/marble_inputs/skoltech_hoverai_reve_anchor_4x3.png`
2. `results/marble_inputs/skoltech_hoverai_car_rear_right_reference.png`
3. `results/marble_inputs/skoltech_hoverai_reve_side_face_car_reference.png`
4. `VR Dataset/IMG_20260527_154723.jpg`
5. `VR Dataset/IMG_20260527_154804.jpg`
6. `VR Dataset/IMG_20260527_154855.jpg`
7. `VR Dataset/IMG_20260527_154948.jpg`

Prompt:

```text
prompts/marble_skoltech_hoverai_scene_car_orbit.txt
```

## Quick QA

Status: `quick_mixed`

Observed from generated CDN thumbnail and panorama:

- Courtyard geometry, cobblestone paths, columns, glass facade, white ribbed
  facades, and lawn are coherent.
- The nearest yellow car on the right is much cleaner than in the first result
  and looks more usable for an orbit/walkaround test.
- The main cobblestone route appears open.
- The face sculpture is present but drifts into a more abstract ribbed vertical
  object instead of preserving the side-face identity.
- Marble appears to duplicate the yellow car: one close car near the columns and
  another yellow car near the sculpture/open plaza.

Before using this as the demo asset, manually open the world and check whether
the closest car can be approached/orbited and whether the duplicate distant car
is acceptable or distracting.
