import pandas as pd
from datetime import datetime

class StoreNotReceipt:
    def storeNotReceipt(self, file_path1, file_path2):
        data = pd.read_excel(file_path1, keep_default_na=False, index_col=None)
        # 输出前几行数据以确认数据加载正确
        print(f"前几行数据:\n{data.head()}")
        # 确认列名，确保使用正确的列名进行筛选
        print(f"列名:\n{data.columns}")
        # 应用筛选条件
        data_filtered = data[
            ((data["库存地点"] == "L001") | (data["库存地点"] == "109S")) & (data["串码状态描述"] == "在库")]
        data_filtered = data_filtered["串码"].values.tolist()
        print(f"data_filtered的数据类型为:{type(data_filtered)}")
        print(f"从文件中筛选出来库存地点为L001或者109S并且串码状态为在库的数据为:\n{data_filtered}")
        print(f"从文件中筛选出来库存地点为L001或者109S并且串码状态为在库的数据长度为:{len(data_filtered)}")

        data2 = pd.read_excel(file_path2, keep_default_na=False, index_col=None)
        data2["入库时间"] = pd.to_datetime(data2["入库时间"])
        current_month = datetime.now().strftime('%Y-%m')
        data2_filtered = data2[(data2["门店类型"] == "自营厅") & (data2["入库时间"].dt.strftime('%Y-%m') == current_month)]
        data2_filtered =data2_filtered[["串号","入库时间"]]
        data2_filtered = data2_filtered.values.tolist()
        print(f"筛选出来入库时间大于当前月份的自营厅数据为:\n{data2_filtered}")
        print(f"筛选出来入库时间大于当前月份的自营厅数据长度为:{len(data2_filtered)}")
        storeNotReceiptTargetList=[]
        for data in data_filtered:
            for item in data2_filtered:
                if data==item[0]:
                    storeNotReceiptTargetList.append(item)
        return storeNotReceiptTargetList

if __name__ == '__main__':
    file_path1 = r'C:\Users\ly320\Desktop\二系统稽核\ScmDownLoad\SCM在库已售串码记录文件.xlsx'
    file_path2 = r'C:\Users\ly320\Desktop\二系统稽核\泛全系统文件下载\串码查询报表.xlsx'
    storeNotReceipt = StoreNotReceipt()
    storeNotReceipt.storeNotReceipt(file_path1, file_path2)
