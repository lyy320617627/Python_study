"""
通过爬虫下载豆瓣电影的第一页
"""
# get请求
# 获取电影排行的第一页的数据，并且保存起来
import urllib.request
import urllib.parse
url = 'https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start=0&limit=20'
headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}
request=urllib.request.Request(url=url,headers=headers)
# 1.请求对象的定制
response=urllib.request.urlopen(request)
# 2.获取相应的对象
content=response.read().decode('utf-8')
print(content)
# 3.数据下载到本地
# open方法默认情况下使用的是gbk的编码，如果我们想要保存汉字 那么需要要使用encoding=utf-8的形式，把文件保存成汉字形式
fp=open('douban.json','w',encoding='utf-8')
fp.write(content)
with open('douban1.json','w',encoding='utf-8') as fp:
        fp.write(content)
