#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: flac.py
@time: 2019-05-08
"""

from .basic import BasicSong

class FlacSong(BasicSong):
    def __init__(self):
        super(FlacSong, self).__init__()
