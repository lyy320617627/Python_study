import requests
from UserId import get_access_token,get_Userid_by_mobile
class DingDingAPI:
    def __init__(self, app_key, app_secret):
        self.app_key = app_key
        self.app_secret = app_secret
        self.access_token = self.get_access_token()

    def get_access_token(self):
        url = "https://oapi.dingtalk.com/gettoken"
        params = {
            "appkey": self.app_key,
            "appsecret": self.app_secret
        }
        response = requests.get(url, params=params)
        result = response.json()
        if result.get("errcode") == 0:
            return result.get("access_token")
        else:
            raise Exception(f"Error getting access token: {result.get('errmsg')}")

    def get_user_info(self, userid):
        url = f"https://oapi.dingtalk.com/topapi/v2/user/get"
        params = {
            "access_token": self.access_token
        }
        data = {
            "userid": userid
        }
        response = requests.post(url, params=params, json=data)
        result = response.json()
        if result.get("errcode") == 0:
            return result.get("result")
        else:
            raise Exception(f"Error getting user info: {result.get('errmsg')}")


# Example usage
app_key = 'dingc8wtmaib95vi3ifz'
app_secret = 'XR4vKpX7Wt4iLK2WE-1IbI_THLwaynDYC6Be0j0j9Fl3e_ev39P9WRu_Fin4GhFt'
userid = '500159250026261710'

dingding_api = DingDingAPI(app_key, app_secret)
user_info = dingding_api.get_user_info(userid)
unionid = user_info.get('unionid')
print(f"UnionID: {unionid}")
# if __name__ == '__main__':
#     app_key = 'dingc8wtmaib95vi3ifz'
#     app_secret = 'XR4vKpX7Wt4iLK2WE-1IbI_THLwaynDYC6Be0j0j9Fl3e_ev39P9WRu_Fin4GhFt'
#     dingding_api = DingDingAPI(app_key, app_secret)
#     target_list=[['楼洲阳', '18857151059', '222463682626855869'], ['张颖佳', '15088712572', '06221849'], ['沈洁', '13868175885', '06221034'], ['吴凡', '15068153341', '2341372361689197'], ['关世红', '15967149266', '283225323420689919'], ['申懿', '18868134005', '016366145504955180'], ['张兵', '13732286893', '06220007'], ['黄诗琪', '15168430601', '01265144302040198391'], ['徐芳丽', '15967122788', '06221021'], ['胡炜男', '15757302285', '183752583632629948'], ['唐亚贤', '15968197473', '01221155340521586650'], ['孔佳佳', '13858119470', '06220111'], ['来君', '13858100169', '06220005'], ['徐化成', '18458106029', '294667564624194378'], ['蔡建光', '18805711711', '06220006'], ['张洪', '18758182552', '06220107']]
#     for data in target_list:
#         userid=data[2]
#         user_info=dingding_api.get_user_info(userid)
#         unionid=user_info.get('unionid')
#         data.append(unionid)
#     print(target_list)