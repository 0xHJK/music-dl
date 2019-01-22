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


def music_list_merge(music_list) -> list:
    ''' 搜索结果合并 '''
    # 先排序
    music_list.sort(key=lambda music: (music['singer'], music['title'], music['size']), reverse=True)
    result_list = []
    for i in range(len(music_list)):
        # 如果名称、歌手都一致的话就去重，保留最大的文件
        if i != 0 \
            and music_list[i]['size'] <= music_list[i-1]['size'] \
            and music_list[i]['title'] == music_list[i-1]['title'] \
            and music_list[i]['singer'] == music_list[i-1]['singer']:
            continue
        result_list.append(music_list[i])

    return result_list
