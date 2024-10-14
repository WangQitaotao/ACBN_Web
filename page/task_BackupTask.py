# -*- encoding: utf-8 -*-
'''
@时间 ： 2024/6/5 14:43
@作者 ： WangQitao
@名称 ： task_BackupTask.py 
@描述 ：
'''
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
import time
from common.Base import Base
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))


class TestBackupTask(Base):
    """
    封装左边导航栏-任务界面-备份任务
    --
    封装定位元素
    """
    # 创建备份任务主流程相关元素
    url = Base.url + "/#/task/backup-task"
    __one_menu_backupTask = ("xpath", "//ul[@role='menu']//li[2]//div[@aria-haspopup='true']")
    __two_menu_backupTask = ("xpath", "//a[@href='#/task/backup-task']")
    __button_create_task = ("xpath", "//button[@class='ant-btn ant-btn-primary']")
    __backup_type = ('xpath', '//form//div[@class="ant-form-item-control has-success"]/span//span[@class="f-mid "]')
    __input_task_name = ("id", "taskName")
    __checkbox_documentation = ('xpath', '//input[@class="ant-checkbox-input"]')
    __button_ok = ("xpath", "//div[@class='subottom']//div")
    __button_start_backup = ("xpath", "//div[@class='ant-btn-group ant-dropdown-button']")

    # 任务建立成功后，断言操作
    __task_assert = ('xpath', '//tbody/tr[1]/td[3]//span/span')    # 断言的是第一个任务
    __task_assert_text = ('xpath', '//tbody/tr[1]/td[3]//span/span')  # 获取的是文本信息
    __task_assert_percentage = ('xpath', '//tbody/tr[1]/td[3]/div/div/span[2]')  # 获取的是任务进度条百分比

    def __init__(self, browser):
        super().__init__(browser)  # 调用父类的__init__方法
        self.click_element(self.__one_menu_backupTask)
        self.click_element(self.__two_menu_backupTask)

# 创建VMWARE ESXi备份、Hyper-V备份
    def test_create_esxi_hyperv_task(self,  backup_type, task_name, source_ip, source_device_name, target_device_name):
        """
        VMWARE ESXi 备份  1
        Hyper-V 备份  2
        """
        self.click_element(self.__button_create_task)   # 新建任务
        self.click_element(self.__backup_type)  # 备份类型
        if backup_type == 1:
            self.click_element(self.__backup_type)
        elif backup_type == 2:
            self.click_element(('xpath', '//ul[@class="ant-select-dropdown-menu ant-select-dropdown-menu-vertical ant-select-dropdown-menu-root"]/li[2]'))
        if task_name is not None:
            self.input_text(self.__input_task_name, task_name)  # 任务名称
        self.click_element(self.__add_select_source)    # 添加设备入口
        self.test_setting_add_source(source_ip, source_device_name)
        self.click_element(self.__add_select_target)    # 添加备份目标入口
        self.test_setting_add_target(target_device_name)
        # self.click_element(self.__checkbox_documentation)   # 是否归档，默认不勾选
        self.click_element(self.__backup_plan)  # 备份计划入口
        self.test_setting_backup_plan(1)
        # self.click_element(self.__version_clean)   # 版本清理入口
        # self.test_setting_version_clean()
        # self.click_element(self.__email_notice)     # 邮件通知入口
        # self.test_setting_email_notice()
        self.click_element(self.__button_start_backup)  # 开始备份按钮
        return self.assert_status_element(self.__task_assert_text)

# 创建Microsoft SQL Server备份
    def test_create_sql_task(self,  task_name, source_ip,source_device_name, target_device_name, user, psw):
        """
        Microsoft SQL Server 备份 3
        """
        self.click_element(self.__button_create_task)
        self.click_element(self.__backup_type)
        self.click_element(('xpath', '//ul[@class="ant-select-dropdown-menu ant-select-dropdown-menu-vertical ant-select-dropdown-menu-root"]/li[3]'))
        if task_name is not None:
            self.input_text(self.__input_task_name, task_name)
        self.click_element(self.__add_select_source)
        self.test_setting_add_source(source_ip, source_device_name, user, psw)
        self.click_element(self.__add_select_target)
        self.test_setting_add_target(target_device_name)
        self.click_element(self.__button_start_backup)
        self.assert_status_element(self.__task_assert_text)


# 创建磁盘备份和分区备份
    __disk_add_select_source_ok = ('xpath', '/html/body/div[4]//div[@class="subottom"]/button[3]')
    __add_select_source_list = ('xpath', '//div[@class="i-loading ant-spin-nested-loading"]//tbody/tr[1]')  # 添加设备中的选择第一个设备
    __add_select_content_list = ('xpath', '//div[@class="ant-spin-nested-loading"]/div/div/div[1]')  # 添加备份内容,选择第一块磁盘
    __add_select_target_1 = ('xpath', '//form//div[5]//span[@class="f-mid"]')  # 选择备份目标
    __disk_add_select_content_ok = ('xpath', '/html/body/div[5]//div[@class="subottom"]/button[2]')
    __disk_add_target_ok = ('xpath', '/html/body/div[6]//button[@class="ant-btn ant-btn-primary"]')

    def test_create_disk_partition_backup(self, backup_type, task_name, source_ip, backup_content, target_device_name):
        """
        磁盘备份    4
        分区备份    5
        """
        self.click_element(self.__button_create_task)
        self.click_element(self.__backup_type)
        if backup_type == 4:
            self.click_element(('xpath', '//ul[@class="ant-select-dropdown-menu ant-select-dropdown-menu-vertical ant-select-dropdown-menu-root"]/li[4]'))
        elif backup_type == 5:
            self.click_element(('xpath', '//ul[@class="ant-select-dropdown-menu ant-select-dropdown-menu-vertical ant-select-dropdown-menu-root"]/li[5]'))
        self.click_element(self.__add_select_source)
        self.click_element(('xpath', f'//span[contains(text(),"{source_ip}")]'))
        self.click_element(('xpath', '/html/body/div[4]//div[@class="subottom"]/button[3]'))
        if task_name is not None:
            self.input_text(self.__input_task_name, task_name)
        self.click_element(self.__add_select_target)
        self.click_element(('xpath', f'//p[contains(text(),"{backup_content}")]'))
        self.click_element(self.__disk_add_select_content_ok)
        self.click_element(self.__add_select_target_1)
        self.click_element(('xpath', f'//div[contains(text(),"{target_device_name}")]'))
        self.click_element(self.__disk_add_target_ok)
        self.click_element(self.__button_start_backup)
        self.assert_status_element(self.__task_assert_text)

# 创建系统备份和文件备份
    __file_backup_input_path = ('xpath', '//span[@class="input ant-input-affix-wrapper"]/input')
    __file_backup_input_path_search = ('xpath', '//div[@class="i-loading ant-spin-nested-loading"]//button')
    __file_backup_button_ok = ('xpath', '/html/body/div[4]//div[@class="subottom"]/button[2]')
    __add_select_target_button_ok_1 = ('xpath', '/html/body/div[6]//button[@class="ant-btn ant-btn-primary"]')

    def test_create_system_file_backup(self, backup_type, task_name, source_ip, target_device_name, path=''):
        """
        系统备份    6
        文件备份    7
        """
        self.click_element(self.__button_create_task)
        self.click_element(self.__backup_type)
        if backup_type == 6:
            self.click_element(('xpath', '//ul[@class="ant-select-dropdown-menu ant-select-dropdown-menu-vertical ant-select-dropdown-menu-root"]/li[6]'))
        elif backup_type == 7:
            self.click_element(('xpath', '//ul[@class="ant-select-dropdown-menu ant-select-dropdown-menu-vertical ant-select-dropdown-menu-root"]/li[7]'))
        if task_name is not None:
            self.input_text(self.__input_task_name, task_name)
        self.click_element(self.__add_select_source)
        if backup_type == 6:
            self.click_element(('xpath', f'//span[contains(text(),"{source_ip}")]'))
            self.click_element(self.__disk_add_select_source_ok)
            self.click_element(self.__add_select_target)
            self.click_element(('xpath', f'//td/div[contains(text(),"{target_device_name}")]'))
            self.click_element(self.__add_select_target_button_ok)
        elif backup_type == 7:
            self.input_text(self.__file_backup_input_path, path)
            self.click_element(self.__file_backup_input_path_search)
            self.click_element(('xpath', f'//span[contains(text()," {path} ")]'))
            self.click_element(('xpath', '/html/body/div[4]//div[@class="subottom"]/button[2]'))
            self.click_element(self.__add_select_target)
            self.click_element(('xpath', f'//td/div[contains(text(),"{target_device_name}")]'))
            self.click_element(self.__add_select_target_button_ok_1)
        self.click_element(self.__button_start_backup)
        self.assert_status_element(self.__task_assert_text)

    # 新建任务-选择设备（源）
    __add_select_source = ("xpath", "//form//div[3]//span[@class='f-mid']")    # 添加设备入口
    __source_name_list = ('xpath', '//div[@class="vmpclist ant-col"]//tbody/tr[1]')     # 选中设备列表中的第一个
    __add_select_source_button_ok = ("xpath", '//div[@class="ant-drawer-content-wrapper"]//div[@class="subottom"]/span/../button[2]')
    __validate = ('xpath', '//div[@class="vxe-table--empty-placeholder"]//p/a')

    def test_setting_add_source(self, source_ip, source_device_name, user='', password=''):
        """添加设备"""
        if self.is_element_exist(self.__validate) is True:
            self.click_element(self.__validate)
            self.input_text(('xpath', '//form//div[@class="ant-form-item-control"]//input[@type="text"]'), user)
            self.input_text(('xpath', '//form//div[@class="ant-form-item-control"]//input[@type="password"]'), password)
            self.click_element(('xpath', '//div[@class="vxe-modal--footer"]/button[2]'))
        self.click_element(('xpath', f"//span[contains(text(),' {source_ip} ')]"))
        self.click_element(('xpath', f"//span[contains(text(),' {source_device_name} ')]"))
        self.click_element(self.__add_select_source_button_ok)

    # 新建任务-选择备份目标位置（目标）
    __add_select_target = ("xpath", "//form//div[4]//span[@class='f-mid']")      # 添加备份目标
    __common_target = ('xpath', '//div[@class="ant-tabs-bar ant-tabs-left-bar"]/div/div/div/div/div/div[2]')   # 常用位置
    __add_select_target_button_ok = ('xpath', '/html/body/div[5]//button[@class="ant-btn ant-btn-primary"]')

    def test_setting_add_target(self, target_device_name):
        self.click_element(('xpath', f'//div[contains(text()," {target_device_name} ")]'))
        self.click_element(self.__add_select_target_button_ok)

    # 新建任务-备份计划
    __backup_plan = ("xpath", '//dl[@class="stext fedit"]/dt')    # 备份计划入口
    __button_enable_schedule = ("id", "planform_enable")   # 是否开启计划任务
    __button_backup_method = ("xpath", "//*[@id='planform_strategy']/div")      # 定位到复选框，备份方式
    __backup_method_type = ("xpath", "//li[contains(text(),' Differential Backup ')]")  # 选择备份类型
    __button_schedule_type = ("xpath", "//form//div[3]/div[2]/div/span/div[1]/div")  # 定位到复选框，计划类型
    __schedule_type_1 = ("xpath", "//span[contains(text(),' (By Week) ')]")   # 针对于Every Month (By week)和(By Date)
    __schedule_type_2 = ("xpath", "//li[contains(text(),' Everyday ')]")   # 针对于Everyday 和 Every Week
    __backup_plan_type_select_every_Day = ("xpath", '//span[@class="c-grey"]/../../li[1]')      # 选择每天
    __backup_plan_type_start_time = ("xpath", '//div[@class="setime"]/div[1]//input')
    __backup_plan_type_start_time_num = ("xpath", '//div[@class="ant-time-picker-panel-combobox"]/div[1]/ul/li[1]')
    __backup_plan_type_end_time = ("xpath", '//div[@class="setime"]/div[2]//input')
    __backup_plan_type_end_time_num = ("xpath", '//div[@class="ant-time-picker-panel-combobox"]/div[1]/ul/li[24]')
    __backup_plan_type_time_interval = ("xpath", '//input[@class="ant-input-number-input"]')    # 时间间隔
    __backup_plan_type_time_interval_up = ("xpath", '//span[@aria-label="Increase Value"]')    # 时间间隔，向上
    __backup_plan_button_ok = ("xpath", '/html/body/div[6]//button[@class="ant-btn ant-btn-primary"]')

    __sql_backup_plan_full_backup = ('xpath', '//form[@class="ant-form ant-form-horizontal ant-form-hide-required-mark"]/div[3]//p')
    __sql_backup_plan_incremental_backup = ('xpath', '//form[@class="ant-form ant-form-horizontal ant-form-hide-required-mark"]/div[4]//p')
    __sql_backup_plan_time_interval = ('xpath', '//span[@class="ant-form-item-children"]/div/div/label[2]')  # 时间区间
    __sql_backup_plan_button_ok = ('xpath', '/html/body/div[7]//button[@class="ant-btn ant-btn-primary"]')

    def test_setting_backup_plan(self, backup_type):
        """新建任务-备份计划设置（只写了增量备份-每天），这里用到了模拟鼠标方法，所以运行的时候不要移动鼠标"""
        # self.click_element(self.__button_enable_schedule)   # 是否开启计划任务
        if backup_type == 1:
            # self.click_element(self.__button_backup_method)     # 点击备份方式复选框
            # self.click_element(self.__backup_method_type)       # 备份方式展开的备份类型
            self.click_element(self.__button_schedule_type)        # 点击计划类型复选框
            # 选择每天
            self.click_element(self.__backup_plan_type_select_every_Day)
        elif backup_type == 3:
            self.click_element(self.__sql_backup_plan_full_backup)
            self.click_element(self.__sql_backup_plan_time_interval)
        self.click_element(self.__backup_plan_type_start_time)  # 开始时间复选框
        self.pyautogui_to_move(self.get_location(("xpath", '//div[@class="ant-time-picker-panel-combobox"]'), add_x=30, add_y=140))
        self.pyautogui_to_scroll(3, 1000)
        self.click_element(self.__backup_plan_type_start_time_num)  # 选择时间段 00点开始，不管分钟
        self.pyautogui_to_click(self.get_location(("xpath", '//div[@class="ant-time-picker-panel-combobox"]'), add_x=-100, add_y=140))
        self.click_element(self.__backup_plan_type_end_time)    # 结束时间复选框
        self.pyautogui_to_move(self.get_location(("xpath", '//div[@class="ant-time-picker-panel-combobox"]'), add_x=30, add_y=200))
        self.pyautogui_to_scroll(3, -1000)
        self.click_element(self.__backup_plan_type_end_time_num)    # 选择时间段 23点结束，不管分钟
        self.pyautogui_to_click(self.get_location(("xpath", '//div[@class="ant-time-picker-panel-combobox"]'), add_x=-100, add_y=140))
        # self.click_element(self.__backup_plan_type_time_interval)   # 时间间隔输入框
        # self.click_element(self.__backup_plan_type_time_interval_up)    # 向上点击
        if backup_type == 1:
            self.click_element(self.__backup_plan_button_ok)
        else:
            self.click_element(self.__sql_backup_plan_button_ok)

    # 新建任务-版本清理
    __version_clean = ("xpath", "//p[@class='stext fedit ']")      # 设置入口
    __open_version_clean = ("id", "strategyform_enable")     # 是否开启计划任务
    __full_backup_time = ("xpath", "//*[@id='strategyform_daysForFull']/div[2]/input")      # 完全备份保留时间
    __all_backup_time = ("xpath", "//*[@id='strategyform_daysForDiffInc']/div[2]/input")    # 增量/差异备份保留时间
    __checkbox_other_settings = ("id", "strategyform_isSave")    # 其他设置（复选框）,是否始终保留
    __checkbox_other_settings_dropdown = ('id', 'strategyform_keepFull')    # 其他设置(下拉框)
    __checkbox_other_settings_dropdown_num = ('id', '//ul[@class="ant-select-dropdown-menu ant-select-dropdown-menu-vertical ant-select-dropdown-menu-root"]/li[1]') # 修改li[x]

    def test_setting_version_clean(self):
        """新建任务-版本清理设置（）"""
        self.click_element(self.__open_version_clean)   # 是否开启计划任务
        self.input_text(self.__full_backup_time,10)      # 完全备份保留时间
        self.input_text(self.__all_backup_time,10)   # 增量/差异备份保留时间
        self.click_element(self.__checkbox_other_settings)  # 其他设置（复选框）,是否始终保留,默认开启
        self.click_element(self.__checkbox_other_settings_dropdown_num)

    # 新建任务-邮件通知
    __email_notice = ('xpath', '//button[@class="ant-switch"]')   # 邮件通知
    __email_notice_goto = ('xpath', '//span[@class="ant-form-item-children"]/p/a')  # 立即前往
    __email_notice_input_email = ('xpath', '//input[@placeholder="Gmail 邮箱"]')
    __email_notice_input_code = ('xpath', '//input[@placeholder="授权码"]')
    __email_notice_input_recipients = ('xpath', '//input[@placeholder="user1@example.com;user2@example.com;"]')
    __email_content_fail_button = ('xpath', '//div[@class="ant-col ant-form-item-control-wrapper"]//label[1]')   # 邮箱内容，失败才发
    __email_content_success_button = ('xpath', '//div[@class="ant-col ant-form-item-control-wrapper"]//label[2]')    # 邮箱内容，成功才发
    __email_button_ok = ('xpath', '/html/body/div[6]//button[@class="ant-btn ant-btn-primary"]')

    def test_setting_email_notice(self):
        self.click_element(self.__email_notice_goto)
        self.input_text(self.__email_notice_input_email, '123456789@gmail.com')
        self.input_text(self.__email_notice_input_code, 'WRWFSGAEGSDGE')
        self.input_text(self.__email_notice_input_recipients, 'Aomeitest9999@gmail.com')
        self.click_element(self.__email_content_fail_button)    # 选择失败发送邮箱
        self.click_element(self.__email_button_ok)
