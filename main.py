#!/usr/bin/env python  
#-*- coding:utf-8 _*-  
"""
@author: HJK 
@file: main.py 
@time: 2019-01-08

"""

import sys
import re
import getopt
import threading
import glovar
from core.extractors import kugou
from core.extractors import qq
from core.extractors import netease
from core.extractors import baidu
from core.extractors import xiami
from core.common import music_list_merge
from utils import echo
from utils.customlog import CustomLog

addons = {
    'qq': qq,
    'kugou': kugou,
    'netease': netease,
    'baidu': baidu,
    'xiami': xiami,
}

logger = CustomLog(__name__).getLogger()

def setopts(args):
    '''
    根据命令行输入的参数修改全局变量
    :param args: 命令行参数列表
    :return:
    '''
    try:
        opts, others = getopt.getopt(args, 'vhmk:s:c:o:',
                                        ['verbose', 'help', 'merge', 'nomerge',
                                         'keyword=', 'source=', 'count=', 'outdir='])
    except getopt.GetoptError as e:
        logger.error('命令解析失败')
        logger.error(e)
        echo.usage()
        sys.exit(2)

    for o, a in opts:
        if o in ('-h', '--help'):
            echo.usage()
            sys.exit(2)
        elif o in ('-v', '--verbose'):
            glovar.set_option('verbose', True)
        elif o in ('-k', '--keyword'):
            glovar.set_option('keyword', a)
        elif o in ('-s', '--source'):
            glovar.set_option('source', a)
        elif o in ('-c', '--count'):
            glovar.set_option('count', int(a))
        elif o in ('-o', '--outdir'):
            glovar.set_option('outdir', a)
        elif o in ('-m', '--merge'):
            glovar.set_option('merge', True)
        elif o in ('--nomerge'):
            glovar.set_option('merge', False)
        else:
            assert False, 'unhandled option'


def music_search(source, music_list, errors):
    ''' 音乐搜索，music_list是搜索结果 '''
    try:
        music_list += addons.get(source).search(glovar.get_option('keyword'))
    except Exception as e:
        errors.append((source, e))
    finally:
        # 放在搜索后输出是为了营造出搜索很快的假象
        echo.brand(source=source)


def music_download(idx, music_list):
    music = music_list[int(idx)]
    try:
        addons.get(music['source']).download(music)
    except Exception as e:
        logger.error('下载音乐失败')
        logger.error(e)


def main():
    music_list = []
    thread_pool = []
    errors = []

    if not glovar.get_option('keyword'):
        # 如果未设置关键词
        keyword = input('请输入要搜索的歌曲，名称和歌手一起输入可以提高匹配（如 空帆船 朴树）：\n > ')
        glovar.set_option('keyword', keyword)

    echo.notice(glovar.get_option('keyword'))

    for source in glovar.get_option('source').split():
        t = threading.Thread(target=music_search, args=(source, music_list, errors))
        thread_pool.append(t)
        t.start()

    for t in thread_pool:
        t.join()

    echo.line()

    for err in errors:
        logger.error('Get %s music list failed.' % err[0].upper())
        logger.error(err[1])

    if glovar.get_option('merge'):
        # 对搜索结果排序和去重
        music_list = music_list_merge(music_list)

    echo.menu(music_list)
    choices = input('请输入要下载的歌曲序号，多个序号用空格隔开：')

    for choice in choices.split():
        start, _, end = choice.partition('-')
        if end:
            for i in range(int(start), int(end)+1):
                music_download(i, music_list)
        else:
            music_download(start, music_list)

    # 下载完后继续搜索
    keyword = input('请输入要搜索的歌曲，或Ctrl+C退出：\n > ')
    glovar.set_option('keyword', keyword)
    main()


if __name__ == '__main__':
    # 初始化全局变量
    glovar.init_option()

    if len(sys.argv) > 1:
        setopts(sys.argv[1:])
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)

