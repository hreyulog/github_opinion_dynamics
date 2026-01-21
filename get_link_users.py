import pandas as pd
from collections import defaultdict
def get_inter(df1,df2):
    #how many df2 in df1
    # print(df1[['PULL_REQUEST_AUTHOR', 'COMMENT_AUTHOR']])
    # print(df2[['PULL_REQUEST_AUTHOR', 'COMMENT_AUTHOR']])
    return len(df2)/len(df1)

# 转换为 DataFrame
df = pd.read_csv('filtered_issue_swift_10.csv')
df = df.dropna(subset=['COMMENT_AUTHOR'])
role_counts = defaultdict(lambda: {"PULL_REQUEST_AUTHOR": 0, "COMMENT_AUTHOR": 0})
interaction_counts = defaultdict(int)

# 遍历数据并统计
pr_authors=[]
for _, row in df.iterrows():
    pr_authors.append(row["PULL_REQUEST_AUTHOR"])
pr_authors=list(set(pr_authors))
print(pr_authors)
authors_dict = {}
data=[]
for i in range(len(pr_authors)):
    for j in range(len(pr_authors)):
        df1=df[df['PULL_REQUEST_AUTHOR'] == pr_authors[i]]
        data.append((pr_authors[i],pr_authors[j],get_inter(df1,df1[df1['COMMENT_AUTHOR'] == pr_authors[j]])))
df = pd.DataFrame(data, columns=['Author1', 'Author2', 'Score'])

matrix = df.pivot(index='Author1', columns='Author2', values='Score').fillna(0)

print(matrix)


