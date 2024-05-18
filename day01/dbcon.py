import pymysql
import requests
import pymysql
import json
url = 'https://api.yingdao.com/api/console/app/queryAppUseRecordList'
headers = {
    'Authorization': access_token,
    'Content-Type': 'application/json'
}
conn = pymysql.connect(host="192.168.0.148",user="ZSD",password="Cmdc2023",database="zhelixing_data")
cursor = conn.cursor()
sql = "select * from  yindao_program_base_info"
cursor.execute(sql)
data=cursor.fetchall()
data=list(data)
runstatelist=list()
for row in data:

    uuid=row[1]
    appName=row[2]
    tel_num=row[3]
    data = {
        "page": 1,
        "size": 1,
        "appId": appName
    }
    # 发送POST请求
    response = requests.post(url, headers=headers, json=data)
    # 打印响应内容
    runstateName = (response.json()['data'][0]['runStatusName'])
    runStateRow=[appName,tel_num,runstateName]
    runstatelist.append(runStateRow)
def null_list():
    myName=list()
    print(null_list())