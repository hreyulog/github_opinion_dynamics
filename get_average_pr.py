import pandas as pd
import requests
from tqdm import tqdm
import torch
import numpy as np
def main(repo_name):
    diff_code_emb = np.load(f"difference_code_emb_{repo_name}.npy")
    pr_df = pd.read_csv(f"{repo_name}_diff.csv")
    pr_time = pd.read_csv(f"filtered_issue_{repo_name}_10.csv")
    pr_nums = set(pr_df["PULL_REQUEST_NUMBER"])
    pr_dict = {}
    id_name_dict = pr_time.set_index("PULL_REQUEST_NUMBER")["YEAR_HALF"].to_dict()
    id_name_dict2 = pr_time.set_index("PULL_REQUEST_NUMBER")[
        "PULL_REQUEST_AUTHOR"
    ].to_dict()
    time_list = []
    autor_list = []
    for num in pr_nums:
        indices_list = pr_df[pr_df["PULL_REQUEST_NUMBER"] == num].index.tolist()
        emb_list = [diff_code_emb[idx] for idx in indices_list]
        emb_list = [arr for arr in emb_list if not np.all(arr == 0, axis=1)]
        if len(emb_list)==0:
            continue
        #     print(num)
        pr_emb = np.mean(emb_list, axis=0)
        pr_dict[num] = pr_emb
        time_list.append(id_name_dict[num])
        autor_list.append(id_name_dict2[num])
    data = {
        "pr_num": list(pr_dict.keys()),
        "pr_time": time_list,
        "pr_author": autor_list,
    }
    df = pd.DataFrame(data)
    np.save(f"pr_emb_{repo_name}.npy", np.stack(list(pr_dict.values())))
    df.to_csv(f"pr_time_{repo_name}.csv", index=False)


if __name__ == "__main__":
    repo_names=['swift','pytorch','ceph']
    for repo_name in repo_names:
        main(repo_name)