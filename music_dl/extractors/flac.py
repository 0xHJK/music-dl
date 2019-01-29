#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author: HJK
@file: flac.py
@time: 2019-01-25

从百度音乐获得flac无损音乐

"""

import requests
from .. import config
from ..exceptions import RequestError, ResponseError, DataError
from ..music import Music

__all__ = ["flac_search", "flac_download"]


def flac_search(keyword) -> list:
    """ 搜索无损音乐 """
    params = {"word": keyword, "version": "2", "from": 0}

    music_list = []
    r = requests.get(
        "http://sug.music.baidu.com/info/suggestion",
        params=params,
        proxies=config.get("proxies"),
    )
    if r.status_code != requests.codes.ok:
        raise RequestError(r.text)
    j = r.json()

    for m in j["data"]["song"]:
        music = Music()
        music.source = "flac"
        music.id = m["songid"]
        music.title = m["songname"]
        music.singer = m["artistname"]

        m_params = {"songIds": int(music.id), "type": "flac"}
        # 不在同一个session能提高请求成功率
        mr = requests.get(
            "http://music.baidu.com/data/music/fmlink",
            params=m_params,
            proxies=config.get("proxies"),
        )
        if mr.status_code != requests.codes.ok:
            raise RequestError(mr.text)
        mj = mr.json()
        if mj["errorCode"] != 22000 or not mj["data"]["songList"]:
            continue

        mj_music = mj["data"]["songList"][0]
        music.url = mj_music["songLink"]
        if not music.avaiable:
            continue
        music.duration = mj_music["time"]
        music.rate = mj_music["rate"]
        music.ext = mj_music["format"]
        music.album = mj_music["albumName"]
        music_list.append(music)

    return music_list


def flac_download(music):
    """ 从百度音乐下载无损音乐 """
    music.download()


search = flac_search
download = flac_download
