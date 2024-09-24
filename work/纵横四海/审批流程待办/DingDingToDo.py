import requests
import json
from MySQLUtil import MySQLUtil
from decimal import Decimal
def get_access_token(app_key, app_secret):
    url = "https://api.dingtalk.com/v1.0/oauth2/accessToken"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "appKey": app_key,
        "appSecret": app_secret
    }
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    if "accessToken" in result:
        return result["accessToken"]
    else:
        raise Exception(f"Error getting access token: {result.get('errmsg')}")


def start_process_instance(access_token, form_data):
    url = "https://api.dingtalk.com/v1.0/yida/processes/instances/start"
    headers = {
        "x-acs-dingtalk-access-token": access_token,
        "Content-Type": "application/json"
    }
    data = {
        "appType": "APP_JZPKU34KB64WUGDVUDB8",
        "systemToken": "K766647133IMK5GS7685R59GEXP22W8RXG5YL04",
        "userId":"01036168441812848521",
        "formUuid": "FORM-AF5DC139BBF040709F1E5EDF174452974N4Q",
        "formDataJson": json.dumps(form_data),  # Ensure form_data is a JSON string
        "processCode": "TPROC--ZKC66Y61UPIMY0HPACP0045BJ8D53J54AI5YL1",
    }
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    result=result['result']
    return result
def convert_decimal_to_string(data):
    # 遍历每一行
    for row in data:
        # 遍历每一列
        for i in range(len(row)):
            # 如果该列的值是Decimal类型，则转换为字符串
            if isinstance(row[i], Decimal):
                row[i] = str(row[i])
    return data

if __name__ == '__main__':
    app_key = "dingc8wtmaib95vi3ifz"
    app_secret = "XR4vKpX7Wt4iLK2WE-1IbI_THLwaynDYC6Be0j0j9Fl3e_ev39P9WRu_Fin4GhFt"
    access_token = get_access_token(app_key, app_secret)
    print(f"从钉钉后台获取到的access_token：{access_token}")
    # 从数据库中筛选条件并且在循环中每次查询出对应联系人的userId，然后循环调用接口去发送流程待办功能
    conn2 = MySQLUtil(host="192.168.0.148", port=3306, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
    sql="SELECT billDate, displayName, purResultCode, title, stateName, purchaseAmountTag, diff_days, safeDays, line,isCaution FROM  bs_pur_purchase_result_bill WHERE  (  purchaseAmountTag = '9000万及以上' AND safeDays - diff_days < 2  ) AND stateName = '已完结';"
    data=conn2.execute(sql)
    print(f"从数据库中筛选出来的数据为:{data}")
    print(f"从数据库中筛选出来的数据类型为:{type(data)}")
    print(f"从数据库中筛选出来的数据长度为:{len(data)}")
    # 使用列表推导式转换为二维列表
    data_list = [list(row) for row in data]
    print(f"转换后的元组数据类型为:{type(data_list)}")
    print(f"转换后的元组数据的长度为:{len(data_list)}")
    target_list = convert_decimal_to_string(data_list)
    target_list = target_list[:1]
    userid = "500159250026261710"
    print(target_list)
    for data in target_list:
        try:
            bs_username_unionId_dataList=conn2.select("bs_userName_unionId","name",str(data[1]))
            print(f"{data[1]}从数据中查找联系人返回的结果为:{bs_username_unionId_dataList}")
            if len(bs_username_unionId_dataList) ==0:
                userId=""
            else:
                userIdList=convert_decimal_to_string(bs_username_unionId_dataList)
                print(f"userIdList:{userIdList}")
                userId=bs_username_unionId_dataList[0][-2]
        except Exception as e:
            print(f"从数据库中查询联系人时出错：{e}")
            raise
        print(f"{data[1]}对应的userId为{userId}")
        form_data = {
            "textField_7khh170": str(data[2]),
            "textField_1g3v05k": str(data[3]),
            "textField_hml7egp": str(data[4]),
            "textField_fkap1yo": str(data[5]),
            "textField_60ya0m6": str(data[6]),
            "textField_92n4lql": str(data[7]),
            "textField_tb95x91": str(data[8]),
            "textField_lyfn86i9":str(data[9]),
            "textareaField_ly5iixf8": "",
            'employeeField_ly5mjfs4':'010423174810253075194'
        }
        result = start_process_instance(access_token, form_data)
        print("审批流程发起结果:", result)
