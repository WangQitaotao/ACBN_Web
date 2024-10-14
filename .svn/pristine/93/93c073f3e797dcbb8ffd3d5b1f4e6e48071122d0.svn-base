# -*- encoding: utf-8 -*-
'''
@时间 ： 2024/6/20 15:47
@作者 ： WangQitao
@名称 ： test_add_source.py 
@描述 ：
'''
import sys
import os
import pytest

from common.all_paths import ACBN_DATA_EXCEL
from page.source_Device import TestSourceDevice
from tools.excel_openyxl_data import HandleExcel

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))


class TestAddSource:
    excel_source = HandleExcel(ACBN_DATA_EXCEL, "device")
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
        elif args['module'] == 'add_sql_server':
            result = TestSourceDevice(after_init).test_add_microsoft_sql_server(args['ip'], args['user'], args['pass'])
            self.excel_source.write_test_data(idx, 6, result)
        elif args['module'] == 'add_windows':
            result = TestSourceDevice(after_init).test_add_windows(args['ip'], args['user'], args['pass'])
            self.excel_source.write_test_data(idx, 6, result)
