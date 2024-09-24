"""
表单详情接口
"""
import requests


class WisdomTest:
    def __init__(self, access_token):
        self.access_token = access_token
    def get_form_detail(self, payload):
        """
        调用钉钉接口获取表单详情。

        :param payload: 请求体，包含需要传递的参数
        :return: 返回接口的响应数据
        """
        url = "https://app2076.eapps.dingtalkcloud.com/gateway/rwgj/jsgo.lianjieqi.open/Rwgj9.task.OpenFromDetail"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
        sourceList=[]
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            response=response.json()
            datalist=response['data'].get("form_content")
            for data in datalist:
                if data["key_type"]==18:
                    sourceList.append(data)

            return sourceList

        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return None
        except ValueError:
            print("响应不是有效的JSON")
            return None


if __name__ == "__main__":
    token = "cq3psoccmhabtm5ff2rg"
    # 获取表单详情
    params = {
        "arg": {
            "accesskey": token,
            "id": "cq2voaaie99usu3pj2a0"
        }
    }
    target=['cp6qn99ddemfq6vbaum0', 'cp6r52hddemfq6vbb1cg', 'cp7fip9ddemfq6vbdqjg', 'cp7fje1ddemfq6vbdqk0', 'cp7fke1ddemfq6vbdqkg', 'cp7fl0pddemfq6vbdql0', 'cp7g2i1ddemfq6vbdtr0', 'cp7g3phddemfq6vbdtug', 'cp7g5b9ddemfq6vbe0gg', 'cp7g6jpddemfq6vbe0ig', 'cp7g6mhddemfq6vbe0jg', 'cp7gb5hddemfq6vbe150', 'cp7gr41ddemfq6vbe48g', 'cp7gs21ddemfq6vbe4a0', 'cp7gsb9ddemfq6vbe4fg', 'cp7gsnpddemfq6vbe4ig', 'cp7gudpddemfq6vbe4kg', 'cp7gvi1ddemfq6vbe4mg', 'cp7h5dhddemfq6vbe6fg', 'cp7h60hddemfq6vbe6m0', 'cp7hbg9ddemfq6vbe760', 'cp7hc59ddemfq6vbe77g', 'cp7hc6pddemfq6vbe78g', 'cp7hc79ddemfq6vbe79g', 'cp7hc91ddemfq6vbe7ag', 'cp7hcshddemfq6vbe7bg', 'cp7hdjpddemfq6vbe7dg', 'cp7hds9ddemfq6vbe7e0', 'cp7he09ddemfq6vbe7n0', 'cp7he0hddemfq6vbe800', 'cp7hfbhddemfq6vbe8mg', 'cp7hfj1ddemfq6vbe8n0', 'cp7hfj9ddemfq6vbe8ng', 'cp7hfjhddemfq6vbe8o0', 'cp7hfjpddemfq6vbe8og', 'cp7hg9hddemfq6vbe8p0', 'cp7hgapddemfq6vbe8q0', 'cp7hgb1ddemfq6vbe8r0', 'cp7hgdhddemfq6vbe8v0', 'cp7hgdpddemfq6vbe900', 'cp7hge9ddemfq6vbe910', 'cp7hj6pddemfq6vbe92g', 'cp7hj91ddemfq6vbe93g', 'cp7hrmhddemfq6vbe9b0', 'cp7u81pddemfq6vber3g', 'cq5q7g1ddemcqbmhodl0', 'cq6vio1ddemaqvvt50ig', 'cq706a1ddemaqvvt54ug', 'cq708c9ddemaqvvt54v0', 'cq7ip19ddem9a0v0fet0', 'cqo2et1ddem8nkdrvung', 'cqo2phhddem8nkds025g', 'cqo6oe1ddem8nkds0p2g', 'cqo82o1ddem8nkds0qqg', 'cqo89cpddem8nkds0s2g']

    wisdom_test = WisdomTest(token)
    form_result = wisdom_test.get_form_detail(params)
    finallyList=[]
    for param in form_result:
        if param["key_id"] in target and param["key_name"]=="14、高低温循环试验（A样）":
            finallyList.append(param)

    if finallyList:
        print("子表单详情信息为:", finallyList)
    else:
        print("无法获取表单详情")
