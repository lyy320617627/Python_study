import requests
"""
    通过代码演示requests请求代理的使用
"""
url="https://www.baidu.com/s?"
headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }
data={
    'wd':'ip'
}
proxy={
    'http':'58.100.94.148:8080'
}
response=requests.get(url=url,headers=headers,params=data,proxies=proxy)
content=response.text
with open('response.html','w',encoding='utf-8') as fp:
    fp.write(content)