#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: test_source.py
@time: 2019-06-11
"""


from music_dl.source import MusicSource


def test_search():
    ms = MusicSource()
    songs_list = ms.search("五月天", ["baidu"])
    assert songs_list is not None


# def test_single():
#     ms = MusicSource()
#     song = ms.single("https://music.163.com/#/song?id=26427663")
#     assert song is not None
#
#
# def test_playlist():
#     ms = MusicSource()
#     songs_list = ms.playlist("https://music.163.com/#/playlist?id=2602222983")
#     assert songs_list is not None
