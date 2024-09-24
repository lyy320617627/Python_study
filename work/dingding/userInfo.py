import requests


def get_user_info(app_key, app_secret, userid):
    """
    通过钉钉接口获取用户个人信息。

    :param app_key: 钉钉应用的 appKey
    :param app_secret: 钉钉应用的 appSecret
    :param userid: 用户的 userid
    :return: 用户的个人信息
    :raises Exception: 当获取 access_token 或 用户信息失败时抛出异常
    """

    def get_access_token():
        """
        获取钉钉的 access_token。

        :return: access_token
        :raises Exception: 当获取 access_token 失败时抛出异常
        """
        url = 'https://oapi.dingtalk.com/gettoken'
        params = {
            'appkey': app_key,
            'appsecret': app_secret
        }
        response = requests.get(url, params=params)
        response_data = response.json()

        if response_data.get('errcode') == 0:
            return response_data.get('access_token')
        else:
            raise Exception(f"获取 access_token 失败: {response_data.get('errmsg')}")

    def fetch_user_info(access_token, userid):
        """
        获取用户个人信息。

        :param access_token: 钉钉的 access_token
        :param userid: 用户的 userid
        :return: 用户的个人信息
        :raises Exception: 当获取用户信息失败时抛出异常
        """
        url = 'https://oapi.dingtalk.com/user/get'
        params = {
            'access_token': access_token,
            'userid': userid
        }
        response = requests.get(url, params=params)
        response_data = response.json()

        if response_data.get('errcode') == 0:
            return response_data
        else:
            raise Exception(f"获取用户信息失败: {response_data.get('errmsg')}")

    try:
        # 获取 access_token
        access_token = get_access_token()

        # 获取用户个人信息
        user_info = fetch_user_info(access_token, userid)
        return user_info

    except Exception as e:
        print(f"发生错误: {e}")

import requests

def get_user_info_by_userid(access_token, userid):
    url = "https://oapi.dingtalk.com/topapi/v2/user/get"
    params = {
        "access_token": access_token
    }
    data = {
        "userid": userid
    }
    response = requests.post(url, params=params, json=data)
    response_data = response.json()
    print(f"完整响应数据: {response_data}")  # 打印完整的响应数据
    if response_data["errcode"] == 0:
        user_info = response_data.get("result")
        print(f"用户信息: {user_info}")
        return user_info
    else:
        raise Exception(f"Error getting user info: {response_data}")

def get_access_token(app_key, app_secret):
    url = "https://oapi.dingtalk.com/gettoken"
    params = {
        "appkey": app_key,
        "appsecret": app_secret
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

# 示例使用
if __name__ == '__main__':
    app_key = 'dingc8wtmaib95vi3ifz'      # 替换为实际的 appKey
    app_secret = 'XR4vKpX7Wt4iLK2WE-1IbI_THLwaynDYC6Be0j0j9Fl3e_ev39P9WRu_Fin4GhFt' # 替换为实际的 appSecret
    userid = "01265144302040198391"  # 替换为实际的 userId

    access_token = get_access_token(app_key, app_secret)
    user_info = get_user_info_by_userid(access_token, userid)
    print(f"用户信息: {user_info}")
#
# # 示例使用
# if __name__ == '__main__':
#     app_key = 'dingc8wtmaib95vi3ifz'  # 替换为实际的 appKey
#     app_secret = 'XR4vKpX7Wt4iLK2WE-1IbI_THLwaynDYC6Be0j0j9Fl3e_ev39P9WRu_Fin4GhFt'  # 替换为实际的 appSecret
#     userid = '01265144302040198391'  # 替换为实际的用户 ID
#
#     user_info = get_user_info(app_key, app_secret, userid)
#     if user_info:
#         print(f"用户信息: {user_info}")
