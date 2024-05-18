import requests
import json
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
import urllib.request
import urllib.parse
from requests.adapters import HTTPAdapter
import ssl
class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        kwargs['ssl_context'] = context
        return super(SSLAdapter, self).init_poolmanager(*args, **kwargs)

def create_request(page,authorization,cookie):
    base_url="https://wap.zj.10086.cn/ai/shopkf/oneframe/qrySession/qrySessions"
    data = {
    "authAgentId": "undefined",
    "start": page,
    "pageNum": 10,
    "starttimeStart": "",
    "starttimeEnd": "",
    "tenantId": "ff8080826537c4fc016538bd3b010089",
    "undefined": "不限",
    "session": "",
    "siginid": "",
    "agentid": "",
    "user": "",
    "type": "不限"
    }
    headers={
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': cookie,
        'Referer': 'https://wap.zj.10086.cn/ai/shopkf/ucfront/log/html/qrySession.html',
        'Authorization': authorization
    }
    # data=urllib.parse.urlencode(data).encode('utf-8')
    # print(data)
    try:
        # 创建一个会话
        session = requests.Session()
        # 安装自定义 SSL 适配器
        session.mount('https://', SSLAdapter())
        # 发送 POST 请求
        response = session.post(base_url, headers=headers, data=data)

        # response = requests.post(url=base_url, data=data, headers=headers, verify=False)
        print(response)
        # request=urllib.request.Request(url=base_url,data = data,headers=headers)
    except Exception as e:
        print("异常：",str(e))
        raise
    # request=requests.post(url=base_url,data=data,headers=headers)
    # content=urllib.request.urlopen(request)
    # print(content.read().decode('utf-8'))


    #请求频率过于频繁
    # r = requests.request('POST', base_url, data=data, headers=headers)
    # print(r.json())
    print(request)
    return request
def get_content(request):
    response=urllib.request.urlopen(request)
    content=response.read().decode('utf-8')
    print(content)
    return content
def download_file(page,content):
    with open("json_kendeji"+str(page)+".json",'w',encoding='utf-8') as fp:
        fp.write(content)


if __name__ == '__main__':
    Authorization='Bearer 2cc5221f-8229-4360-84df-84b8c7d03377'
    cookie='STSESSION=6388A7B8F77FC2FEB174E95C67EE84A0; SINOSESSION_ID_=87fe408070f44572a0e193e2153751cb; ha-wap-pas=c1b26a4764c38987; waparrayid=wapserv_ec_20230907_03; VALIDATE_ID=AUTH_SMS20240517MtCRZDsT02; tokenInfo=%7B%22access_token%22%3A%222cc5221f-8229-4360-84df-84b8c7d03377%22%2C%22scope%22%3A%22all%22%2C%22staff_id%22%3A%22znydadmin%22%2C%22token_type%22%3A%22bearer%22%2C%22expires_in%22%3A43199%2C%22targetUrl%22%3A%22https%3A//wap.zj.10086.cn/ai/shopkf/ucfront/index.html%22%2C%22client_id%22%3A%22ucfront%22%7D'
    # start_page=int(input("请输入起始页码"))
    # end_page=int(input("请输入结束页码"))
    start_page = 0
    end_page = 0
    for page in range(start_page,end_page+1):
#       获取请求体
        request=create_request(page,Authorization,cookie)
        # content=get_content(request)
        # print(content)