"""
通过代码演示学习字符串的常用操作以及定义
"""
# 列表，元组，字符串都支持下标索引从前向后查找或者从后向前查找
# 同元组一样，字符串也不支持修改，如果非要修改字符串，只会得到一个新的字符串，而原来的字符串不会改变
my_str="lyyy and zmk"
# 通过下标索引取出元素的值
print(f"通过下标索引3取出元素的值应该是y，实际上是{my_str[3]}")
print(f"通过下标索引-9取出元素的值应该是y，实际上是{my_str[-9]}")
# index:查找元素在字符串中的起始位置
print(f"通过index方法查找and在原来字符串的索引下标应该是5，实际上是{my_str.index("and")}")
# replace:将字符串中的元素替换成目标字符串
# 注意：replace方法会将字符串中的匹配到的所有元素都替换成为目标元素
new_str=my_str.replace("y","z")
print(f"将{my_str}字符串替换成功之后，得到的字符串是{new_str}")
# split:按照指定的分隔字符串，将字符串划分为多个字符串，并存入到列表对象中
# 注意：字符串本身不变，而是得到一个列表对象
my_list=my_str.split(" ")
print(my_list)
# strip:字符串的规整操作
# strip():不传入参数时，将会去除字符串前后空格
# strip(字符串):将会去除前后指定字符串,并且传入的字符串将会被拆分成为单个字符串
my_str="  21lyyy and zmk12"
new_my_str1=my_str.strip()
new_my_str2=new_my_str1.strip("12")
print(f"当字符串{my_str}调用strip()方法后，其中的内容是:{new_my_str1}")
print(f"当字符串{new_my_str1}调用strip('12')之后，结果是:{new_my_str2}")
# 统计字符串中某个字符串出现的次数
count=my_str.count(" ")
print(f"字符串{my_str}中出现‘ ’的次数是:{count}")
# 统计字符串的长度
length=len(my_str)
print(f"字符串{my_str}的长度是:{length}")
# 字符串的遍历
# 方式一：while循环
i=0
while i <len(my_str):
    print(my_str[i])
    i+=1
for i in my_str:
    print(f"for 循环:{i}")
# -----------------字符串的练习--------------------
test_str="itheima itcast xoxuegu"
length=len(test_str)
print(f"字符串{test_str}的长度是:{length}")
replace_test_str=test_str.replace(" ","|")
print(f"字符串{test_str}将里面的元素全被替换成为|之后的结果是:{replace_test_str}")
# 按照|将字符串进行切割
test_str_list=replace_test_str.split("|")
print(f"将字符串{test_str}按照'|'进行切割之后得到的列表是:{test_str_list}")
for i in test_str_list:
    print(i)
