# MovieLens model registry and preview plan

## Goal

Show Top-20 recommendations from the existing BPR, LightGCN, and MultiVAE
MovieLens 1M checkpoints in a single-participant Empirica preview. Keep model
files local and make model and user labels hideable in the UI.

## Existing code and inputs

- `server/src/callbacks.js` creates the Empirica game and stage.
- `client/src/Stage.jsx` renders the participant stage.
- `../rerank_experiment/defaults.yaml` identifies the three checkpoints, logs,
  MovieLens files, and TMDB mapping source.
- `../rerank_experiment/checkpoints.py` reconstructs the checkpoint's ID mapping
  and split and provides RecBole reference rankings.

## Work units

1. Export the three trusted checkpoints into `model_registry/`. Record source,
   paths, hashes, epoch, metrics, and matching mapping/split fingerprints.
   Ignore data and weights in Git; track only `.gitkeep` layout files.
2. Run CPU inference from exported tensor weights and dataset metadata without
   importing RecBole in the Empirica runtime. Exclude training and validation
   history. Compare Top-20 rankings with RecBole for a representative user.
3. Generate a scenario at game start and show all three lists. Show model name
   and MovieLens user ID by default; hide both with `VITE_SHOW_IDENTITIES=false`.
4. Document registry setup and run instructions. Review the diff, commit each
   work unit separately, and open a draft PR for a Mac browser check.

## Acceptance checks

- Each registry hash matches its local file and all three mappings/splits agree.
- Standalone inference returns three 20-item lists for an eligible user and
  recommends no training or validation item.
- RecBole comparison passes for the same user.
- Empirica shows the lists with labels on, and hides labels with the flag off.
- Only code, documentation, and `.gitkeep` files appear in the PR.

The preview does not collect participant judgments. The display flag does not
remove model identities from participant-accessible game data; study-grade
blinding and judgment collection require separate work.
