# 数据采集的时候 绕过登录 然后进入到某个页面
# 个人信息页面是utf-8  但是还是报错了编码错误 因为并没有进入到个人信息页面 而是跳转到登录页面
# 登录页面不是utf-8 所以报编码错误
import urllib.request
import urllib.parse
import json1
url="https://weibo.com/ajax/getNavConfig"
headers={
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
'Cookie':'XSRF-TOKEN=Hip6THXIq1TB6Swx8Wa6vMqy; SUB=_2A25LQHyTDeRhGeNG4lYV9i7MzjWIHXVoPPBbrDV8PUNbmtANLUrskW9NSuz_6SbxxfNQjSGylrMA60pGjEX0cyJo; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFKcI1-J-OQ3ZrppDV4BCXg5JpX5KzhUgL.Fo-R1KBXSo57SK.2dJLoIE5LxK-LBo5L12qLxK.L1-BL1KzLxK-LBo.LBoBESKq41Btt; ALF=02_1718327747; WBPSESS=hmNG8jMbphrTMCyKv_PS66X0Q_qd8LEhHsl5Yt1ZAWrxPmULFwXqzJGNH7hJHZm__oSq3zW62yjoYFBDKRVsCLcNJTOHquCWSwPxPT9USq4Xmclac6Mg624-NiN2VgPteqv1EVYv8FhCRZuhXlKX_w==',
'Referer':'https://weibo.com/u/5894460059'
}
# 相应对象的定制
request=urllib.request.Request(url=url,headers=headers)
# 获取相应的对象
response=urllib.request.urlopen(request)
# 获取响应的源码
content=response.read().decode('utf-8')
with open('cookie.html','w',encoding='utf-8') as fp:
    fp.write(content)
print(content)
