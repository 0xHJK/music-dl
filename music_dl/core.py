#!/usr/bin/env python  
#-*- coding:utf-8 _*-  
"""
@author: HJK 
@file: common.py 
@time: 2019-01-09

公用的一些方法

"""

import re
import importlib
import traceback
from . import config
from . import utils
from .exceptions import *
from .log import CustomLog

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
        utils.brand(source=source)


def music_download(idx, music_list):
    ''' 音乐下载，music_list是搜索结果 '''
    music = music_list[int(idx)]
    try:
        addon = importlib.import_module('.extractors.' + music.source, __package__)
        addon.download(music)
    except Exception as e:
        logger.error('下载音乐失败')
        err = traceback.format_exc() if config.get('verbose') else str(e)
        logger.error(err)


def music_list_merge(music_list) -> list:
    ''' 搜索结果合并 '''
    # 先排序
    music_list.sort(key=lambda music: (music.singer, music.title, music.size), reverse=True)
    result_list = []
    for i in range(len(music_list)):
        # 如果名称、歌手都一致的话就去重，保留最大的文件
        if i > 0 \
            and music_list[i].size <= music_list[i-1].size \
            and music_list[i].title == music_list[i-1].title \
            and music_list[i].singer == music_list[i-1].singer:
            continue
        result_list.append(music_list[i])

    return result_list


def get_sequence(numbers) -> list:
    ''' 输入3 4-6 9，返回一个列表[3,4,5,6,9] '''
    result = []
    if not re.match(r'^((\d+\-\d+)|(\d+)|\s+)+$', numbers):
        return result

    for choice in numbers.split():
        start, _, end = choice.partition('-')
        if end:
            result += range(int(start), int(end)+1)
        else:
            result.append(start)

    return result
