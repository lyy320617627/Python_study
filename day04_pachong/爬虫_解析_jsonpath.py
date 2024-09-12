import json
import jsonpath

"""
json中方法的讲解:
loads：将json字符串解码为Python数据类型。它接收一个json字符串作为输入，并返回一个Python对象（通常是字典或者列表），该对象应用与JSON数据结构。
dumps：方法将Python数据类型编码为JSON格式的字符串。它用于接收一个Python对象（通常是字典或者列表）作为1输入，
并返回一个JSON字符串，该字符串表示了Python对象的结构。
注意:jsonpath只能遍历json字符串

"""
# loads:把json对象转换成基本的Python对象
obj=json.load(open("爬虫_解析_jsonpath.json",'r',encoding='utf-8'))
# print(obj
# 书店所有书的作者
# '$.store.book[0].author': 可以通过下标来获取相对应的值
# '$.store.book[*].author':表示获取所有书店书店的书的作者
author_list=jsonpath.jsonpath(obj,'$.store.book[0].author')
print(author_list)
# 获取所有的作者
author_list=jsonpath.jsonpath(obj,'$..author')
print(author_list)
# 获取store下面所有的标签
target_list=jsonpath.jsonpath(obj,'$.store.*')
print(f"target_list={target_list}")
# 获取store里面所有的price
price_list=jsonpath.jsonpath(obj,"$.store.book..price")
print(price_list)
# 获取第三本书
book=jsonpath.jsonpath(obj,"$..book[2]")
print(book)
# 获取最后一本书
last_book=jsonpath.jsonpath(obj,"$..book[(@.length-1)]")
print(last_book)
# 获取前面的两本书
book_list=jsonpath.jsonpath(obj,"$..book[0,1]")
book_list=jsonpath.jsonpath(obj,"$..book[:2]")
print(book_list)
# 条件过滤中需要在()的前面添加一个?
# 过滤出所有包含isbn的书
book_list=jsonpath.jsonpath(obj,"$..book[?(@.isbn)]")
print(book_list)
# 过滤出所有价格超过十块钱的书本
book_price_list=jsonpath.jsonpath(obj,"$..book[?(@.price>10)]")
print(book_price_list)