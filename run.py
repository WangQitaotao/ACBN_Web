# -*- encoding: utf-8 -*-
'''
@时间 ： 2024/6/19 9:35
@作者 ： WangQitao
@名称 ： run.py
@描述 ：
'''
import sys
import os
import pytest
from common.all_paths import ACBN_DATA_EXCEL, ACBN_ADD_LOCAL, CURRENT, ACBN_ADD_SOURCE, ACBN_ADD_TASK

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))


# def check_excel_file(excel_path):
#     if os.path.exists(excel_path):
#         print("在 D 盘找到 Excel 文件:", excel_path)
#         return excel_path
#     else:
#         print("在 D 盘没有找到 Excel 文件", excel_path)
#         new_excel_path = input("请输入新的 Excel 存放位置(绝对位置)：")
#         return new_excel_path


if __name__ == '__main__':
    print("---------------------> 执行ACBN脚步 <---------------------")
    run_type = input("""
    你想执行什么操作？
    
    1.添加路径(对应Excel中表location)
    2.添加设备(对应Excel中表device)
    3.创建备份任务(对应Excel中表task)
    
    请输入对应的序号：""")
    run_type = int(run_type)
    if run_type == 1:
        print("开始执行 添加路径 操作")
        pytest.main(['-sv', ACBN_ADD_LOCAL])
        print("执行完成")
    elif run_type == 2:
        print("开始执行 添加设备 操作")
        pytest.main(['-sv', ACBN_ADD_SOURCE])
        print("执行完成")
    elif run_type == 3:
        print("开始执行 创建备份任务 操作")
        pytest.main(['-sv', ACBN_ADD_TASK])
        print("执行完成")
    else:
        print("请输入正确的编号（1、2、3）")

