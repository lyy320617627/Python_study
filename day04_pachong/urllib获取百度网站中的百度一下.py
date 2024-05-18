"""
获取百度网站中的百度一下
"""
# 获取网页的源码
# 解析 解析服务器响应的文件 tree.HTML()
# 打印获取到的内容
import urllib.request
import urllib.parse
from lxml import etree
import json1
url="http://www.baidu.com"
headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
             }
# 请求对象的定制
request = urllib.request.Request(url=url,headers=headers)
response=urllib.request.urlopen(request)
content=response.read().decode('utf-8')
print(content)
# 相应内容的解析
detail_content=etree.HTML(content)
print()
baiduyixia=detail_content.xpath("//input[@id='su']/@value")[0]
print(baiduyixia)