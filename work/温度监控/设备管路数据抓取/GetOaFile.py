import requests
from datetime import datetime
import math

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
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
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
            "appType": "APP_SUB13RIZ6QXPXG4ZXUWI",
            "systemToken": "9CC66GD1FYGO2Z1X8WY7U6NG8XNO34BS54W0MT",
            "userId": "500159250026261710",
            "formUuid": "FORM-70816AA0614241E89D08EFAC23F40CE3RS8L"
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
        url = "https://api.dingtalk.com/v1.0/yida/forms/formFields"
        headers = {
            "x-acs-dingtalk-access-token": self.__access_token,
            "Content-Type": "application/json"
        }
        params = {
            "appType": "APP_SUB13RIZ6QXPXG4ZXUWI",
            "systemToken": "9CC66GD1FYGO2Z1X8WY7U6NG8XNO34BS54W0MT",
            "formUuid": "FORM-70816AA0614241E89D08EFAC23F40CE3RS8L",
            "userId": "500159250026261710"
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            labelList = response.json().get("result", [])
            for label in labelList:
                self.labelDict[label["label"]["zh_CN"]] = label["fieldId"]
            print(f"标签字典: {self.labelDict}")
        else:
            print(f"请求失败，状态码: {response.status_code}，错误信息: {response.text}")

    def parse_timestamp(self, timestamp):
        """
        尝试解析时间字符串，支持秒和不含秒的格式。

        :param timestamp: 时间字符串，格式为 "YYYY-MM-DDTHH:MM:SSZ" 或 "YYYY-MM-DDTHH:MMZ"
        :return: datetime 对象
        """
        try:
            return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            return datetime.strptime(timestamp, '%Y-%m-%dT%H:%MZ')

    def getDetailData(self):
        """
        获取详细实例数据并筛选符合当月政策的数据。
        """
        url = "https://api.dingtalk.com/v1.0/yida/forms/instances/advances/query"
        headers = {
            "Content-Type": "application/json",
            "x-acs-dingtalk-access-token": self.__access_token
        }
        for index in range(self.totalPageNum + 1):
            params = {
                "pageNumber": index + 1,
                "formUuid": "FORM-70816AA0614241E89D08EFAC23F40CE3RS8L",
                "systemToken": "9CC66GD1FYGO2Z1X8WY7U6NG8XNO34BS54W0MT",
                "pageSize": 100,
                "userId": "500159250026261710",
                "appType": "APP_SUB13RIZ6QXPXG4ZXUWI"
            }
            response = requests.post(url, headers=headers, json=params)
            if response.status_code == 200:
                maxTime = None
                dataList = response.json().get("data", [])
                for data in dataList:
                    timestamp = data.get("createTimeGMT")
                    if timestamp:
                        timestamp_dt = self.parse_timestamp(timestamp)
                        if not maxTime or timestamp_dt > maxTime:
                            maxTime = timestamp_dt

                for data in dataList:
                    formData = data.get("formData", {})
                    createTime = data.get("createTimeGMT")
                    if createTime:
                        createTime_dt = self.parse_timestamp(createTime)
                        if createTime_dt == maxTime:
                            tempData = [
                                formData.get(self.labelDict.get("设备名称")),
                                formData.get(self.labelDict.get("资产编号")),
                                formData.get(self.labelDict.get("使用情况")),
                                formData.get(self.labelDict.get("下一次维护")),
                                formData.get(self.labelDict.get("下一次校准")),
                                formData.get(self.labelDict.get("是否重点设备"))
                            ]
                            self.finalyDataList.append(tempData)
                print(f"最终数据: {self.finalyDataList}")
                print(f"最终数据的长度: {len(self.finalyDataList)}")
            else:
                try:
                    error_msg = response.json()
                except ValueError:
                    error_msg = response.text
                print(f"请求失败，状态码: {response.status_code}，错误信息: {error_msg}")

if __name__ == '__main__':
    getfile = GetFile()
    getfile.getInstanceCount()
    getfile.get_form_fields()
    getfile.getDetailData()
    print(f"最终数据为：{len(getfile.finalyDataList)}")
    # getfile.dataUpLoad()  # 根据实际需要上传数据
