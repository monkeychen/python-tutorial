"""
@File: pandas01 
@Author: chenzhian
@Time: 2023/11/30 11:51
"""
import pandas as pd

# 从Excel文件中读取数据
tmp_dir = '/Users/chenzhian/workspace/python/tutorial/temp'
file_path = f'{tmp_dir}/topo.xlsx'
df: pd.DataFrame = pd.read_excel(file_path, sheet_name="合并", engine="openpyxl")

df['C'] = df['C'].astype(str)
# 使用groupby分组，并应用lambda函数来合并C列的值
# result = df.groupby(['A', 'B']).agg({'C': '|'.join}).reset_index()
result = df.groupby(['A', 'B'])['C'].agg('|'.join).reset_index()

result.to_excel(f'{tmp_dir}/merge.xlsx', index=False, header=True)


