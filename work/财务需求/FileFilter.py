import pandas as pd


def delete_last_row(file_path, output_file_path):
    # 读取 Excel 文件
    df = pd.read_excel(file_path)

    # 删除最后一行
    df = df.iloc[:-1]

    # 将结果写入新的 Excel 文件
    df.to_excel(output_file_path, index=False)


# 示例调用
if __name__ == '__main__':
    input_file_path = r'C:\Users\ly320\Desktop\EXPORT0上游价保返利清单（6月）.XLSX'
    output_file_path = r'C:\Users\ly320\Desktop\EXPORT0上游价保返利清单（6月）.XLSX'
    delete_last_row(input_file_path, output_file_path)
