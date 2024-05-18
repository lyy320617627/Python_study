"""
通过代码演示range函数的使用
方式一：
     range(num):
     表示从生成零开始一直到num的数字序列，但是不包含num
方式二：
     range(num1,num2)
     表示生成从num1开始，到num2结束，但是不包含num2
方式三：
      range(num1,num2,step)
      表示生成从num1开始以步长step为基准到num2结束的数字序列
"""
for i in range(5):
    print(i,end='')
print("\n")
for i in range(5,10):
    print(i,end='')
print("\n")
for i in range(0,10,2):
    print(i,end='')
print("\n")
count=0
for i in range(1,100):
    if i%2==0:
        count+=1
print(f"从1到100(不含100本身)，共有{count}个偶数")