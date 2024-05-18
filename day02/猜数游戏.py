import random
num=random.randint(1,10)
flag=True
while flag:
    guess_num=int(input("请输入你猜的数字\n"))
    if guess_num==num:
        flag=False
        print("恭喜你猜对了！")
    else:
        if guess_num>num:
            print("不好意思，你输入的数字过大")
            continue
        else:
            print("不好意思，你输入的数字过小!")
            continue