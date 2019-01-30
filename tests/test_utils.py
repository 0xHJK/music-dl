#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: test_utils.py
@time: 2019-01-30
"""

import platform
from music_dl import utils


def test_color():
    if platform.system() == "Windows":
        assert utils.colorize("music-dl", "qq") == "music-dl"
        assert utils.colorize(1234, "qq") == "1234"
    else:
        assert utils.colorize("music-dl", "qq") == "\033[92mmusic-dl\033[0m"
        assert utils.colorize(1234, "xiami") == "\033[93m1234\033[0m"
    assert utils.colorize("music-dl", "fsadfasdg") == "music-dl"
