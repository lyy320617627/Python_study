"""
通过xpath代码爬取站长素材中的数据元素
"""
import urllib.request
import urllib.parse
from lxml import etree
import json1
# 请求对象的定制
# 获取网页的源码
# 下载
# 需求 下载站长素材中前十页图片中的数据
def create_request(page):
    if (page==1):
        url="https://sc.chinaz.com/tupian/siwameinvtupian.html"
    else:
        url="https://sc.chinaz.com/tupian/siwameinvtupian_"+str(page)+".html"
    print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    request=urllib.request.Request(url=url,headers=headers)
    return request
def get_content(request):
    response=urllib.request.urlopen(request)
    content=response.read().decode('utf-8')
    print(content)
    return content
def down_load(content):
    tree=etree.HTML(content)
    # 注意 有的图片会进行懒加载 而对应的url要使用改变之前的
    img_alt=tree.xpath('//img[@class="lazy"]/@data-original')
    img_src=tree.xpath('//img[@class="lazy"]/@alt')
    print(len(img_alt),len(img_src))
    for i in range(len(img_alt)):
        name=img_src[i]
        url="https:"+img_alt[i]
        print(name,url)
        urllib.request.urlretrieve(url=url,filename='./love_img/'+name+".jpg")
if __name__ == '__main__':
    start_page=int(input("请输入起始页码"))
    end_page=int(input("请输入结束页码"))
    for page in range(start_page,end_page+1):
#          请求对象的定制
        request=create_request(page)
#          获取响应的源码
        content=get_content(request)
        # down_load(content)