import time

import requests


class EnvMonitoringPlatform:
    def __init__(self, base_url, login_name, password):
        self.base_url = base_url
        self.token = self.get_token(login_name, password)

    #获取请求Token
    def get_token(self, login_name, password):
        url = f"{self.base_url}/api/getToken"
        params = {
            "loginName": login_name,
            "password": password
        }
        response = requests.get(url, params=params)
        print(f"Response from {url}: {response.text}")
        try:
            response_data = response.json()
        except requests.exceptions.JSONDecodeError:
            raise Exception("Failed to parse response as JSON")

        if 'code' in response_data:
            if response_data['code'] == 1000:
                return response_data['data']['token']
            else:
                raise Exception("Failed to get token: " + response_data.get('message', 'Unknown error'))
        else:
            raise Exception("Invalid response format: 'code' key not found")

    def get_headers(self):
        return {
            "authorization": self.token
        }

    def check_response(self, response):
        if response.status_code != 200:
            print(f"Response status code: {response.status_code}")
            print(f"Response text: {response.text}")
            if response.status_code == 404:
                return {"error": "Endpoint not found"}
            raise Exception(f"Request failed with status code {response.status_code}")
        if not response.text:
            raise Exception("Empty response")
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            raise Exception("Failed to parse response as JSON")

    #查询分组列表
    def get_group_list(self):
        url = f"{self.base_url}/api/device/getGroupList"
        headers = self.get_headers()
        response = requests.get(url, headers=headers)
        print(f"获取分组列表{url}: {response.text}")
        return self.check_response(response)
    #获取设备列表
    def get_device_list(self, group_id=None):
        url = f"{self.base_url}/api/device/getDeviceList"
        headers = self.get_headers()
        params = {}
        if group_id:
            params['groupId'] = group_id
        response = requests.get(url, headers=headers, params=params)
        print(f"获取设备列表:{url}: {response.text}")
        return self.check_response(response)


    #根据设备地址查询设备信息
    def get_device_info(self, device_addr):
        url = f"{self.base_url}/api/device/getDevice"
        headers = self.get_headers()
        params = {
            "deviceAddr": device_addr
        }
        response = requests.get(url, headers=headers, params=params)
        print(f"根据设备地址查询设备信息{url}: {response.text}")
        return self.check_response(response)

    # 根据设备地址获取设备继电器列表
    def get_device_relay_list(self, device_addr):
        url = f"{self.base_url}/api/device/getDeviceRelayList"
        headers = self.get_headers()
        params = {
            "deviceAddr": 10053452
        }
        response = requests.get(url, headers=headers, params=params)
        print(f"根据设备地址获取设备继电器列表 {url}: {response.text}")
        if response.status_code == 404:
            print(f"URL not found: {url}")
            return {"error": "Endpoint not found"}
        return self.check_response(response)

    def relay_operation(self, device_addr, relay_id, operation):
        url = f"{self.base_url}/api/device/setRelay"
        headers = self.get_headers()
        payload = {
            "deviceAddr": device_addr,
            "relayId": relay_id,
            "operation": operation
        }
        response = requests.post(url, headers=headers, json=payload)
        print(f"Response from {url}: {response.text}")
        return self.check_response(response)

    def get_realtime_data(self):
        url = f"{self.base_url}/api/data/getRealtimeData"
        headers = self.get_headers()
        params={
            'groupId':""
        }
        response = requests.get(url, headers=headers, params=params)
        print(f"查询所有设备的实时数据 {url}: {response.text}")
        if response.status_code == 404:
            print(f"URL not found: {url}")
            return {"error": "Endpoint not found"}
        return self.check_response(response)


    #获取历史数据列表
    def get_history_data(self, device_addr):
        url = f"{self.base_url}/api/data/historyList"
        headers = self.get_headers()
        params = {
            "deviceAddr": device_addr,
            "nodeId":-1,
            "startTime":"2024-07-31 14:25:00",
            "endTime":"2024-07-31 15:27:00"

        }
        response = requests.get(url, headers=headers, params=params)
        print(f"查询历史数据列表{url}: {response.text}")
        if response.status_code == 404:
            print(f"URL not found: {url}")
            return {"error": "Endpoint not found"}
        return self.check_response(response)

    # 查询继电器操作记录
    def get_relay_operation_records(self, device_addr):
        url = f"{self.base_url}/api/device/getRelayOptRecord"
        headers = self.get_headers()
        params = {
            "deviceAddr": device_addr,
            "beginTime":1722403958,
            "endTime":1722407558
        }
        response = requests.get(url, headers=headers, params=params)
        print(f"查询继电器操作记录{url}: {response.text}")
        if response.status_code == 404:
            print(f"URL not found: {url}")
            return {"error": "Endpoint not found"}
        return self.check_response(response)

    #获取报警数据列表
    def get_alarm_data(self):
        url = f"{self.base_url}/api/data/alarmRecordList"
        headers = self.get_headers()
        params={
            "deviceAddr":10053452,
            "nodeId":-1,
            "startTime":"2024-07-31 14:25:00",
            "endTime":"2024-07-31 15:27:00"
        }
        response = requests.get(url, headers=headers,params=params)
        print(f"Response from {url}: {response.text}")
        return self.check_response(response)

    # 根据设备编码获取实时数据
    def getRealtime_data_by_deviceID(self):
        addressList=["10053434","10053452","10053466","10053475","10053458","10053424"]
        url=f"{self.base_url}/api/data/getRealTimeDataByDeviceAddr"
        for address in addressList:
            headers = self.get_headers()
            params={
                "deviceAddrs":address
            }
            response = requests.get(url, headers=headers, params=params)
            print(f"根据设备地址获取实时数据 {address}: {response.text}")
            time.sleep(30)
# 使用示例
if __name__ == "__main__":
    platform = EnvMonitoringPlatform(
        base_url="http://www.0531yun.com",
        login_name="h230221zhej",
        password="h230221zhej"
    )

    # # 获取分组列表
    # group_list = platform.get_group_list()
    # print(f"获取分组情况:{group_list}")
    #
    # # 获取设备列表
    # device_list = platform.get_device_list()
    # print(f"获取设备列表:{device_list}")
    #
    # # 根据设备地址获取设备信息
    # device_info = platform.get_device_info(device_addr=10053452)
    # print(f"根据设备地址获取设备信息：{device_info}")
    #
    # # 获取设备继电器列表
    # relay_list = platform.get_device_relay_list(device_addr=10053452)
    # if "error" in relay_list:
    #     print(f"Error: {relay_list['error']}")
    # else:
    #     print(f"获取设备继电器列表：{relay_list}")
    #
    # # 继电器操作
    # # relay_op_result = platform.relay_operation(device_addr=10053452, relay_id=1, operation="on")
    # # print(f"继电器操作:{relay_op_result}")
    #
    # # 查询实时数据
    # realtime_data = platform.get_realtime_data()
    # if "error" in realtime_data:
    #     print(f"Error: {realtime_data['error']}")
    # else:
    #     print(f"查询实时数据：{realtime_data}")
    #
    # # 获取历史数据
    # history_data = platform.get_history_data(device_addr=10053434)
    # if "error" in history_data:
    #     print(f"Error: {history_data['error']}")
    # else:
    #     print(f"查询历史数据:{history_data}")
    #
    # # 查询继电器操作记录
    # relay_op_records = platform.get_relay_operation_records(device_addr=10053434)
    # if "error" in relay_op_records:
    #     print(f"Error: {relay_op_records['error']}")
    # else:
    #     print(f"查询继电器操作记录:{relay_op_records}")
    #
    # # 获取报警数据
    # alarm_data = platform.get_alarm_data()
    # print(f"获取报警数据:{alarm_data}")
    # # 根据设备地址获取实时数据
    realtime_data_byDeviceID=platform.getRealtime_data_by_deviceID()
    print(f"根据设备地址获取实时数据:{realtime_data_byDeviceID}")

