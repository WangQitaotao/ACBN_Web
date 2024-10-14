# -*- encoding: utf-8 -*-
'''
@时间 ： 2024/6/20 15:47
@作者 ： WangQitao
@名称 ： test_add_local.py 
@描述 ：
'''
import sys
import os
import pytest
from common.all_paths import ACBN_DATA_EXCEL
from page.target_Storage import TestTargetStorage
from tools.excel_openyxl_data import HandleExcel
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))


class TestAddLocal:
    excel_local = HandleExcel(ACBN_DATA_EXCEL, "location")
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


if __name__ == '__main__':
    pytest.main(['-v', 'test_add_local.py'])
