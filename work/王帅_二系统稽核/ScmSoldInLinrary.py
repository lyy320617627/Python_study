import pandas as pd


class ScmSoldInLinrary:
    def GetSoldInLinrary(self, file_path):
        data = pd.read_excel(file_path, keep_default_na=False, index_col=None)
        print(f'文件的列名为:{data.columns}')
        print(f'文件的读取出来的数据长度为:{len(data)}')

        # 筛选已销售且库存地点为L001或109S的数据
        data = data[(data["串码状态描述"] == "已销售") &
                    ((data["库存地点"] == "L001") | (data["库存地点"] == "109S"))]

        # 使用双层括号来选择多列数据
        data = data["串码"]
        soldInLinraryList = data.values.tolist()
        soldInLinraryList=list(set(soldInLinraryList))
        print(f"SCM系统中已销售并且库存地点为:100L或者109S的数据为{soldInLinraryList}")
        print(f"SCM系统中已销售并且库存地点为100L或者109S的数据去重后的长度为：{len(soldInLinraryList)}")
        return data


if __name__ == '__main__':
    file_path = r'C:\Users\ly320\Desktop\二系统稽核\ScmDownLoad\SCM在库已售串码记录文件.xlsx'
    scmSold = ScmSoldInLinrary()
    scmSoldDataList = scmSold.GetSoldInLinrary(file_path)
