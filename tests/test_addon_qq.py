#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: test_addon_qq.py
@time: 2019-06-10
"""


from music_dl.addons import qq


def test_qq():
    songs_list = qq.search("周杰伦")
    assert songs_list is not None
