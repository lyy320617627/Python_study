import requests
import json
from datetime import datetime, timedelta
import re
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from MySQLUtil import MySQLUtil
from GetKeFuChatInfosList import GetInfosList
def convert_to_str_if_not_empty(value):
    return str(value) if value else None
class GetChatDetailInfo:
    # 发送请求
    def send_post_request( self, cookie,tel_num):
        url="https://wap.zj.10086.cn/ai/shopkf/log/chatlog/searchChatLog"
        headers={
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': cookie,
            'Referer': 'https://wap.zj.10086.cn/ai/shopkf/ucfront/log/html/qrySession.html',
            # 'Authorization': authorization
        }
        data={
                "agentId": "undefined",
                "customer": "18758255905",
                "desc": "true",
                "pageNum": 0,
                "pageSize": 10000,
                "tenantId": "ff8080826537c4fc016538bd3b010089"
            }
        try:
            response = requests.post(url=url, headers=headers, data=json.dumps(data))
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
    def get_chat_detail_info(self,response):
        if response is None:  # 检查响应对象是否为 None
            print("Response is None")
            return []  # 如果响应对象为 None，则返回空列表
        # 文本替换，把content内容中含有所有的网页标签全部去除掉
        response=response.json()
        for item in response:
            text=urllib.parse.unquote(item['content'])
            if text.find("message") != -1 or text.find(""):
                text=text.split(":")[1]
            else:
                text=text
            soup = BeautifulSoup(text, 'html.parser')
            text=soup.get_text()
            print(text)
            item['content'] = text
        # print(response)
        if response is None:
            return []
        else:
            return response
    def get_insert_tuple_list(self,response_list):
        insert_tuple_list=[]
        for item in response_list:
            insert_tuple_list.append(
                (convert_to_str_if_not_empty(item.get('uuId')),
                 convert_to_str_if_not_empty(item.get('chatId')),
                 convert_to_str_if_not_empty(item.get('tenantId')),
                 convert_to_str_if_not_empty(item.get('content')),
                 convert_to_str_if_not_empty(item.get('icon')),
                 convert_to_str_if_not_empty(item.get('flag')),
                 convert_to_str_if_not_empty(item.get('username')),
                 int(item['timestamp']) if item.get('timestamp') is not None else None,
                 # convert_to_str_if_not_empty(item.get('timestamp')),

                 # bool(item.get('mine')) if item.get('mine') is not True else False,
                 # bool(item.get('play')) if item.get('play') is not True else False,
                 # bool(item.get('read')) if item.get('read') is not True else False,
            ))
        print(insert_tuple_list)
        return insert_tuple_list

    def insert_into_table(self,insert_tuple_list):
        mysqlUtil = MySQLUtil(host="172.16.8.241", user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
        insert_sql = """
        INSERT INTO kf_chat_detail_info (uuId, chatId, tenantId, content, icon, flag, username, timestamp1)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                ON DUPLICATE KEY UPDATE
                                chatId = VALUES(chatId),
                                tenantId = VALUES(tenantId),
                                content = VALUES(content),
                                icon = VALUES(icon),
                                flag = VALUES(flag),
                                username = VALUES(username),
                                timestamp1 = VALUES(timestamp1)
        """
        mysqlUtil.executemany(insert_sql, insert_tuple_list)
        # 聊天记录自动插入
    def auto_insert_into_chat_detail(self,cookie,tell_num_list):
        insert_tuple_list=[]
        for tel_num in tell_num_list:
            response=self.send_post_request(cookie,tel_num)
            response=self.get_chat_detail_info(response)
            insert_tuple_list_temp=self.get_insert_tuple_list(response)
            insert_tuple_list.extend(insert_tuple_list_temp)
            self.insert_into_table(insert_tuple_list_temp)
        return insert_tuple_list





if __name__ == '__main__':
    # 发送 POST 请求并打印返回结果
    authorization = "Bearer 2cc5221f-8229-4360-84df-84b8c7d03377"

    cookie = 'STSESSION=6388A7B8F77FC2FEB174E95C67EE84A0; SINOSESSION_ID_=87fe408070f44572a0e193e2153751cb; ha-wap-pas=c1b26a4764c38987; waparrayid=wapserv_ec_20230907_03; VALIDATE_ID=AUTH_SMS20240517MtCRZDsT02; tokenInfo=%7B%22access_token%22%3A%222cc5221f-8229-4360-84df-84b8c7d03377%22%2C%22scope%22%3A%22all%22%2C%22staff_id%22%3A%22znydadmin%22%2C%22token_type%22%3A%22bearer%22%2C%22expires_in%22%3A43199%2C%22targetUrl%22%3A%22https%3A//wap.zj.10086.cn/ai/shopkf/ucfront/index.html%22%2C%22client_id%22%3A%22ucfront%22%7D'
    getInfoList = GetInfosList()
    tell_num_list = getInfoList.auto_insert(authorizaation=authorization, cookie=cookie)
    print(len(tell_num_list))
    print(tell_num_list)
    getDetail=GetChatDetailInfo()
    insert_tuple_list=getDetail.auto_insert_into_chat_detail(cookie, tell_num_list)
    print(insert_tuple_list)
    print(len(insert_tuple_list))



