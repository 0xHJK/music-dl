#!/usr/bin/env python  
#-*- coding:utf-8 _*-  
"""
@author: HJK 
@file: common.py 
@time: 2019-01-09

公用的一些方法

"""

import re

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
