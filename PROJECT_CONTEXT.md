# Identity Drift in Generative World Models

## Project goal
Comparative study of identity preservation in generative world models across
two domains: AV simulation (literature review) and car visualization
(empirical experiment on selected 2D car reference images). Final artefact:
defense presentation for Skoltech course "VR & AR" (Prof. Tsetserukou),
12-14 slides.

## Background: 2D car reference inputs

### What it is
The empirical part uses selected 2D car reference images as inputs to World
Labs Marble. Each image contains a target car with visible body shape, wheel
identity cues, paint color, and proportions. Marble then generates a navigable
3D scene from the reference.

### Why these inputs are relevant to this research
The selected car references provide a practical test case for identity
preservation. The world model must infer unseen sides of the car while keeping
the same body silhouette, wheel style, proportions, and other visible identity
cues. This makes the setup useful for studying the gap between visual
plausibility and geometry that is reliable enough for robot navigation.

### What we use in this research
1. **Selected 2D car images** as inputs to Marble for world generation.
2. **Manual quality criteria** for what "acceptable identity preservation"
   means in the generated 3D scene.
3. **Controlled orbit recordings** to evaluate the same object from repeatable
   viewpoints.

### What is not in scope
- We do not evaluate the original image creation pipeline.
- We do not improve the input images themselves.
- We focus on identity preservation after 3D world generation.

## Core hypothesis
Identity drift is a domain-invariant failure mode of pixel-space world models.
Mitigation strategies, however, are domain-specific. We test this empirically
on one shared model (World Labs Marble) applied to the car visualization use
case, and review existing literature for the AV case.

## Empirical experiment (Case B — generated car world)
- 10 selected 2D car reference images.
- Each photo -> 1 generated world in Marble (free tier, single-image input).
- 360 degree walkthrough recording of each world (every 45 degrees -> 8 frames
  per world).
- Total dataset: 10 worlds x 8 angles = 80 generated frames + 10 originals.

## Metrics
For each (original_photo, generated_frame_at_angle) pair, compute:
1. **SSIM** — structural similarity (scikit-image)
2. **pHash Hamming distance** — perceptual hash distance (imagehash)
3. **LPIPS** — learned perceptual similarity (lpips library) [optional,
   for SIGGRAPH submission quality]
4. **CLIP cosine similarity** — semantic embedding distance (transformers)
   [optional]

Output: a results table of 10 cars x 8 angles x 4 metrics = 320 measurements,
saved as `results/metrics.csv`.

## User study
- 10 participants (Skoltech students)
- Within-subjects design, 3 conditions per participant:
  1. Original photo
  2. Selected 2D car reference image
  3. Marble walkthrough video (recorded screen capture, viewed in identical
     environment — Oculus headset OR Android AR browser, decided on day 1)
- Likert 1-7 scale: "How well does this preserve the identity of the original
  car?"
- Analysis: one-way ANOVA across 3 conditions, post-hoc Tukey HSD
- Tools: Python (scipy.stats) or JASP

## Tech stack
- Python 3.10+
- Libraries: scikit-image, imagehash, lpips, transformers, opencv-python,
  pandas, scipy, matplotlib, seaborn, jupyter

## Constraints
- Free tier Marble first; Standard plan ($20) only if export is needed
- All artefacts in shared workspace, not local machines
- Daily standups, hard deadline 9 days
- No live demo at defense — only pre-recorded screen captures
- Cars' license plates must be blurred in any published photos (privacy)

## Team roles
- Lead (Nikolai): coordination, slides, presentation
- AV-track owner: literature review slides, extract metrics from
  SceneDiffuser++ / Waymo WM papers
- Marble experiment owner: account setup, world generation, walkthrough
  recording
- User study owner: experiment design, questionnaire, recruitment, ANOVA
- VR/AR integrator: Oculus or Android AR setup for user study

## Out of scope
- Real-time world generation (Marble doesn't support, Genie 3 too expensive)
- Other world models in empirical experiment (Cosmos, Isaac, Alpamayo) —
  mentioned only in Discussion section
- Physics simulation
- Closed-loop policy training
