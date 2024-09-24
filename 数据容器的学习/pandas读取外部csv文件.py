import numpy as np
import pandas as pd
"""
通过代码演示读取csv文件的使用方法
"""
# pandas读取csv文件中的数据
data=pd.read_csv('dogNames2.csv')
# print(data)
# dataFrame对象既有行索引，也有列索引
# 行索引，表明不同行，横向索引，叫index，0轴，axis=0
# 列索引，表明不同列，纵向索引，叫columns,1轴，axis=1
df=pd.DataFrame(np.arange(12).reshape(3,4))
# print(df)
# 在创建dataframe时指定行列的索引
df2=pd.DataFrame(np.arange(12).reshape(3,4),index=list("789"),columns=['X','Y','Z','W'])
# print(df2)
# 传入一个字典作为DataFrame数据类型
dictData={"name":["lyy","zmk","zzz"],"age":[21,22,23],"tel":[123,456,789]}
dict_DataFrame=pd.DataFrame(dictData)
print(dict_DataFrame)
"""
字典作为数据传入dataFrame时，列索引为字典对应的key值，字典中的key值对应的value数据数据长度要一致
  name  age  tel
0  lyy   21  123
1  zmk   22  456
2  zzz   23  789
"""
# 显示数据前几行 df.head(n)：n表示显示几行数据
print(dict_DataFrame.head(1))
# 显示数据的后几行
print(dict_DataFrame.tail(1)) # 1:表示传入的参数，表示显示几行数据
# 展示DataFrame数据的概要
print(dict_DataFrame.info())
# 统计DataFrame数据的均值参数
print(dict_DataFrame.describe())
# DataFrame数据中的排序
df=dict_DataFrame.sort_values(by="name",ascending=False)
print(df)
print("**"*50)
# 取出数据的前n行
# 方括号写数字，表示取行，对行进行操作
# 方括号写字符串，表示取列
# 形式df[:20]
print(df[:1]["age"])
# df.loc通过标签索引行数据
# df.iloc通过位置获取行数据
# index:表示行索引，columns:表示列索引
df1=pd.DataFrame(np.arange(12).reshape(3,4),index=list("789"),columns=list("WXYZ"))
# 对行进行操作时，冒号后面的是闭合的，即会选择到冒号后面的数据
print(df1.loc["7":"9",["X","Y"]])
# 通过iloc对位置索引进行操作，取出数据的元素
# 表示取出第二行的所有元素
print(df1.iloc[1,:])
# 取出第三列的元素
print(f"第三列的数据为：{df1.iloc[:,2]}")

