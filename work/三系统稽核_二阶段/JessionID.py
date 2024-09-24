import requests

# 发送 HTTP GET 请求
response = requests.get('https://www.example.com')

# 获取 Cookie
cookies = response.cookies

# 打印所有 Cookie
for cookie in cookies:
    print(f"{cookie.name}: {cookie.value}")

# 或者将 Cookie 转换为字典形式
cookie_dict = requests.utils.dict_from_cookiejar(cookies)
print(cookie_dict)
