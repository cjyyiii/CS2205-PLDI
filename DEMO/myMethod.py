import numpy as np
import matplotlib.pyplot as plt

# 函数：计算单条链路在时间t时的故障概率
def link_failure_probability(lambda_i, t):
    return 1 - np.exp(-lambda_i * t)

# 函数：计算整个系统在时间t时至少一条链路发生故障的概率
def system_failure_probability(lambdas, t):
    failure_prob = 1 - np.prod([np.exp(-lambda_i * t) for lambda_i in lambdas])
    return failure_prob

# 设置参数
n = 3  # 链路数量
lambdas = [0.2, 0.5, 0.3]  # 每条链路的故障速率（λ）
t_values = np.linspace(0, 10, 100)  # 时间范围，从0到10，取100个时间点

# 存储每条链路的故障概率和系统故障概率
link_failures = np.array([[link_failure_probability(lambda_i, t) for t in t_values] for lambda_i in lambdas])
system_failures = np.array([system_failure_probability(lambdas, t) for t in t_values])

# 绘制每条链路的故障概率
plt.figure(figsize=(10, 6))
for i in range(n):
    plt.plot(t_values, link_failures[i], label=f"Link {i+1} (λ={lambdas[i]})")

# 绘制系统故障概率
plt.plot(t_values, system_failures, label="System Failure", color='black', linestyle='--')

# 图形设置
plt.title("Link Failure Probabilities and System Failure Probability Over Time")
plt.xlabel("Time (t)")
plt.ylabel("Failure Probability")
plt.legend()
plt.grid(True)
plt.show()
