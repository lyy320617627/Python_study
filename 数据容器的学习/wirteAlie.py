import pandas as pd

# 示例数据列表
data_list = [10, 20, 30, 40, 50]

# 创建 DataFrame
df = pd.DataFrame(data_list, columns=['A'])

# 指定文件路径
excel_file_path = r'C:\Users\ly320\Desktop\export\num_list.xlsx'

# 将 DataFrame 写入 Excel 文件
df.to_excel(excel_file_path, index=False, header=False)
