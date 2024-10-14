# -*- encoding: utf-8 -*-
'''
@时间 ： 2021/9/30 15:26
@作者 ： 王齐涛
@文件名称： read_yaml.py
'''
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import yaml


class ReadYaml:

    # def __init__(self,filename):
    #     self.filename = filename
    def read_yaml(self, filename):
        """
        读yaml文件
        :param filename:
        :return:
        """
        try:
            with open(filename + ".yaml", encoding="utf-8", mode="r") as f:
                all_data = yaml.load(stream=f, Loader=yaml.FullLoader)   #表示加载的方式
                return all_data
                # va = all_data.get(key, "None")
                # if value != None:
                #     return va.get(value)
                # else:
                #     return all_data
        except FileNotFoundError as f:
            print(f"代码本身报错：{f}")
            print("你输入的文件名不正确或者文件不存在。")
        except UnicodeDecodeError as u:
            print(f"代码本身报错：{u}")
            print("你编辑的yaml文件内容格式可能不正确。")


    def write_yaml(self,filename,data):
        """
        写yaml文件
        :param filename:
        :param data:
        :return:
        """
        try:
            with open(filename + ".yaml",  encoding="utf-8", mode="a") as f:
                yaml.dump(data, stream=f, allow_unicode=True)
            # print(f"数据成功写入到文件：{filename}，内容如下：{data}")
        except Exception as e:
            print(e)


    def clear_yaml(self,filename):
        """
        清空yaml数据
        :param filename:
        :return:
        """
        try:
            with open(filename + ".yaml", encoding="utf-8", mode="w") as f:
                   f.truncate()
            # print("数据全部清空啦！！！")
        except Exception as e:
            print(e)


#
# if __name__ == '__main__':
#     a = ReadYaml()
#     b=a.read_yaml("../testcase_py/get_session")
#     print(b)
#     # a.write_yaml("../data/test002", {"qb": {"host": "123456", "port": "3306"}})
#     # a.clear_yaml("../data/test002")
