"""
每日流程预警汇总
用于每日流程预警汇总
"""
from MySQLUtil import MySQLUtil
import pandas as pd
import os

class DailyAlertSummary:

    def get_desktop_path(self):
        """获取系统桌面路径并返回"""
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        return desktop_path

    def __init__(self):
        # 初始化数据库连接
        self.conn = MySQLUtil(host="192.168.0.148", port=3306, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
        self.__table__ = "bs_daily_rtime_oper_eff_warn"
        self.__filePath__ = f"{self.get_desktop_path()}\\每日预警数据汇总.xlsx"

    def dailyAlertSummary(self):
        # 从数据库中获取数据
        data = self.conn.select_all(self.__table__)
        data = pd.DataFrame(list(data))
        print(f"从数据库筛选出来的数据为:\n{data}")
        print(f"从数据库筛选出来的数据的长度为:\n{len(data)}")

        # 设置列名
        data.columns = ['更新日期', '更新时间', '订单类型', '警告情况', '超时', '发货仓库', '移出货主', '移出库存地',
                        '指令类型', '指令编号', '指令行项|交货序号', '数量', '业务执行状态', '移出物料',
                        '物料描述', '运单编号', '承运商名称', '售达方编号', '售达方名称', '收货人',
                        '电话1', '省份描述', '城市描述', '地区描述', '收货地址', '创建日期', '预警次数']

        # 根据列名筛选数据
        data = data[['订单类型', '发货仓库', '移出货主', '移出库存地', '指令类型', '指令编号',
                     '指令行项|交货序号', '数量', '业务执行状态', '移出物料', '物料描述', '运单编号',
                     '承运商名称', '售达方编号', '售达方名称', '收货人', '电话1', '省份描述',
                     '城市描述', '地区描述', '收货地址', '更新时间', '预警次数']]

        # 根据指令编号和指令行项|交货序号进行分组，并筛选出不同的数据
        grouped_data = data.groupby(['指令编号', '指令行项|交货序号'])

        # 筛选出每组中第一条数据
        filtered_data = grouped_data.first().reset_index()

        print(f"筛选后的数据为:\n{filtered_data}")
        print(f"筛选后的数据的长度为:\n{len(filtered_data)}")

        # 将筛选后的数据保存到 Excel 文件中
        filtered_data.to_excel(self.__filePath__, index=False)

if __name__ == '__main__':
    dailyDataSummary = DailyAlertSummary()
    dailyDataSummary.dailyAlertSummary()
    print(f"每日流程预警数据汇总的数据保存为: {dailyDataSummary.__filePath__}")
