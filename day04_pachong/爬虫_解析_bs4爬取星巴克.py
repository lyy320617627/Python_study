"""
通过bs解析星巴克官网来爬取所有的饮料和图片
"""
import urllib

from bs4 import BeautifulSoup
from urllib import request
from urllib import parse
import json
url="https://www.starbucks.com.cn/menu/"
request=urllib.request.Request(url)
response=urllib.request.urlopen(request)
content=response.read().decode('utf-8')
soup=BeautifulSoup(content,'lxml')
name_list=soup.select('ul[class="grid padded-3 product"] strong')
for name in name_list:
    print(name.get_text())



