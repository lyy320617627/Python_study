""""
通过代码演示对类型注解的使用
为变量设置类型注解
基础语法：变量:类型
 基础类型注解
 var_1:int=10
 var_2:float=3.1415926
 var_3:str="itheima"
 var_4:bool=True
类对象类型注解
class Student：
    pass
    stu：student=Student()
"""
# 基础类型注解
var_1:int=10
var_2:float=3.14
var_3:str="itheima"
var_4:bool=True
print(var_1,var_2,var_3)
# 10 3.14 itheima
# 类对象的注解
class Student(object):
    pass
stu:Student=Student()
# 基础容器类型注解
my_list:list=[1,2,3,4]
my_tuple:tuple=(1,2,3,4)
my_set:set={1,2,3,4}
my_dict:dict={"name":"lyy"}
print(my_list,my_tuple,my_set)
# [1, 2, 3, 4] (1, 2, 3, 4) {1, 2, 3, 4}
# 在注释中进行类型注解
# 语法：# type:类型
var_5=True # type:bool
# 函数和方法的形参类型注解语法：
# def 函数方法名(形参名: 类型,形参名:类型，.......):
#     pass
def add(x:int,y:int):
    return x+y
print(add(1,2))
def func(data:list):
    data.append(1)
# 对返回值进行注解
def func2(data:list)-> list:
    return data
data_list=func2(my_list)
print(data_list)
# 混合类型数据的注解
# 需要导入union的包
from typing import Union
# 使用Union进行注解时，表明进行赋值的变量的类型即为Union中所枚举的类型之中的数据
my_list:Union[int,float,str]=[1,2,3,"lyy"]
