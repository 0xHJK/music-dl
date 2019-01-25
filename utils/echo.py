#!/usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author: HJK 
@file: echo.py 
@time: 2019-01-09

控制台输出内容控制

"""
import platform
import glovar

colors = {
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'pink': '\033[95m',
    'cyan': '\033[96m',

    'qq': '\033[92m',
    'kugou': '\033[94m',
    'netease': '\033[91m',
    'baidu': '\033[96m',
    'xiami': '\033[93m',
    'flac': '\033[95m',
}


def colorize(string, color):
    if not color in colors: return string
    if platform.system() == 'Windows':
        return string
    return colors[color] + string + '\033[0m'


def info(music):
    ''' 打印歌曲信息 '''
    if not glovar.get_option('verbose'):
        return
    s = '\n ------------ \n -> 歌曲：%s\n -> 歌手：%s\n -> 时长: %s\n -> 大小: %s\n -> 比特率: %s\n -> URL: %s\n' % \
        (music['title'], music['singer'], music['duration'], music['size'], music['rate'], music['url'])
    print(s)


def menu(music_list):
    ''' 打印歌曲列表信息 '''
    for music in music_list:
        idx = colorize(' [ %2s ] ' % music_list.index(music), 'cyan')
        source = colorize('%7s | ' % music['source'].upper(), music['source'])
        size = colorize('%5sMB' % music['size'], 'yellow')
        title = colorize(music['title'], 'yellow')
        info = '%s - %s - %s - %s - %s' % \
               (music['duration'], size, music['singer'], title, music['album'])

        print(idx + source + info)

def usage():
    print('usage: python main.py [-k keyword] [-s source] [-c count] [-o outdir] [-v] [-m]')
    print('\t%-16s %s' % ('-h --help ', '帮助'))
    print('\t%-16s %s' % ('-v --verbose ', '详细模式'))
    print('\t%-16s %s' % ('-m --merge ', '对搜索结果去重和排序'))
    print('\t%-16s %s' % ('--nomerge ', '对搜索结果不去重（默认不去重）'))
    print('\t%-16s %s' % ('-k --keyword= ', '搜索关键字'))
    print('\t%-16s %s' % ('-s --source= ', '数据源目前支持qq netease kugou baidu xiami flac'))
    print('\t%-16s %s' % ('-c --count= ', '数量限制'))
    print('\t%-16s %s' % ('-o --outdir= ', '指定输出目录'))
    print('\t%-16s %s' % ('-x --proxy= ', '指定代理（如http://127.0.0.1:1087）'))
    print('example: python main.py -k "周杰伦" -s "qq netease kugou baidu xiami" -c 10 -o "/tmp"')


def notice(keyword):
    print('\nSearching %s from ...' % colorize(keyword, 'yellow'), end='', flush=True)

def brand(source):
    print(' %s ...' % colorize(source.upper(), source), end='', flush=True)

def line():
    print('\n---------------------------\n')