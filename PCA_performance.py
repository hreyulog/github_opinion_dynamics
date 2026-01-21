import numpy as np


if __name__=="__main__":
    emb_before_PCA=np.load('/srv/nfs/VESO/home/heyulong_others/github_opinion/author_time_emb_ceph.npy')
    c = np.linalg.eig(emb_before_PCA)
