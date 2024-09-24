"""
此类用于将线上线下数据从文件中读取下来并且上传到数据库中，
注意：
"""
from MySQLUtil import MySQLUtil
import os
import pandas as pd
from datetime import datetime
import requests
from datetime import datetime
import math
from GetOAFile import GetFile
pd.set_option('display.max_rows', None)  # 设置显示最大行数为 None，即不限制
pd.set_option('display.max_columns', None)  # 设置显示最大列数为 None，即不限制
pd.set_option('display.max_colwidth', None)  # 设置列宽为 None，即不限制
class DataUpLoad:
    def __init__(self):
        self.__destTopPath=self.getDestTopPath()
        self.offonlineDataFilePath=self.getFilePath()[0]
        self.onlineDataFilePath=self.getFilePath()[1]
        self.formatDateList=self.getCurrDate()
        self.saleDataList=self.dataUpLoad()

    # 返回桌面路径
    def getDestTopPath(self):
        """获取系统桌面路径并返回"""
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        return desktop_path
    # 返回当前日期的特定形式用于判断目标文件夹下是否包含当前月份的模板文件
    def getCurrDate(self):
        today = datetime.today()
        # 格式化日期，包含前导零
        date1 = today.strftime('%Y年%m月')
        # 将月份部分中的前导零去掉
        month = today.strftime('%m')  # 只获取月份
        if month.startswith('0'):
            month = month[1:]  # 去掉前导零
        date2 = today.strftime(f'%Y年{month}月')
        return [date1, date2]

    # 读取目标文件夹下的文件总数和文件名称
    # def get_files_in_directory(self):
    #     directory_path=os.path.join(self.__destTopPath,"实时监控返利程序")
    #     print(f"实时监控程序模板文件所在的文件夹路径为:{directory_path}")
    #     # 获取指定目录下的所有文件
    #     files = os.listdir(directory_path)
    #     try:
    #         if len(files)!=0:
    #             files = [f for f in files if os.path.isfile(os.path.join(directory_path, f))]
    #             for file in files:
    #                 if any(pattern in file for pattern in self.formatDateList):
    #                     return os.path.join(directory_path,file)
    #     except FileNotFoundError:
    #         return None
    #     except Exception as e:
    #         print(f"发生错误: {e}")
    #         return None
    # 获取从泛全上下载下来文件路径
    def getFilePath(self):
        offOnlineDataFilePath = os.path.join(self.__destTopPath,"线下和零售销售数据.xlsx")
        onlineDataFilePath = os.path.join(self.__destTopPath,"线上销售数据.xlsx")
        return offOnlineDataFilePath, onlineDataFilePath
    # 读取线下和零售、线上的销售数据并上传到对应的数据库中
    import pandas as pd

    def dataUpLoad(self):
        conn2 = MySQLUtil(host="192.168.0.148", port=3306, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
        # 读取线下和零售销售数据
        offonlineData = pd.read_excel(self.offonlineDataFilePath, keep_default_na=False, header=0, index_col=False)
        offonlineData = offonlineData[
            ["供应商", "供应商类型", "品牌", "商品分类", "数量", "零售报价", "归属地市", "SCM物料编码", "活动内类型"]]
        # 计算销售金额
        offonlineData['销售金额'] = offonlineData['数量'] * offonlineData['零售报价']
        # 按照 '归属地市' 和 'SCM物料编码' 进行分组，计算总销售金额和总销量
        grouped = offonlineData.groupby(['归属地市', 'SCM物料编码']).agg({
            '销售金额': 'sum',  # 销售金额相加
            '数量': 'sum'  # 数量相加作为销量
        }).reset_index()
        # 将分组后的数据合并回原始数据
        offonlineData = pd.merge(offonlineData, grouped, on=['归属地市', 'SCM物料编码'], suffixes=('', '_总计'))
        # 去除所有重复的行，只保留每个商品分类、SCM物料编码和归属地市相同的记录中的第一条
        offonlineData = offonlineData.drop_duplicates(subset=['商品分类', 'SCM物料编码', '归属地市'],
                                                             keep='first')
        # 根据活动内类型添加商品分类列
        def classify_product(row):
            if row['活动内类型'] in ['A', '']:
                return '线下'
            elif row['活动内类型'] == 'F1':
                return '零售'
            else:
                return '其他'

        offonlineData.loc[:, '商品活动分类'] = offonlineData.apply(classify_product, axis=1)
        print(f"去重后的线下和零售销售数据为:\n{offonlineData.head(10)}")
        offonlineData=offonlineData[["归属地市","供应商类型","供应商","商品分类","品牌","SCM物料编码","数量_总计","商品活动分类"]]
        offonlineData.columns=["地市","供应商类型","供应商名称","商品分类","品牌","物料编码","销量","商品活动类型"]
        # 筛选特定 SCM物料编码 的数据
        #测试数据
        # offonlineData = offonlineData[offonlineData["物料编码"] == "001217048357900000"]
        # 打印去重后的数据
        # print(f"去重后的线下和零售销售数据为:\n{offonlineData.head(10)}")
        # print(f"去重后的线下和零售销售数据列名为:{offonlineData.columns.tolist()}")
        # 读取线上销售数据
        onlineData = pd.read_excel(self.onlineDataFilePath, keep_default_na=False, header=0, index_col=False)
        onlineData=onlineData[
            ["物料编码","商品品牌","商品分类","数量","市"]]
        onlineData["商品活动类型"]="线上"
        onlineData["供应商类型"]=""
        onlineData["供应商名称"]=""
        #按照物料编码和市进行分组，计算数量总和
        onlineData_grouped = onlineData.groupby(['物料编码', '市']).agg({
            '数量': 'sum'
        }).reset_index()
        onlineData_grouped.rename(columns={'数量': '销量'}, inplace=True)
        # 将销量信息合并回原始的线上销售数据中
        onlineData = pd.merge(onlineData, onlineData_grouped, on=['物料编码', '市'], how='left')
        onlineData = onlineData.drop_duplicates(subset=['物料编码', '商品品牌', '市'],
                                                      keep='first')
        onlineData=onlineData[["市","供应商类型","供应商名称","商品分类","商品品牌","物料编码","销量","商品活动类型"]]
        onlineData.columns=["地市","供应商类型","供应商名称","商品分类","品牌","物料编码","销量","商品活动类型"]
        onlineDataList=onlineData.values.tolist()
        # print(f"onlineDataList的数据长度为:{len(onlineDataList)}")
        offonlineDataList=offonlineData.values.tolist()
        # print(f"offonlineDataList的数据长度为:{len(offonlineDataList)}")
        for onlineData in onlineDataList:
            for offlineData in offonlineDataList:
                if onlineData[-3]==offlineData[-3]:
                    onlineData[1]=offlineData[1]
                    onlineData[2]=offlineData[2]
                    continue
        onlineData=pd.DataFrame(onlineDataList)
        TotalList=onlineDataList+offonlineDataList
        print(f"数据汇总后的列表形式为:{TotalList}")
        # 将销量信息合并回原始的线上销售数据中
        print(f"去重后的线下和零售销售数据量为:{len(offonlineData)}")
        # print(f"线上销售数据为:\n{onlineData.head}")
        print(f"线上销售数据量为:{len(onlineData)}")
        print(f"线上、线下和零售数据合并完后的数据长度为：{len(TotalList)}")
        return TotalList

    def dataUpLoad(self):
        if len(self.saleDataList)!=0:
            conn2 = MySQLUtil(host="192.168.0.148", port=3306, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
            keyList=["city","supplier_type","supplier_name","product_category","brand","material_code","sales","product_activity_type"]
            conn2.batchInsert("bs_sale_data",keyList,self.saleDataList)

    # def FinalDataDeal(self):
    #     getfile = GetFile()
    #     getfile.getInstanceCount()
    #     getfile.get_form_fields()
    #     getfile.getDetailData()
    #     print(f"最总数据为：{len(getfile.finalyDataList)}")
    #     policyData=getfile.finalyDataList
    #     if not policyData:  # 检查 policyData 是否为空
    #         print("没有读取到政策数据，请检查源文件或接口是否正常工作。")
    #         return
    #     self.templateDataList=pd.DataFrame(policyData)
    #     self.templateDataList.columns=["政策时间","品牌","通路类型","地市侧","返利类型","政策起始日期","政策截止日期","物料编码","机型系列","产品俗称","预估数量","返利金额"]
    #     print(f"从OA审批流程中读取到的数据为:\n{policyData}")
    #     FinalDataList = []
    #     if policyData is not None:
    #         saleData = pd.DataFrame(self.saleDataList,
    #                                 columns=["地市", "供应商类型", "供应商名称", "商品分类", "品牌", "物料编码", "销量",
    #                                          "商品活动类型"])
    #         print(f"线上线下和零售数据汇总的数据为\n{saleData}")
    #         print(f"线上线下和零售数据汇总的数据长度为\n{len(saleData)}")
    #         templateFileData = pd.DataFrame(self.templateDataList,
    #                                         columns=["物料编码", "返利类型", "返利金额", "机型系列"])
    #         # 根据物料编码合并销售数据与政策文件
    #         FinalData = pd.merge(saleData, templateFileData, how="left", on="物料编码")
    #         FinalData["返利金额"] = pd.to_numeric(FinalData["返利金额"], errors='coerce')
    #         FinalData["销量"] = pd.to_numeric(FinalData["销量"], errors='coerce')
    #         # 计算返利总金额
    #         FinalData.loc[:, "返利总金额"] = FinalData.loc[:, "销量"] * FinalData.loc[:, "返利金额"]
    #         print(f"合并政策文件后的数据为：\n{FinalData.head(10)}")
    #         # 对合并后的数据去重
    #         FinalData = FinalData.drop_duplicates(subset=["供应商名称", "品牌", "物料编码", "返利类型", "商品活动类型"],
    #                                               keep='first')
    #         # 将NaN值替换为空字符串
    #         FinalData = FinalData.fillna("")
    #         print(f"FinalDataList:{FinalDataList}")
    #         FinalDataList = FinalData.values.tolist()
    #         for data in FinalDataList:
    #             print(f"data数据为:{data}")
    #         print(f"经过去重后的总数据长度为：{len(FinalDataList)}")


if __name__ == '__main__':

    dataUpLoad=DataUpLoad()
    print(f"线下和零售数据文件路径为:{dataUpLoad.offonlineDataFilePath}\n线上销售数据文件路径为:{dataUpLoad.onlineDataFilePath}")
    print(f"已经格式化的日期数据为：{dataUpLoad.formatDateList}")
    dataUpLoad.dataUpLoad()
    dataUpLoad.dataUpLoad()


