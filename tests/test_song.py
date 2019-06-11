#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: test_song
@time: 2019-05-28
"""

import os
from music_dl.song import BasicSong
from music_dl import config


def test_music(capsys):
    config.init()
    config.set("outdir", "/tmp")
    # config.set("cover", True)
    # config.set("lyrics", True)
    config.set("verbose", True)
    song = BasicSong()
    song.id = 816477
    song.title = "cheering"
    song.singer = "crowd"
    song.ext = "mp3"
    song.album = "sample"
    song.rate = 128
    song.source = "sample"
    song.duration = 28
    song.song_url = "https://github.com/0xHJK/music-dl/raw/master/static/sample.mp3"

    assert song.available
    assert song.size == 0.42
    assert song.duration == "0:00:28"

    os.system("rm /tmp/*.mp3")

    assert song.song_fullname == "/tmp/crowd - cheering.mp3"
    assert song.cover_fullname == "/tmp/crowd - cheering.jpg"
    assert song.lyrics_fullname == "/tmp/crowd - cheering.lrc"

    str(song)

    song.download()
    out, err = capsys.readouterr()
    assert out.find("/tmp/crowd - cheering")

    os.system("rm /tmp/*.mp3")
