import pandas as pd
from datetime import datetime


class IsReasonExist:
    def Filter_excel(self, excel_path):
        # 读取 Excel 文件
        df = pd.read_excel(excel_path, keep_default_na=False, index_col=None, header=0)

        # 去除列名前后的空格
        df.columns = df.columns.str.strip()

        # 将日期列转换为 datetime 格式
        df['过账日期'] = pd.to_datetime(df['过账日期'], format='%Y/%m/%d', errors='coerce')

        # 指定的日期
        specified_date = datetime.strptime('2024-05-21', '%Y-%m-%d')

        # 进行判断，筛选出符合条件的行
        matching_rows = df[df['过账日期'] >= specified_date]
        return matching_rows

    def data_reasonOne(self, num, DataForm):
        # 将 '客户' 列转换为字符串类型
        DataForm['客户'] = DataForm['客户'].astype(str)

        data = DataForm[(DataForm["客户明细账类别"] == "销售退货") & (DataForm["客户"] == num) &(DataForm["销售凭证"].notna())]
        print(data)
        data = data.groupby("销售凭证")["本币金额"].apply(lambda x: x.abs().sum()).reset_index()
        data_list=data.values.tolist()
        dict_data_list=[]
        print(data)
        print(data_list)
        dict_data={}
        for data in data_list:
            dict_data[data[0]]=data[1]
        print(f"data_reason1_dict: {dict_data}")
        return dict_data
    def data_reasonTwo(self, num, DataForm):
        # 将 '客户' 列转换为字符串类型
        DataForm['客户'] = DataForm['客户'].astype(str)
        # 筛选条件：客户明细账类别为"确认返利使用"或"确认价保使用"，并且客户等于num
        data = DataForm[((DataForm["客户明细账类别"] == "确认返利使用") |
                         (DataForm["客户明细账类别"] == "确认价保使用")) &
                        (DataForm["客户"] == num)]
        data = data[data['本币金额']>0]
        data = data.groupby("客户")["本币金额"].apply(lambda x: x.abs().sum()).reset_index()
        print("-------------------------")
        print(f"分组之后的数据是:{data}")
        print(type(data))
        data_list=data.values.tolist()
        print(data_list)
        print(data_list[0])
        reason_dict_data={}
        # reason_dict_data[data_list[0][0]]=data_list[0][1]
        print(data_list[0][0])
        print(data_list[0][1])
        return data_list[0][0],data_list[0][1]
    def isReason1(self,jb_datalist,jbfl_datalist,dict_data):
        jb_account=0
        jbfl_account=0
        for jbfl in jbfl_datalist:
            if jbfl[14] in dict_data:
                jbfl_account+=float(jbfl[12])
        for jb in jb_datalist:
            if jb in dict_data:
                name=jb[-2][-10:]
                if name in dict_data:
                    jb_account+=float(jb[11])
        total_count=jbfl_account+jb_account
        for key,value in dict_data.items():
            if value==total_count:
                return True
            else:
                return False





if __name__ == '__main__':
    num = "80005083"
    excel_object = IsReasonExist()
    excel_path = r'C:\Users\ly320\Desktop\三系统余额稽核二阶段\scm_download\scmDataDownLoad.xlsx'
    filter_data = excel_object.Filter_excel(excel_path)
    print(f"data数据的长度是:{len(filter_data)}")
    isExistReason1 = excel_object.data_reasonOne(num, filter_data)
    # print(f"isExistReason1={isExistReason1}")
    isExistReason2 = excel_object.data_reasonTwo(num, filter_data)
    print(f"isExistReason2:{isExistReason2}")

