#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: baidu.py
@time: 2019-01-20

百度音乐搜索和下载

"""

import requests
from .. import config
from ..exceptions import RequestError, ResponseError, DataError
from ..music import Music

__all__ = ["baidu_search", "baidu_download"]


def baidu_search(keyword) -> list:
    """ 搜索音乐 """
    count = config.get("count") or 5
    params = {
        "query": keyword,
        "method": "baidu.ting.search.common",
        "format": "json",
        "page_no": 1,
        "page_size": count,
    }
    s = requests.Session()
    s.headers.update(config.get("fake_headers"))
    if config.get("proxies"):
        s.proxies.update(config.get("proxies"))
    s.headers.update({"referer": "http://music.baidu.com/"})

    music_list = []
    r = s.get("http://musicapi.qianqian.com/v1/restserver/ting", params=params)
    if r.status_code != requests.codes.ok:
        raise RequestError(r.text)
    j = r.json()

    for m in j["song_list"]:
        music = Music()
        music.source = "baidu"
        music.id = m["song_id"]
        music.title = m["title"].replace("<em>", "").replace("</em>", "")
        music.singer = m["author"].replace("<em>", "").replace("</em>", "")
        music.album = m["album_title"].replace("<em>", "").replace("</em>", "")

        s.headers.update({"referer": "http://music.baidu.com/song/" + music.id})
        m_params = {"songIds": music.id}
        mr = s.get("http://music.baidu.com/data/music/links", params=m_params)
        if mr.status_code != requests.codes.ok:
            raise RequestError(mr.text)
        mj = mr.json()
        if not mj["data"]["songList"]:
            continue

        mj_music = mj["data"]["songList"][0]
        music.url = mj_music["songLink"]
        if not music.avaiable:  # 如果URL拿不到内容
            continue
        music.duration = mj_music["time"]
        music.rate = mj_music["rate"]
        music.ext = mj_music["format"]
        music_list.append(music)

    return music_list


def baidu_download(music):
    """ 从百度音乐下载音乐 """
    music.download()


search = baidu_search
download = baidu_download
