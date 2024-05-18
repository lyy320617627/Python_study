# -*- coding: utf-8 -*-
import requests
import hashlib
from Sign import get_sign
from decimal import Decimal
import json

class GetDetail:
    def send_get_request(self,authorization,id):
        url = "http://10.217.133.164/apipost/api-request/priceConfirm/detail"
        params = {
            'id': id
            # 添加其他需要的查询参数
        }
        kAppKey = "sino"
        kAppSecret = "SINO@2022"

        headers = {
            'Authorization': authorization,
            'sign': get_sign(params, kAppKey, kAppSecret)
        }

        try:
            response = requests.get(url, params=params, headers=headers)
            if response.status_code == 200:
                print("Response:")
                print(response.json())
            else:
                print(f"Request failed with status code: {response.status_code}")
            return response.json()
        except requests.exceptions.RequestException as e:
            print("Request exception:", e)
    def is_path_present(self,json_str, path):
        try:
            json_obj = json.loads(json_str)
            keys = path.split('.')
            current_obj = json_obj

            for key in keys:
                # 处理数组索引
                if '[' in key and ']' in key:
                    array_key, index_str = key.split('[')
                    index = int(index_str.strip(']'))
                    if isinstance(current_obj.get(array_key), list) and len(current_obj[array_key]) > index:
                        current_obj = current_obj[array_key][index]
                    else:
                        return False
                elif isinstance(current_obj, dict) and key in current_obj:
                    current_obj = current_obj[key]
                else:
                    return False

            return True

        except json.JSONDecodeError:
            return False

    def get_purchaseResultCode(self,response_data):
        if 'code' in response_data and response_data['code'] == 0:
            if 'data' in response_data :
                result = response_data['data']['purchaseResultCode']
                return result
        return None
    def get_prcId(self,response_data):
        if 'code' in response_data and response_data['code'] == 0:
            if 'data' in response_data :
                result = response_data['data']['prcId']
                return result
        return None
    def get_pnrId(self,response_data):
        if 'code' in response_data and response_data['code'] == 0:
            if 'data' in response_data :
                result = response_data['data']['pnrId']
                return result
        return None
    def get_purchaseResultTitle(self,response_data):
        if 'code' in response_data and response_data['code'] == 0:
            if 'data' in response_data :
                result = response_data['data']['purchaseResultTitle']
                return result
        return None
    def get_contractCode(self,response_data):
        if 'code' in response_data and response_data['code'] == 0:
            if 'data' in response_data :
                result = response_data['data']['contractCode']
                return result
        return None
    #去审批列表中去查找申请人的所属部门，如果第一个数组节点的taskGroup包含互联网，则代表互联网。否则就是零售。
    def get_businessType(self,response_data,authorization,log_response):
        if 'code' in response_data and response_data['code'] == 0:
            if 'data' in response_data:
                if self.is_path_present(json.dumps(response_data),"data.priceConfirmBusiEntity.businessType") == True:
                    result = response_data['data']['priceConfirmBusiEntity']['businessType']
                else:
                    result = None
                #businessType节点部分报文可能存在但是是None.
                if result is None:
                    taskGroup = log_response['data'][0]['taskGroup']
                    if "互联网" in taskGroup:
                        result = '互联网中心零售'
                    elif "市场销售部" in taskGroup:
                        result = '供应链服务模式'
                    elif "零售业务部" in taskGroup:
                        result = '传统零售'
                    else:
                        result = 'other'
                return result
        return None
    def get_productList(self,response_data):
        if 'code' in response_data and response_data['code'] == 0:
            if 'data' in response_data :
                productEntityList = response_data['data']['productEntityList']
                # 新列表
                parsed_list = []
                # 遍历原始列表
                for item in productEntityList:
                    # 提取所需字段并添加到新列表中
                    parsed_list.append({
                        "id": item["id"],
                        "priceConfirmLetterId": item["priceConfirmLetterId"],
                        "productCode": item["productCode"],
                        "spuId": item["spuId"],
                        "productName": item["productName"],
                        "brand": item["brand"],
                        "targetProfitRate": item["targetProfitRate"],
                        "estimateProfitRate": item["estimateProfitRate"]
                    })

                # 打印新列表
                for item in parsed_list:
                    print(item)
                return parsed_list
        return None

if __name__ == "__main__":
    # 发送 GET 请求并打印返回结果
    getDetail = GetDetail()
    authorization = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZW5hbnRfaWQiOjQsImNlbnRyYWxfZmxhZyI6Ik4iLCJ1c2VyX25hbWUiOiLog6HngpznlLciLCJyb2xlcyI6W3siYXV0aG9yaXR5IjoiQ0dKQlIifSx7ImF1dGhvcml0eSI6IlBUWUcxMSJ9LHsiYXV0aG9yaXR5IjoiWFQtWkoifSx7ImF1dGhvcml0eSI6IjY4NDgifV0sImNsaWVudF90eXBlIjoiU0giLCJjbGllbnRfaWQiOiJzaW5vLW1hbGwiLCJzY29wZSI6WyJhbGwiXSwiY2F0ZWdvcmllcyI6W3sidGl0bGUiOiLph4fotK0iLCJjb2RlIjoiQ0ctWkoiLCJpbmRleFVyaSI6IumHh-i0rSJ9XSwiY29tcGFueV9zaG9ydF9uYW1lIjoi5rWZIiwiZXhwIjoxNzExMTYwOTM2LCJqdGkiOiIyNDYwOGE4Ni03NmNmLTQxYWYtYmZhNy0zZmE5MmExMTg1MmUiLCJjb21wYW55X2lkIjoxMzM0LCJncm91cF9uYW1lIjoi6YeH6LSt566h55CG5a6kIiwibW9iaWxlIjoiMTU3NTczMDIyODUiLCJ2ZW5kb3JfbmFtZSI6bnVsbCwibGFzdF9jaGFuZ2VfcGFzcyI6MTY4OTU1NjEyNzAwMCwiYXV0aG9yaXRpZXMiOlsiUFRZRzExIiwiQ0dKQlIiLCJYVC1aSiIsIjY4NDgiXSwiY29tcGFueV9sZXZlbCI6IjIiLCJsb2dpbl9uYW1lIjoiaHV3ZWluYW5fWkoiLCJ1c2VyX2lkIjo5NDQ0LCJncm91cF9pZCI6NjM2OSwidmVuZG9yX2lkIjpudWxsLCJjb21wYW55X25hbWUiOiLmtZnmsZ_liIblhazlj7giLCJzZWNvbmRfZGVwdF9pZCI6NjI1NCwic2Vjb25kX2RlcHRfbmFtZSI6IuaUr-aSkeacjeWKoemDqCJ9.dQfAlEbCfYzc4zAHpJJIWkX471ZNInaDNP0mkse6C3klLfvDL_HMgZHiG97xv1ms1YL_b1VG1Wf0lq5SPYoWOVHogbnNGD_4EkD0XUEBYmWEBydXUTjUOr02FCl--cCPFPxFzMQRIHLY8quGga7avYN60RJq5CkGojjdhWuCeWc"
    # id = '2593' #无businessType
    id='2691' #有businessType
    docNum='浙确认函[20240314]06号'
    response = getDetail.send_get_request(authorization,id)
    print('detail:',response)
    # purchaseResultCode = getDetail.get_purchaseResultCode(response)
    # prcId = getDetail.get_prcId(response)
    # pnrId = getDetail.get_pnrId(response)
    # purchaseResultTitle = getDetail.get_purchaseResultTitle(response)
    # contractCode = getDetail.get_contractCode(response)
    # businessType = getDetail.get_businessType(response,authorization,id,docNum)
    # print(purchaseResultCode)
    # print(prcId)
    # print(pnrId)
    # print(purchaseResultTitle)
    # print(contractCode)
    # print(businessType)
    productList = getDetail.get_productList(response)