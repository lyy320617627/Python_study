import  pandas as pd
from  MySQLUtil import  MySQLUtil

import requests, json
class SendMessage:
    # def DownLoadFile(self,file_path):
    #     conn = MySQLUtil(host="192.168.0.148", port=3306, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
    #     data=conn.select_all("bs_historical_of_equity_settle")
    #     print(f"从数据库中下载的数据长度为:{len(data)}")
    #     print(f"从数据库中下载的数据类型是:{type(data)}")
    #     data=pd.DataFrame(list(data))
    #     print(f"data数据转成list类型之后的数据长度是:{len(data)}")
    #     data.columns = ["IMEI", "办理月份", "稽核标记", "结算金额", "客户编码", "客户名称", "品牌", "物料编码",
    #                     "物料描述", "类型", "业务类型"]
    #     data.to_excel(file_path, index=False)

    def send_message(self,file_path1):
        # 1.获取接口凭证
        def getAccess_token():
            # 从小程序应用信息处获取
            appkey = 'dingc8wtmaib95vi3ifz'  # 不要配置服务器ip
            appsecret = 'XR4vKpX7Wt4iLK2WE-1IbI_THLwaynDYC6Be0j0j9Fl3e_ev39P9WRu_Fin4GhFt'  # 不要配置服务器ip

            url = 'https://oapi.dingtalk.com/gettoken?appkey=%s&appsecret=%s' % (appkey, appsecret)

            headers = {
                'Content-Type': "application/x-www-form-urlencoded"
            }
            data = {'appkey': appkey,
                    'appsecret': appsecret}
            r = requests.request('GET', url, data=data, headers=headers)
            access_token = r.json()["access_token"]

            return access_token

        # 2.获取Midia_id
        def getMedia_id(file_path):
            access_token = getAccess_token()
            # 本地文件的绝对路径
            url = r'https://oapi.dingtalk.com/media/upload?access_token=%s&type=file' % access_token
            files = {'media': open(file_path, 'rb')}
            data = {'access_token': access_token,
                    'type': 'file'}
            response = requests.post(url, files=files, data=data)
            json = response.json()
            print('response:', json)
            if 'media_id' in json:
                return json['media_id']
            else:
                raise Exception("钉钉上传文件失败：", json)
            # print(json["media_id"])
            return json['media_id']

        # 3.文件发送
        def SendFile():
            try:
                access_token = getAccess_token()

                # 循环获取指定列表文件，发送指定钉钉群聊

                file_path = file_path1
                # file_path=r"C:\Users\RPA1-1\Desktop\OAO自动生成通报表格\固定表格模板.xlsx"

                print(file_path)
                # 将文件名传给getMedia_id
                media_id = getMedia_id(file_path)
                print(f'media_id:{media_id}')
                # 获取群聊Id
                chatid = 'chat6a75f4d1da3ad6d5cf04a6dac543804c'
                url = 'https://oapi.dingtalk.com/chat/send?access_token=' + access_token
                header = {
                    'Content-Type': 'application/json'
                }
                data = {'access_token': access_token,
                        'chatid': chatid,
                        'msg': {
                            'msgtype': 'file',
                            'file': {'media_id': media_id}
                        }
                        }
                r = requests.request('POST', url, data=json.dumps(data), headers=header)
                print(r.json())
                print('发送成功')
            except Exception as e:
                print("发生异常：", str(e))
                raise

        SendFile()



if __name__ == '__main__':
    file_path=r'C:\Users\ly320\Desktop\权益类结算历史数据.xlsx'
    sendMessage=SendMessage()
    sendMessage.DownLoadFile(file_path)
    sendMessage.send_message(file_path)
