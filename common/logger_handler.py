# -*- encoding: utf-8 -*-
"""
@时间:   2021/11/13 12:10
@作者:   王齐涛
@文件:   test04.py 
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import logging
import os
import colorlog
from logging.handlers import RotatingFileHandler
from datetime import datetime
from common.all_paths import BASE_DIR

# 配置日志文件名称及路径
log_path = os.path.join(BASE_DIR, 'logs')     # log_path为存放日志的路径
if not os.path.exists(log_path):
    os.mkdir(log_path)    # 若不存在logs文件夹，则自动创建

# 终端输出日志颜色配置
colors = {
    'DEBUG': 'white',
    'INFO': 'cyan',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}

# 定义控制台和日志文件的格式
console_fmt = "%(log_color) s%(asctime)s -[line:%(lineno)d]-%(levelname)s-[日志信息]: %(message)s"
logger_fmt = "%(asctime)s - %(filename)s - [line:%(lineno)d] - %(levelname)s - [日志信息]: %(message)s"


class GetLogger:
    """
    先创建日志记录器（logging.getLogger），然后再设置日志级别（logger.setLevel），
    接着再创建日志文件或者控制台（logging.FileHandler或logging.StreamHandler），日志文件有个存放路径参数
    然后再设置日志格式（logging.Formatter），最后再将日志处理程序记录到记录器（addHandler）
    """

    def __init__(self):
        self.__now_time = datetime.now().strftime('%Y-%m-%d')  # 当前日期格式化

        # 收集所有日志文件，名称为：[日志名称] 2020-01-01-all.log；收集错误日志信息文件，名称为：[日志名称] 2020-01-01-error.log
        # 其中，[日志名称]为调用日志时的传入参数
        self.__all_log_path = os.path.join(log_path, self.__now_time + "-all" + ".log")  # 收集所有日志信息文件
        self.__error_log_path = os.path.join(log_path, self.__now_time + "-error" + ".log")  # 收集错误日志信息文件

        # 配置日志记录器及其级别，设置默认日志记录器记录级别为DEBUG
        self.__logger = logging.getLogger()  # 创建日志记录器
        self.__logger.setLevel(logging.DEBUG)  # 设置默认日志记录器记录级别


# 文件日志相关配置
    @staticmethod
    def __init_logger_handler(log_path):
        """
        创建文件日志处理器，用于收集日志
        :param log_path:
        :return:
        """
        # 写入文件，如果文件超过1M大小时，切割日志文件
        logger_handler = RotatingFileHandler(filename=log_path, maxBytes=1 * 1024 * 1024, encoding='utf-8', backupCount=3)  # 可以设置 backupCount=3 在切割日志文件后仅保留3个文件
        return logger_handler

    @staticmethod
    def __set_log_formatter(file_handler):
        """
        设置日志输出格式-日志文件
        :param file_handler:
        """
        # datefmt用于设置asctime的格式，例如：%a, %d %b %Y %H:%M:%S 或者 %Y-%m-%d %H:%M:%S
        formatter = logging.Formatter(fmt=logger_fmt,datefmt="%Y-%m-%d %X")
        file_handler.setFormatter(formatter)

    def __set_color_handle(self, console_handler):
        """
        设置文件日志级别并添加到文件日志处理器
        :param console_handler:
        :param level:
        """
        console_handler.setLevel(level=logging.DEBUG)
        self.__logger.addHandler(console_handler)


# 控制台相关配置
    @staticmethod
    def __init_console_handle():
        """创建控制台日志处理器，用于输出到控制台"""
        console_handle = colorlog.StreamHandler()
        return console_handle

    @staticmethod
    def __set_color_formatter(console_handle):
        """
        设置输出格式-控制台
        :param console_handle:
        :param color_config: 控制台打印颜色配置信息
        :return:
        """
        formatter = colorlog.ColoredFormatter(console_fmt,log_colors=colors,datefmt="%Y-%m-%d %X")
        console_handle.setFormatter(formatter)

    def __set_log_handler(self, logger_handler, level=logging.DEBUG):
        """
        设置控制台级别并添加到控制台日志处理器
        :param logger_handler:
        :param level:
        """
        logger_handler.setLevel(level=level)
        self.__logger.addHandler(logger_handler)  # 添加到logger收集器

# 关闭日志记录器
    @staticmethod
    def __close_handler(file_handler):
        """
        关闭handler
        :param file_handler: 日志记录器
        """
        file_handler.close()

# 调用内部方法
    def __console(self, level, message):
        """构造日志收集器"""
        try:
            # 1.创建日志器   （__init__ 已定义好了）
            # 2.定义处理器,控制台和文本输出两种方式,文本的话要输入路径
            all_logger_handler = self.__init_logger_handler(self.__all_log_path)  # 收集所有日志文件
            error_logger_handler = self.__init_logger_handler(self.__error_log_path)  # 收集错误日志信息文件
            console_handle = self.__init_console_handle()
            # 3.设置日志文件格式
            self.__set_log_formatter(all_logger_handler)
            self.__set_log_formatter(error_logger_handler)
            self.__set_color_formatter(console_handle)
            # 4.将日志器添加到处理器中
            self.__set_log_handler(all_logger_handler)  # 设置handler级别并添加到logger收集器
            self.__set_log_handler(error_logger_handler, level=logging.ERROR)
            self.__set_color_handle(console_handle)
            # 5.下面的方法进行调用，判断传入的level参数,打印对应的信息
            if level == 'info':
                self.__logger.info(message)
            elif level == 'debug':
                self.__logger.debug(message)
            elif level == 'warning':
                self.__logger.warning(message)
            elif level == 'error':
                # exc_info=True, stack_info=True 用于在日志中记录堆栈信息，方便查看日志进行调试
                self.__logger.error(message, exc_info=False,stack_info=False)
            elif level == 'critical':
                # exc_info=True, stack_info=True 用于在日志中记录堆栈信息，方便查看日志进行调试
                self.__logger.critical(message, exc_info=True, stack_info=True)
            # 6.每次调用过后就要删掉日志器，关闭文件日志记录器，避免重复输出日志
            self.__logger.removeHandler(all_logger_handler)  # 避免日志输出重复问题
            self.__logger.removeHandler(error_logger_handler)
            self.__logger.removeHandler(console_handle)
            self.__close_handler(all_logger_handler)
            self.__close_handler(error_logger_handler)
        except:
            raise


# 定义外部调用方法
    def debug(self, message):
        self.__console('debug', message)
    def info(self, message):
        self.__console('info', message)
    def warning(self, message):
        self.__console('warning', message)
    def error(self, message):
        self.__console('error', message)
    def critical(self, message):
        self.__console('critical', message)


# if __name__ == '__main__':
    # log = HandleLog(os.path.split(__file__)[-1].split(".")[0])
    # log.info("这是日志信息")
    # log.debug("这是debug信息")
    # log.warning("这是警告信息")
    # log.error("这是错误日志信息")
    # log.critical("这是严重级别信息")
    # logging.exception()

# 注：不知道为什么不能通过yaml文件来调用
# logger = ReadYaml().read_yaml("./config/log_data")
# console_fmt = logger["log"]["logger_fmt"]
# logger_fmt = logger["log"]["logger_fmt"]
# date_fmt = logger["log"]["date_fmt"]
# colors = logger["log"]["colors"]