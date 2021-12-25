import os, time, logging
from selenium import webdriver
from retrying import retry
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By

# 失败后随机 1-3s 后重试，最多 10 次
@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=10)
def initDriver():
    options = webdriver.FirefoxOptions()
    options.set_preference("security.tls.version.min",1) # https://blog.csdn.net/m0_55391269/article/details/113867365
    try:
        driver = webdriver.Firefox(executable_path=f'{os.getcwd()}/geckodriver.exe', options=options, )
    except:
        logging.error("webdriver初始化失败")
        raise Exception('webdriver初始化失败')
    else:
        #设置超时时间为30s
        driver.set_script_timeout(30)
        logging.info("初始化selenium driver完成")

        return driver

# 失败后随机 3-5s 后重试，最多 10 次
@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=10)
def login(driver):
    logging.info("访问登录页面")
    driver.get("https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/first0")
    time.sleep(10)

    logging.info("读取用户名密码")
    uid = os.environ['ID']
    password = os.environ['PASSWORD']

    logging.info("输入用户名密码")
    driver.find_element_by_xpath('//*[@name="uid"]').send_keys(uid)
    driver.find_element_by_xpath('//*[@name="upw"]').send_keys(password)

    # 点击登录按钮
    logging.info("登录信息门户")
    try:
        driver.find_element_by_xpath('//*[@name="smbtn"]').click()
    except:
        logging.error('登陆失败')
        raise Exception('登陆失败')
    time.sleep(10)

    sbLink=False
    #找出申报的iframe框架
    try:
        sbLink=driver.find_element_by_tag_name("iframe").get_attribute("src")
        #print(sbLink)
    except:
        logging.error('未能找出申报的iframe框架')
        raise Exception('未能找出申报的iframe框架')
    return sbLink

# 失败后随机 3-5s 后重试，最多 6 次
@retry(wait_random_min=3000, wait_random_max=5000, stop_max_attempt_number=6)
def jksb(sbLink,driver):
    logging.info('访问健康申报页面')
    driver.get(sbLink)
    time.sleep(10)

    try:
        driver.find_element_by_xpath('//*[@name="day6"]')
        logging.info('打开健康申报成功')
    except:
        logging.error('打开健康申报失败')
        raise Exception('打开健康申报失败')

    logging.info("点击本人填报")
    form = driver.find_element_by_xpath('//form')
    form.submit()
    time.sleep(10)

    logging.info("选择'绿码'")
    Select(driver.find_element_by_xpath("//select[@name='myvs_13']")).select_by_value('g')
    time.sleep(2)

    logging.info("提交健康申报")
    driver.find_element_by_xpath('//form').submit()
    time.sleep(2)

    logging.info("点击'确认'按钮")
    driver.find_element_by_xpath('//div[text()="确认"]').click()
    time.sleep(1)

    logging.info("完成健康申报")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,format='[%(levelname)s] %(asctime)s %(message)s')
    driver=initDriver()
    sbLink=login(driver)
    time.sleep(2)
    jksb(sbLink,driver)
    driver.quit()

