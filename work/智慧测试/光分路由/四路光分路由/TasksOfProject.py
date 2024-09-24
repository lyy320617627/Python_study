import requests

class TaskOfProject:
    def __init__(self, access_token):
        self.access_token = access_token

    def list_tasks(self, payload):
        """
        调用钉钉接口获取任务列表。

        :param payload: 请求体，包含需要传递的参数
        :return: 返回接口的响应数据
        """
        url = "https://app2076.eapps.dingtalkcloud.com/gateway/rwgj/jsgo.lianjieqi.open/Rwgj9.project.TaskList"

        # 设置请求头，包括认证令牌
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"  # 假设使用 Bearer token，如有需要可调整
        }

        try:
            # 发送 POST 请求
            response = requests.post(url, json=payload, headers=headers)

            # 检查响应状态码并处理
            response.raise_for_status()  # 先检查HTTP状态码

            # 解析JSON响应
            response_data = response.json()
            dataList=response_data["data"]
            dataDetailList=[]
            # for data in dataList:

            print(f"获取项目下任务返回任务长度为：{len(dataList)}")

            # 返回 JSON 响应
            return response_data

        except requests.exceptions.RequestException as e:
            # 捕获所有请求异常
            print(f"请求失败: {e}")
            return None
        except ValueError:
            # 捕获 JSON 解码异常
            print("响应不是有效的JSON")
            return None

if __name__ == "__main__":
    token = "cq3psoccmhabtm5ff2rg"  # 替换为有效的访问令牌
    params = {
        "arg": {
            "page": 1,
            "page_size": 10,
            "show_child_task": 1,
            "project_id": "cqo8copddem8nkds0s50",  # 替换为实际的项目ID
            "accesskey": token  # 如果API需要这个参数在请求体中，保留它
        }
    }

    task_of_project = TaskOfProject(token)
    result = task_of_project.list_tasks(params)

    if result:
        print("任务列表:", result)
    else:
        print("无法获取任务列表")
