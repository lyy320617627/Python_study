import urllib.parse

import requests
"""
# 总结：
(1):参数使用params传递
(2):参数无需使用urlencode编码
(3):不需要请求对象的定制
(4)：请求资源路径中的?可以加也可以不加
"""
url="https://www.baidu.com/?s"
# response=requests.get(url)
# response.encoding="utf-8"

# # requests的一个类型和六个属性
# # requests.get返回的类型是Response
# # response.text:返回的是网页源码
# print(response.text)
# # response.url:返回的是请求的url
# print(f"url:{response.url}")
# # response.content:返回的是二进制的数据
# print(f"response_content:{response.content}")
# # response.status_code:返回响应的状态码
# print(f"response.status_code:{response.status_code}")
# # response.headers:返回的是响应的请求头信息
# print(f"response.headers:{response.headers}")
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
}
data={
    'wd':"北京"
}
response=requests.get(url=url,headers=headers,params=data)
response_data=requests.get(url=url,headers=headers,data=data)
response_data_text=response_data.text
response_text=response.text
print(f"response_text:{response_text}")
# print(response_text==response_data_text)
