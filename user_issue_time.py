import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# 加载数据
from tqdm import tqdm
from itertools import combinations
repo_name='ceph'
issue_df = pd.read_csv(f'filtered_pr_{repo_name}.csv')
type_name='PULL_REQUEST'
# 处理日期格式
issue_df[f'{type_name}_CREATION_DATE'] = pd.to_datetime(issue_df[f'{type_name}_CREATION_DATE'], errors='coerce')
# 去掉缺失的ISSUE_AUTHOR
issue_df = issue_df.dropna(subset=[f'{type_name}_AUTHOR'])

# 确保数据中没有重复的issue记录
issue_df = issue_df.drop_duplicates(subset=['REPO_URL', f'{type_name}_NUMBER'])

# 查看处理后的数据
# start_date = '2016-04-01'
# end_date = '2018-10-31'
# issue_df = issue_df[(issue_df[f'{type_name}_CREATION_DATE'] >= start_date) & (issue_df[f'{type_name}_CREATION_DATE'] <= end_date)]

# 统计每个用户提issue的次数
user_issue_count = issue_df.groupby(f'{type_name}_AUTHOR').size().reset_index(name='issue_count')
issue_sum = user_issue_count.groupby('PULL_REQUEST_AUTHOR')['issue_count'].sum().reset_index()
print(issue_sum['issue_count'].describe())
threshold = issue_sum['issue_count'].quantile(0.99)
top_5_percent = issue_sum[issue_sum['issue_count'] >= threshold]
print(top_5_percent)
author_nums=len(top_5_percent)
print(author_nums)

top_users_list=top_5_percent[f'{type_name}_AUTHOR'].tolist()

# 排序，找出提issue最多的前几个用户
print(user_issue_count)
user_issue_count_sorted=user_issue_count[user_issue_count[f'{type_name}_AUTHOR'].isin(top_users_list)]
print(user_issue_count_sorted)

# user_issue_count_sorted = user_issue_count.sort_values(by='issue_count', ascending=False).head(30)

issue_df[f'{type_name}_CREATION_DATE'] = pd.to_datetime(issue_df[f'{type_name}_CREATION_DATE'], errors='coerce')
issue_df['YEAR'] = issue_df[f'{type_name}_CREATION_DATE'].dt.year
issue_df['MONTH'] = issue_df[f'{type_name}_CREATION_DATE'].dt.month
def get_three_month_period(month):
    if month in [1, 2, 3]:
        return '01'  # 第一季度：1-3月
    elif month in [4, 5, 6]:
        return '04'  # 第二季度：4-6月
    elif month in [7, 8, 9]:
        return '07'  # 第三季度：7-9月
    else:
        return '10'  # 第四季度：10-12月
def get_six_month(month):
    if month in [1, 2, 3,4, 5, 6]:
        return '01'  # 第一季度：1-3月
    else:
        return '07'  # 第二季度：4-6月
# issue_df['HALF_YEAR'] = issue_df['MONTH'].apply(get_three_month_period)
issue_df['HALF_YEAR'] = issue_df['MONTH']
issue_df['YEAR_HALF'] = issue_df['YEAR'].astype(str) + '-' + issue_df['HALF_YEAR'].astype(str)
issue_semiannual_user = issue_df.groupby([f'{type_name}_AUTHOR', 'YEAR_HALF']).size().reset_index(name='issue_count')

# issue_monthly_user = issue_df.groupby([f'{type_name}_AUTHOR', issue_df[f'{type_name}_CREATION_DATE'].dt.to_period('6M')]).size().reset_index(name='issue_count')
# issue_monthly_user[f'{type_name}_CREATION_DATE'] = issue_monthly_user[f'{type_name}_CREATION_DATE'].dt.to_timestamp()
top_10_users = user_issue_count_sorted[f'{type_name}_AUTHOR'].tolist()
issue_monthly_top_10 = issue_semiannual_user[issue_semiannual_user[f'{type_name}_AUTHOR'].isin(top_10_users)]
print(issue_monthly_top_10)
issue_monthly_top_10['YEAR_HALF'] =  pd.to_datetime(issue_monthly_top_10['YEAR_HALF'])
print(issue_monthly_top_10['YEAR_HALF'].dtype)
print(issue_monthly_top_10)
user_dict = issue_monthly_top_10.groupby(f'{type_name}_AUTHOR')['YEAR_HALF'].apply(list).to_dict()
user_sets = {user: set(dates) for user, dates in user_dict.items()}
combinations_of_users = combinations(user_sets.keys(),7)  # 获取所有 7 个用户的组合
user_intersections = []
def getmax(sorted_timestamps):
    max_len = 1
    current_len = 1
    max_start = sorted_timestamps[0]
    max_end = sorted_timestamps[0]
    current_start = sorted_timestamps[0]

    for i in range(1, len(sorted_timestamps)):
        prev = sorted_timestamps[i-1]
        current = sorted_timestamps[i]

        # 预期的下一个月
        expected = prev + pd.DateOffset(months=1)

        if current == expected:
            current_len += 1
            current_end = current
        else:
            current_len = 1
            current_start = current

        # 更新最长序列的信息
        if current_len > max_len:
            max_len = current_len
            max_start = current_start if current_len == 1 else (current - pd.DateOffset(months=(current_len-1)))
            max_end = current
    return max_len,max_start,max_end
# 遍历每个组合，计算交集的大小
for combo in tqdm(combinations_of_users):
    # 计算该组合的交集
    intersection = user_sets[combo[0]]
    for user in combo[1:]:
        intersection &= user_sets[user]
    # 记录该组合及其交集的大小
    timestamps=list(intersection)
    sorted_timestamp=sorted(timestamps)
    if len(sorted_timestamp)!=0:
        max_len,max_start,max_end=getmax(sorted_timestamp)
        user_intersections.append((combo, max_len,max_start,max_end,timestamps))

# 按照交集大小降序排序，选择前五个组合
user_intersections_sorted = sorted(user_intersections, key=lambda x: x[1], reverse=True)[:5]
print(user_intersections_sorted)
plt.figure(figsize=(12, 8))
authors_to_filter = list(user_intersections_sorted[0][0])
print(authors_to_filter)
filtered_issue_df = issue_monthly_top_10[issue_monthly_top_10[f'{type_name}_AUTHOR'].isin(authors_to_filter)]
# 绘制每个用户的时间-issue数量图
print(filtered_issue_df)
sns.lineplot(x='YEAR_HALF', y='issue_count', hue=f'{type_name}_AUTHOR', data=filtered_issue_df, marker='o')

filtered_issue_df = issue_df[issue_df[f'{type_name}_AUTHOR'].isin(authors_to_filter)]
filtered_issue_df.to_csv(f'filtered_issue_{repo_name}_10.csv', index=False)

# 设置标题和标签
plt.title('Number of PR Created per Month by Each User')
plt.xlabel('Month')
plt.ylabel('Number of PR')
plt.xticks(rotation=45)
plt.grid(True)

# 显示图表
plt.tight_layout()
plt.legend(title='User', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()
plt.savefig('sample_plot.png', bbox_inches='tight')  # 保存为 PNG 格式
