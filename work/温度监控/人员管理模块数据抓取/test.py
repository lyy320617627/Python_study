import requests
import time
from datetime import datetime

class DingTalkAPI:
    def __init__(self):
        self.base_url = "https://oapi.dingtalk.com"
        self.app_key = "dingyyvsukrcwgjrrbyt"
        self.app_secret = "6h2WK5gA2Xct-5GoVDgVEv3rmHgDPWRgyBXJmLYsG8OGW78NZFCyWZjDVEpQFs5i"
        self.access_token = self.getAccessToken()
        self.testTeamDict = self.get_all_department_ids()  # 用来存储测试团队的部门id和部门名称。
        self.all_user = self.get_all_users()
        self.flag=True


    def getAccessToken(self):
        url = f"{self.base_url}/gettoken"
        params = {
            "appkey": self.app_key,
            "appsecret": self.app_secret
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            result = response.json()
            if result['errcode'] == 0:
                print(f"accessToken: {result['access_token']}")
                return result['access_token']
            else:
                print(f"获取access_token失败: {result['errmsg']}")
                return None
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None

    def get_department_list(self, dept_id):
        """
        获取指定部门的子部门列表
        :param dept_id: 部门ID
        :return: 子部门列表
        """
        url = f"{self.base_url}/topapi/v2/department/listsub"
        headers = {"Content-Type": "application/json"}
        params = {
            "access_token": self.access_token
        }
        data = {
            "dept_id": dept_id  # 根部门ID为1
        }

        response = requests.post(url, headers=headers, params=params, json=data)

        if response.status_code == 200:
            result = response.json()
            if result['errcode'] == 0:
                return result['result']
            else:
                print(f"获取部门列表失败: {result['errmsg']}")
                return None
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None

    def get_all_department_ids(self, dept_id=1):
        """
        获取所有部门ID，找到“测试团队”及其子部门
        """
        print(f"当前部门ID: {dept_id}")  # 打印当前部门ID
        testTeamDict = {}
        finaltestTeamDict = {}
        sub_departments = self.get_department_list(dept_id)
        if sub_departments:
            for sub_dept in sub_departments:
                if sub_dept['name'] == "测试团队":
                    print(f"子部门ID: {sub_dept['dept_id']}, 部门名称: {sub_dept['name']}")  # 打印子部门ID和名称
                    testTeamDict[sub_dept['name']] = sub_dept['dept_id']
                    break
                else:
                    print(f"没有找到测试团队信息，请检查是否更换名称")

        if testTeamDict:
            for key, value in testTeamDict.items():
                testTeamList = self.get_department_list(value)
                for testTeam in testTeamList:
                    print(f"testTeam: {testTeam}")
                    finaltestTeamDict[testTeam["name"]] = testTeam["dept_id"]
        print(f"finaltestTeamDict: {finaltestTeamDict}")
        return finaltestTeamDict

    def get_department_users(self, dept_id, cursor=0, size=100):
        """
        获取指定部门下的用户列表，并处理分页
        :param dept_id: 部门ID
        :param cursor: 分页游标，默认0
        :param size: 每页的记录数，最大100
        :return: 用户列表和是否还有更多
        """
        url = f"{self.base_url}/topapi/v2/user/list"
        headers = {"Content-Type": "application/json"}
        params = {
            "access_token": self.access_token
        }
        data = {
            "dept_id": dept_id,
            "cursor": cursor,
            "size": size
        }

        response = requests.post(url, headers=headers, params=params, json=data)

        if response.status_code == 200:
            result = response.json()
            if result['errcode'] == 0:
                return result['result']['list'], result['result']['has_more']
            else:
                print(f"获取部门用户失败: {result['errmsg']}")
                return None, False
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None, False

    def get_all_users(self):
        """
        获取所有部门下的所有用户
        :return: 用户列表
        """
        all_users = {}
        for key, value in self.testTeamDict.items():
            cursor = 0
            has_more = True
            userList=[]
            tmp_user = {}
            # 循环直到没有更多用户
            while has_more:
                users, has_more = self.get_department_users(value, cursor)
                if users:
                    for user in users:
                        print(f"userName: {user['name']}, userId: {user['userid']}")

                        tmp_user[user['name']] = user['userid']
                    cursor += len(users)  # 更新游标以获取下一页的用户
            all_users[key] = tmp_user
        print(f"tmp_userList的长度为:{len(userList)}")
        return all_users

    def get_attendance_records(self, user_id, offset=0, limit=5):
        # 时间范围，获取今天的考勤记录
        # 获取当前日期
        start_time = datetime.now().strftime('%Y-%m-%d 00:00:00')
        end_time = datetime.now().strftime('%Y-%m-%d 23:59:59')
        print(f"start_time: {start_time}")
        print(f"end_time: {end_time}")
        url = f"{self.base_url}/attendance/list"
        headers = {"Content-Type": "application/json"}
        params = {
            "access_token": self.access_token
        }
        data = {
            "userIds": [user_id],
            "workDateFrom": start_time,
            "workDateTo": end_time,
            "offset": offset,
            "limit": limit
        }
        flag=True
        while flag:
            response = requests.post(url, headers=headers, params=params, json=data)
            result = response.json()
            if result.get("errcode") == 0:
                print(f"result:{result}")
                flag=False
                return result.get("recordresult")
            else:
                print(f"获取考勤记录失败: {result.get('errmsg')}")
                time.sleep(30)
if __name__ == "__main__":
    ding_api=DingTalkAPI()
    userIdList = []
    # 遍历所有部门和用户
    for department, users in ding_api.all_user.items():
        for user_name, user_id in users.items():
            userIdList.append(user_id)
    print(f"userIdList:{userIdList}")
    print(f"userIdList的长度为:{len(userIdList)}")
    # 分页获取考勤记录
    all_records = []
    records = ding_api.get_attendance_records(userIdList)
    print(f"records:{records}")

