import pandas as pd
# 泛全串码查询报表文件读取
class PanFullSerCode:
    def GetData(self,file_path):
        data=pd.read_excel(file_path,keep_default_na=False,index_col=None)
        print(f"文件数据的列名为:{data.columns}")
        print(f"读出来的数据长度为:{len(data)}")
        # 这里只需要返回的是泛全串码查询出来的文件的中的串号做为匹配参照表
        data=data["串号"].values.tolist()
        data=list(set(data))
        panfullsercodeList=data
        print(f"去重后后串码查询报表中的串码为:{panfullsercodeList}")
        print(f"去重后后串码查询报表中的串码长度为:{len(panfullsercodeList)}")
        return panfullsercodeList




if __name__ == '__main__':
    file_path=r'C:\Users\ly320\Desktop\二系统稽核\泛全系统文件下载\串码查询报表.xlsx'
    panfullsercode=PanFullSerCode()
    panfullsercode.GetData(file_path)