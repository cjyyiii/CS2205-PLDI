import numpy as np
import matplotlib.pyplot as plt

# 参数设置
num_links = 30         # 链路总数（根据图像估计）
num_days = 100        # 模拟两年（约与图像范围相同）
failure_prob = 0.01      # 每条链路的每日故障概率（可调整）
impactful_failure_prob = 0.01 # 故障为影响性故障的概率

# 蒙特卡罗模拟函数
def simulate_link_failures(num_links, num_days, failure_prob, impactful_failure_prob):
    # 初始化记录每日故障和影响性故障的数组
    daily_failures = np.zeros(num_days)
    impactful_failures = np.zeros(num_days)
    
    for day in range(num_days):
        # 确定每条链路当天是否发生故障
        failures = np.random.rand(num_links) < failure_prob
        daily_failures[day] = np.sum(failures)
        
        # 在发生故障的链路中确定哪些为影响性故障
        impactful_failures_today = np.random.rand(np.sum(failures)) < impactful_failure_prob
        impactful_failures[day] = np.sum(impactful_failures_today)
        
    return daily_failures, impactful_failures

# 运行模拟
daily_failures, impactful_failures = simulate_link_failures(num_links, num_days, failure_prob, impactful_failure_prob)

# 绘制结果
plt.figure(figsize=(14, 6))

# 绘制每日链路故障图
plt.subplot(1, 2, 1)
plt.plot(daily_failures, color='black', marker='o', markersize=1, linestyle='none')
plt.title("每日链路故障")
plt.xlabel("天数")
plt.ylabel("故障数量")

# 绘制影响性故障图
plt.subplot(1, 2, 2)
plt.plot(impactful_failures, color='red', marker='o', markersize=1, linestyle='none')
plt.title("影响性链路故障")
plt.xlabel("天数")
plt.ylabel("影响性故障数量")

plt.tight_layout()
plt.show()
