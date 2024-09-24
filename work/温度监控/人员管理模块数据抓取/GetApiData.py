import requests
import json
from datetime import datetime, timedelta
from test import DingTalkAPI
from MySQLUtil import MySQLUtil
import pandas as pd

class DingTalkAttendance:
    def __init__(self, app_key, app_secret):
        self.app_key = app_key
        self.app_secret = app_secret
        self.access_token = self.get_access_token()
    # 获取钉钉access_token
    def get_access_token(self):
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
    # 获取组织下人员考勤记录，使用分页获取
    def get_attendance_records(self, user_ids, offset=0, limit=50):
        # 获取当前日期范围
        start_time = datetime.now().strftime('%Y-%m-%d 00:00:00')
        end_time = datetime.now().strftime('%Y-%m-%d 23:59:59')
        url = "https://oapi.dingtalk.com/attendance/list"
        headers = {
            "Content-Type": "application/json"
        }
        params = {
            "access_token": self.access_token
        }
        data = {
            "userIdList": user_ids,  # 人员ID列表
            "workDateFrom": start_time,  # 开始时间
            "workDateTo": end_time,  # 结束时间
            "offset": offset,  # 分页偏移量
            "limit": limit,  # 每次请求的记录数
            "isI18n": False
        }
        response = requests.post(url, headers=headers, params=params, data=json.dumps(data))
        result = response.json()
        if result.get("errcode") == 0:
            return result.get("recordresult")
        else:
            raise Exception(f"获取考勤记录失败: {result.get('errmsg')}")
    # 时间戳转换函数，返回年月日 时分秒格式
    def convert_timestamp_to_date(self, timestamp):
        return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
    # 处理考勤记录，转换时间戳
    def process_attendance_records(self, records):
        for record in records:
            record['baseCheckTime'] = self.convert_timestamp_to_date(record['baseCheckTime'])
            record['userCheckTime'] = self.convert_timestamp_to_date(record['userCheckTime'])
            record['workDate'] = self.convert_timestamp_to_date(record['workDate'])
        return records

    def attendanceDeal(self, attendanceDict):
        """
        :param attendanceDict: 处理完后的考勤字典
        :return:
        """
        attendanceList = []

        # 收集每个部门的考勤数据
        for department, users in attendanceDict.items():
            for name, attendanceSitution in users.items():
                # 判断打卡记录是否为正常
                is_absent = 0 if attendanceSitution == "Normal" else 1
                attendanceList.append([department, name, attendanceSitution, is_absent])

        # 创建DataFrame
        attendanceData = pd.DataFrame(attendanceList)
        attendanceData.columns = ["部门", "姓名", "打卡", "是否缺勤"]

        # 计算每个部门的出勤率和缺勤人数
        department_stats = attendanceData.groupby("部门").apply(
            lambda x: pd.Series({
                '总人数': x.shape[0],
                '缺勤人数': x.shape[0]-x['是否缺勤'].sum(), # 此处数据的意义为出勤人数，为后期调整
                '出勤率': (x.shape[0] - x['是否缺勤'].sum()) / x.shape[0] * 100
            })
        ).reset_index()
        # 获取部门信息字典
        ding_api = DingTalkAPI()
        departmentDict = ding_api.testTeamDict
        # 为每个部门新增 "部门ID" 列
        department_stats['部门ID'] = None  # 初始化部门ID列
        # 根据部门名称为部门ID赋值
        for departmentName, deptId in departmentDict.items():
            department_stats.loc[department_stats['部门'] == departmentName, '部门ID'] = deptId
        # 格式化出勤率保留两位小数，并将缺勤人数转换为整数类型
        department_stats['出勤率'] = department_stats['出勤率'].round(2)
        department_stats['缺勤人数'] = department_stats['缺勤人数'].astype(int)
        department_stats['总人数'] = department_stats['总人数'].astype(int)
        department_stats['部门ID'] = department_stats['部门ID'].astype(str)
        print(f"最终的考勤列表为：{attendanceList}")
        print(f"考勤数据:\n{attendanceData}")
        print(f"部门统计结果:\n{department_stats}")
        # 创建 MySQL 数据库连接
        dataBaseData = department_stats[["部门ID", "部门", "总人数", "出勤率", "缺勤人数"]].values.tolist()
        print(f"dataBaseData:\n{dataBaseData}")
        conn = MySQLUtil(host="192.168.0.148", port=3306, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
        excute_sql = """
            INSERT INTO bs_person_managerment_data 
            (dept_id, dept_name, dept_count, attend_rate, attend_count)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            dept_name = VALUES(dept_name),
            dept_count = VALUES(dept_count),
            attend_rate = VALUES(attend_rate),
            attend_count = VALUES(attend_count)
            """

        conn.executemany(excute_sql,dataBaseData)


if __name__ == "__main__":
    # 钉钉应用的app_key和app_secret
    app_key = "dingyyvsukrcwgjrrbyt"
    app_secret = "6h2WK5gA2Xct-5GoVDgVEv3rmHgDPWRgyBXJmLYsG8OGW78NZFCyWZjDVEpQFs5i"
    # 初始化考勤类
    dingtalk_attendance = DingTalkAttendance(app_key, app_secret)
    # 获取用户ID列表
    ding_api = DingTalkAPI()
    userIdList = [user_id for users in ding_api.all_user.values() for user_id in users.values()]
    print(f"需要抓取考勤记录的人员总数为:{len(userIdList)}")
    print(f"ding_api.all_user:\n{ding_api.all_user}")
    finalDict=ding_api.all_user
    # 分页获取考勤记录
    all_records = []
    offset = 0
    limit = 50
    try:
        while True:
            records = dingtalk_attendance.get_attendance_records(userIdList, offset, limit)
            if records:
                all_records.extend(records)
                offset += limit
            else:
                break
        # 处理考勤记录，转换时间戳
        processed_records = dingtalk_attendance.process_attendance_records(all_records)
        print(f"今日考勤记录的人数总数为:{len(processed_records)}")
        # 输出处理后的考勤记录
        for record in processed_records:
            for key, value in finalDict.items():
                for name,userid in value.items():
                    if record['userId']==userid:
                        finalDict[key][name]=record['locationResult']
            print(record)
        print(f"finalDict:\n{finalDict}")
    except Exception as e:
        print(str(e))
    print(f"最终的考勤记录数据为：{finalDict}")
    dingtalk_attendance.attendanceDeal(finalDict)

