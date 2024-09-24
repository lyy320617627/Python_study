import requests
import json

class DingDingAPI:
    def __init__(self, app_key, app_secret):
        self.app_key = app_key
        self.app_secret = app_secret
        self.base_url = "https://oapi.dingtalk.com"
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

    def get_all_users(self):
        url = f"https://oapi.dingtalk.com/topapi/v2/user/list"
        params = {
            "access_token": self.access_token  # 将 access_token 作为 query 参数传递
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "dept_id": 1,  # 正确的部门ID参数名称应该是 department_id
            "size": 100,
            "cursor": 0  # 初始 cursor 设为 0
        }
        print(f"请求URL: {url}")  # 调试信息
        print(f"请求头: {headers}")  # 调试信息
        print(f"请求数据: {json.dumps(data, indent=4)}")  # 调试信息

        response = requests.post(url, headers=headers, params=params, json=data)
        result = response.json()
        print(f"响应数据: {json.dumps(result, indent=4)}")  # 调试信息
        if result.get("errcode") == 0:
            return result.get("result").get("list")
        else:
            raise Exception(f"Error getting user list: {result.get('errmsg')}")

    def get_user_id_by_name(self, name):
        users = self.get_all_users()
        for user in users:
            if user.get("name") == name:
                return user.get("userid")
        raise Exception(f"User with name {name} not found")

    def get_user_details(self, user_id):
        url = f"https://oapi.dingtalk.com/topapi/v2/user/get"
        params = {
            "access_token": self.access_token  # 将 access_token 作为 query 参数传递
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "userid": user_id
        }
        response = requests.post(url, headers=headers, params=params, json=data)
        result = response.json()
        if result.get("errcode") == 0:
            return result.get("result")
        else:
            raise Exception(f"Error getting user details: {result.get('errmsg')}")

if __name__ == '__main__':
    app_key = 'dingc8wtmaib95vi3ifz'
    app_secret = 'XR4vKpX7Wt4iLK2WE-1IbI_THLwaynDYC6Be0j0j9Fl3e_ev39P9WRu_Fin4GhFt'
    name = '张洪'

    dingding_api = DingDingAPI(app_key, app_secret)
    try:
        user_id = dingding_api.get_user_id_by_name(name)
        user_details = dingding_api.get_user_details(user_id)
        print(f"User details: {user_details}")
    except Exception as e:
        print(f"调用获取用户详情时出错: {e}")
