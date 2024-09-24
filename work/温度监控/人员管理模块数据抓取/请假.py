from decimal import Decimal
import requests
import time
from datetime import datetime, timedelta
import json
from MySQLUtil import MySQLUtil
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
        if result.get("errcode") == 0:
            return result.get("access_token")
        else:
            raise Exception(f"获取access_token失败: {result.get('errmsg')}")

    def get_process_code_by_name(self, process_name):
        """
        根据审批流程名称获取审批流程的ID (process_code)
        :param process_name: 审批流程名称
        :return: 审批流程ID (process_code)
        """
        url = "https://oapi.dingtalk.com/topapi/process.get_by_name"
        headers = {
            "Content-Type": "application/json"
        }
        params = {
            "access_token": self.access_token
        }
        data = {
            "name": process_name
        }
        response = requests.post(url, headers=headers, params=params, json=data)
        result = response.json()
        if result.get("errcode") == 0:
            return result.get("process_code")
        else:
            raise Exception(f"获取审批流程ID失败: {result.get('errmsg')}")

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
            "size": 10,  # 一次查询的数量，最多50
            "cursor": 0  # 分页游标，第一次查询传0
        }
        response = requests.post(url, headers=headers, params=params, json=data)
        result = response.json()
        if result.get("errcode") == 0:
            return result.get("result")
        else:
            raise Exception(f"获取审批实例列表失败: {result.get('errmsg', '未知错误')}")

    def get_process_instance_details(self, process_instance_id):
        """
        获取审批实例的详细信息
        :param process_instance_id: 审批实例ID
        :return: 审批实例详情
        """
        url = "https://oapi.dingtalk.com/topapi/processinstance/get"
        headers = {
            "Content-Type": "application/json"
        }
        params = {
            "access_token": self.access_token
        }
        data = {
            "process_instance_id": process_instance_id
        }
        response = requests.post(url, headers=headers, params=params, json=data)
        result = response.json()
        if result.get("errcode") == 0:
            return result.get("process_instance")
        else:
            raise Exception(f"获取审批实例详情失败: {result.get('errmsg', '未知错误')}")

    def is_equal_to_today(self,date_str):
        """
        判断给定的日期时间字符串是否与今天的日期相等（不比较具体的时间部分）
        :param date_str: 日期时间字符串，格式为 "YYYY-MM-DD HH:MM"
        :return: 如果日期与今天相等，返回 True；否则返回 False
        """
        # 将输入的字符串转换为 datetime 对象
        input_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        # 获取今天的日期，不包含时间部分
        today_date = datetime.today().date()
        # 比较日期部分是否相等
        return input_date.date() == today_date

    def fetch_approval_data(self, process_code):
        """
        获取审批流程数据，包括审批实例列表和详情
        """
        today = datetime.today()
        half_month_ago = today - timedelta(days=15)
        start_time = half_month_ago.strftime("%Y-%m-%d 00:00:00")
        end_time = today.strftime("%Y-%m-%d 23:59:59")
        todayVisits = 0
        # 将日期字符串转换为时间戳 (毫秒级)
        start_timestamp = int(time.mktime(datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S").timetuple()) * 1000)
        end_timestamp = int(time.mktime(datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S").timetuple()) * 1000)
        # 获取审批实例列表
        instance_list = self.get_process_instance_list(process_code, start_timestamp, end_timestamp)
        # 获取每个实例的详细信息
        detailed_instances = []
        for instance in instance_list['list']:
            instance_id = instance['process_instance_id']
            instance_details = self.get_process_instance_details(instance_id)
            detailed_instances.append(instance_details)
        print(f"流程实例的长度为: {len(detailed_instances)}")
        print(f"流程实例的数据为: {detailed_instances}")
        visitDict = {}
        for detailed_instance in detailed_instances:
            uniqueId = detailed_instance['business_id']
            formDataList = detailed_instance['form_component_values']
            tmp_formData = {}
            for formData in formDataList:
                if formData['name'] == "到访时间" or formData['name'] == "访问人员信息":
                    if formData['name'] == "访问人员信息":
                        try:
                            # 尝试将其解析为 JSON 格式
                            formData['value'] = json.loads(formData['value'])
                        except json.JSONDecodeError:
                            print(f"无法解析的访问人员信息: {formData['value']}")
                            continue
                    tmp_formData[formData['name']] = formData['value']
            if tmp_formData:
                visitDict[uniqueId] = tmp_formData
        # 检查每个访问数据
        for key, value in visitDict.items():
            for key2, value2 in value.items():
                if key2 == "到访时间":
                    isTodayVisitor = self.is_equal_to_today(value2)
                    if isTodayVisitor:
                        todayVisits+=len(value['访问人员信息'])
        conn=MySQLUtil(host="192.168.0.148", port=3306, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
        query_sql="""SELECT SUM(attend_count)
                   FROM bs_person_managerment_data;"""
        # 提取查询结果中的具体值，并确保它是整数
        query_result = conn.execute(query_sql)
        # 从查询结果中提取第一个值，并确保它是整数
        query_count = query_result[0][0] if query_result[0][0] else Decimal(0)
        query_count = int(query_count)  # 将 Decimal 转换为 int 类型
        print(f"query_count: {query_count}")
        sql="TRUNCATE TABLE bs_visit_data;"
        conn.execute(sql)
        conn.batchInsert("bs_visit_data",["real_time_person","visit_count"],[[(todayVisits+query_count),todayVisits]])
        return todayVisits




# 使用示例
if __name__ == "__main__":
    app_key = "dingyyvsukrcwgjrrbyt"
    app_secret = "6h2WK5gA2Xct-5GoVDgVEv3rmHgDPWRgyBXJmLYsG8OGW78NZFCyWZjDVEpQFs5i"
    process_name = "外部人员访问申请"  # 审批流程的名称
    dingtalk_api = DingTalkAPI(app_key, app_secret)
    # 获取流程ID
    process_code = dingtalk_api.get_process_code_by_name(process_name)
    print(f"审批流程名称 '{process_name}' 对应的流程ID是: {process_code}")
    # 获取审批流程的详细数据
    approval_data = dingtalk_api.fetch_approval_data(process_code)
    print(f"approval_data: {approval_data}")
