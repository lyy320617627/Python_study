import pymysql
import requests
import json
from xbot import print
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
program_list=[]
for row in data:

    uuid=row[1]
    appName=row[2]
    tel_num=row[4]
    data = {
        "page": 1,
        "size": 1,
        "appId": appName
    }
    data = {
        "page": 1,
        "size": 1,
        "appId":uuid
    }
    response = requests.post(url, headers=headers, json=data)
    runstateName = (response.json()['data'][0]['runStatusName'])
    if runstateName!='运行中':
        program_list.append(appName,tel_num)