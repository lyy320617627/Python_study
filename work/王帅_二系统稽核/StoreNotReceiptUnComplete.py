"""
原因四：门店未确认收货（未完成）
"""
import pandas as pd
class StoreNotReceiptUnComplete:
    def storeNotReceiptUnComplete(self,file_path):
        data=pd.read_excel(file_path,keep_default_na=False,index_col=None)
        data=data["串号"]
        data=data.values.tolist()
        data=list(set(data))
        print(f"从采购订单文件筛选出来的数据为:{data}")
        print(f"从采购订单文件筛选出来的数据长度为：{len(data)}")
        return data










if __name__ == '__main__':
    file_path1=r'C:\Users\ly320\Desktop\二系统稽核\泛全系统文件下载\导出采购明细（串码级别）.xlsx'
    stroneNotReceiptUncomplete=StoreNotReceiptUnComplete()
    storeNotReceiptUnCompleteTargetList=stroneNotReceiptUncomplete.storeNotReceiptUnComplete(file_path1)