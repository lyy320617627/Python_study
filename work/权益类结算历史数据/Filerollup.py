import pandas as pd
import os
from MySQLUtil import MySQLUtil


class Filerollup:
    def list_files_in_directory(self, directory_path):
        all_entries = os.listdir(directory_path)
        files = [entry for entry in all_entries if os.path.isfile(os.path.join(directory_path, entry))]
        return files

    def get_all_sheets(self, excel_file_path):
        try:
            xls = pd.ExcelFile(excel_file_path)
            sheet_names = xls.sheet_names
            return sheet_names
        except Exception as e:
            print(f"An error occurred while getting sheets from file {excel_file_path}: {e}")
            return []

    def get_sheet_columns(self, excel_file_path, sheet_name):
        try:
            df = pd.read_excel(excel_file_path, sheet_name=sheet_name, nrows=0)
            columns = df.columns.tolist()
            return columns
        except Exception as e:
            print(f"An error occurred while getting columns from sheet {sheet_name} in file {excel_file_path}: {e}")
            return []

    def filerollup(self, excel_file_path):
        sheet_names = self.get_all_sheets(excel_file_path)
        temp_total_list = []
        required_columns = ["IMEI", "办理月份", "稽核标记", "结算金额", "客户编码", "客户名称", "品牌", "物料编码",
                            "物料描述", "类型", "业务类型"]

        for sheet in sheet_names:
            columns = self.get_sheet_columns(excel_file_path, sheet)
            if all(column in columns for column in required_columns):
                data = pd.read_excel(excel_file_path, sheet_name=sheet, keep_default_na=False, header=0, index_col=None)
                data = data[required_columns]
                data = data[data["稽核标记"].str.contains("本期结算")]
                data = data.where(pd.notnull(data), "")  # 将NaN替换为空字符串
                data['办理月份'] = data['办理月份'].astype(str)
                data = data.values.tolist()
                temp_total_list.extend(data)
                print(f"文件 {excel_file_path} 的 {sheet} 数据 长度为 {len(temp_total_list)}")
            else:
                pass

        return temp_total_list

    def filerollupDirectory(self, directory_path):
        total_list = []
        files = self.list_files_in_directory(directory_path)
        for file in files:
            file_path = os.path.join(directory_path, file)
            temp_total_list = self.filerollup(file_path)
            total_list.extend(temp_total_list)
        print(len(total_list))
        return total_list

    def writeToDataBase(self, table_name, key_list, data_list):
        conn = MySQLUtil(host="192.168.0.148", port=3306, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
        # unique_data = list(set(tuple(row) for row in data_list))
        # print(f"原始数据长度：{len(data_list)}，去重后数据长度：{len(unique_data)}")
        conn.batchInsert(table_name, key_list, data_list)

    def writeToExcel(self, datalist, excel_path):
        data = pd.DataFrame(datalist)
        data.columns = ["IMEI", "办理月份", "稽核标记", "结算金额", "客户编码", "客户名称", "品牌", "物料编码",
                        "物料描述", "类型", "业务类型"]
        data.to_excel(excel_path, index=None)  # 修改这里的参数顺序


if __name__ == '__main__':
    directory_path = r'C:\Users\ly320\Desktop\test'
    filerollup = Filerollup()
    total_list = filerollup.filerollupDirectory(directory_path)
    key_list = ["IMEI", "TransactionMonth", "AuditMark", "SettlementAmount", "CustomerCode", "CustomerName", "Brand",
                "MaterialCode", "MaterialDescription", "Type", "BusinessType"]
    file_path = r'C:\Users\ly320\Desktop\权益类结算历史数据\result.xlsx'
    conn = MySQLUtil(host="192.168.0.148", port=3306, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
    # # data = conn.select_all("bs_historical_of_equity_settle")
    # data=list(total_list)
    # print(f"数据库中读取的数据长度：{len(data)}")
    # filerollup.writeToExcel(total_list, excel_path=file_path)
    # data=pd.read_excel(file_path,keep_default_na=False,index_col=None,header=0)
    # data=data.values.tolist()
    # print(data)
    # print(len(data))
    filerollup.writeToDataBase("bs_historical_of_equity_settle",key_list,total_list)

