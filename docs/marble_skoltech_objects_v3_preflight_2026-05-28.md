# Marble V3 Preflight: Self-Driving Car, Anton Smit, Mirror Frames

Date: 2026-05-28

## Goal

Prepare a third Marble run for the Skoltech courtyard using the new object set:

- white self-driving car;
- Anton Smit fragmented face sculpture;
- Skolkovo mirrored rectangular frame sculpture.

Do not run Marble generation without explicit user approval, because
`scripts/marble_generate_world.py` spends World Labs credits.

## Input Strategy

The previous Marble results show that a single visible side is not enough for
object identity. Marble tends to hallucinate unobserved sides as blank,
flattened, or abstract geometry. For this run, use multiple scene-reference
images rather than a single collage:

- one establishing courtyard view with all three objects;
- one front/side car-focused view;
- one rear/rear-left car-focused view;
- one Anton front view;
- one Anton rear/rib-side view;
- one mirror-frame-focused view;
- two real courtyard photos to stabilize the building/path geometry.

The dedicated Anton rear/rib-side reference is important. It gives Marble an
explicit complete backside and should reduce the chance that the sculpture
becomes a one-sided billboard.

## Selected Object References

Self-driving car:

- left/profile: `VR Dataset/object_refs/self_driving_car/PXL_20260527_230829993.jpg`
- front-left: `VR Dataset/object_refs/self_driving_car/PXL_20260527_230838584.jpg`
- front: `VR Dataset/object_refs/self_driving_car/PXL_20260527_230844651.jpg`
- rear: `VR Dataset/object_refs/self_driving_car/PXL_20260527_230922069.jpg`
- rear-left: `VR Dataset/object_refs/self_driving_car/PXL_20260527_230916304.jpg`

Anton Smit:

- back/ribs: `VR Dataset/object_refs/art_anton_smit_skolkovo/PXL_20260528_062550326.jpg`
- angled back/ribs: `VR Dataset/object_refs/art_anton_smit_skolkovo/PXL_20260528_062639507.jpg`
- front-left: `VR Dataset/object_refs/art_anton_smit_skolkovo/PXL_20260528_062609700.jpg`
- front: `VR Dataset/object_refs/art_anton_smit_skolkovo/PXL_20260528_062625697.jpg`
- side thickness: `VR Dataset/object_refs/art_anton_smit_skolkovo/skolkovo_anton_smit_1061756.jpg`

Mirror frames:

- front-left: `VR Dataset/object_refs/mirroring_frames_skolkovo/PXL_20260528_062316000.jpg`
- front: `VR Dataset/object_refs/mirroring_frames_skolkovo/PXL_20260528_062340149.jpg`
- side: `VR Dataset/object_refs/mirroring_frames_skolkovo/PXL_20260528_062408747.jpg`

## Local Generated Scene References

These are ignored by git and remain local:

1. `results/marble_inputs/skoltech_objects_v3/01_overview_self_driving_car_anton_mirror.png`
2. `results/marble_inputs/skoltech_objects_v3/02_self_driving_car_focus.png`
3. `results/marble_inputs/skoltech_objects_v3/06_self_driving_car_rear_seedream.png`
4. `results/marble_inputs/skoltech_objects_v3/03_anton_front_focus.png`
5. `results/marble_inputs/skoltech_objects_v3/04_anton_back_focus_repaired_nano.png`
6. `results/marble_inputs/skoltech_objects_v3/05_mirror_frame_focus.png`

Quick visual QA:

- car-focus is the cleanest car identity reference;
- Seedream car-rear adds the missing rear hatch, vertical taillights, rear
  window, roof sensor bar, and rear-left body geometry;
- Anton front and the repaired Nano Banana Anton back/rib-side together are the
  strongest sculpture identity references;
- mirror-focus is usable and gives the clearest frame geometry;
- overview is useful for placement, but its mirror frame is weaker and should
  not be the only mirror reference.

Rejected/generated-but-not-selected local references:

- `results/marble_inputs/skoltech_objects_v3/04_anton_back_focus.png`: rejected
  because the rear side became an oversized smooth blank/melted structure.
- `results/fal_edits/skoltech_objects_v3_repairs/reve_anton_back/...`: rejected
  because it over-cleaned the back into a generic white rib panel and lost too
  much of the colorful side identity.
- `results/fal_edits/skoltech_objects_v3_repairs/nano_car_rear/...`: usable
  rear view, but less consistent with the original car side graphics than the
  selected Seedream rear view.

## Marble Prompt

Use:

```text
prompts/marble_skoltech_objects_v3_self_driving_car_anton_mirror.txt
```

## Proposed Marble Command

Run only after explicit approval to spend World Labs credits:

```bash
python3 scripts/marble_generate_world.py \
  "results/marble_inputs/skoltech_objects_v3/01_overview_self_driving_car_anton_mirror.png" \
  "results/marble_inputs/skoltech_objects_v3/02_self_driving_car_focus.png" \
  "results/marble_inputs/skoltech_objects_v3/06_self_driving_car_rear_seedream.png" \
  "results/marble_inputs/skoltech_objects_v3/03_anton_front_focus.png" \
  "results/marble_inputs/skoltech_objects_v3/04_anton_back_focus_repaired_nano.png" \
  "results/marble_inputs/skoltech_objects_v3/05_mirror_frame_focus.png" \
  "VR Dataset/IMG_20260527_154723.jpg" \
  "VR Dataset/IMG_20260527_154840.jpg" \
  --display-name "Skoltech self-driving car Anton mirror frames" \
  --model marble-1.1 \
  --prompt-file prompts/marble_skoltech_objects_v3_self_driving_car_anton_mirror.txt \
  --reconstruct-images \
  --disable-recaption
```

Rationale for using eight images: Marble reconstruction mode is required for
5-8 images, and this run benefits from explicit object-side coverage more than
from another near-duplicate courtyard angle. The final allocation is six
scene-reference images and two real courtyard geometry anchors.
