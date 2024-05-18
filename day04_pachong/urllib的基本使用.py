"""
爬虫中urllib的基本使用
"""
import urllib.request
url="http://www.baidu.com"
response = urllib.request.urlopen(url)
# read:读取的是二进制形式
content=response.read().decode('utf-8')
print(content)