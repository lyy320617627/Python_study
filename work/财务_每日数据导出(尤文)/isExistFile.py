import os


def delete_file_if_exists(file_path):
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"文件已删除: {file_path}")
        except Exception as e:
            print(f"删除文件时出错: {e}")
    else:
        print(f"文件不存在: {file_path}")


# 示例用法
file_path = r"C:\Users\ly320\Desktop\银行交易明细自动导出-需求对接测试.xlsx"  # 替换为你的文件路径
delete_file_if_exists(file_path)
