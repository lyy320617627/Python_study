"""
通过代码演示handler代码的基本使用
"""
# 需求 使用handler来访问百度 获取网页源码
import urllib.request
url="https://www.baidu.com"
headers={
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}
# 请求对象的定制
requests=urllib.request.Request(url=url,headers=headers)
# 获取handler对象
handler=urllib.request.HTTPHandler()
# 获取openr方法
opener=urllib.request.build_opener(handler)
# 使用打开方法
response=opener.open(requests)
content=response.read().decode('utf-8')
print(content)
