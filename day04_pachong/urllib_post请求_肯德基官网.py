"""
通过post请求，请求肯德基官网的位置信息
"""
"post请求官网地址: https://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=cname"
"""
cname: 北京
pid: 
pageIndex: 1
pageSize: 10
"""
import json1
import urllib.request
import urllib.parse
def create_request(page):
    base_url="https://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=cname"
    data={
        'cname': '北京',
        'pid':'',
        'pageIndex':str(page),
        'pageSize': '10'
    }
    headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
             }
    data=urllib.parse.urlencode(data).encode('utf-8')
    request=urllib.request.Request(url=base_url,data=data,headers=headers)
    return request
def get_content(request):
    response=urllib.request.urlopen(request)
    content=response.read().decode('utf-8')
    return content
def download_file(page,content):
    with open("json_kendeji"+str(page)+".json",'w',encoding='utf-8') as fp:
        fp.write(content)


if __name__ == '__main__':
    start_page=int(input("请输入起始页码"))
    end_page=int(input("请输入结束页码"))
    for page in range(start_page,end_page+1):
#       获取请求体
        request=create_request(page)
#       获取相应的源码
        content=get_content(request)
        download_file(page,content)
