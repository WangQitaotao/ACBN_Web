# -*- encoding: utf-8 -*-
'''
@时间 ： 2024/6/20 15:47
@作者 ： WangQitao
@名称 ： test_add_task.py 
@描述 ：
'''
import sys
import os
import pytest

from common.all_paths import ACBN_DATA_EXCEL
from page.task_BackupTask import TestBackupTask
from tools.excel_openyxl_data import HandleExcel

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))


class TestAddTask:
    excel_task = HandleExcel(ACBN_DATA_EXCEL, "task")
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