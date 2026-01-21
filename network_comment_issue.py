import networkx as nx 
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# 加载数据
# pull_df = pd.read_csv('filtered_pull_ggplot2.csv')
issue_df = pd.read_csv('filtered_issue_spark_10.csv')

# commit_df = pd.read_csv('filtered_commit_ggplot2.csv')

# 创建空图
G = nx.Graph()
type_name='PULL_REQUEST'

# 添加用户节点与项目节点，同时添加权重
def add_interaction_weight(df, interaction_type):
    """
    为每个交互类型（Pull Request、Issue、Commit）添加边，并计算边的权重。
    权重根据评论次数、提交次数或参与次数来确定。
    """
    issues=[]
    for _, row in df.iterrows():
        # user = f"user_{row[f'{interaction_type}_AUTHOR']}"
        user = f"user_{row['COMMENT_AUTHOR']}"
        issue = f"{type_name}_{row[f'{type_name}_AUTHOR']}"
        # 创建用户-项目之间的边，如果已经存在则更新权重
        if G.has_edge(user, issue):
            G[user][issue]['weight'] += 1  # 每个互动增加权重1
        else:
            G.add_edge(user, issue, weight=1)  # 初始权重为1

# 添加Pull Request互动
# add_interaction_weight(pull_df, 'PULL_REQUEST')

# 添加Issue互动
add_interaction_weight(issue_df, 'ISSUE')

# 添加Commit互动
# add_interaction_weight(commit_df, 'COMMIT')

# 可视化网络
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G, k=0.15, iterations=20)  # 使用Spring布局，调整节点间距

# 边的坐标和权重
edge_x = []
edge_y = []
edge_weights = []  # 用于存储每条边的权重（互动次数）

for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_y.append(y0)
    edge_y.append(y1)

    # 将权重按边的权重映射为边的粗细
    edge_weights.append(G[edge[0]][edge[1]]['weight'])

# 节点的坐标和标签
node_x = []
node_y = []
node_color = []  # 用于存储每个节点的颜色（即其交互强度）
user_nodes = []  # 用户节点集合
issue_nodes = []  # 问题节点集合

for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)

    # 分配用户和问题节点
    if node.startswith('user'):  # 假设用户节点的名称以"user"开头
        user_nodes.append(node)
        node_color.append('blue')  # 用户节点颜色为蓝色
    else:
        issue_nodes.append(node)
        node_color.append('green')  # 问题节点颜色为绿色

# 创建 Plotly 图形
edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888', backoff=0.5),
    hoverinfo='none',
    mode='lines',
    line_shape='linear',
    marker=dict(size=edge_weights)  # 边的粗细根据权重设置
)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='YlGnBu',  # 颜色映射
        size=10,
        colorbar=dict(thickness=15, title='Node Interactions', xanchor='left', titleside='right')
    )
)

# 显示节点名称和颜色映射
node_text = []
for node in G.nodes():
    node_text.append(f'Node: {node}')
node_trace.marker.color = node_color
node_trace.text = node_text

# 创建布局
layout = go.Layout(
    title='Interactive Network Graph of User-Project Interactions',
    titlefont_size=16,
    showlegend=False,
    hovermode='closest',
    xaxis=dict(showgrid=False, zeroline=False),
    yaxis=dict(showgrid=False, zeroline=False)
)

# 创建并保存交互式图
fig = go.Figure(data=[edge_trace, node_trace], layout=layout)

# 保存为 HTML 文件
fig.write_html('interactive_network_graph_with_weighted_edges.html')

# 显示图形
fig.show()
