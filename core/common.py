#!/usr/bin/env python  
#-*- coding:utf-8 _*-  
"""
@author: HJK 
@file: common.py 
@time: 2019-01-09

公用的一些方法

"""

import requests
import wget
import glovar
from utils import echo


def music_download(music):
    ''' 下载音乐保存到本地 '''
    echo.info(music)
    wget.download(music['url'], out=music['name'])


def url_available(url) -> bool:
    s = requests.Session()
    s.headers.update(glovar.FAKE_HEADERS)
    r = s.head(url)
    return r.status_code == requests.codes.ok


def content_length(url) -> int:
    s = requests.Session()
    s.headers.update(glovar.FAKE_HEADERS)
    r = s.head(url)
    if r.status_code == requests.codes.ok:
        return int(r.headers.get('Content-Length', 0))
    return 0

