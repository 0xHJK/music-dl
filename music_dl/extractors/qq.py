#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author: HJK
@file: qq.py
@time: 2019-01-09

QQ音乐搜索和下载

"""

import random
import requests
from .. import config
from ..exceptions import RequestError, ResponseError, DataError
from ..music import Music

__all__ = ["qq_search", "qq_download"]


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
        music = Music()
        music.source = "qq"
        music.id = m["songid"]
        music.title = m["songname"]
        music.singer = "、".join(singers)
        music.album = m["albumname"]
        music.duration = m["interval"]
        music.size = round(m["size128"] / 1048576, 2)
        # 特有字段
        music.mid = m["songmid"]

        music_list.append(music)

    return music_list


def qq_download(music):
    """ 根据songmid等信息获得下载链接 """
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

    r = s.get("http://base.music.qq.com/fcgi-bin/fcg_musicexpress.fcg", params=params)
    if r.status_code != requests.codes.ok:
        raise RequestError(r.text)
    j = r.json()
    if j["code"] != 0:
        raise ResponseError(r.text)

    vkey = j["key"]

    for prefix in ["M800", "M500", "C400"]:
        url = "http://dl.stream.qqmusic.qq.com/%s%s.mp3?vkey=%s&guid=%s&fromtag=1" % (
            prefix,
            music.mid,
            vkey,
            guid,
        )
        music.url = url
        if music.avaiable:
            music.rate = 320 if prefix == "M800" else 128
            break

    music.download()


search = qq_search
download = qq_download
