# Marble Scene Preflight: Skoltech HoverAI Demo

Date: 2026-05-27

## Goal

Generate a navigable Marble world based on the central outdoor courtyard of the
Skoltech campus, then use it as a robotics demo scene for HoverAI: an embodied
aerial guide that can explain exhibits, project route cues, and plan a safe
visitor-facing flight path through the space.

## Marble Constraints

- Text prompt limit: up to 2,000 characters.
- Image prompt specs: recommended long side 1024 px, max 20 MB, png/jpg/webp.
- Multi-image mode:
  - Direction control: up to 4 images, with Front/Back/Left/Right labels.
  - Auto Layout: up to 8 images, same aspect ratio/resolution, same space,
    close viewpoints, some overlap.

Recommended path for this scene: Auto Layout with 6-8 courtyard photos, because
the photos are from the same physical space and have overlapping architecture.

## AITUNNEL / VLM Status

AITUNNEL docs specify OpenAI-compatible `/v1/chat/completions` and a public model
catalog at `/public/aitunnel/models/chat`. Local requests from this machine/IP
currently return Cloudflare `403 error code: 1010` even for the public model
catalog, so the block is likely network/firewall-level, not necessarily a bad API
key.

Preferred VLM once access works:

1. `gpt-5.4-mini` or current GPT mini vision model in AITUNNEL: best balance for
   visual scene selection and concise structured output.
2. `gemini-3.1-flash-lite` or current Gemini Flash Lite vision model: cheaper
   fallback for broad contact-sheet triage.
3. `claude-sonnet-4.6`: high-quality reasoning fallback, but more expensive.

Use VLM in two passes only:

1. Contact-sheet triage: choose 8 scene candidates and flag visual issues.
2. Final pass: inspect selected full-resolution images and output Marble prompt.

## Scene Photo Candidates

Local private dataset: `VR Dataset/` (gitignored).

Best Marble scene set:

- `VR Dataset/IMG_20260527_154723.jpg` - strong path, columns, glass facade,
  lawn, clear perspective.
- `VR Dataset/IMG_20260527_154739.jpg` - similar view, sharper entrance and
  column rhythm.
- `VR Dataset/IMG_20260527_154807.jpg` - turn view with central shrubs and white
  ribbed facade.
- `VR Dataset/IMG_20260527_154832.jpg` - open paved plaza and passage through
  the building.
- `VR Dataset/IMG_20260527_154836.jpg` - best view toward the underpass and
  open flight corridor.
- `VR Dataset/IMG_20260527_154934.jpg` - open plaza near the white facade,
  useful for placing exhibits.
- `VR Dataset/IMG_20260527_154948.jpg` - route continuation with trees and white
  facade.

Avoid for base scene:

- Car-park series `155343` onward: useful for vehicle object references, not for
  the central courtyard world.
- Bike storage `160055` onward: good object references only if we want a
  micromobility exhibit.
- Frames with people crossing (`154909`, `154912`, etc.) because Marble docs say
  humans are not well supported.

Trees: keep them. They appear to be permanent campus landscaping, not temporary
holiday decorations. In the prompt, call them "evergreen landscaping and low
shrubs"; do not ask Marble to remove them unless the goal is a clean exhibition
plaza.

## Object / Exhibit Candidates

Current local candidates:

- White BMW SUV from `VR Dataset/IMG_20260527_155343.jpg`: clear side profile but
  adjacent car occludes the front. Use only as a placeholder unless the user
  uploads the 8-angle car set.
- Black/gray cars from `155649`-`160012`: better for "Skolkovo autonomous
  mobility row" atmosphere, but less suitable as a single hero object.
- Bike row from `160055`-`160105`: plausible micromobility exhibit, stable shape,
  easy for Marble to hallucinate correctly.

Internet-based art object candidates to reference in the prompt, not as exact
licensed images:

- Anton Smit, "Reflection on the Origin of Man" / "Размышление о происхождении
  человека": large fragmented face sculpture in Skolkovo.
- A Malevich-inspired black square/cube landmark: good local context because
  Skolkovo/Skoltech route narratives often reference Malevich.
- Abstract technology sculptures from Skolkovo public-art routes: use as generic
  "geometric public art" unless exact photos are provided.

Recommendation: for the first generation, include objects in text prompt only
and keep exact identity evaluation focused on the scene. For a later generation,
use uploaded 8-angle car photos as object references if Marble supports the
desired object-placement workflow.

## Collaboration Scenario

Scenario name: "HoverAI Campus Exhibit Guide"

HoverAI flies a controlled low-altitude route through the Skoltech courtyard. It
uses the generated Marble world as a rehearsal environment for path planning and
human-facing behavior. At each stop, it faces visitors, shows a lip-synced guide
avatar on its onboard screen, and projects a short visual cue on the pavement or
near the exhibit:

1. Start under the columned overhang at the glass entrance.
2. Move along the cobblestone path beside the lawn.
3. Stop at the public-art sculpture zone.
4. Continue to the vehicle exhibit zone.
5. Orbit one car or mobility exhibit at safe distance.
6. Return through the open passage, demonstrating route replanning around
   columns, shrubs, and visitors.

Robotics value: navigable-world generation becomes a low-cost testbed for route
planning, perception of architectural constraints, exhibit-stop selection, and
socially legible drone behavior.

## Proposed Marble Prompt

Create a realistic navigable outdoor courtyard at Skoltech in Skolkovo. Use the
uploaded photos as the main geometry: grey cobblestone paving, curved wood-clad
building edge on concrete columns, dark glass entrance facade, white ribbed
campus buildings, broad open paths, green lawn, evergreen landscaping, low
shrubs, and an underpass-like passage between buildings. Preserve the clean
modern research-campus atmosphere and consistent overcast daylight.

Adapt the courtyard into a robotics demonstration plaza. Add a few realistic
Skolkovo-style exhibits without crowding the space: a large fragmented stone-like
face sculpture with vertical ribs, a minimal black square/cube public-art
landmark, a yellow autonomous taxi-style demo car, and a small micromobility or
bicycle exhibit near the side.

Place the fragmented face sculpture on the lawn side near the open plaza,
visible from the main cobblestone path. Place the yellow demo car on the paved
open area near the white ribbed facade, leaving a wide clear corridor around it.
Put the small micromobility exhibit near the path edge, secondary to the
sculpture and car. Keep the central cobblestone route open for a HoverAI drone
flight path from the glass entrance under the columns, around the sculpture,
past the car, and toward the underpass. No people, no animals, no festive
decorations, no snow, no extra cars blocking the main route.

## Approval Questions

Approve or change:

- Use Auto Layout with the 7 listed courtyard photos.
- Keep evergreen landscaping.
- Use text-only object placement for the first scene generation.
- Ask user to upload the 8-angle car set only if the car must be a hero exhibit
  with stronger identity preservation.
