import requests
from bs4 import BeautifulSoup
from day04_pachong import scrapy

# 创建 session 对象
session = requests.Session()

# 获取登录页面
log_url = "https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.aspx"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}
response = session.get(url=log_url, headers=headers)
content = response.text

# 解析登录页面
soup = BeautifulSoup(content, 'lxml')
viewstate = soup.select_one("#__VIEWSTATE").attrs.get('value')
viewstategenerator = soup.select_one('#__VIEWSTATEGENERATOR').attrs.get('value')

# 获取验证码的 URL 地址
code_url = 'https://so.gushiwen.cn' + soup.select_one("#imgCode").attrs.get('src')

# 下载验证码图片
response_code = session.get(code_url)
with open('code.jpg', 'wb') as fp:
    fp.write(response_code.content)

# 手动输入验证码
code_name = input("请输入你的验证码: ")

# 准备登录的数据
post_url = "https://so.gushiwen.cn/user/login.aspx?from=http%3a%2f%2fso.gushiwen.cn%2fuser%2fcollect.aspx"
post_data = {
    '__VIEWSTATE': viewstate,
    '__VIEWSTATEGENERATOR': viewstategenerator,
    'from': 'https://www.gushiwen.cn/',
    'email': 'ly320617627@163.com',
    'pwd': 'www.jj123456',
    'code': code_name,
    'denglu': '登录'
}

# 提交登录表单
response_post = session.post(url=post_url, headers=headers, data=post_data)
content_post = response_post.text

# 保存登录后的页面内容
with open('gushiwen.html', 'w', encoding='utf-8') as fp:
    fp.write(content_post)

print("登录结果已保存到 gushiwen.html")
