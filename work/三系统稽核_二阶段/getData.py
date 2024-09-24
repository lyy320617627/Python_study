import time

import pandas as pd
import pyautogui
import pyperclip
from MySQLUtil import MySQLUtil
class excelData:

    def getData(self):
        # 文件路径
        excel_path = r"C:\Users\ly320\Desktop\三系余额稽核\结果\差异原因.xlsx"

        # 读取 Excel 文件
        try:
            data = pd.read_excel(excel_path, keep_default_na=False, index_col=None, header=None)
            # data=data[data["差异原因"]=="需要找差异"]
            # 将 DataFrame 转换为列表形式
            data_list=[]
            data_list_temp = data.values.tolist()
            for data in data_list_temp:
                if data[9]=="需要找差异":
                    data_list.append(data)


            # print(data_list)
            return data_list
        except Exception as e:
            return []
            print(f"读取 Excel 文件时出错: {e}")
            raise
    def getScmHigher(self,datalist):
        scmHigher = []
        for data in datalist:
            if float(data[6])>0:
                scmHigher.append(data)
        return scmHigher



    def getScmLower(self, datalist):
        scm_lower = []
        for data in datalist:
            if float(data[6])<0:
                scm_lower.append(data)
        return scm_lower
    def insertIntoTable(self):
        excel_path = r"C:\Users\ly320\Desktop\三系余额稽核\结果\差异原因.xlsx"
        conn2 = MySQLUtil(host="192.168.0.148",port=3306, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
        data=pd.read_excel(excel_path, keep_default_na=False, index_col=None, header=None)
        data_list=data.values.tolist()
        table="huigou_data_phase2"
        key_list=['渠道商名称','渠道商编码','scm余额','惠购和动力余额','同步失败订单','惠购生态订单','本次差异金额','上次差异金额'
                  ,'两次差异金额','差异原因','上次差异原因']
        conn2.batchInsert(table,key_list,data_list)


    def getDictData(self,datalist):
        dictData = {}
        for data in datalist:
            # 创建一个字典，键值为八字码，value值为公司名称
            dictData[data[1]]=data[0]
        return dictData










if __name__ == '__main__':
    excelprogram = excelData()
    excelprogram.insertIntoTable()
    text_path=r"C:\Users\ly320\Desktop\export\num_list.xlsx"
    excelprogram.insertIntoTable()
    data_list=excelprogram.getData()
    # print(data_list)
    # print(len(data_list))
    scmHigher=excelprogram.getScmHigher(data_list)
    print(scmHigher)
    scmLower=excelprogram.getScmLower(data_list)
    num_list=[]
    for data in scmHigher:
        num_list.append(data[1][2:])
    dictData=excelprogram.getDictData(scmHigher)
    print(dictData)
    print(len(dictData))


