from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

"""
使用headless模式进行操作谷歌浏览器的操作
"""
chrome_driver="chromedriver.exe"
option=Options()
option.headless=True
service = Service(chrome_driver)
web_page=webdriver.Chrome(service=service,options=option)
web_page.maximize_window()
web_page.get("https://www.baidu.com")
print(web_page.title)