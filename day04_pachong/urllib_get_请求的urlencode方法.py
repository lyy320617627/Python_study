"""
通过代码演示urlencode方法的使用
urlencode应用场景:多个参数的时候
"""
import urllib.request
import urllib.parse
url="http://www.baidu.com/?s"
data={
    'wd':"周杰伦",
    'sex':'男'
}
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
}
data=urllib.parse.urlencode(data)
url=url+data
response=urllib.request.urlopen(url)
response=response.read().decode('utf-8')
print(response)
