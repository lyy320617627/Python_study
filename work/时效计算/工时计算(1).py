import pandas as pd
import os


def compute():
    # 读取 Excel 文件并展平列名
    df = pd.read_excel(r"C:\Users\ly320\Desktop\4月工时.xlsx", sheet_name='原始记录', header=[2])

    # 展平 MultiIndex 列名
    df.columns = [col[1] if isinstance(col, tuple) else col for col in df.columns]
    print(df.columns)

    # 确保打卡时间列是 datetime 类型
    df['考勤时间'] = pd.to_datetime(df['考勤时间'])
    df = df[df['打卡结果'] == '正常']
    df = df[df['姓名'] == '何必喜']

    # 按日期和时间排序
    df = df.sort_values(by='考勤时间')

    # 提取日期部分
    df['日期'] = df['考勤时间'].dt.date

    # 标记未打卡日期
    df['未打卡日期'] = df['日期'].isin(df['日期'].value_counts()[df['日期'].value_counts() == 1].index).astype(int)

    # 计算每天的打卡时间差
    df['时间差（分钟）'] = df.groupby('日期')['考勤时间'].diff().dt.total_seconds() / 60

    # 移除首个时间记录的 NaN 值
    df['时间差（分钟）'] = df['时间差（分钟）'].fillna(0)
    df = df[['姓名', '考勤时间', '时间差（分钟）', '未打卡日期']]
    df['考勤时间'] = df['考勤时间'].astype(str)

    # 计算不满540分钟[工时分钟/540]
    df['不满540分钟[工时分钟/540]'] = ((540 - df['时间差（分钟）']).clip(lower=0) / 540).round(2)

    # 计算满勤人天[540分钟/人天]
    df['满勤人天[540分钟/人天]'] = (df['时间差（分钟）'] > 540).astype(int) + (df['时间差（分钟）'] / 540).where(
        df['时间差（分钟）'] <= 540, 0).round(2)

    # 计算加班分钟[工时分钟-570]
    df['加班分钟[工时分钟-570]'] = (df['时间差（分钟）'] -480).clip(lower=0)

    # 计算加班人天[加班分钟/480]
    df['加班人天[加班分钟/480]'] = (df['加班分钟[工时分钟-570]'] / 480).round(2)

    # 计算总时列
    df['总时'] = (df['满勤人天[540分钟/人天]'] + df['加班人天[加班分钟/480]']).round(2)

    df['总时'] = df['总时'].astype(float)

    # 计算总时求和列
    total_hours_sum = df['总时'].sum()

    # 添加总时求和列到DataFrame
    df['合计总工时（人/天）'] = [None] * (len(df) - 1) + [total_hours_sum]

    # 计算总时求和列
    total_hours_sum = df['加班人天[加班分钟/480]'].sum()

    # 添加总时求和列到DataFrame
    df['合计加班工时（人/天）'] = [None] * (len(df) - 1) + [total_hours_sum]

    # 计算不满求和列，对满勤人天[540分钟/人天] 小于1的求和，只显示在最后一行
    not_full_sum = df[df['满勤人天[540分钟/人天]'] < 1]['满勤人天[540分钟/人天]'].sum()
    df['有请假工时(人/天)'] = [None] * (len(df) - 1) + [not_full_sum]

    not_full_sum = df[df['满勤人天[540分钟/人天]'] == 1]['满勤人天[540分钟/人天]'].sum()
    df['满勤工时(人/天)'] = [None] * (len(df) - 1) + [not_full_sum]

    # 最后调整顺序
    df = df[['姓名', '考勤时间', '时间差（分钟）', '不满540分钟[工时分钟/540]', '满勤人天[540分钟/人天]',
             '加班分钟[工时分钟-570]',
             '加班人天[加班分钟/480]', '满勤工时(人/天)', '有请假工时(人/天)', '合计加班工时（人/天）',
             '合计总工时（人/天）', '未打卡日期']]

    # 保存结果到新的 Excel 文件
    df.to_excel('打卡记录_带时间差.xlsx', index=False)


compute()
