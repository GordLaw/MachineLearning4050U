import os
from typing import List, Dict

import torch
import torch.nn.functional as F

from torch_geometric.data import Data
from gnn_model import GameGNN, DotProductLinkPredictor

THIS_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(THIS_DIR, "gnn_model.pth")
GRAPH_PATH = os.path.join(THIS_DIR, "graph_data.pt")


def load_model_and_graph():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)

    # Load graph
    data: Data = torch.load(GRAPH_PATH, map_location=device)
    data = data.to(device)

    ckpt = torch.load(MODEL_PATH, map_location=device)
    in_channels = ckpt["in_channels"]
    hidden_dim = ckpt["hidden_dim"]
    embed_dim = ckpt["embed_dim"]

    model = GameGNN(in_channels, hidden_dim, embed_dim).to(device)
    predictor = DotProductLinkPredictor().to(device)

    model.load_state_dict(ckpt["model_state_dict"])
    predictor.load_state_dict(ckpt["predictor_state_dict"])
    model.eval()
    predictor.eval()

    return model, predictor, data, device


def recommend_by_title(
    title: str,
    top_k: int = 10
) -> List[Dict]:
    model, predictor, data, device = load_model_and_graph()

    titles = data.titles  # list of strings
    # Find index of the requested title (case-insensitive)
    try:
        idx = next(i for i, t in enumerate(titles) if t.lower() == title.lower())
    except StopIteration:
        raise ValueError(f"Title '{title}' not found in dataset.")

    with torch.no_grad():
        z = model(data.x, data.edge_index)  # [N, embed_dim]
        z = F.normalize(z, p=2, dim=-1)

        target = z[idx].unsqueeze(0)  # [1, dim]
        # Cosine sim is just dot product of normalized vectors
        sims = (z @ target.T).squeeze(1)  # [N]

        # Remove self
        sims[idx] = -1.0

        topk_vals, topk_idx = torch.topk(sims, k=top_k)

    recs = []
    for score, j in zip(topk_vals.tolist(), topk_idx.tolist()):
        recs.append(
            {
                "title": titles[j],
                "similarity": float(score),
                "index": int(j),
                "appid": data.appids[j] if hasattr(data, "appids") else None,
            }
        )
    return recs


if __name__ == "__main__":
    # Quick manual test
    query_title = "Baldur's Gate 3"  # change as needed
    results = recommend_by_title(query_title, top_k=5)
    print(f"Recommendations for '{query_title}':")
    for r in results:
        print(f"- {r['title']} (sim={r['similarity']:.3f})")