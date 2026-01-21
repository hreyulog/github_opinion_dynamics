import networkx as nx
import pandas as pd
import plotly.graph_objects as go

# 加载数据
pull_df = pd.read_csv('filtered_pull_ggplot2.csv')
issue_df = pd.read_csv('filtered_issue_ggplot2.csv')
commit_df = pd.read_csv('filtered_commit_ggplot2.csv')

# 创建空图
G = nx.Graph()

# 添加用户节点与项目节点，同时添加权重
def add_interaction_weight(df, interaction_type):
    """
    为每个交互类型（Pull Request、Issue、Commit）添加边，并计算边的权重。
    权重根据评论次数、提交次数或参与次数来确定。
    """
    for _, row in df.iterrows():
        user = row[f'{interaction_type}_AUTHOR']
        repo = row['REPO_NAME']
        
        # 创建用户-项目之间的边，如果已经存在则更新权重
        if G.has_edge(user, repo):
            G[user][repo]['weight'] += 1  # 每个互动增加权重1
        else:
            G.add_edge(user, repo, weight=1)  # 初始权重为1

        # 处理评论部分
        comment_author = row['COMMENT_AUTHOR']
        if pd.notna(comment_author):  # 确保评论作者不为空
            if G.has_edge(comment_author, repo):
                G[comment_author][repo]['weight'] += 1  # 评论互动增加权重
            else:
                G.add_edge(comment_author, repo, weight=1)  # 初始评论互动边

# 添加Pull Request互动
add_interaction_weight(pull_df, 'PULL_REQUEST')

# 添加Issue互动
add_interaction_weight(issue_df, 'ISSUE')

# 添加Commit互动
add_interaction_weight(commit_df, 'COMMIT')

# 可视化网络
import matplotlib.pyplot as plt
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G, k=0.15, iterations=20)  # 使用Spring布局，调整节点间距
edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_y.append(y0)
    edge_y.append(y1)

# 提取节点位置和节点标签
node_x = []
node_y = []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)

# 创建 Plotly 图形
edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines'
)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='YlGnBu',
        size=10,
        colorbar=dict(thickness=15, title='Node Connections', xanchor='left', titleside='right')
    )
)

# 显示节点名称
node_text = []
for node in G.nodes():
    node_text.append(f'Node {node}')
node_trace.marker.color = list(range(len(G.nodes())))
node_trace.text = node_text

# 创建布局
layout = go.Layout(
    title='Interactive Network Graph',
    titlefont_size=16,
    showlegend=False,
    hovermode='closest',
    xaxis=dict(showgrid=False, zeroline=False),
    yaxis=dict(showgrid=False, zeroline=False)
)

# 创建并保存交互式图
fig = go.Figure(data=[edge_trace, node_trace], layout=layout)

# 保存为 HTML 文件
fig.write_html('interactive_network_graph.html')

# 显示图形
fig.show()