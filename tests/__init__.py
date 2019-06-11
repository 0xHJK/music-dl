#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: __init__.py
@time: 2019-01-29
"""

import gettext
from music_dl import config

config.init()
gettext.install("music-dl", "locale")
