"""Standalone CPU inference for registered BPR, LightGCN and MultiVAE weights."""

import argparse
import gzip
import json
from pathlib import Path

import torch
import torch.nn.functional as F


REGISTRY = Path(__file__).resolve().parents[1] / "model_registry"


def load_weights(path):
    # The registry exporter writes plain tensor dictionaries, without RecBole objects.
    try:
        return torch.load(path, map_location="cpu", weights_only=True)
    except TypeError:
        return torch.load(path, map_location="cpu")


def normalized_graph(train, n_users, n_items):
    edges = set((int(u), n_users + int(i)) for u, i in train)
    edges |= {(i, u) for u, i in list(edges)}
    row, col = zip(*sorted(edges))
    index = torch.tensor([row, col], dtype=torch.long)
    degree = torch.bincount(index[0], minlength=n_users + n_items).float() + 1e-7
    value = degree[index[0]].rsqrt() * degree[index[1]].rsqrt()
    return torch.sparse_coo_tensor(index, value, (n_users + n_items,) * 2).coalesce()


def scores(name, weights, user, data, config):
    if name == "BPR":
        return weights["user_embedding.weight"][user] @ weights["item_embedding.weight"].T
    if name == "LightGCN":
        users = weights["user_embedding.weight"]
        items = weights["item_embedding.weight"]
        graph = normalized_graph(data["train"], len(users), len(items))
        embedding = torch.cat([users, items])
        layers = [embedding]
        for _ in range(config["n_layers"]):
            embedding = torch.sparse.mm(graph, embedding)
            layers.append(embedding)
        combined = torch.stack(layers).mean(0)
        return combined[user] @ combined[len(users):].T
    if name == "MultiVAE":
        rating = torch.zeros((1, len(data["items"])))
        rating[0, [i for u, i in data["train"] if u == user]] = 1
        hidden = F.normalize(rating)
        for prefix in ("encoder", "decoder"):
            numbers = sorted(int(k.split(".")[1]) for k in weights if k.startswith(prefix + ".") and k.endswith(".weight"))
            for index, number in enumerate(numbers):
                hidden = F.linear(hidden, weights[f"{prefix}.{number}.weight"], weights[f"{prefix}.{number}.bias"])
                if index < len(numbers) - 1:
                    hidden = torch.tanh(hidden)
                if prefix == "encoder" and index == len(numbers) - 1:
                    hidden = hidden[:, : hidden.shape[1] // 2]
        return hidden[0]
    raise ValueError(f"Unsupported model: {name}")


def recommend(user_id, limit=20):
    manifest = json.loads((REGISTRY / "manifest.json").read_text())
    with gzip.open(REGISTRY / "data.json.gz", "rt", encoding="utf8") as stream:
        data = json.load(stream)
    if user_id not in data["eligible_users"]:
        raise ValueError(f"User {user_id} is not an eligible MovieLens test user")
    user = data["users"].index(user_id)
    seen = {int(i) for u, i in data["train"] + data["valid"] if u == user}
    output = {}
    with torch.no_grad():
        for name, entry in manifest["models"].items():
            weights = load_weights(REGISTRY / entry["inference_weights"])
            ranking = scores(name, weights, user, data, entry["config"]).clone()
            ranking[0] = float("-inf")
            ranking[list(seen)] = float("-inf")
            values, indices = torch.topk(ranking, limit)
            if not torch.isfinite(values).all():
                raise ValueError(f"{name} has fewer than {limit} unseen items")
            output[name] = []
            for position, internal_id in enumerate(indices.tolist(), 1):
                movie_id = data["items"][internal_id]
                movie = data["movies"][movie_id]
                output[name].append({"rank": position, "movieId": movie_id,
                                     "title": movie["title"], "year": movie["release_year"],
                                     "genres": movie["genres"],
                                     "tmdbId": data["tmdb_ids"].get(movie_id)})
    return {"userId": user_id, "recommendations": output}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--user-id", default="1080", help="Raw MovieLens user ID")
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    print(json.dumps(recommend(args.user_id, args.limit)))
