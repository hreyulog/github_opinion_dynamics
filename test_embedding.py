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
    # issue_df['new_code_emb']=get_pytorch_serve_embeddings(issue_df['new_code'],model,url)
    # issue_df['old_code_emb']=get_pytorch_serve_embeddings(issue_df['old_code'],model,url)
    matching_rows = issue_df[issue_df['new_code'] == issue_df['old_code']]
    print(matching_rows)
    matching_rows.to_csv(f"test.csv", index=False)
    # issue_df['difference_emb'] = issue_df.apply(lambda row: row['new_code_emb'] - row['old_code_emb'], axis=1)

if __name__=="__main__":
    repo_names=['pytorch']
    for repo_name in repo_names:
        main(repo_name)
    

    # issue_df.to_csv('pr_patch_diff_emb.csv', index=False)
