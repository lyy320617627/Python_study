"""
通过代码将excel表格里的内容转换成为markdown类型
"""
import pandas as pd

def excelToMd(path, sheetName="Sheet1"):
    df = pd.read_excel(path, sheetName)
    title = "|"
    splitLine = "|"
    for i in df.columns.values:
        title = title + i + "|"
        splitLine = splitLine + "--" + "|"
    print(title)
    print(splitLine)
    for i in df.iterrows():
        row = "|"
        for j in df.columns.values:
            row = row + str(i[1][j]) + "|"
        print(row.replace("nan", "-"))

excelToMd("C:\\Users\\ly320\\Desktop\\接单.xlsx")