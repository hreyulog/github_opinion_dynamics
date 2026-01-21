import pandas as pd
import requests
from tqdm import tqdm
import torch
import numpy as np
def get_pytorch_serve_embeddings(texts, model, url):
    post_url = f'{url}{model}'
    headers = {'Content-Type': 'application/json'}
    embeddings = []
    for text in tqdm(texts):
        # print(text)
        # print(len(text))
        # if len(text) == 0:
        #     zero_tensor = torch.zeros(embed.size)
        #     embeddings.append(zero_tensor)
        # else:
        if pd.isna(text):
            text=''
        response = requests.post(post_url, headers=headers, json=text)
        embed=torch.Tensor([response.json()])
        embeddings.append(embed)
    return embeddings

def main(repo_name):
    url='http://localhost:8080/predictions/'
    model='emb_comp'
    issue_df = pd.read_csv(f'{repo_name}_diff.csv')
    issue_df['new_code_emb']=get_pytorch_serve_embeddings(issue_df['new_code'],model,url)
    issue_df['old_code_emb']=get_pytorch_serve_embeddings(issue_df['old_code'],model,url)
    issue_df['difference_emb'] = issue_df.apply(lambda row: row['new_code_emb'] - row['old_code_emb'], axis=1)

    np.save(f'new_code_emb_{repo_name}.npy', np.stack(issue_df['new_code_emb'].values))
    np.save(f'old_code_emb_{repo_name}.npy', np.stack(issue_df['old_code_emb'].values))
    np.save(f'difference_code_emb_{repo_name}.npy', np.stack(issue_df['difference_emb'].values))


if __name__=="__main__":
    repo_names=['swift','pytorch','ceph']
    for repo_name in repo_names:
        main(repo_name)
    

    # issue_df.to_csv('pr_patch_diff_emb.csv', index=False)
