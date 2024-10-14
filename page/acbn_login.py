# -*- encoding: utf-8 -*-
'''
@时间 ： 2021/9/15 16:57
@作者 ： 王齐涛
@文件名称： a_front_end_login.py
'''
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
import time
from common.Base import Base
from selenium import webdriver


class ACBNLogin(Base):
    """
    封装用户登录界面
    --
    封装定位元素
    """
    url = Base.url + "/#/user/login?redirect=%2Foverview%2Fdashboard"
    __gaoji = ("xpath", "//div[@class='nav-wrapper']//button[3]")
    __jixuqianwang = ("xpath", "//a[@class='small-link']")
    __Admin_input_name = ("id", "username")
    __Admin_input_pw = ("id", "password")
    __Admin_input_submit = ("xpath", "//button[@type='submit']")

    """
    封装页面操作
    """
    def acbn_login(self, admin_un, admin_pw):
        """
        :param admin_un:
        :param admin_pw:
        :return:
        """
        self.open_url()
        if self.is_element_exist(self.__gaoji):
            self.click_element(self.__gaoji)
            self.click_element(self.__jixuqianwang)
            self.find(("xpath", "//p[@class='a-logo']"))
        self.input_text(self.__Admin_input_name, admin_un)
        self.input_text(self.__Admin_input_pw, admin_pw)
        self.click_element(self.__Admin_input_submit)
        time.sleep(3)


if __name__ == '__main__':
    driver = webdriver.Chrome()
    ACBNLogin(driver).acbn_login("admin","admin")

