import pandas as pd
import os


def get_desktop_path():
    """获取系统桌面路径并返回"""
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    return desktop_path


def copy_excel_file(source_file_path, target_file_path):
    """将一个文件的所有内容赋值并写入一个新的文件中"""
    with pd.ExcelFile(source_file_path) as xls:
        with pd.ExcelWriter(target_file_path, engine='xlsxwriter') as writer:
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet_name)
                df.to_excel(writer, sheet_name=sheet_name, index=False)


def write_to_existing_excel(file_path, sheet_name, data, startrow=None, startcol=None):
    """
    将数据写入现有的 Excel 文件的指定 sheet 页。
    """
    # 设置默认值为 0
    if startrow is None:
        startrow = 0
    if startcol is None:
        startcol = 0
    with pd.ExcelWriter(file_path, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
        data.to_excel(writer, sheet_name=sheet_name, index=False)



if __name__ == '__main__':
    systemDesktop = get_desktop_path()
    source_file_path = f'{systemDesktop}\\二系统稽核\\盘点报告表\\20240627.xlsx'
    target_file_path = f'{systemDesktop}\\二系统稽核\\结果\\结果.xlsx'
    
    copy_excel_file(source_file_path, target_file_path)
    
    # 示例调用
    sheet_name = '剩余差异'  # 要写入的 sheet 页名称
    data_to_write = pd.DataFrame({
        '列1': [1, 2, 3],
        '列2': [4, 5, 6],
        '列3': [7, 8, 9]
    })
    
    write_to_existing_excel(target_file_path, sheet_name, data_to_write)
