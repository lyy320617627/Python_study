import time
import pandas as pd
import os
from datetime import datetime
import zipfile
from sendmessageTest import SendMessage

class DataFilter:
    def get_date_range(self):
        today = datetime.today()
        month_start = today.replace(day=1)
        month_start_str = month_start.strftime('%m.%d').lstrip('0')
        today_str = today.strftime('%m.%d').lstrip('0')
        return f"{month_start_str}-{today_str}"

    def get_desktop_path(self):
        return os.path.join(os.path.expanduser("~"), "Desktop")

    def __init__(self):
        self.fileList = []
        self.desktop_path = self.get_desktop_path()
        self.time_format = self.get_date_range()
        self.__path__ = os.path.join(self.desktop_path, "司库系统文件导出.xlsx")
        self.zip_file_name = os.path.join(self.desktop_path, f"司库系统导出文件汇总({self.time_format}).zip")

    def data_filter(self):
        print(f"文件的路径为: {self.__path__}")
        # 读取Excel文件，使用第一行为列名
        data = pd.read_excel(self.__path__, keep_default_na=False, index_col=None, header=0)
        print(f"从文件中读取到的数据为:\n{data}")
        # 假设银行账号列的列名为 '银行账号'
        grouped_data = data.groupby('银行账号')
        # 遍历每个分组并输出到不同的Excel文件
        for bank_account, group in grouped_data:
            file_name = ""
            if bank_account == "33001616627053003737":
                file_name = f"3737({self.time_format}).xlsx"
            elif bank_account == "19025201040019973":
                file_name = f"9973({self.time_format}).xlsx"
            elif bank_account == "8888015100005058":
                file_name = f"财务公司支出户5058({self.time_format}).xlsx"
            elif bank_account == "8888014300006429":
                file_name = f"财务公司收入户6429({self.time_format}).xlsx"
            elif bank_account == "33101985136050508425":
                file_name = f"宁波建行8425({self.time_format}).xlsx"
            elif bank_account == "3901110019200177871":
                file_name = f"宁波工行7871({self.time_format}).xlsx"

            if file_name:
                file_path = os.path.join(self.desktop_path, file_name)
                self.fileList.append(file_path)
                group.to_excel(file_path, index=False)

    def compress_files(self):
        # 创建zip文件并写入每个文件
        with zipfile.ZipFile(self.zip_file_name, 'w') as zipf:
            for file_path in self.fileList:
                # 将文件写入压缩文件
                zipf.write(file_path, os.path.basename(file_path))

        print(f"文件已压缩为: {self.zip_file_name}")

    def is_exists_file(self, timeout=120):
        """检查文件是否存在，设置超时时间（秒）"""
        start_time = time.time()
        while not os.path.exists(self.__path__):
            print(f"等待文件: {self.__path__} 下载...")
            time.sleep(5)  # 每5秒检查一次
            if time.time() - start_time > timeout:
                print("等待超时，文件仍未找到。")
                return False
        return True


def main():
    dataFilter = DataFilter()
    dataFilter.data_filter()
    dataFilter.compress_files()

    # # 确保文件已压缩成功后，再发送消息
    # if os.path.exists(dataFilter.zip_file_name):
    #     sendmessage = SendMessage()
    #     sendmessage.send_message()
    # else:
    #     print(f"压缩文件未找到: {dataFilter.zip_file_name}")

main()
