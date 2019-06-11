#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: test_addon_netease.py
@time: 2019-06-10
"""


from music_dl.addons import netease


def test_netease():
    songs_list = netease.search("谢春花")
    assert songs_list is not None
