#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author: HJK
@file: kugou.py
@time: 2019-01-08

酷狗音乐搜索和下载

"""

import requests
from .. import config
from ..exceptions import RequestError, ResponseError, DataError
from ..music import Music

__all__ = ["kugou_search", "kugou_download"]


def kugou_search(keyword) -> list:
    """ 搜索音乐 """
    count = config.get("count") or 5
    params = {
        "keyword": keyword,
        "platform": "WebFilter",
        "format": "json",
        "page": 1,
        "pagesize": count,
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
        music = Music()
        music.source = "kugou"
        music.id = m["Scid"]
        music.title = m["SongName"]
        music.singer = m["SingerName"]
        music.duration = m["Duration"]
        music.album = m["AlbumName"]
        music.size = round(m["FileSize"] / 1048576, 2)
        # 如果有更高品质的音乐选择高品质（尽管好像没什么卵用）
        if m["SQFileHash"] and m["SQFileHash"] != "00000000000000000000000000000000":
            music.hash = m["SQFileHash"]
        elif m["HQFileHash"] and m["HQFileHash"] != "00000000000000000000000000000000":
            music.hash = m["HQFileHash"]
        else:
            music.hash = m["FileHash"]

        music_list.append(music)

    return music_list


def kugou_download(music):
    """ 根据hash从酷狗下载音乐 """
    params = {"cmd": "playInfo", "hash": music.hash}
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

    music.url = j["url"]
    music.rate = j["bitRate"]
    music.ext = j["extName"]

    music.download()


search = kugou_search
download = kugou_download
