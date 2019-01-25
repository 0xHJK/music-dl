#!/usr/bin/env python  
#-*- coding:utf-8 _*-  
"""
@author: HJK 
@file: cli.py 
@time: 2019-01-23

负责用户交互

"""
import re
import sys
import getopt
import glovar
from utils import echo
from utils.customlog import CustomLog

logger = CustomLog(__name__).getLogger()

def set_opts(args):
    '''
    根据命令行输入的参数修改全局变量
    :param args: 命令行参数列表
    :return:
    '''
    try:
        opts, others = getopt.getopt(args, 'vhmk:s:c:o:x:',
                                        ['verbose', 'help', 'merge', 'nomerge',
                                         'keyword=', 'source=', 'count=', 'outdir=', 'proxy='])
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
            c = int(a) if int(a) < 51 else 50
            glovar.set_option('count', c)
        elif o in ('-o', '--outdir'):
            glovar.set_option('outdir', a)
        elif o in ('-x', '--proxy'):
            proxies = { 'http': a, 'https': a}
            glovar.set_option('proxies', proxies)
        elif o in ('-m', '--merge'):
            glovar.set_option('merge', True)
        elif o in ('--nomerge'):
            glovar.set_option('merge', False)
        else:
            assert False, 'unhandled option'


def get_music_select(comment='请输入下载序号，多个序号用空格隔开，输入N跳过下载：\n > ') -> list:
    ''' 得到用户选择的序号，返回一个列表 '''
    selected = []

    choices = input(comment)
    if choices.lower() == 'n':
        print('')
        return selected
    if not re.match(r'^((\d+\-\d+)|(\d+)|\s+)+$', choices):
        return get_music_select('%s仅支持形如 0 3-5 8 的格式，输入N跳过下载：\n > ' % echo.colorize('输入有误！', 'red'))

    for choice in choices.split():
        start, _, end = choice.partition('-')
        if end:
            selected += range(int(start), int(end)+1)
        else:
            selected.append(start)

    return selected


def set_music_keyword(comment='请输入要搜索的歌曲，或Ctrl+C退出：\n > '):
    keyword = input(comment)
    glovar.set_option('keyword', keyword)

