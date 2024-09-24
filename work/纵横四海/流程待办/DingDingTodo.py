import requests
import json
import time


class DingDingTodo:
    def __init__(self, app_key, app_secret):
        self.app_key = app_key
        self.app_secret = app_secret
        self.base_url = "https://oapi.dingtalk.com"
        self.access_token = self.get_access_token()

    def get_access_token(self):
        url = f"{self.base_url}/gettoken"
        params = {
            "appkey": self.app_key,
            "appsecret": self.app_secret
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            result = response.json()
            if result.get("errcode") == 0:
                print(f"获取到的access_token为:{result.get('access_token')}")
                return result.get("access_token")
            else:
                raise Exception(f"Error getting access token: {result.get('errmsg')}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get access token: {str(e)}")

    def create_todo(self, userid, subject, description, due_time):
        url = f"{self.base_url}/topapi/workrecord/add"
        headers = {
            "Content-Type": "application/json"
        }
        params = {
            "access_token": self.access_token
        }
        data = {
            "userid": userid,
            "create_time": int(time.time() * 1000),
            "title": subject,
            "url": "https://example.com",  # 修改为你需要跳转的URL
            "formItemList": [
                {"title": "描述", "content": description},
                {"title": "截止时间", "content": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(due_time / 1000))}
            ]
        }
        try:
            response = requests.post(url, headers=headers, params=params, json=data)
            response.raise_for_status()
            result = response.json()
            if result.get("errcode") == 0:
                return result.get("record_id")
            else:
                raise Exception(f"Error creating todo: {result.get('errmsg')}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to create todo: {str(e)}")

    def get_userid_by_mobile(self, mobile):
        url = f"{self.base_url}/topapi/v2/user/getbymobile"
        params = {
            "access_token": self.access_token
        }
        data = {
            "mobile": mobile
        }
        try:
            response = requests.post(url, params=params, json=data)
            response.raise_for_status()
            response_data = response.json()
            if response_data["errcode"] == 0:
                return response_data["result"]["userid"]
            else:
                raise Exception(f"Error getting userid by mobile: {response_data}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get userid by mobile: {str(e)}")


if __name__ == '__main__':
    mobile = "17767253656"
    app_key = 'dingc8wtmaib95vi3ifz'
    app_secret = 'XR4vKpX7Wt4iLK2WE-1IbI_THLwaynDYC6Be0j0j9Fl3e_ev39P9WRu_Fin4GhFt'
    userid = 'user_id'
    subject = '纵横四海项目采购项目进度明细预警'
    description = '纵横四海项目采购项目进度明细预警(description)'
    due_time = int(time.time() * 1000) + 24 * 60 * 60 * 1000  # 24 hours from now

    dingding_todo = DingDingTodo(app_key, app_secret)

    try:
        userid = dingding_todo.get_userid_by_mobile(mobile)
        print(f"获取到的userid为:{userid}")
        task_id = dingding_todo.create_todo(userid, subject, description, due_time)
        print(f"Todo created with task_id: {task_id}")
    except Exception as e:
        print(f"Error: {e}")
