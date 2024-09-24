from datetime import datetime, timedelta


def get_yesterday_time_range():
    # 获取当前时间
    now = datetime.now()

    # 计算昨天的日期
    yesterday = now - timedelta(days=1)

    # 生成昨天的开始时间和结束时间
    start_time = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    end_time = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)

    # 格式化时间字符串
    start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
    end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S")

    return start_time_str, end_time_str


# 示例调用
start_time, end_time = get_yesterday_time_range()
print(f"Start Time: {start_time}")
print(f"End Time: {end_time}")
