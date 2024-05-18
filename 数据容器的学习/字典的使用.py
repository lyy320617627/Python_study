""""
通过代码学习Python字典的使用
注意：字典的key和value可以是任意类型，但是key不可以是字典
"""
# 空字典的定义
my_dict={}
my_dict2=dict()
print(my_dict)
print(my_dict2)
my_dict={'Person':{
         "lyy":99,
         "zmk":88,
          "lyyy":77}}
print(my_dict['Person']['lyy'])
# 定义重复key的字典（key相同的键值对中新的value会替换掉旧的value）
print(my_dict['Person']['lyy'])
print(my_dict.items())
for key,value in my_dict["Person"].items():
    print(key,value)
# 字典的嵌套
score_dict={'lyy':{
            '语文':99,
            '数学':88,
            '英语':77,
},'zmk':{'语文':99.9,
            '数学':88.8,
            '英语':77.7},
"lyyy":{'语文':99.9,
            '数学':88.8,
            '英语':77.7}}
for key in score_dict:
    for value,values in score_dict[key].items():
        print(value)
        print(values)