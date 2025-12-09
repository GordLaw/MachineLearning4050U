import torch
import torch.serialization
from torch_geometric.data import Data
from torch_geometric.data.data import DataEdgeAttr, DataTensorAttr
from torch_geometric.data.storage import GlobalStorage

from gnn_model import GameGNN, DotProductLinkPredictor

MODEL_PATH = "gnn_model.pth"
GRAPH_PATH = "graph_data.pt"

# Allow PyG objects to load safely
torch.serialization.add_safe_globals([
    Data,
    DataEdgeAttr,
    DataTensorAttr,
    GlobalStorage
])
data: Data = torch.load(GRAPH_PATH, map_location="cpu")
print("Graph loaded!")
print("Node feature shape:", data.x.shape)


ckpt = torch.load(MODEL_PATH, map_location="cpu")

# Extract hyperparameters
in_channels = ckpt["in_channels"]          # input dim
hidden_dim  = ckpt["hidden_dim"]           # hidden size (usually 64)
embed_dim   = ckpt["embed_dim"]            # output embedding dim (64)

print("\nHyperparameters from checkpoint:")
print("in_channels:", in_channels)
print("hidden_dim:", hidden_dim)
print("embed_dim:", embed_dim)


model = GameGNN(
    in_channels=in_channels,
    hidden_channels=hidden_dim,
    out_channels=embed_dim
)

# Predictor
predictor = DotProductLinkPredictor()


model.load_state_dict(ckpt["model_state_dict"])
predictor.load_state_dict(ckpt["predictor_state_dict"])

model.eval()
predictor.eval()

print("\nModel loaded successfully!")
