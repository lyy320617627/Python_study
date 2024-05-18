"""
演示urllib的一个类型和六个方法
一个类型：HTTPResponse
六个方法：read readline readlines getconde geturl getheaders
"""
import urllib.request
url="http://www.baidu.com"
response = urllib.request.urlopen(url)
# 表示读出多少个字符数据
# content=response.read(5)
# 读取数据的一行
# content=response.readline()
# readlines():读取数据的一行一行数据
# content=response.readlines()
# print(type(content))
# 返回程序应用的状态码
# content=response.getcode()
# getUrl:返回程序调用的地址
# content=response.geturl()
# getheaders():返回请求的请求头
content=response.getheaders()
print(content)
contact = ['18458125250', '13260504385', '15696539969', '13777575482', '13456878447']



