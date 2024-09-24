import requests

class WisdomTest:
    def __init__(self, access_token):
        self.access_token = access_token

    def get_child_form_data(self, payload):
        """
        调用钉钉接口获取子表单数据。

        :param payload: 请求体，包含需要传递的参数
        :return: 返回接口的响应数据
        """
        url = "https://app2076.eapps.dingtalkcloud.com/gateway/rwgj/jsgo.lianjieqi.open/Rwgj9.task.OpenGetChildFormData"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()

            # 返回JSON响应
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return None
        except ValueError:
            print("响应不是有效的JSON")
            return None

if __name__ == "__main__":
    token = "cq3psoccmhabtm5ff2rg"
    params =  {
      "arg": {
        "accesskey": token,
        "link_id": "cqo8dvhddem8nkds0sp0", # 此处传入的是获取流程任务详情的的task_info.id为:cqo8dvhddem8nkds0sp0
        "form_id": "cqo2et1ddem8nkdrvuo0",
        "page": 1,
        "page_size": 100
      }
}


    wisdom_test = WisdomTest(token)
    result = wisdom_test.get_child_form_data(params)

    if result:
        print("子表单数据:\n", result)
    else:
        print("无法获取子表单数据")
