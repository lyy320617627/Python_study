import pandas as pd


def SerCodeToExcel(DataList, file_path):
    SercodeList = []
    for data in DataList:
        SercodeList.append(data[1])  # 假设 data[1] 是要保存的串码
    data = pd.DataFrame(SercodeList)
    data.to_excel(file_path, index=False, header=None, startcol=0,)  # 将 DataFrame 写入 Excel 的 A 列

# 示例使用
DataList = [
    [1, 'Sercode1', '其他数据1'],
    [2, 'Sercode2', '其他数据2'],
    [3, 'Sercode3', '其他数据3'],
]

file_path = 'output.xlsx'
SerCodeToExcel(DataList, file_path)
