# Marble Generation Handoff: Skoltech HoverAI Demo Plaza

Date: 2026-05-28

## Objective

Generate the first working Marble 3D scene for the Skoltech central courtyard
demo. The goal is path-planning / VR-Oculus demo readiness for the HoverAI drone
project, not identity-drift research yet.

Do not optimize for exact object identity in this first run. Optimize for a
navigable, coherent courtyard with recognizable Skoltech geometry, clear
cobblestone corridors, columns, lawn, white ribbed facades, pass-through context,
and a plausible sculpture/car demo setup.

## Safety / External State

- Running `scripts/marble_generate_world.py` calls World Labs `worlds:generate`
  and spends Marble/API credits.
- Do not run Marble generation unless the user explicitly approves the spend.
- If generation starts and then crashes, assume an operation may already exist.
  Check World Labs Platform or poll the operation before retrying.
- Local private data is under `VR Dataset/` and must stay untracked.

## Final Input Set For User Approval

Use exactly these 6 images, in this order:

1. `results/marble_inputs/skoltech_hoverai_reve_anchor_4x3.png`
   - Reve edited anchor.
   - Contains intended object placement: yellow demo car and abstract sculpture.
   - Normalized to 4:3, 1168x876, 1.45 MB.
2. `VR Dataset/IMG_20260527_154723.jpg`
   - Colonnade / glass / curved wood facade.
   - 2592x1944, 1.98 MB.
3. `VR Dataset/IMG_20260527_154804.jpg`
   - Central lawn / courtyard path.
   - 2592x1944, 1.98 MB.
4. `VR Dataset/IMG_20260527_154855.jpg`
   - Open plaza / white ribbed facade / pass-through direction.
   - 2592x1944, 1.93 MB.
5. `VR Dataset/IMG_20260527_154948.jpg`
   - Route continuation along white facade.
   - 2592x1944, 2.11 MB.
6. `VR Dataset/IMG_20260527_154615.jpg`
   - Opposite/wood-side shaded pass-through context.
   - 4608x3456, 5.38 MB.

Rationale: this set avoids the earlier near-duplicate cluster and covers a more
useful path-planning route through the courtyard while keeping overlap between
adjacent views.

## Prompt

Prompt file:

```text
prompts/marble_skoltech_hoverai_scene.txt
```

The prompt is 1263 characters and intentionally excludes bicycles:

```text
Create a realistic navigable outdoor courtyard at Skoltech in Skolkovo. Use the uploaded photos as the main geometry: grey cobblestone paving, curved wood-clad building edge on concrete columns, dark glass entrance facade, white ribbed campus buildings, broad open paths, green lawn, evergreen landscaping, low shrubs, and an underpass-like passage between buildings. Preserve the clean modern research-campus atmosphere and consistent overcast daylight.

Adapt the courtyard into a robotics demonstration plaza. Add a few realistic Skolkovo-style exhibits without crowding the space: a large fragmented stone-like face sculpture with vertical ribs, a minimal black square/cube public-art landmark, and a yellow autonomous taxi-style demo car.

Place the fragmented face sculpture on the lawn side near the open plaza, visible from the main cobblestone path. Place the yellow demo car on the paved open area near the white ribbed facade, leaving a wide clear corridor around it. Keep the central cobblestone route open for a HoverAI drone flight path from the glass entrance under the columns, around the sculpture, past the car, and toward the underpass. No people, no animals, no bicycles, no festive decorations, no snow, no extra cars blocking the main route.
```

## Marble Command

Dry-run command already passed with `type: multi-image`,
`reconstruct_images: true`, and `disable_recaption: true`.

Real generation command:

```bash
python3 scripts/marble_generate_world.py \
  "results/marble_inputs/skoltech_hoverai_reve_anchor_4x3.png" \
  "VR Dataset/IMG_20260527_154723.jpg" \
  "VR Dataset/IMG_20260527_154804.jpg" \
  "VR Dataset/IMG_20260527_154855.jpg" \
  "VR Dataset/IMG_20260527_154948.jpg" \
  "VR Dataset/IMG_20260527_154615.jpg" \
  --display-name "Skoltech HoverAI demo plaza Reve anchor" \
  --model marble-1.1 \
  --prompt-file prompts/marble_skoltech_hoverai_scene.txt \
  --disable-recaption
```

Expected output records:

- Operation start/finish JSONL: `results/marble_api_runs.jsonl`
- World URL printed by script when complete.

## How This Input Was Selected

- Initial manually selected photos were too similar.
- fal.ai image-edit candidates were generated with Seedream, Nano Banana, and
  Reve. Reve was selected as the edited anchor because it preserved courtyard
  geometry best, although the sculpture is less face-like than Seedream.
- fal Vision API was used for VLM selection:
  - `openai/gpt-4o` failed in smoke test at result retrieval with provider error.
  - fallback `google/gemini-2.5-flash` produced valid JSON.
  - a second Gemini pass with exact manifest produced valid file paths.
- VLM output was manually checked. The final set replaces weak VLM picks with a
  more coherent route/passage selection.

Local VLM results are in `results/vlm_selection/` and are ignored by git.

## QA After Generation

Use `protocols/marble_quality_check.md`.

For this demo, prioritize:

- world is navigable;
- central cobblestone route is open;
- columns and white ribbed facades are coherent enough for path planning;
- lawn/trees do not block the main route;
- sculpture/car exist and do not create major occlusions;
- no people, bicycles, or extra cars dominate the route;
- route can support a HoverAI drone path from glass entrance/columns through
  sculpture/car zone toward pass-through.

If the world fails because objects disrupt navigation, rerun with real photos
only and keep objects in text prompt. If the world is navigable but object
identity drifts, keep it for demo and postpone identity-drift work to a later
run.
