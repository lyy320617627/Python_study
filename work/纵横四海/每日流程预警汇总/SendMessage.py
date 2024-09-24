import requests
import json


def get_access_token(app_key, app_secret):
    url = f"https://oapi.dingtalk.com/gettoken?appkey={app_key}&appsecret={app_secret}"
    response = requests.get(url)
    response_data = response.json()
    if response_data["errcode"] == 0:
        return response_data["access_token"]
    else:
        raise Exception(f"Failed to get access token: {response_data['errmsg']}")


def upload_file_to_dingtalk(file_path, access_token):
    url = f"https://oapi.dingtalk.com/media/upload?access_token={access_token}&type=file"
    files = {'media': open(file_path, 'rb')}
    response = requests.post(url, files=files)
    response_data = response.json()
    if response_data["errcode"] == 0:
        return response_data["media_id"]
    else:
        raise Exception(f"Failed to upload file: {response_data['errmsg']}")


def send_file_to_user(user_id, media_id, access_token):
    url = f"https://oapi.dingtalk.com/message/send?access_token={access_token}"
    headers = {"Content-Type": "application/json"}
    data = {
        "touser": user_id,
        "agentid": "your_agent_id",
        "msgtype": "file",
        "file": {
            "media_id": media_id
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_data = response.json()
    if response_data["errcode"] == 0:
        print("File sent successfully!")
    else:
        raise Exception(f"Failed to send file: {response_data['errmsg']}")


if __name__ == "__main__":
    # 钉钉应用的 app_key 和 app_secret
    app_key = "your_app_key"
    app_secret = "your_app_secret"

    # 获取 access_token
    access_token = get_access_token(app_key, app_secret)

    # 文件路径
    file_path = "path/to/your/file.txt"

    # 上传文件并获取 media_id
    media_id = upload_file_to_dingtalk(file_path, access_token)

    # 用户 ID，可以是钉钉用户的手机号或用户 ID
    user_id = "user_dingtalk_id"

    # 发送文件
    send_file_to_user(user_id, media_id, access_token)
