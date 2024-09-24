import numpy as np
"""
通过代码演示对数组中为nan的数据进行处理
"""
t1=np.arange(12).reshape((3,4)).astype("float")
print(t1)
t1[1,1:3]=np.nan
print(t1)
print(np.count_nonzero(t1))
# 把nan替换成为均值
for i in range(t1.shape[1]):
    temp_col=t1[:,i] #取出当前的一列
    nan_num=np.count_nonzero(temp_col!=temp_col)
    if nan_num !=0: # 说明这一列含有nan
        temp_not_nan_col=temp_col[temp_col==temp_col] #当前不为nan的array
        temp_col[np.isnan(temp_col)]=temp_not_nan_col.mean()
    print(t1)

