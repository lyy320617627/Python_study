import pandas as pd
import pymysql

from MySQLUtil import MySQLUtil
import openpyxl
import xlwt







if __name__ == '__main__':
    # conn = MySQLUtil(host="192.168.0.148", port=3306, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
    # data=conn.select_all("kf_chat_detail_info")
    # print(data)
    # data=list(data)
    # customer_data=[]
    # agent_data=[]
    # for i in data:
    #     if data[5]=='customer':
    #         customer_data.append(i)
    #     elif data[5]=='agent':
    #         agent_data.append(i)
    # customer_excel=pd.DataFrame(data=customer_data)
    # huizong_excel=pd.DataFrame(data=data)
    # agent_excel=pd.DataFrame(data=agent_data)
    # excel_path='C:\\Users\\ly320\\Desktop\\机器人日常对话数据抓取_.xlsx'
    # write=pd.ExcelWriter(excel_path)
    # # customer_excel.to_excel(write,sheet_name='客户')
    # huizong_excel.to_excel(excel_path,sheet_name='sheet1',index=False)
    # # agent_excel.to_excel(write,sheet_name='客服')
    # write.close()

    # 建立数据库连接
    conn = pymysql.connect(host="192.168.0.148", port=3306, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")

    # 查询数据
    query = "SELECT * FROM kf_chat_detail_info"
    df = pd.read_sql(query, conn)
    selected_data = df[df['flag'] == 'customer']
    selected_data=selected_data.drop_duplicates(subset='content')
    # 关闭数据库连接
    conn.close()

    # 将数据写入 Excel 文件
    # customer_excel=pd.DataFrame(customer_data)
    excel_file_path = "C:\\Users\\ly320\\Desktop\\机器人客户问题数据抓取.xlsx"
    # df.to_excel(excel_file_path, index=False)
    selected_data.to_excel(excel_file_path, index=False)

    print("Data has been written to Excel file:", excel_file_path)






