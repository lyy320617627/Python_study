"""
通过代码演示形式参数和实际参数的传入和使用
"""
num=int(input("请输入你的体温"))
def check(num):
    print("欢迎来到游乐园，请出示你的体温表")
    if num>37.5:
        print("不好意思，你的体温过高，不可以进入游乐园")
    else:
        print("欢迎来到游乐园，祝你玩得开心")
check(num)
# 返回None值的使用
def check2(age):
    if age >18:
        return "SUCCESS"
    else:
        return None
result=check2(16)
if not result:
    print("不好意思，你还是未成年，不可以进入网吧")