def getTarget_count(datalist):
    float_count=0
    for data in datalist:
        if data[7]>0:
            continue
        if data[6]=="基本账户扣减-支付模拟扣减" or data[6]=="价保返利账扣减":
            float_count+=data[7]
    return -float_count






if __name__ == '__main__':
    print(111)