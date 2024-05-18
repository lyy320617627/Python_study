"""
文件的打开和使用
"""
import json

# open()文件的打开或者新的创建：
# open(文件路径，访问模式)
# 注意：文件夹是不支持创建的
fp=open('test.txt',mode='a',encoding='utf-8')
# 注意：文件存在，写入文件时会先清空文件中的内容，然后开始写入
fp.write("你好：lyy\n"*5)

fp.close()
# 读数据
#通过打开文件读取数据
fp=open('test.txt',mode='w',encoding='utf-8')
# readlines 会以多行的形式读取数据，但是会以一个列表的形式返回出去
# data=fp.readlines()
# print(data)
# 字符的序列化和反序列化
# json.dumps(obj)：将对象转换成json字符串序列
info_list=['name','age']
tmp_data=json.dumps(info_list)
print(tmp_data)
fp.write(tmp_data)
# dump的应用
json.dump(info_list,fp)
contact = ['13605810514', '18458125250', '13260504385', '15696539969', '13777575482', '13456878447']
# contact=['李武'，'朱玉杰'，'彭卫勇'，'许劲','杨帅'，'陶秀发']
contact_take_order=[contact[1],contact[0],contact[2],contact[3]]
contact_else=[contact[1],contact[0],contact[4],contact[5]]
print(f"contact_take_order:{contact_take_order}")
print(type(contact_take_order))
print(contact_else)
print(type(contact_else))
message="包装 环节 ，超4时未处理:4单5行14426台请及时处理"
message=message[:2]
print(len(message))
print(message)
