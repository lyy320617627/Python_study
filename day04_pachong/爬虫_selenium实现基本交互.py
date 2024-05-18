from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
"""
通过selenium实现基本的操作
# 一些常用的交互函数
# (1)点击:click()
# (2)输入：:send_keys()
# (3)后退操作:browser.back()
# (4)前进操作:browser.forward()
# (5)模拟js滚动:js="document.doucumentElement.scrollTop="100000""
#              browser.execute_script(js) 执行js代码
# (7)获取网页代码:page_source
# (8)退出:browser.quit()
"""