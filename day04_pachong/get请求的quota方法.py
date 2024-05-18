import urllib.request
import urllib.parse
url="http://www.baidu.com/s?wd="
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
         }
response=urllib.request.urlopen(url)
content=response.read()
name=urllib.parse.quote("周杰伦")
url=url+name
url=urllib.request.Request(url=url,headers=headers)
print(content)