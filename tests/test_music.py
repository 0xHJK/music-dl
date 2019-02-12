#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: test_music
@time: 2019-01-30
"""

import os
from music_dl.music import Music


def test_music(capsys):
    music = Music()
    music.id = 816477
    music.title = "cheering"
    music.singer = "crowd"
    music.ext = "mp3"
    music.album = "sample"
    music.rate = 128
    music.source = "sample"
    music.duration = 28
    music.outdir = "/tmp"
    music.verbose = True
    music.url = "https://github.com/0xHJK/music-dl/raw/master/static/sample.mp3"

    assert music.avaiable
    assert music.size == 0.42
    assert music.duration == "0:00:28"

    os.system("rm /tmp/*.mp3")

    for i in range(10):
        fix = "" if i == 0 else " (%d)" % i
        assert music.fullname == "/tmp/crowd - cheering%s.mp3" % fix
        open(music.fullname, "w").write("")

    str(music)

    music.download()
    out, err = capsys.readouterr()
    assert out.find("/tmp/crowd - cheering")
