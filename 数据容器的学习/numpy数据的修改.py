import  numpy as np
"""
通过代码演示修改numpy中的数据
"""
t2=np.arange(12)
t2=t2.reshape(3,4)
print(t2)
print(t2<10)
# 注意：如果对整个数组进行判断，则会对数组中的每一个数据都进行判断再进行后面的操作
# t2[t2<10]=1
# print(t2)
# 想要对数组中小于5的替换成为1，大于5的替换成为10
# 方法
# python中的三元运算符
# 方法：变量名=x if 条件一 else 条件二 ：注意，条件一返回的是一个bool类型的结果，else中则是当条件一不成立时的赋值
a=3 if False else  4
print(a)
# numpy中的三元运算符
# 方法:np.where(条件一，赋值一，赋值二):当条件一返回的是True时，则赋值为赋值一，否则赋值为赋值二
t2=np.where(t2<5,1,10)
print(t2)
# numpy中的裁剪方法
# 方法:t2.clip(10,18)
# 返回的结果：即对数组中的所有元素进行判断，如果数组中的值小于10，则会自动赋值成为10，大于18的则会赋值为18,注意不会对现有的数组进行操作
# 会自动返回一个新的数组
t3=t2.clip(5,7)
print(t3)
print(t2)
# 将数组中的某一个值赋值为nan
# 注意：nan为浮点型类型，当其他形式的数组将数组中的某一个值转换成为nan时，需要将数组的类型转换成为浮点型类型的数组
t2=t2.astype("float")
t2[1,1]=np.nan
print(t2)
#---------------------------------------------------------------
# 数组的拼接
# 竖直：Vertical 水平：horizontal
# 竖直拼接：
t3=np.loadtxt("1.csv",delimiter=",")
t3=t3.astype("int")
t4=np.loadtxt("2.csv",delimiter=",")
t4=t4.astype("int")
# 竖直方向上的拼接
t5=np.vstack((t3,t4))
print(t5)
t5=np.hstack((t3,t4))
print(f"水平方向上的拼接:{t5}")
# 行列交换的方法
# 行交换 t2[[1,2]，:]=t2[[2,1],:]
# 列交换
# 方法 t2[:,[0,1]]=t2[:,[1,0]]




