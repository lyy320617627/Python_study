import numpy as np
import xlsxwriter
from tqdm import tqdm
import os

def get_desktop_path():
    if os.name == 'nt':  # Windows
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    else:  # macOS/Linux
        desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
    return desktop
def formula(x, y, z, m, n):
    return 12.017 * x + 1.0079 * y + 15.999 * z + 14.0067 * m + 32.065 * n

def search_quick(assumed_M, formula, M=1000, x=50, y=100, z=50, m=10, n=10):
    max_number = x * y * z * m * n
    matrix = np.zeros((max_number, 5), dtype=np.float32)
    idx = 0
    for i in tqdm(range(x)):
        for j in range(y):
            for k in range(z):
                for l in range(m):
                    for o in range(n):
                        matrix[idx] = [i, j, k, l, o]
                        idx += 1
    print("Calculating formula parameters...")
    result = np.dot(matrix, formula.reshape(-1, 1)).reshape(-1)
    filter_M = result <= M
    matrix = matrix[filter_M]
    result = result[filter_M]
    diff = assumed_M - result
    abs_diff = np.abs(diff)
    idx = np.argsort(abs_diff)
    sorted_matrix = matrix[idx]
    sorted_result = result[idx]
    sorted_diff = diff[idx]

    return sorted_matrix, sorted_result, sorted_diff

def writeinto_excel(max_write, assumed_M, sorted_matrix, sorted_result, sorted_diff):
    desktop_path=get_desktop_path()
    fn =  fn = os.path.join(desktop_path, f'assumed_M_{assumed_M}_output_{max_write}.xlsx')
    workbook = xlsxwriter.Workbook(fn)
    print(f"writing into excel {fn}...")
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'x')
    worksheet.write('B1', 'y')
    worksheet.write('C1', 'z')
    worksheet.write('D1', 'm')
    worksheet.write('E1', 'n')
    worksheet.write('F1', 'Result')
    worksheet.write('G1', 'Difference')
    need_to_write = min(max_write, len(sorted_matrix))
    for i in tqdm(range(need_to_write)):
        worksheet.write(i + 1, 0, sorted_matrix[i, 0])
        worksheet.write(i + 1, 1, sorted_matrix[i, 1])
        worksheet.write(i + 1, 2, sorted_matrix[i, 2])
        worksheet.write(i + 1, 3, sorted_matrix[i, 3])
        worksheet.write(i + 1, 4, sorted_matrix[i, 4])
        worksheet.write(i + 1, 5, sorted_result[i])
        worksheet.write(i + 1, 6, sorted_diff[i])
    workbook.close()
    print(f"Done writing into excel {fn}...")

def test():
    # max_write=int(input(" 写入excel的最大行数"))  # 写入excel的最大行数
    # assumed_M=int(input(" # 希望的分子量"))
    max_write=100 # 写入excel的最大行数
    assumed_M=90# 希望的分子量
    M, x, y, z, m, n = 100, 50, 100, 50, 10, 10  # 约束条件
    formula_values = np.array([12.017, 1.0079, 15.999, 14.0067, 32.065], dtype=np.float32)  # 公式
    sorted_matrix, sorted_result, sorted_diff = search_quick(assumed_M, formula_values, M, x, y, z, m, n)
    writeinto_excel(max_write, assumed_M, sorted_matrix, sorted_result, sorted_diff)

if __name__ == '__main__':
    test()
