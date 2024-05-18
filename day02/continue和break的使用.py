"""
continue和break关键字的使用
 continue:
 跳出本次循环，直接进入下一次的循环
 break：
 直接结束所在的循环】
"""
for i in range(10):
    print("语句1")
    for j in range(10):
        print("语句2")
        break
        print("语句3")
print("end")