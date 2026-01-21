import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 设置Seaborn风格
sns.set(style="whitegrid")

# 创建示例数据
data = {
    'pr_time': [
        '2016-04', '2016-04', '2016-04', '2016-04', '2016-04', '2016-04',
        '2016-05', '2016-05', '2016-05', '2016-05', '2016-05', '2016-05',
        '2016-06', '2016-06', '2016-06', '2016-06', '2016-06', '2016-06'
    ],
    'pr_author': [
        'rxin', 'srowen', 'tdas', 'ueshin', 'vanzin', 'viirya',
        'rxin', 'srowen', 'tdas', 'ueshin', 'vanzin', 'viirya',
        'rxin', 'srowen', 'tdas', 'ueshin', 'vanzin', 'viirya'
    ],
    'emb': [
        0.1738328420300212, 0.17678421355113808, 0.14302455498482042,
        0.13702882746521722, 0.17761305175017, 0.13870571729070733,
        0.1800, 0.1750, 0.1400, 0.1350, 0.1780, 0.1405,
        0.1850, 0.1720, 0.1450, 0.1300, 0.1805, 0.1420
    ]
}

# 创建 DataFrame
pr_df = pd.DataFrame(data)
print("原始 DataFrame:")
print(pr_df)

# 步骤1：将 'pr_time' 转换为 datetime 类型
pr_df['pr_time'] = pd.to_datetime(pr_df['pr_time'], format='%Y-%m')
print("\n转换后的 DataFrame:")
print(pr_df)

# 步骤2：按 'pr_time' 和 'pr_author' 分组，并计算平均嵌入
# 如果每个 (pr_time, pr_author) 组合只有一个 emb 值，则无需聚合
# 但假设有多个 emb 值，需要计算平均

# 计算平均 emb
average_df = pr_df.groupby(['pr_time', 'pr_author'])['emb'].mean().reset_index()
print("\n按 pr_time 和 pr_author 计算的平均嵌入:")
print(average_df)

# 步骤3：绘制折线图

# 方法1：使用 Seaborn 的 lineplot


# 方法2：使用 Matplotlib 的原生绘图
plt.figure(figsize=(14, 8))

# 获取所有唯一的 pr_author
authors = average_df['pr_author'].unique()

for author in authors:
    # 筛选当前作者的数据
    author_data = average_df[average_df['pr_author'] == author]
    # 绘制折线
    plt.plot(author_data['pr_time'], author_data['emb'], marker='o', label=author)

plt.title('Author opinion', fontsize=16)
plt.xlabel('time', fontsize=14)
plt.ylabel('Emb', fontsize=14)
plt.xticks(rotation=45)
plt.legend(title='PR author', fontsize=12, title_fontsize=14)
plt.tight_layout()
plt.show()
plt.savefig('opinion.png', bbox_inches='tight')  # 保存为 PNG 格式
