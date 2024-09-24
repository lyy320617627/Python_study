import pandas as pd
from datetime import datetime


def group_and_calculate_time_difference(file_path, sheet_name, column_name):
    # 读取Excel文件
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # 过滤出姓名为"何必喜"的行
    df = df[df["姓名"] == "何必喜"]

    # 将时间列转换为datetime类型
    df[column_name] = pd.to_datetime(df[column_name])

    # 创建一个空的列表来存储结果
    results = []

    # 按天分组
    grouped = df.groupby(df[column_name].dt.date)

    for date, group in grouped:
        # 计算组内两两时间差的绝对值，精确到分钟
        times = group[column_name].tolist()
        for i in range(len(times)):
            for j in range(i + 1, len(times)):
                diff = abs((times[i] - times[j]).total_seconds() // 60)
                results.append({'Date': date, 'Time1': times[i], 'Time2': times[j], 'Difference_in_Minutes': diff})

    # 转换结果为DataFrame
    results_df = pd.DataFrame(results)

    return results_df


# 调用函数
file_path = r'C:\Users\ly320\Desktop\中国移动通信集团终端有限公司浙江分公司_考勤报表_20240101-20240201.xlsx'
sheet_name = '原始记录'
column_name = '打卡时间'

result_df = group_and_calculate_time_difference(file_path, sheet_name, column_name)

# 保存结果到Excel
output_file_path = r'C:\Users\ly320\Desktop\time_differences.xlsx'
result_df.to_excel(output_file_path, index=False)
