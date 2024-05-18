"""
通过代码演示下载豆瓣电影的前十页
"""
import json1
import urllib.request
import urllib.parse
# 下载豆瓣电影的前十页数据
# （1） 请求对象的定制
#  (2) 获取相应的对象
#  (3) 相应数据的下载
# 程序的入口
def create_request(page):
    page=(page-1)*20
    base_url='https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&'
    data={
        'start':page,
        'limit':20
    }
    data=urllib.parse.urlencode(data)
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    url=base_url+data
    response=urllib.request.Request(url=url,headers=headers)
    return response
def get_content(request):
    response=urllib.request.urlopen(request)
    content=response.read().decode('utf-8')
    return content
def download_file(page,content):
     with open('douban_'+str((page-1)/20)+'.json','w',encoding='utf-8') as fp:
         fp.write(content)
if __name__ == '__main__':
    start_page=1
    end_page=10
    for page in range(start_page,end_page+1):
        request=create_request(page)
        content=get_content(request)
        download_file(page,content)