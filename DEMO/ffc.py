from gurobipy import Model, GRB, quicksum
import numpy as np
import matplotlib.pyplot as plt

# ==============================
# 设置参数
# ==============================

# 网络拓扑和参数
V = ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8']  # 8个交换机（节点）
E = ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10']  # 10条链路
T = ['t1', 't2', 't3', 't4', 't5', 't6']  # 6条隧道
F = ['flow1', 'flow2', 'flow3', 'flow4']  # 4个流量需求

# 链路容量 (以 Gbps 为单位)
c = {'e1': 100, 'e2': 120, 'e3': 80, 'e4': 90, 'e5': 110, 'e6': 130, 'e7': 140, 'e8': 150, 'e9': 100, 'e10': 110}

# 流量需求 (以 Gbps 为单位)
d = {'flow1': 70, 'flow2': 50, 'flow3': 30, 'flow4': 20}

# 隧道到链路的映射
L = {
    't1': ['e1', 'e2'],
    't2': ['e3', 'e4'],
    't3': ['e5', 'e6'],
    't4': ['e7', 'e8'],
    't5': ['e9'],
    't6': ['e10']
}

# 故障情况下的最大流量上限
beta = {
    ('s1', 'e1'): 50, ('s2', 'e2'): 60, ('s3', 'e3'): 55, ('s4', 'e4'): 65,
    ('s5', 'e5'): 70, ('s6', 'e6'): 80, ('s7', 'e7'): 90, ('s8', 'e8'): 85,
    ('s1', 'e9'): 45, ('s2', 'e10'): 55
}

# ==============================
# 优化函数定义
# ==============================

# 带FFC的优化
def optimize_with_ffc(fault_links):
    model = Model("TrafficEngineeringWithFFC")
    a = model.addVars(F, T, name="a", lb=0)
    lambda_v = model.addVars(V, vtype=GRB.BINARY, name="lambda")

    # 目标函数
    model.setObjective(quicksum(a[f, t] for f in F for t in T), GRB.MAXIMIZE)

    # 链路容量约束，考虑故障链路
    for e in E:
        if e not in fault_links:
            model.addConstr(
                quicksum(a[f, t] for f in F for t in T if e in L[t]) <= c[e], 
                name=f"LinkCapacity_{e}"
            )

    # 流量需求约束
    for f in F:
        model.addConstr(
            quicksum(a[f, t] for t in T) >= d[f], 
            name=f"FlowDemand_{f}"
        )

    # 控制平面故障约束
    for e in E:
        if e not in fault_links:
            model.addConstr(
                quicksum(lambda_v[v] * (beta[v, e] - quicksum(a[f, t] for f in F for t in T if e in L[t])) 
                         for v in V if (v, e) in beta) <= c[e] - quicksum(a[f, t] for f in F for t in T if e in L[t]),
                name=f"ControlPlaneFault_{e}"
            )

    # 数据平面故障约束
    for f in F:
        for t in T:
            model.addConstr(
                a[f, t] >= d[f] / (len(T) - len(fault_links)),
                name=f"DataPlaneFault_{f}_{t}"
            )

    model.optimize()
    
    link_usage = {e: (sum(a[f, t].x for f in F for t in T if e in L[t]) if e not in fault_links else 0) for e in E}
    
    return link_usage

# 不带FFC的优化（修正后的无故障和故障情况下的流量分配）
def passive_switching(fault_links):
    link_usage = {e: 0 for e in E}  # 初始化所有链路的流量为 0

    for t in T:
        for f in F:
            # 检查该隧道是否包含故障链路
            affected_links = [e for e in L[t] if e in fault_links]
            
            if affected_links:
                # 当隧道中的某些链路发生故障时，将流量均匀分配到剩余可用链路
                available_links = [e for e in L[t] if e not in fault_links]
                if available_links:
                    # 将流量均匀分配到剩余的可用链路，并确保流量总量等于需求
                    flow_per_link = d[f] / len(available_links)
                    for e in available_links:
                        link_usage[e] += flow_per_link
            else:
                # 无故障的情况下，将流量均匀分配到隧道的所有链路上，并确保流量总量等于需求
                flow_per_link = d[f] / len(L[t])
                for e in L[t]:
                    link_usage[e] += flow_per_link
    
    return link_usage



# ==============================
# 仿真时间步
# ==============================

time_steps = ["0-2 seconds", "2-4 seconds"]
ffc_results = []
no_ffc_results = []

# 正常情况下（0-2秒，没有故障）
ffc_results.append(optimize_with_ffc([]))
no_ffc_results.append(passive_switching([]))

# 链路 e1 断开（2-4秒）
ffc_results.append(optimize_with_ffc(['e1']))
no_ffc_results.append(passive_switching(['e1']))

# ==============================
# 绘制对比图
# ==============================

fig, axes = plt.subplots(2, len(E)//2, figsize=(18, 12), sharey=True)
axes = axes.flatten()
time_labels = time_steps

# 遍历每条链路并绘制条形图
for i, e in enumerate(E):
    # 获取带 FFC 和不带 FFC 的流量数据
    ffc_usage = [ffc_results[t][e] for t in range(len(time_steps))]
    no_ffc_usage = [no_ffc_results[t][e] for t in range(len(time_steps))]
    capacity = c[e]
    
    # 设置 x 轴的位置
    x = np.arange(len(time_labels))
    bar_width = 0.35

    # 绘制带 FFC 的条形图
    bars1 = axes[i].bar(x - bar_width / 2, ffc_usage, bar_width, label="With FFC", color="green")
    # 绘制不带 FFC 的条形图
    bars2 = axes[i].bar(x + bar_width / 2, no_ffc_usage, bar_width, label="Without FFC", color="orange")
    
    # 绘制链路容量的水平线
    axes[i].axhline(y=capacity, color='red', linestyle='--', linewidth=1, label="Capacity" if i == 0 else "")

    # 标记超载的条形图
    for bar, usage in zip(bars1, ffc_usage):
        if usage > capacity:
            bar.set_color('red')
    for bar, usage in zip(bars2, no_ffc_usage):
        if usage > capacity:
            bar.set_color('red')

    # 设置标题和轴标签
    axes[i].set_title(f"Link {e}")
    axes[i].set_xticks(x)
    axes[i].set_xticklabels(time_labels)
    axes[i].set_ylim(0, max(capacity, max(ffc_usage + no_ffc_usage)) * 1.2)
    axes[i].set_ylabel("Traffic (Gbps)")
    
# 图例设置
fig.suptitle("Traffic Distribution on Links Over Time with and without FFC")
fig.legend(loc="upper center", ncol=3)
plt.tight_layout(rect=[0, 0, 1, 0.95])

plt.show()
