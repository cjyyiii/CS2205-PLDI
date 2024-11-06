import numpy as np
import torch
import glob 

num_of_nodes=4

traffic_matrix = []
traffic_opt = []

hist_files = 'D:\\sjtu\\fault\\Data\\Facebook_pod_a\\train\\*.hist'
opt_files = 'D:\\sjtu\\fault\\Data\\Facebook_pod_a\\train\\*.opt'

for file in glob.glob(hist_files):
    with open(file, 'r') as f:
        for line in f:
            matrix = torch.tensor(list(map(float, line.strip().split()))).reshape(num_of_nodes, num_of_nodes)
            traffic_matrix.append(matrix)

for file in glob.glob(opt_files):
    with open(file, 'r') as f:
        for line in f:
            unit = torch.tensor(list(map(float, line.strip().split())))
            traffic_opt.append(unit)


traffic_tensor = torch.stack(traffic_matrix)
opt_tensor = torch.stack(traffic_opt)

# print(opt_tensor.size())