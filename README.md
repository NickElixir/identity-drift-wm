# identity-drift-wm

Identity Drift in Generative World Models: From AV Simulation to Virtual
Showrooms.

This repository contains the Marble pilot pipeline for testing whether a
generative world model preserves the visual identity of a car after a DW AI
wheel-composite image is converted into a navigable 3D world.

## Current Pilot

- Model: `marble-1.1`
- Input mode: single DW AI/Reve-style image composite
- World type: simple outdoor dealership forecourt
- First generated world:
  <https://marble.worldlabs.ai/world/5519284a-551c-4dbb-a055-c7944c669109>
- Pilot inputs: `inputs/dw_ai_2d/car_01.png` to `car_04.png`
- Prompt: `prompts/marble_outdoor_forecourt.txt`

## Repository Layout

- `PROJECT_CONTEXT.md`: research context and experiment design.
- `inputs/dw_ai_2d/`: selected Marble input images.
- `prompts/`: fixed prompts used for Marble generation.
- `protocols/`: run plans and quality-check procedures.
- `results/`: run tables and annotation templates.
- `scripts/`: World Labs API helper scripts.
- `recordings/`: screen recordings from Marble walkthroughs.
- `analysis/`: image-selection notes and contact sheets.

## Setup

Create a local environment file:

```bash
cp .env.example .env
```

Then paste the World Labs API key into `.env`:

```bash
WORLDLABS_API_KEY=...
```

The `.env` file is ignored by git.

## Generate A Marble World

Use this only when you intentionally want to spend World Labs credits:

```bash
python3 scripts/marble_generate_world.py \
  inputs/dw_ai_2d/car_01.png \
  --display-name car_01_marble_pilot \
  --model marble-1.1 \
  --prompt-file prompts/marble_outdoor_forecourt.txt
```

The script prints the Marble world URL when generation completes and appends
operation records to `results/marble_api_runs.jsonl`.

To poll an existing operation without creating a new generation:

```bash
python3 scripts/marble_poll_operation.py OPERATION_ID
```

## Check Quality

Use two levels of evaluation:

1. Quick QA immediately after opening the Marble URL.
2. Controlled orbit recording plus frame annotation after the world passes quick
   QA.

See `protocols/marble_quality_check.md` for the exact checklist.

For the current first result, the quick observation is mixed: the panorama view
is strong and the car is recognizable from a good angle, but Marble added
extra cars and the front/near geometry shows visible drift. This is still useful
as a first identity-drift example, not a final polished result.

## Credit Safety

Do not rerun `scripts/marble_generate_world.py` to inspect a previous result.
Use the Marble URL, World Labs Platform trace, or `scripts/marble_poll_operation.py`
instead. `marble_generate_world.py` creates a new world generation and spends
credits.
