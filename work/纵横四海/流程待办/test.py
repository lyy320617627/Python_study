import requests


# 通过手机号获取钉钉用户的userid
def get_Userid_by_mobile(access_token, mobile):
    url = "https://oapi.dingtalk.com/topapi/v2/user/getbymobile"
    params = {
        "access_token": access_token
    }
    data = {
        "mobile": mobile
    }
    response = requests.post(url, params=params, json=data)
    response_data = response.json()
    print(f"完整响应数据: {response_data}")  # 打印完整的响应数据
    if response_data["errcode"] == 0:
        print(f"{mobile} 对应的相应的json数据中对应的userid为:{response_data['result']['userid']}")
        return response_data["result"]["userid"]
    else:
        raise Exception(f"Error getting userid by mobile: {response_data}")


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
    app_key = 'dingc8wtmaib95vi3ifz'  # 替换为实际的 appKey
    app_secret = 'XR4vKpX7Wt4iLK2WE-1IbI_THLwaynDYC6Be0j0j9Fl3e_ev39P9WRu_Fin4GhFt'  # 替换为实际的 appSecret
    mobile = "15168430601"

    access_token = get_access_token(app_key, app_secret)
    userid = get_Userid_by_mobile(access_token, mobile)
    print(f"用户ID: {userid}")
