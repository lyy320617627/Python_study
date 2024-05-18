"""
通过代码演示集合的定义和常用操作
集合的特点：
保证是乱序且是不可以重复的
集合是无序的，所以不支持下标索引来取出数据的元素
"""

# 集合的定义
{1,2,3,4,5,6,7,8,9,10,11}
# 定义集合变量
my_set = {1,2,3,4,5,6,7,8,9}
# 定义空的集合
my_set2=set()
# add():表示对集合进行添加一个新的元素
# 集合本身被修改，添加了一个新的元素
my_set.add("Python")
print(f"my_set={my_set}")
# remove(value):移除元素，表明从集合中去除value这个元素
# 集合本身被修改，删除了一个指定的元素
my_set.remove("Python")
print(my_set)
# pop():表示从集合中随机取出一个元素
# 结果：会得到一个元素的结果。同时集合本身被修改，元素被移除
element=my_set.pop()
print(f"随机取出的元素是：{element},取出元素之后的集合是:{my_set}")
# 集合.clear()：清空集合的方法
my_set.clear()
print(f"集合set清空之后的内容是:{my_set}")
# 取出两个集合的差集
# 集合1.difference(集合2),功能:取出集合1和集合2的差集(集合1有的，而集合2没有的)
# 结果:得到一个心机和，集合1和集合2不变
my_set={1,2,3,4,5,6,7,8,9,10}
my_set2={1,2,3,4,5,7,8,10}
diff_set=my_set.difference(my_set2)
print(f"集合{my_set}\t和集合{my_set2}\n的差集是:{diff_set}")
# 删除2个集合的差集
# 语法：集合1.difference_update(集合2)
# 功能:对比集合1和集合2，在集合1内，删除和集合2相同的元素
# 结果：集合1被修改，集合2不变
my_set={1,2,3,4,5,6,7,8,9,10}
my_set2={1,2,3,4,5,7,8,10}
my_set.difference_update(my_set2)
print(f"使用difference_update之后，集合my_set的内容是:{my_set},集合my_set2={my_set2}")
# 两个集合的合并
# 集合1.union(集合2)
# 表示将集合1和集合2的内容组合成一个新的集合
# 结果：得到一个新的集合，集合1和集合2不变
new_union_set=my_set.union(my_set2)
print(f"my_set:{my_set}union{my_set2}之后的结果是{new_union_set}")
# 统计集合元素的长度:len()
# 统计my_set集合的长度
length=len(my_set)
print(f"set:{my_set}集合的长度是:{length}")
# 集合的遍历
# 集合是不支持通过下标索引取出数据的，所以无法通过while循环去取出数据
for i in my_set2:
    print(f"集合的元素有:{i}\t",end='')
    print("\n")
# 集合的练习
my_set={'黑马程序员','传智播客','黑马程序员','传智播客','itcast','itheima','itcast','itheima','best'}
my_set2=set()
for i in my_set:
    my_set2.add(i)
print(f"经过遍历添加好元素之后的结果是:{my_set2}")
my_set={}
print(f"my_set={my_set},my_set的类型是:{type(my_set)}")


