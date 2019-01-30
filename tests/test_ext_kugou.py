#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: test_ext_kugou
@time: 2019-01-30
"""

from music_dl.extractors import kugou


def test_kugou(capsys):
    music_list = kugou.search("周杰伦")
    assert music_list is not None
    # if len(music_list) > 0:
    #     music_list[0].download()
    #     out, err = capsys.readouterr()
    #     assert out.find("已保存到：")
