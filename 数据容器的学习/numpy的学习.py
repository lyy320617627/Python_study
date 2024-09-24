import json
import random

import numpy
import numpy as np
# 利用numpy创建数组
# 方式一
t1 =numpy.array([1,2,3])
print(t1)
print(type(t1))
# 方式二
t2=numpy.array(range(10,20))
print(t2)
print(type(t2))
# 方式三
t3=numpy.arange(10)
print(t3)
print(type(t3))
print(t3.dtype)
# json.loads():json对象转化成为Python对象
# json.dumps():将Python对象（一般是字典类型，转化成为json对象）
# json.dumps()
# 在创建数据时指定数组内数据的类型
t4=numpy.array(range(1,10),dtype=float)
print(t4.dtype)
# numpy中的bool类型
t5=numpy.array([1,1,0,1],dtype=bool)
print(f"t5:{t5}")
print(t5.dtype)
# 调整数据类型
t6=t5.astype("int8")
print(t6)
print(t6.dtype)
# numpy中的小数
t7=numpy.array([random.random() for i in range(10)])
print(t7)
print(t7.dtype)
# t8=t7.round(t7,2)
# print(t8)
# print(t8.dtype)
print("=======================================")
# shape和reshape方法
t9=numpy.arange(24)
t10=t9.reshape((3,8))
t9=t9.reshape((3,8))
# 如果print的结果是None，则表明就是原地操作，返回的是None，再次赋值也是None
print(t10)
print(type(10))
print(t9)
print(t9.dtype)
t11=t9.reshape(24,1)
print(f"t11:{t11}")
print(t11.dtype)
# 当不知道二维数组的总长度时。
# 想要继续把数组的形式转换成为一维的形式时
print("===============================")
t12=t11.reshape(t11.shape[0]*t11.shape[1])
print(f"t12:{t12}")
print(f"t12中的数据类型是:{t12.dtype}")
print(f"t12的类型是:{type(t12)}")
# 展开的方法:flatten(),当不知道数组的形式时，可以使用flatten方法把数组展开成为一维的
print(f"t10的内容是:{t10}")
print(f"t10 flatten之后的内容是:{t10.flatten()}")
# 对数组中的每一个数都加2
t11=t10+2
print(f"t10数组中的每个数字都加上2之后的结果是:{t11}")
# 三维数组的运算
shape_3=numpy.arange(18)
shape_3=shape_3.reshape(3,3,2)
print(f"shape_e:{shape_3}")
shape_2=numpy.arange(9).reshape(3,3)
print(f"shape_2:{shape_2}")
shape_1=shape_3-shape_2
print(f"相减之后的shap：{shape_1}")