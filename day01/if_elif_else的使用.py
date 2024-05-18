"""
通过代码演示
if_elif_else的使用
"""
age = int(input("请输入你的年龄:\n"))
vip_level = int(input("请输入你的会员等级(1~5)\n"))
if age<=13:
    print("你的年龄小于13")
    print("你可以免费游玩")
elif vip_level>=3:
    print("你的会员级别大于3")
    print("你可以免费游玩")
print("祝你游玩愉快")