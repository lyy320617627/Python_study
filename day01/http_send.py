import requests
import json
# 设置请求的URL
url = 'https://api.yingdao.com/api/console/app/queryAppUseRecordList'

# 设置请求头，包括token
headers = {
    'Authorization': access_token,
    'Content-Type': 'application/json'
}

# 设置请求的数据
data = {
  "page": 1,
  "size": 1,
  "appId": "803c6184-a751-4514-8b10-65172a73fa04"
}

# 发送POST请求
response = requests.post(url, headers=headers, json=data)



# 打印响应内容
runstateName=(response.json()['data'][0]['runStatusName'])