import re
def extract_numbers(text):
    # 使用正则表达式 \d+ 来匹配所有连续的数字
    numbers = re.findall(r'\d+', text)
    return numbers


if __name__ == '__main__':
    # 示例字符串
    text = "系统数据导出均需审批。导出申请单：1261288250375454720已提交，详情至【导出报表下载】页查看"

    # 提取所有数字
    numbers = extract_numbers(text)
    numbers=numbers[0]
    print(numbers)
    print(type(numbers))
