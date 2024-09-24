from MySQLUtil import MySQLUtil
from GetOaFile import GetFile
import pandas as pd
from datetime import datetime

class DataToDataBase:
    def __init__(self, datalist):
        self.datalist = datalist
        self.conn = MySQLUtil(host="192.168.0.148", port=3306, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")

    def deaData(self):
        # 将数据转换为 DataFrame
        pdData = pd.DataFrame(self.datalist)
        pdData.columns = ["设备名称", "资产编号", "使用情况", "下一次维护", "下一次校准", "是否重点设备"]

        # 定义日期格式化函数
        def format_date(date):
            if pd.isnull(date) or str(date).strip() == "":
                return None  # 返回 None 以在 SQL 中处理为 NULL
            try:
                # 将日期字符串转换为 datetime 对象
                date_obj = pd.to_datetime(date, errors='coerce')
                if pd.isnull(date_obj):
                    return None
                return date_obj.strftime('%Y-%m-%d')
            except Exception as e:
                print(f"日期格式化失败: {e}")
                return None

        # 处理使用情况列
        pdData["使用情况"] = pdData["使用情况"].apply(lambda x: x if x == "使用中" else "空闲")

        # 处理下一次维护和下一次校准列，应用日期格式化
        pdData["下一次维护"] = pdData["下一次维护"].apply(format_date)
        pdData["下一次校准"] = pdData["下一次校准"].apply(format_date)

        # 获取今天的日期
        today = datetime.now()

        # 计算是否重点设备的数量
        重点设备_count = pdData["是否重点设备"].astype(str).apply(lambda x: x == "1").sum()
        print(f"重点设备的个数为: {重点设备_count}")

        # 找到“下一次维护”和“下一次校准”大于今天的最小日期
        pdData["下一次维护"] = pd.to_datetime(pdData["下一次维护"], errors='coerce')
        pdData["下一次校准"] = pd.to_datetime(pdData["下一次校准"], errors='coerce')

        future_维护_dates = pdData["下一次维护"].dropna().loc[pdData["下一次维护"] > today]
        future_校准_dates = pdData["下一次校准"].dropna().loc[pdData["下一次校准"] > today]

        date1 = future_维护_dates.min().strftime('%Y-%m-%d') if not future_维护_dates.empty else ""
        date2 = future_校准_dates.min().strftime('%Y-%m-%d') if not future_校准_dates.empty else ""

        print(f"下一次维护大于今天的最小日期为: {date1}")
        print(f"下一次校准大于今天的最小日期为: {date2}")

        # 新增“维护/校准预警”列
        def check_warning(row):
            next_maintenance = pd.to_datetime(row["下一次维护"], errors='coerce')
            next_calibration = pd.to_datetime(row["下一次校准"], errors='coerce')
            if pd.notnull(next_maintenance) and next_maintenance < today:
                if pd.notnull(next_calibration) and next_calibration < today:
                    return "维护校准预警"
                return "维护预警"
            elif pd.notnull(next_calibration) and next_calibration < today:
                return "校准预警"
            return "正常"

        pdData["维护/校准预警"] = pdData.apply(check_warning, axis=1)

        # 选择需要的列并转换为列表
        bs_device_data = pdData[["设备名称", "资产编号", "使用情况", "下一次维护", "下一次校准", "维护/校准预警"]].values.tolist()

        print(f"bs_device_data 前 10 行数据:\n {bs_device_data[:10]}")  # 输出前 10 行检查

        # 执行 SQL 插入操作
        excute_sql = """
        INSERT INTO bs_LargeScreen_device_data 
        (deviceName, assent_number, use_situation, next_maint, next_calibration, warn_situation)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        deviceName = VALUES(deviceName),
        assent_number = VALUES(assent_number),
        use_situation = VALUES(use_situation),
        next_maint = VALUES(next_maint),
        next_calibration = VALUES(next_calibration),
        warn_situation = VALUES(warn_situation)
        """
        self.conn.executemany(excute_sql, bs_device_data)
        print(f"插入成功，数据条目数: {len(pdData)}")
        print(pdData.head(5))

if __name__ == '__main__':
    getfile = GetFile()
    getfile.getInstanceCount()
    getfile.get_form_fields()
    getfile.getDetailData()
    print(f"最终数据条数：{len(getfile.finalyDataList)}")
    dataDeal = DataToDataBase(getfile.finalyDataList)
    dataDeal.deaData()

