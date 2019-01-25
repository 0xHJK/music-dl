#!/usr/bin/env python  
#-*- coding:utf-8 _*-  
"""
@author: HJK 
@file: env.py 
@time: 2019-01-08

全局变量

"""
import logging

FAKE_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',  # noqa
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',  # noqa
    'referer': 'https://www.google.com'
}

IOS_USERAGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'

# QQ下载音乐不能没有User-Agent
# 百度下载音乐User-Agent不能是浏览器，神奇……
WGET_HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "identity",
    "User-Agent": "Wget/1.19.5 (darwin17.5.0)"
}

# 日志
LOG_LEVEL = logging.DEBUG


def init_option():
    # 命令行参数，写到函数里防止被意外初始化
    global OPTS
    OPTS = {
        # 自定义来源 -s --source
        'source': 'qq netease kugou baidu xiami',
        # 自定义数量 -c --count
        'count': 5,
        # 保存目录 -o --outdir
        'outdir': '.',
        # 搜索关键字
        'keyword': '',
        # 显示详情
        'verbose': False,
        # 搜索结果排序和去重
        'merge': False,
        # 代理
        'proxies': None,
    }

def set_option(opt, value):
    OPTS[opt] = value

def get_option(opt):
    return OPTS.get(opt, '')
