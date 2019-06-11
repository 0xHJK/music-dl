#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: qq.py
@time: 2019-05-08
"""

import random
import base64
import copy
from .. import config
from ..api import MusicApi
from ..song import BasicSong


class QQApi(MusicApi):
    session = copy.deepcopy(MusicApi.session)
    session.headers.update(
        {
            "referer": "https://y.qq.com/portal/player.html",
            "User-Agent": config.get("ios_useragent"),
        }
    )


class QQSong(BasicSong):
    def __init__(self):
        super(QQSong, self).__init__()
        self.mid = ""

    def download_lyrics(self):
        url = "https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg"
        params = {
            "songmid": self.mid,
            "loginUin": "0",
            "hostUin": "0",
            "format": "json",
            "inCharset": "utf8",
            "outCharset": "utf-8",
            "notice": "0",
            "platform": "yqq.json",
            "needNewCode": "0",
        }

        res_data = QQApi.request(
            "https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg",
            method="GET",
            data=params,
        )
        lyric = res_data.get("lyric", "")
        self.lyrics_text = base64.b64decode(lyric).decode("utf-8")
        super(QQSong, self)._save_lyrics_text()

    def download_cover(self):
        pass

    def download(self):
        # 计算vkey
        guid = str(random.randrange(1000000000, 10000000000))
        params = {"guid": guid, "format": "json", "json": 3}

        QQApi.session.headers.update({"referer": "http://y.qq.com"})
        res_data = QQApi.request(
            "http://base.music.qq.com/fcgi-bin/fcg_musicexpress.fcg",
            method="GET",
            data=params,
        )
        vkey = res_data.get("key", "")

        for prefix in ["M800", "M500", "C400"]:
            url = (
                "http://dl.stream.qqmusic.qq.com/%s%s.mp3?vkey=%s&guid=%s&fromtag=1"
                % (prefix, self.mid, vkey, guid)
            )
            self.song_url = url
            if self.available:
                self.rate = 320 if prefix == "M800" else 128
                break
        super(QQSong, self).download()


def qq_search(keyword) -> list:
    """ 搜索音乐 """
    number = config.get("number") or 5
    params = {"w": keyword, "format": "json", "p": 1, "n": number}

    songs_list = []
    QQApi.session.headers.update(
        {"referer": "http://m.y.qq.com", "User-Agent": config.get("ios_useragent")}
    )
    res_data = (
        QQApi.request(
            "http://c.y.qq.com/soso/fcgi-bin/search_for_qq_cp",
            method="GET",
            data=params,
        )
        .get("data", {})
        .get("song", {})
        .get("list", [])
    )

    for item in res_data:
        # 获得歌手名字
        singers = [s.get("name", "") for s in item.get("singer", "")]
        song = QQSong()
        song.source = "qq"
        song.id = item.get("songid", "")
        song.title = item.get("songname", "")
        song.singer = "、".join(singers)
        song.album = item.get("albumname", "")
        song.duration = item.get("interval", 0)
        song.size = round(item.get("size128", 0) / 1048576, 2)
        # 特有字段
        song.mid = item.get("songmid", "")

        songs_list.append(song)

    return songs_list


def qq_playlist(url):
    pass


search = qq_search
playlist = qq_playlist
