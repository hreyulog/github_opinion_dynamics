import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# 假设有一个高维嵌入数据集
# 例如，1000 个样本，每个样本 768 维
embedding = np.random.rand(1000, 768)

pca = PCA(n_components=1)
embedding_pca = pca.fit_transform(embedding)

print("PCA 降维后的形状:", embedding_pca.shape)  # 输出: (1000, 50)
print(embedding_pca)