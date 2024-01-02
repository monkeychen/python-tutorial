"""
@File: pandas01 
@Author: chenzhian
@Time: 2023/11/30 11:51
"""
import os

import pandas as pd

# 从Excel文件中读取数据
tmp_dir = '/Users/chenzhian/workspace/python/tutorial/temp'
file_path = f'{tmp_dir}/topo2.xlsx'
df: pd.DataFrame = pd.read_excel(file_path, sheet_name="Sheet1", engine="openpyxl")

df['C'] = df['C'].astype(str)
# 使用groupby分组，并应用lambda函数来合并C列的值
# result = df.groupby(['A', 'B']).agg({'C': '|'.join}).reset_index()
result = df.groupby(['ne_type', 'sc_type'])['measure_id'].agg('|'.join).reset_index()

out_path = f"{tmp_dir}/merge2.xlsx"
if os.path.exists(out_path):
    os.remove(out_path)
result.to_excel(out_path, index=True, header=True)


