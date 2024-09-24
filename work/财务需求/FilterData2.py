import pandas as pd

# 读取文件
file_path = r'C:\Users\ly320\Desktop\上游价保返利文件.xlsx'
df = pd.read_excel(file_path)
# 找到重复的行
duplicates = df[df.duplicated(subset=["折让单号", "折让单项目"], keep=False)]

# 找到不重复的行
non_duplicates = df.drop_duplicates(subset=["折让单号", "折让单项目"], keep=False)

# 打印筛选掉重复数据后的值
print("筛选掉重复数据后的值：")
print(non_duplicates)

# 打印被筛选掉的重复数据的值
print("被筛选掉的重复数据的值：")
print(duplicates)
