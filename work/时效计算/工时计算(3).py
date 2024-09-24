# coding=utf8
# DOWNLOAD_URL= pip install -i http://pypi.mirrors.ustc.edu.cn/simple/       --trusted-host pypi.mirrors.ustc.edu.cn
"""
    @Author:zhongdf
    @date: 2024/6/19 16:01
"""

import pandas as pd
import os
import math


def compute(file, save_path, name):
    # 读取 Excel 文件
    df = pd.read_excel(file, sheet_name='原始记录', header=2)
    print(df.columns)

    # 确保打卡时间列是 datetime 类型
    df['考勤时间'] = pd.to_datetime(df['考勤时间'])
    df = df[df['打卡结果'] == '正常']
    df = df[df['姓名'] == name]

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
    print(df.head(10))

    # 计算不满540分钟[工时分钟/540]
    df['不满540分钟[工时分钟/540]'] = ((540 - df['时间差（分钟）']).clip(lower=0) / 540).round(5)

    # 计算满勤人天[540分钟/人天]
    df['满勤人天[540分钟/人天]'] = (df['时间差（分钟）'] > 540).astype(int) + (df['时间差（分钟）'] / 540).where(
        df['时间差（分钟）'] <= 540, 0).round(5)

    # 计算加班分钟[工时分钟-570]
    df['加班分钟[工时分钟-570]'] = (df['时间差（分钟）'] - 570).clip(lower=0)

    # 定义取模函数
    def mod_0625(x):
        return ((math.floor(x / 30)) * 30) / 480

    # 计算加班人天[加班分钟/480]
    df['加班人天[加班分钟/480]'] = (df['加班分钟[工时分钟-570]'].apply(mod_0625)).round(5)

    # 计算总时列
    df['总时'] = (df['满勤人天[540分钟/人天]'] + df['加班人天[加班分钟/480]']).round(5)

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

    df = df[['姓名', '考勤时间', '时间差（分钟）', '不满540分钟[工时分钟/540]', '满勤人天[540分钟/人天]',
             '加班分钟[工时分钟-570]',
             '加班人天[加班分钟/480]', '满勤工时(人/天)', '有请假工时(人/天)', '合计加班工时（人/天）',
             '合计总工时（人/天）', '未打卡日期']]

    # 保存结果到新的 Excel 文件
    df.to_excel(save_path, index=False)


# 示例调用
if __name__ == '__main__':
    list_month = [4, 5, 6]
    list_name = ["钟敦峰", "何必喜", "李杨杨", "徐黄超"]

    for month in list_month:
        for name in list_name:
            file = f"C:\\Users\\ly320\\Desktop\\{month}月工时.xlsx"
            print(f"文件地址为: {file}")
            save_dir = f"C:\\Users\\ly320\\Desktop\\工时计算\\{name}"
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, f"{month}月工时.xlsx")
            print(f"{name}保存文件的地址为: {save_path}")
            compute(file, save_path, name)
