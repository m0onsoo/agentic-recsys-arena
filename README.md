# Agentic RecSys Arena

This is the main Empirica v2 project for comparing recommender systems using matched human and browser-agent judgments. The separate `../test/` directory is a pilot prototype and is not part of this repository.

## Current state

This repository contains an Empirica 1.12.5 single-participant MovieLens recommendation preview. It shows checkpoint rankings but does not collect judgments or provide a study-ready protocol.

## Run locally

1. Ensure the `empirica` CLI is installed. This project was initialized with CLI v1.12.5.
2. On a new checkout, install dependencies with `npm ci` in both `client/` and `server/`, then run `node scripts/init-local-config.mjs` from this directory.
3. Populate the private `model_registry/` from a trusted local copy or run the exporter described below in the original experiment environment.
4. Set `ARA_PYTHON` to a Python interpreter with PyTorch installed, then run `empirica` from this directory. For example, `ARA_PYTHON=/home1/moonsoo/projects/venv/bin/python empirica`.
5. Open `http://localhost:3000/` for the participant page or `http://localhost:3000/admin/` for the admin panel.
6. Admin credentials are in the local `.empirica/empirica.toml` file. Keep that file private.
7. In the admin panel, create and start a batch using the `Solo` treatment and `Default individual` lobby. Each participant needs a separate game.

Set `ARA_USER_ID=1080` (or another eligible raw MovieLens 1M user ID) on the Empirica server to change the preview user. At game start the server invokes `scripts/recommend.py`, which reads only the local registry and PyTorch weights; it does not import RecBole. The three Top-20 lists exclude items in that user's training and validation history. Movie titles, years and genres come from the exported dataset. The private registry also contains locally validated TMDB IDs; no TMDB request is needed to view a list. Set `VITE_SHOW_IDENTITIES=false` before starting Empirica to replace model names with List 1/2/3 and hide the user ID in the UI. This is a display flag, not research-grade blinding of participant-accessible game data.

## Model registry

`model_registry/` holds local `manifest.json`, `data.json.gz`, and per-model `original.pth` and `weights.pt`. All data files are Git-ignored; only `.gitkeep` files preserve the directory layout. `manifest.json` records model names, paths, hashes, epochs, and logged test metrics. LightGCN's test metrics are empty because its training job ended at the time limit; its saved checkpoint is still usable for inference.

The initial export was made from `../rerank_experiment/defaults.yaml` using `/home1/moonsoo/projects/venv/bin/python -B scripts/register_models.py` in the trusted experiment environment. After replacing a source checkpoint, update that YAML path and rerun the exporter. It verifies that all three checkpoints share the same user/item mapping and data split before writing the manifest. The exporter needs the original RecBole installation; the Empirica runtime does not. This preview requires PyTorch and the registry files on the machine running the Empirica server.

The CLI and `@empirica/core` are pinned to 1.12.5 for this foundation. Local Empirica credentials and data are generated per installation and are excluded from Git. If ports 3000 and 8844 are occupied, set `ARA_SERVER_URL` and `ARA_VITE_PORT` when starting Empirica, and pass matching `--server.addr` and `--server.proxyaddr` flags.

## Research boundaries

- A scenario will represent a dataset user, with training-only history and a fixed evidence-supported persona.
- Humans and interactive agents will use the same participant interface and accessible movie information.
- Hide model identities for evaluator-facing sessions with `VITE_SHOW_IDENTITIES=false`; offline metrics stay in the private registry.
- Valid A/B/No Preference judgments must be distinguished from missing responses and execution failures.
- Distinct personas (P), repeated agent runs (R), total jobs, and concurrency are separate counts.
- The history display direction and other protocol choices remain open; see the prior workspace's `docs/REQUIREMENTS.md` before implementing real scenarios.

The pilot prototype, its exports, and its credentials remain in the previous workspace. No deployment target is configured.
