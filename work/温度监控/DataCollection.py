"""
通过调用接口用来采集大屏各个模板所需要的各个数据
"""
import time

import requests
class DataCollection:
    def __init__(self,username,password):
        self.__username=username
        self.__password=password
        self.base_url="http://www.0531yun.com"
        self.token=self.getToken() #通过用户民和密码来获取后续调用接口所需要的Token值
        self.groupId=self.getGroupList() #获取所在账户所属的分组ID
        self.deviceListDict=self.getDeviceList() # 查询在同一组织下的设备列表，形成的字典，形如：{'力学实验室（温箱）': {'力学实验室（温箱）': 10053452, 'deviceCode': 'c4840d09d58ddeb49250390c9118a2f4'}}
        self.deviceInfoListDict=self.getRealTimeDataByDeviceAddr() #获取所有在线设备的温度和湿度
    # 通过登录名和登录密码来获取Token
    def getToken(self):
        url = f"{self.base_url}/api/getToken"
        params = {
            "loginName": self.__username,
            "password": self.__password
        }
        max_retries = 5  # 最大重试次数
        retries = 0

        while retries < max_retries:
            try:
                response = requests.get(url, params=params)
                print(f"请求状态码: {response.status_code}")  # 打印请求的状态码
                print(f"响应文本: {response.text}")  # 打印响应的内容

                if response.status_code == 200:  # 如果状态码是200，尝试解析JSON
                    try:
                        response_data = response.json()
                        print(f"解析后的JSON响应: {response_data}")
                    except requests.exceptions.JSONDecodeError:
                        raise Exception("解析成JSON失败")

                    if 'code' in response_data:
                        if response_data['code'] == 1000:
                            print(f"获取到的token是:\n{response_data['data']['token']}")
                            return response_data['data']['token']
                        else:
                            raise Exception("获取Token失败: " + response_data.get('message', 'Unknown error'))
                    else:
                        raise Exception("无效的响应体: 'code' 关键字不存在")
                else:
                    raise Exception(f"请求失败，状态码: {response.status_code}, 响应内容: {response.text}")

            except Exception as e:
                retries += 1
                print(f"请求过程中出现错误: {e}，重试 {retries}/{max_retries}")
                if retries < max_retries:
                    time.sleep(20)  # 休息20秒后重试
                else:
                    raise Exception("已达到最大重试次数，获取Token失败")

        return None
    # 根据接口查询分组列表
    def getGroupList(self):
        url=f"{self.base_url}/api/device/getGroupList"
        header={
            "authorization":self.token
        }
        response = requests.get(url, headers=header).json().get('data')[0]
        print(f"获取到的分组id是:\n{response['groupId']}")

    #getDeviceList：通过getDeviceList接口查询设备列表
    def getDeviceList(self):
        url = f"{self.base_url}/api/device/getDeviceList"
        headers = {
            "authorization": self.token
        }
        params = {
            "groupId": self.groupId
        }
        deviceListDict = {}

        try:
            # 发送请求并检查响应
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                response_json = response.json()  # 尝试解析为 JSON
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
            else:
                print(f"请求失败，状态码: {response.status_code}, 响应内容: {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"请求过程中发生异常: {str(e)}")

        return deviceListDict if deviceListDict else None
    # 根据设备地址获取设备继电器列表
    # def getRelayList(self):
    #     url = f"{self.base_url}/api/device/getRelayList"
    #     headers = {
    #         "authorization": self.token
    #     }
    #
    #     for key, values in self.deviceListDict.items():
    #         for name, deviceaddr1 in values.items():
    #
    #             # 将 name 和 deviceaddr1 转换为字符串进行比较
    #             if str(name) != str(deviceaddr1) and name != "deviceCode":
    #                 print(f"设备名称: {name}, 对应的字典数据为: {deviceaddr1}")
    #                 params = {
    #                     "deviceAddr": deviceaddr1
    #                 }
    #
    #                 # 发送请求
    #                 response = requests.get(url, headers=headers, params=params)
    #
    #                 if response.status_code == 200:
    #                     # relay_data = response.json()
    #                     # print(f"设备名称: {name} 的继电器列表为: {relay_data}")
    #                 else:
    #                     print(f"获取设备 {name} 的继电器列表失败，状态码: {response.status_code}")
    # 根据实时数据接口查询到每个设备的实时数据
    def getRealTimeDataByDeviceAddr(self):
        url = f"{self.base_url}/api/data/getRealTimeDataByDeviceAddr"
        headers = {
            "authorization": self.token
        }
        deviceInfoListDict = {}
        for key, values in self.deviceListDict.items():
            for name, deviceaddress in values.items():
                # 将 name 和 deviceaddr1 转换为字符串进行比较
                if str(name) != str(deviceaddress) and name != "deviceCode":
                    print(f"name: {name}, deviceaddr1: {deviceaddress}")
                    params = {
                        "deviceAddrs": str(deviceaddress)
                    }

                    flag=False
                    while(flag==False):
                        response = requests.get(url, headers=headers, params=params)
                        # 检查状态码和响应内容
                        if response.status_code == 200:
                            flag=True
                            print(f"根据设备地址获取实时数据 {url}: {response.text}")
                            try:
                                response_json = response.json()
                                dataList = response_json.get("data")
                                print(f"{str(name)}:{str(deviceaddress)} 的响应数据为: {dataList}")
                                deviceInfoDict = {}
                                for data in dataList:
                                    registDataList = data.get("dataItem")[0]
                                    registDataList=registDataList["registerItem"]
                                    for registData in registDataList:
                                        deviceInfoDict[registData["registerName"]] = str(registData["data"])
                                deviceInfoDict["deviceAddrs"] = str(deviceaddress)
                                deviceInfoListDict[str(name)] = deviceInfoDict
                            except requests.exceptions.JSONDecodeError:
                                print(f"设备 {name} 的响应不是有效的 JSON: {response.text}")
                        else:
                            # print(f"设备:{name}，地址为:{deviceaddress}的设备响应的文本为:{response.text}")
                            time.sleep(10)
        if deviceInfoListDict:
            return deviceInfoListDict
        else:
            return None




if __name__ == '__main__':
    FinaldeviceInfoList ={}
    User=[{
        "username":"h230221zhej",
        "password":"h230221zhej"
    },
        {
        "username":"zhejiang",
        "password":"zhejiang2023"
    }]
    for user in User:
        dataCenter = DataCollection(user["username"],user["password"])
        dataCenter.getDeviceList()
        dataCenter.getRealTimeDataByDeviceAddr()
        deviceInfoList = dataCenter.deviceInfoListDict
        if deviceInfoList:
            for key,values in deviceInfoList.items():
                print(f"{key}:{values}")
                FinaldeviceInfoList[key]=values
    print(f"最终的数据为:\n")
    for key,values in FinaldeviceInfoList.items():
        print(f"{key}:{values}")
