import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

# 1. Data Initialization
# Node set V and Edge set E
num_nodes = 10  # Number of nodes
nodes = list(range(num_nodes))  # Node IDs from 0 to 9

# Generate link set and link capacity matrix
link_capacity = np.full((num_nodes, num_nodes), 100)  # All link capacities are 100G
np.fill_diagonal(link_capacity, 0)  # Self-loop capacity set to 0

# Generate traffic demand matrix D according to a fixed pattern, representing traffic demand between nodes
traffic_demand = np.zeros((num_nodes, num_nodes))
for i in nodes:
    for j in nodes:
        if i != j:
            # Fixed pattern: traffic demand is the absolute difference of node IDs plus a constant
            traffic_demand[i, j] = abs(i - j) + 10 + np.random.rand(1)*30

# Visualize the initial traffic distribution
# plt.figure(figsize=(7, 6))
# sns.heatmap(traffic_demand, annot=True, fmt=".1f", cmap="Blues")
# plt.title("Initial Traffic Distribution")
# plt.xlabel("Destination Node")
# plt.ylabel("Source Node")
# plt.tight_layout()
# plt.show()

# 2. Traffic Path Information Generation
# Use networkx to generate multiple link paths
G = nx.complete_graph(num_nodes)
traffic_paths = np.zeros((num_nodes, num_nodes, num_nodes, num_nodes))

for i in nodes:
    for j in nodes:
        if i != j:
            # Use networkx's shortest path algorithm to get the path from node i to node j
            shortest_path = nx.shortest_path(G, source=i, target=j)
            # Convert the path to link representation and update the traffic_paths matrix
            for k in range(len(shortest_path) - 1):
                u = shortest_path[k]
                v = shortest_path[k + 1]
                traffic_paths[i, j, u, v] = 1  # Path passes through link (u, v)

# Visualize some traffic path information (e.g., paths from node 0 to other nodes)
# fig, axes = plt.subplots(2, 5, figsize=(20, 8))
# for j in range(1, num_nodes):
#     sns.heatmap(traffic_paths[0, j], annot=True, fmt=".0f", cmap="Greens", ax=axes[(j-1) // 5, (j-1) % 5])
#     axes[(j-1) // 5, (j-1) % 5].set_title(f"Path from Node 0 to Node {j}")
#     axes[(j-1) // 5, (j-1) % 5].set_xlabel("Node")
#     axes[(j-1) // 5, (j-1) % 5].set_ylabel("Node")

# plt.tight_layout()
# plt.show()

# 3. Feature Vector Construction
# Combine adjacency matrix, traffic demand matrix, link capacity matrix, and traffic path matrix to obtain the feature vector
adjacency_matrix = nx.to_numpy_array(G)
features = np.concatenate([
    adjacency_matrix.flatten(),
    traffic_demand.flatten(),
    link_capacity.flatten(),
    traffic_paths.flatten()
])
features = torch.tensor(features, dtype=torch.float32).unsqueeze(0)  # Convert to PyTorch tensor and add batch dimension

# 4. Deep Neural Network Design
# Input features: adjacency matrix, traffic demand matrix, link capacity matrix, traffic path matrix
# Output: traffic allocation proportion for each link
input_dim = features.shape[1]  # Input dimension is the length of the feature vector
output_dim = num_nodes * num_nodes  # Output dimension is the number of links

class TrafficModel(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(TrafficModel, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, output_dim)
        self.softmax = nn.Softmax(dim=1)  # Use Softmax to ensure the traffic allocation proportion for each source-destination pair sums to 1

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        x = self.softmax(x)
        return x

# Initialize model
model = TrafficModel(input_dim, output_dim)

# Print model structure
print(model)

# 5. Loss Function Definition - Maximum Link Utilization (MLU)
def mlu_loss(y_pred, link_capacity):
    link_load = y_pred.view(num_nodes, num_nodes) * torch.tensor(link_capacity, dtype=torch.float32)
    # Calculate maximum link utilization
    capacities = torch.tensor(link_capacity, dtype=torch.float32)
    mlu = torch.max(link_load / (capacities + 1e-6))  # Avoid division by 0
    return mlu

# Optimizer settings
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Example forward propagation and loss calculation
output = model(features)
# Ensure that the traffic allocation proportion for each source-destination pair sums to 1 (strong constraint) and no self-loop traffic
output = output.view(num_nodes, num_nodes).clone()  # Use clone() to prevent in-place operation
output = output / output.sum(dim=1, keepdim=True)  # Normalize each row (i.e., traffic allocation for each source node)
output.fill_diagonal_(0)  # Set diagonal to 0 to ensure no self-loop traffic
# Incorporate link capacity into the allocation
output = output * torch.tensor(link_capacity, dtype=torch.float32) / torch.max(output * torch.tensor(link_capacity, dtype=torch.float32), torch.tensor(1e-6))
loss = mlu_loss(output, link_capacity)
print("Model Output:", output)
print("MLU Loss:", loss.item())

# 6. Train the model
num_epochs = 100
for epoch in range(num_epochs):
    model.train()
    optimizer.zero_grad()
    output = model(features)
    # Ensure that the traffic allocation proportion for each source-destination pair sums to 1 (strong constraint) and no self-loop traffic
    output = output.view(num_nodes, num_nodes).clone()  # Use clone() to prevent in-place operation
    output = output / output.sum(dim=1, keepdim=True)  # Normalize each row
    output.fill_diagonal_(0)  # Set diagonal to 0 to ensure no self-loop traffic
    # Incorporate link capacity into the allocation
    output = output * torch.tensor(link_capacity, dtype=torch.float32) / torch.max(output * torch.tensor(link_capacity, dtype=torch.float32), torch.tensor(1e-6))
    loss = mlu_loss(output, link_capacity)
    loss.backward()
    optimizer.step()
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# 7. Visualize the traffic allocation pattern after the decision
plt.figure(figsize=(7, 6))
sns.heatmap(output.detach().numpy(), annot=True, fmt=".2f", cmap="Reds")
plt.title("Traffic Allocation Pattern After Decision")
plt.xlabel("Destination Node")
plt.ylabel("Source Node")
plt.tight_layout()
plt.show()
