import datetime
import os
import pandas as pd
from openpyxl import load_workbook
from RetailData import RetailData
from PanFullSerCodeFileRead import PanFullSerCode
from ScmSoldInLinrary import ScmSoldInLinrary
from FanQuanPiLiangZhuiZongFile import FanQuanPiLiangZhuiZongFile
from ReasonThreeConditTwo import  ReasonThreeConditonTwo
from StoreNotReceipt import StoreNotReceipt
from StoreNotReceiptUnComplete import StoreNotReceiptUnComplete
class DataDeal:
    def get_desktop_path(self):
        """获取系统桌面路径并返回"""
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        return desktop_path
    # 获取现在日期的上个月并以202405这种字符串形式返回
    def get_last_month(self):
        # 获取当前日期
        today = datetime.date.today()
        # 计算上个月的年份和月份
        if today.month == 1:
            last_month = 12
            year = today.year - 1
        else:
            last_month = today.month - 1
            year = today.year
        # 返回格式化的字符串
        return f"{year}{last_month:02d}"
    def clean_data(self, data):
        """清洗数据，将所有非数值和非字符串类型的数据转换为字符串"""
        for column in data.columns:
            try:
                data[column] = data[column].apply(
                    lambda x: str(x) if not (isinstance(x, (int, float, str)) or pd.isnull(x)) else x)
            except Exception as e:
                print(f"清洗列 {column} 时出错: {e}")
                print(data[column])
        return data

    def ScmReadData(self, filename):
        try:
            data = pd.read_excel(filename, sheet_name='SCM串码', keep_default_na=False, header=0, index_col=None)
            print("SCM串码表的列名：", data.columns.tolist())  # 打印列名

            # 清洗数据
            data = self.clean_data(data)
            data = data[["串码", "库存地点", "物料编号", "物料描述"]].astype("str")

            target_data_list = pd.read_excel(filename, sheet_name='泛全串码', keep_default_na=False, header=0, index_col=None)
            print(f"泛全表单的列名为: {target_data_list.columns.tolist()}")
            target_data_list = target_data_list["串号"].astype("str").tolist()
            target_data_list = list(set(target_data_list))

            scMisNull_list = []
            data = data.values.tolist()
            for item in data:
                if item[0] not in target_data_list:
                    scMisNull_list.append(item)
            scMisNull_list = pd.DataFrame(scMisNull_list, columns=["串码", "库存地点", "物料编号", "物料描述"])
            scMisNull_list["状态"] = "S有F无"
            scMisNull_list["分类"] = ""
            scMisNull_list["备注"] = ""
            scMisNull_list["处理状态"] = ""
            scMisNull_list["差异产生月份"] = ""
            scMisNull_list = scMisNull_list[["状态", "串码", "库存地点", "物料编号", "物料描述", "分类", "备注", "处理状态", "差异产生月份"]].values.tolist()
            return scMisNull_list
        except Exception as e:
            print(f"读取 SCM 数据时发生错误: {e}")
            raise

    def FanquanDataDeal(self, filename):
        try:
            data = pd.read_excel(filename, sheet_name='泛全串码', keep_default_na=False, header=0, index_col=None)
            print("泛全串码表的列名：", data.columns.tolist())  # 打印列名

            # 清洗数据
            data = self.clean_data(data)
            data = data[["串号", "scm物料编码", "商品全称", "当前仓库"]]
            target_data_list = pd.read_excel(filename, sheet_name='SCM串码', keep_default_na=False, header=0, index_col=None)
            target_data_list = target_data_list["串码"].astype("str").tolist()
            print(f"scm目标列的长度是: {len(target_data_list)}")
            target_data_list = list(set(target_data_list))
            FanquanDataList = []
            data = data.values.tolist()
            for item in data:
                if item[0] not in target_data_list:
                    FanquanDataList.append(item)
            FanquanDataList = pd.DataFrame(FanquanDataList, columns=["串号", "scm物料编码", "商品全称", "当前仓库"])
            FanquanDataList["状态"] = "F有S无"
            FanquanDataList["分类"] = ""
            FanquanDataList["备注"] = ""
            FanquanDataList["处理状态"] = ""
            FanquanDataList["差异产生月份"] = ""
            FanquanDataList = FanquanDataList[["状态", "串号", "当前仓库", "scm物料编码", "商品全称", "分类", "备注", "处理状态", "差异产生月份"]]
            FanquanDataList = FanquanDataList.values.tolist()
            return FanquanDataList
        except Exception as e:
            print(f"处理泛全数据时发生错误: {e}")
            raise

    def DataMatch(self, rawDataList, retailDataList):

        i=0
        TargetList = set()
        if rawDataList is None or retailDataList is None:
            return list(TargetList)
        try:
            items_to_remove = []
            for rawData in rawDataList:
                for retailData in retailDataList:
                    if rawData[1] == retailData[1]:
                        matched_rawData = list(rawData)  # 转回 list 以修改内容
                        matched_rawData[-1] = retailData[0]
                        matched_rawData[-3] = retailData[-1]
                        matched_rawData[-4] = "销售未录"
                        print(f"原因为销售未录的数据为：{rawData}=={retailData}")
                        print(f"在未录入数据的串码为{matched_rawData} == {retailData}--{++i}")
                        TargetList.add(tuple(matched_rawData))  # 使用 tuple 存入 set
                        items_to_remove.append(rawData)
                        break  # 一旦找到匹配项，跳出内层循环
            for item in items_to_remove:
                rawDataList.remove(item)
        except Exception as e:
            print(f"合并数据时出错:{e}")
        print(f"销售未录的数据总长度为:{len(TargetList)}")
        print(f"原因一后剩余需要查找的原因数据长度为:{len(rawDataList)}")
        return list(TargetList),list(rawDataList)
    # 原因二:时间差销售未未录
    def timeDiffUnrecord(self, rawDataList,panfullsercodeList,scmSoldDataList):
        reasonTwoDataList=[]
        for item in rawDataList:
            if item[1] not in panfullsercodeList and item[1] in scmSoldDataList:
                item[-1]=self.get_last_month()
                item[-2]="已处理"
                item[-4]="时间差销售未录"
                reasonTwoDataList.append(item)
        for item in reasonTwoDataList:
            rawDataList.remove(item)
        print(f"原因为时间销售未录的数据长度为:{len(reasonTwoDataList)}")
        print(f"原因二后未找到数据长度为:{len(rawDataList)}")
        return list(set(reasonTwoDataList)),rawDataList
    def reaThreeConditOne(self,rawDataList,targetlist):
        reasonThreeConditOneList=[]
        for item in rawDataList:
            for data in targetlist:
                if item[1]==data[0]:
                    item[-4]="促销品未领用"
                    item[-3]="SCM已出库，泛全未处理"
                    item[-1]=data[-1]
                    reasonThreeConditOneList.append(item)
                    break
        for item in reasonThreeConditOneList:
            rawDataList.remove(item)
        return list(set(map(tuple, reasonThreeConditOneList))), rawDataList
        # return list(set(reasonThreeConditOneList)),rawDataList
    def reaThreeConditTwo(self,rawDataList,targetlist):
        reasonThreeConditTwoList=[]
        for item in rawDataList:
            for data in targetlist:
                if item[1]==data[0]:
                    item[-4]="促销品未领用"
                    item[-3]="泛全已处理，SCM未领用"
                    item[-1]=data[-1]
                    reasonThreeConditTwoList.append(item)
        for item in reasonThreeConditTwoList:
            rawDataList.remove(item)
        return list(set(map(tuple, reasonThreeConditTwoList))), rawDataList
        # return list(set(reasonThreeConditTwoList)),rawDataList
    #   # 门店未确认收货（已完成）
    def storeNotReceipt(self,rawDataList,targetlist):
        storeNotReceiptList=[]
        for item in rawDataList:
            for data in targetlist:
                if item[1]==data[0]:
                    item[-2]="已处理"
                    item[-4]='门店未确认收货'
                    storeNotReceiptList.append(item)
                    break
        for item in storeNotReceiptList:
            rawDataList.remove(item)
        return list(set(map(tuple, storeNotReceiptList))), rawDataList
        # return list(set(storeNotReceiptList)),rawDataList
    def storeNotReceiptUncomplete(self,rawDataList,targetList):
        if targetList is None:
            print("Error: targetList is None")
            return [], rawDataList
        storeNotReceiptUncompleteList=[]
        for data in rawDataList:
            if data[1] in targetList:
                data[-4]="门店未确认收货"
                storeNotReceiptUncompleteList.append(data)
        for item in storeNotReceiptUncompleteList:
            rawDataList.remove(item)
        return list(set(map(tuple, storeNotReceiptUncompleteList))), rawDataList

    def copy_excel_file(self,source_file_path, target_file_path):
        # 读取源Excel文件的所有内容
        with pd.ExcelFile(source_file_path) as xls:
            # 创建一个ExcelWriter对象，指定目标文件路径和引擎
            with pd.ExcelWriter(target_file_path, engine='xlsxwriter') as writer:
                # 遍历所有sheet并写入目标文件
                for sheet_name in xls.sheet_names:
                    df = pd.read_excel(xls, sheet_name=sheet_name)
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
        # return list(set(storeNotReceiptUncompleteList)),rawDataList

    def write_to_existing_excel(self,file_path, sheet_name, data, startrow=None, startcol=None):
        """
        将数据写入现有的 Excel 文件的指定 sheet 页。
        """
        # 设置默认值为 0
        if startrow is None:
            startrow = 0
        if startcol is None:
            startcol = 0
        with pd.ExcelWriter(file_path, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
            data.to_excel(writer, sheet_name=sheet_name, index=False)



if __name__ == '__main__':
    dataDeal = DataDeal()
    systemDesktop=dataDeal.get_desktop_path()
    file_path = f'{systemDesktop}\\二系统稽核\\盘点报告表\\20240627.xlsx'
    RetailNotEntered_file_path = f'{systemDesktop}\\二系统稽核\\销售未录入数据\\零售未录数据7.9.xlsx'
    print(RetailNotEntered_file_path)
    print(file_path)
    data = None
    FanquanData = None
    retailData = None

    try:
        data = dataDeal.ScmReadData(file_path)
        print(f"scm串码有泛全没有的数据长度是：{len(data)}")
        FanquanData = dataDeal.FanquanDataDeal(file_path)
        print(f"泛全有SCM无的数据列表长度是：{len(FanquanData)}")
        print(f"合并之后的数据类型为:{type(data)}")
        print(f"合并之后的数据长度为:{len(data)}")
    except Exception as e:
        print(f"在处理数据时发生错误: {e}")
    try:
        retailData = RetailData()
        retailData = retailData.ReadData(RetailNotEntered_file_path).values.tolist()
    except Exception as e:
        print(f"读取零售数据时出错:{e}")
    readlist,rawDataList=dataDeal.DataMatch(data + FanquanData, retailData)
    print(f"需要查找原因的数据为长度为:{len(rawDataList)}")
    # 读取泛全系统下载下来串码查询报告表
    file_path = f'{systemDesktop}\\二系统稽核\\泛全系统文件下载\\串码查询报告表.xlsx'
    panfullsercode = PanFullSerCode()
    panfullsercodeList=panfullsercode.GetData(file_path)
    # 读取SCM在库已售串码记录文件
    file_path3 = f'{systemDesktop}\\二系统稽核\\ScmDownLoad\\SCM在库已售串码记录文件.xlsx'
    scmSoldData=ScmSoldInLinrary()
    scmSoldDataList=scmSoldData.GetSoldInLinrary(file_path3)
    reasonTwoDataList,rawDataListAfterReasonTwo=dataDeal.timeDiffUnrecord(rawDataList,panfullsercodeList,scmSoldDataList)
    # 原因三：情况一SCM已出库泛全未处理
    # 1.泛全批量追踪文件读取
    file_path = f'{systemDesktop}\\二系统稽核\\泛全系统文件下载\\串号全程跟踪查询报表.xlsx'
    fanquanpiliangzhuizongfileFilter = FanQuanPiLiangZhuiZongFile()
    TargetList = fanquanpiliangzhuizongfileFilter.FanquanPiLiangZhuiZongFile(file_path)
    # 读取销售订单列中全部的销售组织为z004的数据
    file_path1 = f'{systemDesktop}\\二系统稽核\\ScmDownLoad\\SCM销售串码记录文件.xlsx'
    file_path2 = f'{systemDesktop}\\二系统稽核\\ScmDownLoad\\SCM销售订单.xlsx'
    scmXiaoChuanMa_filtered = fanquanpiliangzhuizongfileFilter.scmXiaoShouchuanMaJiLu(file_path1, file_path2)
    rawDataListTargetList = []
    for item in scmXiaoChuanMa_filtered:
        if item[0] in TargetList:
            print(f"SCM已出库泛全未处理的数据有:{item}")
            rawDataListTargetList.append(item)
    print(f"SCM已出库泛全未处理的数据的长度为:{len(rawDataListTargetList)}")
    reasonThreeConditOneList,rawDataListAfterReasonThree1=dataDeal.reaThreeConditOne(rawDataListAfterReasonTwo,rawDataListTargetList)
    # 原因三情况二的数据匹配和筛选
    file_path1 = f'{systemDesktop}\\二系统稽核\\ScmDownLoad\\SCM在库已售串码记录文件.xlsx'
    file_path2 = f'{systemDesktop}\\二系统稽核\\泛全系统文件下载\\串号全程跟踪查询报表(在库串码).xlsx'
    reasonThreeCondition2 = ReasonThreeConditonTwo()
    reason_three_condition2_targteList = reasonThreeCondition2.reasonThreeConditonTwo(file_path1, file_path2)
    reasonThreeConditTwoList,rawDataListAfterReasonTwo=dataDeal.reaThreeConditTwo(rawDataListAfterReasonThree1,reason_three_condition2_targteList)
    # 门店未确认收货（已完成）
    file_path1 = f'{systemDesktop}\\二系统稽核\\ScmDownLoad\\SCM在库已售串码记录文件.xlsx'
    file_path2 = f'{systemDesktop}\\二系统稽核\\泛全系统文件下载\\串码查询报告表.xlsx'
    storeNotReceipt = StoreNotReceipt()
    storeNotReceiptTargetList=storeNotReceipt.storeNotReceipt(file_path1, file_path2)
    storeNotReceiptList,rawDataListAfterstoreNotReceipt=dataDeal.storeNotReceipt(rawDataListAfterReasonTwo,storeNotReceiptTargetList)
    #门店未确认收货(未完成)
    file_path1 = f'{systemDesktop}\\二系统稽核\\泛全系统文件下载\\导出采购明细（串码级别）.xlsx'
    stroneNotReceiptUncomplete = StoreNotReceiptUnComplete()
    storeNotReceiptUnCompleteTargetList = stroneNotReceiptUncomplete.storeNotReceiptUnComplete(file_path1)
    storeNotReceiptUncompleteList,rawDataListFinally=dataDeal.storeNotReceiptUncomplete(rawDataListAfterstoreNotReceipt,storeNotReceiptUnCompleteTargetList)
    # 所有的结果表回写Excel文件中
    TotalList=readlist+reasonTwoDataList+reasonThreeConditOneList+reasonThreeConditTwoList+storeNotReceiptList+storeNotReceiptUncompleteList+rawDataListFinally
    FinallyData=pd.DataFrame(TotalList)
    FinallyData.columns=["状态", "串号", "当前仓库", "scm物料编码", "商品全称", "分类", "备注", "处理状态", "差异产生月份"]
    FinalFile_path=f'{systemDesktop}\\二系统稽核\\结果\\结果.xlsx'
    file_path = f'{systemDesktop}\\二系统稽核\\盘点报告表\\20240627.xlsx'
    dataDeal.copy_excel_file(file_path,FinalFile_path)
    dataDeal.write_to_existing_excel(FinalFile_path,sheet_name="剩余差异",data=FinallyData)
    test=True







