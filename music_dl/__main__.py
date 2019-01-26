#!/usr/bin/env python  
#-*- coding:utf-8 _*-  
"""
@author: HJK 
@file: main.py 
@time: 2019-01-08

"""

import sys
import importlib
import threading
import traceback
import click
from . import config
from .common import music_list_merge
from .exceptions import *
from .utils import echo
from .utils import cli
from .utils.log import CustomLog

__version__ = '2.0.0'

# 初始化全局变量
config.init()
logger = CustomLog(__name__).getLogger()

def music_search(source, music_list, errors):
    ''' 音乐搜索，music_list是搜索结果 '''
    try:
        addon = importlib.import_module('.extractors.' + source, __package__)
        music_list += addon.search(config.get('keyword'))
    except (RequestError, ResponseError, DataError) as e:
        errors.append((source, e))
    except Exception as e:
        err = traceback.format_exc() if config.get('verbose') else str(e)
        errors.append((source, err))
    finally:
        # 放在搜索后输出是为了营造出搜索很快的假象
        echo.brand(source=source)


def music_download(idx, music_list):
    ''' 音乐下载，music_list是搜索结果 '''
    music = music_list[int(idx)]
    try:
        addon = importlib.import_module('.extractors.' + music['source'], __package__)
        addon.download(music)
    except Exception as e:
        logger.error('下载音乐失败')
        err = traceback.format_exc() if config.get('verbose') else str(e)
        logger.error(err)


def run():
    music_list = []
    thread_pool = []
    errors = []

    if not config.get('keyword'):
        # 如果未设置关键词
        cli.set_music_keyword('请输入要搜索的歌曲，名称和歌手一起输入可以提高匹配（如 空帆船 朴树）：\n > ')

    echo.notice(config.get('keyword'))

    # 多线程搜索
    for source in config.get('source').split():
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

    if config.get('merge'):
        # 对搜索结果排序和去重
        music_list = music_list_merge(music_list)

    echo.menu(music_list)

    selected = cli.get_music_select()
    for idx in selected:
        music_download(idx, music_list)

    # 下载完后继续搜索
    cli.set_music_keyword()
    run()

@click.command()
@click.version_option()
@click.option('-k', '--keyword', prompt='请输入要搜索的歌曲，名称和歌手一起输入可以提高匹配（如 空帆船 朴树）',
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
