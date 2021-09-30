import os, time
from selenium import webdriver
from util import get_img, tgbot_send
from retrying import retry
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By

options = webdriver.FirefoxOptions()
options.set_preference("security.tls.version.min",1) #https://blog.csdn.net/m0_55391269/article/details/113867365
driver = webdriver.Firefox(executable_path=f'{os.getcwd()}/geckodriver.exe', options=options)
print("初始化selenium driver完成")

# 失败后随机 3-5s 后重试，最多 10 次
@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=10)
def login():
    print("访问登录页面")
    driver.get("https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/first0")
    time.sleep(2)

    print("读取用户名密码")
    uid = os.environ['ID']
    password = os.environ['PASSWORD']

    print("输入用户名密码")
    driver.find_element_by_xpath('//*[@name="uid"]').send_keys(uid)
    driver.find_element_by_xpath('//*[@name="upw"]').send_keys(password)

    # 点击登录按钮
    print("登录信息门户")
    try:
        driver.find_element_by_xpath('//*[@name="smbtn"]').click()
    except:
        raise Exception('登陆失败')
    time.sleep(2)

    sbLink=False
    #找出申报的iframe框架
    try:
        sbLink=driver.find_element_by_tag_name("iframe").get_attribute("src")
        print(sbLink)
    except:
        raise Exception('未能找出申报的iframe框架')
    return sbLink

# 失败后随机 3-5s 后重试，最多 6 次
@retry(wait_random_min=3000, wait_random_max=5000, stop_max_attempt_number=6)
def jksb(sbLink):
    print('访问健康申报页面')
    driver.get(sbLink)
    time.sleep(2)

    try:
        driver.find_element_by_xpath('//*[@name="day6"]')
        print('打开健康申报成功')
    except:
        time.sleep(10)
        print('打开健康申报失败')
        raise Exception('打开健康申报失败')

    print("点击本人填报")
    form = driver.find_element_by_xpath('//form')
    form.submit()
    time.sleep(2)

    print("选择’绿码‘")
    Select(driver.find_element_by_xpath("//select[@name='myvs_13']")).select_by_value('g')
    time.sleep(2)

    print("提交健康申报")
    driver.find_element_by_xpath('//form').submit()
    time.sleep(2)

    print("点击’确认‘按钮")
    driver.find_element_by_xpath('//div[text()="确认"]').click()
    time.sleep(1)

    print("完成健康申报")

if __name__ == "__main__":
    sbLink=login()
    time.sleep(2)
    try:
        jksb(sbLink)
        driver.quit()
    except:
        print('健康申报失败')
        driver.quit()

