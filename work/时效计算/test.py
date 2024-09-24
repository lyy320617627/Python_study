from datetime import datetime

# 定义两个时间字符串
start_time_str = "2024-06-21 13:45"
end_time_str = "2024-06-21 17:53"

# 将时间字符串转换为 datetime 对象
start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")
end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M")

# 计算时间差
time_difference = end_time - start_time

# 将时间差转换为分钟数
minutes_difference = time_difference.total_seconds() / 60

print(f"两个时间相隔 {minutes_difference} 分钟")
print(float(minutes_difference)/540)