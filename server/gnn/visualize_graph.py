import torch
import torch.serialization
from torch_geometric.data.data import Data, DataEdgeAttr, DataTensorAttr
from torch_geometric.data.storage import GlobalStorage
from torch_geometric.utils import to_networkx
import networkx as nx
import matplotlib.pyplot as plt

# Enable loading PyG graph
torch.serialization.add_safe_globals([
    Data, DataEdgeAttr, DataTensorAttr, GlobalStorage
])

# Load graph
data = torch.load("graph_data.pt", map_location="cpu")

# Convert to NetworkX (only a subset for visualization)
G = to_networkx(data, to_undirected=True)

# Take a small subgraph (first 200 nodes)
small_nodes = list(G.nodes())[:200]
H = G.subgraph(small_nodes)

# Take the largest connected component
components = list(nx.connected_components(G))
largest_cc = max(components, key=len)

# Use up to 200 nodes from that connected component
small_nodes = list(largest_cc)[:200]
H = G.subgraph(small_nodes)

# Use a spring layout (more meaningful than circular)
pos = nx.spring_layout(H, seed=42)

plt.figure(figsize=(10, 8))
nx.draw(H, pos, node_size=20, width=0.3)
plt.title("Graph Visualization (Largest Connected Component Subset)")
plt.savefig("graph_lcc.png", dpi=300)
print("Saved graph to graph_lcc.png")

plt.figure(figsize=(10, 8))
nx.draw(H, node_size=30, width=0.3)
plt.title("Graph Visualization (Subset of 200 Nodes)")
plt.savefig("graph_subset.png", dpi=300)
print("Saved graph to graph_subset.png")

