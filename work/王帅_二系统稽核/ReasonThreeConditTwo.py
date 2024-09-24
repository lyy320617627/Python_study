import pandas as pd


class ReasonThreeConditonTwo:
    def reasonThreeConditonTwo(self, file_path1, file_path2):
        data = pd.read_excel(file_path1, keep_default_na=False, index_col=None)
        # 输出前几行数据以确认数据加载正确
        print(f"前几行数据:\n{data.head()}")
        # 确认列名，确保使用正确的列名进行筛选
        print(f"列名:\n{data.columns}")
        # 应用筛选条件
        data_filtered = data[
            ((data["库存地点"] == "L001") | (data["库存地点"] == "109S")) & (data["串码状态描述"] == "在库")]
        data_filtered=data_filtered["串码"].values.tolist()
        print(f"data_filtered的数据类型为:{type(data_filtered)}")
        print(f"从文件中筛选出来库存地点为L001或者109S并且串码状态为在库的数据为:\n{data_filtered}")
        print(f"从文件中筛选出来库存地点为L001或者109S并且串码状态为在库的数据长度为:{len(data_filtered)}")
        data2 = pd.read_excel(file_path2, keep_default_na=False, index_col=None)
        data2["日期"] = pd.to_datetime(data2["日期"], errors='coerce')
        data2 = data2.sort_values(by=["串号", "日期"]).groupby("串号").tail(1)
        data2 = data2[(data2["操作类型"] == "采购退货出库") & (data2["制单人"] == "楼小建")]
        data2["日期"] = data2["日期"].apply(lambda x: x.strftime('%Y%m') if not pd.isnull(x) else '')
        data2=data2[["串号","日期"]]
        data2=data2.values.tolist()
        print(f"从串号全程跟踪查询报表(在库串码)中选出串号和日期最新的一列的数据为:\n{data2}")
        print(f"从串号全程跟踪查询报表(在库串码)中选出串号和日期最新的一列的数据长度为:{len(data2)}")
        # for index, row in data2.iterrows():
        #     print(row["串号"])
        reason_three_condition2_targteList =[]
        for data in data_filtered:
            for item in data2:
                if data==item[0]:
                    reason_three_condition2_targteList.append(item)
        print(f"原因三情况二参照的目标列为:{reason_three_condition2_targteList}")
        print(f"原因三情况二参照的目标列为:{len(reason_three_condition2_targteList)}")
        return reason_three_condition2_targteList


if __name__ == '__main__':
    file_path1 = r'C:\Users\ly320\Desktop\二系统稽核\ScmDownLoad\SCM在库已售串码记录文件.xlsx'
    file_path2 = r'C:\Users\ly320\Desktop\二系统稽核\泛全系统文件下载\串号全程跟踪查询报表(在库串码).xlsx'
    reasonThreeCondition2 = ReasonThreeConditonTwo()
    reason_three_condition2_targteList= reasonThreeCondition2.reasonThreeConditonTwo(file_path1, file_path2)
