import os
from typing import List, Dict

import torch
import torch.nn.functional as F

from torch_geometric.data import Data
from torch_geometric.data.data import DataEdgeAttr, DataTensorAttr
from torch_geometric.data.storage import GlobalStorage

from gnn.gnn_model import GameGNN, DotProductLinkPredictor


THIS_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(THIS_DIR, "gnn_model.pth")
GRAPH_PATH = os.path.join(THIS_DIR, "graph_data.pt")


def load_model_and_graph():
    # ✔ FIX: allow PyTorch to unpickle PyG objects safely
    import torch.serialization
    torch.serialization.add_safe_globals([
        Data,
        DataEdgeAttr,
        DataTensorAttr,
        GlobalStorage
    ])

    # ✔ FIX: device selection AFTER imports
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)

    # Load graph
    data: Data = torch.load(GRAPH_PATH, map_location=device)
    data = data.to(device)

    # Load model checkpoint
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


def recommend_by_title(title: str, top_k: int = 10) -> List[Dict]:
    model, predictor, data, device = load_model_and_graph()

    titles = data.titles

    # Title lookup
    try:
        idx = next(i for i, t in enumerate(titles) if t.lower() == title.lower())
    except StopIteration:
        raise ValueError(f"Title '{title}' not found in dataset.")

    # Generate recommendations
    with torch.no_grad():
        z = model(data.x, data.edge_index)
        z = F.normalize(z, p=2, dim=-1)

        target = z[idx].unsqueeze(0)
        sims = (z @ target.T).squeeze(1)

        sims[idx] = -1  # don't recommend itself

        top_vals, top_idx = torch.topk(sims, k=top_k)

    results = []
    for score, j in zip(top_vals.tolist(), top_idx.tolist()):
        results.append({
            "title": titles[j],
            "similarity": float(score),
            "index": int(j),
            "appid": data.appids[j] if hasattr(data, "appids") else None,
        })

    return results

def recommend_multiple_titles(titles_input, top_k=10):
    model, predictor, data, device = load_model_and_graph()
    titles = data.titles

    # Title lookup
    idx_list = []
    for title in titles_input:
        try:
            idx = next(i for i, t in enumerate(titles) if t.lower() == title.lower())
            idx_list.append(idx)
        except StopIteration:
            raise ValueError(f"Title '{title}' not found in dataset.")

    # Generate recommendations
    with torch.no_grad():
        z = model(data.x, data.edge_index)
        z = F.normalize(z, p=2, dim=-1)

        target = z[idx_list].mean(dim=0, keepdim=True)
        target = F.normalize(target, p=2, dim=-1)

        sims = (z @ target.T).squeeze(1)

        # Exclude input titles
        for idx in idx_list:
            sims[idx] = -1

        top_vals, top_idx = torch.topk(sims, k=top_k)

    results = []
    for score, j in zip(top_vals.tolist(), top_idx.tolist()):
        results.append({
            "title": titles[j],
            "similarity": float(score),
            "index": int(j),
            "appid": data.appids[j] if hasattr(data, "appids") else None,
        })

    return results


#if __name__ == "__main__":
#    q = ["Baldur's Gate 3", "Dota 2"]
#    recs = recommend_multiple_titles(q, top_k=5)
#
#    print(f"\nRecommendations for '{q}':\n")
#    for r in recs:
#        print(f"- {r['title']}  (sim={r['similarity']:.3f})")
