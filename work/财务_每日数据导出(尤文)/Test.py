import os
import requests


def send_file_to_dingtalk_group(app_key, app_secret, chat_id, file_path):
    # Step 1: Get access token
    def get_access_token():
        url = 'https://oapi.dingtalk.com/gettoken'
        params = {
            'appkey': app_key,
            'appsecret': app_secret
        }
        response = requests.get(url, params=params)
        result = response.json()
        if result.get('errcode') == 0:
            return result['access_token']
        else:
            raise Exception(f"Error getting access token: {result['errmsg']}")

    # Step 2: Upload file to get media_id
    def upload_file(access_token, file_path):
        url = f'https://oapi.dingtalk.com/media/upload?access_token={access_token}&type=file'
        with open(file_path, 'rb') as file:
            files = {'media': file}
            response = requests.post(url, files=files)
            result = response.json()
            if result.get('errcode') == 0:
                return result['media_id']
            else:
                raise Exception(f"Error uploading file: {result['errmsg']}")

    # Step 3: Send file to the group
    def send_message(access_token, chat_id, media_id):
        url = f'https://oapi.dingtalk.com/chat/send?access_token={access_token}'
        headers = {'Content-Type': 'application/json'}
        data = {
            'chatid': chat_id,
            'msg': {
                'msgtype': 'file',
                'file': {
                    'media_id': media_id
                }
            }
        }
        response = requests.post(url, json=data, headers=headers)
        result = response.json()
        if result.get('errcode') == 0:
            print('文件发送成功!')
        else:
            raise Exception(f"发送消息错误: {result['errmsg']}")

    try:
        # Execute the steps
        access_token = get_access_token()
        media_id = upload_file(access_token, file_path)
        send_message(access_token, chat_id, media_id)

        # Delete the original and renamed files
        if os.path.exists(file_path):
            os.remove(file_path)
        print(f"文件已成功发送并删除: {file_path}")
    except Exception as e:
        print(f"操作失败: {e}")


# Example usage
app_key = 'your_app_key'
app_secret = 'your_app_secret'
chat_id = 'your_chat_id'
file_path = '/path/to/your/file.zip'

send_file_to_dingtalk_group(app_key, app_secret, chat_id, file_path)
