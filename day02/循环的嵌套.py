"""
通过代码演示嵌套循环的使用
"""
i=1
while i<=100:
    j=1
    while j<=10:
        print(f"这是今天送小美的第{j}枝玫瑰花")
        j+=1
    print(f"这是坚持向小美表白的{i}天")
    i+=1
print(f"坚持到{i-1}天，小美答应了我的表白")
# 打印九九乘法表
k=1
G=1
while k<=9:
   while G<=k:
       print(f"{G}*{k}={G*k}\t",end='')
       G+=1
   G=1
   k+=1
   print("\n")