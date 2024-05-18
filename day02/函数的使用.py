"""
通过代码演示函数的使用
"""
str1="lyy"
str2="lyyyyyyyyyyyy"
str3="lyyamk131311"
def my_len(data):
    count=0
    for i in data:
        count+=1
    print(f"{data}字符串的长度是:{count}")
my_len(str1)
my_len(str2)
my_len(str3)