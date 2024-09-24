import pandas as pd
"""
学习pandas的基本概念和使用
"""
data_1=pd.Series([1,2,3,4,5,6,7])
print(data_1)
print(type(data_1))
# 指定索引的类型创建数据,在创建数据时使用index=这个属性，可以指定series的索引类型
t2=pd.Series([1,2,3,4,5],index=list(("abcde")))
print(f"t2:{t2}")
# 使用字典创建series时，默认情况下字典中key充当索引
temp_dict={"name":"lyy","age":21,"gender":"male"}
t3=pd.Series(temp_dict)
print(f"t3:{t3}")
# 取出Series中的索引和value值
print(f"t3.index:{t3.index}")
# 取出Series中的值
print(f"t3.values:{t3.values}")
