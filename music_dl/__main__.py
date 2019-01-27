#!/usr/bin/env python  
#-*- coding:utf-8 _*-  
"""
@author: HJK 
@file: main.py 
@time: 2019-01-08

"""

import sys
import re
import threading
import click
from . import config
from .utils import colorize
from .core import *
from .exceptions import *
from .log import CustomLog

__version__ = '2.0.0'

# 初始化全局变量
config.init()
logger = CustomLog(__name__).getLogger()

def run():
    music_list = []
    thread_pool = []
    errors = []

    click.echo('\nSearching %s from ...' % colorize(config.get('keyword'), 'yellow'), nl=False)

    # 多线程搜索
    for source in config.get('source').split():
        t = threading.Thread(target=music_search, args=(source, music_list, errors))
        thread_pool.append(t)
        t.start()
    for t in thread_pool:
        t.join()

    # 分割线
    click.echo('\n---------------------------\n')
    # 输出错误信息
    for err in errors:
        logger.error('Get %s music list failed.' % err[0].upper())
        logger.error(err[1])

    if config.get('merge'):
        # 对搜索结果排序和去重
        music_list = music_list_merge(music_list)

    for index, music in enumerate(music_list):
        idx = colorize(' [ %2s ] ' % index, 'cyan')
        click.echo(idx + music.info)

    choices = click.prompt('请输入下载序号，多个序号用空格隔开，输入N跳过下载\n >>')
    while choices.lower() != 'n' and not re.match(r'^((\d+\-\d+)|(\d+)|\s+)+$', choices):
        choices = click.prompt('输入有误！仅支持形如 0 3-5 8 的格式，输入N跳过下载\n >>')

    selected_list = get_sequence(choices)
    for idx in selected_list:
        music_download(idx, music_list)

    # 下载完后继续搜索
    keyword = click.prompt('请输入要搜索的歌曲，或Ctrl+C退出\n >>')
    config.set('keyword', keyword)
    run()


@click.command()
@click.version_option()
@click.option('-k', '--keyword', prompt='请输入要搜索的歌曲，名称和歌手一起输入可以提高匹配（如 空帆船 朴树）\n >>',
              help='搜索关键字')
@click.option('-s', '--source', default='qq netease kugou baidu xiami',
              help='数据源目前支持qq netease kugou baidu xiami flac')
@click.option('-c', '--count', default=5, help='搜索数量限制')
@click.option('-o', '--outdir', default='.', help='指定输出目录')
@click.option('-x', '--proxy', default='', help='指定代理（如http://127.0.0.1:1087）')
@click.option('-m', '--merge', default=False, is_flag=True,
              help='对搜索结果去重和排序（默认不去重）')
@click.option('-v', '--verbose', default=False, is_flag=True,
              help='详细模式')
def main(keyword, source, count, outdir, proxy, merge, verbose):
    '''
        Search and download music from netease, qq, kugou, baidu and xiami.
        example: music-dl -k "周杰伦" -s "qq  baidu xiami" -c 10 -o "/tmp
    '''
    # if len(sys.argv) > 1:
    #     cli.set_opts(sys.argv[1:])
    config.set('keyword', keyword)
    config.set('source', source)
    config.set('count', count)
    config.set('outdir', outdir)
    config.set('merge', merge)
    config.set('verbose', verbose)
    if proxy:
        proxies = {
            'http': proxy,
            'https': proxy
        }
        config.set('proxies', proxies)
    try:
        run()
    except (EOFError, KeyboardInterrupt):
        sys.exit(0)

if __name__ == '__main__':
    main()
