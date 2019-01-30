#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: test_ext_netease
@time: 2019-01-30
"""

from music_dl.extractors import netease


def test_netease(capsys):
    music_list = netease.search("朴树")
    assert music_list is not None
    # if len(music_list) > 0:
    #     music_list[0].download()
    #     out, err = capsys.readouterr()
    #     assert out.find("已保存到：")
