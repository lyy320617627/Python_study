# (1) 导入 selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

"""
演示 selenium 操作对象去访问浏览器的基本使用
"""
# (2) 设置 chromedriver 的路径
path = r"E:\\py_workstation\\py_start\\New_Py_learn\\day04_pachong\\chromedriver.exe"

# (3) 创建 Service 对象并指定 ChromeDriver 的路径
service = Service(executable_path=path)

# (4) 创建浏览器操作对象
browser = webdriver.Chrome(service=service,keep_alive=True)
url="http://jd.com"
# (5) 访问网站
browser.get(url)
# 获取网页的源码
content=browser.page_source
print(content)