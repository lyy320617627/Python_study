import requests
import json
import hmac
import hashlib
import base64
import urllib.parse
import time

class DingTalkAPI:
    def __init__(self, webhook_url, secret):
        self.webhook_url = webhook_url
        self.secret = secret

    def generate_sign(self):
        timestamp = str(round(time.time() * 1000))
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return timestamp, sign

    def send_text_message(self, message):
        timestamp, sign = self.generate_sign()
        url = f"{self.webhook_url}&timestamp={timestamp}&sign={sign}"

        data = {
            "msgtype": "text",
            "text": {
                "content": message
            },
            "at": {
                "atMobiles": ["17767253656"],
                "isAtAll": False
            }
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        result = response.json()

        if result.get("errcode") == 0:
            return result
        else:
            raise Exception(f"消息发送失败: {result.get('errmsg')}")
def sendMessage():
    webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=2e68523b96aa842d7ce5834057c44f6cd63270d2a53f811a9957eadddd55771e"
    secret = "SEC00d8c3223fbe38b9349c6878a56fc20e4f948c2daf550b5f3b2d51745c00cabb"
    message = "这是发送到钉钉群里的消息"
    # at_mobiles = ["17767253656"]
    ding_api = DingTalkAPI(webhook_url, secret)
    try:
        # 发送消息到指定群聊
        result = ding_api.send_text_message(message)
        print("消息发送成功:", result)

    except Exception as e:
        print("操作失败:", e)

sendMessage()