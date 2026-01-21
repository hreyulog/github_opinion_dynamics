import pandas as pd
import requests
from tqdm import tqdm
import torch
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler,RobustScaler
from sklearn.preprocessing import StandardScaler, QuantileTransformer

from matplotlib import rcParams
from sklearn.manifold import TSNE, trustworthiness, LocallyLinearEmbedding
from umap import UMAP

# 设置全局字体参数

rcParams['font.size'] = 15  # 默认字体大小
def compute_mean_emb(emb_series):
    # 堆叠所有嵌入向量
    stacked_emb = np.vstack(emb_series)
    # 计算平均嵌入
    mean_emb = np.mean(stacked_emb, axis=0)
    return mean_emb

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main(repo_name):
    pr_df = pd.read_csv(f'pr_time_{repo_name}.csv')
    print("DataFrame 行数:", pr_df.shape[0])

    # 加载嵌入数组
    pr_emb = np.load(f'pr_emb_{repo_name}.npy')
    print("Embeddings 形状:", pr_emb.shape)
    pr_df['emb']=pr_emb.tolist()
    pr_df['emb'] = pr_df['emb'].apply(np.array)
    print(pr_df)
    average_df = pr_df.groupby(['pr_time', 'pr_author'])['emb'].apply(compute_mean_emb).reset_index()
    average_df['emb'] = average_df['emb'].apply(lambda x: x.tolist())
    np.save(f'author_time_emb_{repo_name}.npy', np.stack(average_df['emb'].values))

    emb_pca_scaled=np.stack(average_df['emb'].values)
    from sklearn.decomposition import PCA,FastICA
    # fastica=UMAP(n_components=1)
    # emb_pca_scaled = fastica.fit_transform(np.stack(average_df['emb'].values))
    scaler = StandardScaler()
    emb_pca_scaled = scaler.fit_transform(emb_pca_scaled)
    # tsne=TSNE(n_components=1)
    # emb_pca_scaled = tsne.fit_transform(np.stack(average_df['emb'].values))
    pca = PCA(n_components=1)
    emb_pca_scaled = pca.fit_transform(emb_pca_scaled)
    # emb_pca_scaled=np.stack(average_df['emb'].values)
    
    # standard_emb = scaler.fit_transform()
    emb_pca_scaled = QuantileTransformer(output_distribution='normal').fit_transform(emb_pca_scaled)
    scaler = MinMaxScaler()
    emb_pca_scaled = scaler.fit_transform(emb_pca_scaled)

    average_df['emb']=emb_pca_scaled

    print(average_df)
    average_df.to_csv(f'author_time_{repo_name}.csv', index=False)
    # plt.rc('font',family='Times New Roman')
    fig,ax = plt.subplots()
    linewidth = 2
    authors = average_df['pr_author'].unique()
    average_df['pr_time'] = pd.to_datetime(average_df['pr_time'])
    df_common = average_df.dropna(how='any').sort_values('pr_time')
    print(df_common)
    times = sorted(list(set(df_common['pr_time'].tolist())))
    consecutive_groups = []
    if times:
        current_group = [times[0]]
        for t in times[1:]:
            filtered_data = df_common[df_common['pr_time'] == t]
            if len(filtered_data)==len(authors):
                if (t == current_group[-1]+ pd.DateOffset(months=1)):
                    current_group.append(t)
                else:
                    consecutive_groups.append(current_group)
                    current_group = [t]
        consecutive_groups.append(current_group)
    max_con=0
    start=0
    end=0
    for idx, group in enumerate(consecutive_groups, 1):
        print(f"连续时间段 {idx}: 开始于 {group[0].strftime('%Y-%m-%d')}, 结束于 {group[-1].strftime('%Y-%m-%d')}, 共 {len(group)} 月")
        filtered_data = df_common[df_common['pr_time'].isin(group)]
        if max_con<len(group):
            max_con=len(group)
            start=group[0]
            end=group[-1]
    average_df = average_df[(average_df['pr_time'] >= start) & (average_df['pr_time'] <= end)]
    start=start+ pd.DateOffset(months=4)
    end=start+pd.DateOffset(months=12)
    average_df = average_df[(average_df['pr_time'] >= start) & (average_df['pr_time'] <= end)]
    average_df=average_df.sort_values('pr_time')
    for author in authors:
        author_data = average_df[average_df['pr_author'] == author]
        ax.plot(author_data['pr_time'], author_data['emb'], marker='o', label=author,linewidth=linewidth)

    # plt.title(f'Author opinion of REPO \'{repo_name}\'', fontsize=16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.set_xlabel('Time')
    ax.set_ylabel('Emb')
    plt.xticks(rotation=30)
    legend = ax.legend(fontsize=15,edgecolor='black',loc='upper center',bbox_to_anchor=(0.5, -0.3), ncol=3)

    ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
    plt.savefig(f'opinion_{repo_name}_all3.png', bbox_inches='tight', dpi=300)
    plt.show()
    pivot_df = average_df.pivot(index='pr_time', columns='pr_author', values='emb').reset_index()
    print(pivot_df)
    pivot_df.to_csv(f'{repo_name}_for_mathematica.csv', index=False)

if __name__=="__main__":
    repo_names=['swift']
    #,'pytorch','ceph'
    # repo_names=['pytorch','ceph','swift']
    for repo_name in repo_names:
        main(repo_name)