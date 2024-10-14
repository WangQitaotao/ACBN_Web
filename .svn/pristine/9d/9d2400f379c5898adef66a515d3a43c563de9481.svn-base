# -*- encoding: utf-8 -*-
'''
@时间 ： 2024/6/26 16:55
@作者 ： WangQitao
@名称 ： get_excel_body.py
@描述 ：
'''
import sys
import os
import xml.etree.ElementTree as ET
from openpyxl import Workbook


def get_xml_body(xml_path, Excel_path, variable):
    # 解析XML文件
    try:
        # 解析 XML 文件
        tree = ET.parse(xml_path)
        root = tree.getroot()
        # 创建一个新的Excel工作簿
        wb = Workbook()
        ws = wb.active
        ws.title = "获取数据"
        # 写入表头
        ws.append(["private_body"])
        # 遍历所有 <helpdesk-ticket> 下的 <notes> 下的 <helpdesk-note>
        for ticket in root.findall(".//helpdesk-ticket"):
            for helpdesk_note in ticket.findall(".//notes/helpdesk-note"):
                # 找到 private 字段并获取其值
                private_element = helpdesk_note.find('private')
                if private_element is not None:
                    private_value = private_element.text
                    if private_value == variable:
                        private_body = helpdesk_note.find('body').text
                        # print(f"private_body 字段的值为: {private_body}")
                        ws.append([private_body])
                else:
                    print("未找到 private 字段")
        path = Excel_path+r"\\"+"data_body.xlsx"
        wb.save(path)
        print(f"Excel数据存放路径 {path}")
        print("代码执行完成！")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    xml_path = input(r"请输入存放XML文件的绝对路径(例:C:\Users\AOMEI 2021\Desktop\Tickets0.xml)：")
    Excel_path = input(r"请输入存放Excel表格的绝对路径(例:C:\Users\AOMEI 2021\Desktop)：")
    variable = input(r"请输入筛选的字段(true 或 false)：")
    get_xml_body(xml_path, Excel_path, variable)
    print("")
    print("执行完成。请点击回车或直接关闭窗口")
