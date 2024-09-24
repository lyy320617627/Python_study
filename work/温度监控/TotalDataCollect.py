""""
通过调用不同的接口返回的数据进行汇总，现进行接口的替换和测试
"""
import requests
class TotalDataCollect:
    def __init__(self,username,password):
        self.__username=username,
        self.__password=password,
        self.base_url = "http://www.0531yun.com"
        self.Token=self.getToken()
        self.GroupIdList=self.getGroupList()
    # 现在换用接口，进行不同数据的汇总
    def getToken(self):
        url = f"{self.base_url}/api/getToken"
        params = {
            "loginName": self.__username,
            "password": self.__password
        }
        response = requests.get(url, params=params)
        try:
            response_data = response.json()
        except requests.exceptions.JSONDecodeError:
            raise Exception("解析成JSON失败")

        if 'code' in response_data:
            if response_data['code'] == 1000:
                # print(f"获取到的token是:\n{response_data['data']['token']}")
                return response_data['data']['token']
            else:
                raise Exception("获取Token失败: " + response_data.get('message', 'Unknown error'))
        else:
            raise Exception("无效的响应体: 'code' 关键字不存在")
    #查询分组列表
    def getGroupList(self):
        url = f"{self.base_url}/api/device/getGroupList"
        header = {
            "authorization": self.Token
        }
        response = requests.get(url, headers=header).json().get('data')
        # response = requests.get(url, headers=header)
        print(f"获取到的响应体为:{response}")
        groupIdList=[]
        for data in response:
            groupIdList.append(data["groupId"])
        print(f"在添加完groupId之后的GroupIdList为:{groupIdList}")
        if len(groupIdList)>0:
            return groupIdList
        else:
            return None
        # print(f"获取到的分组id是:\n{response['groupId']}")
    # 根据分组Id查询设备列表
    def getDeviceList(self):
        url = f"{self.base_url}/api/device/getDeviceList"
        if self.GroupIdList:
            for groupId in self.GroupIdList:
                headers = {
                    "authorization": self.Token
                }
                params = {
                    "groupId": "820e2befa4784aedae6069a5b6e5281d"
                }
                deviceListDict = {}
                try:
                    # 发送请求并检查响应
                    response = requests.get(url, headers=headers, params=params)
                    if response.status_code == 200:
                        try:
                            response_json = response.json()
                            print(f"response_json:{response_json}")
                            dataList = response_json.get("data")
                            if dataList is not None:
                                for data in dataList:
                                    deviceDict = {}
                                    deviceDict[data["deviceName"]] = data["deviceAddr"]
                                    deviceDict["deviceCode"] = data["deviceCode"]
                                    deviceListDict[data["deviceName"]] = deviceDict
                                print(f"deviceListDict: {deviceListDict}")
                                print(f"查询到的设备列表中的所有设备长度为: {len(dataList)}")
                            else:
                                print("响应数据中不包含 'data' 字段")
                        except requests.exceptions.JSONDecodeError:
                            print(f"响应不是有效的 JSON: {response.text}")
                    else:
                        print(f"请求失败，状态码: {response.status_code}, 响应内容: {response.text}")

                except requests.exceptions.RequestException as e:
                    print(f"请求过程中发生异常: {str(e)}")

        # return deviceListDict if deviceListDict else None



if __name__ == '__main__':
    username="h230221zhej"
    password="h230221zhej"
    # username="zhejiang"
    # password="zhejiang2023"
    totalDataCollect=TotalDataCollect(username,password)
    totalDataCollect.getToken()
    totalDataCollect.getGroupList()
    totalDataCollect.getDeviceList()
