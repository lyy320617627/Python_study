import requests
from datetime import datetime
import math
from MySQLUtil import MySQLUtil

class GetFile:
    def __init__(self):
        self.__access_token = self.getAccessToken()
        self.labelDict = {}
        self.totalPageNum = 0
        self.finalyDataList = []

    def check_year_month(self, time_str):
        """
        检查给定的时间字符串是否与当前的年份和月份相同。

        :param time_str: 时间字符串，格式为 "YYYY-MM-DD HH:MM:SS"
        :return: bool，返回给定时间的年份和月份是否与当前时间的年份和月份相等。
        """
        time_obj = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        current_year = datetime.now().year
        current_month = datetime.now().month
        return time_obj.year == current_year and time_obj.month == current_month

    def getAccessToken(self):
        """
        获取钉钉 API 的 access_token。

        :return: str，返回获取到的 access_token。
        """
        appkey = 'dingc8wtmaib95vi3ifz'
        appsecret = 'XR4vKpX7Wt4iLK2WE-1IbI_THLwaynDYC6Be0j0j9Fl3e_ev39P9WRu_Fin4GhFt'
        url = f'https://oapi.dingtalk.com/gettoken?appkey={appkey}&appsecret={appsecret}'
        headers = {
            'Content-Type': "application/x-www-form-urlencoded"
        }
        response = requests.get(url, headers=headers)
        access_token = response.json().get("access_token")
        if access_token:
            print(f"获取到的 access_token 为: {access_token}")
            return access_token
        else:
            raise Exception(f"获取 access_token 失败: {response.json()}")

    def getInstanceCount(self):
        """
        获取流程实例的总数并计算页数。
        """
        url = "https://api.dingtalk.com/v1.0/yida/processes/instances?pageNumber=1&pageSize=100"
        headers = {
            "x-acs-dingtalk-access-token": self.__access_token,
            "Content-Type": "application/json"
        }
        data = {
            "appType": "APP_LXV15EUL0I74JEIJZB1B",
            "systemToken": "G0A66Z81CN1OA7Y99GCK29WCRNWD2JKNJSA0MOI1",
            "userId": "500159250026261710",
            "formUuid": "FORM-00B12B9EF687446592A4A0F689BD11ACXBQK",
        }
        response = requests.post(url=url, headers=headers, json=data)
        if response.status_code == 200:
            totalCount = response.json().get("totalCount")
            self.totalPageNum = math.ceil(totalCount / 100)
            print(f"实例总数: {totalCount}, 页数: {self.totalPageNum}")
        else:
            print(f"请求失败，状态码: {response.status_code}，错误信息: {response.json()}")

    def get_form_fields(self):
        """
        获取表单字段并存储到字典中。
        """
        base_url = "https://api.dingtalk.com/v1.0/yida/forms/formFields"
        headers = {
            "x-acs-dingtalk-access-token": self.__access_token,
            "Content-Type": "application/json"
        }
        params = {
            "appType": "APP_LXV15EUL0I74JEIJZB1B",
            "systemToken": "G0A66Z81CN1OA7Y99GCK29WCRNWD2JKNJSA0MOI1",
            "formUuid": "FORM-00B12B9EF687446592A4A0F689BD11ACXBQK",
            "userId": "500159250026261710"
        }
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code == 200:
            labelList = response.json().get("result", [])
            for label in labelList:
                self.labelDict[label["label"]["zh_CN"]] = label["fieldId"]
            print(f"标签字典: {self.labelDict}")
        else:
            print(f"Error: {response.status_code}, {response.text}")

    def getDetailData(self):
        """
        获取详细实例数据并筛选符合当月政策的数据。
        """
        url = "https://api.dingtalk.com/v1.0/yida/forms/instances/advances/query"
        headers = {
            "Content-Type": "application/json",
            "x-acs-dingtalk-access-token": self.__access_token
        }
        for index in range(self.totalPageNum+1):
            params = {
                "pageNumber": index+1,
                "formUuid": "FORM-00B12B9EF687446592A4A0F689BD11ACXBQK",
                "systemToken": "G0A66Z81CN1OA7Y99GCK29WCRNWD2JKNJSA0MOI1",
                "pageSize": 100,
                "userId": "500159250026261710",
                "appType": "APP_LXV15EUL0I74JEIJZB1B"
            }
            response = requests.post(url, headers=headers, json=params)
            if response.status_code == 200:
                dataList = response.json().get("data", [])
                for data in dataList:
                    formData = data.get("formData", {})
                    policyTime = formData.get(self.labelDict.get("政策时间"))
                    if policyTime and self.check_year_month(str(policyTime)):
                        tempData = [
                            formData.get(self.labelDict.get("政策时间")),
                            formData.get(self.labelDict.get("品牌")),
                            formData.get(self.labelDict.get("通路类型")),
                            formData.get(self.labelDict.get("地市侧")),
                            formData.get(self.labelDict.get("返利类型")),
                            formData.get(self.labelDict.get("政策起始日期")),
                            formData.get(self.labelDict.get("政策截止日期")),
                            formData.get(self.labelDict.get("物料编码")),
                            formData.get(self.labelDict.get("机型系列")),
                            # formData.get(self.labelDict.get("产品俗称")),
                            formData.get(self.labelDict.get("预估数量")),
                            formData.get(self.labelDict.get("返利金额")),
                            formData.get(self.labelDict.get("商品名称"))
                        ]
                        self.finalyDataList.append(tempData)
                print(f"最终数据: {self.finalyDataList}")
                print(f"最终数据的长度: {len(self.finalyDataList)}")
            else:
                print(f"请求失败，状态码: {response.status_code}，错误信息: {response.json()}")
    def dataUpLoad(self):
        if self.finalyDataList:
            conn2 = MySQLUtil(host="192.168.0.148",port=3306, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
            keyList=keyList = [
                "policy_time", "brand", "channel_type", "city_side", "rebate_type",
                "policy_start_date", "policy_end_date", "material_code", "model_series",
                 "estimated_quantity", "rebate_amount","product_name"
            ]

            conn2.batchInsert("policy_data",keyList,self.finalyDataList)


if __name__ == '__main__':
    getfile = GetFile()
    getfile.getInstanceCount()
    getfile.get_form_fields()
    getfile.getDetailData()
    print(f"最总数据为：{len(getfile.finalyDataList)}")
    getfile.dataUpLoad()
