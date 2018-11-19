# -*- coding: utf-8 -*-
# @Date:   2017-10-25 10:29:58
# @Last Modified time: 2018-01-20 21:28:45
import os
import sys
import logging
import logging.config
from logging import handlers
from .utils import get_script_path


class Colors(object):
    """
    打印颜色
    """
    @classmethod
    def create_color_str(cls, display: int, fg_color: int, bg_color: int, message: str) -> str:
        return '\033[%s;%s;%sm %s \033[0m' % (
            display, fg_color, bg_color, message
        )

    @classmethod
    def error_message(cls, message: str) -> str:
        return cls.create_color_str(1, 31, 40, message)

    @classmethod
    def info_message(cls, message: str) -> str:
        return cls.create_color_str(1, 32, 40, message)


color = Colors()


def rollback_handler(log_file: str) -> handlers.RotatingFileHandler:
    rollback = handlers.RotatingFileHandler(
        filename='{}.log'.format(log_file),
        mode='a',
        maxBytes=10000,
        backupCount=10
    )
    rollback.setFormatter(
        logging.Formatter(
            fmt='%(asctime)s %(levelname)s at %(filename)s[line:%(lineno)d]\n%(message)s', datefmt='%Y-%m-%d %H:%M:%S'
        )
    )
    rollback.setLevel(logging.ERROR)
    return rollback


def stream_info_handler() -> logging.StreamHandler:
    info_handler = logging.StreamHandler(sys.stdout)
    info_handler.setFormatter(
        logging.Formatter(
            fmt='%(levelname)s at %(filename)s\n{}'.format(color.info_message('%(message)s'))
        )
    )
    info_handler.setLevel(logging.INFO)  # levelno > INFO
    info_filter = logging.Filter()       # levelno < ERROR
    info_filter.filter = lambda record: record.levelno < logging.ERROR
    info_handler.addFilter(info_filter)
    return info_handler


def stream_error_handler() -> logging.StreamHandler:
    error_handler = logging.StreamHandler(sys.stderr)
    error_handler.setFormatter(
        logging.Formatter(
            fmt='%(levelname)s at %(filename)s[line:%(lineno)d]\n{}'.format(color.error_message('%(message)s'))
        )
    )
    error_handler.setLevel(logging.ERROR)  # levelno > ERROR
    return error_handler


def logger_facade(log_path: str, name: str) -> logging.getLogger():
    """
    logging 模块内部存在线程锁
    logger.error() 不能再封装，否则无法正确打印 lineno
    logger.getLogger(name)
        无法靠类的实例区分，只靠 name 区分
        多次 getLogger 使用同一个 name 会造成重复打印
    """
    log_file = os.path.join(get_script_path(), log_path, name)
    logger = logging.getLogger(name=name)
    logger.addHandler(stream_info_handler())
    logger.addHandler(stream_error_handler())
    logger.addHandler(rollback_handler(log_file))
    logger.setLevel(logging.INFO)
    return logger
