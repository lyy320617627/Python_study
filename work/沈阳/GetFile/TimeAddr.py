from datetime import datetime, timedelta


def get_month_start_and_yesterday():
    today = datetime.today()
    month_start = today.replace(day=1).strftime('%Y-%m-%d')
    yesterday = (today - timedelta(days=1)).strftime('%Y-%m-%d')

    return month_start, yesterday


# 调用函数并打印结果
month_start, yesterday = get_month_start_and_yesterday()
print("本月的第一天:", month_start)
print("昨天的日期:", yesterday)
