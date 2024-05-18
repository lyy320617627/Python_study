"""
通过代码演示post请求
"""
import json1
import urllib.request
import urllib.parse
url="https://fanyi.baidu.com/sug"
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
}
data={
    'kw':'spider'
}

# post请求是不会拼接在url的后面的,而是需要放在定制对象的参数中
data=urllib.parse.urlencode(data).encode('utf-8')
print(data)
request=urllib.request.Request(url=url,data=data,headers=headers)
print(request)
# 模拟浏览器向服务器发送请求
response=urllib.request.urlopen(request)
print(response)
content=response.read().decode('utf-8')
print(content)
# 注意：post请求方式的参数 必须编码 data=urllib.parse.urlencode(data)
# 编码之后 必须调用encode方法
# 参数是放在定制请求对象的方法中  requests=urllib.requests.Request(url=url,data=data,headers=headers)
obj=json.loads(content)
print(type(obj))
print(obj)