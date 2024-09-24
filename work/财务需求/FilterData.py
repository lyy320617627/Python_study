import pandas as pd

# Load the file
file_path = r'C:\Users\ly320\Desktop\上游价保返利文件.xlsx'
data = pd.read_excel(file_path)

# Group by '折让单号' and '折让单项目' and filter for unique values
unique_data = data.drop_duplicates(subset=['折让单号', '折让单项目'])

# Save the filtered data to a new Excel file
unique_data.to_excel('filtered_data.xlsx', index=False)

print("Filtered data saved to 'filtered_data.xlsx'")
