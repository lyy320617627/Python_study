import numpy as np
"""
numpy的综合练习
"""
data_1=np.loadtxt("1.csv",delimiter=",",dtype="int")
data_2=np.loadtxt("2.csv",delimiter=",",dtype="int")
# 构造全为0和1的数组
zeros_data=np.zeros((data_1.shape[0],1)).astype(int)
ones_data=np.ones((data_2.shape[0],1)).astype(int)
# 水平方向上分别拼接0和1的数组
data_1=np.hstack((data_1,zeros_data))
data_2=np.hstack((data_2,ones_data))
# 拼接两组的数据
data_3=np.vstack((data_1,data_2))
# print(data_1)
# print(data_2)
# print(data_3)
t4=np.arange(12).reshape(3,4)
print(t4)
print(np.sum(t4,axis=1))
