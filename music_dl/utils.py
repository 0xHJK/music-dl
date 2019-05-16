#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author: HJK
@file: utils.py
@time: 2019-01-28

控制台输出内容控制

"""
import platform

colors = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "pink": "\033[35m",
    "cyan": "\033[36m",
    "qq": "\033[92m",
    "kugou": "\033[94m",
    "netease": "\033[91m",
    "baidu": "\033[96m",
    "xiami": "\033[93m",
    "flac": "\033[95m",
    "highlight": "\033[93m",
    "error": "\033[31m",
}


def colorize(string, color):
    string = str(string)
    if color not in colors:
        return string
    if platform.system() == "Windows":
        return string
    return colors[color] + string + "\033[0m"
