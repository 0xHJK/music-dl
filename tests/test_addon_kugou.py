#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: test_addon_kugou.py
@time: 2019-06-10
"""


from music_dl.addons import kugou


def test_kugou():
    songs_list = kugou.search("周杰伦")
    assert songs_list is not None
