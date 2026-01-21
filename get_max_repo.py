import pandas as pd

# 假设你已经加载了 issue 数据集
issue_df = pd.read_csv('pr_Python.csv')

# 统计每个项目的 issue 数量
repo_issue_counts = issue_df.groupby(['REPO_NAME', 'REPO_OWNER']).size().reset_index(name='COUNT')

# 按照 issue 数量排序，获取最多的 repo
top_repos = repo_issue_counts.sort_values(by='COUNT', ascending=False)

# 输出最多 issue 的项目
print(top_repos.head(10))  # 获取前 10 个项目
