"""
通过代码演示对列表的循环遍历
"""
my_list = [1,2,3,4,5,6,7,8,9,10]
def while_for_list(my_list):
    index=0
    while index<len(my_list):
        if my_list[index]%2==0:
            my_list.pop(index)
        index+=1
    print(my_list)
def for_list(my_list):
    for i in range(0,len(my_list)):
        if my_list[i]%2==0:
            my_list.pop(i)
    print(my_list)
while_for_list(my_list)
for_list(my_list)