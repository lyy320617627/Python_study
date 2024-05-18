import random
money=10000
flag=True
i=1
while flag:
    grade_index = random.randint(1, 10)
    if grade_index<5:
        print(f"员工{i},绩效分{grade_index},低于5，不发工资，下一位：")
        i+=1
        continue
    elif money>=1000:
        print(print(f"向员工{i},发放工资1000,账户余额还剩余{money-1000}"))
        i+=1
        money-=1000
    else:
        print(f"工资发放完了，下个月再来领吧")
        break