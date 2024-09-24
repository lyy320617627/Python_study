import  pandas as pd
class SaleOrderNum:
    def getSaleOrderNum(self,file_path,file_path2):

        data=pd.read_excel(file_path,header=None,index_col=None,keep_default_na=False)
        SaleOrderNumList=data.iloc[1:,4]
        print(f"销售订单列表的数据为:{SaleOrderNumList}")
        print(f"销售订单列表的数据长度为为:{len(SaleOrderNumList)}")
        data=pd.DataFrame(SaleOrderNumList)
        data.to_excel(file_path2,startcol=0,header=None,index=False)
if __name__ == '__main__':
    file_path=r'C:\Users\ly320\Desktop\二系统稽核\ScmDownLoad\SCM销售串码记录文件.xlsx'
    file_path2=r'C:\Users\ly320\Desktop\二系统稽核\串码文件\销售订单.xlsx'
    saleOrderNum=SaleOrderNum()
    saleOrderNum.getSaleOrderNum(file_path,file_path2)