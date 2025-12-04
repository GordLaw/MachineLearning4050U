import torch
from torch import nn
from torch_geometric.nn import SAGEConv


class GameGNN(nn.Module):
    def __init__(self, in_channels: int, hidden_channels: int = 64,
                 out_channels: int = 64, dropout: float = 0.2):
        super().__init__()
        self.conv1 = SAGEConv(in_channels, hidden_channels)
        self.conv2 = SAGEConv(hidden_channels, out_channels)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, edge_index):
        # x: [num_nodes, in_channels]
        # edge_index: [2, num_edges]
        x = self.conv1(x, edge_index)
        x = torch.relu(x)
        x = self.dropout(x)
        x = self.conv2(x, edge_index)
        return x  # node embeddings


class DotProductLinkPredictor(nn.Module):
    """
    Scores pairs of nodes by dot product of their embeddings.
    Used for link prediction / similarity learning.
    """
    def forward(self, z_i, z_j):
        # z_i, z_j: [num_pairs, embed_dim]
        return (z_i * z_j).sum(dim=-1)