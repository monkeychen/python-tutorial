import time
from selenium import webdriver

browser = webdriver.Chrome()
# browser.get('https://mail.10086.cn/')
browser.get("http://www.baidu.com")
# ########百度输入框的定位方式##########
# 通过id方式定位
browser.find_element_by_id("kw").send_keys("selenium")
# 通过name方式定位
# browser.find_element_by_name("wd").send_keys("selenium")
# 通过tag name方式定位
# # browser.find_element_by_tag_name("input").send_keys("selenium")
# 通过class name方式定位
# browser.find_element_by_class_name("s_ipt").send_keys("selenium")
# 通过CSS方式定位
# browser.find_element_by_css_selector("#kw").send_keys("selenium")
# 通过xpath方式定位
# browser.find_element_by_xpath("//input[@id='kw']").send_keys("selenium")
# ###########################################
browser.find_element_by_id("su").click()
time.sleep(30)
browser.quit()


"""
chrome_options = webdriver.ChromeOptions()
# 使用headless无界面浏览器模式
# 增加无界面选项
chrome_options.add_argument('--headless')
# 如果不加这个选项，有时定位会出现问题
chrome_options.add_argument('--disable-gpu')

# 启动浏览器，获取网页源代码
browser = webdriver.Chrome(chrome_options=chrome_options)
mainUrl = "https://www.taobao.com/"
browser.get(mainUrl)
print(f"browser text = {browser.page_source}")
browser.quit()
"""
