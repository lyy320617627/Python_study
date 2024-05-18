import requests
import json

class ActLog:


    def send_post_request(self,authorization,id,docNum):
        url = "http://10.217.133.164/apipost/api-flow/flow/workbench/actLog"
        payload = {
            "applId": id,
            "docNum": docNum
        }

        headers = {
            "Content-Type": "application/json",
            "authorization": authorization
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                result_list = response.json()
                # print("Response:")
                # print(result_list)
                return result_list

            else:
                print(f"Request failed with status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print("Request exception:", e)

    def get_list(self,response_data,parentId,order_type):#返回审批列表
        log_list_data = []
        if 'code' in response_data and response_data['code'] == '0':
            if 'data' in response_data :
                tmpList = response_data['data']
                #审批结果数据
                print(tmpList)
                # 转换为列表并添加 parentId 和 order_type
                for logItem in tmpList:
                    # 获取每个子列表的值
                    lineList = list(logItem.values())
                    # 在最前面添加 parentId 和 order_type
                    lineList.insert(0, parentId)
                    lineList.insert(1, order_type)
                    log_list_data.append(lineList)
                return log_list_data
        return None
    def get_firstAuditTime(self,response_data): #需求引入工单提交的审批时间
        if 'code' in response_data and response_data['code'] == '0':
            if 'data' in response_data :
                completeDate = response_data['data'][0]['completeDate']
                return completeDate
        return None

if __name__ == "__main__":
    # 发送 POST 请求并打印返回结果
    authorization = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZW5hbnRfaWQiOjQsImNlbnRyYWxfZmxhZyI6Ik4iLCJ1c2VyX25hbWUiOiLog6HngpznlLciLCJyb2xlcyI6W3siYXV0aG9yaXR5IjoiQ0dKQlIifSx7ImF1dGhvcml0eSI6IlBUWUcxMSJ9LHsiYXV0aG9yaXR5IjoiWFQtWkoifSx7ImF1dGhvcml0eSI6IjY4NDgifV0sImNsaWVudF90eXBlIjoiU0giLCJjbGllbnRfaWQiOiJzaW5vLW1hbGwiLCJzY29wZSI6WyJhbGwiXSwiY2F0ZWdvcmllcyI6W3sidGl0bGUiOiLph4fotK0iLCJjb2RlIjoiQ0ctWkoiLCJpbmRleFVyaSI6IumHh-i0rSJ9XSwiY29tcGFueV9zaG9ydF9uYW1lIjoi5rWZIiwiZXhwIjoxNzEyMTE0NDI1LCJqdGkiOiI4ZjM1ZDY0MS0yNmVmLTQzM2UtYjM2NC1hM2UxZDc2MTc0NDAiLCJjb21wYW55X2lkIjoxMzM0LCJncm91cF9uYW1lIjoi6YeH6LSt566h55CG5a6kIiwibW9iaWxlIjoiMTU3NTczMDIyODUiLCJ2ZW5kb3JfbmFtZSI6bnVsbCwibGFzdF9jaGFuZ2VfcGFzcyI6MTY4OTU1NjEyNzAwMCwiYXV0aG9yaXRpZXMiOlsiUFRZRzExIiwiQ0dKQlIiLCJYVC1aSiIsIjY4NDgiXSwiY29tcGFueV9sZXZlbCI6IjIiLCJsb2dpbl9uYW1lIjoiaHV3ZWluYW5fWkoiLCJ1c2VyX2lkIjo5NDQ0LCJncm91cF9pZCI6NjM2OSwidmVuZG9yX2lkIjpudWxsLCJjb21wYW55X25hbWUiOiLmtZnmsZ_liIblhazlj7giLCJzZWNvbmRfZGVwdF9pZCI6NjI1NCwic2Vjb25kX2RlcHRfbmFtZSI6IuaUr-aSkeacjeWKoemDqCJ9.dXViSJJdXAjWF_LIU1c8sXUsitY48dLrmxbQgOwpaltiJPRICWnQT567SMR3ujCIlW6mvAfufW8Pyj0rUClmI0D5plDfrKjGFSBljCpwal3oME5U3ue2QnIqFPciNNTbQacrLD3O_-6hjAiRr9F6QGE371DxaFX4T-NxdXk8Nes"
    actLog = ActLog()
    response = actLog.send_post_request(authorization,185937,'浙采需[20240328]015号')
    len = len(response['data'])
    print(response['data'][0]['completeDate'])
    print(actLog.get_list(response,185937,'结果工单'))

