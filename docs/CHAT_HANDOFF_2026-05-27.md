# Chat Handoff — 2026-05-27

## Repository

- Local repo: `/Users/nikolai/Documents/GitHub/identity-drift-wm`
- Remote: `https://github.com/NickElixir/identity-drift-wm`
- Branch: `main`
- Local branch status at handoff: ahead of `origin/main` by 3 commits.
- Important local ignored files/directories:
  - `.env`
  - `.DS_Store`
  - `VR Dataset/`
  - `results/marble_api_runs.jsonl`
  - `results/vlm_batches/`
  - `scripts/__pycache__/`

## Current Research Direction

We are moving from the first car/Marble identity-drift pilot to a robotics demo:

1. Take photos of a large street/campus place.
2. Generate a virtual world in World Labs Marble.
3. Export the scene using Marble Pro.
4. Use ROS2 + OMPL for drone path planning around objects in that world.
5. Animate a HoverAI drone avatar moving along the path.
6. Optionally show the result in Oculus/VR.

The target demo should emphasize robotics usefulness: path planning, inspection,
safe navigation around obstacles, and a plausible collaboration between Marble
world generation and HoverAI.

## Marble Context

Marble Pro has been purchased to export scenes.

Known relevant export formats from Marble docs:

- `High-quality Mesh GLB`: visual rendering asset.
- `Collider Mesh GLB`: simplified collision/planning geometry.
- `Splats SPZ/PLY`: higher visual fidelity, less convenient for ROS/OMPL.
- `360 panorama`: useful for slides and quick visual inspection.

For ROS2/OMPL, use `Collider Mesh GLB`.
For presentation/VR animation, use `High-quality Mesh GLB` or a Blender/WebXR
render path.

Existing diagram:

- `docs/drone_world_pipeline.md`
- `docs/drone_world_pipeline.svg`

## New Scene Goal

Generate a Marble scene of the central plaza in the Skoltech campus using photos
from:

```text
VR Dataset/
```

This directory contains 106 local images named like:

```text
VR Dataset/IMG_20260527_154448.jpg
...
VR Dataset/IMG_20260527_160105.jpg
```

The directory was added to `.gitignore` and should not be committed.

Desired scene concept:

- Base place: central Skoltech campus square/plaza.
- Add exhibits from other Skolkovo locations:
  - cars;
  - art objects;
  - potentially campus installations.
- Existing Christmas trees in the photos may need to be removed unless they help
  spatial recognition. Current assumption: remove or de-emphasize them if they
  distract from drone navigation and exhibit placement.

Open question:

- We currently do not have local photos of art objects. Need either web search
  for Skolkovo/Skoltech public art or user-provided photos.

## Marble Input Strategy For The Next Generation

Important constraint: Marble multi-image input is best when images describe the
same physical scene with consistent scale/lighting/overlap. Do not mix central
plaza photos and unrelated object closeups as if they are the same scene unless
the goal is explicitly collage-like generation.

Recommended approach:

1. Select 4-8 best central-plaza images as Marble scene references.
2. Use prompt text to request removal/de-emphasis of unwanted seasonal objects.
3. Add exhibit concepts through prompt text first.
4. Use object photos only if Marble's selected workflow supports image editing
   or controlled object insertion; otherwise use them as visual references for
   prompt writing and presentation, not as scene input.

If the user has 8-view car photos:

- They are useful if we decide to add one specific car exhibit.
- They are not necessary for reconstructing the plaza.
- They should probably be used in a separate object/asset workflow, not mixed
  into the base plaza multi-image reconstruction.

## AITUNNEL / VLM Status

`.env` contains:

```text
WORLDLABS_API_KEY
AITUNNEL_API_KEY
AITUNNEL_BASE_URL
```

`.env.example` was updated locally to include AITUNNEL variables but is not yet
committed at this handoff.

Attempted to list models using:

```text
GET {AITUNNEL_BASE_URL}/models
Authorization: Bearer {AITUNNEL_API_KEY}
```

Result:

```text
HTTP 403
error code: 1010
```

This may be Cloudflare/access protection, a wrong base URL, or an endpoint
restriction. Next chat should inspect `https://docs.aitunnel.ru` and use the
documented OpenAI-compatible endpoint format before trying again.

VLM selection goal:

- Choose a strong vision-language model for scene/object selection.
- Required tasks:
  - identify which plaza photos best support Marble world generation;
  - detect unwanted objects such as Christmas trees, crowds, signs, occlusions;
  - identify candidate places for exhibit placement;
  - summarize spatial layout for the Marble prompt;
  - later score generated outputs.

Practical candidate model types:

- Best quality if available: GPT-4o / GPT-4.1 vision-class model through
  AITUNNEL.
- Cost-effective if available: GPT-4.1 mini / Qwen-VL / Gemini Flash-class VLM.

Do not spend many VLM calls immediately. First create contact sheets and send a
small number of image grids to the VLM.

## HoverAI Context

The user mentioned HoverAI:

- Repository to inspect: `NickElixir/hoverai_rag`
- Concept: drone-avatar with screen and projector.

Need to study the repo in the next chat.

Potential collaboration scenario:

- Marble creates a digital twin-like campus plaza.
- ROS2 + OMPL plans a safe drone route around exhibits and pedestrians/obstacles.
- HoverAI is represented as an avatar drone with a screen/projector.
- Demo mission: HoverAI guides visitors through a temporary open-air robotics
  exhibit in Skoltech central plaza, stopping near cars/art objects and projecting
  labels or route information.

## Recommended Next Steps

1. Keep `VR Dataset/` ignored; do not commit raw photos.
2. Generate local contact sheets for `VR Dataset/`.
3. Use VLM via AITUNNEL to rank photos:
   - scene reconstruction quality;
   - spatial coverage;
   - low occlusion;
   - absence/removability of Christmas trees;
   - useful surfaces for drone route and exhibit placement.
4. Search web for Skolkovo/Skoltech art objects if user does not provide photos.
5. Inspect `NickElixir/hoverai_rag` for HoverAI wording and capabilities.
6. Propose for user approval:
   - scenario;
   - selected base scene photos;
   - selected object/exhibit references;
   - final Marble prompt;
   - approximate HoverAI drone route.
7. Only after approval, run Marble generation.

## Existing Useful Files

- `AGENTS.md`: agent instructions and commit discipline.
- `README.md`: project overview.
- `PROJECT_CONTEXT.md`: original Marble identity-drift research context.
- `protocols/marble_test_plan.md`: Marble pilot plan.
- `protocols/marble_quality_check.md`: quality checklist.
- `protocols/automatic_video_analysis.md`: automatic video analysis notes.
- `scripts/marble_generate_world.py`: creates a new Marble world and spends credits.
- `scripts/marble_poll_operation.py`: polls an existing operation without spending credits.
- `scripts/extract_orbit_frames.py`: extracts reproducible frames from walkthrough video.
- `scripts/make_vlm_review_batch.py`: creates VLM scoring batches.

## Credit Safety

Do not run `scripts/marble_generate_world.py` unless the user explicitly approves
spending Marble credits. Use local analysis, VLM ranking, and prompt preparation
first.

## Uncommitted Work At Handoff

Expected uncommitted changes:

- `.gitignore`: added `VR Dataset/` and `.DS_Store`.
- `.env.example`: added AITUNNEL variable placeholders.
- This handoff file.

Before switching chats or pushing, consider committing these documentation and
ignore-file changes.
