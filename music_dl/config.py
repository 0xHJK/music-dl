#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author: HJK
@file: config.py
@time: 2019-01-27

全局变量

"""

__all__ = ["init", "set", "get"]


def init():
    global opts
    opts = {
        # 自定义来源 -s --source
        "source": "qq netease kugou baidu xiami",
        # 自定义数量 -c --count
        "count": 5,
        # 保存目录 -o --outdir
        "outdir": ".",
        # 搜索关键字
        "keyword": "",
        # 显示详情
        "verbose": False,
        # 搜索结果排序和去重
        "merge": False,
        # 代理
        "proxies": None,
        # 一般情况下的headers
        "fake_headers": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",  # noqa
            "Accept-Charset": "UTF-8,*;q=0.5",
            "Accept-Encoding": "gzip,deflate,sdch",
            "Accept-Language": "en-US,en;q=0.8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",  # noqa
            "referer": "https://www.google.com",
        },
        # QQ下载音乐不能没有User-Agent
        # 百度下载音乐User-Agent不能是浏览器
        # 下载时的headers
        "wget_headers": {
            "Accept": "*/*",
            "Accept-Encoding": "identity",
            "User-Agent": "Wget/1.19.5 (darwin17.5.0)",
        },
        # 移动端useragent
        "ios_useragent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46"
        + " (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
    }


def get(key):
    return opts.get(key, "")


def set(key, value):
    opts[key] = value
