import requests
import os
from datetime import datetime

class SendMessage():
    # 配置你的 AppKey 和 AppSecret
    def __init__(self):
        self.__APP_KEY = 'dingc8wtmaib95vi3ifz'
        self.__APP_SECRET = 'XR4vKpX7Wt4iLK2WE-1IbI_THLwaynDYC6Be0j0j9Fl3e_ev39P9WRu_Fin4GhFt'
        self.__CHAT_ID = 'Chatf2dea949dfb343e0381d7804C91ff828'  # 群组 ID
        self.__access_token =self.get_access_token()
        self.__time_format=self.get_date_range()
        self.__file_path=f"{self.get_desktop_path()}\\司库系统导出文件汇总({self.__time_format}).zip"
        self.__media_id=self.upload_file()
        print(f"文件的路径为:{self.__file_path}")
    def get_desktop_path(self):
        return os.path.join(os.path.expanduser("~"), "Desktop")
    def get_date_range(self):
        today = datetime.today()
        month_start = today.replace(day=1)
        month_start_str = month_start.strftime('%m.%d').lstrip('0')
        today_str = today.strftime('%m.%d').lstrip('0')
        return f"{month_start_str}-{today_str}"

    def get_access_token(self):
        url = 'https://oapi.dingtalk.com/gettoken'
        params = {
            'appkey': self.__APP_KEY,
            'appsecret': self.__APP_SECRET
        }
        response = requests.get(url, params=params)
        result = response.json()
        if result['errcode'] == 0:
            return result['access_token']
        else:
            raise Exception(f"Error getting access token: {result['errmsg']}")

    def upload_file(self):
        url = f'https://oapi.dingtalk.com/media/upload?access_token={self.__access_token}&type=file'
        files = {'media': open(self.__file_path, 'rb')}
        response = requests.post(url, files=files)
        result = response.json()
        if result['errcode'] == 0:
            return result['media_id']
        else:
            raise Exception(f"Error uploading file: {result['errmsg']}")

    def send_message(self):
        url = f'https://oapi.dingtalk.com/chat/send?access_token={self.__access_token}'
        headers = {'Content-Type': 'application/json'}
        data = {
            'chatid': self.__CHAT_ID,
            'msg': {
                'msgtype': 'file',
                'file': {
                    'media_id': self.__media_id
                }
            }
        }
        response = requests.post(url, json=data, headers=headers)
        result = response.json()
        if result['errcode'] == 0:
            print('File sent successfully!')
        else:
            raise Exception(f"Error sending message: {result['errmsg']}")
if __name__ == '__main__':
    sendmessage=SendMessage()
    sendmessage.send_message()

