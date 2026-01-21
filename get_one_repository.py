import pandas as pd
# pull_df = pd.read_csv('pr_R.csv')
issue_df = pd.read_csv('pr_C-PlusPlus.csv')
# commit_df = pd.read_csv('co_R.csv')
repo_name = 'pytorch'
issue_df.rename(
columns={'PULL_REQUEST_TITLE': 'PULL_REQUEST_CREATION_DATE', 
'PULL_REQUEST_CREATION_DATE': 'PULL_REQUEST_TITLE'}, inplace=True)
issue_filtered = issue_df[issue_df['REPO_NAME'] == repo_name]
# commit_filtered = commit_df[commit_df['REPO_NAME'] == repo_name]


# pull_filtered.to_csv(f'filtered_pull_{repo_name}.csv', index=False)
issue_filtered.to_csv(f'filtered_pr_{repo_name}.csv', index=False)
# commit_filtered.to_csv(f'filtered_commit_{repo_name}.csv', index=False)