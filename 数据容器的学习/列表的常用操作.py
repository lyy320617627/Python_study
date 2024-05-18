"""
通过代码演示列表常用方法的操作
"""
my_list = ["lyy","zmk",1122]
# 通过下标索引查找元素
print(my_list[1])
# 通过下标元素修改元素的值
my_list[1]="zmk222"
print(my_list)
# 通过insert方法在指定的下标插入一个元素的值
my_list.insert(1,"lyyya")
print(my_list)  #注意：传入的index参数就是指定变量所在的索引位置
# 通过append在列表的末尾追加一个元素
my_list.append("112233")
print(my_list)
# 通过extend方法将另一个列表的所有元素依次添加到列表的末尾
my_list2=[1,2,3]
my_list.append(my_list2)
print(my_list)
my_list.extend(my_list2)
print(my_list)
# 通过del和pop删除列表的元素位置
my_list.pop(len(my_list)-1)
del my_list[len(my_list)-1]
print(f"删除元素之后，列表元素：{my_list}")
# 删除列表中第一个匹配的元素
# num=my_list.remove(1)
print(my_list)
# 清空列表中的所有元素
# my_list.clear()
print(my_list)
# 统计列表中某个元素的值
count=my_list.count(1)
print(count)
# 统计列表所有元素的个数
len=len(my_list)
print(len)