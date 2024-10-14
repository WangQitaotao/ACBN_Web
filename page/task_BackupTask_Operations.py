# -*- encoding: utf-8 -*-
'''
@时间 ： 2024/6/14 11:12
@作者 ： WangQitao
@名称 ： task_BackupTask_Operations.py
@描述 ：
'''
import sys
import os
import time
from page.task_BackupTask import TestBackupTask
from common.Base import Base
from testcase_py.conftest import after_init
from testcase_py.upload_network_files import upload_files

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))


class TestTaskBackupTaskOperations(Base):

    __one_menu_backupTask = ("xpath", "//ul[@role='menu']//li[2]//div[@aria-haspopup='true']")
    __two_menu_backupTask = ("xpath", "//a[@href='#/task/backup-task']")

    # 想精确到某一个任务：//div[contains(text(),' VMware ESXi 备份任务 (5) ')]
    __task_operations = ('xpath', '//tbody/tr[1]//a')
    __task_operations_list = ('xpath', '//ul[@class="ant-dropdown-menu ant-dropdown-menu-vertical ant-dropdown-menu-root ant-dropdown-menu-light ant-dropdown-content"]/li[1]')
    __task_operations_backup = ('xpath', '//ul[@class="ant-dropdown-menu ant-dropdown-menu-vertical ant-dropdown-menu-sub ant-dropdown-menu-submenu-content"]/li[1]')
    # 公用
    __close_button = ('xpath', '//button[@class="ant-drawer-close"]/i')

    def test_task_operations_backup(self, task_name, back_type):
        """备份"""
        self.click_element(self.__one_menu_backupTask)
        self.click_element(self.__two_menu_backupTask)
        self.click_element(('xpath', f'//div[contains(text(),"{task_name}")]'))
        self.click_element(('xpath', f'//div[contains(text(),"{task_name}")]/../../td[8]//a'))
        self.pyautogui_to_move(self.get_location(('xpath', '//ul[@class="ant-dropdown-menu ant-dropdown-menu-vertical ant-dropdown-menu-root ant-dropdown-menu-light ant-dropdown-content"]/li[1]'), add_x=52, add_y=103))
        self.click_element(('xpath', f'//ul[@class="ant-dropdown-menu ant-dropdown-menu-vertical ant-dropdown-menu-sub ant-dropdown-menu-submenu-content"]//a[contains(text(),"{back_type}")]'))
        time.sleep(4)
        self.assert_status_element(('xpath', f'//div[contains(text(),"{task_name}")]/../../td[3]//span[@class="f-mid"]'))

    __task_details_button_ok = ('xpath', '/html/body/div[8]//button[@class="ant-btn ant-btn-primary"]')

    def test_task_operations_details(self):
        """详情"""
        self.click_element(self.__one_menu_backupTask)
        self.click_element(self.__two_menu_backupTask)
        self.click_element(self.__task_operations)

        self.click_element(('xpath', '//ul[@class="ant-dropdown-menu ant-dropdown-menu-vertical ant-dropdown-menu-root ant-dropdown-menu-light ant-dropdown-content"]/li[2]'))
        # 打开页面后选择关闭窗口或开始备份
        self.click_element(self.__close_button)
        # self.click_element(self.__task_details_button_ok)

    __task_edit = ('xpath', '//table[@class="info"]/tr[1]')
    __task_edit_button_ok = ('xpath', '/html/body/div[7]//button[@class="ant-btn ant-btn-primary"]')
    # __operations_target = ('xpath', '//table/tr[4]')
    __button_enable_schedule = ("id", "planform_enable")   # 是否开启计划任务

    def test_task_operations_edit(self, driver, target_name):
        """编辑"""
        self.click_element(self.__one_menu_backupTask)
        self.click_element(self.__two_menu_backupTask)
        self.click_element(self.__task_operations)
        __whether_plan = self.get_element_text(('xpath', '//div[contains(text()," 分区备份 任务 (2) ")]/../../td[7]/div'))
        self.click_element(('xpath', '//ul[@class="ant-dropdown-menu ant-dropdown-menu-vertical ant-dropdown-menu-root ant-dropdown-menu-light ant-dropdown-content"]/li[3]'))
        # 编辑目标
        self.click_element(('xpath', '//table/tr[4]/td[2]'))
        self.click_element(('xpath', f'//div[contains(text(),"{target_name}")]'))
        self.click_element(('xpath', '/html/body/div[4]//button[2]'))
        # 归档（需要判断之前的任务是否开启）
        self.click_element(('xpath', '//table/tr[5]/td[2]'))
        # 备份计划（需要判断之前的任务是否开启）
        self.click_element(('xpath', '//table/tr[6]/td[2]'))
        if '未启用计划' in __whether_plan:
            print("未开计划任务")
            self.click_element(self.__button_enable_schedule)
        test_task_backup_operations_instance = TestBackupTask(driver)    # 这里调用的时候要传入driver
        test_task_backup_operations_instance.test_setting_backup_plan(1)
        self.click_element(('xpath', '/html/body/div[3]//button[2]'))

    def test_task_operations_activity(self):
        """活动"""
        self.click_element(('xpath', '//ul[@class="ant-dropdown-menu ant-dropdown-menu-vertical ant-dropdown-menu-root ant-dropdown-menu-light ant-dropdown-content"]/li[4]'))

    def test_task_operations_log(self):
        """日志"""
        self.click_element(('xpath', '//ul[@class="ant-dropdown-menu ant-dropdown-menu-vertical ant-dropdown-menu-root ant-dropdown-menu-light ant-dropdown-content"]/li[5]'))

    __task_delete_popup_all_delete = ('xpath', '//div[@class="ant-radio-group ant-radio-group-outline ant-radio-group-default"]/label[2]')  # 永久删除
    __task_delete_button_ok = ('xpath', '//div[@id="app"]//div[@class="vxe-modal--footer"]/button[2]')  # 确定按钮
    __task_assert_text = ('xpath', '//tbody/tr[1]/td[3]//span/span')

    def test_task_operations_delete(self):
        """删除"""
        # 删除单个
        # self.click_element(self.__one_menu_backupTask)
        # self.click_element(self.__two_menu_backupTask)
        # self.click_element(self.__task_operations)
        # if "成功" in self.get_element_text(self.__task_assert_text):
        #     self.click_element(('xpath', '//ul[@class="ant-dropdown-menu ant-dropdown-menu-vertical ant-dropdown-menu-root ant-dropdown-menu-light ant-dropdown-content"]/li[7]'))
        # elif "失败" or '取消' in self.get_element_text(self.__task_assert_text):
        #     self.click_element(('xpath', '//ul[@class="ant-dropdown-menu ant-dropdown-menu-vertical ant-dropdown-menu-root ant-dropdown-menu-light ant-dropdown-content"]/li[6]'))
        # self.click_element(self.__task_delete_popup_all_delete)
        # self.click_element(self.__task_delete_button_ok)

        # 删除所有
        self.click_element(self.__one_menu_backupTask)
        self.click_element(self.__two_menu_backupTask)
        for i in range(1, self.len_find_2(('xpath', '//tbody/tr'))+1):
            self.click_element(('xpath', f'//tbody/tr[1]//a'))
            if "成功" in self.get_element_text(self.__task_assert_text):
                self.click_element(('xpath', '//ul[@class="ant-dropdown-menu ant-dropdown-menu-vertical ant-dropdown-menu-root ant-dropdown-menu-light ant-dropdown-content"]/li[7]'))
            elif "失败" or '取消' in self.get_element_text(self.__task_assert_text):
                self.click_element(('xpath', '//ul[@class="ant-dropdown-menu ant-dropdown-menu-vertical ant-dropdown-menu-root ant-dropdown-menu-light ant-dropdown-content"]/li[6]'))
            self.click_element(self.__task_delete_popup_all_delete)
            self.click_element(self.__task_delete_button_ok)

    def test_task_operations_backup_2(self, task_name, sum):
        """备份"""

        self.click_element(self.__one_menu_backupTask)
        self.click_element(self.__two_menu_backupTask)
        for i in range(0, int(sum)):
            print(f"执行第 {i} 次")
            upload_files(i)
            time.sleep(2)
            self.click_element(('xpath', f'//div[contains(text(),"{task_name}")]'))
            self.click_element(('xpath', '//div[@class="a-head"]/div/div[2]'))
            self.click_element(('xpath', '//div[@class="ant-drawer-content-wrapper"]//div[@class="ant-btn-group ant-dropdown-button"]/button[2]'))
            time.sleep(0.5)
            self.click_element(('xpath', '//ul[@class="ant-dropdown-menu ant-dropdown-menu-vertical ant-dropdown-menu-root ant-dropdown-menu-light ant-dropdown-content"]/li[1]'))
            self.assert_status_element(('xpath', f'//div[contains(text(),"{task_name}")]/../../td[3]//span/span/span'))


if __name__ == '__main__':
    TestTaskBackupTaskOperations(after_init).test_task_operations_backup_2(' VMware ESXi 备份任务 (1) ')