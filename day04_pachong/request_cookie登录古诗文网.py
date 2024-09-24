""""
绕过登录去爬取古诗文网的内容
"""
import requests

session=requests.sessions.Session()

log_url="https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.aspx"
headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }
response=session.get(url=log_url,headers=headers)
content=response.text
from bs4 import BeautifulSoup
soup=BeautifulSoup(content,'lxml')
viewstatus=soup.select("#__VIEWSTATE")[0].attrs.get('value')
VIEWSTATEGENERATOR=soup.select('#__VIEWSTATEGENERATOR')[0].attrs.get('value')
print(viewstatus)
print(VIEWSTATEGENERATOR)
# 获取验证码的url地址
code=soup.select("#imgCode")[0].attrs.get('src')
# 获取了验证码的图片之后 下载到本地 然后观察验证码 观察之后 然后在控制台输入这个验证码 就可以将这个值给code
# code的参数 就可以登录
# 通过urllib下载验证码的图片
"""
# 有坑：通过调用urllib.requests.urlretrieve再次调用时，和requests不是同一个请求
import urllib.request
code_jpg=urllib.request.urlretrieve(code_url,filename='code.jpg')
print(code_jpg)
"""
# 方法：requests里面有一个方法 session() 通过session的返回值 就能使用请求变成一个对象
code_url='https://so.gushiwen.cn'+code
response_code=session.get(code_url)
content_code=response_code.content
with open('code.jpg','wb') as fp:
    fp.write(content_code)

code_name=input("请输入你的验证码")
# 调用登录接口
post_url="https://so.gushiwen.cn/user/login.aspx?from=http%3a%2f%2fso.gushiwen.cn%2fuser%2fcollect.aspx"
post_data={
    '__VIEWSTATE':viewstatus,
    '__VIEWSTATEGENERATOR': VIEWSTATEGENERATOR,
    'from': 'https://www.gushiwen.cn/',
    'email': 'ly320617627@163.com',
    'pwd': 'www.jj123456',
    'code': code_name,
    'denglu': '登录'
}
response_post=session.post(url=post_url,headers=headers,data=post_data)
print(response_post)
content_post=response_post.text
with open('gushiwen.html','w',encoding='utf-8') as fp:
    fp.write(content_post)




