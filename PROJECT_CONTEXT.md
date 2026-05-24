# Identity Drift in Generative World Models

## Project goal
Comparative study of identity preservation in generative world models 
across two domains: AV simulation (literature review) and consumer 
visualization (empirical experiment on DW AI). Final artefact: defense 
presentation for Skoltech course "VR & AR" (Prof. Tsetserukou), 
12–14 slides, deadline 9 days from kickoff.

## Background: DW AI (Dream Wheels AI)

### What it is
DW AI is a 2D automotive visualization product developed by the project 
lead prior to this research. It is a Telegram bot that allows car owners 
to preview how their own car would look with different wheels before 
making a purchase decision.

Bot handle: @DreamWheelsAI_bot
Status: working MVP, used by ~50 testers from automotive marketplaces

### Why DW AI is relevant to this research
DW AI provides the **input pipeline** for our Case B empirical experiment. 
The bot's output (a photorealistic 2D composite of a user's car with new 
wheels) is the input we feed into World Labs Marble to generate a 3D 
navigable showroom world. This makes DW AI the bridge between a 
real-world consumer use case and the world model under test.

### Technical architecture of DW AI (current state)
- **Frontend**: Telegram bot (python-telegram-bot)
- **Stage 1 — Composite generation**: Reve API (image-to-image inpainting 
  with mask)
- **Stage 2 — Quality filter**: Vision-Language Model (VLM) gate that 
  rejects failed compositions (wrong wheel placement, distorted geometry, 
  reflections artifacts)
- **Inputs**: user photo of their car + selected wheel reference image
- **Output**: photorealistic 2D image with new wheels composited onto 
  the user's car

### What we use from DW AI in this research
1. **Output images** (10 selected examples) as inputs to Marble for 
   world generation
2. **Quality criteria** from Stage 2 VLM filter as informal baseline 
   for what "acceptable identity preservation" means in consumer context
3. **Real user demand signal** — the bot has actual users with 
   identity-preservation requirements, which grounds the research in 
   a practical use case rather than purely theoretical concern

### What DW AI is NOT in the scope of this research
- We do not modify or improve the DW AI pipeline itself
- We do not evaluate DW AI's 2D output quality as the primary research 
  question — it serves as a baseline condition in the user study
- Bot internals (Reve API specifics, VLM model identity, prompt 
  engineering) are not relevant to the research question and should 
  not appear in defense slides or paper

### Reference notation
When referring to DW AI in code comments, slides, or paper text:
- First mention: "DW AI (Dream Wheels AI)"
- Subsequent mentions: "DW AI"
- Bot handle for reproducibility: @DreamWheelsAI_bot
- In code/data, use `dw_ai_2d` as the condition label (consistent with 
  user study schema)

## Core hypothesis
Identity drift is a domain-invariant failure mode of pixel-space world 
models. Mitigation strategies, however, are domain-specific. We test 
this empirically on one shared model (World Labs Marble) applied to 
the consumer showroom use case, and review existing literature for 
the AV case.

## Empirical experiment (Case B — DW AI showroom)
- 10 input car photos from the DW AI bot pipeline (@DreamWheelsAI_bot)
- Each photo → 1 generated world in Marble (free tier, single-image input)
- 360° walkthrough recording of each world (every 45° → 8 frames per world)
- Total dataset: 10 worlds × 8 angles = 80 generated frames + 10 originals

## Metrics
For each (original_photo, generated_frame_at_angle) pair, compute:
1. **SSIM** — structural similarity (scikit-image)
2. **pHash Hamming distance** — perceptual hash distance (imagehash)
3. **LPIPS** — learned perceptual similarity (lpips library) [optional, 
   for SIGGRAPH submission quality]
4. **CLIP cosine similarity** — semantic embedding distance (transformers) 
   [optional]

Output: a results table of 10 cars × 8 angles × 4 metrics = 320 measurements,
saved as `results/metrics.csv`.

## User study
- 10 participants (Skoltech students)
- Within-subjects design, 3 conditions per participant:
  1. Original photo
  2. DW AI 2D composite output
  3. Marble walkthrough video (recorded screen capture, viewed in 
     identical environment — Oculus headset OR Android AR browser, 
     decided on day 1)
- Likert 1–7 scale: "How well does this preserve the identity of the 
  original car?"
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