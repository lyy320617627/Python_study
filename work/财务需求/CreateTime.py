from datetime import datetime, timedelta
import calendar

def get_dates():
    today = datetime.today()
    if today.day >= 5:
        first_day_of_month = today.replace(day=1)
        return (first_day_of_month.year, first_day_of_month.month, first_day_of_month.day),(today.year, today.month, today.day)
    else:
        first_day_of_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
        last_day_of_last_month = today.replace(day=1) - timedelta(days=1)
        return (first_day_of_last_month.year, first_day_of_last_month.month, first_day_of_last_month.day),(last_day_of_last_month.year, last_day_of_last_month.month, last_day_of_last_month.day)
def get_cuurent_day():
    today = datetime.today().day
    print(f"当前日期为当月的第{today}号")
"""
下游价保返利：
当月8-15日每日导出当月1号至导出日数据
当月22-31日每日导出当月1日至导出日数据
次月1-4号导出时间段未上月1号-上个月的最后一天
上游价保返利：

"""
def isDownStreamLoad(number):
    if 1 <= number <= 4 or 8 <= number <= 15 or 22 <= number <= 31:
        return True
    return False
def IsDownLoad():
    today=get_cuurent_day()
    isDownStream=isDownStreamLoad(today)
    return isDownStream

if __name__ == '__main__':
    first_day,current_day=get_dates()
    print(f"上个月或者当月的月份第一天的日期为:{first_day}")
    print(f"上个月或者当月的当日的日期为:{current_day}")
    today=get_cuurent_day()
    isDownStream=IsDownLoad()
    print(f"是否进行下游价保返利下下载文件:{isDownStream}")

