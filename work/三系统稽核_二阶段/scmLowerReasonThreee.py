# 使用提醒:
# 1. xbot包提供软件自动化、数据表格、Excel、日志、AI等功能
# 2. package包提供访问当前应用数据的功能，如获取元素、访问全局变量、获取资源文件等功能
# 3. 当此模块作为流程独立运行时执行main函数
# 4. 可视化流程中可以通过"调用模块"的指令使用此模块
import pandas as pd
from datetime import datetime

def convert_to_datetime(date_str):
    try:
        # 处理格式如 202023/6/21
        date_obj = datetime.strptime(date_str, '%Y%j/%m/%d')
    except ValueError:
        try:
            # 处理其他格式，如 2024-05-21
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Unsupported date format")
    return date_obj

def scmLowerReasonThreeeDataFilter(excel_path,pri_jhri_time):
    df = pd.read_excel(excel_path, keep_default_na=False, index_col=None, header=0, sheet_name="撤单")
    data = df[df["处理日期"].apply(lambda x: convert_to_datetime(x.strftime('%Y-%m-%d')) >= convert_to_datetime(pri_jhri_time))]
    # 筛选出有订单号的行
    data = data[(data['BOSS订单号'].notna()) & (data['BOSS订单号']!="/")]
    # 进一步筛选，选择 B2B 订单号列为空或者为 "/" 的行
    data = data[(data['B2B订单号']=="") | (data['B2B订单号'] == '/')]

    # 进一步筛选，选择订单状态为"惠购侧异常订单"的行，并统计数量
    data=data[data['订单状态'] == '惠购侧异常订单']
    length = len(data)
    print(data)
    print(length)
    ReasonThreeDataList=data.values.tolist()
    print(data)
    print(length)
    print(ReasonThreeDataList)
    return ReasonThreeDataList

if __name__ == '__main__':
    pri_jhrq_time="2024-06-14"
    excel_path=r"C:\Users\ly320\Desktop\三系统余额稽核二阶段\撤单台账\撤单台账6.21.xlsx"
    reasonThreeDataList=scmLowerReasonThreeeDataFilter(excel_path,pri_jhrq_time)
    print(reasonThreeDataList)
    "惠购异常订单撤单，需地市提交资金流程" + str(abs(float(scmLower_loop_item[6]))) + str(abs(float(loop_item[7])))