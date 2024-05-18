import requests
import json
from datetime import datetime, timedelta
import re
from MySQLUtil import MySQLUtil


def convert_to_str_if_not_empty(value):
    return str(value) if value else None
class GetInfosList:

    def send_post_request(self,authorization,cookie,pageNo):
        url = "https://wap.zj.10086.cn/ai/shopkf/oneframe/qrySession/qrySessions"
        payload = {
            "authAgentId": "undefined",
            "start": pageNo,
            "pageNum": 10000,
            "starttimeStart": "",
            "starttimeEnd": "",
            "tenantId": "ff8080826537c4fc016538bd3b010089",
            "undefined": "不限",
            "session": "",
            "siginid": "",
            "agentid": "",
            "user": "",
            "type": "不限"
        }

        headers={
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': cookie,
            'Referer': 'https://wap.zj.10086.cn/ai/shopkf/ucfront/log/html/qrySession.html',
            'Authorization': authorization
        }

        try:
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code == 200:
                # result_list = self.parse_records(response.json())
                print("Response:",response.json())
                # print(result_list)
                print(type(response))
                return response

            else:
                print(f"Request failed with status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print("Request exception:", e)


    # 获取电话列表方便查找详细对话内容
    def getChat_detail_tel(self,response):
        tel_num_list=[]
        response_dict=response.json()['rows']
        for item in response_dict:
            tel_num_list.append(item['callerNumber'])
        # print(tel_num_list)
        print(len(tel_num_list))
        return tel_num_list
    #将获取到的字典自动转化成元组，方便后续插入到数据库中

    def idct_to_tuple(self,response):
        if response is None:  # 检查响应对象是否为 None
            print("Response is None")
            return []  # 如果响应对象为 None，则返回空列表
        response_dict=response.json()['rows']
        insert_tuple_list = []
        for item in response_dict:
            insert_tuple_list.append(
                (convert_to_str_if_not_empty(item.get('serialId')),
                 convert_to_str_if_not_empty(item.get('uuid')),
                 convert_to_str_if_not_empty(item.get('legaUuid')),
                 convert_to_str_if_not_empty(item.get('legbUuid')),
                 convert_to_str_if_not_empty(item.get('agentId')),
                 convert_to_str_if_not_empty(item.get('callerNumber')),
                 convert_to_str_if_not_empty(item.get('calleeNumber')),
                 convert_to_str_if_not_empty(item.get('startTime')),
                 convert_to_str_if_not_empty(item.get('stopTime')),
                 int(item['duration']) if item.get('duration') is not None else None,
                 convert_to_str_if_not_empty(item.get('callType')),
                 convert_to_str_if_not_empty(item.get('checkinId')),
                 int(item['accessType']) if item.get('accessType') is not None else None,
                 convert_to_str_if_not_empty(item.get('sessionType')),
                 convert_to_str_if_not_empty(item.get('satisfactionLevel')),
                 convert_to_str_if_not_empty(item.get('satisfactionContext')),
                 int(item['acceptMonth']) if item.get('acceptMonth') is not None else None,
                 convert_to_str_if_not_empty(item.get('skillGroupId')),
                 convert_to_str_if_not_empty(item.get('recordUrl')),
                 convert_to_str_if_not_empty(item.get('interConfrcId')),
                 convert_to_str_if_not_empty(item.get('sessionId')),
                 convert_to_str_if_not_empty(item.get('createTime')),
                 convert_to_str_if_not_empty(item.get('tenantId')),
                 convert_to_str_if_not_empty(item.get('satisfactionStatus')),
                 convert_to_str_if_not_empty(item.get('qualityId')),
                 convert_to_str_if_not_empty(item.get('qualityLevel')),
                 convert_to_str_if_not_empty(item.get('qualityStatus')),
                 convert_to_str_if_not_empty(item.get('qualityTime')))
            )
        print(insert_tuple_list)
        return insert_tuple_list
    def insert_into_table(self,insert_tuple_list):
        mysqlUtil = MySQLUtil(host="172.16.8.241", user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
        insert_query = """
                        INSERT INTO kf_chat_infolist 
                        (serialId, uuid, legaUuid, legbUuid, agentId, callerNumber, calleeNumber, startTime, stopTime, duration, callType, checkinId, accessType, sessionType, satisfactionLevel, satisfactionContext, acceptMonth, skillGroupId, recordUrl, interConfrcId, sessionId, createTime, tenantId, satisfactionStatus, qualityId, qualityLevel, qualityStatus, qualityTime) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                        ON DUPLICATE KEY UPDATE 
                        uuid = VALUES(uuid),
                        legaUuid = VALUES(legaUuid),
                        legbUuid = VALUES(legbUuid),
                        agentId = VALUES(agentId),
                        callerNumber = VALUES(callerNumber),
                        calleeNumber = VALUES(calleeNumber),
                        startTime = VALUES(startTime),
                        stopTime = VALUES(stopTime),
                        duration = VALUES(duration),
                        callType = VALUES(callType),
                        checkinId = VALUES(checkinId),
                        accessType = VALUES(accessType),
                        sessionType = VALUES(sessionType),
                        satisfactionLevel = VALUES(satisfactionLevel),
                        satisfactionContext = VALUES(satisfactionContext),
                        acceptMonth = VALUES(acceptMonth),
                        skillGroupId = VALUES(skillGroupId),
                        recordUrl = VALUES(recordUrl),
                        interConfrcId = VALUES(interConfrcId),
                        sessionId = VALUES(sessionId),
                        createTime = VALUES(createTime),
                        tenantId = VALUES(tenantId),
                        satisfactionStatus = VALUES(satisfactionStatus),
                        qualityId = VALUES(qualityId),
                        qualityLevel = VALUES(qualityLevel),
                        qualityStatus = VALUES(qualityStatus),
                        qualityTime = VALUES(qualityTime);
                    """
        mysqlUtil.executemany(insert_query,insert_tuple_list)
        print(len(insert_tuple_list))
    # p判断是否有下一页，如果有下一页则自动进行插入
    def auto_insert(self,authorizaation,cookie):
        response=self.send_post_request(authorizaation,cookie,0)
        current_total_count=int(response.json().get('total'))
        PageNum=current_total_count//10000
        tel_num_list=[]
        for pageNo in range(0,PageNum+1):
            response=self.send_post_request(authorizaation, cookie, pageNo)
            tel_num_list1 = self.getChat_detail_tel(response)
            insert_tuple_list=self.idct_to_tuple(response)
            self.insert_into_table(insert_tuple_list)
            tel_num_list.extend(tel_num_list1)
        return tel_num_list



if __name__ == "__main__":
    # 发送 POST 请求并打印返回结果
    authorization = "Bearer 2cc5221f-8229-4360-84df-84b8c7d03377"

    cookie='STSESSION=6388A7B8F77FC2FEB174E95C67EE84A0; SINOSESSION_ID_=87fe408070f44572a0e193e2153751cb; ha-wap-pas=c1b26a4764c38987; waparrayid=wapserv_ec_20230907_03; VALIDATE_ID=AUTH_SMS20240517MtCRZDsT02; tokenInfo=%7B%22access_token%22%3A%222cc5221f-8229-4360-84df-84b8c7d03377%22%2C%22scope%22%3A%22all%22%2C%22staff_id%22%3A%22znydadmin%22%2C%22token_type%22%3A%22bearer%22%2C%22expires_in%22%3A43199%2C%22targetUrl%22%3A%22https%3A//wap.zj.10086.cn/ai/shopkf/ucfront/index.html%22%2C%22client_id%22%3A%22ucfront%22%7D'
    getInfoList=GetInfosList()
    tell_num_list=getInfoList.auto_insert(authorizaation=authorization,cookie=cookie)
    print(len(tell_num_list))
    print(tell_num_list)



