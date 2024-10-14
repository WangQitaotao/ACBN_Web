# -*- encoding: utf-8 -*-
'''
@时间 ： 2024/6/5 14:44
@作者 ： WangQitao
@名称 ： task_BackupArchive.py
@描述 ：
'''
import sys
import os

from common.Base import Base
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))


class TestBackupArchive(Base):
    """
    封装左边导航栏-任务界面-备份归档
    --
    封装定位元素
    """
    # 针对没任务时，整个完整流程
    __one_menu_backupTask = ("xpath", "//ul[@role='menu']//li[2]//div[@aria-haspopup='true']")
    __two_menu_archive = ("xpath", '//a[@href="#/task/backup-archive"]')
    __new_create_file = ("xpath", "//button[@class='ant-btn ant-btn-primary']")     # 新建归档按钮（没有任务时）
    __select_task = ('xpath', '//form[@class="ant-form ant-form-horizontal ant-form-hide-required-mark"]/div[1]/div[2]/div/span')   # 选择任务
    __select_archive_task = ('xpath', '//tbody/tr[1]')  # 选择第一个任务
    __button_ok_select_task = ('xpath', '//div[@class="ant-drawer ant-drawer-right ant-drawer-open no-mask"]//div[@class="subottom"]/button[2]')
    __archive_target = ('xpath', '//form[@class="ant-form ant-form-horizontal ant-form-hide-required-mark"]/div[2]/div[2]/div/span')    # 归档目标
    __select_rchive_target = ('xpath', '//div[@class="ttabs ant-tabs ant-tabs-left ant-tabs-vertical ant-tabs-line"]//tbody/tr[1]')    # 选择第一个常用归档目标
    __button_ok_archive_target = ('xpath', '//div[@class="ttabs ant-tabs ant-tabs-left ant-tabs-vertical ant-tabs-line"]/..//button[2]')
    __archive_mode = ('xpath', '//div[@class="archive-group ant-radio-group ant-radio-group-outline ant-radio-group-default"]/label[1]')  # 归档方式，默认选择第一个
    __start_new_create_file = ('xpath', '//form[@class="ant-form ant-form-horizontal ant-form-hide-required-mark"]/..//button[2]')  # 开始按钮
    # 针对有任务时
    __new_create_file_1 = ('xpath', '//div[@class="ant-space ant-space-horizontal ant-space-align-center"]/div[1]/button') # 新建归档按钮（有任务时）
    __select_archive_task_1 = ('xpath', '//div[@class="ant-drawer ant-drawer-right ant-drawer-open no-mask"]//tbody/tr[1]')  # 选择第一个任务
    # 其他操作
    __all_start = ('xpath', '//div[@class="ant-space ant-space-horizontal ant-space-align-center"]/div[2]/button')  # 全部开始
    __all_halt = ('', '//div[@class="ant-space ant-space-horizontal ant-space-align-center"]/div[3]/button')    # 全部暂停
    __task_editing_1 = ('xpath', '//div[@class="vmtree vxe-table vxe-table--render-default tid_86 size--default border--none row--highlight is--header is--animat"]//tbody/tr[1]//span[@class="task-more more"]')
    __task_editing_2 = ('xpath', "//span[contains(text(),' VMware ESXi 备份任务 (1) ')]")   # 任务展开按钮，可以启动归档和删除
    __task_editing_satart_file = ('xpath', '//div[@class="ant-dropdown ant-dropdown-placement-bottomLeft"]/ul/li[1]')   # 启动归档
    __task_editing_satart_file_ok = ('xpath', '//div[@class="vxe-modal--wrapper type--modal status--confirm is--animat lock--view is--mask is--visible is--active"]//button[@class="ant-btn ant-btn-primary"]')   # 启动归档弹窗，点击是
    __task_editing_delete = ('xpath', '//div[@class="ant-dropdown ant-dropdown-placement-bottomLeft"]/ul/li[2]')  # 删除
    __task_editing_delete_check = ('xpath', '//label/span[@class="ant-checkbox ant-checkbox-checked"]')  # 删除弹窗，点击删除历史版本
    __task_editing_delete_ok = ('xpath', '//div[@class="vxe-modal--wrapper type--modal status--confirm is--animat lock--view is--mask is--visible is--active"]//button[@class="ant-btn"]')  # 删除弹窗，点击是
    # 断言操作
    __assert_all_start_task = ('xpath', '//div[@class="ant-notification-notice-description"]')  # 获取文本，断言字段：所有归档任务已经开始。 或  所有归档任务已经暂停。

    def test_create_new_archive(self):
        """新建归档任务(有任务和无任务)，前提是必须要有任务和目标位置"""
        self.click_element(self.__one_menu_backupTask)
        self.click_element(self.__two_menu_archive)
        if self.len_find_2(self.__new_create_file) > 1:
            self.click_element(self.__new_create_file_1)
            self.click_element(self.__select_task)
            self.click_element(self.__select_archive_task_1)
        else:
            self.click_element(self.__new_create_file)
            self.click_element(self.__select_task)
            self.click_element(self.__select_archive_task)
        self.click_element(self.__button_ok_select_task)
        self.click_element(self.__archive_target)
        self.click_element(self.__select_rchive_target)
        self.click_element(self.__button_ok_archive_target)
        self.click_element(self.__start_new_create_file)
