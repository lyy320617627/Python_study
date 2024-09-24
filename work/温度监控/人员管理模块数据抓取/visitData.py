import requests
import time
from datetime import datetime

class DingTalkAPI:
    def __init__(self, app_key, app_secret):
        self.app_key = app_key
        self.app_secret = app_secret
        self.access_token = self.get_access_token()

    def get_access_token(self):
        """
        获取钉钉的Access Token
        :return: Access Token
        """
        url = "https://oapi.dingtalk.com/gettoken"
        params = {
            "appkey": self.app_key,
            "appsecret": self.app_secret
        }
        response = requests.get(url, params=params)
        result = response.json()
        print(f"Access Token API 响应: {result}")  # 打印返回值帮助调试
        if result.get("errcode") == 0:
            return result.get("access_token")
        else:
            raise Exception(f"获取access_token失败: {result.get('errmsg')}")

    def get_process_instance_list(self, process_code, start_time, end_time):
        """
        获取审批实例列表
        :param process_code: 审批模板编码
        :param start_time: 开始时间，格式为 Unix 时间戳（毫秒）
        :param end_time: 结束时间，格式为 Unix 时间戳（毫秒）
        :return: 审批实例列表
        """
        url = "https://oapi.dingtalk.com/topapi/processinstance/list"
        headers = {
            "Content-Type": "application/json"
        }
        params = {
            "access_token": self.access_token
        }
        data = {
            "process_code": process_code,
            "start_time": start_time,
            "end_time": end_time,
            "size": 20,  # 一次查询的数量，最多50
            "cursor": 0  # 分页游标，第一次查询传0
        }
        response = requests.post(url, headers=headers, params=params, json=data)
        result = response.json()

        # 打印完整响应，帮助调试
        print(f"API 响应结果: {result}")

        if result.get("errcode") == 0:
            return result.get("result")
        elif result.get("errcode") == 200003:
            # Access token 失效，重新获取并重试
            print("Access Token 失效，正在重新获取...")
            self.access_token = self.get_access_token()
            return self.get_process_instance_list(process_code, start_time, end_time)
        else:
            raise Exception(f"获取审批实例列表失败: {result.get('errmsg', '未知错误')}")

    def fetch_approval_data(self, process_code, start_time, end_time):
        """
        获取审批流程数据，包括审批实例列表和详情
        :param process_code: 审批模板编码
        :param start_time: 开始时间，格式为 "yyyy-MM-dd HH:mm:ss"
        :param end_time: 结束时间，格式为 "yyyy-MM-dd HH:mm:ss"
        :return: 审批流程的详细数据
        """
        # 将日期字符串转换为时间戳 (毫秒级)
        start_timestamp = int(time.mktime(datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S").timetuple()) * 1000)
        end_timestamp = int(time.mktime(datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S").timetuple()) * 1000)

        instance_list = self.get_process_instance_list(process_code, start_timestamp, end_timestamp)
        detailed_instances = []
        for instance in instance_list['list']:
            instance_id = instance['process_instance_id']
            instance_details = self.get_process_instance_details(instance_id)
            detailed_instances.append(instance_details)
        return detailed_instances

# 使用示例
if __name__ == "__main__":
    app_key = "dingyyvsukrcwgjrrbyt"
    app_secret = "6h2WK5gA2Xct-5GoVDgVEv3rmHgDPWRgyBXJmLYsG8OGW78NZFCyWZjDVEpQFs5i"
    process_code = "PROC-4714D117-3604-4071-9060-30621C6B13A5"
    start_time = "2024-09-20 00:00:00"
    end_time = "2024-09-20 23:59:59"
    dingtalk_api = DingTalkAPI(app_key, app_secret)
    approval_data = dingtalk_api.fetch_approval_data(process_code, start_time, end_time)
