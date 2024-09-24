"""
调用任务列表的测试接口，查看测试接口返回的效果
"""
import requests

class TaskList:
    def __init__(self, access_token):
        self.access_token = access_token

    def get_task_list(self, payload):
        """
        调用钉钉接口获取任务列表。

        :param payload: 请求体，包含需要传递的参数
        :return: 返回接口的响应数据
        """
        url = "https://app2076.eapps.dingtalkcloud.com/gateway/rwgj/jsgo.lianjieqi.open/Rwgj9.task.OpenTaskList"

        # 设置请求头，包括认证令牌
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"  # Assuming Bearer token usage, adjust as necessary
        }

        try:
            # 发送 POST 请求
            response = requests.post(url, json=payload, headers=headers)

            # 检查响应状态码并处理
            response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code

            # 返回 JSON 响应
            return response.json()

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
            "project_id": "cqo8copddem8nkds0s50",
        }
    }

    wisdom_test = TaskList(token)
    result = wisdom_test.get_task_list(params)

    if result:
        print("任务列表:", result)
    else:
        print("无法获取任务列表")
