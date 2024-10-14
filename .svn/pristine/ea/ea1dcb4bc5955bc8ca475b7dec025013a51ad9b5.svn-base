# -*- encoding: utf-8 -*-
"""
@时间:   2021/11/14 13:46
@作者:   王齐涛
@文件:   read_ini.py
"""
import os
from configparser import ConfigParser
from common.all_paths import CONFIG_PATH


def get_url(name, key):
    """读取请求url的地址"""
    cf = ConfigParser()
    cf.read(CONFIG_PATH + os.sep + "conf.ini")
    value = cf.get(name, key)
    return value


class ReadINI:

    def __init__(self, path_name):
        self.con = ConfigParser()
        self.con.read(path_name + ".ini")

    def read_ini(self, name, key):
        value = self.con.get(name, key)
        return value

    def write_ini(self):
        pass




"""
ini配置文件以.ini结尾，config文件以.config结尾，他们的配置方式相同
配置文件由两部分组成sections与items，sections 用来区分不同的配置块，items 是sections下面的键值。
cf = ConfigParser()
cf.read("mysql_data.ini")
print(cf.sections())
print(cf.options("mysql"))   #输出MySQL下的所有配置项
print(cf.items("mysql"))    #输出MySQL下的所有键值对
print(cf.get("mysql","host"))   #输出MySQL下的host值
"""