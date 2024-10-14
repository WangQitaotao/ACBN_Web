# -*- encoding: utf-8 -*-
'''
@时间 ： 2021/11/8 22:21
@作者 ： 王齐涛
@文件名称： times.py
'''
import time
import datetime
from functools import wraps

from common.logger_handler import GetLogger

log = GetLogger()

def timestamp():
    """时间戳"""
    return time.time()


def dt_strftime(fmt="%Y%m"):
    """
    datetime格式化时间
    :param fmt "%Y%m%d %H%M%S
    """
    return datetime.datetime.now().strftime(fmt)


def sleep(seconds=1.0):
    """
    睡眠时间
    """
    time.sleep(seconds)


def running_time(func):
    """统计函数的运行时间"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = timestamp()
        res = func(*args, **kwargs)
        log.debug("执行完成！用时%.3f秒！" % (timestamp() - start))
        return res
    return wrapper


if __name__ == '__main__':
    print(dt_strftime("%Y%m%d%H%M%S"))
