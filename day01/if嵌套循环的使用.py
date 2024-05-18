"""
通过if嵌套循环的使用
来判断条件是否符合
"""
import pymysql
import requests
age=int(input("请输入你的年龄\n"))
vip_level=int(input("请输入你的vip级别:(1~5)\n"))
if age >13:
    print("你的年龄已经大于13")
    print("如果你的vip级别大于3,也可以免费游玩，请输入你的vip级别")
    if vip_level>=3:
        print("你的vip级别大于3")
        print("你可以免费游玩")
    else:
        print("不好意思，你需要补票10元")
print("祝你游玩愉快")
# --------------------------------------------------------------
#--------------------------------------------------------------------
url = 'https://api.yingdao.com/api/console/app/queryAppUseRecordList'
headers = {
    'Authorization': access_token,
    'Content-Type': 'application/json'
}
conn = pymysql.connect(host="192.168.0.148", user="ZSD", password="Cmdc2023", database="zhelixing_data")
cursor = conn.cursor()
sql = "select * from  yindao_program_base_info"
cursor.execute(sql)
data = cursor.fetchall()
conn.close()
data = list(data)
program_list = []
for row in data:
    uuid = row[1]
    appName = row[2]
    tel_num = row[4]
    data = {
        "page": 1,
        "size": 1,
        "appId": appName
    }
    data = {
        "page": 1,
        "size": 1,
        "appId": uuid
    }
    response = requests.post(url, headers=headers, json=data)
    runstateName = (response.json()['data'][0]['runStatusName'])
    if runstateName != "运行中":
        row_list = [appName, tel_num, runstateName]
        program_list.append(row_list)

