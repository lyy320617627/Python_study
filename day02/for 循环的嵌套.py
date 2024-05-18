"""
代码演示for循环嵌套的使用
"""
for i in range(1,101):
    for j in range(1,11):
        print(f"这是今天向小美送的{j}朵玫瑰")
    print(f"这是向小美表白的第{i}天")
for i in range(1,10):
    for j in range(1,i+1):
        print(f"{j}*{i}={j*i}\t",end='')
    print("\n")
