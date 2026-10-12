"""One-time export of trusted RecBole checkpoints into a standalone arena registry.

Run in the original experiment environment. Runtime inference never imports RecBole.
"""

import gzip
import hashlib
import json
import shutil
import sys
from pathlib import Path

import torch
import yaml


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT.parent
sys.path.insert(0, str(EXPERIMENT))
from rerank_experiment.checkpoints import LoadedRecommender, read_logged_metrics  # noqa: E402
from rerank_experiment.metadata import read_extended, read_movielens  # noqa: E402


def digest(path):
    sha = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            sha.update(block)
    return sha.hexdigest()


def pairs(loader, user_field, item_field):
    rows = loader._dataset.inter_feat
    return list(zip(rows[user_field].tolist(), rows[item_field].tolist()))


def main():
    settings = yaml.safe_load((EXPERIMENT / "rerank_experiment/defaults.yaml").read_text())
    registry = ROOT / "model_registry"
    items, _ = read_movielens(settings["dataset_path"], settings["dataset"])
    tmdb_ids, _, _ = read_extended(settings["extended_movie_path"], items)
    manifest = {"dataset": settings["dataset"], "models": {}}
    reference = None
    for name in ("BPR", "LightGCN", "MultiVAE"):
        source = Path(settings["checkpoints"][name])
        ctx = LoadedRecommender(source, settings["dataset"], settings["dataset_path"],
                                recbole_root=settings["recbole_root"])
        if ctx.model_name != name:
            raise ValueError(f"Expected {name}, found {ctx.model_name}")
        if reference is None:
            reference = ctx
            user_field, item_field = ctx.config["USER_ID_FIELD"], ctx.config["ITEM_ID_FIELD"]
            payload = {
                "users": [str(x) for x in ctx.dataset.field2id_token[user_field]],
                "items": [str(x) for x in ctx.dataset.field2id_token[item_field]],
                "train": pairs(ctx.train, user_field, item_field),
                "valid": pairs(ctx.valid, user_field, item_field),
                "eligible_users": [ctx.raw_user(uid) for uid in ctx.eligible_users()],
                "movies": items,
                "tmdb_ids": tmdb_ids,
            }
            with gzip.open(registry / "data.json.gz", "wt", encoding="utf8") as stream:
                json.dump(payload, stream, separators=(",", ":"))
        elif ctx.mapping_hash != reference.mapping_hash or ctx.split_hash != reference.split_hash:
            raise ValueError(f"{name} has a different ID mapping or data split")
        dest = registry / name
        dest.mkdir(exist_ok=True)
        copy = dest / "original.pth"
        if not copy.exists() or digest(copy) != digest(source):
            shutil.copy2(source, copy)
        weights = dest / "weights.pt"
        torch.save(ctx.model.state_dict(), weights)
        manifest["models"][name] = {
            "checkpoint": f"{name}/original.pth",
            "inference_weights": f"{name}/weights.pt",
            "sha256": digest(copy),
            "weights_sha256": digest(weights),
            "source_checkpoint": str(source),
            "epoch": ctx.checkpoint_epoch,
            "test_metrics": read_logged_metrics(settings["log_paths"].get(name)),
            "metrics_source": settings["log_paths"].get(name) if name != "LightGCN" else None,
            "config": {"n_layers": ctx.config["n_layers"] if name == "LightGCN" else None},
            "mapping_hash": ctx.mapping_hash,
            "split_hash": ctx.split_hash,
        }
        print(f"Registered {name}")
    manifest["data_sha256"] = digest(registry / "data.json.gz")
    (registry / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
