"""
通过代码演示urllib代理的使用
"""
import urllib.request
import urllib.parse
url="http://www.baidu.com/s?wd=ip"
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
         }
request=urllib.request.Request(url=url,headers=headers)
# response = urllib.request.urlopen(request)
# content=response.read().decode('utf-8')
proxies={
    'http':'59.54.238.249:21042',

}
handler=urllib.request.ProxyHandler(proxies=proxies)
opener=urllib.request.build_opener(handler)
content=opener.open(request)

with open('baidu.html','w',encoding='utf-8') as fp:
    fp.write(content)