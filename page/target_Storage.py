# -*- encoding: utf-8 -*-
'''
@时间 ： 2022/12/5 14:04
@作者 ： WangQitao
@文件名称： target_Storage.py
'''
import sys
import os
import time
from common.Base import Base
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
"""
封装左边导航栏-目标界面
--
封装定位元素
"""


class TestTargetStorage(Base):
    __one_menu_sourcedevice = ("xpath", "//ul[@role='menu']//li[4]//div[@aria-haspopup='true']")    # 目标
    __two_menu_local_location = ('xpath', '//ul[@role="menu"]//li[4]//div[@aria-haspopup="true"]/../ul/li[1]')  # 本地位置
    __add_local_target = ('xpath', '//button[@class="ant-btn ant-btn-primary"]')
    __ok_add_target = ('xpath', '//div[@class="subottom"]//button[@class="ant-btn ant-btn-primary"]')

    def __init__(self, browser):
        super().__init__(browser)  # 调用父类的__init__方法
        self.click_element(self.__one_menu_sourcedevice)

    __judge_target_exist = ('xpath', '//div[@class="vxe-modal--wrapper type--alert status--error is--animat lock--view is--mask is--visible is--active"]//div[@class="vxe-modal--content"]')
    __judge_target_exist_ok = ('xpath', '//div[@class="vxe-modal--wrapper type--alert status--error is--animat lock--view is--mask is--visible is--active"]//button/span')

    def test_add_target(self, target_name):  # 比如 target_name=本地磁盘 (C:)
        """添加本地位置"""
        self.click_element(self.__two_menu_local_location)
        self.click_element(self.__add_local_target)
        self.click_element(('xpath', f'//span[contains(text(),"{target_name}")]'))
        self.click_element(self.__ok_add_target)
        # 断言添加是否已存在
        if self.is_element_exist(self.__judge_target_exist) is True:
            self.log.error(f"目标位置 {target_name}   ---> 存在")
            text = self.get_element_text(self.__judge_target_exist)
            self.click_element(self.__judge_target_exist_ok)
            self.click_element(('xpath', '//div[@class="subottom"]//button[1]'))
            return text
        else:
            # 断言成功
            start_index = target_name.find('(')  # 查找左括号位置
            end_index = target_name.find(')')  # 查找右括号位置
            if start_index != -1 and end_index != -1:  # 确保找到左右括号
                content_inside_brackets = target_name[start_index + 1: end_index]  # 截取括号中的内容,就是 C:
                time.sleep(4)
                if self.is_element_clickable(('xpath', f'//td[2]//span[contains(text(),"{content_inside_brackets}")]')) is True:
                    self.log.info("添加成功")
                    return 'Success'
                else:
                    self.log.error("添加失败")
                    return 'Failed'

    __two_menu_network_lcoation = ('xpath', '//ul[@role="menu"]//li[4]//div[@aria-haspopup="true"]/../ul/li[2]')
    __input_network_path = ('xpath', '//input[@class="ant-input"]')
    __network_path_validate = ('xpath', '//button[@class="search-btn ant-btn ant-btn-primary ant-input-search-button"]')
    __validate_user = ('xpath', '//form/div[2]//input')
    __validate_pass = ('xpath', '//form/div[3]//input')
    __validate_button = ('xpath', '//div[@class="vxe-modal--footer"]/button[2]')

    def test_add_network_target(self, network_path, user, pw):
        """添加网络位置"""
        self.click_element(self.__two_menu_network_lcoation)
        self.click_element(self.__add_local_target)
        self.input_text(self.__input_network_path, network_path)
        self.click_element(self.__network_path_validate)
        if self.is_element_exist(('xpath', '//div[@class="ant-form-explain"]')) is True:
            self.log.error(f"网络位置: {network_path}   ---> 存在")
            text = self.get_element_text(('xpath', '//div[@class="ant-form-explain"]'))
            self.click_element(('xpath', '//div[@class="subottom"]//button[1]'))
            return text
        else:
            self.input_text(self.__validate_user, user)
            self.input_text(self.__validate_pass, pw)
            self.click_element(self.__validate_button)
            self.click_element(self.__ok_add_target)
            # 断言
            time.sleep(4)
            if self.is_element_clickable(('xpath', f'//td[2]//span[contains(text(),"{network_path}")]')) is True:
                self.log.info("添加成功")
                return 'Success'
            else:
                self.log.error("添加失败")
                return 'Failed'

    __two_menu_amazonS3 = ('xpath', '//ul[@role="menu"]//li[4]//div[@aria-haspopup="true"]/../ul/li[3]')

    def test_add_amazonS3(self, username, password, bucket_name, name=None):
        """添加Amazon S3"""
        self.click_element(self.__two_menu_amazonS3)
        self.click_element(self.__add_local_target)
        self.input_text(('xpath', '//form/div[1]//input'), name)
        self.input_text(('xpath', '//form/div[3]//input'), username)
        self.input_text(('xpath', '//form/div[4]//input'), password)
        self.input_text(('xpath', '//form/div[5]//input'), bucket_name)
        self.click_element(self.__ok_add_target)