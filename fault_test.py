import numpy as np
from config import RESULT_DIR
import random
# 读取流量分配比例
with open('Result\\Facebook_pod_a\\Fault\\split.txt', 'r') as f:
    split_ratios = [float(line.strip()) for line in f.readlines()]

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
    [0, 100, 100, 100],
    [100, 0, 100, 100],
    [100, 100, 0, 100],
    [100, 100, 100, 0]
])

# 设置随机生成的流量需求张量的参数
time_steps = 10  # 生成的时间步数
num_nodes = 4

# 初始化用于存储每一时刻链路利用率的列表
time_link_utilizations = []

# 初始化流量需求张量
traffic_tensor = np.random.randint(50, 100, size=(time_steps, num_nodes, num_nodes))
for t in range(time_steps):
    for i in range(num_nodes):
        traffic_tensor[t][i][i] = 0  # 设置对角线为0，表示无自环流量

real_flow_throughput = 0  # 总的流量通过量
theory_demand_flow = 0  # 实际的需求流量

# 模拟每个时间步内的流量需求张量，并根据泊松分布引入链路故障
lambda_poisson = 1  # 泊松分布的参数（平均每时间步发生的链路故障数量）

# 模拟每个时间步内的流量需求张量，并随机引入链路故障
for t in range(time_steps):
    # 获取当前时间步的流量需求矩阵
    traffic_matrix = traffic_tensor[t]
    
    # 初始化链路流量矩阵
    link_flow = np.zeros((num_nodes, num_nodes))
    link_flow_fault = np.zeros((num_nodes, num_nodes))

    # 根据泊松分布引入链路故障
    num_failures = np.random.poisson(lambda_poisson)
    failed_links = []
    for _ in range(num_failures):
        failed_src = random.randint(0, num_nodes - 1)
        failed_dst = random.randint(0, num_nodes - 1)
        while failed_src == failed_dst or (failed_src, failed_dst) in failed_links or link_capacity[failed_src][failed_dst] == 0:
            failed_src = random.randint(0, num_nodes - 1)
            failed_dst = random.randint(0, num_nodes - 1)
        failed_links.append((failed_src, failed_dst))
    
    if failed_links:
        print(f"Time Step {t + 1}: Failed Links: {failed_links}")
    # 遍历每一对节点，计算链路流量, 考虑故障！！！
    split_index = 0
    for (src, dst), paths in routes.items():
        demand = traffic_matrix[src][dst]
        for path in paths:
            split_ratio = split_ratios[split_index]
            split_index += 1
            # 对于路径中的每一条链路，增加相应的流量
            for i in range(len(path) - 1):
                link_flow[path[i]][path[i + 1]] += demand * split_ratio
                if (path[i], path[i + 1]) not in failed_links:  # 跳过故障链路
                    link_flow_fault[path[i]][path[i + 1]] += demand * split_ratio

    # 计算当前时刻的链路利用率矩阵
    link_utilization = np.divide(link_flow, link_capacity, where=link_capacity != 0)
    time_link_utilizations.append(link_utilization)
    real_flow_throughput = np.sum(link_flow_fault)  # 累加当前时间步的总流量通过量
    theory_demand_flow = np.sum(link_flow)
    flow_throughput_rate = (real_flow_throughput / theory_demand_flow) * 100
    print("Flow Throughput Rate (%):")
    print(flow_throughput_rate)

# 输出每一时刻的链路利用率矩阵
# np.set_printoptions(suppress=True)
# for t, utilization in enumerate(time_link_utilizations):
#     print(f"Time Step {t + 1} Link Utilization Matrix:")
#     print(utilization)

