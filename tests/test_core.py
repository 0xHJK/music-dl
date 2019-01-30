#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: test_core
@time: 2019-01-30
"""

from music_dl import config
from music_dl import core
from music_dl.music import Music


def test_music_list_merge():
    config.init()
    m1 = Music()
    m1.size, m1.title, m1.singer = 4.3, "七里香", "周杰伦"
    m2 = Music()
    m2.size, m2.title, m2.singer = 5.3, "告白气球", "周杰伦"
    m3 = Music()
    m3.size, m3.title, m3.singer = 10.51, "告白气球", "周杰伦"
    m4 = Music()
    m4.size, m4.title, m4.singer = 4.5, "告白气球", "李狗蛋"
    music_list = core.music_list_merge([m1, m2, m3, m4])
    assert len(music_list) == 3
    assert music_list[0] == m4
    assert music_list[1] == m3
    assert music_list[2] == m1


def test_get_sequence():
    assert len(core.get_sequence("asdfkwe")) == 0
    assert core.get_sequence("1 3 4") == [1, 3, 4]
    assert core.get_sequence("1 4-6 20") == [1, 4, 5, 6, 20]
