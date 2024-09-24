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
        important_count = pdData["是否重点设备"].astype(str).apply(lambda x: x == "1").sum()
        print(f"重点设备的个数为: {important_count}")
        # 计算在使用中的重点设备数量
        usingImportant_count = \
        pdData[(pdData["是否重点设备"].astype(str) == "1") & (pdData["使用情况"] == "使用中")].shape[0]
        print(f"使用中的重点设备的个数为: {important_count}")
        # 计算重点设备的利用率
        if important_count > 0:
            using_rate = usingImportant_count / important_count
            using_rate = f"{using_rate:.2%}"
        else:
            using_rate = 0
        # 找到“下一次维护”和“下一次校准”大于今天的最小日期
        pdData["下一次维护"] = pd.to_datetime(pdData["下一次维护"], errors='coerce')
        pdData["下一次校准"] = pd.to_datetime(pdData["下一次校准"], errors='coerce')
        future_维护_dates = pdData["下一次维护"].dropna().loc[pdData["下一次维护"] > today]
        future_校准_dates = pdData["下一次校准"].dropna().loc[pdData["下一次校准"] > today]
        # 计算下一次维护到今天的剩余天数
        if not future_维护_dates.empty:
            date1 = (future_维护_dates.min() - today).days+1  # 剩余天数
            print(f"下一次维护大于今天的最小日期为: {date1}")
        else:
            date1 = ""  # 如果没有日期，返回空字符串
        # 计算下一次校准到今天的剩余天数
        if not future_校准_dates.empty:
            date2 = (future_校准_dates.min() - today).days+1  # 剩余天数
            print(f"下一次校准大于今天的最小日期为: {date2}")
        else:
            date2 = ""  # 如果没有日期，返回空字符串
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
        bs_device_data = pdData[["设备名称", "资产编号", "使用情况", "下一次维护", "下一次校准", "维护/校准预警"]]
        # 替换 NaT 为 None (或空字符串)，确保没有无效日期进入 MySQL
        bs_device_data["下一次维护"] = bs_device_data["下一次维护"].apply(lambda x: "-1" if pd.isnull(x) or x == "NaT" else x)
        bs_device_data["下一次校准"] = bs_device_data["下一次校准"].apply(lambda x: "-1" if pd.isnull(x) or x == "NaT" else x)
        bs_device_data = bs_device_data.values.tolist()
        finallList=[]
        for data in bs_device_data:
            if data[-2] == "-1" and data[-3]=="-1":
                data[-2]=None
                data[-3]=None
            elif data[-3]=="-1":
                data[-3]=None
            elif data[-2]=="-1":
                data[-2]=None
            finallList.append(data)
        print(f"finallList:\n{finallList}")
        print(f"finallList的长度为:\n{len(finallList)}")
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
        sql="""UPDATE bs_LargeScreen_device_data
        SET 
            next_maint = DATE(next_maint),
            next_calibration = DATE(next_calibration)
                WHERE next_maint IS NOT NULL OR next_calibration IS NOT NULL;"""
        self.conn.executemany(excute_sql, finallList)
        self.conn.execute(sql)
        # 插入信息管理汇总表
        sql_truncate="TRUNCATE TABLE bs_Large_environment_info;"
        self.conn.execute(sql_truncate)
        deviceInfo=[[str(important_count),str(using_rate),"剩余"+str(date1)+"日","剩余"+str(date2)+"日"]]
        key_list=["import_device","use_rate","maintance_alerts","calibration_alerts"]
        self.conn.batchInsert("bs_Large_environment_info",key_list,deviceInfo)
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
