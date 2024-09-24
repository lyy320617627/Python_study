import pandas as pd

def GetFinallyExcelFile(excel_file_name):
    excel_file_name=r'C:\Users\ly320\Desktop\三系余额稽核\结果\差异原因.xlsx'
    data=pd.read_excel(excel_file_name)
    print(data.columns)
    data=data.values.tolist()
    df=pd.DataFrame(data,columns=['渠道商名称', '渠道商编码', 'scm余额', '惠购+和动力余额', '同步失败订单', '惠购生态订单', '本次差异金额','上次差异金额', '两次差异金额', '差异原因', '上次差异原因'])
    finally_excel_file=r'C:\Users\ly320\Desktop\三系统余额稽核二阶段\result\结果.xlsx'
    df.to_excel(finally_excel_file)



if __name__ == '__main__':
    excel_file_name = r'C:\Users\ly320\Desktop\三系余额稽核\结果\差异原因.xlsx'
    GetFinallyExcelFile(excel_file_name)
    文件汇总