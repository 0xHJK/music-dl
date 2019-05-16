#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: qq.py
@time: 2019-05-08
"""

import random
import requests
from .. import config
from ..exceptions import RequestError, ResponseError, DataError
from ..song import BasicSong


class QQSong(BasicSong):
    def __init__(self):
        super(QQSong, self).__init__()
        self.mid = ""

    def download_lyrics(self):
        pass

    def download_cover(self):
        pass

    def download(self):
        # 计算vkey
        guid = str(random.randrange(1000000000, 10000000000))
        params = {"guid": guid, "format": "json", "json": 3}
        s = requests.Session()
        s.headers.update(config.get("fake_headers"))
        if config.get("proxies"):
            s.proxies.update(config.get("proxies"))
        s.headers.update(
            {"referer": "http://y.qq.com", "User-Agent": config.get("ios_useragent")}
        )

        r = s.get(
            "http://base.music.qq.com/fcgi-bin/fcg_musicexpress.fcg", params=params
        )
        if r.status_code != requests.codes.ok:
            raise RequestError(r.text)
        j = r.json()
        if j["code"] != 0:
            raise ResponseError(r.text)

        vkey = j["key"]

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
    count = config.get("count") or 5
    params = {"w": keyword, "format": "json", "p": 1, "n": count}
    s = requests.Session()
    s.headers.update(config.get("fake_headers"))
    if config.get("proxies"):
        s.proxies.update(config.get("proxies"))
    s.headers.update(
        {"referer": "http://m.y.qq.com", "User-Agent": config.get("ios_useragent")}
    )

    music_list = []
    r = s.get("http://c.y.qq.com/soso/fcgi-bin/search_for_qq_cp", params=params)
    if r.status_code != requests.codes.ok:
        raise RequestError(r.text)
    j = r.json()
    if j["code"] != 0:
        raise ResponseError(r.text)

    for m in j["data"]["song"]["list"]:
        # 获得歌手名字
        singers = [s["name"] for s in m["singer"]]
        song = QQSong()
        song.source = "qq"
        song.id = m["songid"]
        song.title = m["songname"]
        song.singer = "、".join(singers)
        song.album = m["albumname"]
        song.duration = m["interval"]
        song.size = round(m["size128"] / 1048576, 2)
        # 特有字段
        song.mid = m["songmid"]

        music_list.append(song)

    return music_list


def qq_playlist(url):
    pass


search = qq_search
playlist = qq_playlist
