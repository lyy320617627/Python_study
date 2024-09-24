from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class GetTime:
    def current_time(self):
    # 获取当前时间
        current_time = datetime.now()
        current_time_formatted = current_time.strftime("%Y-%m-%d")
        return current_time_formatted

    def one_week_ago(self):
        # 获取一周之前的时间
        current_time = datetime.now()
        one_week_ago = current_time - timedelta(weeks=1)
        one_week_ago_formatted = one_week_ago.strftime("%Y-%m-%d")
        return one_week_ago_formatted

if __name__ == '__main__':
    get_time = GetTime()
    current=get_time.current_time()
    one_week_ago=get_time.one_week_ago()
    # 获取当前日期和时间
    now = datetime.now()

    # 将当前时间设置为23:59
    current_date_time = now.replace(hour=23, minute=59, second=0, microsecond=0)

    # 获取六个月前的日期
    six_months_ago = now - relativedelta(months=6)
    # 将时间设置为00:00
    six_months_ago_date_time = six_months_ago.replace(hour=0, minute=0, second=0, microsecond=0)

    print("当前日期时间（23:59）:", current_date_time)
    print("六个月前的日期时间（00:00）:", six_months_ago_date_time)
