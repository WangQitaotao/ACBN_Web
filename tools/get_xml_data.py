# -*- encoding: utf-8 -*-
'''
@时间 ： 2024/6/24 11:17
@作者 ： WangQitao
@名称 ： get_xml_data.py
@描述 ：
'''
import sys
import os

from openpyxl import Workbook

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
import xml.etree.ElementTree as ET


def get_xml_data(xml_path, Excel_path):
    # 解析XML文件
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        # # 查找并获取字段值
        num = len(root.findall('./helpdesk-ticket'))
        print(f"总共有 {num} 条数据!")
        # 创建一个新的Excel工作簿
        wb = Workbook()
        ws = wb.active
        ws.title = "获取数据"
        # 写入表头
        ws.append(["Description", "Spam", "To Email"])
        # 查找并获取字段值，并写入Excel
        for ticket in root.findall('./helpdesk-ticket'):
            description = ticket.find('description').text
            spam = ticket.find('spam').text
            to_email = ticket.find('to-email').text
            ws.append([description, spam, to_email])
        # 保存Excel文件
        path = Excel_path+r"\\"+"data.xlsx"
        wb.save(path)
        print(f"Excel数据存放路径 {path}")
        print("代码执行完成！")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    xml_path = input(r"请输入存放XML文件的绝对路径(例:C:\Users\AOMEI 2021\Desktop\Tickets0.xml)：")
    Excel_path = input(r"请输入存放Excel表格的绝对路径(例:C:\Users\AOMEI 2021\Desktop)：")
    get_xml_data(xml_path, Excel_path)

