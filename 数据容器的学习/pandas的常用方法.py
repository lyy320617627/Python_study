import  pandas as pd
import numpy as np
df=pd.read_csv("dogNames2.csv")
# 筛选出Row_Labels字段字符串长度大于4，并且Count_AnimalName大于700的数据
print(df[(df["Row_Labels"].str.len()>4)&(df["Count_AnimalName"]>700)])
# 对缺失数据的处理
# axis：表示沿数轴的某一个轴，how中any：表示只要有一个为nan都要删除，all：表示所有的都为nan时才会删除，inplace：表示是否是原地修改
# 为True时，表示是对df本身修改，False表示不会对df本身修改，会再返回一个参数
df=df.dropna(axis=0,how="any",inplace=False)
# 求某一行或者某一列的长度的方法
print(len(set((df["Row_Labels"].tolist()))))
print(len((df["Row_Labels"].unique())))
np.arange(12).reshape((3,4)).flatten()
