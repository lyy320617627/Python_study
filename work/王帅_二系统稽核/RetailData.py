import pandas as pd
from datetime import datetime

class RetailData:
    def ReadData(self, filename):
        # 读取 '泛智能未录' 表
        data = pd.read_excel(filename, sheet_name='泛智能未录', keep_default_na=False, header=0, index_col=None)
        data = data.iloc[:, [3, 22, 34]]
        data.columns = ['录入日期', '串号', '备注']
        data = data[data['串号'] != ""]
        print(f"从泛智能未录入的数据长度为: {len(data)}")
        print(f"从泛智能未录入的数据类型为: {type(data.iloc[:, 0])}")

        # 读取 '宁波未录' 表
        data2 = pd.read_excel(filename, sheet_name='宁波未录', keep_default_na=False, header=0, index_col=None)
        data2 = data2.iloc[:, [2, 21, 30]]
        data2.columns = ['录入日期', '串号', '备注']
        data2 = data2[data2['串号'] != ""]
        print(f"从宁波未录入的数据长度为: {len(data2)}")
        data=pd.concat([data, data2])
        for index, row in data.iterrows():
            # 将字符串转换为 datetime 对象
            date_str = row['录入日期']
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                # 提取年和月并拼接成所需的格式
                formatted_date = date_obj.strftime('%Y%m')
                row['录入日期'] = formatted_date
            except ValueError:
                print(f"日期格式不正确: {date_str}")
        print(f"使用concat方法后，变成的类型是:{type(pd.concat([data, data2]))}")
        return data
if __name__ == '__main__':
    file_path = r'C:\Users\ly320\Desktop\零售未录数据7.9.xlsx'
    dataDeal = RetailData()
    data = dataDeal.ReadData(file_path)
    print(f"从零售未录入表中筛选出来的数据长度为: {len(data)}")
    print(f"从零售未录入表中筛选出来的数据类型为: {type(data)}")
    # for index, row in data.iterrows():
    #     # 将字符串转换为 datetime 对象
    #     date_str = row['录入日期']
    #     try:
    #         date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    #         # 提取年和月并拼接成所需的格式
    #         formatted_date = date_obj.strftime('%Y%m')
    #         row['录入日期'] = formatted_date
    #     except ValueError:
    #         print(f"日期格式不正确: {date_str}")
