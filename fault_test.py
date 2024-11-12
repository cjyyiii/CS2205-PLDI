import numpy as np
from config import RESULT_DIR
import random
import torch
import glob 

# 读取流量分配比例
with open('Result\\Facebook_pod_a\\Fault\\split.txt', 'r') as f:
    split_ratios = [float(line.strip()) for line in f.readlines()]

traffic_matrix = []
traffic_opt = []

num_nodes = 4

# hist_files = 'D:\\sjtu\\fault\\Data\\Facebook_pod_a\\test\\*.hist'
hist_files = 'D:\\SJTU_NETWORK\\sjtu\\fault\\Data\\Facebook_pod_a\\test\\*.hist'

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
# 可以根据具体情况进行修改
link_capacity = np.array([
    [0, 10000, 10000, 10000],
    [10000, 0, 10000, 10000],
    [10000, 10000, 0, 10000],
    [10000, 10000, 10000, 0]
])
for trial in range(0,10):
    # 初始化用于存储每一时刻链路利用率的列表
    time_link_utilizations = []

    real_flow_throughput = 0  # 总的流量通过量
    theory_demand_flow = 0  # 实际的需求流量
    real_throughput_total=0
    theory_demand_total=0
    # 模拟每个时间步内的流量需求张量，并根据泊松分布引入链路故+-------------障
    lambda_poisson = 0.5 #0.124 # 泊松分布的参数（平均每时间步发生的链路故障数量）
    flow_throughput_rate_total=0

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
        # failed_links = []
        for _ in range(num_failures):
            failed_src = random.randint(0, num_nodes - 1)
            failed_dst = random.randint(0, num_nodes - 1)
            while failed_src == failed_dst or (failed_src, failed_dst) in failed_links or link_capacity[failed_src][failed_dst] == 0:
                failed_src = random.randint(0, num_nodes - 1)
                failed_dst = random.randint(0, num_nodes - 1)
            failed_links.append((failed_src, failed_dst))
            link_recovery[(failed_src,failed_dst)] = t + link_fault_duration

        for i in range(0,num_nodes):
            for j in range(0,num_nodes):
                if ((i,j) in link_recovery):
                    if(t == link_recovery[(i,j)]):
                        failed_links.remove((i, j))
        # 遍历每一对节点，计算链路流量, 考虑故障！！！
        split_index = 0
        failed_path=[]
        bad_path_flag=0
        for (src, dst), paths in routes.items():
            demand = traffic_matrix[src][dst]
            for path in paths:
                split_ratio = split_ratios[split_index]
                split_index += 1
                # 对于路径中的每一条链路，增加相应的流量
                for i in range(len(path) - 1):
                    link_flow[path[i]][path[i + 1]] += demand * split_ratio
                    if ((path[i-1], path[i]) in failed_links) | ((path[i-1], path[i]) == failed_path):
                        failed_path=(path[i], path[i+1])
                    if (path[i], path[i + 1]) not in failed_links:  # 跳过故障链路
                        if(path[i], path[i+1]) != failed_path:
                            link_flow_fault[path[i]][path[i + 1]] += demand * split_ratio
                    if(path[i], path[i+1]) in failed_links:
                        bad_path_flag=1
                    if(bad_path_flag==1):
                        # print(f"Time Step {t + 1}: Failed Links: {failed_links}")
                        # print(f"Time Step {t + 1}: Failed Path: {path}")
                        bad_path_flag = 0
        # 计算当前时刻的链路利用率矩阵
        link_utilization = np.divide(link_flow, link_capacity, where=link_capacity != 0)
        time_link_utilizations.append(link_utilization)
        real_flow_throughput = np.sum(link_flow_fault)  # 累加当前时间步的总流量通过量
        theory_demand_flow = np.sum(link_flow)      
        flow_throughput_rate = (real_flow_throughput / theory_demand_flow) * 100
        real_throughput_total += real_flow_throughput
        theory_demand_total += theory_demand_flow
        # if failed_links:
        #     print("Flow Throughput Rate (%):")
        #     print(flow_throughput_rate)
    flow_throughput_rate_total=real_throughput_total/theory_demand_total
    # print("Total Flow Throughput Rate (%):")
    print(flow_throughput_rate_total)

