# -*- encoding: utf-8 -*-
"""
@时间 ： 2021/9/15 16:19
@作者 ： 王齐涛
@文件名称： Base.py 
"""
import os
import sys
import time
import allure
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
import traceback
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException, \
    NoSuchWindowException
from common.all_paths import PTHOTOS_PATH
from common.logger_handler import GetLogger
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from io import BytesIO
from PIL import Image, ImageGrab
from selenium.webdriver.common.keys import Keys
import pyautogui
from selenium.webdriver.common.by import By
"""
系统自带的
element_by_id = driver.find_element(By.ID, "element_id")
element_by_id.click()
element_by_id.send_keys()
"""


class MaxRetriesExceededException(Exception):
    def __init__(self, message="最大重试次数已超过"):
        self.message = message
        super().__init__(self.message)


class Base:
    url = "https://localhost:9072"
    # url = "https://analytics.google.com"
    log = GetLogger()

    def __init__(self, browser):
        """
        初始化浏览器
        """
        # option = webdriver.ChromeOptions()
        # option.add_argument('blink-settings=imagesEnabled=false')
        # option.add_argument('--headless')
        self.driver = browser

    def open_url(self):
        """
        打开网址并进行验证，本方法没有传入url参数，是因为在每个page中定义了url，直接调用就好，所以在定义时，不要忘记url参数
        """
        # delete_run_driver("chromedriver.exe")   # 默认杀掉所有未关闭的进程
        self.driver.maximize_window()
        self.log.debug("浏览器最大化")
        try:
            self.driver.set_page_load_timeout(60)   # 设置网页超时加载时间,默认页面会加载完成才进入到下一步
            # selenium.common.exceptions.TimeoutException: Message: timeout: Timed out receiving message from renderer
            self.driver.get(self.url)
            self.log.debug(f"读取url：{self.url}")
        except TimeoutException:
            self.log.error("报错异常 - 网页时间加载超时")
        except Exception as e:
            self.log.error(f"报错异常 ---> : {e}")

    def exit_driver(self):
        """
        退出驱动并关闭所有关联的窗口
        """
        self.driver.quit()
        self.log.debug("退出驱动并关闭所有关联的窗口")
        # delete_run_driver("chromedriver.exe")

# 封装常用的点击和输入文本操作
    def find(self, locator, timeout=20, interval=1):
        """
        定位到元素，locator传入元组 ("id", "value1")
        WebDriverWait:创建一个 WebDriverWait 对象，用于等待页面元素状态的改变。
        .until:调用 WebDriverWait 对象的 until 方法，并传入一个期待条件（Expected Condition）以等待指定定位信息的页面元素出现。
        其中期待条件是visibility_of_element_located：等待页面中至少一个元素匹配指定的定位信息，并且该元素可见
        """
        max_retries = 10
        retries = 0
        while retries < max_retries:
            try:
                if not isinstance(locator, tuple):
                    self.log.error('locator参数类型错误，必须传元祖类型：loc = ("id", "value1")')
                else:
                    self.log.debug(f"正在定位元素信息：定位方式->  {locator[0]}, 元素值->  {locator[1]}")
                    ele = WebDriverWait(self.driver, timeout, interval).until(EC.visibility_of_element_located(locator))
                    if ele:
                        return ele      # 返回的是找到的页面元素对象
                    else:
                        self.log.error(f"定位失败：定位方式->{locator[0]}, 元素值->{locator[1]}")
                        return None
            except ElementClickInterceptedException:
                retries += 1
                self.log.error("find事件  -->  当前元素可能被遮挡或页面未完全加载")
                element = self.driver.find_element(locator)
                webdriver.ActionChains(self.driver).move_to_element(element).click(element).perform()
            except NoSuchElementException:
                self.log.error("find事件  -->  找不到元素")
            except NoSuchWindowException:
                self.log.error("find事件  -->  浏览器窗口已关闭")    # 当尝试操作一个已经关闭的浏览器窗口或标签时触发该异常
                sys.exit()
            except TimeoutException:
                retries += 1
                self.log.error(f"find事件  -->  元素查找超时,正在进行第 {retries+1} 次重试")
            except Exception as e:
                self.log.error(f"find事件  报错异常 ---> : {e}")
                raise
        self.log.error(f"重试 {max_retries} 次后仍未找到元素")
        sys.exit()

    def click_element(self, ele_loc):
        """
        元素点击事件
        """
        try:
            MAX_RETRIES = 20  # 最大重试次数
            retries = 0
            while retries < MAX_RETRIES:
                try:
                    ele = self.find(ele_loc)
                    if ele is not None:
                        # 通过执行 JavaScript 来操作网页，将找到的元素滚动到可视区域内
                        self.driver.execute_script("arguments[0].scrollIntoView(false)", ele)
                    ele.click()
                    self.log.debug(f"点击元素：{ele_loc}")
                    break
                except ElementClickInterceptedException:
                    retries += 1
                    self.log.error(f"点击事件被拦截，尝试重试操作次数 {retries}")
                    time.sleep(10)
                    if retries >= MAX_RETRIES:
                        raise MaxRetriesExceededException("点击操作重试次数已达到最大限制")
                    # element = self.driver.find_element(ele_loc)
                    # webdriver.ActionChains(self.driver).move_to_element(element).click(element).perform()
                except Exception as e:
                    self.log.error(f"click事件 报错异常 ---> : {e}")
                    break
        except MaxRetriesExceededException as m:
            self.log.error(f"捕获到最大重试次数异常: {m}")
            self.exit_driver()
            sys.exit()

    def input_text(self, ele_loc, text, clear_first=True):
        """
        输入文本内容
        """
        time.sleep(1)
        try:
            ele = self.find(ele_loc)
            if clear_first:
                # self.log.debug("清空输入框数据")
                time.sleep(0.5)
                self.driver.execute_script("arguments[0].value = '';", ele)  # 使用脚本清空数据
                ele.clear()
                time.sleep(0.5)
                ele.send_keys(text)
                self.log.debug(f"--->  输入的值：{text}")
            else:
                ele.send_keys(text)
                self.log.debug(f"--->  输入的值：{text}")
        except Exception as e:
            self.log.error(f"send_keys事件 报错异常 --->: {e}")

    def click(self, ele_loc):
        """系统自带的点击事件"""
        try:
            self.log.debug(f"点击事件   --->  系统自带的click")
            element = self.driver.find_element(ele_loc)
            element.click()
        except Exception as e:
            pass

# 模拟鼠标操作（ActionChains模拟网页和PyAutoGUI模拟桌面程序 ）
    def click_js(self, ele_loc):
        """
        通过 JavaScript 来点击一个指定的页面元素.
        第一个参数是 "arguments[0].click();"，表示让定位到的元素执行点击事件，
        第二个参数 js 是要点击的页面元素。
        """
        time.sleep(5)
        js = self.driver.find_element(*ele_loc)
        self.driver.execute_script("arguments[0].click();", js)

    def click_js2(self, ele_loc):
        """模拟鼠标移动到指定元素上并点击该元素"""
        element = self.driver.find_element(*ele_loc)
        ActionChains(self.driver).move_to_element(element).click(element).perform()

    def double_click(self, ele_loc):
        """模拟鼠标双击"""
        ActionChains(self.driver).double_click(ele_loc).perform()

    def move_to_element_1(self, element_locator):
        """将鼠标移动到指定元素"""
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(element_locator)
        )
        ActionChains(self.driver).move_to_element(element).perform()
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)  # 使用 JavaScript 将元素滚动到视口内
        ActionChains(self.driver).move_to_element(element).perform()

    def pyautogui_to_scroll(self, num=4, px=1000):
        """鼠标滚轮向上或向下滚动来实现屏幕内容的上下滚动"""
        for i in range(0, num):
            time.sleep(1)
            pyautogui.scroll(px)     # 默认向下滚动1000个单位
            self.log.debug(f"模拟鼠标第：{i} 次滚动")

    def pyautogui_to_scroll_click_element(self, ele_loc):
        """鼠标滚轮向上或向下滚动来实现屏幕内容的上下滚动，直到元素出现"""
        print(1111111111)
        max_scroll = 10  # 最多滚动次数
        found_element = False
        for i in range(max_scroll):
            time.sleep(1)
            try:
                if self.find(ele_loc) == False:
                    pyautogui.scroll(1000)
                    self.log.debug(f"模拟鼠标第：{i} 次滚动并尝试点击元素")
                found_element = True
                break
            except Exception as e:
                continue
        self.click(ele_loc)
        if not found_element:
            print("未找到元素")

    def pyautogui_to_move(self, screen_width_height):
        """鼠标移动到指定的屏幕坐标"""
        # 获取屏幕的大小 (1746, 349)
        # screen_width, screen_height = pyautogui.size()
        pyautogui.moveTo(screen_width_height)

    def pyautogui_to_click(self, screen_width_height):
        """鼠标移动到指定的屏幕坐标"""
        # 获取屏幕的大小 (1746, 349)
        # screen_width, screen_height = pyautogui.size()
        pyautogui.click(screen_width_height)

    def pyautogui_enter(self):
        pyautogui.press('enter')

# 操作浏览器中的元素
    def get_element(self, ele_loc, ele_name):
        """
        获取某一个元素的属性，比如获取type、name、value标签后面的值(还有其他方法 get_attribute('textContent')获取所有的文本内容)
        """
        text_name = self.find(ele_loc).get_attribute(ele_name)
        return text_name

    def get_element_text(self, ele_loc):
        """
        获取标签对应的文本内容
        """
        time.sleep(1)
        ele = self.find(ele_loc)
        if ele:
            self.log.info(f"获取文本内容：{ele.text}")
            return ele.text
        else:
            self.log.error("未能找到元素，获取文本内容失败")
            return None

    def get_location(self, ele_loc, add_x=0, add_y=0):
        """通过定位元素返回坐标"""
        ele = self.find(ele_loc)
        location = ele.location
        self.log.debug(f"获取到的元素坐标 (x, y):{location['x']} {location['y']}")
        return (location['x']+add_x, location['y']+add_y)

    def len_find(self, ele_loc):
        """GA打点用到，获取子标签的数量"""
        ele = self.find(ele_loc)
        ele2 = ele.find_element_elements(By.XPATH, "*")
        self.log.info(f"统计当前标签{ele_loc}的子标签数量：{len(ele2)}")
        return len(ele2)

    def len_find_2(self, ele_loc):
        """爬取Facebook用到，获取子标签的数量"""
        time.sleep(2)
        parent_element = self.find(ele_loc)
        # 在父元素内查找所有匹配子元素
        child_elements = parent_element.find_elements(*ele_loc)
        # 统计子元素数量
        num_child_elements = len(child_elements)
        self.log.info(f"统计当前标签{ele_loc}的子标签数量：{num_child_elements}")
        return num_child_elements

    def scroll_element_into_view(self, element):
        self.driver.execute_script("window.scrollTo(0, arguments[0].getBoundingClientRect().top)", element)

# 封装显示等待和隐式等待（判断元素的所有方法）
    def get_presence_element(self, locator, timeout=20):
        """
        期待条件，结合WebDriverWait().until使用
        该方法表示：等待页面中至少一个元素匹配指定的定位信息。
        """
        try:
            return WebDriverWait(self.driver, timeout).until(
                ec.presence_of_element_located(locator))
        except Exception as e:
            self.log.error("获取存在元素失败：{}".format(e))

    def get_visible_element(self, locator, timeout=20):
        """
        期待条件，结合WebDriverWait().until使用
        该方法表示：等待页面中至少一个元素匹配指定的定位信息，并且该元素可见。
        """
        try:
            return WebDriverWait(self.driver, timeout).until(
                ec.visibility_of_element_located(locator))
        except Exception as e:
            self.log.error(f"获取可视元素失败：{e}")

    def get_clickable_element(self, locator, timeout=20):
        """
        期待条件，结合WebDriverWait().until使用
        该方法表示：等待页面中至少一个元素匹配指定的定位信息，并且该元素可点击。
        """
        try:
            return WebDriverWait(self.driver, timeout).until(
                ec.element_to_be_clickable(locator))
        except Exception as e:
            self.log.error("可点击元素获取失败：{}".format(e))

    def text_in_element(self, locator, text, timeout=20):
        """
        期待条件，结合WebDriverWait().until使用
        该方法表示：等待指定元素的文本内容包含指定的文本。
        """
        try:
            return WebDriverWait(self.driver, timeout).until(EC.text_to_be_present_in_element(locator, text))
        except Exception as e:
            self.log.error("等待元素的文本内容没有指定的文本：{}".format(e))

    def is_element_clickable(self, locator):
        """
        判断元素是否存在并是可点击状态。
        element.is_displayed():用于验证元素是否已正确加载、是否可见,该方法返回一个布尔值
        element.is_enabled():用于验证元素是否处于可以操作的状态,该方法返回一个布尔值
        """
        try:
            element = self.find(locator)
            if element.is_displayed() and element.is_enabled():
                return True
            else:
                return False
        except TimeoutException:
            self.log.error(f"Timeout while waiting for element {locator} to be clickable")
            return False
        except selenium.common.exceptions.ElementNotInteractableException:
            self.log.error("元素不可交互(可能是当前界面元素没有加载出来或者不存在该元素)")
            return False
        except Exception as e:
            self.log.error(f"Error occurred while checking element {locator} clickable status: {e}")
            return False

    def is_element_exist(self, locator, timeout=10):
        """这里find用的是系统自带的driver.find_element,判断元素是否存在"""
        locator_type, locator_value = locator
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((getattr(By, locator_type.upper()), locator_value)))
            return True
        except NoSuchElementException:
            self.log.error(f"元素未找到: 定位器 {locator}")
            return False
        except Exception as e:
            self.log.error(f"发送错误: {e}")
            return False

# 处理浏览器相关操作
    def browser_back(self):
        """
        浏览器导航栏的按钮：后退
        :return:
        """
        self.driver.back()

    def browser_forward(self):
        """
        浏览器导航栏的按钮：前进
        :return:
        """
        self.driver.forward()

    def browser_refresh(self):
        """
        浏览器导航栏的按钮：刷新
        :return:
        """
        self.driver.refresh()

    def scroll_browser(self, x_offset=0, y_offset=100):
        """
        操作浏览器滚动条，向下移动 指定 偏移量
        :param x_offset: 水平滚动偏移量，默认为0
        :param y_offset: 垂直滚动偏移量，默认为100
        """
        self.log.debug(f"操作浏览器滚动条")
        script = f"window.scrollBy({x_offset}, {y_offset});"
        self.driver.execute_script(script)

    def scroll_browser_num(self, num):
        """
        操作浏览器滚动条，基于当前显示的滚动条移动到底
        """
        self.log.debug(f"操作浏览器滚动条")
        for i in range(0, int(num)):
            time.sleep(1)
            script = "window.scrollTo(0, document.body.scrollHeight);"
            self.driver.execute_script(script)

    def scroll_browser_with_scroll_wheel(self, scroll_amount):
        """
        使用鼠标滚轮操作浏览器滚动条
        """
        self.log.debug(f"使用鼠标滚轮操作浏览器滚动条")

        action = ActionChains(self.driver)
        for i in range(0, int(scroll_amount)):
            time.sleep(1)
            action.send_keys(Keys.PAGE_DOWN).perform() # 模拟按下 Page Down 键

    def get_browser_url(self):
        """
        获取浏览器窗口的url
        :return:
        """
        self.log.debug(f"当前浏览器窗口的URL是：{self.driver.current_url}")
        return self.driver.current_url

    def get_title(self):
        """
        获取浏览器的窗口标题
        :return:
        """
        self.driver.title()

    def get_page_source(self):
        """
        获取当前网页的源码
        :return:
        """
        self.driver.page_source()

    # 处理界面框架和窗口曲柄
    def switch_frame_to_163(self, ele):
        login_frame = self.driver.find_element_by_xpath(ele)
        self.driver._switch_to.frame(login_frame)

    # def switch_frame(self, ele_loc,):
    #     """切换页面框架"""
    #     if self.is_element_clickable(ele_loc) == True:
    #         i = 1
    #         while i <= 4:
    #             if self.find_element(ele_loc):
    #                 self.log.debug(f"切换到框架：{ele_loc}")
    #                 self.driver.switch_to.frame(ele_loc[1])
    #                 break
    #             i += 1
    #             time.sleep(3)
    #             self.log.debug(f"执行循环，开始第{i}次查找")
    #         else:
    #             self.log.error(f"没有找到框架或者框架不存在：{ele_loc}")

    def switch_frame(self, ele_loc, operation=None, click_ele=None):
        """
        切换页面框架，这里有两种情况
        1.只是单纯的切换到某个框架，然后是其他操作事件（比如MC的首页登录，需要切换到登录弹窗，然后输入参数登录）
        2.切换到该框架，然后进行关闭操作（比如MC的营销弹窗，需要切换到该框架，然后进行关闭）
        :param ele_loc:框架名称，一般输入 (By.ID, "layui-layer-iframe1")
        :param operation: 需要进行的操作，一般输入 'click'
        :param click_ele:需要进行的操作，一般输入操作的元素
        :return:
        """
        if self.is_element_clickable(ele_loc) == True:
            i = 1
            while i <= 4:
                if self.find(ele_loc):
                    self.log.debug(f"切换到框架：{ele_loc}")
                    if operation:
                        self.driver.switch_to.frame(ele_loc[1])
                        self.click_element(click_ele)
                        self.quit_switch_frame()
                        break
                    self.driver.switch_to.frame(ele_loc[1])
                    break
                i += 1
                time.sleep(3)
                self.log.debug(f"执行循环，开始第{i}次查找")
            else:
                self.log.error(f"没有找到框架或者框架不存在：{ele_loc}")

    def quit_switch_frame(self):
        """切换框架回主文档中的默认内容"""
        self.driver.switch_to.default_content()

    def new_window(self, new_url="输入新的URL地址"):
        """
        生成新的窗口
        :param new_url:
        :return:
        """
        js = "window.open('{}','_blank');"
        self.driver.execute_script(js.format(new_url))  # 生成一个变量存储新的网址

    def switch_new_window(self):
        """
        切换至新窗口
        :return:
        """
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[-1])  # 切换到最新的窗口

    def switch_old_window(self):
        """
        切换至旧窗口
        :return:
        """
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[0])

    def switch_appoint_window(self, index):
        """
        切换至指定的窗口
        :return:
        """
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[index])

    def switch_to_default(self):
        """
        切换回默认窗口
        :return:
        """
        self.driver.switch_to.default_content()

    def exit_window(self):
        """
        关闭当前窗口
        :return:
        """
        self.driver.close()

# 部分断言
    def assert_status_element(self, ele_loc):
        """
        断言备份任务
        """
        num = 0
        while True:
            get_text = self.get_element_text(ele_loc)
            if "成功" in get_text or 'Successful' in get_text:
                self.log.info(f"任务执行成功")
                return get_text
            elif "失败" in get_text or 'Failed' in get_text:
                self.log.error("任务执行失败")
                return get_text
            elif "取消" in get_text or 'Canceled' in get_text:
                self.log.error("任务已取消")
                return get_text
            else:
                self.log.debug("备份中...")
            time.sleep(60)
            num += 1
            self.log.debug(f"循环第 {num} 次")

    def assert_add_device(self, expect_ele):
        """
        断言添加设备
        """
        num = 0
        while True:
            get_text = self.get_element_text(expect_ele)    # 预期结果，失败或者成功
            if "成功" in get_text or 'successfully' in get_text:
                self.log.info(f"设备添加成功")
                return get_text
            elif "失败" in get_text or 'Failed' in get_text:
                self.log.error("设备添加失败")
                return get_text
            else:
                self.log.debug("正在添加")   # 实际结果，获取到的结果一般是 正在添加中
            time.sleep(10)
            num += 1
            self.log.debug(f"循环第 {num} 次")

    # def assert_add_local(self, expect, actual):
    #     """
    #     断言添加位置
    #     """
    #     num = 0
    #     while True:
    #         if expect in actual:
    #             self.log.debug(f"位置添加成功")
    #             break
    #         elif num == 5:
    #             self.log.error("位置添加失败")
    #             break
    #         else:
    #             self.log.debug("正在添加")   # 实际结果，获取到的结果一般是 正在添加中
    #         time.sleep(10)
    #         num += 1
    #         self.log.debug(f"循环第 {num} 次")

# 封装其他方法
    def clear(self, ele_loc):
        """
        清空内容
        :param ele_loc:
        :return:
        """
        ele = self.find(ele_loc)
        ele.clear()
        self.log.debug("清空输入框内容")

    def select(self,ele_loc,method,data):
        """
        操作下拉框选项
        :param ele_loc: 定位下拉框的元素
        :param method: 选择哪一种方法定位下拉框选项
        :param data: 输入的值
        :return:
        """
        ele = self.find(ele_loc)
        ele.click_element()
        if method == "value":
            Select(ele).select_by_value(data)

        elif method == "text":
            Select(ele).select_by_visible_text(data)

        elif method == "index":
            Select(ele).select_by_index(data)

    def upload_files(self, ele_loc, path):
        """
        上传文件：该方法只封装了input属性的上传文件，没有封装div属性
        :param ele_loc:
        :param path: 上传的文件绝对路径，注意转义
        :return:
        """
        try:
            self.input_text(ele_loc, path)

        except Exception:
            self.log.error("上传文件失败：可能是文件路径不对或文件不存在")
            raise

    def pop_up_windows(self):
        """
        处理界面弹窗（有三个选择：获取文件内容、确认、取消）
        :return:
        """
        # text=self.driver.switch_to.alert.text # 获取文本
        self.driver.switch_to.alert.accept()  # 确认
        # self.driver.switch_to.alert.dismiss()  # 取消

    def screenshot(self, name):
        """
        截图（只截图当前浏览器页面，不是全屏）
        :param name:  截图的命名规范 【截屏时间_xx页面_xx操作.png】
        :return:
        """
        catalogue_name = datetime.now().strftime('%Y')  # 一级目录
        file_name = datetime.now().strftime('%m-%d')  # 二级目录
        dateDir = os.path.join(PTHOTOS_PATH, catalogue_name)
        print(dateDir)
        if not os.path.exists(dateDir):
            os.mkdir(dateDir)
        timeDir = os.path.join(dateDir, file_name)
        if not os.path.exists(timeDir):
            os.mkdir(timeDir)
        photo_time = datetime.now().strftime('%H-%M-%S')
        path = os.path.join(timeDir, photo_time + '_' + name + '.png')
        # path = os.path.join(r"N:\MC_UI\report\photos\2023", photo_time + '_' + name + '.png')
        try:
            self.driver.get_screenshot_as_file(path)
            self.log.info(f"截图成功：{photo_time + '_'+ name}.png ,保存路径：{path}")
            return path
        except Exception:
            self.log.error(f"截图失败：{name} ,报错提示：{traceback.print_exc()}")
            raise

    def allure_attach(self, file_path, file_name, file_type):
        """
        上传文件
        :param file_path:
        :param file_name:
        :param file_type:
        :return:
        """
        file_png = open(file_path, mode='rb').read()
        if file_type == "png":
            allure.attach(body=file_png, name=file_name, attachment_type=allure.attachment_type.PNG)
        elif file_type == "jpg":
            allure.attach(body=file_png, name=file_name, attachment_type=allure.attachment_type.JPG)
        elif file_type == "text":
            allure.attach(body=file_png, name=file_name, attachment_type=allure.attachment_type.TEXT)
        else:
            self.log.error("你输入的文件类型暂时不支持上传，需要自己去封装")

    def get_captcha(self, element, path):
        """
        通过定位标签 截图验证码照片
        :param element:
        :param path:
        :return:
        """
        login_kuangjia = (By.ID, 'layui-layer-iframe2')
        self.switch_frame(login_kuangjia)
        location = self.find(element).location  # 获取元素坐标
        size = self.find(element).size
        # print(location,size)
        # 获取当前浏览器窗口的截图，并加载为Pillow的Image对象
        screenshot = self.driver.get_screenshot_as_png()
        screenshot_image = Image.open(BytesIO(screenshot))
        # 裁剪验证码图片
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        # print(left,top,right,bottom)
        captcha_image = screenshot_image.crop((left, top, right, bottom))
        # 保存验证码图片到文件
        captcha_image.save(path+'.png')
        return path+'.png'
