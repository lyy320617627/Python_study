from lxml import etree
# xpath的两种使用方法
# 解析本地文件 etree.parse()
# 解析网页响应的数据 etree.HTML()
"""
xpath基本语法：
1.路径查询:
//:查找所有子孙节点，不考虑层级关系
/:找直接子节点
2.谓词查询
//div[@id]
//div[@id='maincontent'] 其中div对应标签的属性名
3.属性查询
//@class
4.模糊查询
//div[contains(@id,'he')]
//div[starts-with(@id,'he')] 其中div对应标签的属性名  
5.内容查询
//div/h1/text()
6.逻辑查询
//div[@id='head' and @class='s_down]
//title | //price
"""
tree=etree.parse('urllib_xpath的基本使用.html')
print(tree)
# tree.xpath('xpath路径')
# 查找ul下面的li
list_li=tree.xpath('//body/ul/li')
print(list_li)
# 判断列表的长度
print(len(list_li))
# 查找所有有id属性的li标签
# text():获取标签中的内容
list_li=tree.xpath('//body//li[@id]/text()')
print(list_li)
# 找到标签id为l1的标签的文本内容 //ul/li[@id='l1']/text()
list_li=tree.xpath("//ul/li[@id='l1']/text()")
print(list_li)
# 查找到id为l1的li标签的class的属性值
class_content=tree.xpath("//ul/li[@id='l1']//@class")
print(class_content)
# 查找所有li标签中id包含l的标签的文本内容 //li[contains(@id, 'l')]/text()
contains_l=tree.xpath("//ul/li[contains(@id, 'l')]/text()")
print(contains_l)
# 查询id的值以l开头的li标签中的内容
start_with=tree.xpath("//ul/li[starts-with(@id,'l')]/text()")
print(f"starts-with开头的文本的内容:",start_with)
# 查询id为l1而且class为lyy的li标签中的内容
l1_and_lyy=tree.xpath("//ul/li[@id='l1' and @class='lyy']/text()")
print(l1_and_lyy)
# 查询id为l1或者id为c3的li标签中的内容 |:只能通过标签进行或操作而标签中的内容不能通过或标签内容进行判断
# l1_or_c3=tree.xpath("//ul/li[@id='l1' or @id='c3']/text()")
l1_orc3=tree.xpath("//ul/li[@id='l1']/text() | //ul/li[@id='c3']/text()")
print(l1_orc3)