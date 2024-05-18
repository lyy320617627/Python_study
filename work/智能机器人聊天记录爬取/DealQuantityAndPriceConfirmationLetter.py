# coding=UTF-8
from GetQuantityAndPriceConfirmationLetterInfos import GetInfos
from GetQuantityAndPriceConfirmationLetterInfo import GetDetail
from MySQLUtil import MySQLUtil
import time
from ActLog import ActLog

class DealQuantityAndPriceConfirmationLetter:
    def __init__(self):
        pass

    def deal(self,pages=10,authorization=None):
        #发送 POST 请求并打印返回结果
        result_list = []
        #1 取10页。
        getInfos = GetInfos()
        for num in range(0,pages):
            num = num+1
            pageList = getInfos.send_post_request(authorization,num)
            # 移除每行中第五个元素等于 "草稿" 的行
            pageList = [row for row in pageList if list(row)[10] != "草稿中"]

            result_list.extend(pageList)

        mysqlUtil = MySQLUtil(host="172.16.8.241", user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
        #只取昨天的数据。如果该页数据由小于10条数据的，则停止循环
        #目前发现编号的日期，有可能滞后展示。他是根据提交审批来控制是否展示的。比如编号是昨天的，有可能在今天展示出来
        #简单暴力，取n页的数据，直接插入/更新表数据。

        insert_list = result_list
        product_list = []
        #插入新元素
        getDetail = GetDetail()
        actLog = ActLog()
        if insert_list:
            for item in insert_list:
                id = item[0]
                docNum = item[4]
                status = item[10]
                #详情页
                response = getDetail.send_get_request(authorization,id)
                #审批结果数据
                log_response = actLog.send_post_request(authorization,id,docNum)

                purchaseResultCode = getDetail.get_purchaseResultCode(response)
                prcId = getDetail.get_prcId(response)
                pnrId = getDetail.get_pnrId(response)
                purchaseResultTitle = getDetail.get_purchaseResultTitle(response)
                contractCode = getDetail.get_contractCode(response)
                businessType = getDetail.get_businessType(response,authorization,log_response)
                item[16] = purchaseResultCode
                item[17] = prcId
                item[18] = pnrId
                item[19] = purchaseResultTitle
                item[20] = contractCode
                item[21] = businessType
                #获取审批完成时间
                if status== '已完成':
                    size = len(log_response['data'])
                    approvedDate =log_response['data'][size-1]['completeDate']
                    item[22] = approvedDate
                #获取量价函明细内的产品列表
                tmpProductList = getDetail.get_productList(response)
                array_list = [[value for value in item.values()] for item in tmpProductList]

                if tmpProductList:
                    product_list.extend(array_list)
            # 插入数据库
            # print(insert_list)
            # print(product_list)
            try:
                self.insertOrUpdateLetterDetail(insert_list)
                #写入产品表
                if product_list:
                    self.insertOrUpdateLetterDetailProduct(product_list)
            except ValueError:
                print(ValueError)
                raise#往上继续抛出
        result = f"dps量价函：插入or更新条数：{len(insert_list)};产品列表：插入or更新条数：{len(product_list)}"
        return result

    def insertOrUpdateLetterDetail(self,dataList):
        mysqlUtil = MySQLUtil(host="172.16.8.241", user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
        # 使用INSERT ON DUPLICATE KEY UPDATE插入或更新数据
        insert_query = """
            INSERT INTO dps_quan_price_confirm_letter 
            (id, confirmTitle, vendorId, vendorName, confirmCode, applyCompanyId, applyCompanyName, applyDate, applyUserId, applyUserName, 
            status, quoteDate, createDate, productNameStr, sumTargetPurchaseQuantity, sumTargetPurchaseAmount, purchaseResultCode, 
            prcId, pnrId, purchaseResultTitle, contractCode, businessType,approvedDate) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            confirmTitle = VALUES(confirmTitle), vendorId = VALUES(vendorId), vendorName = VALUES(vendorName), confirmCode = VALUES(confirmCode),
            applyCompanyId = VALUES(applyCompanyId), applyCompanyName = VALUES(applyCompanyName), applyDate = VALUES(applyDate),
            applyUserId = VALUES(applyUserId), applyUserName = VALUES(applyUserName), status = VALUES(status), quoteDate = VALUES(quoteDate),
            createDate = VALUES(createDate), productNameStr = VALUES(productNameStr), sumTargetPurchaseQuantity = VALUES(sumTargetPurchaseQuantity),
            sumTargetPurchaseAmount = VALUES(sumTargetPurchaseAmount), purchaseResultCode = VALUES(purchaseResultCode), prcId = VALUES(prcId),
            pnrId = VALUES(pnrId), purchaseResultTitle = VALUES(purchaseResultTitle), contractCode = VALUES(contractCode), businessType = VALUES(businessType),
            approvedDate = VALUES(approvedDate);
        """
        mysqlUtil.executemany(insert_query,dataList)

    def insertOrUpdateLetterDetailProduct(self,dataList):
        mysqlUtil = MySQLUtil(host="172.16.8.241", user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
        # 使用INSERT ON DUPLICATE KEY UPDATE插入或更新数据
        insert_query = """
        INSERT INTO dps_quan_price_confirm_letter_product 
        (id, priceConfirmLetterId, productCode, spuId, productName, brand, targetProfitRate, estimateProfitRate) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) 
        ON DUPLICATE KEY UPDATE 
        priceConfirmLetterId = VALUES(priceConfirmLetterId), 
        productCode = VALUES(productCode), 
        spuId = VALUES(spuId), 
        productName = VALUES(productName), 
        brand = VALUES(brand), 
        targetProfitRate = VALUES(targetProfitRate), 
        estimateProfitRate = VALUES(estimateProfitRate);
        """
        mysqlUtil.executemany(insert_query,dataList)

    def updateApproveInfo(self,mysqlUtil,id,stateName):

        sql = f'''
                update dps_quan_price_confirm_letter set status='{stateName}'  where id={id} and status<>'{stateName}'
                '''
        # print(sql)
        result = mysqlUtil.execute(sql)
        return result

if __name__ == "__main__":
    # print(f"当前时间："+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
    dealProgram = DealQuantityAndPriceConfirmationLetter()
    auth = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZW5hbnRfaWQiOjQsImNlbnRyYWxfZmxhZyI6Ik4iLCJ1c2VyX25hbWUiOiLog6HngpznlLciLCJyb2xlcyI6W3siYXV0aG9yaXR5IjoiQ0dKQlIifSx7ImF1dGhvcml0eSI6IlBUWUcxMSJ9LHsiYXV0aG9yaXR5IjoiWFQtWkoifSx7ImF1dGhvcml0eSI6IjY4NDgifV0sImNsaWVudF90eXBlIjoiU0giLCJjbGllbnRfaWQiOiJzaW5vLW1hbGwiLCJzY29wZSI6WyJhbGwiXSwiY2F0ZWdvcmllcyI6W3sidGl0bGUiOiLph4fotK0iLCJjb2RlIjoiQ0ctWkoiLCJpbmRleFVyaSI6IumHh-i0rSJ9XSwiY29tcGFueV9zaG9ydF9uYW1lIjoi5rWZIiwiZXhwIjoxNzExMTYwOTM2LCJqdGkiOiIyNDYwOGE4Ni03NmNmLTQxYWYtYmZhNy0zZmE5MmExMTg1MmUiLCJjb21wYW55X2lkIjoxMzM0LCJncm91cF9uYW1lIjoi6YeH6LSt566h55CG5a6kIiwibW9iaWxlIjoiMTU3NTczMDIyODUiLCJ2ZW5kb3JfbmFtZSI6bnVsbCwibGFzdF9jaGFuZ2VfcGFzcyI6MTY4OTU1NjEyNzAwMCwiYXV0aG9yaXRpZXMiOlsiUFRZRzExIiwiQ0dKQlIiLCJYVC1aSiIsIjY4NDgiXSwiY29tcGFueV9sZXZlbCI6IjIiLCJsb2dpbl9uYW1lIjoiaHV3ZWluYW5fWkoiLCJ1c2VyX2lkIjo5NDQ0LCJncm91cF9pZCI6NjM2OSwidmVuZG9yX2lkIjpudWxsLCJjb21wYW55X25hbWUiOiLmtZnmsZ_liIblhazlj7giLCJzZWNvbmRfZGVwdF9pZCI6NjI1NCwic2Vjb25kX2RlcHRfbmFtZSI6IuaUr-aSkeacjeWKoemDqCJ9.dQfAlEbCfYzc4zAHpJJIWkX471ZNInaDNP0mkse6C3klLfvDL_HMgZHiG97xv1ms1YL_b1VG1Wf0lq5SPYoWOVHogbnNGD_4EkD0XUEBYmWEBydXUTjUOr02FCl--cCPFPxFzMQRIHLY8quGga7avYN60RJq5CkGojjdhWuCeWc"
    result = dealProgram.deal(1,auth)
    print(result)
    print(f"当前时间："+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))

    # test
    # insert_list = [{'id': 75427, 'priceConfirmLetterId': 2691, 'productCode': 'SP23121804200175', 'spuId': 15536, 'productName': 'REMAX其他个人类马力系列 PD65W快充数据线  RC-191 C-C', 'brand': 'REMAX', 'targetProfitRate': '4%', 'estimateProfitRate': '58.97%'}]
    # array_list = [[value for value in item.values()] for item in insert_list]
    # dealProgram.insertOrUpdateLetterDetailProduct(array_list)


