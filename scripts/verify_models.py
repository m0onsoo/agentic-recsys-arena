"""Compare standalone rankings to RecBole for one user after registry export."""

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent))
from rerank_experiment.checkpoints import LoadedRecommender  # noqa: E402
from recommend import recommend  # noqa: E402


settings = yaml.safe_load((ROOT.parent / "rerank_experiment/defaults.yaml").read_text())
user_id = sys.argv[1] if len(sys.argv) > 1 else "1080"
result = recommend(user_id, 20)["recommendations"]
for name, path in settings["checkpoints"].items():
    model = LoadedRecommender(path, dataset_path=settings["dataset_path"],
                              recbole_root=settings["recbole_root"])
    uid = model.dataset.token2id(model.config["USER_ID_FIELD"], user_id)
    expected, _ = model.top_candidates([uid], 20)[uid]
    expected_ids = [model.raw_item(item) for item in expected]
    actual_ids = [movie["movieId"] for movie in result[name]]
    assert actual_ids == expected_ids, f"{name}: ranking differs\nexpected={expected_ids}\nactual={actual_ids}"
    print(f"{name}: exact Top-20 match")
