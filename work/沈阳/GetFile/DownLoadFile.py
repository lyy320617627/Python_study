from MySQLUtil import MySQLUtil
import os
import pandas as pd

class DownLoadFile:
    def __init__(self):
        self.fileSavePath = self.getDesktopPath()

    def getDesktopPath(self):
        desktopPath = os.path.join(os.path.expanduser("~"), "Desktop")
        filePath = os.path.join(desktopPath, "实时监控数据汇总.xlsx")
        return filePath

    def downLoadFile(self):
        conn2 = MySQLUtil(host="192.168.0.148", port=3306, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
        sql="CALL proc_monitor_rebate_procedures();"
        conn2.execute(sql)
        finallData = conn2.select_all("summary_sale_data")
        print(f"需要导出的数据为：{finallData}")
        print(f"需要导出的数据长度为：{len(finallData)}")

        # 将查询的数据转换为 DataFrame
        finallData = pd.DataFrame(finallData)
        print(f"转换成为 DataFrame 类型的数据为: {type(finallData)}")

        # 设置 DataFrame 的列名
        finallData.columns = [
            "CURRENT_DATE", "product_activity_type", "material_code", "city", 
            "supplier_type", "supplier_name", "product_category", "brand", 
            "product_name", "model_series", "sales", "rebate_total", "rebate_type"
        ]

        # 保存到 Excel 文件
        finallData.to_excel(self.fileSavePath, index=False)  # 指定文件保存路径，不保存索引

if __name__ == '__main__':
    downloadfile = DownLoadFile()
    downloadfile.downLoadFile()
