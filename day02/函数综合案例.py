"""
通过ATM自动取款机来演示函数的综合练习
"""
money=5000000
name=None
name=input("请输入你的名字")
# 定义查询余额函数
def query(show_headers):
    if show_headers:
        print("--------查询余额--------")
    print(f"你的账户余额为{money}元")
# 定义存款函数
def saving(num):
    global money
    money+=num
    print("--------存入金钱---------")
    print("你已经成功存入%d元，账户余额剩余%d元"%(num,money))
    query(False)
# 定义取款
def Withdrawal(num):
    global money
    money-=num
    print("----------取出金钱---------")
    print("你已经成功取出%d元，账户余额还剩%d元"%(num,money))
    query(False)
# 定义主函数
def main(show_headers):
    if show_headers:
        print("%s你好，欢迎来到黑马ATM。请输入你的选择"%name)
    print("--------主菜单---------")
    print("余额查询\t[输入1]")
    print("取款\t\t[输入2]")
    print("存款\t\t[输入3]")
    print("退出\t\t[输入4]")
    return int(input("请输入你的选择"))
# 保证循环不会退出
while True:
    select=main(True)
    if select==1:
        query(True)
        continue
    elif select==2:
        num=int(input("请输入你需要取出的金额"))
        Withdrawal(num)
        continue
    elif select==3:
        num=int(input("请输入需要存入的金额"))
        saving(num)
        continue
    else:
        print("程序退出啦")
        break

