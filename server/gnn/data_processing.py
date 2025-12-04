import pandas as pd
import numpy as np
import torch
from torch_geometric.data import Data
from sklearn.metrics.pairwise import cosine_similarity


def build_graph_from_games_csv(
    csv_path: str,
    similarity_threshold: float = 0.3,      
    use_genre_filter: bool = True,         
) -> Data:
    
    # Load Data
    df = pd.read_csv(csv_path)

    # Columns that are NOT tag features
    remove_cols = [
        "appid", "AppID",
        "Title", "title",
        "Release Year", "Original Price",
        "Recent Reviews Summary", "All Reviews Summary"
    ]

    tag_cols = [c for c in df.columns if c not in remove_cols]

    #Reduce features
    print("Reducing features to top 100 tags...")
    col_sums = df[tag_cols].sum().sort_values(ascending=False)
    top_100 = col_sums.iloc[:100].index.tolist()

    features = df[top_100].values.astype(np.float32)
    x = torch.tensor(features, dtype=torch.float)

    print("Reduced feature shape:", x.shape)  # e.g., (5115, 100)

    #Build sparse graph
    print("Building sparse similarity graph...")

    sim = cosine_similarity(x)                # compute similarity matrix
    rows, cols = np.where(sim > 0.9)          # keep only strong edges

    # Build edge list
    edge_list = []
    for r, c in zip(rows, cols):
        if r != c:
            edge_list.append([r, c])
            edge_list.append([c, r])          # undirected graph

    edge_index = torch.tensor(edge_list, dtype=torch.long).t()

    print(f"Nodes: {x.shape[0]} | Edges: {edge_index.shape[1]}")

    #Build Pytorch Geometric Data 
    data = Data(x=x, edge_index=edge_index)

    # Optional metadata for inference
    if "Title" in df.columns:
        data.titles = df["Title"].tolist()
    elif "title" in df.columns:
        data.titles = df["title"].tolist()

    if "appid" in df.columns:
        data.appids = df["appid"].tolist()

    return data
