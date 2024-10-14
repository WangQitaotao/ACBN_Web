import sys
import time
from selenium import webdriver
from selenium.common import NoSuchElementException, ElementClickInterceptedException, NoSuchWindowException, \
    TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import random
import hashlib
from datetime import datetime
import ssl
def get_latest_folder(directory):
    # 获取目录下所有的文件和文件夹
    entries = [os.path.join(directory, entry) for entry in os.listdir(directory)]
    # 过滤出所有文件夹
    folders = [entry for entry in entries if os.path.isdir(entry)]
    if not folders:
        return None
    # 按照文件夹的创建时间进行排序，并获取最新的文件夹
    latest_folder = max(folders, key=os.path.getctime)
    # 返回最新文件夹的名称

    return os.path.basename(latest_folder)


def check_vmdk_files(input_path):
    time.sleep(2)
    directory = os.path.join(input_path, get_latest_folder(input_path))
    # 检查目录是否存在
    if not os.path.isdir(directory):
        print(f"目录 {directory} 不存在")
        return False
    # 遍历目录中的文件
    for filename in os.listdir(directory):
        if filename.endswith('.vmdk'):
            print(f"find .vmdk files:  {directory}\{filename}")
            return True
    return False

def generate_unique_file(filepath, size_mb):
    """生成一个指定大小（MB）的文件，并确保内容唯一"""
    size_bytes = size_mb * 1024 * 1024  # 将MB转换为字节
    with open(filepath, 'wb') as f:
        # 生成一个唯一的随机字节序列
        unique_content = os.urandom(size_bytes)
        f.write(unique_content)
    return filepath


def get_md5(filepath):
    """计算文件的MD5哈希"""
    hash_md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def upload_files(network_directory, number):
    num_files = 5
    min_size_mb = 1
    max_size_mb = 10
    # 获取当前时间，并格式化为目录名
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_directory = os.path.join(network_directory, current_time+f"第 {number} 次增量")
    os.makedirs(output_directory, exist_ok=True)  # 创建目录（如果不存在）
    filenames = []
    md5_set = set()
    while len(filenames) < num_files:
        size_mb = random.randint(min_size_mb, max_size_mb)
        filepath = os.path.join(output_directory, f"file_{len(filenames) + 1}.bin")

        # 生成文件并检查其MD5
        generate_unique_file(filepath, size_mb)
        file_md5 = get_md5(filepath)

        if file_md5 not in md5_set:
            md5_set.add(file_md5)
            filenames.append(filepath)
        else:
            # 如果MD5值重复，删除文件并重新生成
            os.remove(filepath)
        # print("生成的文件及其MD5:")
    # for filepath in filenames:
        # print(f"{filepath}: {get_md5(filepath)}")



class Base:
    __gaoji = ("xpath", "//div[@class='nav-wrapper']//button[3]")
    __jixuqianwang = ("xpath", "//a[@class='small-link']")
    __Admin_input_name = ("id", "username")
    __Admin_input_pw = ("id", "password")
    __Admin_input_submit = ("xpath", "//button[@type='submit']")
    __one_menu_backupTask = ("xpath", "//ul[@role='menu']//li[2]//div[@aria-haspopup='true']")
    __two_menu_backupTask = ("xpath", "//a[@href='#/task/backup-task']")

    def __init__(self, browser):
        """
        初始化浏览器
        """
        self.driver = browser
    def open_url(self,url):
        """
        打开网址并进行验证，本方法没有传入url参数，是因为在每个page中定义了url，直接调用就好，所以在定义时，不要忘记url参数
        """
        # delete_run_driver("chromedriver.exe")   # 默认杀掉所有未关闭的进程
        self.driver.maximize_window()
        # print("浏览器最大化")
        try:
            self.driver.set_page_load_timeout(60)   # 设置网页超时加载时间,默认页面会加载完成才进入到下一步
            # selenium.common.exceptions.TimeoutException: Message: timeout: Timed out receiving message from renderer
            self.driver.get(url)
        except TimeoutException:
            print("报错异常 - 网页时间加载超时")
        except Exception as e:
            print(f"报错异常 ---> : {e}")
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
                    print('locator参数类型错误，必须传元祖类型：loc = ("id", "value1")')
                else:
                    # print(f"正在定位元素信息：定位方式->  {locator[0]}, 元素值->  {locator[1]}")
                    ele = WebDriverWait(self.driver, timeout, interval).until(EC.visibility_of_element_located(locator))
                    if ele:
                        return ele      # 返回的是找到的页面元素对象
                    else:
                        print(f"定位失败：定位方式->{locator[0]}, 元素值->{locator[1]}")
                        return None
            except ElementClickInterceptedException:
                retries += 1
                print("find事件  -->  当前元素可能被遮挡或页面未完全加载")
                element = self.driver.find_element(locator)
                webdriver.ActionChains(self.driver).move_to_element(element).click(element).perform()
            except NoSuchElementException:
                print("find事件  -->  找不到元素")
            except NoSuchWindowException:
                print("find事件  -->  浏览器窗口已关闭")    # 当尝试操作一个已经关闭的浏览器窗口或标签时触发该异常
                sys.exit()
            except TimeoutException:
                retries += 1
                print(f"find事件  -->  元素查找超时,正在进行第 {retries+1} 次重试")
            except Exception as e:
                print(f"find事件  报错异常 ---> : {e}")
                raise
        print(f"重试 {max_retries} 次后仍未找到元素")
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
                    # print(f"点击元素：{ele_loc}")
                    break
                except ElementClickInterceptedException:
                    retries += 1
                    print(f"点击事件被拦截，尝试重试操作次数 {retries}")
                    time.sleep(10)
                    if retries >= MAX_RETRIES:
                        print("点击操作重试次数已达到最大限制")
                except Exception as e:
                    print(f"click事件 报错异常 ---> : {e}")
                    break
        except Exception as m:
            print(f"捕获到最大重试次数异常: {m}")
            sys.exit()
    def input_text(self, ele_loc, text, clear_first=True):
        """
        输入文本内容
        """
        time.sleep(1)
        try:
            ele = self.find(ele_loc)
            if clear_first:
                # print("清空输入框数据")
                time.sleep(0.5)
                self.driver.execute_script("arguments[0].value = '';", ele)  # 使用脚本清空数据
                ele.clear()
                time.sleep(0.5)
                ele.send_keys(text)
                # print(f"--->  输入的值：{text}")
            else:
                ele.send_keys(text)
                # print(f"--->  输入的值：{text}")
        except Exception as e:
            print(f"send_keys事件 报错异常 --->: {e}")
    def is_element_exist(self, locator, timeout=10):
        """这里find用的是系统自带的driver.find_element,判断元素是否存在"""
        locator_type, locator_value = locator
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((getattr(By, locator_type.upper()), locator_value)))
            return True
        except NoSuchElementException:
            # print(f"元素未找到: 定位器 {locator}")
            return False
        except Exception as e:
            # print(f"发送错误: {e}")
            return False

    def get_element_text(self, ele_loc):
        """
        获取标签对应的文本内容
        """
        time.sleep(1)
        ele = self.find(ele_loc)
        if ele:
            # print(f"获取文本内容：{ele.text}")
            return ele.text
        else:
            # print("未能找到元素，获取文本内容失败")
            return None

    def assert_status_element(self, ele_loc):
        """
        断言备份任务
        """
        num = 0
        while True:
            get_text = self.get_element_text(ele_loc)
            if "成功" in get_text or 'Successful' in get_text:
                print(f"Task Successful")
                return get_text
            elif "失败" in get_text or 'Failed' in get_text:
                print("Task Failed")
                return get_text
            elif "取消" in get_text or 'Canceled' in get_text:
                print("Task Canceled")
                return get_text
            else:
                print("备份中...")
            time.sleep(60)
            num += 1
            # print(f"循环第 {num} 次")

    def backup(self, url, username, password, task_name, network_directory, number ,vmdk_path):
        self.open_url(url)
        if self.is_element_exist(self.__gaoji):
            self.click_element(self.__gaoji)
            self.click_element(self.__jixuqianwang)
            self.find(("xpath", "//p[@class='a-logo']"))
        self.input_text(self.__Admin_input_name, username)
        self.input_text(self.__Admin_input_pw, password)
        self.click_element(self.__Admin_input_submit)
        time.sleep(3)
        # 进入界面
        self.click_element(self.__one_menu_backupTask)
        self.click_element(self.__two_menu_backupTask)
        for i in range(0, int(number)):
            print(f"execute {i+1} number of times")
            upload_files(network_directory, i+1)
            time.sleep(2)
            try:
                self.click_element(('xpath', f'//div[contains(text(),"{task_name}")]'))
                self.click_element(('xpath', '//div[@class="a-head"]/div/div[2]'))
                self.click_element(('xpath', '//div[@class="ant-drawer-content-wrapper"]//div[@class="ant-btn-group ant-dropdown-button"]/button[2]'))
                time.sleep(1)
                self.click_element(('xpath', '//ul[@class="ant-dropdown-menu ant-dropdown-menu-vertical ant-dropdown-menu-root ant-dropdown-menu-light ant-dropdown-content"]/li[1]'))
                self.assert_status_element(('xpath', f'//div[contains(text(),"{task_name}")]/../../td[3]//span/span/span'))
                time.sleep(5)
                check_vmdk_files(vmdk_path)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    url = input("input url: ")
    username = input("input username: ")
    password = input("input password: ")
    task_name = input("input task name: ")
    network_directory = input("input deposit data path: ")
    number = input("input loop index: ")
    vmdk_path = input("input .vmdk path: ")
    time.sleep(2)
    edge_options = webdriver.EdgeOptions()
    edge_options.add_argument('--ignore-certificate-errors')
    browser = webdriver.Edge(options=edge_options)
    base = Base(browser)
    base.backup(url, username, password, task_name, network_directory, number, vmdk_path)
    browser.quit()  # 确保在脚本结束时关闭浏览器
