#!/usr/bin/env python  
#-*- coding:utf-8 _*-  
"""
@author: HJK 
@file: customlog.py 
@time: 2019-01-08

自定义日志格式

"""

import logging
import glovar


class CustomLog(object):
    def __init__(self, name, level=glovar.LOG_LEVEL):
        super(CustomLog, self).__init__()
        self.name = name
        self.level = level

        # 控制台输出样式
        self.formatter = logging.Formatter(
            fmt='[%(asctime)s] %(levelname)-8s | %(msg)s （%(filename)s %(funcName)s %(lineno)s）',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self.level)

        # 如果已有handler则不再处理
        # 修复重复输出的bug
        if self.logger.handlers:
            return

        sh = logging.StreamHandler()
        sh.setLevel(self.level)
        sh.setFormatter(self.formatter)

        self.logger.addHandler(sh)

    def getLogger(self):
        return self.logger

