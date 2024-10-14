# -*- encoding: utf-8 -*
"""
@时间:   2021/11/7 11:10
@作者:   王齐涛
@文件:   conftest.py
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from page.acbn_login import ACBNLogin
import time
from selenium.webdriver.common.by import By
import json
from importlib import reload
from random import random
import pytest
from filelock import FileLock
from selenium import webdriver
from common.logger_handler import GetLogger
reload(sys)

# 其他驱动
# driver = undetected_chromedriver.Chrome(use_subprocess=True)
driver = webdriver.Edge()
# driver = webdriver.Chrome()
# driver = webdriver.Firefox()
# driver = undetected_chromedriver.Chrome()

# options = webdriver.ChromeOptions()
# options.accept_insecure_certs = True
# 忽略证书错误
# options.add_argument('--headless')
# options.add_argument('--ignore-certificate-errors')
# # 忽略 Bluetooth: bluetooth_adapter_winrt.cc:1075 Getting Default Adapter failed. 错误
# options.add_experimental_option('excludeSwitches', ['enable-automation'])
# # 忽略 DevTools listening on ws://127.0.0.1... 提示
# options.add_argument('excludeSwitches', ['enable-logging'])
# driver = undetected_chromedriver.Chrome(use_subprocess=True, options=options)

@pytest.fixture(autouse=False)
def home_page():
    """浏览器的驱动"""
    GetLogger().debug("----------  测试开始  ----------")
    yield driver
    driver.quit()
    GetLogger().debug("----------  测试结束  ----------")


@pytest.fixture(scope="class", autouse=False)
def after_init():
    """ACBN登录模块，作用于class"""
    GetLogger().debug("----------测试开始----------")
    ACBNLogin(driver).acbn_login("admin", "admin")
    time.sleep(2)
    yield driver
    # driver.close()
    driver.quit()
    GetLogger().debug("----------测试结束----------")


@pytest.fixture(scope="session")
def test(tmp_path_factory, worker_id):
    """参考官网，解决多线程的问题"""
    # 针对单机运行，运行下面的代码块
    if worker_id == "master":
        # 自定义代码块
        token = str(random())
        print("请求登录接口，获取token", token)
        os.environ["token"] = token
        return token
    # 针对分布式运行，获取所有子节点共享的临时目录
    root_tmp_dir = tmp_path_factory.getbasetemp().parent
    fn = root_tmp_dir / "data.json"
    with FileLock(str(fn) + ".lock"):
        if fn.is_file():
            # 缓存文件中读取数据，像登录操作的话就是token，如果是session就返回session
            token = json.loads(fn.read_text())
            print(f"读取缓存文件，token 是{token} ")
        else:

            # 这里是自定义代码块，跟上面的if一样就可以了
            token = str(random())
            print("fixture:请求登录接口，获取token", token)
            # 不可删除、修改
            fn.write_text(json.dumps(token))
            print(f"首次执行，token 是{token} ")

        # 最好将后续需要保留的数据存在某个地方，比如这里是 os 的环境变量
        os.environ["token"] = token
    return token


