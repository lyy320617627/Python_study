import numpy as np
import pandas as pd
def ScmLowerFileRead(file_path):
    data=pd.read_excel(file_path)
    data=data[data["同步失败原因"].str.contains("未同步集团主数据")]
    # print(data)
    data=data.values.tolist()
    # customer_list=data["渠道商/门店"].tolist()
    # print(customer_list)
    # return customer_list
    return data

file_path=r'C:\Users\ly320\Desktop\三系统余额稽核二阶段\和动力下载文件\发货单.xlsx'
data=ScmLowerFileRead(file_path)
for i in data:
    print(i)