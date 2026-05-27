# Marble Result: Skoltech HoverAI Demo Plaza

Date: 2026-05-28

## Result

- Operation: `95684ef4-9dd6-4c74-a033-37307d2df909`
- Status: `SUCCEEDED`
- Model: `marble-1.1`
- Credits: `1600`
- World: https://marble.worldlabs.ai/world/4b3aac0a-422b-4306-9c4b-73d47e0e170c
- Collider mesh: https://cdn.marble.worldlabs.ai/4b3aac0a-422b-4306-9c4b-73d47e0e170c/bdd63f65.glb
- Panorama: https://cdn.marble.worldlabs.ai/4b3aac0a-422b-4306-9c4b-73d47e0e170c/ba594720-4ae9-431d-b68b-6689f4f35d81_panos/rgb_0.png
- Thumbnail: https://cdn.marble.worldlabs.ai/4b3aac0a-422b-4306-9c4b-73d47e0e170c/e3cdca5c-fb9b-406e-b24a-433dd2063f58_sand_mpi/thumbnail.webp

The raw operation records were appended locally to
`results/marble_api_runs.jsonl`.

## Input

Generated from the final six-image set documented in
`docs/MARBLE_GENERATION_HANDOFF_2026-05-28.md`, using
`prompts/marble_skoltech_hoverai_scene.txt`.

## Quick QA

Status: `quick_mixed`

Observed from the generated CDN thumbnail and panorama:

- The Skoltech-like courtyard is visually coherent.
- The cobblestone route, columns, curved wood facade, glass edge, and white
  ribbed facades are recognizable.
- The large face sculpture and yellow demo car are present.
- The main route appears open enough for the HoverAI path-planning demo.
- No people, bicycles, or extra blocking cars dominate the visible route.

Limitation: interactive Marble viewer walkthrough was not completed in this
environment because the in-app browser target was unavailable. Before using this
as the final demo asset, open the world in Marble and verify walk/orbit
navigation, route continuity under the columns, and whether the collider mesh is
usable for ROS2/OMPL planning.
