#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: kugou.py
@time: 2019-05-08
"""

import requests
from .. import config
from ..exceptions import RequestError, ResponseError, DataError
from ..song import BasicSong


class KugouSong(BasicSong):
    def __init__(self):
        super(KugouSong, self).__init__()
        self.hash = ""

    def download_lyrics(self):
        pass

    def download(self):
        params = {"cmd": "playInfo", "hash": self.hash}
        s = requests.Session()
        s.headers.update(config.get("fake_headers"))
        if config.get("proxies"):
            s.proxies.update(config.get("proxies"))
        s.headers.update(
            {"referer": "http://m.kugou.com", "User-Agent": config.get("ios_headers")}
        )

        r = s.get("http://m.kugou.com/app/i/getSongInfo.php", params=params)
        if r.status_code != requests.codes.ok:
            raise RequestError(r.text)
        j = r.json()
        if j["status"] != 1:
            raise ResponseError(r.text)
        self.song_url = j["url"]
        self.rate = j["bitRate"]
        self.ext = j["extName"]
        self.cover_url = j["album_img"].replace("{size}", "150")

        super(KugouSong, self).download()


def kugou_search(keyword) -> list:
    """ 搜索音乐 """
    number = config.get("number") or 5
    params = {
        "keyword": keyword,
        "platform": "WebFilter",
        "format": "json",
        "page": 1,
        "pagesize": number,
    }
    s = requests.Session()
    s.headers.update(config.get("fake_headers"))
    if config.get("proxies"):
        s.proxies.update(config.get("proxies"))
    s.headers.update({"referer": "http://www.kugou.com"})

    music_list = []
    r = s.get("http://songsearch.kugou.com/song_search_v2", params=params)
    if r.status_code != requests.codes.ok:
        raise RequestError(r.text)
    j = r.json()
    if j["status"] != 1:
        raise ResponseError(r.text)

    for m in j["data"]["lists"]:
        song = KugouSong()
        song.source = "kugou"
        song.id = m["Scid"]
        song.title = m["SongName"]
        song.singer = m["SingerName"]
        song.duration = m["Duration"]
        song.album = m["AlbumName"]
        song.size = round(m["FileSize"] / 1048576, 2)
        # 如果有更高品质的音乐选择高品质（尽管好像没什么卵用）
        if m["SQFileHash"] and m["SQFileHash"] != "00000000000000000000000000000000":
            song.hash = m["SQFileHash"]
        elif m["HQFileHash"] and m["HQFileHash"] != "00000000000000000000000000000000":
            song.hash = m["HQFileHash"]
        else:
            song.hash = m["FileHash"]

        music_list.append(song)

    return music_list


def kugou_playlist(url):
    pass


search = kugou_search
playlist = kugou_playlist
