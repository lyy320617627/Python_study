import requests
class WisdomTest:
    def __init__(self, projectName):
        """
        :param projectName: 项目的名称
        """
        self.__accesskey = "cq3psoccmhabtm5ff2rg"
        self.__headers = self.GetHttpHeader()
        self.__projectName = projectName
        self.__baseUrl = "https://app2076.eapps.dingtalkcloud.com/gateway/rwgj/jsgo.lianjieqi.open/Rwgj9"
        self.__projectId = self.getProjectId()[0]
        self.__projectFormID = self.getProjectId()[1]
        self.taskPictureIdList = []  # 用来保存任务中后续用于下载图片的图片id列表  提交的图片不唯一
        self.taskDict = {}  # 调用获取项目下任务返回的字典，用来保存任务id和任务表单id
        self.TaskAfieldConfigList =self.processTaskDetail()
        self.link_id=None
        self.nodeDict={}# 用于保存所有节点表单详情中所有的key_id和key_name
        self.childFormDataDict={}

    def HttpRequests(self, params, httpUrl):
        # 发送post请求获取项目id
        try:
            # 发送 POST 请求
            response = requests.post(httpUrl, json=params, headers=self.__headers)
            # 检查响应状态码并处理
            response.raise_for_status()
            response = response.json()
            # 返回 JSON 响应
            return response
        except requests.exceptions.RequestException as e:
            # 捕获所有请求异常
            print(f"调用接口地址为{httpUrl}时出现错误: {e}")
            return None
        except ValueError:
            # 捕获 JSON 解码异常
            print(f"调用接口地址为{httpUrl}时不是有效的JSON")
            return None

    def GetHttpHeader(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.__accesskey}"
        }
        return headers

    def getProjectId(self):
        projectListUrl = f"{self.__baseUrl}.project.listProject"
        params = {
            "arg": {
                "page": 1,
                "page_size": 10,
                "project_name": self.__projectName,  # 项目名称
                'accesskey': self.__accesskey
            }
        }
        response = self.HttpRequests(params, projectListUrl)
        projectList = response.get("data").get("list").get("project")
        projectId = projectList[0].get("id")
        projectFormId = projectList[0].get("form_id")  # 获取项目的表单ID
        return projectId, projectFormId

    def taskOfProject(self):
        taskOfProjectUrl = f"{self.__baseUrl}.project.TaskList"
        params = {
            "arg": {
                "page": 1,
                "page_size": 10,
                "project_id": self.__projectId,
                "accesskey": self.__accesskey
            }
        }
        response = self.HttpRequests(params, taskOfProjectUrl)
        taskList = response.get("data")
        for task in taskList:
            if task.get("father_id") == "is_father":
                for item in task.get("cp7fip9ddemfq6vbdqjg"):
                    self.taskPictureIdList.append(item)
                self.taskDict["taskFormId"] = str(task.get("form_id"))
                self.taskDict["taskId"] = str(task.get("id"))
        print(f"taskDict内容: {self.taskDict}")

    def processTaskDetail(self):
        # 在调用 processTaskDetail 方法之前确保 taskDict 中有必要的键
        if "taskFormId" not in self.taskDict or "taskId" not in self.taskDict:
            print("taskDict 中缺少必要的键。请确保 taskOfProject 方法已正确执行。")
            return

        openFlowTaskDetailUrl = "https://app2076.eapps.dingtalkcloud.com/gateway/rwgj/jsgo.lianjieqi.open/Rwgj9.task.OpenFlowTaskDetail"
        params = {
            "arg": {
                "accesskey": self.__accesskey,
                "form_id": self.taskDict["taskFormId"],
                "id": self.taskDict["taskId"]
            }
        }
        response = self.HttpRequests(params=params, httpUrl=openFlowTaskDetailUrl)
        self.link_id=response.get("data").get("task_info").get("id")
        print(f"流程的link_id:{self.link_id}")
        nodeDataList = response.get("data").get("node_info")
        i = 0
        for nodeData in nodeDataList:
            i += 1
            if nodeData.get("node_name") == "检测执行（A样）":
                field_config = nodeData.get("field_config")
                keys_not_equal_3 = [key for key, value in field_config.items() if value != 3]
                print(f"field_config中的键值对中value对应的值不为3的列表集合为:{keys_not_equal_3}")
                return keys_not_equal_3

    # 表单详情接口，用来获取目标节点中对应的子表单id和子表单名称并保存到一个字典中
    def openFromDetail(self):
        url="https://app2076.eapps.dingtalkcloud.com/gateway/rwgj/jsgo.lianjieqi.open/Rwgj9.task.OpenFromDetail"
        params={
              "arg": {
                "accesskey":self.__accesskey,
                "id":self.taskDict["taskFormId"],
                "company_id": ""
              }
            }
        response = self.HttpRequests(params=params, httpUrl=url)
        response=response.get("data").get("form_content")
        for node in response:
            childNode={}
            if node.get("key_type")==18:
                self.nodeDict[str(node["key_name"])]=node["sub_form_value"]["form_id"]
                childDataList=node["sub_form_value"]["form_content"]
                for childData in childDataList:
                    childNode[childData["key_name"]]=childData["key_id"]
                self.childFormDataDict[node["key_name"]]=childNode
                print(f"node的类型为:{type(node)}:node的内容为:{node}")
        print(f"childFormDataDict中的数据为:{self.childFormDataDict}")
        # print(f"表单详情接口返回的响应数据为:{response}")
    # 子表单数据接口，获取子表单数据
    def subformData(self):
        url = "https://app2076.eapps.dingtalkcloud.com/gateway/rwgj/jsgo.lianjieqi.open/Rwgj9.task.OpenGetChildFormData"
        print(f"nodeDict: {self.nodeDict}")

        for node in self.nodeDict.keys():
            params = {
                "arg": {
                    "accesskey": self.__accesskey,
                    "link_id": self.link_id,
                    "form_id": self.nodeDict[node],
                    "page": 1,
                    "page_size": 100
                }
            }
            response = self.HttpRequests(params=params, httpUrl=url)
            response = response.get("data")

            if response.get("count") != 0:
                # 用于存放该节点所有子表单数据的列表
                all_subform_data = []

                for data in response.get("lists"):
                    row_data = {}
                    for item in data.keys():
                        for childkey, childValue in self.childFormDataDict[node].items():
                            if childValue == item:
                                row_data[childkey] = data[item]

                    # 将每一行的数据添加到列表中
                    all_subform_data.append(row_data)

                # 将所有子表单数据存储到对应的节点中
                self.childFormDataDict[node] = all_subform_data

                print(f"{node}对应的子表单数据为: {response}")

        print(f"childFormDataDict: {self.childFormDataDict}")

    # def subformData(self):
    #     url="https://app2076.eapps.dingtalkcloud.com/gateway/rwgj/jsgo.lianjieqi.open/Rwgj9.task.OpenGetChildFormData"
    #     print(f"nodeDict:{self.nodeDict}")
    #     for node in self.nodeDict.keys():
    #         params=  {
    #               "arg": {
    #                 "accesskey":self.__accesskey,
    #                 "link_id":self.link_id,
    #                 "form_id":self.nodeDict[node],
    #                 "page": 1,
    #                 "page_size": 100
    #               }
    #             }
    #         response = self.HttpRequests(params=params, httpUrl=url)
    #         response=response.get("data")
    #         if response.get("count")!=0:
    #             for data in response.get("lists"):
    #                 # 用于存放所有子表单数据的列表
    #                 all_subform_data = []
    #                 row_data = {}
    #                 for item in data.keys():
    #                     for childkey,childValue in self.childFormDataDict[node].items():
    #                         if childValue==item:
    #                             row_data[childkey]=data[item]
    #                 print(f"raw_data:{row_data}")
    #                 all_subform_data.append(row_data)
    #             # self.childFormDataDict[node][childkey]=data[item]
    #             self.childFormDataDict[node][childkey]=all_subform_data
    #                     # 将每一行的数据添加到列表中x
    #             print(f"{node}对应的子表单数据为:{response}")
    #             # print(f"所有子表单数据: {all_subform_data}")
    #     print(f"childFormDataDict:{self.childFormDataDict}")



if __name__ == '__main__':
    projectName = "取数测试0913（1:64版）"
    wisdomTest = WisdomTest(projectName)
    wisdomTest.taskOfProject()
    wisdomTest.processTaskDetail()
    wisdomTest.openFromDetail()
    wisdomTest.subformData()
