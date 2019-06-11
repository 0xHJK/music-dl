#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: test_addon_baidu.py
@time: 2019-06-10
"""


from music_dl.addons import baidu


def test_baidu():
    songs_list = baidu.search("许巍")
    assert songs_list is not None
