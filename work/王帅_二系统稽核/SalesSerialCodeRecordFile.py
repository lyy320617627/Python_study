import pandas as pd

class SalesSerialCodeRecordFile:
    def GetSaleSerCodeRecordData(self, file_path):
        data = pd.read_excel(file_path, keep_default_na=False, index_col=None)
        # 确保销售组织列为字符串类型
        data["销售组织"] = data["销售组织"].astype(str)
        # 使用 | (按位或) 代替 or，并将条件包含在圆括号内
        data = data[(data["销售组织"] == "3300") | (data["销售组织"] == "3302")]
        print(f"文件数据的列名为:{data.columns}")
        print(f"数据为：{data}")
        print(f"数据的长度为：{len(data)}")
        return data  # 返回过滤后的数据

if __name__ == '__main__':
    file_path = r'C:\Users\ly320\Desktop\二系统稽核\ScmDownLoad\SCM销售串码记录文件.xlsx'
    saleSerCodeRecord = SalesSerialCodeRecordFile()
    filtered_data = saleSerCodeRecord.GetSaleSerCodeRecordData(file_path=file_path)