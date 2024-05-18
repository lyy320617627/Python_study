"""
演示函数嵌套调用的流程和结果
"""
def func_b():
    print("----b----")
def func_a():
    print("----a----")
    func_b()
    print("----c----")