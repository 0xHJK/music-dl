#!/usr/bin/env python  
#-*- coding:utf-8 _*-  
"""
@author: HJK 
@file: common.py 
@time: 2019-01-09

公用的一些方法

"""

import os
import requests
import wget
import glovar
from utils import echo
from utils.customlog import CustomLog

logger = CustomLog(__name__).getLogger()

def music_download(music):
    ''' 下载音乐保存到本地 '''
    echo.info(music)
    outfile = os.path.abspath(os.path.join(glovar.get_option('outdir'), music['name']))
    try:
        wget.download(music['url'], out=outfile)
        print('\n已保存到：%s\n' % outfile)
    except Exception as e:
        print('')
        logger.error('下载音乐失败：')
        logger.error('URL：%s' % music['url'])
        logger.error('位置：%s\n' % outfile )
        if glovar.get_option('verbose'):
            logger.error(e)


def url_available(url) -> bool:
    s = requests.Session()
    s.headers.update(glovar.FAKE_HEADERS)
    r = s.head(url)
    return r.status_code == requests.codes.ok


def content_length(url) -> int:
    s = requests.Session()
    s.headers.update(glovar.FAKE_HEADERS)
    try:
        r = s.head(url)
        if r.status_code == requests.codes.ok:
            return int(r.headers.get('Content-Length', 0))
    except:
        pass
    return 0

