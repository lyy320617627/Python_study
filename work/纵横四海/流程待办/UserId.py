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
        print(f"{mobile} 对应的相应的json数据中对应的userid为:{response_data["result"]["userid"]}")
        return response_data["result"]["userid"]
    else:
        raise Exception(f"Error getting unionid by mobile: {response_data}")
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
mobile="15168430601"
access_token="4e8dd77a6936357d84ad47aee645516b"
userid=get_Userid_by_mobile(access_token, mobile)
# if __name__ == '__main__':
#     # target_list=[["楼洲阳","18857151059"],["张颖佳","15088712572"],["沈洁","13868175885"],["吴凡","15068153341"],["关世红","15967149266"],["申懿","18868134005"],["张兵","13732286893"],["黄诗琪","15168430601"],["徐芳丽","15967122788"],["胡炜男","15757302285"],
#     #              ["唐亚贤","15968197473"],["孔佳佳","13858119470"],["来君","13858100169"],["徐化成","18458106029"],["蔡建光","18805711711"],["张洪","18758182552"]
#     #              ]
#     # for data in target_list:
#     #     mobile=data[1]
#     #     userId=get_Userid_by_mobile(access_token,mobile)
#     #     data.append(userId)
#     # print(target_list)
