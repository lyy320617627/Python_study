import pandas as pd

def read_excel(file_path):
    # 读取Excel文件
    df = pd.read_excel(file_path)

    # 提取A列内容，并转换成列表
    a_column_list = df.iloc[:, 0].tolist()  # 使用列索引提取A列内容

    # 去除列表名
    a_column_list = a_column_list[1:]  # 去除第一行的列名
    return a_column_list
file_path=r"C:\Users\ly320\Desktop\供应商列表.xlsx"
result_list=read_excel(file_path)
print(result_list)
print(len(result_list))
