from MySQLUtil import MySQLUtil
import pandas as pd
class DownLoadData:
    def downLoadData(self):
        conn = MySQLUtil(host="192.168.0.148", port=3306, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
        data=conn.select_all("bs_pur_purchase_result_bill")
        print(f"从数据库中选出的数据长度为:{len(data)}")
        target_list=[]
        for item  in  data:
            if item[7]=="流转中" and item[-3]=="是":
                # print(item)
                target_list.append(item)
        return target_list


if __name__ == '__main__':
    downloadData=DownLoadData()
    data=downloadData.downLoadData()
    print(f"从数据库中查出来的数据长度为:{len(data)}")