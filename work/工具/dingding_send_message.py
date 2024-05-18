import requests
import json

# 钉钉机器人的Webhook URL
webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=16042d865568e6e27d40e46ded567e547048245ca7940724b4df37bd4a3c5207"

# 要发送的Excel文件路径
excel_file_path = 'C:\\Users\\ly320\\Desktop\\test.xlsx'

# 构建消息体
msg = {
    "msgtype": "file",
    "file": {
        "media_id": excel_file_path
    }
}

# 发送消息
response = requests.post(webhook_url, json=msg)

# 打印响应结果
print(response.json())