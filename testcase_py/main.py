# -*- encoding: utf-8 -*-
'''
@时间 ： 2024/6/18 16:44
@作者 ： WangQitao
@名称 ： run.py
@描述 ：
'''
import sys
import os
import pytest
from page.source_Device import TestSourceDevice
from page.target_Storage import TestTargetStorage
from page.task_BackupTask import TestBackupTask
from tools.excel_openyxl_data import HandleExcel
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

"""
纯新环境ACBN流程：
1.先添加目标（本地位置、网络位置、Amazon S3）
2.再添加设备（代理设备、Vmware ESXI、Hyper-V）只要添加了代理设备SQL和Windows就都有数据了
3.最后添加备份任务（7种）
"""


class TestAddSource:
    excel_source = HandleExcel(r"N:\\UI_WEB_ALL\\data\\ACBN.xlsx", "device")
    """添加设备"""
    @pytest.mark.parametrize("idx, args", enumerate(excel_source.get_test_case(), start=2))
    def test_add_source(self, idx, args, after_init):
        if args['start'] != 1:
            pytest.skip("Skipping test case with start value 0")
        elif args['module'] == 'add_source_agent':
            result = TestSourceDevice(after_init).test_add_proxy_device(args['ip'], args['user'], args['pass'])
            self.excel_source.write_test_data(idx, 6, result)
        elif args['module'] == 'add_source_esxi':
            result = TestSourceDevice(after_init).test_add_vmware_esxi(args['ip'], args['user'], args['pass'])
            self.excel_source.write_test_data(idx, 6, result)
        elif args['module'] == 'add_source_hyperv':
            result = TestSourceDevice(after_init).test_add_hyperV(args['ip'], args['user'], args['pass'])
            self.excel_source.write_test_data(idx, 6, result)


class TestAddLocal:
    excel_local = HandleExcel(r"N:\\UI_WEB_ALL\\data\\ACBN.xlsx", "location")
    """添加位置"""
    @pytest.mark.parametrize("idx,args", enumerate(excel_local.get_test_case(), start=2))
    def test_add_local(self, idx, args, after_init):
        if args['start'] != 1:
            pytest.skip("Skipping test case with start value 0")
        elif args['module'] == 'add_target_local':
            result = TestTargetStorage(after_init).test_add_target(args['path'])
            self.excel_local.write_test_data(idx, 6, result)
        elif args['module'] == 'add_target_network':
            result = TestTargetStorage(after_init).test_add_network_target(args['path'], args['user'], args['pass'])
            self.excel_local.write_test_data(idx, 6, result)


class TestAddTask:
    excel_task = HandleExcel(r"N:\\UI_WEB_ALL\\data\\ACBN.xlsx", "task")
    """添加备份任务"""
    @pytest.mark.parametrize("idx,args", enumerate(excel_task.get_test_case(), start=2))
    def test_add_task(self, idx, args, after_init):
        if args['start'] != 1:
            pytest.skip("Skipping test case with start value 0")
        elif args['module'] == 'add_esxi' or args['module'] == 'add_hyperv':
            result = TestBackupTask(after_init).test_create_esxi_hyperv_task(args['type'], args['task_name'], args['device_name'], args['source'], args['target'])
            self.excel_task.write_test_data(idx, 8, result)
        elif args['module'] == 'add_sql':
            result = TestBackupTask(after_init).test_create_sql_task(args['task_name'], args['device_name'], args['source'], args['target'], args['user'], args['pass'])
            self.excel_task.write_test_data(idx, 8, result)
        elif args['module'] == 'add_disk' or args['module'] == 'add_partition':
            result = TestBackupTask(after_init).test_create_disk_partition_backup(args['type'], args['task_name'], args['device_name'], args['source'], args['target'])
            self.excel_task.write_test_data(idx, 8, result)
        elif args['module'] == 'add_system':
            result = TestBackupTask(after_init).test_create_system_file_backup(args['type'], args['task_name'], args['device_name'], args['target'])
            self.excel_task.write_test_data(idx, 8, result)
        elif args['module'] == 'add_file':
            result = TestBackupTask(after_init).test_create_system_file_backup(args['type'], args['task_name'], args['device_name'], args['target'], args['source'])
            self.excel_task.write_test_data(idx, 8, result)


if __name__ == '__main__':
    # pytest.main(["-s", "run.py"])
    pytest.main(["-s", "run.py::TestAddSource"])
    pytest.main(["-s", "run.py::TestAddLocal"])
    pytest.main(["-s", "run.py::TestAddTask"])
