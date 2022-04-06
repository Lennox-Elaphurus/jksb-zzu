import os, time, logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from retrying import retry
from util import get_img
import ddddocr

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
        driver.set_script_timeout(3)
        logging.info("webdriver初始化完成")

        return driver

# 失败后随机 3-5s 后重试，最多 10 次
@retry(wait_random_min=3000, wait_random_max=5000, stop_max_attempt_number=10)
def login(driver,uid,password,ocr):
    logging.info("访问登录页面")
    driver.get("https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/first0")
    time.sleep(5)

    logging.info("输入用户名密码")
    driver.find_element_by_xpath('//*[@name="uid"]').send_keys(uid)
    driver.find_element_by_xpath('//*[@name="upw"]').send_keys(password)

    try:
        img_element=driver.find_element_byxpath('//*[@id="myimg6"]')
    except:
        logging.info("未找到验证码提示,可能不需要输入验证码")
    else:
        img_link=img_element.get_attribute('src')
        # print(img_link)

        # 识别验证码
        code = get_img(img_link,ocr,driver)

        logging.info("输入验证码")
        driver.find_element_by_xpath('//*[@name="ver6"]').send_keys(code)

    # 点击登录按钮
    logging.info("点击登录按钮")
    try:
        driver.find_element_by_xpath('//*[@name="smbtn"]').click()
    except:
        logging.error('登陆失败')
        raise Exception('登陆失败')
    time.sleep(5)

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
def jksb(sb_link,driver,uid):
    logging.info('访问健康申报页面')
    driver.get(sb_link)
    # print(sb_link)
    time.sleep(5)

    try:
        driver.find_element_by_xpath('//*[@name="zzj_fun_426"]')
        logging.info('打开健康申报成功')
    except:
        logging.error('打开健康申报失败')
        raise Exception('打开健康申报失败')

    # report_message = driver.find_element_by_xpath("//*[@id='bak_0']/div[5]/span").text
    # if report_message == "今日您已经填报过了":
    #     logging.info("该uid今日已经填报过了")
    #     return

    logging.info("点击本人填报")
    form = driver.find_element_by_xpath('//form')
    form.submit()
    time.sleep(5)

    # logging.info("选择'绿码'")
    # Select(driver.find_element_by_xpath("//select[@name='myvs_13']")).select_by_value('g')
    # time.sleep(2)

    try:
        logging.info("提交健康申报")
        driver.find_element_by_xpath('//form').submit()
        time.sleep(1)
    except Exception as e:
        logging.error("提交健康申报失败")
        logging.error(e.args)
        raise Exception("提交健康申报失败")

    try:
        logging.info("点击'确认'按钮")
        driver.get("https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/endok?uid="+uid)
        time.sleep(1)
    except Exception as e:
        logging.error("点击'确认'失败")
        logging.error(e.args)
        raise Exception("点击'确认'失败")
    else:
        logging.info("完成健康申报")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,format='[%(levelname)s] %(asctime)s %(message)s')
    driver=initDriver()

    ocr = ddddocr.DdddOcr()
    logging.info("初始化ddddocr完成")

    logging.info("读取用户名密码")
    try:
        uids = os.environ['ID'].split()
        passwords = os.environ['PASSWORD'].split()
    except:
        logging.error("读取用户名密码失败,请检查Github Actions的secrets是否正确输入")
        raise Exception('读取用户名密码失败')
    else:
        for i in range(len(uids)):
            sb_link=login(driver,uids[i],passwords[i],ocr)
            jksb(sb_link,driver,uids[i])
            logging.info(str(i+1) + " finished.")
    driver.quit()

