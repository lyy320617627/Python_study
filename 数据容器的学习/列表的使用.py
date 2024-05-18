"""
演示列表的基本用法
-------------------------------
注意点1:
列表一次性可以存储多个数据，而且每个数据的类型可以不同
"""
# 列表的定义
[1,"2","lyy",False,5,6,7,8,9,10]
num=[1,"2","lyy",False,5,6,7,8,9,10]
# 空列表的定义
num2=[]
num3=list()
print(num,type(num2),type(num3))
# 通过下标索引取出数据元素
my_list=[["lyy","朱梦珂","1122"],[1122,"zmk","李杨杨"]]
for i in range(0,int(len(my_list[0])-1)):
    for j in range(0,int(len(my_list[0]))):
        print(my_list[i][j])
print(isinstance(num,(
    tuple,dict)))