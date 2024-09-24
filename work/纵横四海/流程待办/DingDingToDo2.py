import requests
import json
import time

class DingDingTodo:
    def __init__(self, app_key, app_secret):
        self.app_key = app_key
        self.app_secret = app_secret
        self.base_url = "https://api.dingtalk.com"
        self.access_token = self.get_access_token()

    def get_access_token(self):
        url = f"https://oapi.dingtalk.com/gettoken"
        params = {
            "appkey": self.app_key,
            "appsecret": self.app_secret
        }
        response = requests.get(url, params=params)
        result = response.json()
        if result.get("errcode") == 0:
            print(f"获取到的access_token: {result.get('access_token')}")
            return result.get("access_token")
        else:
            raise Exception(f"Error getting access token: {result.get('errmsg')}")

    def create_todo(self, user_id1, subject, description, dueTime):
        url = f"{self.base_url}/v1.0/todo/users/{user_id1}/tasks"
        headers = {
            "x-acs-dingtalk-access-token": self.access_token,
            "Content-Type": "application/json"
        }
        data = {
            "subject": subject,
            "executorIds": [user_id1],
            "priority": 40,
            "description":description,
            "isOnlyShowExecutor":False,
            "participantIds":[user_id1],
            "notifyConfigs": {
                "dingNotify": "1"
            }
        }
        if dueTime:
            data["dueTime"] = dueTime

        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        if response.status_code == 200 and 'id' in result:
            return result['id']
        else:
            raise Exception(f"Error creating todo: {result}")

if __name__ == '__main__':
    app_key = 'dingc8wtmaib95vi3ifz'
    app_secret = 'XR4vKpX7Wt4iLK2WE-1IbI_THLwaynDYC6Be0j0j9Fl3e_ev39P9WRu_Fin4GhFt'



    description="lyyyyy测试钉钉待办流程"
    user_id1 = "zrM2t3DBxpotSZvdQiPe9pAiEiE"
    user_id2="zrM2t3DBxpotSZvdQiPe9pAiEiE" # 用户ID
    subject = '纵横四海项目采购项目进度明细预警'
    priority = 20  # 设置优先级为最高
    dueTime = int(time.time() * 1000) + 24 * 60 * 60 * 1000  # 24 hours from now

    dingding_todo = DingDingTodo(app_key, app_secret)
    try:
        task_id = dingding_todo.create_todo(user_id1,user_id2, subject, priority, dueTime)
        print(f"Todo created with task_id: {task_id}")
    except Exception as e:
        print(f"调用待办事项时出错: {e}")
