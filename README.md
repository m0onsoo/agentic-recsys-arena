# Agentic RecSys Arena

This is the main Empirica v2 project for comparing recommender systems using matched human and browser-agent judgments. The separate `../test/` directory is a pilot prototype and is not part of this repository.

## Current state

This repository contains a working Empirica 1.12.5 foundation and a single-participant setup check. It does not yet contain MovieLens data, recommender outputs, personas, comparison scenarios, browser agents, or study-ready data collection. The setup check is not a research task, and its results must not be included in analyses.

## Run locally

1. Ensure the `empirica` CLI is installed. This project was initialized with CLI v1.12.5.
2. On a new checkout, install dependencies with `npm ci` in both `client/` and `server/`, then run `node scripts/init-local-config.mjs` from this directory.
3. Run `empirica` from this directory.
4. Open `http://localhost:3000/` for the participant page or `http://localhost:3000/admin/` for the admin panel.
5. Admin credentials are in the local `.empirica/empirica.toml` file. Keep that file private.
6. In the admin panel, create and start a batch using the `Solo` treatment and `Default individual` lobby. Each participant needs a separate game.

The CLI and `@empirica/core` are pinned to 1.12.5 for this foundation. Local Empirica credentials and data are generated per installation and are excluded from Git. If ports 3000 and 8844 are occupied, set `ARA_SERVER_URL` and `ARA_VITE_PORT` when starting Empirica, and pass matching `--server.addr` and `--server.proxyaddr` flags.

## Research boundaries

- A scenario will represent a dataset user, with training-only history and a fixed evidence-supported persona.
- Humans and interactive agents will use the same participant interface and accessible movie information.
- Actual model identities and offline metrics must stay out of evaluator-facing content.
- Valid A/B/No Preference judgments must be distinguished from missing responses and execution failures.
- Distinct personas (P), repeated agent runs (R), total jobs, and concurrency are separate counts.
- The history display direction and other protocol choices remain open; see the prior workspace's `docs/REQUIREMENTS.md` before implementing real scenarios.

The pilot prototype, its exports, and its credentials remain in the previous workspace. No deployment target is configured.
