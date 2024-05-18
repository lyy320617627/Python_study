import requests
import json
from datetime import datetime, timedelta
import re

class GetInfos:


    def send_post_request(self,authorization,pageNo):
        url = "http://10.217.133.164/apipost/api-request/priceConfirm/getAll"
        payload = {
            "confirmCode": "",
            "applyDateStr": None,
            "applyDateEnd": None,
            "status": None,
            "productName": "",
            "vendorName": "",
            "current": pageNo,
            "size": 10
        }

        headers = {
            "Content-Type": "application/json",
            "authorization": authorization
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                result_list = self.parse_records(response.json())
                # print("Response:")
                # print(result_list)
                return result_list

            else:
                print(f"Request failed with status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print("Request exception:", e)

    def timestampToStr(self,timestampNum):
        timestamp = timestampNum / 1000  # 转换为秒
        # 将时间戳转换为 datetime 对象
        dt_object = datetime.fromtimestamp(timestamp)
        # 将 datetime 对象转换为字符串
        date_string = dt_object.strftime("%Y-%m-%d %H:%M:%S")
        return date_string

    def parse_records(self,response_data):
        result_list = []
        if 'code' in response_data and response_data['code'] == 0:
            if 'data' in response_data and 'records' in response_data['data']:
                records = response_data['data']['records']

                for record in records:
                    result = [
                        record.get('id'),
                        record.get('confirmTitle'),
                        record.get('vendorId'),
                        record.get('vendorName'),
                        record.get('confirmCode'),
                        record.get('applyCompanyId'),
                        record.get('applyCompanyName'),
                        self.timestampToStr(record.get('applyDate')),
                        record.get('applyUserId'),
                        record.get('applyUserName'),
                        record.get('status'),
                        self.timestampToStr(record.get('quoteDate')),
                        self.timestampToStr(record.get('createDate')),
                        record.get('productNameStr'),
                        record.get('sumTargetPurchaseQuantity'),
                        record.get('sumTargetPurchaseAmount'),
                        None, #purchaseResultCode 详情页获取
                        None, #prcId 详情页获取
                        None, #pnrId 详情页获取
                        None, #purchaseResultTitle 详情页获取
                        None, #contractCode  详情页获取
                        None, #businessType  详情页获取
                        None #审批完成时间  详情页获取
                    ]
                    result_list.append(result)
        else:
            raise ValueError("Error in response data. Code is not 0.")

        return result_list


if __name__ == "__main__":
    # 发送 POST 请求并打印返回结果
    authorization = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZW5hbnRfaWQiOjQsImNlbnRyYWxfZmxhZyI6Ik4iLCJ1c2VyX25hbWUiOiLog6HngpznlLciLCJyb2xlcyI6W3siYXV0aG9yaXR5IjoiQ0dKQlIifSx7ImF1dGhvcml0eSI6IlBUWUcxMSJ9LHsiYXV0aG9yaXR5IjoiWFQtWkoifSx7ImF1dGhvcml0eSI6IjY4NDgifV0sImNsaWVudF90eXBlIjoiU0giLCJjbGllbnRfaWQiOiJzaW5vLW1hbGwiLCJzY29wZSI6WyJhbGwiXSwiY2F0ZWdvcmllcyI6W3sidGl0bGUiOiLph4fotK0iLCJjb2RlIjoiQ0ctWkoiLCJpbmRleFVyaSI6IumHh-i0rSJ9XSwiY29tcGFueV9zaG9ydF9uYW1lIjoi5rWZIiwiZXhwIjoxNzA2NzU4NTg5LCJqdGkiOiJjNTRiMDY5OS1iOGQ2LTRkNzYtODU1Yy1iYmU1MTE4NjQxYzkiLCJjb21wYW55X2lkIjoxMzM0LCJncm91cF9uYW1lIjoi6YeH6LSt566h55CG5a6kIiwibW9iaWxlIjoiMTU3NTczMDIyODUiLCJ2ZW5kb3JfbmFtZSI6bnVsbCwibGFzdF9jaGFuZ2VfcGFzcyI6MTY4OTU1NjEyNzAwMCwiYXV0aG9yaXRpZXMiOlsiUFRZRzExIiwiQ0dKQlIiLCJYVC1aSiIsIjY4NDgiXSwiY29tcGFueV9sZXZlbCI6IjIiLCJsb2dpbl9uYW1lIjoiaHV3ZWluYW5fWkoiLCJ1c2VyX2lkIjo5NDQ0LCJncm91cF9pZCI6NjM2OSwidmVuZG9yX2lkIjpudWxsLCJjb21wYW55X25hbWUiOiLmtZnmsZ_liIblhazlj7giLCJzZWNvbmRfZGVwdF9pZCI6NjI1NCwic2Vjb25kX2RlcHRfbmFtZSI6IuaUr-aSkeacjeWKoemDqCJ9.FpRk6O3jLyypee9kOD5MPZsNzuY-1ipxTtNXjWDhKO4GKHFrzU2KiDPoSdqII5sJlwmdqQT08Z0PwG4mR-MBWwKdBXKve9Ay9cwwQw9yIHF1by2C1rX3dAXV2-wQLQj2ICdF3v7gm_UoJiQTrUIHncXnW1CGrOzIJmiq8-gvCIg"
    result_list = []
    #取10页。
    getResultBillInfos = GetInfos()
    for num in range(1,2):
        list = getResultBillInfos.send_post_request(authorization,num)
        result_list.extend(list)
    for record in result_list:
        print(record)

