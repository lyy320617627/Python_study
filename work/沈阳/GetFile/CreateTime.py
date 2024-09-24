from datetime import datetime, timedelta


def get_month_start_and_yesterday():
    today = datetime.today()
    # 本月的第一天，格式为 YYYY-MM-DD 00:00:00
    month_start = today.replace(day=1).strftime('%Y-%m-%d 00:00:00')
    # 昨天的日期，格式为 YYYY-MM-DD 23:59:59
    yesterday = (today - timedelta(days=1)).strftime('%Y-%m-%d 23:59:59')

    return month_start, yesterday


# 调用函数并打印结果
month_start, yesterday = get_month_start_and_yesterday()
print("本月的第一天:", month_start)
print("昨天的日期:", yesterday)
