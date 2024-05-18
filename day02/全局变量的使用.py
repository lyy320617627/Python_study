""""
通过代码演示全局变量的使用
"""
num=10
def func_a():
    global num
    num+=10
    print(num)
def func_b():

    print(num)
func_a()
func_b()