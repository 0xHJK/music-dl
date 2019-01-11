#!/usr/bin/env python  
#-*- coding:utf-8 _*-  
"""
@author: HJK 
@file: main.py 
@time: 2019-01-08

"""

import sys
import re
from core.extractors import kugou
from core.extractors import qq
from core.extractors import netease
from utils import echo
from utils.customlog import CustomLog

addons = {
    'qq': qq,
    'kugou': kugou,
    'netease': netease,
}

logger = CustomLog(__name__).getLogger()

def indexOrRange(item):
    pattern=r'^(\d*)[-,:](\d*)$'
    m=re.match(pattern,str(item))
    if m:
        index1=int(m.group(1))
        index2=int(m.group(2))
        return 'range' , list(range(index1,index2+1))
    else:
        return 'index' , item

def downloadByIndexList(indexlist,music_list):
    for i in indexlist:
        itemtype,value=indexOrRange(i)
        if itemtype=='range' :
            downloadByIndexList(value,music_list)
            continue
        if int(i) < 0 or int(i) >= len(music_list): raise ValueError
        music = music_list[int(i)]
        addons.get(music['source']).download(music)
    return

def main(keyword):
    music_list = []
    try:
        music_list += qq.search(keyword)
    except Exception as e:
        logger.error('Get QQ music list failed.')
        logger.error(e)
    try:
        music_list += kugou.search(keyword)
    except Exception as e:
        logger.error('Get KUGOU music list failed.')
        logger.error(e)
    try:
        music_list += netease.search(keyword)
    except Exception as e:
        logger.error('Get NETEASE music list failed.')
        logger.error(e)

    echo.menu(music_list)
    choices = input('请输入要下载的歌曲序号，多个序号用空格隔开：')
    downloadByIndexList(choices.split(),music_list)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        keyword = input('请输入要搜索的歌曲，名称和歌手一起输入可以提高匹配（如 空帆船 朴树）：\n > ')
    else:
        keyword = ' '.join(sys.argv[1:])
    main(keyword)

