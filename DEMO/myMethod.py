import numpy as np
import random
import torch
import glob
import os

# 读取流量分配比例
with open('Result\\Facebook_pod_a\\Fault\\split.txt', 'r') as f:
    split_ratios = [float(line.strip()) for line in f.readlines()]

traffic_matrix = []
traffic_opt = []

num_nodes = 4

hist_files = 'D:\\sjtu\\fault\\Data\\Facebook_pod_a\\test\\*.hist'

for file in glob.glob(hist_files):
    with open(file, 'r') as f:
        for line in f:
            matrix = torch.tensor(list(map(float, line.strip().split()))).reshape(num_nodes, num_nodes)
            traffic_matrix.append(matrix)

traffic_tensor = torch.stack(traffic_matrix)
time_steps = traffic_tensor.shape[0]
print(time_steps)

# 路由表（路径选择）
routes = {
    (0, 1): [(0, 1), (0, 2, 1), (0, 3, 1)],
    (0, 2): [(0, 2), (0, 1, 2), (0, 3, 2)],
    (0, 3): [(0, 3), (0, 1, 3), (0, 2, 3)],
    (1, 0): [(1, 0), (1, 2, 0), (1, 3, 0)],
    (1, 2): [(1, 2), (1, 0, 2), (1, 3, 2)],
    (1, 3): [(1, 3), (1, 0, 3), (1, 2, 3)],
    (2, 0): [(2, 0), (2, 1, 0), (2, 3, 0)],
    (2, 1): [(2, 1), (2, 0, 1), (2, 3, 1)],
    (2, 3): [(2, 3), (2, 0, 3), (2, 1, 3)],
    (3, 0): [(3, 0), (3, 1, 0), (3, 2, 0)],
    (3, 1): [(3, 1), (3, 0, 1), (3, 2, 1)],
    (3, 2): [(3, 2), (3, 0, 2), (3, 1, 2)],
}

# 假设链路容量矩阵（单位：单位流量）
link_capacity = np.array([
    [0, 100000, 100000, 100000],
    [100000, 0, 100000, 100000],
    [100000, 100000, 0, 100000],
    [100000, 100000, 100000, 0]
])

# 流量转移函数，处理链路故障并检查带宽限制
def transfer_flow(link_flow, demand, path, split_ratio, failed_links):
    for i in range(len(path) - 1):
        # 检查链路是否故障，跳过故障链路
        if (path[i], path[i + 1]) in failed_links:
            continue  # 这个链路已经故障，跳过
        
        # 将流量分配到链路
        link_flow[path[i]][path[i + 1]] += demand * split_ratio
        
        # 检查是否超过链路容量，若超过则丢弃超出部分
        if link_flow[path[i]][path[i + 1]] > link_capacity[path[i]][path[i + 1]]:
            link_flow[path[i]][path[i + 1]] = link_capacity[path[i]][path[i + 1]]  # 丢弃超出的流量

# 主模拟过程
for trial in range(0, 1):
    # 初始化用于存储每一时刻链路利用率的列表
    time_link_utilizations = []

    real_flow_throughput = 0  # 总的流量通过量
    theory_demand_flow = 0  # 实际的需求流量
    real_throughput_total = 0
    theory_demand_total = 0
    # 模拟每个时间步内的流量需求张量，并根据泊松分布引入链路故障
    lambda_poisson = 0.124  # 泊松分布的参数（平均每时间步发生的链路故障数量）
    flow_throughput_rate_total = 0

    failed_links = []
    link_recovery = {}
    link_fault_duration = 5
    
    # 模拟每个时间步内的流量需求张量，并随机引入链路故障
    for t in range(time_steps):
        # 获取当前时间步的流量需求矩阵
        traffic_matrix = traffic_tensor[t]
        
        # 初始化链路流量矩阵
        link_flow = np.zeros((num_nodes, num_nodes))
        link_flow_fault = np.zeros((num_nodes, num_nodes))

        # 根据泊松分布引入链路故障
        num_failures = np.random.poisson(lambda_poisson)
        for _ in range(num_failures):
            failed_src = random.randint(0, num_nodes - 1)
            failed_dst = random.randint(0, num_nodes - 1)
            while failed_src == failed_dst or (failed_src, failed_dst) in failed_links or link_capacity[failed_src][failed_dst] == 0:
                failed_src = random.randint(0, num_nodes - 1)
                failed_dst = random.randint(0, num_nodes - 1)
            failed_links.append((failed_src, failed_dst))
            link_recovery[(failed_src, failed_dst)] = t + link_fault_duration

        # 恢复链路故障
        for i in range(0, num_nodes):
            for j in range(0, num_nodes):
                if (i, j) in link_recovery and t == link_recovery[(i, j)]:
                    failed_links.remove((i, j))

        # 遍历每一对节点，计算链路流量, 考虑故障
        split_index = 0
        for (src, dst), paths in routes.items():
            demand = traffic_matrix[src][dst]
            for path in paths:
                split_ratio = split_ratios[split_index]
                split_index += 1
                # 使用流量转移函数处理链路故障
                transfer_flow(link_flow, demand, path, split_ratio, failed_links)

        # 计算当前时刻的链路利用率矩阵
        link_utilization = np.divide(link_flow, link_capacity, where=link_capacity != 0)
        time_link_utilizations.append(link_utilization)
        real_flow_throughput = np.sum(link_flow_fault)  # 累加当前时间步的总流量通过量
        theory_demand_flow = np.sum(link_flow)
        flow_throughput_rate = (real_flow_throughput / theory_demand_flow) * 100
        real_throughput_total += real_flow_throughput
        theory_demand_total += theory_demand_flow

    flow_throughput_rate_total = real_throughput_total / theory_demand_total
    print(f"Total Flow Throughput Rate (%): {flow_throughput_rate_total}")
