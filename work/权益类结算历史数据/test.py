import os
import requests
import json
import rarfile
from pyunpack import Archive


class SendMessage:
    def send_message(self, file_path1):
        # 获取接口凭证
        def getAccess_token():
            appkey = 'dingc8wtmaib95vi3ifz'
            appsecret = 'XR4vKpX7Wt4iLK2WE-1IbI_THLwaynDYC6Be0j0j9Fl3e_ev39P9WRu_Fin4GhFt'
            url = 'https://oapi.dingtalk.com/gettoken?appkey=%s&appsecret=%s' % (appkey, appsecret)
            headers = {
                'Content-Type': "application/x-www-form-urlencoded"
            }
            response = requests.get(url, headers=headers)
            result = response.json()
            print(f'getAccess_token response: {result}')
            if 'access_token' in result:
                return result["access_token"]
            else:
                raise Exception(f"Error getting access token: {result}")

        # 压缩文件为RAR
        def compress_to_rar(file_path):
            rar_file_path = file_path + ".rar"
            with rarfile.RarFile(rar_file_path, 'w') as rar:
                rar.write(file_path, os.path.basename(file_path))
            return rar_file_path

        # 获取Midia_id
        def getMedia_id(file_path):
            access_token = getAccess_token()
            url = r'https://oapi.dingtalk.com/media/upload?access_token=%s&type=file' % access_token
            with open(file_path, 'rb') as file:
                files = {'media': file}
                response = requests.post(url, files=files)
                if response.status_code != 200:
                    print(f'Error in media upload, status code: {response.status_code}, response: {response.text}')
                    raise Exception("Error uploading media")
                try:
                    result = response.json()
                except json.JSONDecodeError:
                    print(f'Failed to decode JSON, response text: {response.text}')
                    raise Exception("Failed to decode JSON response from media upload")
                print(f'getMedia_id response: {result}')
                if 'media_id' in result:
                    return result['media_id']
                else:
                    raise Exception(f"钉钉上传文件失败： {result}")

        # 文件发送
        def SendFile():
            try:
                access_token = getAccess_token()
                file_path = file_path1
                print(f'File path: {file_path}')

                # 压缩文件
                rar_file_path = compress_to_rar(file_path)
                print(f'RAR file path: {rar_file_path}')

                media_id = getMedia_id(rar_file_path)
                print(f'media_id: {media_id}')
                chatid = 'chat6a75f4d1da3ad6d5cf04a6dac543804c'
                url = 'https://oapi.dingtalk.com/chat/send?access_token=' + access_token
                headers = {
                    'Content-Type': 'application/json'
                }
                data = {
                    'chatid': chatid,
                    'msg': {
                        'msgtype': 'file',
                        'file': {'media_id': media_id}
                    }
                }
                response = requests.post(url, headers=headers, data=json.dumps(data))
                print(f'SendFile response status code: {response.status_code}')
                print(f'SendFile response text: {response.text}')
                try:
                    result = response.json()
                except json.JSONDecodeError:
                    print(f'Failed to decode JSON, response text: {response.text}')
                    raise Exception("Failed to decode JSON response from chat send")
                print(f'SendFile response: {result}')
                if response.status_code == 200 and 'errcode' in result and result['errcode'] == 0:
                    print('发送成功')
                else:
                    raise Exception(f"发送文件失败：{result}")
            except Exception as e:
                print("发生异常：", str(e))
                raise

        SendFile()


def main(file_path):
    sendMessage = SendMessage()
    sendMessage.send_message(file_path)


if __name__ == "__main__":
    file_path = "path/to/your/file.xlsx"  # 替换为你的文件路径
    main(file_path)
