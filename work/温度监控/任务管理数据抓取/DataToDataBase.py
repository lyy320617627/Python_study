from MySQLUtil import MySQLUtil
from GetOaFile import GetFile
import pandas as pd
from datetime import datetime


class DataToDataBase:
    def __init__(self, datalist):
        self.datalist = datalist
        self.conn = MySQLUtil(host="192.168.0.148", port=3306, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")

    def deaData(self):
        # 将数据转换为DataFrame
        pdData = pd.DataFrame(data=self.datalist)
        pdData.columns = ["产品", "送检量", "完成量", "在测量", "任务预警量"]

        # 将字符串类型转换为数字类型，遇到非数字值时用 NaN 替代
        pdData["送检量"] = pd.to_numeric(pdData["送检量"], errors='coerce')
        pdData["完成量"] = pd.to_numeric(pdData["完成量"], errors='coerce')
        pdData["在测量"] = pd.to_numeric(pdData["在测量"], errors='coerce')
        pdData["任务预警量"] = pd.to_numeric(pdData["任务预警量"], errors='coerce')

        # 将 NaN 值填充为 0（如果需要）
        pdData = pdData.fillna(0)

        # 对各列进行求和
        # 送检任务量 \
        inspection_quantity  = pdData["送检量"].sum()
        completed_quantity = pdData["完成量"].sum()
        ongoing_task = pdData["在测量"].sum()
        overdue_warn_tasks = pdData["任务预警量"].sum()

        # 打印DataFrame和各列的求和结果
        print(f"pdData:\n{pdData}")
        print(f"送检任务量: {inspection_quantity}")
        print(f"已完成任务: {completed_quantity}")
        print(f"进行中任务: {ongoing_task}")
        print(f"超期预警任务: {overdue_warn_tasks}")
        trancate_sql1="truncate table bs_task_data;"
        truncate_sql2="truncate table bs_task_info;"
        self.conn.execute(trancate_sql1)
        self.conn.execute(truncate_sql2)
        key_list1=["conduct","inspection_quantity","completed_quantity","measure_quantity","task_warning_quantity"]
        self.conn.batchInsert("bs_task_data",key_list1,self.datalist)
        key_list2=["inspection_quantity","completed_quantity","ongoing_task","overdue_warn_tasks"]
        datalist2=[
            [str(inspection_quantity)+"项",str(completed_quantity)+"项",str(ongoing_task)+"项",str(overdue_warn_tasks)+"项"]
        ]
        self.conn.batchInsert("bs_task_info",key_list2,datalist2)

if __name__ == '__main__':
    getfile = GetFile()
    getfile.getInstanceCount()
    getfile.get_form_fields()
    getfile.getDetailData()
    print(f"最终数据条数：{len(getfile.finalyDataList)}")

    # 处理数据
    dataDeal = DataToDataBase(getfile.finalyDataList)
    dataDeal.deaData()
