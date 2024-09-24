from datetime import datetime, timedelta

def get_yesterday_date():
    # 获取今天的日期
    today = datetime.now().date()
    # 计算昨天的日期
    yesterday = today - timedelta(days=1)
    return yesterday

# 测试函数\
if __name__ == '__main__':
    yesterday=get_yesterday_date()
    print(f"昨天的日期类型为:{type(yesterday)}")
    print(f"昨天的日期为：{yesterday}")
