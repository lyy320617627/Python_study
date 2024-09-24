import json
import time

import requests
from datetime import datetime, timedelta
class HeDongli:
    def GetJessionID(self):
        # 获取网页的会话id

    def GetTime(self):
        # 获取当前日期时间
        today = datetime.now()

        # 计算一个月之前的日期时间
        one_month_ago = today - timedelta(days=30)

        # 将日期时间格式化为所需的字符串类型
        today_str = today.strftime('%Y-%m-%d 23:59:59')
        one_month_ago_str = one_month_ago.strftime('%Y-%m-%d 00:00:00')

        print("今天的日期时间（格式化）：", today_str)
        print("一个月之前的日期时间（格式化）：", one_month_ago_str)
        return today_str,one_month_ago_str
    def HeDongliPostRequest(self,Authorization,Cookie,Token):
        url="http://admin.hedongli.com/hdlmgmtcomp/order/orderHandle/v1.0/pageOrderHandle"
        headers={
            "Content-Type":"application/json",
            "Authorization":Authorization,
            "Cookie":Cookie,
            "Host":"admin.hedongli.com",
            "Origin":"http://admin.hedongli.com",
            "Referer":"http://admin.hedongli.com/",
            "Token":Token,
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Accept":"application/json, text/plain, */*"
        }
        startTime=self.GetTime()[1]
        endTime=self.GetTime()[0]
        data={
            {"deliverState": 114,
             "orderState": 3,
             "dealerProvinceId": 330000,
             "mch": "浙江终端公司",
             "endTime": endTime,
             "startTime": startTime,
             "mchtId": 10781,
             "userInfo":
                 {
                     "cityId": "-1",
                     "id": 0,
                     "mchtId": 10781,
                     "mchtName": "浙江终端公司",
                     "mchtType": 1, "opId": 30838,
                     "provinceId": -1,
                     "regionId": 330000,
                     "username": "王逸洁"

                 }, "dealerNameList": [],
             "dealerName": "",
             "page":
                 {
                     "pageNum": 1,
                     "pageSize": 100

                 },
             "lctnProvinceId":
                 "330000"

             }
        }
        data = json.dumps(data)
        try:
            response = requests.post(url, headers=headers, data=data, timeout=30)
            response_json = response.json()
            print(response_json)
            data_list=json.loads(response_json)

        except:
            time.sleep(3)
            response = requests.post(url, headers=headers, data=data, timeout=30)
            response_json = response.json()
            data_list = json.loads(response_json)













if __name__ == '__main__':
    hdl=HeDongli()
    hdl.GetTime()
