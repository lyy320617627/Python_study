from MySQLUtil import MySQLUtil
import os
import pandas as pd
from datetime import datetime
import requests
import math
from GetOAFile import GetFile

pd.set_option('display.max_rows', None)  # 设置显示最大行数为 None，即不限制
pd.set_option('display.max_columns', None)  # 设置显示最大列数为 None，即不限制
pd.set_option('display.max_colwidth', None)  # 设置列宽为 None，即不限制


class DataUpLoad:
    def __init__(self):
        self.__destTopPath = self.getDestTopPath()
        self.offonlineDataFilePath = self.getFilePath()[0]
        self.onlineDataFilePath = self.getFilePath()[1]
        # self.formatDateList = self.getCurrDate()
        self.saleDataList = []  # 初始化为空列表

    # 返回桌面路径
    def getDestTopPath(self):
        """获取系统桌面路径并返回"""
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        return desktop_path

    # # 返回当前日期的特定形式用于判断目标文件夹下是否包含当前月份的模板文件
    # def getCurrDate(self):
    #     today = datetime.today()
    #     # 格式化日期，包含前导零
    #     date1 = today.strftime('%Y年%m月')
    #     # 将月份部分中的前导零去掉
    #     month = today.strftime('%m')  # 只获取月份
    #     if month.startswith('0'):
    #         month = month[1:]  # 去掉前导零
    #     date2 = today.strftime(f'%Y年{month}月')
    #     return [date1, date2]

    # 获取从泛全上下载下来文件路径
    def getFilePath(self):
        offOnlineDataFilePath = os.path.join(self.__destTopPath, "线下和零售销售数据.xlsx")
        onlineDataFilePath = os.path.join(self.__destTopPath, "线上销售数据.xlsx")
        return offOnlineDataFilePath, onlineDataFilePath

    # 读取线下和零售、线上的销售数据并处理
    def processData(self):
        conn2 = MySQLUtil(host="192.168.0.148", port=3306, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")

        # 读取线下和零售销售数据
        offonlineData = pd.read_excel(self.offonlineDataFilePath, keep_default_na=False, header=0, index_col=False)
        offonlineData = offonlineData[
            ["供应商", "供应商类型", "品牌", "商品分类", "数量", "零售报价", "归属地市", "SCM物料编码", "活动内类型"]]
        offonlineData['销售金额'] = offonlineData['数量'] * offonlineData['零售报价']
        grouped = offonlineData.groupby(['归属地市', 'SCM物料编码']).agg({
            '销售金额': 'sum',
            '数量': 'sum'
        }).reset_index()
        offonlineData = pd.merge(offonlineData, grouped, on=['归属地市', 'SCM物料编码'], suffixes=('', '_总计'))
        offonlineData = offonlineData.drop_duplicates(subset=['商品分类', 'SCM物料编码', '归属地市'], keep='first')

        def classify_product(row):
            if row['活动内类型'] in ['A', '']:
                return '线下'
            elif row['活动内类型'] == 'F1':
                return '零售'
            else:
                return '其他'

        offonlineData.loc[:, '商品活动分类'] = offonlineData.apply(classify_product, axis=1)
        offonlineData = offonlineData[
            ["归属地市", "供应商类型", "供应商", "商品分类", "品牌", "SCM物料编码", "数量_总计", "商品活动分类"]]
        offonlineData.columns = ["地市", "供应商类型", "供应商名称", "商品分类", "品牌", "物料编码", "销量",
                                 "商品活动类型"]

        # 读取线上销售数据
        onlineData = pd.read_excel(self.onlineDataFilePath, keep_default_na=False, header=0, index_col=False)
        onlineData = onlineData[["物料编码", "商品品牌", "商品分类", "数量", "市"]]
        onlineData["商品活动类型"] = "线上"
        onlineData["供应商类型"] = ""
        onlineData["供应商名称"] = ""
        onlineData_grouped = onlineData.groupby(['物料编码', '市']).agg({
            '数量': 'sum'
        }).reset_index()
        onlineData_grouped.rename(columns={'数量': '销量'}, inplace=True)
        onlineData = pd.merge(onlineData, onlineData_grouped, on=['物料编码', '市'], how='left')
        onlineData = onlineData.drop_duplicates(subset=['物料编码', '商品品牌', '市'])
        onlineData = onlineData[
            ["市", "供应商类型", "供应商名称", "商品分类", "商品品牌", "物料编码", "销量", "商品活动类型"]]
        onlineData.columns = ["地市", "供应商类型", "供应商名称", "商品分类", "品牌", "物料编码", "销量",
                              "商品活动类型"]

        onlineDataList = onlineData.values.tolist()
        offonlineDataList = offonlineData.values.tolist()

        for onlineData in onlineDataList:
            for offlineData in offonlineDataList:
                if onlineData[-3] == offlineData[-3]:
                    onlineData[1] = offlineData[1]
                    onlineData[2] = offlineData[2]
                    continue

        onlineData = pd.DataFrame(onlineDataList)
        TotalList = onlineDataList + offonlineDataList
        print(f"数据汇总后的列表形式为:{TotalList}")
        print(f"去重后的线下和零售销售数据量为:{len(offonlineData)}")
        print(f"线上销售数据量为:{len(onlineData)}")
        print(f"线上、线下和零售数据合并完后的数据长度为：{len(TotalList)}")

        self.saleDataList = TotalList  # 保存处理后的数据

    # 将处理后的数据上传到数据库
    def uploadData(self):
        if len(self.saleDataList) != 0:
            conn2 = MySQLUtil(host="192.168.0.148", port=3306, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
            sql="truncate table bs_sale_data;"
            conn2.execute(sql)
            keyList = ["city", "supplier_type", "supplier_name", "product_category", "brand", "material_code", "sales",
                       "product_activity_type"]
            conn2.batchInsert("bs_sale_data", keyList, self.saleDataList)


if __name__ == '__main__':
    dataUpLoad = DataUpLoad()
    print(
        f"线下和零售数据文件路径为:{dataUpLoad.offonlineDataFilePath}\n线上销售数据文件路径为:{dataUpLoad.onlineDataFilePath}")
    # print(f"已经格式化的日期数据为：{dataUpLoad.formatDateList}")
    dataUpLoad.processData()  # 处理数据
    dataUpLoad.uploadData()  # 上传数据
