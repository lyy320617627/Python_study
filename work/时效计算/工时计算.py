import pandas as pd


def process_attendance(file_path, output_file_path):
    # 读取Excel文件，跳过前两行
    df = pd.read_excel(file_path,sheet_name="原始记录",keep_default_na=False,index_col=None, skiprows=2)

    # 输出原始数据框的前几行，查看列名和数据格式
    print(df.head())
    print(df.columns)

    # 确保列名与文件中的实际列名匹配
    if len(df.columns) >= 3:
        df = df.iloc[:, :3]  # 只保留前三列
        df.columns = ["姓名", "考勤日期", "打卡时间"]
    else:
        raise ValueError("文件中的列数少于3列，无法继续处理。")

    # 转换考勤日期和打卡时间为日期时间格式
    df["考勤日期"] = pd.to_datetime(df["考勤日期"])
    df["打卡时间"] = pd.to_datetime(df["打卡时间"])

    # 按姓名和考勤日期分组，计算每组的工作时长（分钟）
    def calculate_work_duration(group):
        # 排序打卡时间
        group = group.sort_values("打卡时间")
        # 计算打卡时间差
        duration = (group["打卡时间"].iloc[-1] - group["打卡时间"].iloc[0]).total_seconds() / 60.0
        return pd.Series({
            "姓名": group["姓名"].iloc[0],
            "考勤日期": group["考勤日期"].iloc[0],
            "工作时长": duration
        })

    result = df.groupby(["姓名", "考勤日期"]).apply(calculate_work_duration).reset_index(drop=True)

    # 将结果写入新的 Excel 文件
    result.to_excel(output_file_path, index=False)


# 示例调用
if __name__ == '__main__':
    input_file_path = r'C:\Users\ly320\Desktop\4月工时.xlsx'
    output_file_path = r'C:\Users\ly320\Desktop\4月工作时间统计.xlsx'
    process_attendance(input_file_path, output_file_path)
