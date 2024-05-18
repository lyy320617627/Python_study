
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, os, time
import requests, json, os, time, re
from email.mime.image import MIMEImage



def send_message(file_path1):

    # 1.获取接口凭证
    def getAccess_token():
        # 从小程序应用信息处获取
        appkey = 'dingc8wtmaib95vi3ifz'  # 不要配置服务器ip
        appsecret = 'XR4vKpX7Wt4iLK2WE-1IbI_THLwaynDYC6Be0j0j9Fl3e_ev39P9WRu_Fin4GhFt'  # 不要配置服务器ip

        url = 'https://oapi.dingtalk.com/gettoken?appkey=%s&appsecret=%s' % (appkey, appsecret)

        headers = {
            'Content-Type': "application/x-www-form-urlencoded"
        }
        data = {'appkey': appkey,
                'appsecret': appsecret}
        r = requests.request('GET', url, data=data, headers=headers)
        access_token = r.json()["access_token"]

        return access_token

    # 2.获取Midia_id
    def getMedia_id(file_path):
        access_token = getAccess_token()
        # 本地文件的绝对路径
        url = r'https://oapi.dingtalk.com/media/upload?access_token=%s&type=file' % access_token
        files = {'media': open(file_path, 'r')}
        data = {'access_token': access_token,
                'type': 'file'}
        response = requests.post(url, files=files, data=data)
        json = response.json()
        print(json["media_id"])
        return json["media_id"]

    # 3.文件发送
    def SendFile():
        access_token = getAccess_token()

        # 循环获取指定列表文件，发送指定钉钉群聊

        file_path = file_path1
        # file_path=r"C:\Users\RPA1-1\Desktop\OAO自动生成通报表格\固定表格模板.xlsx"

        print(file_path)
        # 将文件名传给getMedia_id
        media_id = getMedia_id(file_path)
        # 获取群聊Id
        chatid = 'chat58714d2798355e1f579ebe9c09958a2f'
        url = 'https://oapi.dingtalk.com/chat/send?access_token=' + access_token
        header = {
            'Content-Type': 'application/json'
        }
        data = {'access_token': access_token,
                'chatid': chatid,
                'msg': {
                    'msgtype': 'file',
                    'file': {'media_id': media_id}
                }
                }
        r = requests.request('POST', url, data=json.dumps(data), headers=header)
        print(r.json())
        print('发送成功')

    SendFile()
send_message(file_path1)


