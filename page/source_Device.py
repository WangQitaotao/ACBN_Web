# -*- encoding: utf-8 -*-
'''
@时间 ： 2022/12/5 14:04
@作者 ： WangQitao
@文件名称： source_Device.py
'''
import sys
import os
import time

from common.Base import Base
from common.all_paths import DATA_PATH
from common.read_yaml import ReadYaml

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))


class TestSourceDevice(Base):
    """
    封装左边导航栏-设备界面
    --
    封装定位元素
    """
    __one_menu_sourcedevice = ("xpath", "//ul[@role='menu']//li[3]//div[@aria-haspopup='true']")    # 设备

    __add_proxy_device = ('xpath', '//div[@class="ant-space ant-space-horizontal ant-space-align-center"]/div[1]/button')  # 添加代理
    __input_ip = ("id", "devedit_addr")
    __input_username = ("id", "devedit_userName")
    __input_password = ("id", "devedit_passWord")
    __ok_confirm = ("xpath", "//div[@class='subottom']//button[2]")

    # 断言
    __get_expect_text = ("xpath", '//form/div[4]//span')
    __get_actual_text = ("xpath", '//form/div[4]//p')
    """
    封装操作
    """
    def __init__(self, browser):
        super().__init__(browser)  # 调用父类的__init__方法
        self.click_element(self.__one_menu_sourcedevice)

    __two_menu_proxy_device = ('xpath', '//ul[@role="menu"]//li[3]//div[@aria-haspopup="true"]/../ul/li[1]')  # 代理设备

    def test_add_proxy_device(self, ip_url, username, password):
        """添加代理设备"""
        self.click_element(self.__two_menu_proxy_device)
        self.click_element(self.__add_proxy_device)
        self.input_text(self.__input_ip, ip_url)
        self.input_text(self.__input_username, username)
        self.input_text(self.__input_password, password)
        if self.is_element_exist(('xpath', '//div[@class="ant-form-explain"]')) is False:
            self.click_element(self.__ok_confirm)
            return self.assert_add_device(self.__get_actual_text)
        else:
            self.log.error("添加失败")
            return self.get_element_text(('xpath', '//div[@class="ant-form-explain"]'))


# ------------------------------------------------------------------->
    __two_menu_vmware_esxi = ('xpath', '//ul[@role="menu"]//li[3]//div[@aria-haspopup="true"]/../ul/li[2]')

    def test_add_vmware_esxi(self, ip_url, username, password):
        """添加VMware ESXi"""
        self.click_element(self.__two_menu_vmware_esxi)
        self.click_element(self.__add_proxy_device)
        self.input_text(self.__input_ip, ip_url)
        self.input_text(self.__input_username, username)
        self.input_text(self.__input_password, password)
        if self.is_element_exist(('xpath', '//div[@class="ant-form-explain"]')) is False:
            self.click_element(self.__ok_confirm)
            return self.assert_add_device(self.__get_actual_text)
        else:
            self.log.error("添加失败")
            return self.get_element_text(('xpath', '//div[@class="ant-form-explain"]'))


# ------------------------------------------------------------------->
    __two_menu_hyperV = ('xpath', '//ul[@role="menu"]//li[3]//div[@aria-haspopup="true"]/../ul/li[3]')

    def test_add_hyperV(self, ip_url, username, password):
        """添加hyper-V"""
        self.click_element(self.__two_menu_hyperV)
        self.click_element(self.__add_proxy_device)
        self.input_text(self.__input_ip, ip_url)
        self.input_text(self.__input_username, username)
        self.input_text(self.__input_password, password)
        if self.is_element_exist(('xpath', '//div[@class="ant-form-explain"]')) is False:
            self.click_element(self.__ok_confirm)
            return self.assert_add_device(self.__get_actual_text)
        else:
            self.log.error("添加失败")
            return self.get_element_text(('xpath', '//div[@class="ant-form-explain"]'))


# ------------------------------------------------------------------->
    __two_menu_sql_server = ('xpath', '//ul[@role="menu"]//li[3]//div[@aria-haspopup="true"]/../ul/li[4]')

    def test_add_microsoft_sql_server(self, ip_url, username, password):
        """添加sql"""
        self.click_element(self.__two_menu_sql_server)
        self.click_element(self.__add_proxy_device)
        self.input_text(self.__input_ip, ip_url)
        self.input_text(self.__input_username, username)
        self.input_text(self.__input_password, password)
        if self.is_element_exist(('xpath', '//div[@class="ant-form-explain"]')) is False:
            self.click_element(self.__ok_confirm)
            return self.assert_add_device(self.__get_actual_text)
        else:
            self.log.error("添加失败")
            return self.get_element_text(('xpath', '//div[@class="ant-form-explain"]'))


# ------------------------------------------------------------------->
    __two_menu_windows = ('xpath', '//ul[@role="menu"]//li[3]//div[@aria-haspopup="true"]/../ul/li[5]')

    def test_add_windows(self, ip_url, username, password):
        """添加Windows"""
        self.click_element(self.__two_menu_windows)
        self.click_element(self.__add_proxy_device)
        self.input_text(self.__input_ip, ip_url)
        self.input_text(self.__input_username, username)
        self.input_text(self.__input_password, password)
        if self.is_element_exist(('xpath', '//div[@class="ant-form-explain"]')) is False:
            self.click_element(self.__ok_confirm)
            return self.assert_add_device(self.__get_actual_text)
        else:
            self.log.error("添加失败")
            return self.get_element_text(('xpath', '//div[@class="ant-form-explain"]'))
