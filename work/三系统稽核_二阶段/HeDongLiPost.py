# 使用提醒:
# 1. xbot包提供软件自动化、数据表格、Excel、日志、AI等功能
# 2. package包提供访问当前应用数据的功能，如获取元素、访问全局变量、获取资源文件等功能
# 3. 当此模块作为流程独立运行时执行main函数
# 4. 可视化流程中可以通过"调用模块"的指令使用此模块

import json
import time
import datetime
import requests
import base64
import datetime


#  发货单下载
def get_file_Invoice(Authorization, Cookie, save_path):
    #  触发下载， 查询下载，得到 id，进行下载
    url_acctbaseinfo = 'http://admin.hedongli.com/hdlmgmtcomp/order/DeliverBase/v1.0/exportDelivers'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiLnjovpgLjmtIEiLCJtY2h0X25hbWUiOiLmtZnmsZ_nu4jnq6_lhazlj7giLCJyZWdpb25faWQiOjMzMDAwMCwib3BfaWQiOjMwODM4LCJhdXRob3JpdGllcyI6WyJST0xFX1VTRVIiXSwiY2xpZW50X2lkIjoiZjc2ZjNjZDg3NGE3NDI5YTNhZWVlNzViZmVlNDRlMjciLCJ1c2VyX3N0YXRlIjoxLCJzdXBlcl9yb2xlX2lkIjoyMTEsInByb3ZpY2VfaWQiOi0xLCJzdXBfbWNodF9pZCI6bnVsbCwibWNodF90eXBlIjoxLCJyY3ZfY291bnRyeV9pZCI6bnVsbCwidXNlcl9pZCI6MzA4MzgsInJvbGVfaWQiOiIyMTEiLCJvcmdfaWQiOjEwOTIxLCJzY29wZSI6WyJhbGwiXSwicmN2X3Byb3ZpbmNlX2lkIjozMzAwMDAsImV4cCI6MTY3OTkzMjk5Niwib3JnX25hbWUiOiLnu4jnq6_lhazlj7jmtZnmsZ_liIblhazlj7giLCJqdGkiOiI4OGI5MzZlMi05Y2U2LTQ1MmItYmM0ZC00YjFjYzdjZmU3NjAiLCJtY2h0X2lkIjoxMDc4MSwiY2l0eV9pZCI6Ii0xIiwicmN2X2NpdHlfaWQiOlstMV19.IxNvamNWhGUjm9QeCQcHzNvI7lGtJWMXvN7Pz1mfUg48-2A0chp3EXX9OkkkMxU_ZQZ-x2Q-srBroK61w3xqiU49r98NWo7SjypIl21mkmMQAzkSyFsx4be0Daeu9tUy7h3bgah57tTjCKjzFYbJRJCM8kE9tLc2Nm37sK3bX2u3waX0nbBhq7A_pAWLZyrouX3gTA85F3PqzvGC_dfPUbXt4O5k7bORS7aeiXLaPzuSuMl6JZq3bviC0Ma0f3OBTZR-ymjdtAS-1X7Z5oKSl-D5qrfQpA3M_FyDmRfYlEnD40txg5TIq_NHEheso4B4YWybZSOWY5UCbMf_XU9PpA',
        'Authorization': Authorization,
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '165',
        'Content-Type': 'application/json',
        # 'Cookie': 'JSESSIONID=B141239B4651AA9CCB39BC3458B04A24; Hm_lvt_43d60ebe530b59b32819870ba2eebcdf=1679903229; Hm_lpvt_43d60ebe530b59b32819870ba2eebcdf=1679903229',
        'Cookie': Cookie,
        'Host': 'admin.hedongli.com',
        'Origin': 'http://admin.hedongli.com',
        'Pragma': 'no-cache',
        'Referer': 'http://admin.hedongli.com/',
        # 'token': 'c03fe461cb1cad2cec126fe62ee2ec36',
        'token': '',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }
    now = datetime.datetime.now()
    today = str(now.date())

    today2 = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = str(today2 - oneday)
    # data = {"mchtType":1,"deliverGoodsState":20,"mchtId":10781,"orderTimeRange":["",""],"TimeRange":[f"{today} 00:00:00",f"{today} 23:59:59"],"createTimeFrom":f"{today} 00:00:00","createTimeTo":f"{today} 23:59:59","outerTimeRange":[],"loginOperator":"王帅","loginOperatorId":13966,"page":{"pageNum":1,"pageSize":10},"lctnProvinceId":"330000"}
    data = {"mchtType": 1, "deliverGoodsState": 20, "mchtId": 10781, "orderTimeRange": 'null',
            "TimeRange": [f"{today} 00:00:00", f"{today} 23:59:59"], "createTimeFrom": f"{today} 00:00:00",
            "createTimeTo": f"{today} 23:59:59", "outerTimeRange": [], "loginOperator": "王帅",
            "loginOperatorId": 28434, "page": {"pageNum": 1, "pageSize": 10}, "lctnProvinceId": "330000"}
    data = json.dumps(data)
    # response = ''
    try:
        response = requests.post(url_acctbaseinfo, headers=headers, data=data, timeout=30)
        response_json = response.json()
    except Exception as e:
        time.sleep(3)
        response = requests.post(url_acctbaseinfo, headers=headers, data=data, timeout=30)
        response_json = response.json()
    # response = requests.post(url_acctbaseinfo, headers=headers, data=data, timeout=60)
    # response_json = response.json()

    state = response_json['resultMessage']
    if state == '操作成功':  # 触发下载成功，则进入文件导出列表接口等候处理成功，进行下载
        print('触发 查询下载 成功！！！！！！')
        time.sleep(2)
        url_query_export_list = 'http://admin.hedongli.com/hdlmgmtcomp/mgmt/common/v1.0/queryExportTask'  # 文件导出状态列表
        # data = {"applyid":13966,"timeData":["2023-03-29",f"{today}"],"beginTimeStr":"2023-03-29","endTimeStr":f"{today}","page":{"pageNum":1,"pageSize":10},"lctnProvinceId":"330000"} 朱玉杰
        data = {"applyid": 28434, "timeData": ["2023-04-30", f"{today}"], "beginTimeStr": "2023-04-30",
                "endTimeStr": f"{today}", "page": {"pageNum": 1, "pageSize": 10}, "lctnProvinceId": "330000"}
        # data = {"applyid":30838,"timeData":["2023-02-25",f"{today}"],"beginTimeStr":"2023-02-25","endTimeStr":f"{today}","page":{"pageNum":1,"pageSize":10},"lctnProvinceId":"330000"}
        data = json.dumps(data)
        latest_id_first = -1  # 处理中 id
        num = 1
        flag = False
        while num < 61:  # 最多循环访问接口 30 次, 一次间隔一分钟
            print(f'查询文件导出列表{num}次')
            try:
                response = requests.post(url_query_export_list, headers=headers, data=data, timeout=30)
                response = response.json()
            except Exception as e:
                time.sleep(2)
                print(e)
                continue

            if response['resultMessage'] == '操作成功':
                print('查询文件导出列表成功！！！！！！')
                task_list = response['result']['pageData']
                for item in task_list:  # 查找指定人最近的一次处理中的指定文件
                    id = item['id']
                    name = item['applyname']  # 王帅
                    exportType = item['exportType']  # 3 为发货单导出
                    exportState = item['exportState']  # 1 为处理中， 2 为处理成功
                    # list {'id': 131608, 'exportCode': 131608, 'exportType': 3, 'fileName': 'deliver-20230327141453861.xlsx', 'exportState': 2, 'exportBeginTime': '2023-03-27 14:14:36', 'exportEndTime': '2023-03-27 14:14:53', 'applyid': 30838, 'applyname': '王逸洁'}
                    if name == '王帅' and exportType == 3 and exportState == 1:  # 判断指定人文件且为处理中地指定文件
                        latest_id_first = id
                        # flag = True
                        break
                    if latest_id_first == id and name == '王帅' and exportType == 3 and exportState == 2:  # 判断指定人文件且为处理成功地指定文件
                        flag = True  # 文件处理成功标记
                        print('处理成功！！！！！！')
                        break
                    if latest_id_first == id and name == '王帅' and exportType == 3 and exportState == 3:  # 判断指定人文件且为处理成功地指定文件
                        return 'faile'
                print(task_list)
                print('latest_id_first: ', latest_id_first)
            else:
                reason = response['resultMessage']
                print(f'查询文件导出列表失败：{reason}')
                break
            if flag:  # 导出文件成功，则下载文件
                try:
                    url_export = 'http://admin.hedongli.com/hdlmgmtcomp/mgmt/common/v1.0/downloadExportTask'  # 通过 id 导出文件
                    data = {"id": latest_id_first, "lctnProvinceId": "330000"}
                    data = json.dumps(data)
                    response_download_file = requests.post(url_export, headers=headers, data=data, timeout=30)
                    print('下载文件：', response_download_file.status_code)
                    # file_path = save_path + '\\' + f'{today}发货单.xlsx'
                    with open(save_path, 'wb') as f:
                        f.write(response_download_file.content)
                    print('发货单下载成功！！！！！！')
                    break
                except Exception as reason:
                    print(f'下载文件失败：{reason}')
                    break
            time.sleep(120)
            num += 1


# 订单总览下载
def get_file_Order_Review(Authorization, Cookie, save_path):
    #  触发下载， 查询下载，得到 id，进行下载
    url_acctbaseinfo = 'http://admin.hedongli.com/hdlmgmtcomp/order/DeliverBase/v1.0/exportDelivers'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiLnjovpgLjmtIEiLCJtY2h0X25hbWUiOiLmtZnmsZ_nu4jnq6_lhazlj7giLCJyZWdpb25faWQiOjMzMDAwMCwib3BfaWQiOjMwODM4LCJhdXRob3JpdGllcyI6WyJST0xFX1VTRVIiXSwiY2xpZW50X2lkIjoiZjc2ZjNjZDg3NGE3NDI5YTNhZWVlNzViZmVlNDRlMjciLCJ1c2VyX3N0YXRlIjoxLCJzdXBlcl9yb2xlX2lkIjoyMTEsInByb3ZpY2VfaWQiOi0xLCJzdXBfbWNodF9pZCI6bnVsbCwibWNodF90eXBlIjoxLCJyY3ZfY291bnRyeV9pZCI6bnVsbCwidXNlcl9pZCI6MzA4MzgsInJvbGVfaWQiOiIyMTEiLCJvcmdfaWQiOjEwOTIxLCJzY29wZSI6WyJhbGwiXSwicmN2X3Byb3ZpbmNlX2lkIjozMzAwMDAsImV4cCI6MTY3OTkzMjk5Niwib3JnX25hbWUiOiLnu4jnq6_lhazlj7jmtZnmsZ_liIblhazlj7giLCJqdGkiOiI4OGI5MzZlMi05Y2U2LTQ1MmItYmM0ZC00YjFjYzdjZmU3NjAiLCJtY2h0X2lkIjoxMDc4MSwiY2l0eV9pZCI6Ii0xIiwicmN2X2NpdHlfaWQiOlstMV19.IxNvamNWhGUjm9QeCQcHzNvI7lGtJWMXvN7Pz1mfUg48-2A0chp3EXX9OkkkMxU_ZQZ-x2Q-srBroK61w3xqiU49r98NWo7SjypIl21mkmMQAzkSyFsx4be0Daeu9tUy7h3bgah57tTjCKjzFYbJRJCM8kE9tLc2Nm37sK3bX2u3waX0nbBhq7A_pAWLZyrouX3gTA85F3PqzvGC_dfPUbXt4O5k7bORS7aeiXLaPzuSuMl6JZq3bviC0Ma0f3OBTZR-ymjdtAS-1X7Z5oKSl-D5qrfQpA3M_FyDmRfYlEnD40txg5TIq_NHEheso4B4YWybZSOWY5UCbMf_XU9PpA',
        'Authorization': Authorization,
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '165',
        'Content-Type': 'application/json',
        # 'Cookie': 'JSESSIONID=B141239B4651AA9CCB39BC3458B04A24; Hm_lvt_43d60ebe530b59b32819870ba2eebcdf=1679903229; Hm_lpvt_43d60ebe530b59b32819870ba2eebcdf=1679903229',
        'Cookie': Cookie,
        'Host': 'admin.hedongli.com',
        'Origin': 'http://admin.hedongli.com',
        'Pragma': 'no-cache',
        'Referer': 'http://admin.hedongli.com/',
        # 'token': 'c03fe461cb1cad2cec126fe62ee2ec36',
        'token': '',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }
    now = datetime.datetime.now()
    today = str(now.date())

    today2 = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = str(today2 - oneday)

    # data = {"mchtId":10781,"mchtType":1,"orderTimeRange":["2023-03-29 00:00:00",f"{today} 23:59:59"],"orderStartTime":"2023-03-29 00:00:00","orderEndTime":f"{today} 23:59:59","orderTime":[f"{today} 00:00:00",f"{today} 23:59:59"],"endTime":f"{today} 23:59:59","startTime":f"{today} 00:00:00","loginOperator":"王帅","loginOperatorId":13966,"dealerProvinceId":330000,"page":{"pageNum":1,"pageSize":10},"lctnProvinceId":"330000"} 朱玉杰
    data = {"mchtId": 10781, "mchtType": 1, "orderTimeRange": ["2023-04-30 00:00:00", f"{today} 23:59:59"],
            "orderStartTime": "2023-04-30 00:00:00", "orderEndTime": f"{today} 23:59:59",
            "orderTime": [f"{today} 00:00:00", f"{today} 23:59:59"], "endTime": f"{today} 23:59:59",
            "startTime": f"{today} 00:00:00", "loginOperator": "王帅", "loginOperatorId": 28434,
            "dealerProvinceId": 330000, "page": {"pageNum": 1, "pageSize": 10}, "lctnProvinceId": "330000"}
    data = json.dumps(data)
    response = ''
    url_Order_Review = 'http://admin.hedongli.com/hdlmgmtcomp/order/queryOrder/v1.0/orderExport'
    try:
        response = requests.post(url_Order_Review, headers=headers, data=data, timeout=30)
        response_json = response.json()
    except Exception as e:
        time.sleep(3)
        print(e)
        response = requests.post(url_Order_Review, headers=headers, data=data, timeout=30)
        response_json = response.json()
    # response = requests.post(url_Order_Review, headers=headers, data=data, timeout=30)
    # response_json = response.json()
    state = response_json['resultMessage']

    if state == '操作成功':
        print('订单总览触发下载成功！！！')
    else:
        print('订单总览触发下载异常：', state)

    ############################################################################################################################################################################
    if state == '操作成功':  # 触发下载成功，则进入文件导出列表接口等候处理成功，进行下载
        print('触发 查询下载 成功！！！！！！')
        time.sleep(2)
        url_query_export_list = 'http://admin.hedongli.com/hdlmgmtcomp/mgmt/common/v1.0/queryExportTask'  # 文件导出状态列表
        # data = {"applyid":13966,"timeData":["2023-03-29",f"{today}"],"beginTimeStr":"2023-03-29","endTimeStr":f"{today}","page":{"pageNum":1,"pageSize":10},"lctnProvinceId":"330000"}  朱玉杰
        data = {"applyid": 28434, "timeData": ["2023-04-30", f"{today}"], "beginTimeStr": "2023-04-30",
                "endTimeStr": f"{today}", "page": {"pageNum": 1, "pageSize": 10}, "lctnProvinceId": "330000"}
        data = json.dumps(data)
        latest_id_first = -1  # 处理中 id
        num = 1
        flag = False
        while num < 61:  # 最多循环访问接口 30 次, 一次间隔一分钟
            print(f'查询订单总览文件导出列表{num}次')
            try:
                response = requests.post(url_query_export_list, headers=headers, data=data, timeout=30)
                response = response.json()
            except Exception as e:
                time.sleep(2)
                print(e)
                continue
            if response['resultMessage'] == '操作成功':
                print('查询订单总览文件导出列表成功！！！！！！')
                task_list = response['result']['pageData']
                for item in task_list:  # 查找指定人最近的一次处理中的指定文件
                    id = item['id']
                    name = item['applyname']  # 王帅
                    exportType = item['exportType']  # 3 为发货单导出
                    exportState = item['exportState']  # 1 为处理中， 2 为处理成功
                    # list {'id': 131608, 'exportCode': 131608, 'exportType': 3, 'fileName': 'deliver-20230327141453861.xlsx', 'exportState': 2, 'exportBeginTime': '2023-03-27 14:14:36', 'exportEndTime': '2023-03-27 14:14:53', 'applyid': 30838, 'applyname': '王逸洁'}
                    if name == '王帅' and exportType == 2 and exportState == 1:  # 判断指定人文件且为处理中地指定文件
                        latest_id_first = id
                        # flag = True
                        break
                    if latest_id_first == id and name == '王帅' and exportType == 2 and exportState == 2:  # 判断指定人文件且为处理成功地指定文件
                        flag = True  # 文件处理成功标记
                        print('处理成功！！！！！！')
                        break
                    if latest_id_first == id and name == '王帅' and exportType == 2 and exportState == 3:  # 判断指定人文件且为处理成功地指定文件
                        return 'faile'
                print(task_list)
                print('latest_id_first: ', latest_id_first)
            else:
                reason = response['resultMessage']
                print(f'查询订单总览文件导出列表失败：{reason}')
                break
            if flag:  # 导出文件成功，则下载文件
                try:
                    url_export = 'http://admin.hedongli.com/hdlmgmtcomp/mgmt/common/v1.0/downloadExportTask'  # 通过 id 导出文件
                    data = {"id": latest_id_first, "lctnProvinceId": "330000"}
                    data = json.dumps(data)
                    response_download_file = requests.post(url_export, headers=headers, data=data, timeout=30)
                    print('下载文件：', response_download_file.status_code)
                    # file_path = save_path + '\\' + f'{today}订单总览.xlsx'
                    with open(save_path, 'wb') as f:
                        f.write(response_download_file.content)
                    print('订单总览下载成功！！！！！！')
                    break
                except Exception as reason:
                    print(f'订单总览下载失败：{reason}')
                    break
            time.sleep(120)
            num += 1

# auth = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiLnjovluIUiLCJtY2h0X25hbWUiOiLmtZnmsZ_nu4jnq6_lhazlj7giLCJyZWdpb25faWQiOjMzMDAwMCwib3BfaWQiOjI4NDM0LCJhdXRob3JpdGllcyI6WyJST0xFX1VTRVIiXSwiY2xpZW50X2lkIjoiZjc2ZjNjZDg3NGE3NDI5YTNhZWVlNzViZmVlNDRlMjciLCJ1c2VyX3N0YXRlIjoxLCJzdXBlcl9yb2xlX2lkIjoyMTEsInByb3ZpY2VfaWQiOi0xLCJzdXBfbWNodF9pZCI6bnVsbCwibWNodF90eXBlIjoxLCJyY3ZfY291bnRyeV9pZCI6bnVsbCwidXNlcl9pZCI6Mjg0MzQsInJvbGVfaWQiOiIyMTEiLCJvcmdfaWQiOjEwOTIxLCJzY29wZSI6WyJhbGwiXSwicmN2X3Byb3ZpbmNlX2lkIjozMzAwMDAsImV4cCI6MTY4NTk2NDc3OCwib3JnX25hbWUiOiLnu4jnq6_lhazlj7jmtZnmsZ_liIblhazlj7giLCJqdGkiOiIyZmM3NDJiMi1lM2FhLTRjZjItYTNmMi01M2NkZDNjMWIwMmUiLCJtY2h0X2lkIjoxMDc4MSwiY2l0eV9pZCI6Ii0xIiwicmN2X2NpdHlfaWQiOlstMV19.j2N1IFXCHDpr95dWVq-mFxhUhh09vg-dyrM3sP8M9-syKrTPjY9BAuh8-hD0HiB9vFfwLZybu9F0mvQXAZqsIjvPaYcZGB10jGx39u_R9J_-srYtyEbg77YqINxMvXqhFi6a9GND54xlyIbhuKJvciAK5SGlPKR7RDnBCz1NsTKbPwOnNUaywgAFSRotC-jDGfwwQG1576xFI515dsT6d8YOsn_ijXrSFKfdPkbzJgtsmgxSyK88ey038XTAJNNs-RPmaLDQcauDZONU_GS1mfXkMj6_kOkJ_CYm5L7hscK0kARGdg1IQOzSlsqPZ56P7HnGUN0sUotbAmcpCFF9_g'
# cokie = 'JSESSIONID=B3D5EAE7C4AD67F552C09083E330FE80; Hm_lvt_43d60ebe530b59b32819870ba2eebcdf=1685698961,1685950332; Hm_lpvt_43d60ebe530b59b32819870ba2eebcdf=1685953934'
# fh = './0605发货单.xlsx'
# zl = './0605订单总览.xlsx'
# get_file_Invoice(auth, cokie, fh)
# get_file_Order_Review(auth, cokie, zl)
