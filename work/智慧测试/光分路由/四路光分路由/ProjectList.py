"""
注意:项目名称搜索获取到的数据可能按照模糊匹配进行搜索，
    防止搜索的结果存在差异，务必保持项目名称精准。

项目列表接口：用于返回项目id
"""
import requests

class ProjectList:
    def __init__(self, access_token):
        self.access_token = access_token

    def list_projects(self, payload):
        """
        调用钉钉接口获取项目列表。

        :param payload: 请求体，包含需要传递的参数
        :return: 返回接口的响应数据
        """
        url = "https://app2076.eapps.dingtalkcloud.com/gateway/rwgj/jsgo.lianjieqi.open/Rwgj9.project.listProject"

        # 设置请求头，包括认证令牌
        headers = {
            "Content-Type": "application/json",
        }

        try:
            # 发送 POST 请求
            response = requests.post(url, json=payload, headers=headers)

            # 检查响应状态码并处理
            response.raise_for_status()
            response = response.json()
            projectList=response.get("data").get("list").get("project")
            projectId=projectList[0].get("id")
            projectName=projectList[0].get("project_name")
            # 返回 JSON 响应
            return projectId,projectName

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
            "project_name": "字段对应测试0805",  # 项目名称
            'accesskey' :"cq3psoccmhabtm5ff2rg"  # 替换为有效的访问令牌
        }
    }

    projectList = ProjectList(token)
    projectId,projectName = projectList.list_projects(params)

    if projectId:
        print(f"通过项目列表获取到的项目id为:{projectId}\n获取到的项目名称为:{projectName}")
    else:
        print("无法获取项目列表")

