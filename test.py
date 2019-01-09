#!/usr/bin/env python  
#-*- coding:utf-8 _*-  
"""
@author: HJK 
@file: test.py 
@time: 2019-01-09

简单的测试

"""

from core.extractors import kugou
from core.extractors import qq
from utils import echo

def test_qq():
    music_list = qq.search('女儿国', 5)
    echo.menu(music_list)
    choices = input('请输入要下载的歌曲序号：')
    for i in choices.split():
        if int(i) < 0 or int(i) >= len(music_list): raise ValueError
        music = music_list[int(i)]
        qq.download(music)

def test_kugou():
    music_list = kugou.search('女儿国', 5)
    echo.menu(music_list)
    choices = input('请输入要下载的歌曲序号：')
    for i in choices.split():
        if int(i) < 0 or int(i) >= len(music_list): raise ValueError
        music = music_list[int(i)]
        kugou.download(music)
