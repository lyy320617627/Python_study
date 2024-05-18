"""演示字典的常用操作"""
my_dict={"lyy":99,"zmk":88}
# 向字典中新增加一个键值对
#字典[key]=value
# 结果：如果字典中存在对应的key，则对应key对应的value则会被更新如果不存在，则会添加一个新的键值对
# 新增加一个键值对
my_dict["zmkkk"]=100
print(my_dict)
#修改已经存在的键值对
my_dict['zmkkk']=200
print(my_dict)
# 删除字典中已经存在的值
#字典.pop(key)：删除字典中存在key对应的value值,同时返回对应的key对应的value
socre=my_dict.pop('lyy')
print(socre)
print(my_dict)
# my_dict.pop('zmkkkkk')
# 字典清空
# 字典.clear()
# 结果：把整个字典的内容清空掉
my_dict.clear()
print(my_dict)
# 获取字典中的全部keys
# 字典.keys(): 得到字典对应的所有key值
my_dict={"lyy":99,"zmk":88}
keys=my_dict.keys()
print(type(keys))
print(keys)



