""""
通过代码演示元组的使用
"""
# 注意：元组一旦定义完成之后不可以进行修改，只能进行读操作
# 元组的定义方式
# 元组可以包含多个元素，并且元素的类型也是不受限制的
# 注意：当元组中只包含一个元素时，要在元素后面加上一个","号，否则不是元组类型
# 元组内容是不能够修改的，但是当元组内嵌套一个list列表时，列表的内容是可以修改的
# 元组和list列表一样，可以支持多个数据，不同类型的数据，支持重复的数据
(1,2,3,4,5,6,7,8,9,10,11,12)
num=(1,2,3,4,5,6,7,8,9,10,11)
num2=(1,)
print(type(num2))
num4=tuple()
# 元组的嵌套
num=((1,2,3),(4,5,6))
print(f"num的内容是{num}\n,类型是{type(num)}")
# 通过下标元素取出数据的值
print(num[1][2])
# 元组的常用方法
# index：和列表的方法一样，查找元素再元组中的下标索引
num=(1,2,3,4,5,6,7,8,9,10)
print(num.index(8))
# count(num):统计元组中一共包含多少num个元素
print(num.count(1))
# len:表示统计元组的长度，即包含多少个元素
print(len(num))
# 元组的遍历
# while循环遍历元组
i=0
while i <len(num):
    print(num[i])
    i+=1
print(i)
# 通过for循遍历元组
print("通过for循环遍历num元组开始")
for j in range(0,len(num)):
    print(num[j])
print("通过for循环遍历元组结束")
# 修改嵌套在元组中的list列表的元素
t9=(1,2,3,["itcast","itheima"])
print(f"修改之前t9的值为:{t9}")
t9[3][0]="lyy"
t9[3][1]="zmk"
print(f"t9修改之后为：{t9}")
# -----------------------元组的练习-------------------------------------------------------
my_tuple=('周杰伦',11,['football','music'])
print(my_tuple.index(11))
print(my_tuple[0])
my_tuple[2].pop(0)
my_tuple[2].append("coding")
print(my_tuple[-1])

