from bs4 import BeautifulSoup
"""
通过代码研究bs4的基本使用
bs4对象的创建：
服务器响应的文件生成对象
soup=BeautifullSoup(response.read().decode,'lxml')
本地文件生成对象
soup=BeautifulSoup(open('1.html'),'lxml')
注意：默认打开文件的编码格式是gbk所以需要指定打开编码格式
# 获取节点信息某些方法的函数
    (1):获取节点内容:使用与标签中嵌套标签的结构
    obj.string
    obj.get_text()
    (2)：节点的属性
    tag.name 获取标签名
    eg:tag=find('li')
        print(tag.name)
    (3):获取节点属性
    obj.attrs.get('title')【常用】
    obj.get('title')
    obj['title']
    
"""

# 通过解析本地文件 来将bs4的基础语法进行讲解
# 默认打开的文件的编码格式是gbk，所以在打开文件的时候需要指定编码
soup=BeautifulSoup(open('爬虫_解析_bs4的基本使用.html',encoding='utf-8'),'lxml')
# 根据标签名查找节点
# 注意 找到的是第一个符合条件的数据
print(soup.a)
# 注意 attrs返回的是标签的属性
print(soup.a.attrs)
# bs4的一些函数
# 1.find
# 返回的是第一个符合条件的数据
a_list=soup.find('a')
print(soup.find('a'))
print(soup.find('a',title='a2')) #通过筛选title='a2'的标签来获取a标签的属性1
print(soup.find('a',class_='123')) # 注意:class属性值不能直接拿来引用，如果要通过class属性筛选数据，则需要在class后面加上下划线，如：class_
# 2.find_all
# find_all 返回的是一个列表 并且返回所有的a标签
a_find_all_list=soup.find_all('a')
print(f"a_find_all_list={a_find_all_list}")
# 查找所有的a标签和span标签
# 如果想要获取的是多个标签的数据，那么需要在find_all的参数中添加的是列表的数据

a_span_list=soup.find_all(['a','span'])
print(f"a_span_list={a_span_list}")
# 获取所有的a标签，可以使用limit限制返回的数据的数量
two_limit_li=soup.find_all('li',limit=2) # 返回所有的li标签形成的列表，并且限制返回的数量为前两个
print(f"two_limit_li={two_limit_li}")

# 3.select
# select方法返回的是一个列表 并且会返回多个数据
a_select_list=soup.select('a')
print(f"a_select_list={a_select_list}")
# 如果标签中含有class 则可以通过.加上class对应的值来获取指定class属性值的标签的列表
# 可以通过.代表class 这种叫做类选择器
select_123_list=soup.select('.123',limit=1)
print(f"select_123_list={select_123_list}")
# 可以通过#代表id 这种叫做id选择器
id_list=soup.select('#l1')
print(f"id_list={id_list}")
# 属性选择器 通过标签加上[属性名] 来查找标签中含有属性值的元素
li_id_list=soup.select('li[id]')
print(f"li_id_list={li_id_list}")
# 查找li标签中id标签为l2的标签
li_l2_list=soup.select('li[id="l2"]')
print(f"li_l2_list={li_l2_list}")

# 层级选择器
# 后代选择器
# 找到div下面的li
div_li_list=soup.select('div li')
print(f"div_li_list={div_li_list}")
# 子代选择器
# 某标签的第一级子标签
# 形式：标签1>标签2>..>标签n
div_ul_li_list=soup.select('div > ul > li')
print(f"div_ul_li_list={div_ul_li_list}")
# 通过select选择所有的 a标签和li标签
a_li_list=soup.select('a,li')
print(f"a_li_list={a_li_list}")
# 获取节点内容
# 如果标签对象中 只有内容 那么string和get_text()都可以使用
# 如果标签对象中 除了内容还有标签 那么string就获取不到数据 而get_text()是可以获取数据
# 我们一般情况喜 推荐使用get_text()
obj=soup.select('#123')
for li in obj:
    print(li.string)
    print(li.get_text())
# 节点的属性
# 方法：obj.name
# 返回的是标签的名字
# 无论在调用那个方法是一定要注意soup.select返回的是一个列表
obj=soup.select('#123')[0]
print(obj.name)
# find返回的数据类型
print(f"find函数返回的数据类型是:{type(a_list)}")
# find_all返回的数据类型
print(f"fand_all函数返回的数据类型是:{(type(a_find_all_list))}")
# obj.attrs
#将属性作为一个字典返回
print(obj.attrs)
# 获取节点的属性对应的值
print(obj.attrs.get('class'))
print(obj.get('class'))
print(obj['class'])