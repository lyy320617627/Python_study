from datetime import datetime


def get_dates():
    # 获取当前日期
    today = datetime.today()

    # 获取本月的月初日期
    first_day_of_month = today.replace(day=1)

    # 将日期格式化为 YYYY-MM-DD
    today_str = today.strftime("%Y-%m-%d")
    first_day_str = first_day_of_month.strftime("%Y-%m-%d")

    return first_day_str, today_str


# 示例用法
first_day, today = get_dates()
print("本月月初:", first_day)
print("今日日期:", today)
