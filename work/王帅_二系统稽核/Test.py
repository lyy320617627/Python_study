import pandas as pd
import os

def get_desktop_path():
    """获取系统桌面路径并返回"""
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    return desktop_path

def main():
    systemDesktop = get_desktop_path()
    file_path = f'{systemDesktop}\\二系统稽核\\泛全系统文件下载\\串号全程跟踪查询报表.xlsx'
    print(f"文件的路径为:{file_path}")
    data = pd.read_excel(file_path, keep_default_na=False, index_col=None)
    data_columns = data.columns.tolist()
    print(f"文件的列名为:{data_columns}")
    # 创建一个新的 DataFrame，其中每列的数据都是 1
    new_row = pd.DataFrame([[1] * len(data_columns)], columns=data_columns)
    # 将新行添加到原始 DataFrame
    # data = pd.concat([data, new_row], ignore_index=True)
    # 保存修改后的 DataFrame 回到 Excel 文件
    new_row.to_excel(file_path, index=False)
    print("已成功填充一行数据，每列的数据都是1")
if __name__ == '__main__':
    list1=[1,2,3,4,5,6,7,8,9,10]
    flag=False
    if flag==False:
        for i  in list1:
            if i ==3:
                break