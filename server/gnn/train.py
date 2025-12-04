print("TRAIN.PY STARTED")


import os
import torch
from torch import nn, optim
from torch_geometric.utils import negative_sampling
from torch_geometric.data import Data

from data_processing import build_graph_from_games_csv
from gnn_model import GameGNN, DotProductLinkPredictor

SIMILARITY_THRESHOLD = 0.3
HIDDEN_DIM = 64
EMBED_DIM = 64
EPOCHS = 20
LR = 1e-3

THIS_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(THIS_DIR, "..", "model", "processed_games.csv")
MODEL_PATH = os.path.join(THIS_DIR, "gnn_model.pth")
GRAPH_PATH = os.path.join(THIS_DIR, "graph_data.pt")


def build_graph() -> Data:
    print(f"Loading games from {CSV_PATH}")
    data = build_graph_from_games_csv(
        csv_path=CSV_PATH,
        similarity_threshold=SIMILARITY_THRESHOLD,
    )
    print("Graph built.")
    return data

def make_train_edges(data: Data, num_neg_multiplier: int = 1):
    pos_edge_index = data.edge_index  # [2, num_edges]
    num_pos = pos_edge_index.size(1)

    # Negative sampling
    neg_edge_index = negative_sampling(
        edge_index=pos_edge_index,
        num_nodes=data.num_nodes,
        num_neg_samples=num_pos * num_neg_multiplier,
        method="sparse"
    )

    return pos_edge_index, neg_edge_index

def train():
    #Build graph
    data = build_graph()

    # Save graph for inference later
    torch.save(data, GRAPH_PATH)
    print(f"Saved graph Data to {GRAPH_PATH}")

    # Prepare model
    in_channels = data.x.size(1)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)

    model = GameGNN(in_channels, HIDDEN_DIM, EMBED_DIM).to(device)
    predictor = DotProductLinkPredictor().to(device)

    data = data.to(device)

    optimizer = optim.Adam(
        list(model.parameters()) + list(predictor.parameters()),
        lr=LR
    )
    criterion = nn.BCEWithLogitsLoss()

    pos_edge_index, neg_edge_index = make_train_edges(data)

    #Training loop 
    for epoch in range(1, EPOCHS + 1):
        model.train()
        predictor.train()
        optimizer.zero_grad()

        # Node embeddings
        z = model(data.x, data.edge_index)  # [N, EMBED_DIM]

        # Positive pairs
        pos_i = z[pos_edge_index[0]]
        pos_j = z[pos_edge_index[1]]
        pos_out = predictor(pos_i, pos_j)
        pos_label = torch.ones(pos_out.size(0), device=device)

        # Negative pairs
        neg_i = z[neg_edge_index[0]]
        neg_j = z[neg_edge_index[1]]
        neg_out = predictor(neg_i, neg_j)
        neg_label = torch.zeros(neg_out.size(0), device=device)

        out = torch.cat([pos_out, neg_out], dim=0)
        label = torch.cat([pos_label, neg_label], dim=0)

        loss = criterion(out, label)
        loss.backward()
        optimizer.step()

        with torch.no_grad():
            preds = (torch.sigmoid(out) > 0.5).float()
            acc = (preds == label).float().mean().item()

        print(f"Epoch {epoch:03d} | Loss: {loss.item():.4f} | Acc: {acc:.4f}")

    #Save model
    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "predictor_state_dict": predictor.state_dict(),
            "in_channels": in_channels,
            "hidden_dim": HIDDEN_DIM,
            "embed_dim": EMBED_DIM,
        },
        MODEL_PATH,
    )
    print(f"Saved trained model to {MODEL_PATH}")


if __name__ == "__main__":
    train()

