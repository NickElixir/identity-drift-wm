# Instructions For AI Agents

## Project

This repo supports a short research pilot on identity drift in generative world
models. The empirical track uses DW AI car wheel-composite images as inputs to
World Labs Marble, then evaluates whether the generated navigable world
preserves the car identity.

## Safety

- Never commit `.env` or API keys.
- Do not run `scripts/marble_generate_world.py` unless the user explicitly asks
  to spend World Labs credits.
- To inspect an existing operation, use `scripts/marble_poll_operation.py`.
- If a generation command crashes after `worlds:generate`, assume the API
  operation may already exist and check World Labs Platform before retrying.
- Do not overwrite selected input images without updating
  `inputs/dw_ai_2d/selection_manifest.csv`.

## Commit Discipline

- Run `git status --short` before starting work and before every commit.
- Commit regularly after each meaningful, working step so experiment state is
  not lost.
- Prefer small topical commits:
  - dataset/input selection
  - prompt or protocol changes
  - API/tooling changes
  - run results and QA notes
  - presentation/report updates
- Use concise imperative commit messages, for example:
  - `Add Marble pilot input manifest`
  - `Document first Marble QA result`
  - `Add frame extraction script`
- Do not mix unrelated changes in one commit.
- Do not commit generated cache files, local API logs, `.env`, credentials, or
  private scratch files.
- If a command spends credits or changes external state, commit local setup
  before running it when practical, then commit results/notes after inspection.
- Never rewrite or delete previous experiment results unless the user explicitly
  asks for cleanup. Add corrected notes as a new change instead.

## Current Marble Baseline

- Model: `marble-1.1`
- Prompt file: `prompts/marble_outdoor_forecourt.txt`
- First successful world:
  `https://marble.worldlabs.ai/world/5519284a-551c-4dbb-a055-c7944c669109`
- Main run table: `results/marble_runs.csv`

## Quality Workflow

1. Open the Marble world URL.
2. Do quick QA using `protocols/marble_quality_check.md`.
3. If it passes, record a controlled orbit around the car.
4. Save the video in `recordings/` using the run id.
5. Extract or capture 8 frames at repeatable orbit positions.
6. Fill `results/frame_annotations.csv`.
7. Keep notes concrete: car count, wheel preservation, body shape drift,
   occlusions, route feasibility, and whether panorama/walk view differs.

## Expected Constraints

- Pro subscription may be required for high-quality export/download.
- Browser walkthrough recordings are sufficient for the core experiment.
- Unity/GLB/splat export is optional and should not block the research pilot.
