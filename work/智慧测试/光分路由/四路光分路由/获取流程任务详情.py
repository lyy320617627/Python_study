import requests

class WisdomTest:
    def __init__(self, access_token):
        self.access_token = access_token

    def get_task_list(self, payload):
        """
        调用钉钉接口获取任务列表。

        :param payload: 请求体，包含需要传递的参数
        :return: 返回接口的响应数据或指定节点信息
        """
        url = "https://app2076.eapps.dingtalkcloud.com/gateway/rwgj/jsgo.lianjieqi.open/Rwgj9.task.OpenFlowTaskDetail"

        # 设置请求头，包括认证令牌
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

        try:
            # 发送 POST 请求
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  # 检查HTTP错误

            # 解析响应
            json_response = response.json()
            nodes_list = json_response.get("data", {}).get("node_info")
            print(f"流程的task_info.id为:{json_response.get('data').get('task_info').get('id')}")


            if not nodes_list:
                print("未找到节点信息")
                return None
            # 遍历节点列表，查找目标节点
            field_config = []
            for node in nodes_list:
                if node.get("node_name") == "检测执行（A样）":
                    for key, value in node.get("field_config", {}).items():
                        if value != 3:
                            field_config.append(key)
                    print(f"节点信息：{field_config}")
                    return field_config, json_response
            print(f"节点信息：{field_config}")


            print("未找到指定节点")
            return None

        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return None
        except ValueError:
            print("响应不是有效的JSON")
            return None

if __name__ == "__main__":
    token = "cq3psoccmhabtm5ff2rg"  # 替换为有效的访问令牌
    params = {
        "arg": {
            "accesskey": token,
            "form_id": "cq2voaaie99usu3pj2a0",
            "id": "cqo8dvhddem8nkds0sp0"
        }
    }

    wisdom_test = WisdomTest(token)
    result,json_response= wisdom_test.get_task_list(params)

    if result:
        print("检测执行（A样）节点信息为:\n", result)
        print("流程任务:\n", json_response)
    else:
        print("无法获取任务列表")
