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
    music.title = "晴天"
    music.singer = "周杰伦"
    music.ext = "mp3"
    music.album = "叶惠美"
    music.rate = 128
    music.source = "baidu"
    music.duration = 269
    music.outdir = "/tmp"
    music.verbose = True
    music.url = "http://zhangmenshiting.qianqian.com/data2/music/ab9c8eb09a3dac4df11c1256eb6cb422/599519664/816477248400128.mp3?xcode=9df0a76ce2477d6837ff48ca31f559c2"

    assert music.avaiable
    assert music.size == 4.12
    assert music.duration == "0:04:29"

    os.system("rm /tmp/*.mp3")

    for i in range(10):
        fix = "" if i == 0 else " (%d)" % i
        assert music.fullname == "/tmp/周杰伦 - 晴天%s.mp3" % fix
        open(music.fullname, "w").write("")

    music.download()
    out, err = capsys.readouterr()
    assert out.find("已保存到：/tmp/周杰伦 - 晴天")
