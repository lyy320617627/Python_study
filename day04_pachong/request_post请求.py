import json

import requests
"""
使用request的post请求
"""
url="https://fanyi.baidu.com/sug"
headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }
data={
    'kw':'eye'
}
req=requests.post(url=url,headers=headers,data=data)
print(req.json())
print(f"req:{req}")
response_text=req.text
obj=json.loads(response_text)
print(obj)
