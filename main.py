#!/usr/bin/env python  
#-*- coding:utf-8 _*-  
"""
@author: HJK 
@file: main.py 
@time: 2019-01-08

"""

import sys
import threading
import traceback
import glovar
from core.extractors import kugou
from core.extractors import qq
from core.extractors import netease
from core.extractors import baidu
from core.extractors import xiami
from core.common import music_list_merge
from core.exceptions import *
from utils import echo
from utils import cli
from utils.customlog import CustomLog

addons = {
    'qq': qq,
    'kugou': kugou,
    'netease': netease,
    'baidu': baidu,
    'xiami': xiami,
}

logger = CustomLog(__name__).getLogger()

def music_search(source, music_list, errors):
    ''' 音乐搜索，music_list是搜索结果 '''
    try:
        music_list += addons.get(source).search(glovar.get_option('keyword'))
    except (RequestError, ResponseError, DataError) as e:
        errors.append((source, e))
    except Exception as e:
        err = traceback.format_exc() if glovar.get_option('verbose') else str(e)
        errors.append((source, err))
    finally:
        # 放在搜索后输出是为了营造出搜索很快的假象
        echo.brand(source=source)


def music_download(idx, music_list):
    ''' 音乐下载，music_list是搜索结果 '''
    music = music_list[int(idx)]
    try:
        addons.get(music['source']).download(music)
    except Exception as e:
        logger.error('下载音乐失败')
        err = traceback.format_exc() if glovar.get_option('verbose') else str(e)
        logger.error(err)


def main():
    music_list = []
    thread_pool = []
    errors = []

    if not glovar.get_option('keyword'):
        # 如果未设置关键词
        cli.set_music_keyword('请输入要搜索的歌曲，名称和歌手一起输入可以提高匹配（如 空帆船 朴树）：\n > ')

    echo.notice(glovar.get_option('keyword'))

    # 多线程搜索
    for source in glovar.get_option('source').split():
        t = threading.Thread(target=music_search, args=(source, music_list, errors))
        thread_pool.append(t)
        t.start()
    for t in thread_pool:
        t.join()

    # 分割线
    echo.line()
    # 输出错误信息
    for err in errors:
        logger.error('Get %s music list failed.' % err[0].upper())
        logger.error(err[1])

    if glovar.get_option('merge'):
        # 对搜索结果排序和去重
        music_list = music_list_merge(music_list)

    echo.menu(music_list)

    selected = cli.get_music_select()
    for idx in selected:
        music_download(idx, music_list)

    # 下载完后继续搜索
    cli.set_music_keyword()
    main()


if __name__ == '__main__':
    # 初始化全局变量
    glovar.init_option()

    if len(sys.argv) > 1:
        cli.set_opts(sys.argv[1:])
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)

