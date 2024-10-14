# -*- encoding: utf-8 -*-
'''
@时间 ： 2024/6/21 17:55
@作者 ： WangQitao
@名称 ： get_xml_data.py
@描述 ：
'''
import sys
import os

import pytest

from page.task_BackupTask_Operations import TestTaskBackupTaskOperations
from testcase_py.upload_network_files import upload_files

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))


class TestIncrementBackup:
    def test_all(self, after_init):
        TestTaskBackupTaskOperations(after_init).test_task_operations_backup_2(' VMware ESXi 备份任务 (1) ', 2)
