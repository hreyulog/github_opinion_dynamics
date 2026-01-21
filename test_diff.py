import pandas as pd
import difflib
import re
import regex as regex_lib  # 用于处理嵌套多行注释
def remove_scala_comments(code):
    # 移除多行注释，包括嵌套
    pattern_multiline = regex_lib.compile(r'/\*(?:[^*/]|(?:/(?!\*)|\*(?!/))|(?R))*\*/', regex_lib.DOTALL)
    code_no_multiline = regex_lib.sub(pattern_multiline, '', code)
    
    # 移除单行注释
    pattern_singleline = re.compile(r'//.*')
    code_no_comments = re.sub(pattern_singleline, '', code_no_multiline)
    
    return code_no_comments
# 读取数据
def main(repo_name):
    issue_df = pd.read_csv(f'filenames_issue_{repo_name}_10.csv')
    issue_df = issue_df[
    issue_df['filename'].str.contains('\.', na=False)&
    ~issue_df['filename'].str.endswith('.md')]
    idxs = issue_df['PULL_REQUEST_NUMBER']
    patches = issue_df['patch']

    # 存储修改前后的代码
    old_codes = []
    new_codes = []

    # 解析每个 patch
    for patch in patches:
        old_code = []
        new_code = []
        if pd.isna(patch) or len(patch) == 0:  # 检查是否为 NaN
            old_codes.append('')
            new_codes.append('')
            continue  # 跳过 NaN 值，直接处理下一个 patch

        # 使用 difflib 解析 diff 输出
        diff_lines = patch.strip().split("\n")

        for line in diff_lines:
            if line.startswith("-"):  # 修改前的行
                old_code.append(line[1:])  # 去掉前缀 "-" 获取修改前的代码
            elif line.startswith("+"):  # 修改后的行
                new_code.append(line[1:])  # 去掉前缀 "+" 获取修改后的代码
            else:
                line = re.sub(r'^@@ -\d+,\d+ \+\d+,\d+ @@', '', line, flags=re.MULTILINE)
                old_code.append(line[1:])
                new_code.append(line[1:])

        # 处理提取的内容
        old_code_str="\n".join(old_code)
        old_code_fin_str=" ".join(old_code_str.strip().split())
        new_code_str="\n".join(new_code)
        new_code_fin_str=" ".join(new_code_str.strip().split())
        if old_code_fin_str==new_code_fin_str:
            print(patch)
            print(new_code_fin_str)
            print(old_code)
            print(new_code)
        old_codes.append(old_code_fin_str)  # 将修改前的代码合并为一个字符串
        new_codes.append(new_code_fin_str)  # 将修改后的代码合并为一个字符串
        
    # 将结果保存到新的 DataFrame
    issue_df['old_code'] = old_codes
    issue_df['new_code'] = new_codes
    issue_df['old_code'] = issue_df['old_code']
    issue_df['new_code'] = issue_df['new_code']
    # issue_df['old_code'] = issue_df['old_code'].apply(remove_scala_comments)
    # issue_df['new_code'] = issue_df['new_code'].apply(remove_scala_comments)
    issue_df = issue_df.drop('patch', axis=1)

    # 保存到新的 CSV 文件
    # issue_df.to_csv(f'{repo_name}_diff.csv', index=False)
if __name__=="__main__":
    repo_names=['swift','pytorch','ceph']
    for repo_name in repo_names:
        main(repo_name)