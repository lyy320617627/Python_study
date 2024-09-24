import pandas as pd

class Cancel:
    def getScmNum(self, num, excel_cancel_path):
        # 读取 Excel 文件
        data = pd.read_excel(excel_cancel_path, index_col=None, sheet_name="撤单", keep_default_na=False)
        # 去除列名前后的空格
        data.columns = data.columns.str.strip()
        # 将 'SCM编码' 列转换为字符串类型
        data["SCM编码"] = data["SCM编码"].astype(str)
        data["SCM订单号"] = data["SCM订单号"].astype(str)
        # 筛选数据
        filtered_data = data[(data["SCM编码"] == num) & (data["SCM订单号"] != "/")]
        boss_num_list = []
        for index, row in filtered_data.iterrows():
            boss_num_list.append(row["BOSS订单号"])
        return boss_num_list

if __name__ == '__main__':
    num = "0080041766"
    # 定义撤单台账文件所在的目录
    excel_cancel_path = r"C:\Users\ly320\Desktop\三系余额稽核\撤单台账5.21.xlsx"
    cancel = Cancel()
    boss_num_list = cancel.getScmNum(num, excel_cancel_path)
    print(f"boss_num_list: {boss_num_list}")
